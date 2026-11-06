"""Main Streamlit application for the Public Holiday & Cultural Awareness Planner.

Integration contract:
- HolidayAPIClient.get_public_holidays(country_code, year) or fetch_holidays(country_code, year) -> list of Holiday objects or dictionaries
- CultureGuideGenerator.generate_guide(country_code, holiday_name, year) -> guide text or dictionary
- validators.validate_country_code(code) and validators.validate_year(year)
- storage.save_favorite(item), storage.load_favorites(), storage.save_guide(item),
  storage.load_guides(), storage.save_comparison(item), storage.load_comparisons()
- comparison.compare_holidays(first_country_holidays, second_country_holidays)
"""

import streamlit as st

st.set_page_config(
    page_title="Holiday & Culture Planner",
    page_icon="🌍",
    layout="wide",
)

COUNTRIES = {
    "Nigeria": "NG",
    "United States": "US",
    "United Kingdom": "GB",
    "Ghana": "GH",
    "Canada": "CA",
    "India": "IN",
    "South Africa": "ZA",
    "Kenya": "KE",
}


def get_value(item, key, default=""):
    """Read a value from either a dictionary or an object."""
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def holiday_to_dict(holiday, country_code):
    """Normalize API dictionaries and Holiday objects for the UI."""
    name = (
        get_value(holiday, "name", "")
        or get_value(holiday, "local_name", "")
        or "Unnamed holiday"
    )

    # Usman's API uses "types", which may be a list such as ["Public"].
    types = get_value(holiday, "types", [])
    if isinstance(types, (list, tuple)):
        types_text = ", ".join(str(item) for item in types)
    else:
        types_text = str(types or "")

    holiday_type = (
        get_value(holiday, "holiday_type", "")
        or get_value(holiday, "type", "")
        or types_text
        or "Public holiday"
    )

    return {
        "name": str(name),
        "date": str(get_value(holiday, "date", "") or ""),
        "country_code": str(
            get_value(holiday, "country_code", "")
            or get_value(holiday, "country", "")
            or country_code
        ),
        "description": str(get_value(holiday, "description", "") or ""),
        "holiday_type": str(holiday_type),
    }


def show_module_notice(module_name):
    st.info(
        module_name + " is not available yet. The responsible team member should "
        "push the module to their branch and submit a pull request."
    )


def load_holidays(country_code, year):
    """Load holidays using the API team's available client method."""
    from holiday_api import HolidayAPIClient

    client = HolidayAPIClient()

    # Support the agreed interface and Usman's current branch implementation.
    if hasattr(client, "get_public_holidays"):
        return client.get_public_holidays(country_code, year)

    if hasattr(client, "fetch_holidays"):
        return client.fetch_holidays(country_code, year)

    raise AttributeError(
        "HolidayAPIClient must provide get_public_holidays() or fetch_holidays()."
    )


def validate_inputs(country_code, year):
    """Run the shared validation functions when they are available."""
    from validators import validate_country_code, validate_year

    validate_country_code(country_code)
    validate_year(year)


def create_culture_guide(country_code, holiday_name, year):
    """Generate a cultural guide through the Gemini module."""
    from culture_guide import CultureGuideGenerator

    generator = CultureGuideGenerator()
    return generator.generate_guide(country_code, holiday_name, year)


def render_holiday_list(holidays, country_code):
    """Display returned holidays and allow the user to save a favorite."""
    if not holidays:
        st.warning("No holidays were returned for this country and year.")
        return

    st.success("Found " + str(len(holidays)) + " holiday(s).")

    normalized_holidays = [
        holiday_to_dict(holiday, country_code) for holiday in holidays
    ]
    normalized_holidays.sort(key=lambda item: (item["date"], item["name"].casefold()))

    for number, item in enumerate(normalized_holidays):
        title = item["name"] + " — " + item["date"]
        with st.expander(title):
            st.write("**Country:** " + item["country_code"])
            st.write("**Type:** " + item["holiday_type"])
            if item["description"]:
                st.write(item["description"])

            if st.button("Save to favourites", key="save_holiday_" + str(number)):
                try:
                    from storage import save_favorite

                    save_favorite(item)
                    st.success("Holiday saved to favourites.")
                except ImportError:
                    show_module_notice("storage.py")
                except Exception as error:
                    st.error("Could not save this holiday: " + str(error))


def render_holidays_tab():
    st.subheader("Explore public holidays")
    left, right = st.columns([2, 1])

    with left:
        country_name = st.selectbox("Choose a country", list(COUNTRIES.keys()))
    with right:
        year = st.number_input(
            "Choose a year",
            min_value=2000,
            max_value=2100,
            value=2026,
            step=1,
        )

    country_code = COUNTRIES[country_name]

    if st.button("Find public holidays", type="primary"):
        # Clear dependent results so a failed search cannot leave stale data on screen.
        for state_key in (
            "holidays",
            "active_country_code",
            "active_country_name",
            "active_year",
            "current_guide",
            "comparison_result",
        ):
            st.session_state.pop(state_key, None)

        try:
            validate_inputs(country_code, int(year))
            holidays = load_holidays(country_code, int(year))
            st.session_state["holidays"] = holidays
            st.session_state["active_country_code"] = country_code
            st.session_state["active_country_name"] = country_name
            st.session_state["active_year"] = int(year)
        except ImportError as error:
            st.error("A required project module has not been added yet: " + str(error))
        except Exception as error:
            st.error("We could not retrieve the holidays. Please check your input or try again.")
            with st.expander("Technical details for the team"):
                st.code(str(error))

    if "holidays" in st.session_state:
        st.write(
            "Showing results for "
            + st.session_state.get("active_country_name", country_name)
            + " — "
            + str(st.session_state.get("active_year", int(year)))
        )
        render_holiday_list(
            st.session_state["holidays"],
            st.session_state.get("active_country_code", country_code),
        )


