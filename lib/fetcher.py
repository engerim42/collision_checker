from __future__ import annotations

import csv
import time
import urllib.request
from io import StringIO
from pathlib import Path

from .aural import AuralSimilarityChecker
from .colors import DIM, GREEN, YELLOW
from .ithi import ITHIClient
from .visual import VisualSimilarityChecker


class ResourceFetcher:
    SOURCES: dict[str, dict] = {
        "iana_tlds":    {"url": "https://data.iana.org/TLD/tlds-alpha-by-domain.txt",
                         "file": "iana_tlds.txt", "ttl": 86_400,
                         "desc": "IANA Root Zone TLD List"},
        "special_use":  {"url": ("https://www.iana.org/assignments/special-use-domain-names/"
                                 "special-use-domain.csv"),
                         "file": "special_use.csv", "ttl": 604_800,
                         "desc": "IANA Special-Use Domain Names (RFC 6761/2606)"},
        "public_suffix": {"url": "https://publicsuffix.org/list/public_suffix_list.dat",
                          "file": "public_suffix_list.dat", "ttl": 86_400,
                          "desc": "Mozilla Public Suffix List"},
        "lang_subtags": {"url": ("https://www.iana.org/assignments/language-subtag-registry/"
                                 "language-subtag-registry"),
                         "file": "lang_subtags.txt", "ttl": 604_800,
                         "desc": "IANA Language Subtag Registry (ISO 3166-1 codes & names)"},
        "iso3166_csv":  {"url": ("https://raw.githubusercontent.com/lukes/"
                                 "ISO-3166-Countries-with-Regional-Codes/master/all/all.csv"),
                         "file": "iso3166_all.csv", "ttl": 604_800,
                         "desc": "ISO 3166-1 Codes & Names (alpha-2/3, names)"},
    }

    def __init__(self, base_dir: Path, force_refresh: bool = False):
        self.cache_dir = base_dir / ".cache"; self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.force_refresh = force_refresh; self._memo: dict[str, str] = {}
        self.ithi       = ITHIClient(self.cache_dir, force_refresh)
        self.similarity = VisualSimilarityChecker(self.cache_dir, force_refresh)
        self.aural      = AuralSimilarityChecker()

    def fetch(self, key):
        if key in self._memo: return self._memo[key]
        src = self.SOURCES[key]; path = self.cache_dir / src["file"]
        age = time.time() - path.stat().st_mtime if path.exists() else float("inf")
        if self.force_refresh or age > src["ttl"]:
            print(DIM(f"  [fetch] {src['desc']} …"), end=" ", flush=True)
            try:
                req = urllib.request.Request(src["url"],
                      headers={"User-Agent": "gTLD-CollisionChecker/2.0"})
                with urllib.request.urlopen(req, timeout=15) as r:
                    data = r.read().decode("utf-8", errors="replace")
                path.write_text(data, encoding="utf-8"); print(GREEN("ok"))
            except Exception as e:
                print(YELLOW(f"failed ({e})"))
                data = path.read_text(encoding="utf-8") if path.exists() else ""
        else:
            data = path.read_text(encoding="utf-8")
        self._memo[key] = data; return data

    def source_status(self):
        rows = []
        for src in self.SOURCES.values():
            p = self.cache_dir / src["file"]
            rows.append({"desc": src["desc"], "url": src["url"],
                         "age_s": int(time.time()-p.stat().st_mtime) if p.exists() else None,
                         "size": p.stat().st_size if p.exists() else 0,
                         "fresh": p.exists() and (time.time()-p.stat().st_mtime) < src["ttl"]})
        rows.append(self.ithi.status())
        rows.append(self.similarity.status())
        rows.append(AuralSimilarityChecker.status())
        return rows

    def get_delegated_tlds(self):
        return frozenset(l.strip().lower() for l in self.fetch("iana_tlds").splitlines()
                         if l.strip() and not l.startswith("#"))

    def get_special_use_names(self):
        names = {"local", "localhost", "example", "test", "invalid", "onion",
                 "home.arpa", "internal", "alt", "localdomain"}
        try:
            for row in csv.DictReader(StringIO(self.fetch("special_use"))):
                n = (row.get("Name") or next(iter(row.values()), "")).strip().lower().lstrip(".")
                if n: names.add(n.split(".")[-1]); names.add(n)
        except Exception:
            pass
        return frozenset(names)

    def get_psl_private_labels(self):
        names, in_priv = set(), False
        for line in self.fetch("public_suffix").splitlines():
            line = line.strip()
            if "BEGIN PRIVATE DOMAINS" in line: in_priv = True; continue
            if "END PRIVATE DOMAINS" in line: break
            if not in_priv or not line or line.startswith("//"): continue
            lbl = line.lstrip("*.").split(".")[0].lower()
            if lbl: names.add(lbl)
        return frozenset(names)

    def get_iso3166_data(self):
        codes, names = set(), set()
        raw = self.fetch("lang_subtags")
        for record in raw.replace("\r\n", "\n").split("\n%%\n"):
            fields: dict[str, str] = {}; cur = None
            for line in record.splitlines():
                if not line: continue
                if line[0].isspace() and cur: fields[cur] += " " + line.strip()
                elif ": " in line: cur, val = line.split(": ", 1); fields[cur] = val
            if fields.get("Type") == "region":
                sub = fields.get("Subtag", "").lower(); desc = fields.get("Description", "").lower()
                if len(sub) == 2: codes.add(sub)
                if desc: names.add(desc)
        try:
            for row in csv.DictReader(StringIO(self.fetch("iso3166_csv"))):
                a2 = row.get("alpha-2", "").strip().lower(); a3 = row.get("alpha-3", "").strip().lower()
                nm = row.get("name", "").strip().lower()
                if a2: codes.add(a2)
                if a3: codes.add(a3)
                if nm: names.add(nm)
        except Exception:
            pass
        return frozenset(codes), frozenset(names)
