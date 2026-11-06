"""
holiday_api.py
Role 2 — API Client

Fetches public holidays from the free Nager.Date API (no API key needed).
Supports one country, or a whole region: Africa, Americas, Europe.

Requires: requests   (see requirements.txt)

Failures are never silent. Every country that returns no holidays comes back
as a Failure — a string that behaves exactly like the country code but also
carries a .reason, so you can tell "this country is not covered" apart from
"the network is down". If every country fails for a reason that is not about
the country (network, rate limit, server), the whole call raises instead of
returning an empty list.

To save results as JSON, use to_json_dict() or save_json() at the bottom.
"""

import json
import random
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import requests

# Country codes (ISO 2-letter) grouped by region.
# Note: the API does not cover every country. Unsupported ones are
# skipped and reported back instead of crashing the program.
REGIONS = {
    "africa": [
        "DZ", "AO", "BJ", "BW", "BF", "BI", "CM", "CV", "CF", "TD", "KM",
        "CG", "CD", "CI", "DJ", "EG", "GQ", "ER", "SZ", "ET", "GA", "GM",
        "GH", "GN", "GW", "KE", "LS", "LR", "LY", "MG", "MW", "ML", "MR",
        "MU", "MA", "MZ", "NA", "NE", "NG", "RW", "ST", "SN", "SC", "SL",
        "SO", "ZA", "SS", "SD", "TZ", "TG", "TN", "UG", "ZM", "ZW",
    ],
    "americas": [
        "US", "CA", "MX", "BR", "AR", "CL", "CO", "PE", "VE", "EC", "BO",
        "PY", "UY", "CR", "PA", "GT", "HN", "NI", "SV", "CU", "DO", "JM",
        "BS", "BB", "BZ", "HT", "TT", "GY", "SR",
    ],
    "europe": [
        "AL", "AD", "AT", "BY", "BE", "BA", "BG", "HR", "CY", "CZ", "DK",
        "EE", "FI", "FR", "DE", "GR", "HU", "IS", "IE", "IT", "LV", "LI",
        "LT", "LU", "MT", "MD", "MC", "ME", "NL", "MK", "NO", "PL", "PT",
        "RO", "SM", "RS", "SK", "SI", "ES", "SE", "CH", "UA", "GB", "VA",
    ],
}

# Status codes worth retrying: the request may succeed on a second attempt.
RETRY_STATUS_CODES = frozenset({429, 500, 502, 503, 504})

# Reasons a country can end up in the failed list.
NOT_FOUND = "not_found"          # 404 — country code unknown to the API
NO_DATA = "no_data"              # 204 — valid country, nothing published
NETWORK = "network"              # could not reach the API at all
RATE_LIMITED = "rate_limited"    # 429 persisted through every retry
SERVER_ERROR = "server_error"    # 5xx (or other unexpected status)
BAD_RESPONSE = "bad_response"    # 200, but the body was not readable JSON

# Reasons that mean "the problem is the service or our connection", not the country.
CONNECTIVITY_REASONS = frozenset({NETWORK, RATE_LIMITED, SERVER_ERROR})


class HolidayAPIError(Exception):
    """Raised when the holiday API cannot give us usable data."""


class NetworkError(HolidayAPIError):
    """The API could not be reached: DNS, connection refused, or timeout."""


class CountryNotFoundError(HolidayAPIError):
    """The API does not know this country code (HTTP 404)."""


class BadResponseError(HolidayAPIError):
    """The API answered 200 but the body was not valid JSON."""


class HTTPStatusError(HolidayAPIError):
    """The API returned an unexpected status code."""

    def __init__(self, status_code, message):
        super().__init__(message)
        self.status_code = status_code


class Failure(str):
    """
    A country code that produced no holidays, with the reason attached.

    It IS the country code — it subclasses str — so code written against the
    old version still works unchanged: ", ".join(failed), "GB" in failed,
    and comparing to "GB" all behave normally. The extra .reason attribute is
    what tells you *why*:

        failed[0]         -> 'DJ'                 (the code)
        failed[0].reason  -> 'no_data'            (why)
        repr(failed[0])   -> 'DJ (no_data)'       (both, for printing)
    """

    def __new__(cls, code, reason):
        obj = super().__new__(cls, code)
        obj.code = code
        obj.reason = reason
        return obj

    def __repr__(self):
        return f"{self.code} ({self.reason})"