def render_culture_tab():
    st.subheader("AI cultural guide")
    holidays = st.session_state.get("holidays", [])

    if not holidays:
        st.info("Find a country's public holidays first, then choose a holiday for its cultural guide.")
        return

    country_code = st.session_state.get("active_country_code", "NG")
    country_name = st.session_state.get("active_country_name", country_code)
    holiday_names = [
        holiday_to_dict(item, country_code)["name"] for item in holidays
    ]
    selected_holiday = st.selectbox("Choose a holiday", holiday_names)

    if st.button("Generate cultural guide", type="primary"):
        try:
            guide = create_culture_guide(
                country_code,
                selected_holiday,
                st.session_state.get("active_year", 2026),
            )
            if isinstance(guide, dict):
                guide_text = guide.get("guide", guide.get("content", str(guide)))
            else:
                guide_text = str(guide)

            st.session_state["current_guide"] = {
                "country": country_name,
                "country_code": country_code,
                "holiday": selected_holiday,
                "year": st.session_state.get("active_year", 2026),
                "guide": guide_text,
            }
        except ImportError as error:
            st.error("The AI guide module is not available yet: " + str(error))
        except Exception as error:
            st.warning("The AI guide could not be generated. Please try again.")
            with st.expander("Technical details for the team"):
                st.code(str(error))

    guide_item = st.session_state.get("current_guide")
    if guide_item:
        st.markdown("### " + guide_item["holiday"] + " in " + guide_item["country"])
        st.write(guide_item["guide"])
        if st.button("Save this guide"):
            try:
                from storage import save_guide

                save_guide(guide_item)
                st.success("Cultural guide saved.")
            except ImportError:
                show_module_notice("storage.py")
            except Exception as error:
                st.error("Could not save the guide: " + str(error))


def render_comparison_tab():
    """Delegate the comparison page to the member who owns that UI."""
    try:
        from comparison_ui import render_comparison_page
    except ImportError:
        st.info(
            "The comparison page is being prepared by Favour. "
            "It will appear here when comparison_ui.py is added to the project."
        )
        return

    # Keep the main app responsible for navigation and shared services.
    # The comparison page owns its presentation; Patience's comparison.py
    # owns the actual comparison calculations.
    render_comparison_page(
        countries=COUNTRIES,
        load_holidays=load_holidays,
        validate_inputs=validate_inputs,
    )

def render_saved_tab():
    st.subheader("Your saved items")
    favorites_col, guides_col, comparisons_col = st.columns(3)

    with favorites_col:
        st.markdown("#### ⭐ Favourite holidays")
        try:
            from storage import load_favorites

            favorites = load_favorites()
            if favorites:
                for item in favorites:
                    st.write(
                        str(item.get("name", "Holiday"))
                        + " — "
                        + str(item.get("date", ""))
                    )
            else:
                st.caption("No favourites saved yet.")
        except ImportError:
            st.caption("Storage module is not available yet.")
        except Exception as error:
            st.error("Could not load favourites: " + str(error))

    with guides_col:
        st.markdown("#### 📚 Cultural guides")
        try:
            from storage import load_guides

            guides = load_guides()
            if guides:
                for item in guides:
                    st.write(item.get("holiday", "Saved guide"))
            else:
                st.caption("No guides saved yet.")
        except ImportError:
            st.caption("Storage module is not available yet.")
        except Exception as error:
            st.error("Could not load guides: " + str(error))

    with comparisons_col:
        st.markdown("#### 🌍 Comparisons")
        try:
            from storage import load_comparisons

            comparisons = load_comparisons()
            if comparisons:
                for item in comparisons:
                    st.write(
                        item.get("first_country", "Country 1")
                        + " vs "
                        + item.get("second_country", "Country 2")
                    )
            else:
                st.caption("No comparisons saved yet.")
        except ImportError:
            st.caption("Storage module is not available yet.")
        except Exception as error:
            st.error("Could not load comparisons: " + str(error))


def main():
    st.title("🌍 Public Holiday & Cultural Awareness Planner")
    st.caption(
        "Explore public holidays, discover the cultures behind them, "
        "and compare celebrations across countries."
    )

    holidays_tab, culture_tab, compare_tab, saved_tab = st.tabs(
        ["Public Holidays", "Cultural Guide", "Compare Countries", "Saved Items"]
    )

    with holidays_tab:
        render_holidays_tab()

    with culture_tab:
        render_culture_tab()

    with compare_tab:
        render_comparison_tab()

    with saved_tab:
        render_saved_tab()

    st.divider()
    st.caption("Group 9 • Public Holiday & Cultural Awareness Planner")


if __name__ == "__main__":
    main()
