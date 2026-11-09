# Public Holiday & Cultural Awareness Planner

A Python application that helps users explore public holidays, understand their cultural significance, compare holidays across countries, and save useful information.

## Project objectives

- Select a country and year to retrieve public holidays.
- Display holiday names, dates, and holiday types.
- Generate cultural guides covering meaning, context, greetings, and customs using Gemini.
- Compare public holidays between two countries, including shared holidays and overlapping dates.
- Explain cultural differences between the selected countries.
- Save favorite holidays, cultural guides, and comparisons locally.

## Live application

[Open the Public Holiday & Cultural Awareness Planner](https://public-holiday-cultural-planner-bvklndu7ltbp5e7eesemmu.streamlit.app/)

## Source code

[GitHub repository](https://github.com/MD2007969/public-holiday-cultural-planner)

## Technology

- Python
- Streamlit
- Requests and JSON
- Python date/time handling
- Google Gemini API
- JSON file storage

## Run the application locally

1. Install Python 3.10 or later.
2. Clone the repository and open the project folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. If you want to use the AI cultural-guide feature, configure your Gemini API key in Streamlit secrets. Create `.streamlit/secrets.toml`:

   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```

   Do not commit this file or share your API key.

6. Start the application:

   ```bash
   streamlit run main.py
   ```

## Run the tests

Run the test suite with:

```bash
python -m pytest -q
```

## Project team and contributions

Group 9's documented contributors and responsibilities are:

| Contributor | Role | Contribution |
|---|---|---|
| Muhammad Abdulaziz | Group Leader and Integration Lead | Main application flow and UI, integration of project modules, storage and comparison integration, end-to-end testing, repository coordination, documentation and presentation preparation |
| Usman Ibrahim | Holiday API Client | API requests, holiday data retrieval, JSON response handling, and API error handling |
| Favour Onu | Data Models and Comparison UI | Country and Holiday models, date handling, and the two-country comparison interface |
| Prosper Kwushue | AI Cultural Guide | Gemini integration and AI-generated cultural guidance |

This contributor list reflects the four members whose work is included in the final project. Patience Eche and Haruna Ahmodu are not listed as contributors because their assigned work was not completed or included in the final integrated contribution record.

## Main project modules

| File | Responsibility |
|---|---|
| `main.py` | Main Streamlit application and navigation |
| `holiday_api.py` | Public holiday API client |
| `models.py` | Country and Holiday data models |
| `culture_guide.py` | AI cultural guide generation |
| `comparison.py` | Comparison calculations for holiday data |
| `comparison_ui.py` | Country comparison interface |
| `storage.py` | Saving and loading favorites, guides, and comparisons |

## GitHub contribution workflow

1. Work on an assigned branch.
2. Commit and push changes to that branch.
3. Open a pull request targeting `main`.
4. Describe the changes and tests performed.
5. Review and merge approved changes.

Do not commit API keys, local secrets, virtual environments, or personal saved-data files.

## Python concepts demonstrated

The project uses Python functions and modules, object-oriented data models, API requests, JSON processing, exception handling, date/time handling, and file handling.

## Presentation

See [PRESENTATION_OUTLINE.md](PRESENTATION_OUTLINE.md) for the presentation structure and live demonstration plan.

---

**Group 9 — Public Holiday & Cultural Awareness Planner**
