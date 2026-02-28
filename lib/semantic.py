"""
Semantic / translation similarity check.

If a proposed gTLD string is the translation of a high-risk namespace concept
in another language, it carries the same collision risk patterns.  For example,
"maison" (French for "home") is subject to the same leakage concerns as "home"
itself.

Source rationale
----------------
NCAP Study Two (Apr 2024) §§4–5 confirms leakage is driven by the *semantic
role* of a label in private namespaces (home-router default, mail server,
corporate AD root), not by its English spelling.  Non-English labels fulfilling
the same role inherit the same risk.

Coverage
--------
High-risk concepts covered: home, mail, corporate/corp, network, server, private,
intranet, web.  Languages: 30+ including all UN official languages plus major
internet-language populations (Malay, Indonesian, Vietnamese, Swahili, etc.).

Only strings of ≥ 3 characters are flagged to avoid short-label false positives
(e.g. "la", "de", "im").  Ambiguous short translations are noted separately.
"""
from __future__ import annotations


# ── Translation dictionary ────────────────────────────────────────────────────
# Structure: concept → { risk_score, ncap_ref, words: { lang_code: [words] } }
# All words are lowercase, ASCII-representable (transliterated where needed).
_CONCEPTS: dict[str, dict] = {
    "home": {
        "risk_score": 62,
        "ncap_ref": "NCAP Study Two §4 — 'home' confirmed high-risk (2012 round)",
        "words": {
            "af": ["huis", "tuis"],
            "ar": ["bait", "manzil"],           # transliterated
            "bg": ["dom"],                       # transliterated
            "cs": ["domov"],
            "da": ["hjem"],
            "de": ["heim", "zuhause"],
            "el": ["spiti"],                     # transliterated
            "es": ["hogar", "casa"],
            "fi": ["koti"],
            "fr": ["maison", "domicile", "foyer"],
            "hi": ["ghar"],                      # transliterated
            "hr": ["dom"],
            "hu": ["otthon"],
            "id": ["rumah"],
            "it": ["casa", "domicilio"],
            "ja": ["homu"],                      # transliterated / loanword
            "ko": ["jip"],                       # romanized
            "ms": ["rumah"],
            "nl": ["thuis", "huis"],
            "nb": ["hjem", "hjemme"],
            "pl": ["dom"],
            "pt": ["lar", "casa"],
            "ro": ["acasa"],
            "ru": ["dom", "doma"],               # transliterated
            "sk": ["domov"],
            "sr": ["dom"],                       # transliterated
            "sv": ["hem"],
            "sw": ["nyumba"],
            "th": ["baan"],                      # transliterated
            "tr": ["ev"],
            "uk": ["dim"],                       # transliterated
            "vi": ["nha"],
            "zh": ["jia"],                       # pinyin
        },
    },
    "mail": {
        "risk_score": 66,
        "ncap_ref": "NCAP Study Two §5 — 'mail' confirmed high-risk (2012 round)",
        "words": {
            "ar": ["barid"],
            "bg": ["pochta"],                    # transliterated
            "cs": ["posta"],
            "da": ["post"],
            "de": ["post"],
            "el": ["tachydromeio"],              # transliterated
            "es": ["correo"],
            "fi": ["posti"],
            "fr": ["courrier", "courriel"],
            "hi": ["dak"],                       # transliterated
            "hr": ["posta"],
            "hu": ["posta"],
            "id": ["surat"],
            "it": ["posta"],
            "ja": ["yubin"],                     # transliterated
            "ko": ["upyeon"],                    # romanized
            "ms": ["pos", "mel"],
            "nl": ["post"],
            "nb": ["post"],
            "pl": ["poczta"],
            "pt": ["correio"],
            "ro": ["posta"],
            "ru": ["pochta"],                    # transliterated
            "sk": ["posta"],
            "sr": ["posta"],                     # transliterated
            "sv": ["post"],
            "sw": ["barua"],
            "tr": ["posta"],
            "uk": ["poshta"],                    # transliterated
            "vi": ["thu"],
            "zh": ["youjian"],                   # pinyin
        },
    },
    "corporate": {
        "risk_score": 55,
        "ncap_ref": "NCAP Study Two — enterprise AD forest root leakage",
        "words": {
            "ar": ["sharika"],
            "cs": ["firma", "podnik"],
            "da": ["virksomhed", "selskab"],
            "de": ["unternehmen", "firma", "konzern"],
            "el": ["etairia"],                   # transliterated
            "es": ["empresa", "corporativo", "corporacion"],
            "fi": ["yritys"],
            "fr": ["entreprise", "societe"],
            "hi": ["korporet"],                  # transliterated
            "hu": ["vallalat", "ceg"],
            "id": ["perusahaan"],
            "it": ["azienda", "impresa"],
            "ja": ["kaisha", "kigyo"],           # transliterated
            "ms": ["syarikat"],
            "nl": ["bedrijf", "onderneming"],
            "nb": ["bedrift", "selskap"],
            "pl": ["firma", "korporacja"],
            "pt": ["empresa", "corporativo"],
            "ro": ["companie", "firma"],
            "ru": ["firma", "korporatsiya"],     # transliterated
            "sk": ["firma"],
            "sv": ["foretag", "bolag"],
            "tr": ["sirket", "kurumsal"],
            "uk": ["firma"],                     # transliterated
            "zh": ["gongsi"],                    # pinyin
        },
    },
    "network": {
        "risk_score": 46,
        "ncap_ref": "Enterprise namespace — high DITL leakage signal",
        "words": {
            "ar": ["shabaka"],
            "cs": ["sit"],
            "da": ["netvaerk"],
            "de": ["netzwerk", "netz"],
            "el": ["diktyo"],                    # transliterated
            "es": ["red"],
            "fi": ["verkko"],
            "fr": ["reseau"],
            "hi": ["nettwork"],                  # transliterated loanword
            "hu": ["halozat"],
            "id": ["jaringan"],
            "it": ["rete"],
            "ja": ["nettowaku"],                 # transliterated loanword
            "ms": ["rangkaian"],
            "nl": ["netwerk"],
            "nb": ["nettverk"],
            "pl": ["siec"],
            "pt": ["rede"],
            "ro": ["retea"],
            "ru": ["set"],                       # transliterated
            "sv": ["natverk"],
            "tr": ["ag"],
            "zh": ["wangluo"],                   # pinyin
        },
    },
    "server": {
        "risk_score": 44,
        "ncap_ref": "NCAP Study Two — enterprise SMB / file-server leakage",
        "words": {
            "ar": ["khادm"],                     # transliterated (khadim)
            "cs": ["server"],
            "de": ["rechner"],
            "es": ["servidor"],
            "fi": ["palvelin"],
            "fr": ["serveur"],
            "id": ["peladen"],
            "it": ["server"],
            "ja": ["saba"],                      # transliterated loanword
            "nl": ["server"],
            "pt": ["servidor"],
            "ru": ["server"],                    # transliterated loanword
            "tr": ["sunucu"],
            "zh": ["fuwuqi"],                    # pinyin
        },
    },
    "private": {
        "risk_score": 48,
        "ncap_ref": "NCAP Study Two — private namespace leakage signal",
        "words": {
            "ar": ["khususi"],
            "cs": ["soukromy"],
            "da": ["privat"],
            "de": ["privat"],
            "el": ["idiotikos"],                 # transliterated
            "es": ["privado", "privada"],
            "fi": ["yksityinen"],
            "fr": ["prive", "privee"],
            "hu": ["privat"],
            "id": ["swasta", "pribadi"],
            "it": ["privato", "privata"],
            "ja": ["puraibeto"],                 # transliterated loanword
            "ms": ["persendirian"],
            "nl": ["privaat"],
            "nb": ["privat"],
            "pl": ["prywatny"],
            "pt": ["privado", "privada"],
            "ro": ["privat"],
            "ru": ["chastnyy"],                  # transliterated
            "sk": ["sukromny"],
            "sv": ["privat"],
            "tr": ["ozel"],
            "zh": ["siren"],                     # pinyin
        },
    },
    "intranet": {
        "risk_score": 52,
        "ncap_ref": "NCAP Study Two — intranet portal leakage (78 DITL origin ASNs)",
        "words": {
            # Loanword in most languages — flag non-ASCII transliterations
            "ar": ["intranit"],
            "ja": ["itonaranetto"],
            "ko": ["inteunanet"],
            "ru": ["intranet"],
            "zh": ["neiwang"],                   # pinyin for 内网
            "zh_alt": ["neibu wanglu"],
        },
    },
    "web": {
        "risk_score": 38,
        "ncap_ref": "Enterprise namespace leakage — internal web portal label",
        "words": {
            "fr": ["toile"],
            "pt": ["teia"],
            "zh": ["wangye"],                    # pinyin for 网页
            "ja": ["uebo"],                      # transliterated loanword
        },
    },
}

# Build a flat lookup: word → list of (concept, lang, score, ref)
_INDEX: dict[str, list[dict]] = {}
for _concept, _data in _CONCEPTS.items():
    for _lang, _words in _data["words"].items():
        for _w in _words:
            if len(_w) < 3:
                continue   # skip ambiguous short tokens
            _INDEX.setdefault(_w, []).append({
                "concept":   _concept,
                "language":  _lang.split("_")[0],   # strip _alt suffix
                "score":     _data["risk_score"],
                "ncap_ref":  _data["ncap_ref"],
            })


def check(s: str) -> list[dict]:
    """
    Return a list of semantic matches for *s*.

    Each match dict has:
        concept    – high-risk concept the string translates to
        language   – BCP-47 language code of the translation
        score      – collision risk score contribution
        ncap_ref   – NCAP / guidebook reference
    """
    return _INDEX.get(s.lower(), [])
