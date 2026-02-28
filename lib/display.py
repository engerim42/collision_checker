from __future__ import annotations

import textwrap
from typing import TYPE_CHECKING

from .colors import BOLD, CYAN, DIM, GREEN, RED, YELLOW

if TYPE_CHECKING:
    from .database import CollisionDatabase
    from .fetcher import ResourceFetcher

W = 74


def _build_verdict(r: dict, colour) -> list[str]:
    """Synthesise all risk signals into a final ordered verdict list."""
    sse_risks  = r.get("sse_risks", [])
    has_sco    = bool(r.get("sco_risks"))
    has_geo    = bool(r.get("geo_flag"))
    has_plural = bool(r.get("plural_risks"))
    lro_risks  = r.get("lro_risks", [])
    lpi_risks  = r.get("lpi_risks", [])
    h12        = r.get("history_2012")
    score      = r["score"]

    # Split SSE hits: matches against already-delegated TLDs are confirmed blocks
    # (§7.10 Table 7-5 leaves no discretion); others are panel-dependent risks.
    sse_confirmed = [m for m in sse_risks if "Delegated" in m.get("category", "")]
    sse_risk_only = [m for m in sse_risks if m not in sse_confirmed]

    items: list[str] = []

    # 1 — SSE first: if any match is against a delegated TLD the application
    #     is already blocked — no panel needed, §7.10 Table 7-5 is deterministic.
    if sse_confirmed:
        targets = ", ".join(f".{m['target'].upper()}" for m in sse_confirmed)
        items.append(
            f"APPLICATION CANNOT PROCEED — §7.10 Table 7-5: confusingly similar "
            f"(edit-distance ≤1 / skeleton match) to {targets}, already delegated in "
            f"the IANA root zone. This is not a panel risk — the §7.10 outcome is "
            f"predetermined. Filing fees are non-refundable once submitted."
        )
    elif sse_risk_only:
        targets = ", ".join(f".{m['target'].upper()}" for m in sse_risk_only)
        items.append(
            f"HARD STOP RISK (§7.10 SSE): confusingly similar to {targets}. "
            f"A positive SSE Panel finding will prevent this application from proceeding "
            f"regardless of the collision score. Resolve before committing fees."
        )

    # 2 — Collision leakage score (§7.7 — separate from §7.10 SSE above)
    if score >= 85:
        items.append(
            f"Collision leakage risk is HIGH ({score}/100): almost certain to appear on "
            "the Collision String List. A High-Risk Mitigation Plan (§7.7.5) and an "
            "additional application fee are mandatory."
        )
    elif score >= 55:
        items.append(
            f"Collision leakage risk is MODERATE ({score}/100): significant leakage "
            "signals detected. Temporary Delegation data (§7.7.3) will be decisive — "
            "proactively gather ITHI M4 evidence before filing."
        )
    elif score >= 25:
        items.append(
            f"Collision leakage risk is LOW-MODERATE ({score}/100): some signals present. "
            "Standard §7.7 assessment and Temporary Delegation timeline apply."
        )
    else:
        if sse_risks:
            items.append(
                f"Collision leakage risk is LOW ({score}/100): no match in DNS leakage "
                "datasets or NCAP categories. Note: the §7.10 SSE visual match above is "
                "a separate barrier and does not affect the §7.7 leakage score."
            )
        else:
            items.append(
                f"Collision leakage risk is LOW ({score}/100): no match in known leakage "
                "datasets, NCAP categories, visual/aural similarity, or PSL private domains. "
                "Obtain ICANN's pre-application longitudinal dataset (§7.7.1) when published."
            )

    # 3 — geographic barrier
    if has_geo:
        items.append(
            "GEOGRAPHIC BARRIER (§7.5.3): this string identifies a city or geographic "
            "region. Approval requires documented government support or a demonstrated "
            "legitimate community sponsorship — typically the decisive barrier for "
            "city-name applications."
        )

    # 4 — SCO contention
    if has_sco:
        items.append(
            "CONTENTION RISK (§4.5.1.1 SCO): phonetic similarity may attract a String "
            "Confusion Objection, placing this application in direct contention with the "
            "similar string(s) (§5.2). Budget for contention resolution procedures."
        )

    # 5 — plural notification
    if has_plural:
        items.append(
            "§4.4.3 NOTIFICATION: ICANN will notify applicants whose string is the "
            "singular/plural counterpart of this string. Where the base form is delegated "
            "or high-risk, collision patterns extend to this variant."
        )

    # 6 — LRO (trademark objection)
    if lro_risks:
        tier1 = [m for m in lro_risks if m["tier"] == 1]
        brands = ", ".join(f"'{m['brand']}' ({m['holder']})" for m in lro_risks[:3])
        if tier1:
            items.append(
                f"LRO OBJECTION RISK (§4.5.1.3): string matches or is confusingly similar "
                f"to top-tier globally recognised trademark(s): {brands}. Tier-1 rights "
                f"holders are almost certain to file. A successful LRO prevents the "
                f"application from proceeding. Commission trademark clearance before filing."
            )
        else:
            items.append(
                f"LRO OBJECTION RISK (§4.5.1.3): string matches recognised trademark(s): "
                f"{brands}. Commission a WIPO / TMCH / USPTO trademark clearance search "
                f"and seek legal advice before submitting the application."
            )

    # 7 — LPI (public order / morality objection)
    if lpi_risks:
        cats = "; ".join(m["desc"] for m in lpi_risks)
        items.append(
            f"LPI OBJECTION RISK (§4.5.1.4): string falls within '{cats}'. "
            f"Any person may file an LPI objection; a successful finding prevents the "
            f"application from proceeding. Independent legal review essential before filing."
        )

    # 8 — 2012 round history (only when score contribution > 0, i.e. non-trivial findings)
    if h12 and h12.get("score", 0) > 0:
        obj      = h12["objections"]
        obj_tot  = sum(obj.values())
        outcome  = h12["outcome"].replace("_", " ")
        apps     = h12["applications"]
        if h12["delegated"] == 0:
            items.append(
                f"2012 ROUND HISTORY: '{r['string']}' was applied for {apps} time(s) in 2012 "
                f"but was never delegated (outcome: {outcome}). "
                f"{'Objections filed: ' + str(obj_tot) + ' total. ' if obj_tot else ''}"
                f"The factors that prevented delegation may recur in 2026. "
                f"See the 2012 Round Application History section above for detail."
            )
        else:
            items.append(
                f"2012 ROUND HISTORY: '{r['string']}' had {apps} applicant(s) and "
                f"{obj_tot} objection(s) in 2012. Review the application history section "
                f"above for implications."
            )

    # Clean-bill close when there are no blockers and the score is low
    if len(items) == 1 and score < 25 and not sse_risks and not lro_risks and not lpi_risks:
        items.append(
            "No blocking factors identified at this stage. Proceed to application "
            "preparation with standard due diligence and budget for the Temporary "
            "Delegation timeline (§7.7.3)."
        )

    return items


