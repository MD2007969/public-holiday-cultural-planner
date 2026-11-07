# culture_guide.py
# Role 4 - CultureGuideGenerator
# Uses Gemini to explain holidays and give comparison notes

import os
import logging
import time

# simple logging setup (does not print the API key)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CultureGuideGenerator:
    # messages shown when Gemini is down or key is missing
    FALLBACK_GUIDE = (
        "Sorry, could not get the cultural explanation right now. "
        "Check your internet or API key. You can still look up the holiday online."
    )

    FALLBACK_COMPARISON = (
        "Could not generate the comparison notes at the moment. "
        "Usually shared holidays come from similar history or religion, "
        "while differences are from local traditions."
    )

    # simple map so we can turn country codes into full names
    COUNTRY_NAMES = {
        "NG": "Nigeria",
        "US": "United States",
        "GB": "United Kingdom",
        "GH": "Ghana",
        "CA": "Canada",
        "IN": "India",
        "ZA": "South Africa",
        "KE": "Kenya",
    }

    def __init__(self, api_key=None, model_name=None):
        # try env variables if no key is passed
        self.api_key = (
            api_key
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
        )
        # allow model to be set from env or parameter
        self.model_name = (
            model_name
            or os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        )
        self.client = None
        self.model = None
        self._setup()

    def _setup(self):
        """try to connect to Gemini. if it fails we just leave it as None"""
        if not self.api_key:
            logger.warning("No Gemini API key found")
            return

        # new package
        try:
            from google import genai
            self.client = genai.Client(api_key=self.api_key)
            return
        except Exception as e:
            logger.warning("Could not start new Gemini client: %s", type(e).__name__)

        # older package just in case
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        except Exception as e:
            logger.warning("Could not start old Gemini client: %s", type(e).__name__)
            self.client = None
            self.model = None

    def _ask_gemini(self, prompt):
        """Send prompt to Gemini with automatic retries."""

        if not self.api_key:
            return None

        # Try up to 3 times
        for attempt in range(3):
            try:
                if self.client is not None:
                    resp = self.client.models.generate_content(
                        model=self.model_name,
                        contents=prompt
                    )
                    if resp and hasattr(resp, "text") and resp.text:
                        return resp.text.strip()

                if self.model is not None:
                    resp = self.model.generate_content(prompt)
                    if resp and hasattr(resp, "text") and resp.text:
                        return resp.text.strip()

            except Exception as e:
                logger.warning(
                    "Gemini request failed (attempt %s): %s",
                    attempt + 1,
                    type(e).__name__
                )

                # wait before trying again
                if attempt == 0:
                    logger.info("Gemini is busy. Retrying in 2 seconds...")
                    time.sleep(2)
                elif attempt == 1:
                    logger.info("Still unavailable. Retrying in 4 seconds...")
                    time.sleep(4)
                else:
                    logger.error("Gemini could not respond after 3 attempts.")
                    return None

        return None

    def generate_guide(self, country_code, holiday_name, year):
        """
        Generate a cultural guide for a holiday.

        This matches the call in main.py:
        generator.generate_guide(country_code, holiday_name, year)
        """
        # basic input checks
        if not holiday_name or not str(holiday_name).strip():
            return "Holiday name is missing. Please provide a valid holiday name."

        if not country_code or not str(country_code).strip():
            return "Country code is missing. Please provide a valid country."

        country_code = str(country_code).strip().upper()
        country_name = self.COUNTRY_NAMES.get(country_code, country_code)

        prompt = f"""Explain the public holiday "{holiday_name}" celebrated in {country_name} during {year}.

Please cover these points briefly:
- What the holiday means / why it is celebrated
- A short history
- Common greetings people use (include local language if you know)
- Typical customs, food or activities

Keep it under 250 words and easy to read."""

        answer = self._ask_gemini(prompt)
        if answer:
            return answer
        return self.FALLBACK_GUIDE

    def generate_comparison_notes(self, country1, country2, shared_holidays=None, overlapping_dates=None):
        """
        write a short note about cultural similarities and differences
        between the two countries' holidays
        """
        if not country1 or not country2:
            return "Both country names are required for comparison."

        # safely convert everything to string before joining
        if shared_holidays:
            shared = ", ".join(str(item) for item in shared_holidays)
        else:
            shared = "none found"

        if overlapping_dates:
            dates = ", ".join(str(item) for item in overlapping_dates)
        else:
            dates = "none found"

        prompt = f"""Compare public holiday culture between {country1} and {country2}.

Shared holidays: {shared}
Overlapping dates: {dates}

Write a short note about:
- any common roots (history or religion)
- main cultural differences in how people celebrate
- any useful tips for someone visiting

Keep it under 200 words and neutral."""

        answer = self._ask_gemini(prompt)
        if answer:
            return answer
        return self.FALLBACK_COMPARISON

    def is_available(self):
        """
        Returns True if a Gemini client was created successfully.
        Note: this only checks that the client object exists.
        It does not guarantee that every request will succeed.
        """
        return self.client is not None or self.model is not None


if __name__ == "__main__":
    g = CultureGuideGenerator()
    print("Available:", g.is_available())
    print(
        g.generate_guide(
            "NG",
            "Christmas Day",
            2026
        )
    )
