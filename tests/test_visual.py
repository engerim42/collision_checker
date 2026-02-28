"""
Tests for VisualSimilarityChecker — Levenshtein edit distance.
Pure algorithmic function; no network access required.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
from lib.visual import VisualSimilarityChecker


class TestLevenshtein(unittest.TestCase):
    lev = staticmethod(VisualSimilarityChecker.levenshtein)

    def test_identical(self):
        self.assertEqual(self.lev("corp", "corp"), 0)

    def test_empty_strings(self):
        self.assertEqual(self.lev("", ""), 0)

    def test_one_substitution(self):
        self.assertEqual(self.lev("corp", "carp"), 1)

    def test_one_insertion(self):
        self.assertEqual(self.lev("abc", "abcd"), 1)

    def test_one_deletion(self):
        self.assertEqual(self.lev("abcd", "abc"), 1)

    def test_short_circuit_on_large_length_gap(self):
        """Length difference > 2 immediately returns 99."""
        self.assertEqual(self.lev("a", "abcde"), 99)

    def test_symmetric(self):
        self.assertEqual(self.lev("mail", "meyl"), self.lev("meyl", "mail"))


if __name__ == "__main__":
    unittest.main()
