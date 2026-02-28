from __future__ import annotations

import json
import time
import unicodedata
import urllib.request
from pathlib import Path

from .colors import DIM, GREEN, YELLOW


class VisualSimilarityChecker:
    """
    Unicode UTS #39 skeleton algorithm + Levenshtein edit distance.
    Source: https://www.unicode.org/Public/security/latest/confusables.txt
    """
    CONF_URL  = "https://www.unicode.org/Public/security/latest/confusables.txt"
    CONF_RAW  = "unicode_confusables.txt"
    CONF_JSON = "unicode_confusables_parsed.json"
    CONF_TTL  = 2_592_000   # 30 d

    def __init__(self, cache_dir: Path, force_refresh: bool = False):
        self.cache_dir     = cache_dir
        self.force_refresh = force_refresh
        self._cmap: dict[int, str] | None = None
        self._scache: dict[str, str]       = {}

    def _p(self, f): return self.cache_dir / f
    def _fresh(self, p, ttl):
        return p.exists() and not self.force_refresh and (time.time() - p.stat().st_mtime) < ttl

    def _load_confusables(self) -> dict[int, str]:
        jp = self._p(self.CONF_JSON)
        if self._fresh(jp, self.CONF_TTL):
            try:
                return {int(k): v for k, v in
                        json.loads(jp.read_text(encoding="utf-8")).items()}
            except Exception:
                pass
        rp = self._p(self.CONF_RAW)
        if not self._fresh(rp, self.CONF_TTL):
            print(DIM("  [similarity] Fetching Unicode confusables (UTS #39) …"),
                  end=" ", flush=True)
            try:
                req = urllib.request.Request(self.CONF_URL,
                      headers={"User-Agent": "gTLD-CollisionChecker/2.0"})
                with urllib.request.urlopen(req, timeout=30) as r:
                    data = r.read().decode("utf-8", errors="replace")
                rp.write_text(data, encoding="utf-8"); print(GREEN("ok"))
            except Exception as e:
                print(YELLOW(f"failed ({e})"))
                if not rp.exists(): return {}
        cmap: dict[int, str] = {}
        for line in rp.read_text(encoding="utf-8").splitlines():
            line = line.split("#")[0].strip()
            if not line: continue
            parts = [p.strip() for p in line.split(";")]
            if len(parts) < 2: continue
            try:
                cmap[int(parts[0], 16)] = "".join(
                    chr(int(cp, 16)) for cp in parts[1].split())
            except (ValueError, IndexError):
                continue
        try:
            jp.write_text(json.dumps({str(k): v for k, v in cmap.items()}),
                          encoding="utf-8")
        except Exception:
            pass
        return cmap

    def _ensure(self):
        if self._cmap is None:
            self._cmap = self._load_confusables()

    def skeleton(self, s: str) -> str:
        if s in self._scache: return self._scache[s]
        self._ensure()
        nfd    = unicodedata.normalize("NFD", s)
        parts  = [self._cmap.get(ord(ch), ch) if self._cmap else ch for ch in nfd]
        result = unicodedata.normalize("NFD", "".join(parts))
        self._scache[s] = result; return result

    @staticmethod
    def levenshtein(a: str, b: str) -> int:
        if a == b: return 0
        if abs(len(a) - len(b)) > 2: return 99
        if len(a) < len(b): a, b = b, a
        prev = list(range(len(b) + 1))
        for i, ca in enumerate(a, 1):
            curr = [i]
            for j, cb in enumerate(b, 1):
                curr.append(min(prev[j]+1, curr[-1]+1, prev[j-1]+(ca != cb)))
            prev = curr
        return prev[-1]

    def find_similar(self, s: str, targets: set[str], max_dist: int = 2) -> list[dict]:
        self._ensure()
        skel_s = self.skeleton(s)
        slen   = len(s)
        results: list[dict] = []
        for t in targets:
            if t == s: continue
            skel_match = (skel_s == self.skeleton(t)) if abs(slen - len(t)) <= 3 else False
            dist       = self.levenshtein(s, t) if abs(slen - len(t)) <= max_dist else 99
            if skel_match or dist <= max_dist:
                results.append({"target": t, "distance": dist, "skeleton_match": skel_match})
        results.sort(key=lambda x: (not x["skeleton_match"], x["distance"], x["target"]))
        return results

    def check(self, s: str, db: "CollisionDatabase") -> dict:
        collision: list[dict] = []
        sse:       list[dict] = []

        for m in self.find_similar(s, set(db.prior_high_risk.keys()), max_dist=2):
            score = 70 if m["skeleton_match"] else 50 if m["distance"] == 1 else 28
            collision.append({**m, "category": "Prior High-Risk String", "score": score,
                               "guidebook": "§7.7.1 / 2012 Round"})
        curated = (set(db.enterprise) | set(db.home_labels) | set(db.mail_labels)
                   ) - set(db.prior_high_risk.keys())
        for m in self.find_similar(s, curated, max_dist=1)[:4]:
            collision.append({**m, "category": "Curated Leakage Label",
                               "score": 38 if m["skeleton_match"] else 22,
                               "guidebook": "NCAP Study Two / §7.7.2"})
        for m in self.find_similar(s, db.delegated_tlds, max_dist=1)[:5]:
            sse.append({**m, "category": "Existing Delegated TLD",
                        "outcome": "Application cannot proceed (§7.10 Table 7-5)",
                        "guidebook": "§7.10.3.1"})
        sse_blocked = {k for k, v in db.blocked_names.items()
                       if v["category"] in ("icann_iana_ietf_infrastructure", "protocol_reserved")}
        for m in self.find_similar(s, sse_blocked, max_dist=1)[:3]:
            sse.append({**m, "category": "ICANN Blocked Name",
                        "outcome": "Application will not proceed (§7.10.3.6)",
                        "guidebook": "§7.10.3.6"})
        return {"collision_risks": collision, "sse_risks": sse}

    def status(self) -> dict:
        p = self._p(self.CONF_RAW)
        return {"desc": "Unicode Confusables — UTS #39 (unicode.org/Public/security/latest/)",
                "url":  self.CONF_URL,
                "age_s": int(time.time()-p.stat().st_mtime) if p.exists() else None,
                "size": p.stat().st_size if p.exists() else 0,
                "fresh": self._fresh(p, self.CONF_TTL)}
