# models.py
# Country and Holiday classes for the Public Holiday & Cultural Awareness Planner
# Made by Favour Onu (Models role)

from datetime import datetime

class Country:
    """
    Simple class to represent a country.
    Holds the country code and name.
    """
    def __init__(self, code, name):
        # code should be like "NG", "US", "GB"
        self.code = code.upper()
        self.name = name
        self.holidays = []  # list of Holiday objects for this country

    def add_holiday(self, holiday):
        """Add a holiday to this country."""
        self.holidays.append(holiday)

    def get_holidays_sorted(self):
        """Return holidays sorted by date."""
        return sorted(self.holidays, key=lambda h: h.date)

    def group_holidays_by_month(self):
        """Group holidays by month name. Returns a dictionary."""
        groups = {}
        for holiday in self.get_holidays_sorted():
            month_name = holiday.date.strftime("%B")  # like "January"
            if month_name not in groups:
                groups[month_name] = []
            groups[month_name].append(holiday)
        return groups

    def __str__(self):
        return f"{self.name} ({self.code})"

    def __repr__(self):
        return f"Country(code='{self.code}', name='{self.name}')"


class Holiday:
    """
    Class for a single public holiday.
    Has name, date, type, and the country it belongs to.
    """
    def __init__(self, name, date, holiday_type, country):
        self.name = name
        # date can be a string "YYYY-MM-DD" or a datetime object
        if isinstance(date, str):
            self.date = datetime.strptime(date, "%Y-%m-%d")
        else:
            self.date = date
        self.type = holiday_type  # e.g. "Public", "Bank", etc.
        self.country = country    # Country object

    def get_weekday(self):
        """Return the day of the week, like 'Monday'."""
        return self.date.strftime("%A")

    def get_month(self):
        """Return the month name."""
        return self.date.strftime("%B")

    def get_formatted_date(self):
        """Nice readable date, e.g. '1 January 2026'."""
        return self.date.strftime("%d %B %Y")

    def __str__(self):
        return f"{self.name} - {self.get_formatted_date()} ({self.get_weekday()}) [{self.type}]"

    def __repr__(self):
        return f"Holiday(name='{self.name}', date='{self.date.date()}', type='{self.type}')"