def print_report(r: dict):
    s, colour = r["string"], r["colour"]
    print()

    if not r.get("eligible", True):
        if r["status"] == "ineligible":
            status_line = "ELIGIBILITY REPORT"
        elif r["status"] == "invalid":
            status_line = "INPUT VALIDATION ERROR"
        else:
            status_line = "RESERVED NAME REPORT"
        print(BOLD(f"  {status_line}  ·  .{s.upper()}"))
        print(f"\n  Status   : {colour(BOLD(r['level']))}\n")
        print(BOLD("  Category"))
        print(f"  {colour(r['ineligible_category'])}")
        print()
        print(BOLD("  Reason"))
        for line in textwrap.wrap(r["ineligible_reason"], W-4): print("  " + line)
        print()
        print(BOLD("  Next Steps"))
        for line in textwrap.wrap(r["ineligible_guidance"], W-4): print("  " + line)
        print()
        print(DIM(f"  Source: {r['ineligible_source']}"))
        print(DIM("  Collision scoring not performed — string cannot proceed to §7.7 assessment."))
        print(); return

    print(BOLD(f"  Application Risk Report: .{s.upper()}"))
    score, level = r["score"], r["level"]
    print(f"\n{BOLD('  Name Collision Risk')}")
    print(f"  Score           : {colour(BOLD(str(score)))}/100")
    print(f"  Collision Level : {colour(BOLD(level))}")
    dm_p, dm_s = r.get("aural_dm", ("", ""))
    print(DIM(f"  DM    : primary='{dm_p}'  secondary='{dm_s}'  "
              f"Soundex='{r.get('aural_sdx', '')}'") + "\n")

    # §7.10 SSE risks
    if r.get("sse_risks"):
        print(YELLOW("  ⚠  STRING SIMILARITY EVALUATION RISKS  (§7.10 — Visual)"))
        print(DIM("  Hard stop: a positive SSE Panel finding causes the application NOT to"))
        print(DIM("  proceed, regardless of §7.7 collision score. (§7.10 Table 7-5)"))
        for m in r["sse_risks"]:
            mt = "skeleton match" if m["skeleton_match"] else f"edit-dist {m['distance']}"
            print(f"\n  {RED('✗')}  '.{m['target'].upper()}'  [{mt}]  {DIM(m['category'])}")
            for line in textwrap.wrap(m["outcome"], W-6): print("      " + line)
            print(DIM(f"      ⊕ {m['guidebook']}"))
        print()

    # §4.5.1.1 SCO risks (aural)
    if r.get("sco_risks"):
        print(YELLOW("  ⚠  STRING CONFUSION OBJECTION RISKS  (§4.5.1.1 — Aural)"))
        print(DIM("  NOT a hard stop. A successful SCO places strings in direct contention"))
        print(DIM("  (§5.2). Objections may be filed by existing TLD operators / applicants."))
        for m in r["sco_risks"]:
            conf_col = YELLOW if m["confidence"] == "medium" else RED
            print(f"\n  {conf_col('⚠')}  '.{m['target'].upper()}'  "
                  f"[DM:{m['dm_code']}  confidence:{m['confidence']}]  {DIM(m['category'])}")
            for line in textwrap.wrap(m["outcome"], W-6): print("      " + line)
            if m.get("standing"):
                for line in textwrap.wrap(m["standing"], W-8): print("      " + DIM(line))
        print()

    # §4.4.3 Singular/plural risks
    if r.get("plural_risks"):
        print(YELLOW("  ⚠  SINGULAR / PLURAL PAIR RISKS  (§4.4.3)"))
        print(DIM("  ICANN will notify applicants of singular/plural relationships. Where the "
                  "base form is high-risk or delegated, collision risk patterns extend to the variant."))
        for m in r["plural_risks"]:
            rel = "singular" if m["relation"] == "singular" else "plural"
            print(f"\n  {YELLOW('⚠')}  '{r['string']}' is the {rel} of "
                  f"'.{m['candidate'].upper()}'  {DIM(m['category'])}")
            for line in textwrap.wrap(m["detail"], W-6): print("      " + line)
            print(DIM(f"      ⊕ {m['source']}"))
        print()

    # §4.5.1.3 LRO risks (trademark / famous brand)
    if r.get("lro_risks"):
        print(YELLOW("  ⚠  LEGAL RIGHTS OBJECTION RISKS  (§4.5.1.3 — Trademark)"))
        print(DIM("  NOT a hard stop automatically, but a successful LRO prevents the application"))
        print(DIM("  from proceeding. Any trademark holder with rights in the string may object."))
        for m in r["lro_risks"]:
            tier_col = RED if m["tier"] == 1 else YELLOW
            mt_label = "exact match" if m["match_type"] == "exact" else "edit-distance 1"
            print(f"\n  {tier_col('⚠')}  '{m['brand'].upper()}'  "
                  f"[tier:{m['tier']}  {mt_label}  {m['sector']}]")
            print(f"      Holder: {m['holder']}")
            print(DIM(f"      ⊕ {m['source']}"))
        print()

    # §4.5.1.4 LPI risks (morality / public order)
    if r.get("lpi_risks"):
        print(RED("  ✗  LIMITED PUBLIC INTEREST OBJECTION RISKS  (§4.5.1.4 — Public Order)"))
        print(DIM("  A successful LPI finding prevents the application from proceeding."))
        print(DIM("  Any person may file. ICC Expert Panel applies international public-order norms."))
        for m in r["lpi_risks"]:
            print(f"\n  {RED('✗')}  {m['desc']}")
            for line in textwrap.wrap(m["guidance"], W-6): print("      " + line)
            print(DIM(f"      ⊕ {m['source']}"))
        print()

    # 2012 round application history
    h12 = r.get("history_2012")
    if h12:
        obj     = h12["objections"]
        outcome = h12["outcome"].replace("_", " ")
        obj_parts = [f"{v} {k.upper()}" for k, v in obj.items() if v > 0]
        obj_str = ", ".join(obj_parts) if obj_parts else "none"
        icon = CYAN("ℹ")
        print(CYAN("  ℹ  2012 ROUND APPLICATION HISTORY"))
        print(DIM("  Historical context only — see implications below for 2026 relevance."))
        print(f"\n  {icon}  Applications: {h12['applications']}  "
              f"Contention set: {h12['contention_set']}  "
              f"Delegated: {h12['delegated']}  Withdrawn: {h12['withdrawn']}")
        print(f"      Objections filed: {obj_str}  |  Outcome: {outcome}")
        for line in textwrap.wrap(h12["outcome_note"], W-6): print("      " + line)
        if h12.get("implications"):
            print(f"\n  {DIM('Implications for 2026:')}")
            for imp in h12["implications"]:
                for line in textwrap.wrap(f"• {imp}", W-6): print("      " + line)
        print()

    # Geographic flag
    if r.get("geo_flag"):
        print(YELLOW("  ⚠  GEOGRAPHIC NAME FLAG"))
        for line in textwrap.wrap(r["geo_note"], W-4): print("  " + line)
        print()

    # Summary
    print(BOLD("  Summary"))
    for line in textwrap.wrap(r["summary"], W-4): print("  " + line)

    # Risk Factors
    print()
    print(BOLD("  Risk Factors  (collision score)"))
    for i, f in enumerate(r["factors"], 1):
        pts = f"+{f.score}" if f.score else "0"
        print(f"\n  {BOLD(str(i))}. {CYAN(f.name)}  {colour(f'[{pts}]')}")
        for line in textwrap.wrap(f.description, W-6): print("      " + line)
        if f.recommendation:
            for line in textwrap.wrap(f"→ {f.recommendation}", W-8): print("      " + line)
        if f.source: print(DIM(f"      ⊕ {f.source}"))

    # Overall Verdict
    print()
    print(BOLD("  Overall Verdict"))
    verdict_items = _build_verdict(r, colour)
    for i, item in enumerate(verdict_items, 1):
        lines = textwrap.wrap(item, W - 6)
        print(f"\n  {i}. {lines[0]}")
        for line in lines[1:]:
            print("     " + line)

    print()
    print(DIM("  §4.5.1.1 SCO | §7.7 Collision | §7.7.2 Assessment | §7.7.3 Temp. Delegation"))
    print(DIM("  §7.7.5 Mitigation | §7.10 SSE | §5.2 Contention"))
    print()


