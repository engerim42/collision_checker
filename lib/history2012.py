"""
2012 New gTLD Round Application History checker.

Cross-references the queried string against ICANN's published 2012 round
application data: application counts, contention-set sizes, objections filed
(LRO/LPI/SCO/Community), and final outcomes.

Why this matters for 2026 applicants
--------------------------------------
* Strings that attracted community objections in 2012 are very likely to face
  the same objections again from the same bodies (sports federations, religious
  organisations, geographic-name governments, etc.).
* Large contention sets indicate high commercial demand — applicants should
  budget for contention-resolution procedures (§5.1–§5.2) and last-resort
  auctions, which have reached USD 20–100 M for premium strings.
* Strings where ALL applicants withdrew (excluding the three HIGH RISK strings
  already tracked in prior_high_risk.json) may signal unresolved legal,
  policy, or objection issues that would recur in 2026.
* Strings with filed LRO / LPI objections provide direct precedent for our
  LRO / LPI risk factors (§4.5.1.3 / §4.5.1.4).

Scoring
-------
The score contribution from 2012 history is intentionally modest because the
primary value is contextual, not a primary collision risk signal:

  all_withdrawn (non-high-risk)        +15–20  strong advisory
  community objection filed            +18     rights-holder will likely re-file
  sport / geographic body objection    +18     same bodies still active
  LRO objections ≥ 2 (withdrawn)       +15     trademark holders filed before
  Large contention set (≥ 8)            0      informational (all now INELIGIBLE)

Strings in prior_high_risk (corp/home/mail) are excluded — Factor 2 already
adds 100 points for those.  Strings that are currently delegated (in the IANA
root zone) will be caught by the INELIGIBLE check before factors run, so
their history entries carry score=0 to avoid any future double-counting.

Source
------
ICANN New gTLD Program Application Status Portal; ICANN Contention Resolution
Reports; ICC Expert Determinations 2013.
https://newgtlds.icann.org/en/
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .database import CollisionDatabase


def check(s: str, db: "CollisionDatabase") -> dict | None:
    """
    Return 2012 history context for *s*, or None if no record exists.

    The returned dict (if any) has:
        applications     – total applications filed for this exact label
        contention_set   – size of the contention set (may equal applications)
        delegated        – number of applications that resulted in delegation
        withdrawn        – number that withdrew
        objections       – dict: community / lro / lpi / sco counts
        outcome          – outcome key (see module docstring)
        outcome_note     – human-readable narrative
        score            – score contribution (0 for delegated-only strings)
        implications     – list[str] of applicant-facing advisory sentences
    """
    # Skip strings already covered by Factor 2 (prior_high_risk)
    if s in db.prior_high_risk:
        return None

    rec = db.history_2012.get(s)
    if rec is None:
        return None

    obj          = rec.get("objections", {})
    outcome      = rec.get("outcome", "")
    apps         = rec.get("applications", 0)
    contention   = rec.get("contention_set", 0)
    delegated    = rec.get("delegated", 0)
    all_withdrew = delegated == 0 and outcome in ("all_withdrawn", "rejected")

    implications: list[str] = []

    if all_withdrew:
        implications.append(
            f"All {apps} applicant(s) in the 2012 round withdrew or failed. "
            f"The issues that drove withdrawal may recur in 2026. "
            f"Independent legal review before filing is strongly recommended."
        )

    if obj.get("community", 0) >= 1:
        implications.append(
            f"{obj['community']} community objection(s) were filed in 2012. "
            f"The same bodies (sports federations, geographic governments, religious "
            f"organisations, or sector associations) will likely re-file in 2026 under "
            f"§4.5.1.2 — budget for DRSP objection fees and potential lengthy resolution."
        )

    if obj.get("lro", 0) >= 2 and all_withdrew:
        implications.append(
            f"{obj['lro']} Legal Rights Objections were filed in 2012. "
            f"Trademark holders who objected previously are very likely to file again. "
            f"Cross-check against the LRO risk section above."
        )

    if obj.get("lpi", 0) >= 1 and all_withdrew:
        implications.append(
            f"{obj['lpi']} LPI objection(s) were filed in 2012. "
            f"While ICC Expert Panels set a high threshold, LPI precedent is directly "
            f"relevant to the §4.5.1.4 risk flagged in the LPI section above."
        )

    if contention >= 8 and not all_withdrew:
        implications.append(
            f"This string was in a {contention}-applicant contention set in 2012 — "
            f"the largest category. Expect intense competition in 2026. "
            f"Budget for contention-resolution procedures (§5.1–§5.2) and, if necessary, "
            f"a last-resort auction, which has reached USD 20–100 M for premium strings."
        )
    elif contention >= 4 and not all_withdrew:
        implications.append(
            f"This string attracted {apps} applicants in 2012. "
            f"Competition will likely recur in 2026; budget for contention-resolution "
            f"procedures (§5.2) and a potential last-resort auction."
        )

    if not implications:
        implications.append(
            f"Applied for in 2012 ({apps} applicant(s), outcome: {outcome.replace('_', ' ')}). "
            f"Review the 2012 resolution process for additional context."
        )

    return {
        "applications":   apps,
        "contention_set": contention,
        "delegated":      delegated,
        "withdrawn":      rec.get("withdrawn", 0),
        "objections":     obj,
        "outcome":        outcome,
        "outcome_note":   rec.get("outcome_note", ""),
        "score":          rec.get("score", 0),
        "implications":   implications,
    }
