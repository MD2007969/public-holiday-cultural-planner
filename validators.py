
import re


# Supported country codes in the application
SUPPORTED_COUNTRIES = {
    "NG", "US", "GB", "GH",
    "CA", "IN", "ZA", "KE"
}


def validate_country_code(country_code):
    """Check that the country code is valid and supported."""

    if not isinstance(country_code, str):
        raise ValueError("Country code must be text.")

    country_code = country_code.strip().upper()

    if not re.fullmatch(r"[A-Z]{2}", country_code):
        raise ValueError(
            "Invalid country code. Use a two-letter code."
        )

    if country_code not in SUPPORTED_COUNTRIES:
        raise ValueError(
            f"Country code '{country_code}' is not supported."
        )

    return country_code


def validate_year(year):
    """Check that the year is between 2000 and 2100."""

    try:
        year = int(year)
    except (TypeError, ValueError):
        raise ValueError("Year must be a valid number.")

    if not 2000 <= year <= 2100:
        raise ValueError(
            "Year must be between 2000 and 2100."
        )

    return year
