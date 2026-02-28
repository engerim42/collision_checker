"""
Singular/plural pair detection — §4.4.3 Singular/Plural Notifications.

ICANN sends §4.4.3 notifications to applicants whose string is the singular or
plural of another applied-for string.  Beyond applicant-to-applicant contention,
the same relationship matters for collision risk: if a string is the plural of a
known high-risk or delegated label, the namespace leakage patterns of the base
string apply equally to the variant.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .database import CollisionDatabase


def _plural_forms(s: str) -> set[str]:
    """Return plausible plural forms of *s* (treating s as a singular)."""
    out: set[str] = set()
    out.add(s + "s")
    out.add(s + "es")
    # -y → -ies  (only when y is preceded by a consonant)
    if s.endswith("y") and len(s) > 2 and s[-2] not in "aeiou":
        out.add(s[:-1] + "ies")
    # -f → -ves
    if s.endswith("f") and len(s) > 2:
        out.add(s[:-1] + "ves")
    # -fe → -ves
    if s.endswith("fe") and len(s) > 3:
        out.add(s[:-2] + "ves")
    out.discard(s)
    return out


def _singular_forms(s: str) -> set[str]:
    """Return plausible singular forms of *s* (treating s as a plural)."""
    out: set[str] = set()
    # -ies → -y
    if s.endswith("ies") and len(s) > 4:
        out.add(s[:-3] + "y")
    # -ves → -f / -fe
    if s.endswith("ves") and len(s) > 4:
        out.add(s[:-3] + "f")
        out.add(s[:-3] + "fe")
    # -es → base  (catches boxes→box, matches→match etc.)
    if s.endswith("es") and len(s) > 3:
        out.add(s[:-2])
    # bare -s
    if s.endswith("s") and not s.endswith("ss") and len(s) > 2:
        out.add(s[:-1])
    out.discard(s)
    return out


def _score_and_meta(candidate: str, db: CollisionDatabase) -> dict | None:
    """Return a match dict if *candidate* is a known high-risk / delegated string."""
    if db.is_delegated(candidate):
        return {
            "category": "Existing Delegated TLD",
            "detail":   f".{candidate.upper()} is already in the IANA root zone.",
            "source":   "data.iana.org · §4.4.3",
            "score":    15,
        }
    if candidate in db.prior_high_risk:
        e = db.prior_high_risk[candidate]
        return {
            "category": "Prior High-Risk String (2012 Round)",
            "detail":   e.get("reason", "Confirmed high-risk in the 2012 gTLD round."),
            "source":   "ICANN 2012 Round · §4.4.3",
            "score":    22,
        }
    if candidate in db.mail_labels:
        e = db.mail_labels[candidate]
        return {
            "category": "Mail Infrastructure Leakage Label",
            "detail":   e.get("reason", "High mail-leakage signal."),
            "source":   "NCAP Study Two §5 · §4.4.3",
            "score":    16,
        }
    if candidate in db.home_labels:
        e = db.home_labels[candidate]
        return {
            "category": "Home Network / IoT Leakage Label",
            "detail":   e.get("reason", "Home-network leakage signal."),
            "source":   "NCAP Study Two §4 · §4.4.3",
            "score":    16,
        }
    if candidate in db.enterprise:
        e = db.enterprise[candidate]
        return {
            "category": "Enterprise Namespace Leakage Label",
            "detail":   e.get("reason", "Enterprise namespace leakage signal."),
            "source":   "NCAP Study Two · §4.4.3",
            "score":    13,
        }
    return None


def check(s: str, db: CollisionDatabase) -> list[dict]:
    """
    Check whether *s* is a singular or plural of a known high-risk / delegated string.

    Returns a list of dicts with keys:
        candidate  – the base/variant form that matched
        relation   – "singular" (s is singular of candidate) or
                     "plural"   (s is plural of candidate)
        category, detail, source, score
    """
    results: list[dict] = []
    seen: set[str] = set()

    for candidate in _plural_forms(s):
        if candidate in seen:
            continue
        seen.add(candidate)
        hit = _score_and_meta(candidate, db)
        if hit:
            # s is the singular; candidate (the plural) matched
            results.append({"candidate": candidate, "relation": "singular", **hit})

    for candidate in _singular_forms(s):
        if candidate in seen:
            continue
        seen.add(candidate)
        hit = _score_and_meta(candidate, db)
        if hit:
            # s is the plural; candidate (the singular) matched
            results.append({"candidate": candidate, "relation": "plural", **hit})

    # Sort by descending score so the most impactful hit is first
    results.sort(key=lambda x: -x["score"])
    return results
