"""OOP data models shared by the project modules."""


class Country:
    """Represent a country supported by the planner."""
    def __init__(self, code, name):
        self.code = code
        self.name = name


class Holiday:
    """Represent one public holiday."""
    def __init__(self, name, date, country_code, holiday_type=None, local_name=None):
        self.name = name
        self.date = date
        self.country_code = country_code
        self.holiday_type = holiday_type or []
        self.local_name = local_name or name

    def to_dict(self):
        """Return the holiday as a dictionary."""
        return {"name": self.name, "date": self.date, "country_code": self.country_code,
                "types": self.holiday_type, "local_name": self.local_name}