class HolidayAPIClient:
    BASE_URL = "https://date.nager.at/api/v3"

    def __init__(self, timeout=10, max_retries=3, backoff=0.5, max_workers=8):
        """
        timeout      seconds to wait for each request
        max_retries  extra attempts after a network error or 429/5xx
        backoff      base delay in seconds; doubles each retry, with jitter
        max_workers  concurrent requests when fetching a whole region
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff = backoff
        self.max_workers = max_workers

    # ---------- One country ----------
    def fetch_holidays(self, country_code, year):
        """
        Fetch holidays for one country and one year.
        Returns: list of dicts with keys: name, local_name, date, types, country

        Raises CountryNotFoundError if the code is unknown, NetworkError if the
        API cannot be reached, HTTPStatusError for an unexpected status, and
        BadResponseError if the body is not JSON. Retries happen inside _get.
        """
        country_code = str(country_code).strip().upper()
        url = f"{self.BASE_URL}/PublicHolidays/{year}/{country_code}"

        response = self._get(url)

        if response.status_code == 204:      # "No Content": no data for it
            return []
        if response.status_code == 404:
            raise CountryNotFoundError(f"Country code '{country_code}' not found.")
        if response.status_code != 200:
            raise HTTPStatusError(
                response.status_code,
                f"API error (status {response.status_code}).",
            )

        try:
            raw_holidays = response.json()
        except ValueError as error:
            raise BadResponseError("API returned invalid JSON.") from error

        return [self._parse_holiday(item) for item in raw_holidays]

    # ---------- A whole region ----------
    def fetch_region_holidays(self, region, year):
        """
        Fetch holidays for every country in a region.

        region: "africa", "americas" or "europe"
        Returns: (holidays, failed)
          holidays = list of holiday dicts (all countries together)
          failed   = list of Failure (each is a country code string with a
                     .reason attribute saying why that country has no data)

        Raises HolidayAPIError if EVERY country failed for a connectivity
        reason — that means the service or our connection is down, and
        returning an empty list would be misleading.
        """
        region = str(region).strip().lower()
        if region not in REGIONS:
            raise HolidayAPIError(
                f"Unknown region '{region}'. Choose from: {', '.join(REGIONS)}."
            )

        def fetch_one(code):
            try:
                return code, self.fetch_holidays(code, year), None
            except CountryNotFoundError:
                return code, None, NOT_FOUND
            except BadResponseError:
                return code, None, BAD_RESPONSE
            except HTTPStatusError as error:
                reason = RATE_LIMITED if error.status_code == 429 else SERVER_ERROR
                return code, None, reason
            except NetworkError:
                return code, None, NETWORK
            except HolidayAPIError:
                return code, None, SERVER_ERROR

        # Run several requests at the same time so 50+ countries
        # don't take minutes. max_workers defaults to 8, which is polite.
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            results = list(pool.map(fetch_one, REGIONS[region]))

        holidays, failed = [], []
        for code, data, reason in results:
            if data:
                # Copy rather than mutate: _parse_holiday returns fresh dicts,
                # but building a new one keeps this method free of side effects.
                for holiday in data:
                    holidays.append({**holiday, "region": region})
            else:
                failed.append(Failure(code, reason or NO_DATA))

        # If nothing came back and every failure was about connectivity, the
        # caller must not mistake an outage for "these countries have no data".
        if not holidays and failed and all(f.reason in CONNECTIVITY_REASONS for f in failed):
            raise HolidayAPIError(
                f"Could not reach the holiday API: all {len(failed)} countries in "
                f"'{region}' failed ({failed[0].reason}). Check your network "
                "connection, or the service may be temporarily unavailable."
            )

        return holidays, failed

    def fetch_all_regions(self, year):
        """Africa + Americas + Europe together."""
        all_holidays, all_failed = [], []
        for region in REGIONS:
            holidays, failed = self.fetch_region_holidays(region, year)
            all_holidays.extend(holidays)
            all_failed.extend(failed)
        return all_holidays, all_failed

    # ---------- Internals ----------
    def _get(self, url):
        """
        GET with retries on transient failures.

        Only network errors and 429/5xx are retried; a 404 is a real answer and
        is returned immediately. Backoff is exponential with jitter, so retrying
        threads spread out instead of retrying in lockstep.
        """
        last_error = None

        for attempt in range(self.max_retries + 1):
            try:
                response = requests.get(url, timeout=self.timeout)
            except requests.exceptions.RequestException as error:
                last_error = NetworkError(f"Network problem: {error}")
            else:
                if response.status_code not in RETRY_STATUS_CODES:
                    return response
                last_error = HTTPStatusError(
                    response.status_code,
                    f"Transient API error (status {response.status_code}).",
                )

            if attempt < self.max_retries:
                delay = self.backoff * (2 ** attempt)
                time.sleep(delay * (0.5 + random.random()))

        raise last_error

    @staticmethod
    def _parse_holiday(item):
        """Keep only the fields our project needs."""
        return {
            "name": item.get("name"),
            "local_name": item.get("localName"),
            "date": item.get("date"),            # "YYYY-MM-DD" string
            "types": item.get("types", []),
            "country": item.get("countryCode"),
        }


# ---------- JSON output ----------
def to_json_dict(holidays, failed=None):
    """
    Turn a result from this client into a plain dict, ready to be written as JSON.

    The shape is stable, so Role 3 (or anything else) can rely on it:

        {
          "generated_at": "2026-02-14T10:30:00+00:00",
          "count": 2,
          "holidays": [
            {"name": "...", "local_name": "...", "date": "2026-01-01",
             "types": ["Public"], "country": "GB", "region": "europe"}
          ],
          "failed": [{"code": "DJ", "reason": "no_data"}]
        }
    """
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "count": len(holidays),
        "holidays": holidays,
        "failed": [{"code": f.code, "reason": f.reason} for f in (failed or [])],
    }


def save_json(holidays, path, failed=None):
    """Write holidays to a JSON file and return the path. Creates/overwrites it."""
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(to_json_dict(holidays, failed), handle, indent=2, ensure_ascii=False)
    return path


if __name__ == "__main__":
    # Quick self-test: run `python holiday_api.py`
    client = HolidayAPIClient()

    print("-- single country --")
    try:
        holidays = client.fetch_holidays("GB", 2026)
        print(f"GB 2026: {len(holidays)} holidays")
        for holiday in holidays[:3]:
            print(f"   {holiday['date']}  {holiday['name']}")
    except HolidayAPIError as err:
        print("Error:", err)

    print("\n-- whole region, saved as JSON --")
    try:
        holidays, failed = client.fetch_region_holidays("europe", 2026)
        print(f"Found {len(holidays)} holidays in Europe.")
        if failed:
            print("No data for:")
            for failure in failed:
                print(f"   {failure.code:<3} {failure.reason}")

        written = save_json(holidays, "holidays.json", failed)
        print(f"\nWrote {len(holidays)} holidays to {written}")
    except HolidayAPIError as err:
        print("Error:", err)
