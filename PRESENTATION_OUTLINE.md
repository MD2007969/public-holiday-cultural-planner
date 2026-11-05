# Group 9 Presentation Outline

**Project:** Public Holiday & Cultural Awareness Planner  
**Submission:** 9 November 2026  
**Presentation:** 10 November 2026

This is a preparation outline. Replace placeholders with screenshots, actual implementation details, and test evidence after the modules have been integrated.

## Suggested slide sequence

1. **Title**
   - Project name, Group 9, course/class details, and team members.
2. **Problem statement**
   - Why public-holiday information and cultural context can be difficult to find in one place.
3. **Aim and objectives**
   - Explore holidays by country/year, understand cultural context, compare countries, and save useful information.
4. **System overview**
   - Show the Streamlit interface and a simple module architecture diagram.
5. **Technology stack**
   - Python, Streamlit, Requests, JSON, Gemini API, regular expressions, and date/time handling.
6. **Public holiday feature**
   - Country/year input, API request, JSON parsing, and holiday display.
7. **Cultural awareness feature**
   - Meaning, history/context, greetings, customs, and AI fallback.
8. **Country comparison**
   - Two-country view, shared holidays, overlapping dates, and cultural differences.
9. **Saved information**
   - Favorites, guides, and comparisons stored locally.
10. **Python concepts demonstrated**
    - OOP, API requests, JSON processing, regex, exception handling, date/time, and file handling.
11. **Testing and challenges**
    - Show actual test cases, results, errors handled, and fixes made.
12. **Conclusion and future improvements**
    - Summarize what works and realistic next steps.

## Individual presentation ownership

Each member should present the part they implemented and be ready to explain their code.

- **Muhammad Abdulaziz:** application flow, main UI, integration, testing, repository workflow.
- **Usman Ibrahim:** Requests, JSON parsing, API errors, timeouts, unsupported countries.
- **Favour Onu:** Country and Holiday classes, date/time handling, comparison page UI.
- **Prosper Kwushue:** Gemini integration, cultural guide content, comparison cultural differences, fallback.
- **Haruna Ahmodu:** regex validation, custom exceptions, friendly errors, validation tests.
- **Patience Eche:** JSON file handling, save/load functions, shared-holiday and overlapping-date logic.

## Live demonstration plan

1. Launch the app using `streamlit run main.py`.
2. Select a country and year and retrieve public holidays.
3. Open a holiday and save it to favorites.
4. Generate a cultural guide and demonstrate the fallback behavior if the AI service is unavailable.
5. Compare two countries and explain shared holidays and overlapping dates.
6. Save the comparison and show the saved-items area.
7. Briefly demonstrate one invalid input and the friendly error message.

Only demonstrate features that have been integrated and tested successfully. Keep a short screen recording or screenshots as a backup in case the presentation internet connection fails.
