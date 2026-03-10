from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .colors import MAGENTA, RED, YELLOW, GREEN
from . import singular_plural as _sp
from . import semantic as _sem
from . import lro as _lro
from . import lpi as _lpi
from . import history2012 as _h12

if TYPE_CHECKING:
    from .database import CollisionDatabase


class EligibilityResult:
    __slots__ = ("status", "category", "reason", "source", "geo_flag", "geo_note")

    def __init__(self, status="eligible", category="", reason="",
                 source="", geo_flag=False, geo_note=""):
        self.status   = status
        self.category = category
        self.reason   = reason
        self.source   = source
        self.geo_flag = geo_flag
        self.geo_note = geo_note

    @property
    def eligible(self): return self.status == "eligible"


class RiskFactor:
    __slots__ = ("name", "score", "description", "recommendation", "source")

    def __init__(self, name, score, description, recommendation="", source=""):
        self.name           = name
        self.score          = score
        self.description    = description
        self.recommendation = recommendation
        self.source         = source


class RiskAssessor:
    def __init__(self, db: CollisionDatabase): self.db = db

    def _check_eligibility(self, s: str) -> EligibilityResult:
        db = self.db

        def inelig(cat, reason, src="ICANN Guidebook 2026 §7.2.1"):
            return EligibilityResult("ineligible", cat, reason, src)

        def reserved(cat, reason, src="ICANN Guidebook 2026 §7.2.2"):
            return EligibilityResult("reserved", cat, reason, src)

        if re.fullmatch(r'[a-z0-9]{1,2}', s):
            return inelig("One/Two-Character ASCII String",
                f"'{s}' is {len(s)} char(s). All 1-2-char ASCII strings are reserved for "
                f"ISO 3166 country-code assignment. Minimum 3 chars required (§3.1.8).",
                "ICANN Guidebook §7.2.1; ISO 3166 MA")
        if s.startswith("xn--"):
            return inelig("IDN ACE Prefix",
                "Strings starting with 'xn--' are reserved as the ACE prefix for IDN. "
                "Apply for the Unicode form instead.", "RFC 5891; ICANN §3.1.8")
        if db.is_delegated(s):
            return inelig("Existing Delegated TLD",
                f"'.{s.upper()}' is already in the IANA root zone. Cannot apply (§7.2.1).",
                "data.iana.org/TLD/tlds-alpha-by-domain.txt; §7.2.1")
        if db.is_special_use(s):
            return inelig("IETF Protocol-Reserved Name",
                f"'{s}' is in the IANA Special-Use Domain Names registry (RFC 6761/2606/7686).",
                "IANA Special-Use Registry; RFC 6761/2606/7686")
        if db.is_blocked(s):
            meta = db.blocked_names[s]
            return inelig(meta["desc"],
                f"'{s.upper()}' is on the ICANN Blocked Names list (§7.2.1).", meta["source"])
        if db.is_iso_code(s):
            return inelig("ISO 3166-1 Country/Territory Code",
                f"'{s.upper()}' is an ISO 3166-1 code. Applications 'will not be approved' (§7.5.1).",
                "ISO 3166-1; IANA Subtag Registry; §7.5.1")
        if db.is_iso_name(s):
            return inelig("ISO 3166-1 Country/Territory Name",
                f"'{s}' matches an ISO 3166-1 country/territory name. "
                f"§7.5.1: 'applications will not be approved'. Translations also blocked.",
                "ISO 3166-1; §7.5.1")
        if db.is_reserved(s):
            meta = db.reserved_names[s]
            return reserved(meta["desc"],
                f"'{s.upper()}' is on the ICANN Reserved Names list under '{meta['desc']}'. "
                f"Can ONLY be applied for by the designated entity with documentation.",
                meta["source"])
        if db.is_un_macro(s):
            return reserved("UN M.49 Macro-Geographic Region Name",
                f"'{s}' is a UN M.49 macro-geographic region name. Applications for these "
                f"strings will not be approved per §7.5.2 (same treatment as ISO 3166-1 "
                f"country names). Can only be applied for under a UN/ICANN arrangement.",
                "UN M.49 Standard; ICANN §7.5.2")

        geo_flag = False
        geo_notes: list[str] = []
        city_label = db.get_city(s)
        if city_label:
            geo_flag = True
            geo_notes.append(
                f"'{s}' matches city '{city_label}'. §7.5.3: Geographic Names Review will "
                f"apply. Applicant must provide documented support from the relevant "
                f"government(s) or demonstrate legitimate community sponsorship.")
        sacred_desc = db.get_sacred_site(s)
        if sacred_desc:
            geo_flag = True
            geo_notes.append(
                f"'{s}' is a recognised sacred/pilgrimage site: {sacred_desc}. "
                f"§7.5.3 Geographic Names Review applies. A §4.5.1.2 Community Objection "
                f"from the relevant religious community is almost certain; documented "
                f"community support and non-objection evidence required.")
        if db.is_un_region(s):   # catches sub-regions (macro already blocked above)
            geo_flag = True
            geo_notes.append(
                f"'{s}' is a UN M.49 sub-regional geographic name. §7.5 Geographic Names "
                f"Review applies. Community support documentation required.")
        if not geo_notes:
            for name in db.iso_names:
                if len(name) > 3 and s in name.split():
                    geo_flag = True
                    geo_notes.append(
                        f"'{s}' is a component of country name '{name}'. "
                        f"§7.5.1 also blocks separable components. Verify in TAMS.")
                    break
        geo_note = "  ".join(geo_notes)
        return EligibilityResult("eligible", geo_flag=geo_flag, geo_note=geo_note)

    def _validate_format(self, raw: str) -> "dict | None":
        """Return an error result dict if raw is not a syntactically valid TLD label, else None."""
        s = raw.strip().lstrip(".")

        if not s:
            return self._fmt_error(raw or "(empty)", "Empty Input",
                "No string provided. Please enter a TLD label to assess.")

        if " " in s or "\t" in s:
            return self._fmt_error(s, "Invalid Format — Whitespace",
                f"'{s}' contains spaces or tabs. A TLD label must be a single token "
                f"with no whitespace (RFC 1034 §3.5).")

        if "." in s:
            return self._fmt_error(s, "Invalid Format — Dot",
                f"'{s}' contains a dot ('.'). A TLD is a single DNS label — "
                f"enter the label without the dot prefix or any interior dots.")

        if not re.fullmatch(r'[A-Za-z0-9\-]+', s):
            bad = sorted(set(c for c in s if not re.match(r'[A-Za-z0-9\-]', c)))
            bad_repr = " ".join(repr(c) for c in bad)
            return self._fmt_error(s, "Invalid Characters",
                f"'{s}' contains characters not allowed in a DNS label: {bad_repr}. "
                f"Only letters (a–z), digits (0–9), and hyphens are permitted (RFC 1034 §3.5).")

        if s.isdigit():
            return self._fmt_error(s, "Numeric-Only String",
                f"'{s}' consists entirely of digits. A new gTLD label must contain at least "
                f"one letter (§3.1.8). All-numeric strings cannot be applied for.",
                "ICANN Guidebook §3.1.8")

        if s.startswith("-") or s.endswith("-"):
            return self._fmt_error(s, "Invalid Format — Leading/Trailing Hyphen",
                f"'{s}' starts or ends with a hyphen. DNS labels must not begin or "
                f"end with a hyphen (RFC 1034 §3.5).")

        if len(s) >= 4 and s[2] == '-' and s[3] == '-' and not s.lower().startswith('xn--'):
            return self._fmt_error(s, "Invalid Format — Hyphens in Third and Fourth Position",
                f"'{s}' has hyphens in the third and fourth character positions. "
                f"Per RFC 5891 §4.2.3.1 this pattern is reserved for internationalised domain "
                f"name ACE labels (the xn-- prefix). Use a different label, or if this is an "
                f"IDN, apply using the Unicode form of the string.",
                "RFC 5891 §4.2.3.1; ICANN Guidebook §3.1.8")

        if len(s) > 63:
            return self._fmt_error(s, "Invalid Length — Exceeds 63 Characters",
                f"'{s}' is {len(s)} characters long. DNS labels are limited to "
                f"63 characters (RFC 1035 §2.3.4).")

        return None

    def _fmt_error(self, s: str, category: str, reason: str,
                   source: str = "RFC 1034 §3.5 / RFC 1035 §2.3.4 / ICANN Guidebook §3.1.8") -> dict:
        return {
            "string": s.lower().strip().lstrip("."),
            "eligible": False,
            "status": "invalid",
            "ineligible_category": category,
            "ineligible_reason": reason,
            "ineligible_source": source,
            "ineligible_guidance": (
                "Correct the string format before running the risk assessment. "
                "A valid gTLD applicant string must: contain only letters (a–z), digits (0–9), "
                "or hyphens; contain at least one letter (not all-numeric); not start or end "
                "with a hyphen; not have hyphens in the third and fourth character positions "
                "(reserved for IDN ACE labels); contain no spaces or dots; "
                "and be between 3 and 63 characters."),
            "colour": RED,
            "level": "INVALID FORMAT",
            "score": 0,
            "summary": reason,
            "factors": [],
            "sse_risks": [],
            "sco_risks": [],
            "plural_risks": [],
            "lro_risks": [],
            "lpi_risks": [],
            "history_2012": None,
            "geo_flag": False,
            "geo_note": "",
            "aural_dm": ("", ""),
            "aural_sdx": "",
        }

    def assess(self, string: str) -> dict:
        fmt_err = self._validate_format(string)
        if fmt_err:
            return fmt_err

        s    = string.lower().strip().lstrip(".")
        elig = self._check_eligibility(s)

        if not elig.eligible:
            colour  = RED if elig.status == "ineligible" else MAGENTA
            label   = "INELIGIBLE" if elig.status == "ineligible" else "RESERVED — Restricted"
            guidance = ("Cannot be applied for by any entity in the 2026 round."
                        if elig.status == "ineligible" else
                        "Contact ICANN for Reserved Name exception process (§7.2.2.2.1). "
                        "Required: cert. of incorporation, parent-org letter, non-objection evidence.")
            return {"string": s, "eligible": False, "status": elig.status,
                    "ineligible_category": elig.category, "ineligible_reason": elig.reason,
                    "ineligible_source": elig.source, "ineligible_guidance": guidance,
                    "colour": colour, "level": label, "score": 0, "summary": elig.reason,
                    "factors": [], "sse_risks": [], "sco_risks": [], "plural_risks": [],
                    "lro_risks": [], "lpi_risks": [], "history_2012": None,
                    "geo_flag": False, "geo_note": "", "aural_dm": ("", ""), "aural_sdx": ""}

        # ── Visual similarity ─────────────────────────────────────────────────
        vis_sim   = self.db.fetcher.similarity.check(s, self.db)
        sse_risks = vis_sim["sse_risks"]
        vis_hits  = {m["target"] for m in vis_sim["collision_risks"] + vis_sim["sse_risks"]}

        # ── Aural similarity ──────────────────────────────────────────────────
        aur_sim   = self.db.fetcher.aural.check(s, self.db, visual_hits=vis_hits)
        sco_risks = aur_sim["sco_risks"]

        factors: list[RiskFactor] = []; score = 0
        db = self.db

        def add(f: RiskFactor):
            nonlocal score
            factors.append(f)
            score = min(100, score + f.score)

        # Factor 1 — ITHI M4
        ithi = db.fetcher.ithi.lookup(s)
        if ithi:
            add(RiskFactor("ITHI M4 — Live Root-Server Leakage", score=ithi["score"],
                description=(f"ITHI M4 ({ithi['month']}): {ithi['pct']:.4f}% NXD leakage at public root. "
                             f"Rank #{ithi['rank']} / {ithi['total']} tracked labels "
                             f"(top {100-ithi['pct_rank']:.1f}%). "
                             f"Primary §7.7.2 quantitative input."),
                recommendation="High rank = leading high-risk indicator. Also check ASN origin-diversity.",
                source=f"ithi.research.icann.org · M4Data.txt · {ithi['month']}"))

        # Factor 2 — Prior-round high-risk
        if s in db.prior_high_risk:
            e = db.prior_high_risk[s]
            add(RiskFactor("Confirmed Prior-Round High-Risk (2012)", score=e.get("score", 100),
                description=(f"One of only THREE strings designated HIGH-RISK in 2012 round. "
                             f"{e.get('reason', '')} Not refund-eligible if withdrawn (§3.3.3.1.4)."),
                recommendation="Mandatory High-Risk Mitigation Plan (§7.7.5). Additional fee applies.",
                source="ICANN Guidebook 2026 §7.7.1 / 2012 Round"))

        # Factor 3 — Visual similarity (collision-adjacent)
        if vis_sim["collision_risks"]:
            best      = vis_sim["collision_risks"][0]; max_score = best["score"]
            matches   = "; ".join(
                "'.{}' ({}) [{}]".format(
                    m["target"].upper(),
                    "skeleton" if m["skeleton_match"] else "edit-dist {}".format(m["distance"]),
                    m["category"],
                )
                for m in vis_sim["collision_risks"][:4])
            add(RiskFactor("Visual Similarity — Collision-Adjacent Strings", score=max_score,
                description=(f"'{s}' is visually similar to: {matches}. Near-miss and "
                             f"cross-script confusable strings inherit the same §7.7 collision "
                             f"patterns as the strings they resemble."),
                recommendation=("Skeleton match = cross-script confusability. "
                                "Cross-check ITHI M4 for this exact string."),
                source="Unicode UTS #39 / Levenshtein / NCAP Study Two"))

        # Factor 4 — Aural similarity (collision-adjacent)
        if aur_sim["collision_risks"]:
            best_aural = aur_sim["collision_risks"][0]; aur_score = best_aural["score"]
            aur_matches = "; ".join(
                f"'.{m['target'].upper()}' [DM:{m['dm_code']}, "
                f"confidence:{m['confidence']}, {m['category']}]"
                for m in aur_sim["collision_risks"][:4])
            add(RiskFactor("Aural Similarity — Phonetically Similar Leakage Label",
                score=aur_score,
                description=(f"'{s}' sounds like: {aur_matches}. "
                             f"The underlying namespace leakage patterns (corporate DNS defaults, "
                             f"mail discovery, home-network labels) apply to phonetically "
                             f"equivalent strings. DM codes: primary='{aur_sim['dm_primary']}' "
                             f"secondary='{aur_sim['dm_secondary']}' / "
                             f"Soundex='{aur_sim['soundex']}'."),
                recommendation=("'high' confidence = both Double Metaphone AND Soundex agree. "
                                "Verify ITHI M4 data for this exact string. Aural similarity "
                                "also exposes the application to a §4.5.1.1 SCO (see warnings below)."),
                source="Double Metaphone (Philips 2000) + American Soundex (Russell 1918)"))

        # Factor 5 — Semantic / translation
        sem_hits = _sem.check(s)
        if sem_hits:
            best_sem  = sem_hits[0]
            sem_score = best_sem["score"]
            sem_desc  = "; ".join(
                "'{word}' is {lang} for '{concept}'".format(
                    word=s, lang=m["language"], concept=m["concept"])
                for m in sem_hits[:4])
            add(RiskFactor("Semantic / Translation Match — High-Risk Concept",
                score=sem_score,
                description=(f"'{s}' translates to a high-risk namespace concept: {sem_desc}. "
                             f"Non-English labels that fulfil the same semantic role as confirmed "
                             f"high-risk strings (home, mail, corporate…) inherit the same "
                             f"namespace leakage patterns."),
                recommendation=("Verify ITHI M4 leakage volume for this exact string. "
                                "The NCAP methodology treats semantic equivalents as within scope "
                                "of the collision risk assessment."),
                source="; ".join(dict.fromkeys(m["ncap_ref"] for m in sem_hits))))

        # Factor 6 — Singular/plural pair
        plural_hits = _sp.check(s, db)
        if plural_hits:
            best_pl   = plural_hits[0]
            pl_score  = best_pl["score"]
            pl_desc   = "; ".join(
                "'{s}' is the {rel} of '{cand}' ({cat})".format(
                    s=s, rel=m["relation"], cand=m["candidate"], cat=m["category"])
                for m in plural_hits[:3])
            add(RiskFactor("Singular/Plural Pair — §4.4.3 Notification Risk",
                score=pl_score,
                description=(f"Singular/plural relationship detected: {pl_desc}. "
                             f"Per §4.4.3, ICANN will notify all applicants whose string is "
                             f"the singular or plural of another applied-for string. Where the "
                             f"base form is high-risk, the variant inherits collision risk."),
                recommendation=("A §4.4.3 notification does not automatically block the string "
                                "but may trigger additional community objections. If the base "
                                "form is delegated, a String Confusion Objection (§4.5.1.1) "
                                "is also possible."),
                source="; ".join(dict.fromkeys(m["source"] for m in plural_hits))))

        # Factor 8 — Mozilla PSL
        if db.is_psl_private(s) and s not in db.prior_high_risk and not sem_hits:
            add(RiskFactor("Mozilla Public Suffix List — Private Domains", score=45,
                description=(f"'{s}' is in the PSL PRIVATE DOMAINS section, indicating "
                             f"pre-existing private-namespace usage."),
                recommendation="Cross-check with ITHI leakage data for volume evidence.",
                source="publicsuffix.org/list/public_suffix_list.dat"))

        # Factor 9 — Curated NCAP leakage
        cat, entry = db.get_curated_entry(s)
        if cat and cat != "Prior High-Risk (2012 Round)":
            add(RiskFactor(cat, score=entry.get("score", 60),
                description=(f"'{s}' is in the curated {cat} dataset "
                             f"(NCAP Study Two Apr 2024 / DITL/ITHI / SSAC). "
                             f"{entry.get('reason', '')}"),
                recommendation=("High origin-diversity is the primary §7.7.2 trigger. "
                                "Check ITHI query-volume and ASN-count data."),
                source="NCAP Study Two (Apr 2024) / SAC045 / SAC068 / DITL"))

        # Factor 10 — LRO (Legal Rights Objection)
        lro_hits = _lro.check(s)
        if lro_hits:
            best_lro = lro_hits[0]
            lro_score = best_lro["score"]
            lro_desc = "; ".join(
                "'{s}' {mt} '{b}' ({h}, {sec})".format(
                    s=s, mt="exactly matches" if m["match_type"] == "exact" else "is within edit-distance 1 of",
                    b=m["brand"], h=m["holder"], sec=m["sector"])
                for m in lro_hits[:3])
            add(RiskFactor("Legal Rights Objection (LRO) — Trademark / Famous Brand",
                score=lro_score,
                description=(f"'{s}' matches a globally recognised brand: {lro_desc}. "
                             f"Under §4.5.1.3 any trademark holder with rights in the string "
                             f"may file an LRO. A successful finding prevents the application "
                             f"from proceeding regardless of the §7.7 collision score."),
                recommendation=("Commission a trademark clearance search (WIPO Global Brand DB, "
                                "TMCH, USPTO TESS, EUIPO) before filing. Budget for DRSP "
                                "objection fees and potential contention set costs (§5.2). "
                                "Tier-1 brands are almost certain to file."),
                source="; ".join(dict.fromkeys(m["source"] for m in lro_hits[:3]))))

        # Factor 11 — LPI (Limited Public Interest Objection)
        lpi_hits = _lpi.check(s)
        if lpi_hits:
            best_lpi = lpi_hits[0]
            lpi_score = best_lpi["score"]
            add(RiskFactor("Limited Public Interest (LPI) Objection — Morality / Public Order",
                score=lpi_score,
                description=(f"'{s}' falls within the '{best_lpi['desc']}' category. "
                             f"Under §4.5.1.4, any person may file an LPI objection if the "
                             f"string is contrary to 'generally accepted legal norms of morality "
                             f"and public order recognised under principles of international law'. "
                             f"Category: {best_lpi['category']}."),
                recommendation=best_lpi["guidance"],
                source=best_lpi["source"]))

        # Factor 12 — 2012 round application history
        h12 = _h12.check(s, db)
        if h12 and h12["score"] > 0:
            obj = h12["objections"]
            obj_summary = ", ".join(
                f"{v} {k.upper()}" for k, v in obj.items() if v > 0
            ) or "none filed"
            add(RiskFactor("2012 Round Application History",
                score=h12["score"],
                description=(
                    f"'{s}' was applied for in the 2012 new gTLD round: "
                    f"{h12['applications']} application(s), contention set of "
                    f"{h12['contention_set']}, {h12['delegated']} delegated, "
                    f"{h12['withdrawn']} withdrawn. "
                    f"Objections filed: {obj_summary}. "
                    f"Outcome: {h12['outcome'].replace('_', ' ')}. "
                    f"{h12['outcome_note']}"
                ),
                recommendation="; ".join(h12["implications"]),
                source=(
                    "ICANN New gTLD Program 2012 Round Application Status Portal; "
                    "ICC Expert Determinations 2013; ICANN Contention Resolution Records. "
                    "https://newgtlds.icann.org/en/"
                )))

        # Factor 13 — Geographic name similarity (fuzzy city match, B1)
        # Only fires when the string is NOT an exact city match (geo_flag already set).
        if not elig.geo_flag:
            geo_sim = db.find_similar_cities(s, max_dist=1)
            if geo_sim:
                sim_desc = "; ".join(
                    f"'{r['variant']}' → {r['city']} (edit-dist {r['distance']})"
                    for r in geo_sim[:3])
                add(RiskFactor(
                    "Geographic Name Similarity — Near-Miss City Match",
                    score=28,
                    description=(
                        f"'{s}' is within 1 edit of a recognised geographic city name: "
                        f"{sim_desc}. Near-miss geographic strings carry §7.5.3 review "
                        f"risk and may attract a §4.5.1.2 Community Objection from the "
                        f"affected city's government or local community."),
                    recommendation=(
                        "Verify against ICANN's TAMS geographic name index. "
                        "Obtain non-objection documentation from the relevant "
                        "government(s) if intending to proceed."),
                    source="GeoNames city data; ICANN Guidebook §7.5.3 / §4.5.1.2"))

        # Factor 14 — Sacred / pilgrimage site match (D2)
        # Scored separately from geo_flag because religious community objection
        # standing (§4.5.1.2) is independent of the §7.5.3 geographic review.
        if elig.geo_flag and db.is_sacred_site(s):
            sacred_desc = db.get_sacred_site(s)
            add(RiskFactor(
                "Sacred / Pilgrimage Site — §4.5.1.2 Community Objection Risk",
                score=35,
                description=(
                    f"'{s}' is a globally recognised sacred or pilgrimage site: "
                    f"{sacred_desc}. The associated religious community has standing "
                    f"to file a §4.5.1.2 Community Objection. Historical precedent: "
                    f"multiple community objections against culturally sensitive strings "
                    f"were upheld in the 2012 round."),
                recommendation=(
                    "Obtain explicit non-objection letters from recognised representative "
                    "bodies of the affected religious community before filing. "
                    "Budget for Community Objection proceedings (DRSP fees) if the "
                    "community has not endorsed the application."),
                source="UNWTO Sacred Sites Programme; ICANN §4.5.1.2 / §7.5.3; "
                       "ICC Expert Determinations 2013"))

        # Factor 15 — No signals
        if not factors:
            add(RiskFactor("No Known High-Risk Signals Detected", score=5,
                description=(f"'{s}' does not match any high-risk pattern across IANA TLD list, "
                             f"special-use registry, PSL, NCAP datasets, ITHI M4, visual similarity, "
                             f"or aural similarity checks. Per §7.7.1, low indicator volume does NOT "
                             f"guarantee safety — all strings undergo §7.7.2 and §7.7.3."),
                recommendation=("Obtain ICANN's pre-application longitudinal dataset (§7.7.1) "
                                "when published. Budget for Temporary Delegation timeline."),
                source="—"))

        # Risk level (§7.7 leakage score)
        if score >= 85:
            level, colour = "HIGH", RED
            summary = ("Almost certain to appear on the Collision String List. "
                       "Mandatory High-Risk Mitigation Plan (§7.7.5) required with additional fee.")
        elif score >= 55:
            level, colour = "MODERATE", YELLOW
            summary = ("Significant collision risk factors. Temporary Delegation data will be "
                       "decisive. Proactively gather ITHI evidence.")
        elif score >= 25:
            level, colour = "LOW-MODERATE", YELLOW
            summary = "Some risk signals detected. Standard assessment and Temporary Delegation apply."
        else:
            level, colour = "LOW", GREEN
            summary = "No significant collision risk patterns found. Standard due diligence applies."

        # Override summary when harder barriers are present regardless of score
        sse_confirmed = [m for m in sse_risks if "Delegated" in m.get("category", "")]
        if sse_confirmed:
            targets = ", ".join(f".{m['target'].upper()}" for m in sse_confirmed)
            summary = (f"§7.10 Table 7-5 BLOCK: confusingly similar to {targets} "
                       f"(already delegated). Application cannot proceed.")
        elif sse_risks:
            summary = ("§7.10 SSE match detected. A positive SSE Panel finding will "
                       "prevent this application from proceeding regardless of the leakage score.")

        return {"string": s, "eligible": True, "status": "eligible",
                "score": score, "level": level, "colour": colour, "summary": summary,
                "factors": factors, "sse_risks": sse_risks, "sco_risks": sco_risks,
                "plural_risks": plural_hits, "lro_risks": lro_hits, "lpi_risks": lpi_hits,
                "history_2012": h12,
                "geo_flag": elig.geo_flag, "geo_note": elig.geo_note,
                "aural_dm": (aur_sim["dm_primary"], aur_sim["dm_secondary"]),
                "aural_sdx": aur_sim["soundex"]}
