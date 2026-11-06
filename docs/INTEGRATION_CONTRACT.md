# Group 9 Module Integration Contract

This document defines the proposed boundaries between members' work so modules can be integrated without duplicating responsibilities. Confirm any proposed interface change with the affected member before implementation.

## Agreed names

The following names must remain exact:

- `Country`
- `Holiday`
- `HolidayAPIClient`
- `CultureGuideGenerator`

## Module ownership and expected interfaces

| Owner | File | Responsibility | Expected interface |
|---|---|---|---|
| Usman Ibrahim | `holiday_api.py` | Requests, JSON parsing, timeouts, failed requests, unsupported countries | `HolidayAPIClient.get_public_holidays(country_code, year)` |
| Favour Onu | `models.py`, `comparison_ui.py` | Country/Holiday models, date/time handling, two-country comparison page UI | `Country`, `Holiday`, `render_comparison_page(countries, load_holidays, validate_inputs)` |
| Prosper Kwushue | `culture_guide.py` | Gemini cultural guides and cultural differences, with fallback | `CultureGuideGenerator.generate_guide(country_code, holiday_name, year)` |
| Haruna Ahmodu | `validators.py`, `exceptions.py` | Regex validation, custom exceptions, friendly validation errors | `validate_country_code(code)`, `validate_year(year)` |
| Patience Eche | `storage.py`, `comparison.py` | JSON persistence and comparison calculations | Storage functions and `compare_holidays(first, second)` |
| Muhammad Abdulaziz | `main.py`, README, tests coordination, slides | Main app shell, navigation, holiday/guide UI, integration, end-to-end tests and submission | `main()` and application orchestration |

## Data contracts

### Country and Holiday models

The model implementation should expose enough information for the UI and comparison logic. Proposed minimum fields:

- `Country`: country name and ISO-style country code.
- `Holiday`: holiday name, date, country code, optional description, and holiday type.

The model owner should confirm the constructor signatures and attribute names with the team before finalizing them. The main UI currently accepts either dictionaries or objects with matching attributes.

### Holiday API client

Proposed usage:

```python
client = HolidayAPIClient()
holidays = client.get_public_holidays("NG", 2026)
```

Expected result: a list of `Holiday` objects, or dictionaries with equivalent fields (`name`, `date`, `country_code`, optional `description`, and `holiday_type`/ `type`).

The API client should provide clear, catchable errors for network failures, timeouts, invalid responses, and unsupported country codes. Do not return an HTML error page as if it were holiday data.

### Validators

Proposed usage:

```python
validate_country_code("NG")
validate_year(2026)
```

Validations should return normally for valid input and raise a documented exception for invalid input. The UI will display a friendly message and may show technical details in an expandable developer section.

### Cultural guide generator

Proposed usage:

```python
generator = CultureGuideGenerator()
guide = generator.generate_guide("NG", "Eid al-Fitr", 2026)
```

The guide should cover cultural meaning, history/context, greetings, and customs where relevant. If Gemini is unavailable or fails, return a clear fallback message rather than crashing the app. The exact return type (string or dictionary) must be agreed with the UI owner.

For the comparison page, Prosper should expose a small method or documented function for generating cultural differences from the two countries' comparison data. Agree its signature with Favour before implementation.

### Comparison logic

Proposed usage:

```python
result = compare_holidays(first_country_holidays, second_country_holidays)
```

The result should make it possible for the comparison UI to show:
- Holidays shared by both countries (using a documented matching rule).
- Holidays that fall on the same date.
- Holidays found only in the first country.
- Holidays found only in the second country.

The return structure must be documented with a small example. Matching by holiday name should normalize case and surrounding whitespace; matching dates should use a consistent date format.

### Storage

Expected functions:

```python
save_favorite(item)
load_favorites()
save_guide(item)
load_guides()
save_comparison(item)
load_comparisons()
```

Storage should use JSON, create the data directory/files when needed, and handle missing or malformed files safely. Saved records must be serializable; convert model objects and dates to plain JSON-compatible values before writing.

## Main application integration

The main application owns the overall navigation and page shell. Favour's `comparison_ui.py` must expose `render_comparison_page(countries, load_holidays, validate_inputs)`. The main app passes its country mapping and shared loader/validator functions to that page. Favour's page calls Patience's `comparison.compare_holidays(...)` for calculations. Prosper owns AI-generated cultural explanations. Until `comparison_ui.py` is available, the main app displays a clear placeholder instead of duplicating the comparison UI.

The UI should not reimplement another member's API, validation, AI, storage, or comparison logic.

## Configuration and secrets

- Keep Gemini credentials in local Streamlit secrets or environment variables.
- Never hard-code or commit API keys.
- Document required configuration in the README.
- The app should explain how to proceed when an optional external service is unavailable.
