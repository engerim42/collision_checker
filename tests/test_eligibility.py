"""
Tests for RiskAssessor._check_eligibility — hard stops and advisory flags.
Uses a lightweight MockDB; no network access required.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
from lib.assessor import RiskAssessor


class MockDB:
    delegated_tlds = frozenset(["com", "net", "org", "gov"])
    special_use    = frozenset(["local", "localhost", "example", "test"])
    blocked_names  = {}
    reserved_names = {}
    iso_codes      = frozenset(["us", "gb", "deu", "gbr"])
    iso_names      = frozenset(["germany", "france", "united kingdom"])
    psl_private    = frozenset()
    un_macro       = frozenset(["africa", "europe", "americas", "asia", "oceania"])
    un_regions     = frozenset(["caribbean", "melanesia"])
    _cities        = {"paris": "Paris, France", "berlin": "Berlin, Germany",
                      "london": "London, United Kingdom"}

    def is_delegated(self, s):   return s in self.delegated_tlds
    def is_special_use(self, s): return s in self.special_use
    def is_blocked(self, s):     return s in self.blocked_names
    def is_reserved(self, s):    return s in self.reserved_names
    def is_iso_code(self, s):    return s in self.iso_codes
    def is_iso_name(self, s):    return s in self.iso_names
    def is_un_region(self, s):   return s in self.un_regions
    def is_un_macro(self, s):    return s in self.un_macro
    def get_city(self, s):       return self._cities.get(s)


class TestFormatValidation(unittest.TestCase):
    """Tests for _validate_format — structural invalidity caught before eligibility."""

    def setUp(self):
        self.assessor = RiskAssessor(MockDB())

    def _fmt(self, s):
        return self.assessor._validate_format(s)

    def test_numeric_only_invalid(self):
        r = self._fmt("123")
        self.assertIsNotNone(r)
        self.assertEqual(r["status"], "invalid")
        self.assertIn("Numeric", r["ineligible_category"])

    def test_numeric_only_single_digit_invalid(self):
        r = self._fmt("5")
        self.assertIsNotNone(r)
        self.assertEqual(r["status"], "invalid")
        self.assertIn("Numeric", r["ineligible_category"])

    def test_hyphens_positions_3_4_invalid(self):
        r = self._fmt("ab--foo")
        self.assertIsNotNone(r)
        self.assertEqual(r["status"], "invalid")
        self.assertIn("Third and Fourth", r["ineligible_category"])

    def test_hyphens_positions_3_4_other_chars(self):
        # fo--bar: positions 3 and 4 are both hyphens
        r = self._fmt("fo--bar")
        self.assertIsNotNone(r)
        self.assertEqual(r["status"], "invalid")

    def test_xn_prefix_passes_format_validation(self):
        # xn-- strings must NOT be caught by the positions-3-4 check; they reach eligibility
        r = self._fmt("xn--hello")
        self.assertIsNone(r)

    def test_single_embedded_hyphen_valid_format(self):
        # foo-bar has a hyphen but not in positions 3-4 — valid LDH label
        r = self._fmt("foo-bar")
        self.assertIsNone(r)

    def test_mixed_alpha_digit_valid_format(self):
        r = self._fmt("abc123")
        self.assertIsNone(r)


class TestEligibilityHardStops(unittest.TestCase):
    def setUp(self):
        self.chk = RiskAssessor(MockDB())._check_eligibility

    def test_single_char_ascii_ineligible(self):
        r = self.chk("a")
        self.assertEqual(r.status, "ineligible")
        self.assertIn("One/Two-Character", r.category)

    def test_two_char_ascii_ineligible(self):
        r = self.chk("ab")
        self.assertEqual(r.status, "ineligible")
        self.assertIn("One/Two-Character", r.category)

    def test_xn_prefix_ineligible(self):
        r = self.chk("xn--hello")
        self.assertEqual(r.status, "ineligible")
        self.assertIn("ACE", r.category)

    def test_delegated_tld_ineligible(self):
        r = self.chk("com")
        self.assertEqual(r.status, "ineligible")
        self.assertIn("Delegated", r.category)

    def test_special_use_ineligible(self):
        r = self.chk("local")
        self.assertEqual(r.status, "ineligible")
        self.assertIn("Protocol-Reserved", r.category)

    def test_iso_code_alpha3_ineligible(self):
        r = self.chk("deu")
        self.assertEqual(r.status, "ineligible")
        self.assertIn("ISO 3166-1", r.category)

    def test_iso_name_ineligible(self):
        r = self.chk("germany")
        self.assertEqual(r.status, "ineligible")
        self.assertIn("ISO 3166-1", r.category)

    def test_un_macro_region_reserved(self):
        r = self.chk("europe")
        self.assertEqual(r.status, "reserved")

    def test_capital_city_eligible_with_advisory_flag(self):
        r = self.chk("paris")
        self.assertTrue(r.eligible)
        self.assertTrue(r.advisory_flag)
        self.assertIn("city", r.advisory_note.lower())

    def test_un_subregion_eligible_with_advisory_flag(self):
        r = self.chk("caribbean")
        self.assertTrue(r.eligible)
        self.assertTrue(r.advisory_flag)

    def test_novel_string_fully_eligible(self):
        r = self.chk("mynovelstring")
        self.assertTrue(r.eligible)
        self.assertFalse(r.advisory_flag)


if __name__ == "__main__":
    unittest.main()
