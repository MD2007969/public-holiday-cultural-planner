
from datetime import date, datetime


def _get_value(holiday, key):
    if isinstance(holiday, dict):
        return holiday.get(key)
    return getattr(holiday, key, None)


def _normalise_name(name):
    return " ".join(str(name or "").strip().lower().split())


def _normalise_date(value):
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if value:
        try:
            return date.fromisoformat(str(value)[:10]).isoformat()
        except ValueError:
            return None
    return None


def _holiday_record(holiday):
    return {
        "name": _get_value(holiday, "name")
        or _get_value(holiday, "localName"),
        "date": _normalise_date(_get_value(holiday, "date")),
    }


def compare_holidays(first_country_holidays, second_country_holidays):
    first = [_holiday_record(item) for item in first_country_holidays]
    second = [_holiday_record(item) for item in second_country_holidays]

    first_names = {
        _normalise_name(item["name"])
        for item in first if item["name"]
    }
    second_names = {
        _normalise_name(item["name"])
        for item in second if item["name"]
    }

    shared_names = first_names & second_names

    shared = [
        item for item in first
        if _normalise_name(item["name"]) in shared_names
    ]

    only_first = [
        item for item in first
        if _normalise_name(item["name"]) not in second_names
    ]

    only_second = [
        item for item in second
        if _normalise_name(item["name"]) not in first_names
    ]

    first_dates = {item["date"] for item in first if item["date"]}
    second_dates = {item["date"] for item in second if item["date"]}

    return {
        "total_holidays_country1": len(first),
        "total_holidays_country2": len(second),
        "shared_holidays": shared,
        "shared_holiday_names": [item["name"] for item in shared],
        "overlapping_dates": sorted(first_dates & second_dates),
        "holidays_only_first": only_first,
        "holidays_only_second": only_second,
    }
