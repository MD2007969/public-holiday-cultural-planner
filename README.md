# Public Holiday & Cultural Awareness Planner

A Python application that helps users explore public holidays, understand their cultural significance, compare holidays across countries, and save useful information.

## Project goals

- Select a country and year to retrieve public holidays.
- Display holiday names, dates, and types.
- Generate cultural guides covering meaning, history, greetings, and customs using Gemini.
- Compare public holidays between two countries.
- Save favourite holidays, cultural guides, and comparisons locally.

## Technology

- Python
- Streamlit
- Requests and JSON
- Python date/time handling
- Google Gemini API
- Regular expressions
- JSON file storage

## Run the application

1. Install Python 3.10 or later.
2. Clone the repository.
3. Open the project folder in a terminal.
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Add your Gemini API key using Streamlit secrets. Create `.streamlit/secrets.toml` locally:

   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```

   Do not commit this file or share your API key.

6. Start the app:

   ```bash
   streamlit run main.py
   ```

## Module integration contracts

To keep everyone's modules compatible, use these agreed interfaces:

| File | Required interface |
|---|---|
| `models.py` | `Country` and `Holiday` classes |
| `holiday_api.py` | `HolidayAPIClient.get_public_holidays(country_code, year)` |
| `culture_guide.py` | `CultureGuideGenerator.generate_guide(country_code, holiday_name, year)` |
| `validators.py` | `validate_country_code(code)` and `validate_year(year)` |
| `exceptions.py` | Shared custom exceptions used by validation/API modules |
| `storage.py` | `save_favorite(item)`, `load_favorites()`, `save_guide(item)`, `load_guides()`, `save_comparison(item)`, `load_comparisons()` |
| `comparison.py` | `compare_holidays(first_country_holidays, second_country_holidays)` |

The API client should return a list of `Holiday` objects (or dictionaries with equivalent fields). The comparison function should return a clear result describing shared holidays and overlapping dates.

If a method name or return format needs to change, discuss it with the team before changing the integration code.

## GitHub contribution workflow

1. Work only on your assigned personal branch.
2. Commit and push your work to that branch.
3. Open a Pull Request targeting `main`.
4. Explain what you implemented and how you tested it.
5. Wait for review and approval before merging.

Do not push directly to `main`.

## Required learning concepts

The project demonstrates object-oriented programming, file handling, exception handling, regular expressions, API requests, JSON processing, and date/time handling.

## Team

Group 9 — Public Holiday & Cultural Awareness Planner.

See the project discussion and assigned roles for the current contributor list.
