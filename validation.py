"""Input validation helpers using regular expressions."""
import re


def is_valid_country_code(country_code):
    """Check the two-letter country-code format."""
    return bool(re.fullmatch(r"[A-Za-z]{2}", country_code or ""))


def is_valid_year(year):
    """Check for exactly four digits."""
    return bool(re.fullmatch(r"\d{4}", str(year)))
