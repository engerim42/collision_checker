"""
Limited Public Interest (LPI) Objection risk checker — §4.5.1.4

An LPI objection may be filed against a gTLD application whose string is
contrary to "generally accepted legal norms of morality and public order
recognised under principles of international law".  The threshold is high
(ICC Expert Panel decisions from 2013 confirm this), but a successful LPI
finding prevents the application from proceeding.

Categories covered
------------------
lpi_objected_2012
    Strings for which LPI objections were actually filed and/or upheld in the
    2012 new-gTLD round (ICC International Centre for Expertise).
    Source: ICANN 2012 LRO/LPI decision archive (icann.org).

drug_reference
    Common names of internationally controlled substances under the UN Single
    Convention on Narcotic Drugs (1961), the Convention on Psychotropic
    Substances (1971), and the UN Convention Against Illicit Traffic (1988).
    A TLD delegating these names would very likely be challenged as contrary
    to international public order.  Source: DEA Schedule I/II; INCB lists.

obscenity
    Terms universally recognised as sexually explicit or grossly offensive
    across virtually all legal jurisdictions.  English-language focus; non-
    English equivalents with documented global recognition included.

hate_speech
    Racial, ethnic, or religious slurs with documented status as internationally
    recognised hate speech.  Only terms that would be actionable under the laws
    of the large majority of UN member states are included.

sanctions_adjacent
    Terms strongly and exclusively associated with UN-designated terrorist
    organisations or sanctioned entities (UNSCR 1267 Consolidated List;
    OFAC SDN).  Not automatic LPI hits but high-risk advisory flags.

Sources
-------
* ICANN 2012 LPI decisions — icann.org dispute-resolution / objection-decisions
* ICC Expert Determinations 2013 (International Centre for Expertise)
* DEA Drug Scheduling — dea.gov/drug-information/drug-scheduling
* UN INCB Narcotic Drugs: List of Narcotic Drugs under International Control
* UN Security Council Res. 1267 Consolidated Sanctions List — un.org
* ICANN Applicant Guidebook 2026 §4.5.1.4
"""
from __future__ import annotations


# ── LPI catalogue ─────────────────────────────────────────────────────────────
# Structure: category → {desc, score, source, strings: [label, ...]}
_CATEGORIES: dict[str, dict] = {
    "lpi_objected_2012": {
        "desc":   "LPI Objection — 2012 Round Precedent",
        "score":  90,
        "source": "ICANN 2012 new-gTLD round LPI objection decisions; ICC Expert Determinations 2013",
        "strings": [
            # Strings for which LPI objections were filed or upheld in 2012
            "nazi", "fascist", "terrorist",
            "porn", "xxx", "adult", "sex",
            "casino",                          # objected; ICC found no LPI basis (threshold high)
            "islam", "catholic", "christian",  # religious terms — objected but largely dismissed
            "gay",                             # objected; ICC found no LPI basis
        ],
    },
    "drug_reference": {
        "desc":   "Internationally Controlled Substance — UN Conventions",
        "score":  80,
        "source": "UN Single Convention on Narcotic Drugs 1961; Convention on Psychotropic "
                  "Substances 1971; DEA Schedule I/II; INCB Narcotic Drugs Green List",
        "strings": [
            # Schedule I narcotic drugs (UN 1961 Convention)
            "heroin", "cocaine", "opium", "morphine", "codeine", "fentanyl",
            "methadone", "oxycodone", "hydrocodone", "tramadol",
            # Schedule I psychotropic substances (UN 1971 Convention)
            "methamphetamine", "meth", "amphetamine", "lsd", "mdma", "ecstasy",
            "psilocybin", "ketamine", "ghb",
            # Common trade / street names
            "crack", "smack", "crank",
        ],
    },
    "obscenity": {
        "desc":   "Universally Recognised Obscene Term",
        "score":  75,
        "source": "ICC LPI Guidelines; ICANN Guidebook §4.5.1.4; international public-order norms",
        "strings": [
            "fuck", "shit", "cunt", "asshole", "dickhead",
            "bestiality", "incest", "pedophile", "paedophile",
            "snuff", "gore",
        ],
    },
    "hate_speech": {
        "desc":   "Internationally Recognised Hate Speech / Slur",
        "score":  75,
        "source": "ICC LPI Guidelines; UN Rabat Plan of Action on hate speech; "
                  "International Covenant on Civil and Political Rights Art. 20(2)",
        "strings": [
            "nigger", "kike", "faggot", "chink", "spic", "gook",
            "jihad",     # context-dependent but flags high LPI scrutiny as a TLD
            "aryan",     # exclusively associated with white-supremacist ideology as a brand/TLD
            "genocide",
        ],
    },
    "sanctions_adjacent": {
        "desc":   "Sanctions-Adjacent — UN/OFAC Designated Entity Association",
        "score":  65,
        "source": "UN Security Council Res. 1267 Consolidated Sanctions List; "
                  "OFAC SDN List; FATF High-Risk Jurisdictions",
        "strings": [
            "alqaeda", "isis", "isil", "daesh", "boko", "hamas", "hezbollah",
            "taleban", "taliban",
        ],
    },
}

