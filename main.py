"""
GROUP 9 PROJECT
Public Holiday & Cultural Awareness Planner

Leader: Muhammad Abdulaziz
"""

import re
import streamlit as st


# --------------------------------------------------
# 1. APPLICATION CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Holiday & Culture Planner",
    page_icon="🌍",
    layout="wide"
)


COUNTRIES = {
    "Nigeria": "NG",
    "United States": "US",
    "United Kingdom": "GB",
    "Ghana": "GH",
    "Canada": "CA",
    "India": "IN",
    "South Africa": "ZA",
    "Kenya": "KE"
}


# --------------------------------------------------
# 2. HELPER FUNCTIONS
# --------------------------------------------------

def get_value(item, key, default=""):
    """Read a value from a dictionary or object."""

    if isinstance(item, dict):
        return item.get(key, default)

    return getattr(item, key, default)


def holiday_to_dict(holiday, country_code):
    """Convert holiday data into a standard dictionary."""

    name = (
        get_value(holiday, "name", "")
        or get_value(holiday, "local_name", "")
        or "Unnamed holiday"
    )

    holiday_type = (
        get_value(holiday, "holiday_type", "")
        or get_value(holiday, "type", "")
        or get_value(holiday, "types", "")
        or "Public holiday"
    )

    if isinstance(holiday_type, (list, tuple)):
        holiday_type = ", ".join(
            str(value) for value in holiday_type
        )

    date = get_value(holiday, "date", "")

    if hasattr(date, "isoformat"):
        date = date.isoformat()

    return {
        "name": str(name),
        "date": str(date),
        "country_code": str(
            get_value(holiday, "country_code", "")
            or get_value(holiday, "country", "")
            or country_code
        ),
        "holiday_type": str(holiday_type),
        "description": str(
            get_value(holiday, "description", "")
        )
    }


# --------------------------------------------------
# 3. INPUT VALIDATION
# --------------------------------------------------

def validate_inputs(country_code, year):
    """Validate country code and year."""

    try:
        from validators import (
            validate_country_code,
            validate_year
        )

    except ImportError:

        if not re.fullmatch(r"[A-Z]{2}", str(country_code)):
            raise ValueError("Invalid country code.")

        if not 2000 <= int(year) <= 2100:
            raise ValueError(
                "Year must be between 2000 and 2100."
            )

    else:
        validate_country_code(country_code)
        validate_year(year)


# --------------------------------------------------
# 4. HOLIDAY API INTEGRATION
# --------------------------------------------------

def load_holidays(country_code, year):
    """Retrieve public holidays using Usman's API module."""

    from holiday_api import HolidayAPIClient

    client = HolidayAPIClient()

    if hasattr(client, "get_public_holidays"):

        holidays = client.get_public_holidays(
            country_code,
            year
        )

    elif hasattr(client, "fetch_holidays"):

        holidays = client.fetch_holidays(
            country_code,
            year
        )

    else:
        raise AttributeError(
            "HolidayAPIClient must provide "
            "get_public_holidays() or fetch_holidays()."
        )

    return holidays or []


# --------------------------------------------------
# 5. AI CULTURAL GUIDE INTEGRATION
# --------------------------------------------------

def create_culture_guide(
    country_code,
    holiday_name,
    year
):
    """Generate a cultural guide using Prosper's module."""

    from culture_guide import CultureGuideGenerator

    generator = CultureGuideGenerator()

    return generator.generate_guide(
        country_code,
        holiday_name,
        year
    )


# --------------------------------------------------
# 6. PUBLIC HOLIDAYS PAGE
# --------------------------------------------------

def render_holidays_tab():

    st.header("📅 Explore Public Holidays")

    col1, col2 = st.columns(2)

    with col1:

        country = st.selectbox(
            "Select a country",
            list(COUNTRIES.keys())
        )

    with col2:

        year = st.number_input(
            "Select year",
            min_value=2000,
            max_value=2100,
            value=2026,
            step=1
        )

    country_code = COUNTRIES[country]

    if st.button(
        "Find Public Holidays",
        type="primary"
    ):

        st.session_state.pop("holidays", None)

        try:

            validate_inputs(
                country_code,
                int(year)
            )

            with st.spinner("Retrieving holidays..."):

                holidays = load_holidays(
                    country_code,
                    int(year)
                )

            st.session_state["holidays"] = holidays
            st.session_state["active_country"] = country
            st.session_state["active_code"] = country_code
            st.session_state["active_year"] = int(year)

        except ImportError as error:

            st.error(
                f"A required module is missing: {error}"
            )

        except Exception as error:

            st.error("Unable to retrieve holidays.")
            st.exception(error)

    if "holidays" not in st.session_state:
        return

    holidays = st.session_state["holidays"]

    if not holidays:

        st.warning(
            "No holidays were found for this selection."
        )

        return

    st.success(
        f"{len(holidays)} holidays found!"
    )

    normalized = [
        holiday_to_dict(item, country_code)
        for item in holidays
    ]

    normalized.sort(
        key=lambda item: (
            item["date"],
            item["name"].casefold()
        )
    )

    for index, holiday in enumerate(normalized):

        with st.expander(
            f'{holiday["date"]} - {holiday["name"]}'
        ):

            st.write(
                "Country:",
                holiday["country_code"]
            )

            st.write(
                "Type:",
                holiday["holiday_type"]
            )

            if holiday["description"]:
                st.write(holiday["description"])

            if st.button(
                "⭐ Save Favourite",
                key=f"favorite_{index}"
            ):

                try:

                    from storage import save_favorite

                    save_favorite(holiday)

                    st.success("Holiday saved!")

                except ImportError:

                    st.warning(
                        "Storage module is not available yet."
                    )

                except Exception as error:

                    st.error(str(error))


