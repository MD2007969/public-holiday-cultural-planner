# Public Holiday & Cultural Awareness Planner

A Python application that helps users explore public holidays, understand their cultural significance, compare holidays across countries, and save useful information.

## Project objectives

- Select a country and year to retrieve public holidays.
- Display holiday names, dates, and holiday types.
- Generate cultural guides covering meaning, history/context, greetings, and customs using Gemini.
- Compare public holidays between two countries, including shared holidays and overlapping dates.
- Explain cultural differences between the selected countries.
- Save favorite holidays, cultural guides, and comparisons locally.

## Technology

- Python 3.10+
- Streamlit
- Requests and JSON
- Python date/time handling
- Google Gemini API
- Regular expressions
- JSON file storage

## Run the application

1. Install Python 3.10 or later.
2. Clone the repository and open the project folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Configure your Gemini API key locally. Create `.streamlit/secrets.toml`:

   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```

   Do not commit this file or share your API key. It is excluded by `.gitignore`.

6. Start the application:

   ```bash
   streamlit run main.py
   ```

## Run the tests

Run the initial main-application helper tests with:

```bash
python -m unittest discover -s tests -v
```

Add tests for each module as the team members submit their implementations.

## Team roles and module ownership

| Member | Role | Main deliverables |
|---|---|---|
| Muhammad Abdulaziz | Role 1 — Leader | GitHub coordination, `main.py` app shell and main UI, integration, end-to-end testing, README and presentation slides |
| Usman Ibrahim | Role 2 — API Client | `HolidayAPIClient`, Requests/JSON parsing, failed requests, timeouts, unsupported countries |
| Favour Onu | Role 3 — Models | `Country` and `Holiday` classes, date/time handling, two-country comparison page UI |
| Prosper Kwushue | Role 4 — AI Guide | `CultureGuideGenerator`, Gemini cultural guides, cultural differences, fallback behavior |
| Haruna Ahmodu | Role 5 — Validation | `validators.py`, regex validation, custom exceptions, friendly errors and validation testing |
| Patience Eche | Role 7 — File Handling | `storage.py`, JSON save/load, comparison logic for shared holidays and overlapping dates |

Each member is expected to commit their own work and present their contribution. See [CONTRIBUTING.md](CONTRIBUTING.md) for the GitHub workflow.

## Module integration contracts

The agreed integration interfaces are documented in [docs/INTEGRATION_CONTRACT.md](docs/INTEGRATION_CONTRACT.md). Key names must remain exact:

- `Country`
- `Holiday`
- `HolidayAPIClient`
- `CultureGuideGenerator`

Expected module responsibilities:

| File | Expected interface / responsibility |
|---|---|
| `models.py` | `Country` and `Holiday` classes |
| `holiday_api.py` | `HolidayAPIClient.get_public_holidays(country_code, year)` |
| `culture_guide.py` | `CultureGuideGenerator.generate_guide(country_code, holiday_name, year)` |
| `validators.py` | `validate_country_code(code)` and `validate_year(year)` |
| `exceptions.py` | Shared custom exceptions for validation and application errors |
| `storage.py` | Save/load favorites, guides, and comparisons |
| `comparison.py` | `compare_holidays(first_country_holidays, second_country_holidays)` |
| `comparison_ui.py` | Comparison page UI owned by Favour, coordinated with Patience and Prosper |

If a function signature or return format needs to change, discuss it with the affected members and update the integration contract before merging.

## GitHub contribution workflow

1. Work only on your assigned personal branch.
2. Commit and push your own changes to that branch.
3. Open a pull request targeting `main`.
4. Explain what you implemented and how you tested it.
5. Wait for the group leader's review and approval before merging.

Do not push directly to `main`. Do not commit API keys, local secrets, virtual environments, or personal saved-data files.

## Python concepts demonstrated

The project demonstrates object-oriented programming, API requests, JSON processing, regular expressions, exception handling, date/time handling, and file handling.

## Presentation

See [PRESENTATION_OUTLINE.md](PRESENTATION_OUTLINE.md) for the slide sequence, individual speaking responsibilities, and live demonstration plan.

## Project team

Group 9 — Public Holiday & Cultural Awareness Planner.