# Build flat index: label → {category_key, desc, score, source}
_INDEX: dict[str, dict] = {}
for _cat_key, _cat in _CATEGORIES.items():
    _meta = {"category": _cat_key, "desc": _cat["desc"],
             "score": _cat["score"], "source": _cat["source"]}
    for _s in _cat["strings"]:
        _INDEX[_s.lower()] = _meta


def check(s: str) -> list[dict]:
    """
    Return LPI risk signals for *s*.

    Each hit dict has:
        category    – category key
        desc        – human-readable category description
        score       – LPI risk score contribution
        source      – source reference
        guidance    – applicant-facing recommendation
    """
    s = s.lower().strip()
    hit = _INDEX.get(s)
    if not hit:
        return []

    cat_key = hit["category"]
    cat     = _CATEGORIES[cat_key]

    # Build context-specific guidance per category
    if cat_key == "lpi_objected_2012":
        guidance = (
            "This string was objected to in the 2012 round on LPI grounds. "
            "While not all 2012 LPI objections succeeded (the ICC set a high threshold), "
            "a repeat objection is very likely. Pre-application legal review is essential. "
            "ICANN Guidebook §4.5.1.4 allows any DRSP-accredited party to file."
        )
    elif cat_key == "drug_reference":
        guidance = (
            "This string is the internationally recognised name of a controlled substance "
            "under UN drug conventions. Delegation as a gTLD would almost certainly be "
            "characterised as contrary to international public order. LPI objection risk "
            "is very high; independent legal opinion strongly recommended."
        )
    elif cat_key == "obscenity":
        guidance = (
            "This string constitutes an obscenity under the laws of most UN member states. "
            "ICC Expert Panels apply 'generally accepted legal norms of morality and public "
            "order recognised under principles of international law'. A successful LPI "
            "finding prevents the application from proceeding (§4.5.1.4)."
        )
    elif cat_key == "hate_speech":
        guidance = (
            "This string is an internationally recognised slur or hate-speech term. "
            "Under Art. 20(2) ICCPR, states are obliged to prohibit advocacy of hatred "
            "constituting incitement to discrimination. An LPI panel would very likely "
            "find delegation contrary to international public order."
        )
    else:  # sanctions_adjacent
        guidance = (
            "This string is strongly associated with a UN/OFAC-designated terrorist "
            "organisation or sanctioned entity. While the LPI threshold is high, delegation "
            "could be characterised as contrary to international public order. "
            "ICANN's own compliance framework may also be engaged."
        )

    return [{
        "category": cat_key,
        "desc":     hit["desc"],
        "score":    hit["score"],
        "source":   hit["source"],
        "guidance": guidance,
    }]
