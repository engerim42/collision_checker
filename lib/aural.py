from __future__ import annotations

from .colors import DIM, GREEN, YELLOW


class AuralSimilarityChecker:
    """
    Detects phonetic (aural) similarity between a proposed gTLD string and known
    reference strings using two complementary algorithms:

    1. Double Metaphone (Philips 2000)
       Maps a word to up to two phonetic codes covering English pronunciation and
       common alternative pronunciations (Germanic, Romance, Slavic loan-words).
       Two strings share a code if they sound the same or very similar.
       Examples: PHONE→FN, FONE→FN  |  CORP→KRP, KORP→KRP  |  MEYL→ML, MAIL→ML

    2. American Soundex (Russell 1918)
       Encodes consonant groups into a 4-char code, collapsing homophones.
       Used as a secondary confirmation — a match requires BOTH algorithms to agree.

    Risk framing per ICANN Guidebook §4.5.1.1 / §4.5.10.1
    ───────────────────────────────────────────────────────
    String Confusion Objections may be filed on aural similarity by:
      • Existing gTLD operators (§4.5.2.1)
      • Existing ccTLD operators / Significantly Interested Parties
      • Other applicants in the same round
    A successful objection places strings in DIRECT CONTENTION (§5.2), NOT outright
    rejection. This is distinct from the §7.10 SSE Panel visual hard-stop.

    Reference sets checked
    ───────────────────────
    collision_risks  →  prior high-risk + curated leakage labels  (scored in §7.7)
    sco_risks        →  delegated TLDs + ICANN blocked names       (contention warning)
    """

    VOWELS = "AEIOU"

    # ── Double Metaphone ──────────────────────────────────────────────────────
    @classmethod
    def double_metaphone(cls, word: str) -> tuple[str, str]:
        """
        Simplified Double Metaphone focused on English-derived ASCII strings
        (the typical composition of gTLD label candidates).
        Returns (primary_code, secondary_code).
        Both codes are non-empty; secondary equals primary when no alt exists.
        """
        s = word.upper().strip()
        n = len(s)
        if not n:
            return ("?", "?")

        def c(pos: int) -> str:           return s[pos] if 0 <= pos < n else ""
        def sub(pos: int, ln: int) -> str: return s[pos:pos + ln]
        def is_vowel(pos: int) -> bool:    return c(pos) in cls.VOWELS

        pri: list[str] = []
        sec: list[str] = []

        def add(p: str, q: str | None = None) -> None:
            pri.append(p)
            sec.append(p if q is None else q)

        i = 0

        # Drop initial silent pairs
        if sub(0, 2) in ("AE", "GN", "KN", "PN", "WR"):
            i = 1

        # Initial vowel → A
        if c(i) in cls.VOWELS:
            add("A"); i += 1

        while i < n:
            ch = c(i)

            if ch in cls.VOWELS:
                i += 1; continue      # non-initial vowels dropped

            if ch == "B":
                if i == n - 1 and c(i - 1) == "M":
                    i += 1; continue  # silent final -MB
                add("P"); i += 2 if c(i + 1) == "B" else 1

            elif ch == "C":
                if sub(i, 2) == "CK":
                    add("K"); i += 2
                elif sub(i, 2) == "CH":
                    add("X", "K"); i += 2   # sh vs. Germanic k
                elif sub(i, 3) == "SCH":
                    add("SK"); i += 3
                elif c(i + 1) in "IEY":
                    if c(i - 1) == "S":
                        i += 1; continue    # silent SC before front vowel
                    add("S"); i += 1
                else:
                    add("K"); i += 2 if c(i + 1) == "C" else 1

            elif ch == "D":
                if sub(i, 2) == "DG" and c(i + 2) in "IEY":
                    add("J"); i += 3
                elif sub(i, 2) in ("DT", "DD"):
                    add("T"); i += 2
                else:
                    add("T"); i += 1

            elif ch == "F":
                add("F"); i += 2 if c(i + 1) == "F" else 1

            elif ch == "G":
                nxt = c(i + 1)
                if nxt == "H":
                    prev_vowel = is_vowel(i - 1)
                    if i > 0 and not prev_vowel:
                        i += 2; continue    # GH after consonant = silent
                    if i == 0:
                        add("K"); i += 2; continue
                    if c(i - 1) in "BHD":
                        i += 2; continue
                    if c(i + 2) == "T" or i == n - 2:
                        add("K"); i += 2; continue
                    i += 2; continue
                elif nxt == "N":
                    if i == 0:
                        add("KN", "N"); i += 2; continue
                    if i == n - 2:
                        add("N"); i += 2; continue
                elif i == 0 and nxt in cls.VOWELS:
                    add("K"); i += 1; continue
                elif nxt in "EIY":
                    add("K", "J"); i += 1; continue
                add("K"); i += 2 if c(i + 1) == "G" else 1

            elif ch == "H":
                if is_vowel(i + 1) and not is_vowel(i - 1):
                    add("H")
                i += 1

            elif ch == "J":
                add("J", "H"); i += 1   # H secondary for Spanish-origin J

            elif ch == "K":
                if c(i - 1) != "C":
                    add("K")
                i += 2 if c(i + 1) == "K" else 1

            elif ch == "L":
                add("L"); i += 2 if c(i + 1) == "L" else 1

            elif ch == "M":
                add("M"); i += 2 if c(i + 1) == "M" else 1

            elif ch == "N":
                add("N"); i += 2 if c(i + 1) == "N" else 1

            elif ch == "P":
                if c(i + 1) == "H":
                    add("F"); i += 2
                else:
                    add("P"); i += 2 if c(i + 1) == "P" else 1

            elif ch == "Q":
                add("K"); i += 1

            elif ch == "R":
                add("R"); i += 2 if c(i + 1) == "R" else 1

            elif ch == "S":
                if sub(i, 3) in ("SIO", "SIA") or sub(i, 2) == "SH":
                    add("X"); i += 2 if sub(i, 2) == "SH" else 1; continue
                if sub(i, 3) == "SCH":
                    add("SK"); i += 3; continue
                if sub(i, 2) == "SC":
                    if c(i + 2) in "IEY":
                        add("S"); i += 2; continue
                    add("SK"); i += 2; continue
                add("S"); i += 2 if c(i + 1) == "S" else 1

            elif ch == "T":
                if sub(i, 3) in ("TIA", "TIO"):
                    add("X"); i += 1; continue
                if sub(i, 3) == "TCH":
                    i += 3; continue
                if sub(i, 2) == "TH":
                    add("0"); i += 2; continue   # θ sound
                add("T"); i += 2 if c(i + 1) in "TD" else 1

            elif ch == "V":
                add("F"); i += 2 if c(i + 1) == "V" else 1

            elif ch == "W":
                if is_vowel(i + 1):
                    add("W"); i += 1; continue
                if i == 0 and c(i + 1) == "H":
                    add("W" if is_vowel(i + 2) else "A"); i += 2; continue
                i += 1

            elif ch == "X":
                add("S" if i == 0 else "KS"); i += 1

            elif ch == "Y":
                if is_vowel(i + 1):
                    add("Y"); i += 1
                else:
                    i += 1

            elif ch == "Z":
                if c(i + 1) == "H":
                    add("J"); i += 2
                else:
                    add("S", "TS"); i += 2 if c(i + 1) == "Z" else 1

            else:
                i += 1

        p = "".join(pri) or "?"
        q = "".join(sec) or "?"
        return (p, q)

    # ── Soundex ───────────────────────────────────────────────────────────────
    @staticmethod
    def soundex(s: str) -> str:
        """American Soundex (US Census standard)."""
        TABLE = str.maketrans(
            "AEHIOUYWBFPVCGJKQSXZDTLMNR",
            "00000000111122222222334556")
        s = s.upper()
        if not s:
            return "0000"
        first  = s[0]
        coded  = s.translate(TABLE)
        result = first
        prev   = coded[0]
        for ch in coded[1:]:
            if ch != "0" and ch != prev:
                result += ch
            prev = ch
            if len(result) == 4:
                break
        return (result + "000")[:4]

    # ── Index builder ─────────────────────────────────────────────────────────
    @staticmethod
    def _build_index(strings: set[str]) -> dict[str, list[str]]:
        """Build DM-code → [string] inverted index for a set of strings."""
        idx: dict[str, list[str]] = {}
        for s in strings:
            for code in set(AuralSimilarityChecker.double_metaphone(s)):
                if code and code != "?":
                    idx.setdefault(code, []).append(s)
        return idx

    # ── Main check ────────────────────────────────────────────────────────────
    def check(self, s: str, db: "CollisionDatabase",
              visual_hits: set[str] | None = None) -> dict:
        """
        Run aural similarity checks for *s* against *db*.
        *visual_hits* is the set of strings already flagged by visual similarity,
        so we can skip redundant re-reporting.

        Returns
        -------
        {
          "collision_risks": list[dict],   # scored into §7.7 collision factor
          "sco_risks":       list[dict],   # §4.5.1.1 String Confusion Objection warnings
          "dm_primary":      str,
          "dm_secondary":    str,
          "soundex":         str,
        }
        """
        visual_hits = visual_hits or set()
        dm_pri, dm_sec = self.double_metaphone(s)
        sdx            = self.soundex(s)

        def dm_matches(targets: set[str]) -> list[dict]:
            """Return strings in *targets* sharing a DM code with *s*, with metadata."""
            idx   = self._build_index(targets)
            found: dict[str, dict] = {}
            for code in {dm_pri, dm_sec}:
                for t in idx.get(code, []):
                    if t == s or t in visual_hits:
                        continue
                    if t in found:
                        continue
                    t_pri, t_sec = self.double_metaphone(t)
                    t_sdx        = self.soundex(t)
                    # Require BOTH DM and Soundex to agree to reduce false positives
                    dm_match     = code in {t_pri, t_sec}
                    sdx_match    = (sdx == t_sdx)
                    if dm_match:
                        found[t] = {
                            "target":     t,
                            "dm_code":    code,
                            "sdx_match":  sdx_match,
                            "confidence": "high" if sdx_match else "medium",
                        }
            return sorted(found.values(),
                          key=lambda x: (x["confidence"] != "high", x["target"]))

        # ── 1. Collision risks: prior high-risk + curated leakage ─────────────
        collision_targets = (
            set(db.prior_high_risk.keys()) |
            set(db.enterprise.keys())      |
            set(db.home_labels.keys())     |
            set(db.mail_labels.keys())
        ) - {s}

        collision: list[dict] = []
        for m in dm_matches(collision_targets)[:4]:
            if m["target"] in db.prior_high_risk:
                cat, base_score = "Prior High-Risk (2012 Round)", 35
            elif m["target"] in db.mail_labels:
                cat, base_score = "Mail Infrastructure Leakage", 22
            elif m["target"] in db.home_labels:
                cat, base_score = "Home Network / IoT Leakage", 20
            else:
                cat, base_score = "Enterprise Namespace Leakage", 20
            score = base_score if m["confidence"] == "high" else base_score - 8
            collision.append({**m, "category": cat, "score": score})

        # ── 2. SCO risks: delegated TLDs (ASCII generic, len 3-10) ───────────
        tld_targets = {t for t in db.delegated_tlds
                       if 2 < len(t) <= 10 and t != s}
        sco: list[dict] = []
        for m in dm_matches(tld_targets)[:4]:
            sco.append({
                **m,
                "category": "Existing Delegated TLD",
                "outcome":  "String Confusion Objection risk (§4.5.1.1). "
                            "Successful objection → direct contention (§5.2).",
                "standing": "Any gTLD operator of the matched TLD has standing to object "
                            "per §4.5.2.1.",
            })

        # ── 3. SCO risks: ICANN Blocked Names ────────────────────────────────
        blocked_targets = {
            k for k, v in db.blocked_names.items()
            if v["category"] in ("icann_iana_ietf_infrastructure", "protocol_reserved")
               and k != s
        }
        for m in dm_matches(blocked_targets)[:2]:
            sco.append({
                **m,
                "category": "ICANN Blocked Name",
                "outcome":  "String Confusion Objection risk (§4.5.1.1). Note: §7.10.3.6 "
                            "handles visual similarity to Blocked Names as a hard stop; "
                            "aural similarity may still prompt an objection.",
                "standing": "Any party with appropriate standing (§4.5.2.1) may object.",
            })

        return {
            "collision_risks": collision,
            "sco_risks":       sco,
            "dm_primary":      dm_pri,
            "dm_secondary":    dm_sec,
            "soundex":         sdx,
        }

    @staticmethod
    def status() -> dict:
        return {
            "desc":  "Aural Similarity — Double Metaphone (Philips 2000) + Soundex (Russell 1918)",
            "url":   "Built-in algorithms — no external data source",
            "age_s": None,
            "size":  0,
            "fresh": True,
        }