# --------------------------------------------------
# 7. CULTURAL GUIDE PAGE
# --------------------------------------------------

def render_culture_tab():

    st.header("✨ AI Cultural Guide")

    holidays = st.session_state.get(
        "holidays",
        []
    )

    if not holidays:

        st.info(
            "Find public holidays first before generating a guide."
        )

        return

    country_code = st.session_state["active_code"]
    country = st.session_state["active_country"]
    year = st.session_state["active_year"]

    holiday_names = [
        holiday_to_dict(item, country_code)["name"]
        for item in holidays
    ]

    selected = st.selectbox(
        "Choose a holiday",
        holiday_names
    )

    if st.button(
        "Generate Cultural Guide",
        type="primary"
    ):

        try:

            with st.spinner(
                "Generating cultural guide..."
            ):

                guide = create_culture_guide(
                    country_code,
                    selected,
                    year
                )

            if isinstance(guide, dict):

                guide = guide.get(
                    "guide",
                    guide.get("content", str(guide))
                )

            st.session_state["current_guide"] = {
                "country": country,
                "country_code": country_code,
                "holiday": selected,
                "year": year,
                "guide": str(guide)
            }

        except ImportError:

            st.warning(
                "AI cultural guide module is not available yet."
            )

        except Exception as error:

            st.error(
                "Could not generate the cultural guide."
            )

            st.exception(error)

    guide_data = st.session_state.get(
        "current_guide"
    )

    if guide_data:

        st.subheader(
            f'{guide_data["holiday"]} '
            f'in {guide_data["country"]}'
        )

        st.write(guide_data["guide"])

        if st.button("Save Cultural Guide"):

            try:

                from storage import save_guide

                save_guide(guide_data)

                st.success("Guide saved!")

            except ImportError:

                st.warning(
                    "Storage module is not available yet."
                )

            except Exception as error:

                st.error(str(error))


# --------------------------------------------------
# 8. COUNTRY COMPARISON PAGE
# --------------------------------------------------

def render_comparison_tab():

    st.header("⚖️ Compare Countries")

    try:

        from comparison_ui import render_comparison_page

        render_comparison_page(
            countries=COUNTRIES,
            load_holidays=load_holidays,
            validate_inputs=validate_inputs
        )

    except ImportError:

        st.info(
            "The comparison page is waiting for "
            "Favour's comparison_ui.py module."
        )

    except Exception as error:

        st.error(
            "The comparison page encountered an error."
        )

        st.exception(error)


# --------------------------------------------------
# 9. SAVED ITEMS PAGE
# --------------------------------------------------

def render_saved_tab():

    st.header("💾 Saved Items")

    columns = st.columns(3)

    sections = [
        ("⭐ Favourite Holidays", "load_favorites"),
        ("📚 Cultural Guides", "load_guides"),
        ("🌍 Comparisons", "load_comparisons")
    ]

    for column, (heading, function_name) in zip(
        columns,
        sections
    ):

        with column:

            st.subheader(heading)

            try:

                import storage

                loader = getattr(
                    storage,
                    function_name,
                    None
                )

                if loader is None:

                    st.caption(
                        f"{function_name}() is not implemented yet."
                    )

                    continue

                records = loader()

                if not records:

                    st.caption("Nothing saved yet.")

                else:

                    for record in records:
                        st.write(record)

            except ImportError:

                st.caption(
                    "Storage module is not available yet."
                )

            except Exception as error:

                st.error(str(error))


# --------------------------------------------------
# 10. MAIN APPLICATION
# --------------------------------------------------

def main():

    st.title(
        "🌍 Public Holiday & Cultural Awareness Planner"
    )

    st.write(
        "Explore public holidays, discover cultural "
        "traditions, and compare celebrations across countries."
    )

    tabs = st.tabs([
        "📅 Public Holidays",
        "✨ Cultural Guide",
        "⚖️ Compare Countries",
        "💾 Saved Items"
    ])

    with tabs[0]:
        render_holidays_tab()

    with tabs[1]:
        render_culture_tab()

    with tabs[2]:
        render_comparison_tab()

    with tabs[3]:
        render_saved_tab()

    st.divider()

    st.caption(
        "Group 9 | Public Holiday & Cultural Awareness Planner"
    )


# --------------------------------------------------
# 11. APPLICATION ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    main()
