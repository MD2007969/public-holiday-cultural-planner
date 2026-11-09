# Group 9 Module Integration Contract

This document records the main module interfaces and the responsibilities used to integrate the final Group 9 project.

## Core names

The following project components are used by the application:

- `Country`
- `Holiday`
- `HolidayAPIClient`
- `CultureGuideGenerator`

## Contributor responsibilities

| Contributor | Main files / area | Responsibility |
|---|---|---|
| Muhammad Abdulaziz | `main.py`, `storage.py`, `comparison.py`, integration and tests | Main application flow, integration of modules, JSON persistence, comparison calculations, end-to-end testing |
| Usman Ibrahim | `holiday_api.py` | Public holiday API requests, JSON response handling, and API failure handling |
| Favour Onu | `models.py`, `comparison_ui.py` | Country and Holiday models, date handling, and comparison page interface |
| Prosper Kwushue | `culture_guide.py` | Gemini-powered cultural guides and fallback behavior |

This table identifies the four contributors whose work is represented in the final integrated project.

## Module interfaces and responsibilities

### Data models

The model layer provides Country and Holiday representations for the application. The UI and comparison logic should use consistent country codes, holiday names, and date values.

### Holiday API client

The API client retrieves public holidays for a country and year and handles request/response processing. Expected usage:

```python
client = HolidayAPIClient()
holidays = client.get_public_holidays("NG", 2026)
```

The API layer should handle network failures, timeouts, invalid responses, and unsupported country codes without treating an error page as valid holiday data.

### Cultural guide generator

The cultural guide generator uses Gemini to provide cultural context, greetings, and customs for a selected holiday. If the AI service is unavailable, the application should fail gracefully and provide an appropriate fallback message.

### Country comparison

The comparison feature accepts holiday data for two countries and calculates shared holidays, overlapping dates, and holidays unique to either country. The comparison interface presents these results to the user.

### Storage

The storage module saves and loads favorites, cultural guides, and country comparisons using JSON files. It should handle missing or malformed files safely and serialize saved records into JSON-compatible values.

## Main application integration

The main application coordinates the Streamlit interface and connects the holiday API, data models, cultural guide, comparison interface, and storage functions. Keep module interfaces consistent when making changes, and test affected features after integration.

## Configuration and secrets

- Keep Gemini credentials in Streamlit secrets or environment variables.
- Never hard-code or commit API keys.
- Do not upload local secrets or personal saved-data files to the public repository.
- The application should handle optional external-service failures gracefully.
