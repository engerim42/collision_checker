from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path

from .colors import DIM, GREEN, YELLOW


class ITHIClient:
    """
    Fetches ITHI M4 root-server leakage data from ithi.research.icann.org.

    The ITHI website previously published monthly per-label CSV files at
    /data/M4/ITHI-M4-YYYY-MM.csv.  Those files were retired and the path
    now returns HTTP 404.  M4 data is now served as a single JSON file at
    /M4Data.txt, containing two datasets:

      M42DataSet — top leaking TLD labels at the root (e.g. LOCAL, ONION)
      M43DataSet — leakage by category label  (e.g. HOME, CORP, MAIL)

    Each entry is [label, [monthly_pct_values…]].  Only ~28 labels are
    tracked (vs thousands in the old CSV), and the series is currently
    frozen at 2023/06 on the ITHI side.  The tool uses the last non-zero
    value from each series as the current leakage percentage.
    """

    BASE   = "https://ithi.research.icann.org"
    M4_URL = f"{BASE}/M4Data.txt"

    def __init__(self, cache_dir: Path, force_refresh: bool = False):
        self.cache_dir     = cache_dir
        self.force_refresh = force_refresh
        self._leakage: dict[str, dict] | None = None

    @staticmethod
    def _get(url, timeout=20):
        req = urllib.request.Request(
            url, headers={"User-Agent": "gTLD-CollisionChecker/2.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")

    def _p(self, f): return self.cache_dir / f

    def _fresh(self, p, ttl):
        return p.exists() and not self.force_refresh and \
               (time.time() - p.stat().st_mtime) < ttl

    def _load_m4(self) -> dict[str, dict]:
        path = self._p("ithi_m4data.json")
        if not self._fresh(path, 86_400):          # refresh once per day
            print(DIM("  [ITHI] Fetching M4Data.txt …"), end=" ", flush=True)
            try:
                raw = self._get(self.M4_URL, timeout=30)
                path.write_text(raw, encoding="utf-8")
                print(GREEN("ok"))
            except Exception as e:
                print(YELLOW(f"failed ({e})"))
                if not path.exists():
                    return {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(YELLOW(f"  [ITHI] Read error: {e}"))
            return {}
        return self._parse(data)

    def _parse(self, data: dict) -> dict[str, dict]:
        result: dict[str, dict] = {}
        try:
            month = str(data.get("date", "unknown"))
            rows: list[tuple[str, float]] = []
            for key in ("M42DataSet", "M43DataSet"):
                for entry in data.get(key, []):
                    label, series = entry[0], entry[1]
                    lbl = label.lower().strip().lstrip(".")
                    # Last non-zero value is the most representative recent reading
                    pct = next((v for v in reversed(series) if v > 0), 0.0)
                    rows.append((lbl, pct))
            rows.sort(key=lambda x: x[1], reverse=True)
            n = len(rows)
            for rank, (lbl, pct) in enumerate(rows, 1):
                result[lbl] = {
                    "pct":   round(pct, 6),
                    "rank":  rank,
                    "total": n,
                    "month": month,
                }
        except Exception as e:
            print(YELLOW(f"  [ITHI] Parse error: {e}"))
        return result

    def lookup(self, label: str) -> dict | None:
        if self._leakage is None:
            self._leakage = self._load_m4()
        e = self._leakage.get(label.lower().lstrip("."))
        if not e:
            return None
        n        = len(self._leakage)
        pct_rank = 1 - (e["rank"] - 1) / max(n - 1, 1)
        score    = (95 if pct_rank >= 0.99 else 85 if pct_rank >= 0.95 else
                    75 if pct_rank >= 0.90 else 60 if pct_rank >= 0.75 else
                    40 if pct_rank >= 0.50 else 20 if pct_rank >= 0.25 else 10)
        return {**e, "score": score, "pct_rank": round(pct_rank * 100, 1)}

    def status(self) -> dict:
        path = self._p("ithi_m4data.json")
        return {
            "desc":    "ITHI M4 Root Leakage (ithi.research.icann.org/M4Data.txt)",
            "url":     self.M4_URL,
            "age_s":   int(time.time() - path.stat().st_mtime) if path.exists() else None,
            "size":    path.stat().st_size if path.exists() else 0,
            "fresh":   self._fresh(path, 86_400) if path.exists() else False,
            "records": len(self._leakage) if self._leakage is not None else "not loaded",
        }
