
import pytest

from validators import validate_country_code, validate_year


def test_valid_country_code():
    assert validate_country_code("NG") == "NG"


def test_country_code_is_case_insensitive():
    assert validate_country_code("ng") == "NG"


def test_unsupported_country_code():
    with pytest.raises(ValueError, match="not supported"):
        validate_country_code("XX")


def test_empty_country_code():
    with pytest.raises(ValueError, match="Invalid country code"):
        validate_country_code("")


def test_valid_year():
    assert validate_year(2026) == 2026


def test_year_below_range():
    with pytest.raises(ValueError, match="between 2000 and 2100"):
        validate_year(1999)


def test_year_above_range():
    with pytest.raises(ValueError, match="between 2000 and 2100"):
        validate_year(2200)


def test_invalid_year():
    with pytest.raises(ValueError, match="valid number"):
        validate_year("hello")
