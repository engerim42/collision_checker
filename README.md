# gTLD Application Risk Checker
> **Current Version: 1.0.2**

Assesses proposed new gTLD strings against ICANN eligibility rules and name
collision risk factors, based on the 2026 Applicant Guidebook and the NCAP
Study Two Report (Apr 2024). Produces an **Application Risk Report** covering
eligibility hard stops, collision leakage scoring, and an Overall Verdict.

## Requirements

Python 3.10 or later. No third-party packages required.

## Usage

```
# Interactive mode — enter strings one at a time
python3 collision_checker.py

# Batch mode — assess one or more strings
python3 collision_checker.py corp home mail

# Write a self-contained HTML report alongside terminal output
python3 collision_checker.py corp --html
python3 collision_checker.py corp home mail --html

# Force-refresh all cached remote data
python3 collision_checker.py --refresh
```

`--html` writes `<string>_report.html` for a single string, or
`collision_report.html` when assessing multiple strings at once.

Inside the interactive prompt:

| Command   | Action                              |
|-----------|-------------------------------------|
| `<string>` | Assess that string                 |
| `status`  | Show cache freshness and dataset sizes |
| `refresh` | Re-fetch all remote sources         |
| `quit`    | Exit                                |

## What it checks

**Eligibility (hard stops)**
- Existing delegated TLDs (IANA root zone)
- IETF Special-Use Domain Names (RFC 6761 / 2606 / 7686)
- ICANN Blocked Names (§7.2.1)
- ISO 3166-1 country codes and country names (§7.5.1)
- ICANN Reserved Names — IGO/INGO/IOC/RCRC (§7.2.2)

**Collision risk scoring (§7.7)**
- ITHI M4 live root-server leakage data
- NCAP Study Two curated high-risk string sets (enterprise, home-network, mail)
- Mozilla Public Suffix List (private domains section)
- Visual similarity via Unicode UTS #39 skeleton + Levenshtein distance (§7.10)
- Aural similarity via Double Metaphone + Soundex (§4.5.1.1 SCO risk)
- Semantic / translation check — detects translations of high-risk concepts (e.g.
  "maison" → "home", "correo" → "mail") across 30+ languages
- Singular/plural pair detection — flags strings that are the singular or plural of a
  known high-risk or delegated label (§4.4.3 notification risk)

**Geographic names (§7.5)**
- ISO 3166-1 country codes and names → hard stop (§7.5.1)
- UN M.49 macro-geographic region names (Africa, Americas, Asia, Europe, Oceania,
  Antarctica) → reserved, application will not be approved (§7.5.2)
- UN M.49 sub-regional names (Caribbean, Melanesia, Micronesia, Polynesia,
  Australasia) → advisory flag
- ~160 world capital cities → advisory flag with §7.5.3 guidance

## File layout

```
collision_checker.py      Entry point
lib/
  colors.py               ANSI colour helpers
  seed.py                 Bundled reference data
  aural.py                AuralSimilarityChecker
  visual.py               VisualSimilarityChecker
  ithi.py                 ITHIClient
  fetcher.py              ResourceFetcher (HTTP + disk cache)
  database.py             CollisionDatabase
  assessor.py             RiskAssessor (scoring pipeline)
  display.py              Terminal output (Application Risk Report)
  html_report.py          Self-contained HTML report generator
  singular_plural.py      Singular/plural pair detection (§4.4.3)
  semantic.py             Semantic/translation similarity (30+ languages)
  geo_data.py             Bundled UN macro/sub-region lists; loads world-cities.json
  world-cities.json       Bundled city dataset — all cities > 15 000 population (geonames.org)
  common-strings.json     Bundled common brand strings found in WIPO db and global zone files
tests/                    Unit tests (no network required)
data/                     Local JSON reference files (auto-created on first run)
.cache/                   Cached remote files (auto-managed, TTL-based)
```

## Cache TTLs

| File | Source | TTL |
|------|--------|-----|
| `iana_tlds.txt` | IANA Root Zone | 24 h |
| `special_use.csv` | IANA Special-Use Registry | 7 d |
| `public_suffix_list.dat` | Mozilla PSL | 24 h |
| `lang_subtags.txt` / `iso3166_all.csv` | IANA / GitHub | 7 d |
| `ithi_m4_*.csv` | ITHI M4 | 7 d |
| `unicode_confusables.txt` | Unicode UTS #39 | 30 d |

Run with `--refresh` to bypass all TTLs and re-fetch everything immediately.

## Bundled data sources

The following files ship with the tool and are never fetched remotely:

| File | Description | Source |
|------|-------------|--------|
| `lib/world-cities.json` | All cities with population > 15 000 | [GeoNames](https://www.geonames.org/) |
| `lib/data/prior_high_risk.json` | 2012-round confirmed HIGH-risk strings (corp, home, mail) | ICANN NCAP |
| `lib/data/enterprise_labels.json` | Corporate/AD namespace leakage labels | NCAP Study Two |
| `lib/data/home_labels.json` | Home-network / IoT leakage labels | NCAP Study Two |
| `lib/data/mail_labels.json` | Mail-infrastructure leakage labels | NCAP Study Two |
| `lib/data/reserved_blocked.json` | §7.2.1 Blocked Names | ICANN Guidebook 2026 |
| `lib/data/reserved_igo.json` | §7.2.2 Reserved Names (IGO/INGO/IOC/RCRC) | ICANN Guidebook 2026 |
