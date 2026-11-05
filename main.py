"""Main Streamlit application for the Public Holiday & Cultural Awareness Planner.

Integration contract:
- HolidayAPIClient.get_public_holidays(country_code, year) -> list of Holiday objects or dictionaries
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
    """Convert a Holiday object or API dictionary into a display-friendly dictionary."""
    name = get_value(holiday, "name", "") or get_value(holiday, "local_name", "")
    holiday_type = (
        get_value(holiday, "holiday_type", "")
        or get_value(holiday, "type", "")
        or "Public holiday"
    )
    return {
        "name": str(name or "Unnamed holiday"),
        "date": str(get_value(holiday, "date", "") or ""),
        "country_code": str(get_value(holiday, "country_code", "") or country_code),
        "description": str(get_value(holiday, "description", "") or ""),
        "holiday_type": str(holiday_type),
    }


def show_module_notice(module_name):
    st.info(
        module_name + " is not available yet. The responsible team member should "
        "push the module to their branch and submit a pull request."
    )


def load_holidays(country_code, year):
    """Load holidays through the API module supplied by the API team member."""
    from holiday_api import HolidayAPIClient

    client = HolidayAPIClient()
    return client.get_public_holidays(country_code, year)


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
    st.subheader("Compare two countries")
    first_col, second_col = st.columns(2)

    country_names = list(COUNTRIES.keys())
    with first_col:
        first_country = st.selectbox(
            "First country", country_names, index=0, key="compare_country_one"
        )
    with second_col:
        second_country = st.selectbox(
            "Second country", country_names, index=1, key="compare_country_two"
        )

    year = st.number_input(
        "Comparison year",
        min_value=2000,
        max_value=2100,
        value=2026,
        step=1,
        key="compare_year",
    )

    if first_country == second_country:
        st.session_state.pop("comparison_result", None)
        st.warning("Choose two different countries to compare.")
        return

    if st.button("Compare public holidays", type="primary"):
        # Do not keep showing a previous comparison while a new one is being made.
        st.session_state.pop("comparison_result", None)
        try:
            first_code = COUNTRIES[first_country]
            second_code = COUNTRIES[second_country]
            validate_inputs(first_code, int(year))
            validate_inputs(second_code, int(year))

            first_holidays = load_holidays(first_code, int(year))
            second_holidays = load_holidays(second_code, int(year))

            from comparison import compare_holidays

            result = compare_holidays(first_holidays, second_holidays)
            st.session_state["comparison_result"] = {
                "first_country": first_country,
                "second_country": second_country,
                "year": int(year),
                "result": result,
            }
        except ImportError as error:
            st.error("A required comparison or project module is missing: " + str(error))
        except Exception as error:
            st.error("The comparison could not be completed. Check the selected countries and try again.")
            with st.expander("Technical details for the team"):
                st.code(str(error))

    comparison_item = st.session_state.get("comparison_result")
    if comparison_item:
        st.markdown(
            "### "
            + comparison_item["first_country"]
            + " vs "
            + comparison_item["second_country"]
        )
        st.write(comparison_item["result"])

        if st.button("Save comparison"):
            try:
                from storage import save_comparison

                save_comparison(comparison_item)
                st.success("Comparison saved.")
            except ImportError:
                show_module_notice("storage.py")
            except Exception as error:
                st.error("Could not save the comparison: " + str(error))


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
