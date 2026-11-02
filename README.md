# Public Holiday & Cultural Awareness Planner

A Python application that lets users explore public holidays by country and year, learn about cultural significance, compare holidays between countries, and save holiday guides locally.

## Project requirements

The completed application must demonstrate:
- **Object-Oriented Programming (OOP):** classes for countries, holidays, API access, and guide generation.
- **File handling:** save and load favourites, holiday guides, and comparison results.
- **Exception handling:** handle invalid input, unsupported countries/years, missing files, malformed JSON, and API failures.
- **Regular expressions:** validate two-letter country codes and four-digit years.

## Proposed technology

- Python 3
- Streamlit for the interface
- Requests for HTTP requests
- JSON for data storage
- datetime for date handling
- re for regular-expression validation
- Nager.Date public holidays API as the initial public-holiday data source
- Gemini API may be added for cultural explanations if API access is available; cultural content must be checked for accuracy.

## Run locally

1. Install Python 3.
2. Clone this repository.
3. Create and activate a virtual environment.
4. Install dependencies: `pip install -r requirements.txt`
5. Start the application: `streamlit run app.py`

## Team workflow

- Each member works on their assigned module and tests it before submitting.
- Do not commit directly to `main` for feature work. Create a branch such as `feature/holiday-api`.
- Open a Pull Request to merge completed work into `main`.
- Keep function names, file names, and data structures consistent with this README and the team agreement.
- Never commit API keys, passwords, or private information.

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules and the proposed team allocation.

## Suggested project structure

```
public-holiday-cultural-planner/
├── app.py
├── models.py
├── holiday_api.py
├── holiday_calendar.py
├── cultural_info.py
├── holiday_comparison.py
├── file_manager.py
├── validation.py
├── data/
│   └── cultural_holidays.json
├── tests/
│   └── test_cases.py
├── requirements.txt
├── README.md
├── CONTRIBUTING.md
└── .gitignore
```

## Shared holiday data shape

Modules should exchange holiday records using this structure:

```python
{
    "name": "New Year's Day",
    "date": "2026-01-01",
    "local_name": "New Year's Day",
    "country_code": "NG",
    "types": ["Public"]
}
```

Use ISO date format (`YYYY-MM-DD`). The API may omit optional fields, so code must handle missing values safely.

## Status

Initial repository setup. Feature implementation and tests are to be completed by the team.
