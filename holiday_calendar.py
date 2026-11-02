"""Helpers for sorting and preparing holiday records."""


def sort_holidays(holidays):
    """Return holiday records sorted by ISO date."""
    return sorted(holidays, key=lambda holiday: holiday.get("date", ""))


def get_holiday_summary(holidays):
    """Return the number of holiday records."""
    return len(holidays)
