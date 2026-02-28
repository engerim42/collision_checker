from __future__ import annotations

import json
from pathlib import Path

from .colors import DIM, YELLOW
from .fetcher import ResourceFetcher
from .geo_data import UN_MACRO_REGIONS, UN_REGIONS, load_world_cities
from .seed import _SEED


class CollisionDatabase:
    def __init__(self, base_dir: Path, fetcher: ResourceFetcher):
        self.data_dir = base_dir / "data"; self.data_dir.mkdir(parents=True, exist_ok=True)
        self.fetcher = fetcher; self._ensure_data_files(); self._load()

    def _ensure_data_files(self):
        for fname, content in _SEED.items():
            p = self.data_dir / fname
            if not p.exists(): p.write_text(json.dumps(content, indent=2), encoding="utf-8")

    def _load_json(self, fname):
        try: return json.loads((self.data_dir / fname).read_text(encoding="utf-8"))
        except Exception as e: print(YELLOW(f"  [warn] {fname}: {e}")); return {}

    @staticmethod
    def _flatten(data):
        result = {}
        for cat_key, cat in data.get("categories", {}).items():
            meta = {"category": cat_key, "desc": cat.get("desc", cat_key), "source": cat.get("source", "—")}
            for s in cat.get("strings", []): result[s.lower()] = meta
        return result

    def _load(self):
        self.prior_high_risk = self._load_json("prior_high_risk.json").get("strings", {})
        self.enterprise      = self._load_json("enterprise_labels.json").get("strings", {})
        self.home_labels     = self._load_json("home_labels.json").get("strings", {})
        self.mail_labels     = self._load_json("mail_labels.json").get("strings", {})
        self.history_2012    = self._load_json("history_2012.json").get("strings", {})
        self.blocked_names   = self._flatten(self._load_json("reserved_blocked.json"))
        self.reserved_names  = self._flatten(self._load_json("reserved_igo.json"))
        print(DIM("  [db] Loading network sources …"))
        self.delegated_tlds = self.fetcher.get_delegated_tlds()
        self.special_use    = self.fetcher.get_special_use_names()
        self.psl_private    = self.fetcher.get_psl_private_labels()
        self.iso_codes, self.iso_names = self.fetcher.get_iso3166_data()
        self.un_regions    = UN_REGIONS
        self.un_macro      = UN_MACRO_REGIONS
        _cities_json = Path(__file__).parent / "world-cities.json"
        self.cities = load_world_cities(_cities_json)

    def reload(self): self._load()

    def is_delegated(self, s):   return s in self.delegated_tlds
    def is_special_use(self, s): return s in self.special_use
    def is_psl_private(self, s): return s in self.psl_private
    def is_blocked(self, s):     return s in self.blocked_names
    def is_reserved(self, s):    return s in self.reserved_names
    def is_iso_code(self, s):    return s in self.iso_codes
    def is_iso_name(self, s):    return s in self.iso_names
    def is_un_region(self, s):   return s in self.un_regions
    def is_un_macro(self, s):    return s in self.un_macro
    def is_city(self, s):        return s in self.cities
    def get_city(self, s):       return self.cities.get(s)   # returns "City, Country" or None

    def get_curated_entry(self, s):
        for cat, store in (("Prior High-Risk (2012 Round)", self.prior_high_risk),
                           ("Enterprise Namespace Leakage", self.enterprise),
                           ("Home Network / IoT Leakage",   self.home_labels),
                           ("Mail Infrastructure Leakage",  self.mail_labels)):
            if s in store: return cat, store[s]
        return None, {}

    def data_file_meta(self):
        rows = []
        for fname in _SEED:
            data = self._load_json(fname)
            n = len(data.get("strings", {})) or sum(
                len(c.get("strings", [])) for c in data.get("categories", {}).values())
            rows.append({"file": fname, "strings": n,
                         "source": data.get("_meta", {}).get("source", "—")})
        return rows
