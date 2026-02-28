#!/usr/bin/python3

"""
gTLD Name Collision Likelihood Checker
========================================
Based on ICANN New gTLD Program 2026 Applicant Guidebook (§7.2.1, §7.5, §7.7, §7.10, §4.5.1.1)
and the Name Collision Analysis Project (NCAP) Study Two Report (Apr 2024).

Usage:
  python collision_checker.py              # interactive
  python collision_checker.py corp home    # batch
  python collision_checker.py corp --html  # batch + write HTML report
  python collision_checker.py --refresh    # force-refresh all caches

Directory layout:
  collision_checker.py
  lib/
    colors.py          ANSI colour helpers
    seed.py            Bundled reference data (high-risk strings, blocked/reserved names)
    aural.py           AuralSimilarityChecker  (Double Metaphone + Soundex)
    visual.py          VisualSimilarityChecker (Unicode UTS #39 + Levenshtein)
    ithi.py            ITHIClient              (ITHI M4 root-leakage data)
    fetcher.py         ResourceFetcher         (HTTP caching layer)
    database.py        CollisionDatabase       (aggregates all datasets)
    assessor.py        RiskAssessor            (scoring pipeline)
    display.py         Terminal output helpers
    html_report.py     Self-contained HTML report generator
  data/
    prior_high_risk.json       NCAP/2012-round confirmed high-risk strings
    enterprise_labels.json     AD/corporate namespace leakage labels
    home_labels.json           Home-network / IoT leakage labels
    mail_labels.json           Mail-infrastructure leakage labels
    reserved_blocked.json      §7.2.1 Blocked Names
    reserved_igo.json          §7.2.2 Reserved Names (IGO/INGO/IOC/RCRC)
  .cache/
    iana_tlds.txt                    IANA Root Zone TLD list             TTL 24 h
    special_use.csv                  IANA Special-Use names              TTL  7 d
    public_suffix_list.dat           Mozilla PSL                         TTL 24 h
    lang_subtags.txt                 IANA Language Subtag Registry       TTL  7 d
    iso3166_all.csv                  ISO 3166-1 codes & names            TTL  7 d
    ithi_index.json                  ITHI M4 index                       TTL 24 h
    ithi_m4_<YYYY-MM>.csv            ITHI M4 leakage data                TTL  7 d
    unicode_confusables.txt          Unicode UTS #39 confusables         TTL 30 d
    unicode_confusables_parsed.json  Parsed confusables cache            TTL 30 d
"""

import sys
from pathlib import Path

from lib.assessor import RiskAssessor
from lib.colors import BOLD, GREEN
from lib.database import CollisionDatabase
from lib.display import print_report, print_status
from lib.fetcher import ResourceFetcher


def main():
    base     = Path(__file__).parent
    refresh  = "--refresh" in sys.argv
    html_out = "--html" in sys.argv
    args     = [a for a in sys.argv[1:] if not a.startswith("--")]

    fetcher  = ResourceFetcher(base, force_refresh=refresh)
    db       = CollisionDatabase(base, fetcher)
    assessor = RiskAssessor(db)

    if args:
        results = [assessor.assess(a) for a in args]
        for r in results:
            print_report(r)
        if html_out:
            from lib.html_report import render_html
            fname = f"{args[0]}_report.html" if len(args) == 1 else "collision_report.html"
            (base / fname).write_text(render_html(results), encoding="utf-8")
            print(GREEN(f"  HTML report written to {fname}\n"))
        return

    print(BOLD("\n  gTLD Collision Checker  —  type a string to assess, 'status', 'refresh', or 'quit'\n"))
    while True:
        try:
            raw = input(BOLD("  › ")).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Goodbye."); break
        cmd = raw.lower()
        if not raw: continue
        if cmd in ("quit", "exit", "q"): print("  Goodbye."); break
        if cmd == "status": print_status(fetcher, db); continue
        if cmd == "refresh":
            fetcher.force_refresh = fetcher.ithi.force_refresh = True
            fetcher.similarity.force_refresh = True
            db.reload()
            fetcher.force_refresh = fetcher.ithi.force_refresh = False
            fetcher.similarity.force_refresh = False
            print(GREEN("  Sources refreshed.\n")); continue
        print_report(assessor.assess(raw))


if __name__ == "__main__":
    main()
