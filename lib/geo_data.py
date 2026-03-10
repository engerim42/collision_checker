"""
Geographic reference data for §7.5 Geographic Names Review.

UN M.49 macro-geographic regions and sub-regions
-------------------------------------------------
Source: UN Statistics Division M.49 Standard
        https://unstats.un.org/unsd/methodology/m49/
ICANN treatment (§7.5.2 / §7.5.3): Applications for UN macro-geographic region
names will not be approved.  Sub-region and other geographic terms may still
trigger a Geographic Names Review even when not automatically blocked.

World cities
------------
Source: world-cities.json (GeoNames, cities > 15 000 population).
ICANN treatment (§7.5.3): Not automatically blocked, but §7.5 review applies.
Applicants must demonstrate support from the relevant government(s) or community.

Unicode / IDN handling
----------------------
Each city name generates up to four lookup variants so that both the Unicode
form and the ASCII transliteration are caught:

  München  → münchen  (Unicode TLD), munchen  (ASCII approximation)
  Zürich   → zürich,  zurich
  São Paulo→ são paulo, saopaulo, sao paulo, saopaulo  (+ space-stripped)
  Kuala Lumpur → kuala lumpur, kualalumpur

Non-decomposable characters (ł, ø, ß, etc.) are handled via an explicit
transliteration supplement applied before the NFD strip.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

# ── Religious / sacred sites — §4.5.1.2 Community Objection risk ─────────────
# These sites carry community objection standing from their respective religious
# communities.  They are not automatically blocked, but §7.5.3 Geographic Names
# Review applies and a §4.5.1.2 Community Objection is almost certain.
# Sources: UNWTO Sacred Sites Programme; ICOMOS; WIPO Traditional Knowledge DB;
#          ICANN 2012-round community objection precedents.
SACRED_SITES: dict[str, str] = {
    # Islam
    "mecca":        "Mecca (Makkah al-Mukarramah), Saudi Arabia — holiest city in Islam",
    "makkah":       "Makkah al-Mukarramah, Saudi Arabia — holiest city in Islam",
    "medina":       "Medina (Al-Madinah al-Munawwarah), Saudi Arabia — second holiest city in Islam",
    "kaaba":        "Kaaba, Mecca — most sacred structure in Islam",
    # Judaism / Christianity / Islam
    "jerusalem":    "Jerusalem — holy city for Judaism, Christianity, and Islam (§7.5.1 / §7.5.3)",
    # Hinduism
    "varanasi":     "Varanasi (Benares/Kashi), India — holiest city in Hinduism",
    "vrindavan":    "Vrindavan, India — sacred Hindu site associated with Krishna",
    "tirupati":     "Tirupati, India — most visited Hindu pilgrimage site",
    "haridwar":     "Haridwar, India — major Hindu pilgrimage city on the Ganges",
    "ayodhya":      "Ayodhya, India — sacred Hindu city, traditional birthplace of Rama",
    # Buddhism
    "lumbini":      "Lumbini, Nepal — birthplace of Gautama Buddha (UNESCO World Heritage)",
    "bodhgaya":     "Bodh Gaya, India — site of the Buddha's enlightenment (UNESCO)",
    # Christianity
    "vatican":      "Vatican City — seat of the Roman Catholic Church; also a state name",
    "lourdes":      "Lourdes, France — major Catholic Marian pilgrimage site",
    "fatima":       "Fátima, Portugal — major Catholic pilgrimage site",
    "assisi":       "Assisi, Italy — birthplace of St Francis; major Catholic pilgrimage city",
    "medjugorje":   "Medjugorje, Bosnia-Herzegovina — major Catholic pilgrimage site",
    # Sikhism
    "amritsar":     "Amritsar, India — location of the Golden Temple (Harmandir Sahib), holiest Sikh site",
    # Mormonism
    "nauvoo":       "Nauvoo, Illinois, USA — historic Latter-day Saints pilgrimage site",
}

# ── UN M.49 Macro-geographic regions — §7.5.2 hard-stop ─────────────────────
UN_MACRO_REGIONS: frozenset[str] = frozenset({
    "africa",
    "americas",
    "asia",
    "europe",
    "oceania",
    "antarctica",
})

# ── UN M.49 Sub-regions & geographic groupings — §7.5 advisory flag ──────────
UN_SUBREGIONS: frozenset[str] = frozenset({
    "caribbean",
    "melanesia",
    "micronesia",
    "polynesia",
    "australasia",
})

# Combined for fast lookup
UN_REGIONS: frozenset[str] = UN_MACRO_REGIONS | UN_SUBREGIONS


# ── City name normalisation ───────────────────────────────────────────────────

# Characters that NFD decomposition cannot strip (no canonical base + combining
# mark split). Map to their closest ASCII equivalents.
_SUPPLEMENT = str.maketrans({
    'ł': 'l',  'ø': 'o',  'đ': 'd',  'ı': 'i',
    'æ': 'ae', 'œ': 'oe', 'ß': 'ss', 'þ': 'th', 'ð': 'd',
    'ħ': 'h',  'ŋ': 'n',  'ŧ': 't',
})

_SPACE_RE = re.compile(r"[\s\-\u2019']+")


def _city_variants(name: str) -> set[str]:
    """
    Return up to four normalised lookup forms for a city name:

      1. Unicode lowercase                      e.g. "münchen"
      2. Unicode lowercase, spaces stripped     e.g. "kualalumpur"
      3. ASCII transliteration                  e.g. "munchen"
      4. ASCII transliteration, spaces stripped e.g. "saopaulo"
    """
    variants: set[str] = set()
    n = name.lower().strip()
    if not n:
        return variants

    def _add(s: str) -> None:
        s = s.strip()
        if len(s) >= 3:
            variants.add(s)
            variants.add(_SPACE_RE.sub('', s))

    # Unicode form
    _add(n)

    # ASCII form via supplement table + NFD + strip combining marks
    supplemented = n.translate(_SUPPLEMENT)
    nfd = unicodedata.normalize('NFD', supplemented)
    ascii_form = ''.join(
        c for c in nfd
        if unicodedata.category(c) != 'Mn' and ord(c) < 128
    ).strip()
    if ascii_form and ascii_form != n:
        _add(ascii_form)

    return variants


def load_world_cities(json_path: Path) -> dict[str, str]:
    """
    Load *json_path* (world-cities.json format) and return a dict mapping
    every normalised lookup form → canonical "City, Country" display label.

    Multiple cities may share a normalised form; ``setdefault`` keeps the
    first (alphabetically earlier in the file) to avoid overwriting.
    """
    try:
        raw = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception:
        return {}

    columns = raw.get("columns", [])
    try:
        name_idx    = columns.index("name")
        country_idx = columns.index("country")
    except ValueError:
        return {}

    result: dict[str, str] = {}
    for row in raw.get("data", []):
        name    = row[name_idx]
        country = row[country_idx]
        label   = f"{name}, {country}"
        for variant in _city_variants(name):
            result.setdefault(variant, label)

    return result
