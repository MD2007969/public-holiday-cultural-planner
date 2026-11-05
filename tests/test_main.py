"""Unit tests for the main application's display-data helpers."""

import unittest
from types import SimpleNamespace

from main import COUNTRIES, get_value, holiday_to_dict


class MainHelperTests(unittest.TestCase):
    def test_country_codes_include_required_examples(self):
        self.assertEqual(COUNTRIES["Nigeria"], "NG")
        self.assertEqual(COUNTRIES["United States"], "US")
        self.assertEqual(COUNTRIES["United Kingdom"], "GB")

    def test_get_value_reads_dictionary(self):
        self.assertEqual(get_value({"name": "Eid"}, "name"), "Eid")
        self.assertEqual(get_value({}, "name", "unknown"), "unknown")

    def test_get_value_reads_object_attribute(self):
        holiday = SimpleNamespace(name="Eid al-Fitr")
        self.assertEqual(get_value(holiday, "name"), "Eid al-Fitr")

    def test_holiday_to_dict_normalizes_dictionary(self):
        holiday = {
            "name": "Eid al-Fitr",
            "date": "2026-03-20",
            "type": "Public",
            "description": "A religious celebration",
        }
        result = holiday_to_dict(holiday, "NG")
        self.assertEqual(result["name"], "Eid al-Fitr")
        self.assertEqual(result["date"], "2026-03-20")
        self.assertEqual(result["country_code"], "NG")
        self.assertEqual(result["holiday_type"], "Public")
        self.assertEqual(result["description"], "A religious celebration")

    def test_holiday_to_dict_normalizes_model_like_object(self):
        holiday = SimpleNamespace(
            name="New Year",
            date="2026-01-01",
            country_code="GB",
            holiday_type="Public holiday",
            description="",
        )
        result = holiday_to_dict(holiday, "NG")
        self.assertEqual(result["name"], "New Year")
        self.assertEqual(result["country_code"], "GB")
        self.assertEqual(result["holiday_type"], "Public holiday")

    def test_missing_holiday_name_gets_safe_fallback(self):
        result = holiday_to_dict({"date": "2026-01-01"}, "NG")
        self.assertEqual(result["name"], "Unnamed holiday")


if __name__ == "__main__":
    unittest.main()
