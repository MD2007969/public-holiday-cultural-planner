"""Public holiday API client. Initial provider: Nager.Date."""
import requests

BASE_URL = "https://date.nager.at/api/v3"


class HolidayAPIClient:
    """Retrieve public holidays from the Nager.Date API."""
    def get_public_holidays(self, year, country_code):
        """Return holiday records; raise clear exceptions on request/JSON errors."""
        url = f"{BASE_URL}/PublicHolidays/{year}/{country_code.upper()}"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list):
            raise ValueError("The holiday API returned an unexpected response.")
        return data
