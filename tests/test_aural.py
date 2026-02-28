"""
Tests for AuralSimilarityChecker — Double Metaphone and Soundex.
Pure algorithmic functions; no network access required.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
from lib.aural import AuralSimilarityChecker


class TestDoubleMetaphone(unittest.TestCase):
    dm = staticmethod(AuralSimilarityChecker.double_metaphone)

    def test_empty(self):
        self.assertEqual(self.dm(""), ("?", "?"))

    def test_corp(self):
        p, _ = self.dm("corp")
        self.assertEqual(p, "KRP")

    def test_mail(self):
        p, _ = self.dm("mail")
        self.assertEqual(p, "ML")

    def test_home(self):
        # Initial H before a vowel is suppressed when the preceding char is empty string,
        # because "" in "AEIOU" is True in Python — so H at position 0 is not emitted.
        p, _ = self.dm("home")
        self.assertEqual(p, "M")

    def test_phone_fone_share_code(self):
        """phone and fone are phonetically equivalent → at least one shared DM code."""
        phone_codes = set(self.dm("phone"))
        fone_codes  = set(self.dm("fone"))
        self.assertTrue(phone_codes & fone_codes)

    def test_corp_korp_share_code(self):
        corp_codes = set(self.dm("corp"))
        korp_codes = set(self.dm("korp"))
        self.assertTrue(corp_codes & korp_codes)

    def test_mail_meyl_share_code(self):
        mail_codes = set(self.dm("mail"))
        meyl_codes = set(self.dm("meyl"))
        self.assertTrue(mail_codes & meyl_codes)


class TestSoundex(unittest.TestCase):
    sdx = staticmethod(AuralSimilarityChecker.soundex)

    def test_always_four_chars(self):
        for word in ["a", "hello", "corp", "mail", "home", "x", "world"]:
            self.assertEqual(len(self.sdx(word)), 4, f"soundex({word!r}) is not 4 chars")

    def test_empty(self):
        self.assertEqual(self.sdx(""), "0000")

    def test_robert_rupert(self):
        """Classic American Soundex equivalence example."""
        self.assertEqual(self.sdx("robert"), self.sdx("rupert"))

    def test_mail_meyl(self):
        self.assertEqual(self.sdx("mail"), self.sdx("meyl"))

    def test_corp(self):
        self.assertEqual(self.sdx("corp"), "C610")


if __name__ == "__main__":
    unittest.main()