def print_status(fetcher: ResourceFetcher, db: CollisionDatabase):
    print()
    print(BOLD("  Network Sources"))
    for s in fetcher.source_status():
        fresh = GREEN("✓ fresh") if s.get("fresh") else YELLOW("⟳ stale/uncached")
        age   = f"{s['age_s']}s" if s.get("age_s") is not None else "not cached"
        sz    = f"{s.get('size', 0):,} B" if s.get("size") else "—"
        extra = s.get("records", "")
        print(f"  {fresh}  {s['desc']}")
        print(DIM(f"         age={age}  size={sz}" + (f"  records={extra}" if extra and extra != "not loaded" else "")))
    print()
    print(BOLD("  Local Data Files"))
    for m in db.data_file_meta():
        print(f"  {GREEN('●')} {m['file']}  ({m['strings']} entries)")
        print(DIM(f"    {m['source'][:72]}"))
    print()
    print(BOLD("  Eligibility Datasets"))
    print(f"  Delegated TLDs   : {len(db.delegated_tlds):,}")
    print(f"  Special-Use      : {len(db.special_use):,}")
    print(f"  Blocked Names    : {len(db.blocked_names):,}  (§7.2.1)")
    print(f"  Reserved Names   : {len(db.reserved_names):,}  (§7.2.2)")
    print(f"  ISO 3166-1 codes : {len(db.iso_codes):,}  (alpha-2 + alpha-3)")
    print(f"  ISO 3166-1 names : {len(db.iso_names):,}  (English forms)")
    print(f"  PSL private      : {len(db.psl_private):,}")
    print()
