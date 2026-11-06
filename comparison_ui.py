# comparison_ui.py
# Comparison UI helpers for the Public Holiday & Cultural Awareness Planner
# Based on Favour Onu's original comparison module, with main-app integration.

from datetime import date, datetime
from types import SimpleNamespace

import streamlit as st

from models import Country, Holiday


def _as_date(value):
    """Convert supported date values to a date object, or return None."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if value is None or value == "":
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return None


def _holiday_value(holiday, key, default=None):
    """Read a holiday field from either a dictionary or an object."""
    if isinstance(holiday, dict):
        return holiday.get(key, default)
    return getattr(holiday, key, default)


def _normalise_holiday(holiday, country):
    """Convert API holiday data into the project's Holiday model."""
    name = (
        _holiday_value(holiday, "name")
        or _holiday_value(holiday, "local_name")
        or "Unnamed holiday"
    )
    raw_date = _holiday_value(holiday, "date")
    parsed_date = _as_date(raw_date)
    if parsed_date is None:
        return None

    holiday_type = (
        _holiday_value(holiday, "holiday_type")
        or _holiday_value(holiday, "type")
        or _holiday_value(holiday, "types")
        or "Public holiday"
    )
    if isinstance(holiday_type, (list, tuple)):
        holiday_type = ", ".join(str(item) for item in holiday_type)

    return Holiday(
        str(name),
        datetime.combine(parsed_date, datetime.min.time()),
        str(holiday_type),
        country,
    )


class ComparisonUI:
    """
    Compare public holidays between two Country objects.

    The original Favour methods are retained, with date handling that
    supports datetime, date, and ISO-formatted string values.
    """

    def __init__(self, country1, country2):
        self.country1 = country1
        self.country2 = country2

    def find_shared_holidays(self):
        """Find holiday names appearing in both countries, ignoring case."""
        names1 = {
            str(holiday.name).strip().casefold()
            for holiday in self.country1.holidays
        }
        shared = []
        seen = set()
        for holiday in self.country2.holidays:
            name = str(holiday.name).strip()
            key = name.casefold()
            if key in names1 and key not in seen:
                shared.append(name)
                seen.add(key)
        return shared

    def find_overlapping_dates(self):
        """Find holidays that occur on the same calendar date."""
        dates1 = {}
        for holiday in self.country1.holidays:
            key = _as_date(holiday.date)
            if key is not None:
                dates1.setdefault(key, holiday)

        overlaps = []
        for holiday in self.country2.holidays:
            key = _as_date(holiday.date)
            if key is not None and key in dates1:
                first = dates1[key]
                overlaps.append({
                    "date": key.strftime("%d %B %Y"),
                    "country1_holiday": first.name,
                    "country2_holiday": holiday.name,
                })
        return overlaps

    def get_comparison_summary(self):
        """Return comparison results in a dictionary."""
        shared = self.find_shared_holidays()
        overlaps = self.find_overlapping_dates()
        return {
            "country1": str(self.country1),
            "country2": str(self.country2),
            "shared_holiday_names": shared,
            "overlapping_dates": overlaps,
            "total_holidays_country1": len(self.country1.holidays),
            "total_holidays_country2": len(self.country2.holidays),
        }

    def get_formatted_result(self):
        """Return a readable text summary of the comparison."""
        summary = self.get_comparison_summary()
        lines = [
            f"Comparison: {summary['country1']} vs {summary['country2']}",
            "-" * 50,
            (
                "Total holidays: "
                f"{summary['total_holidays_country1']} vs "
                f"{summary['total_holidays_country2']}"
            ),
            "",
        ]

        if summary["shared_holiday_names"]:
            lines.append("Shared holiday names:")
            lines.extend(
                f"  - {name}" for name in summary["shared_holiday_names"]
            )
        else:
            lines.append("No shared holiday names found.")

        lines.append("")
        if summary["overlapping_dates"]:
            lines.append("Overlapping dates:")
            for item in summary["overlapping_dates"]:
                lines.append(
                    f"  {item['date']}: {item['country1_holiday']} | "
                    f"{item['country2_holiday']}"
                )
        else:
            lines.append("No overlapping dates found.")

        return "\n".join(lines)


def render_comparison_page(countries, load_holidays, validate_inputs):
    """
    Render the comparison page expected by main.py.

    Args:
        countries: Mapping of display country names to country codes.
        load_holidays: Callable accepting (country_code, year).
        validate_inputs: Callable accepting (country_code, year).
    """
    st.subheader("Compare public holidays between two countries")

    country_names = list(countries.keys())
    if len(country_names) < 2:
        st.warning("At least two countries are required for comparison.")
        return

    col1, col2 = st.columns(2)
    with col1:
        country1_name = st.selectbox(
            "First country",
            country_names,
            key="comparison_country_one",
        )
    with col2:
        country2_options = [
            name for name in country_names if name != country1_name
        ]
        country2_name = st.selectbox(
            "Second country",
            country2_options,
            key="comparison_country_two",
        )

    year = st.number_input(
        "Holiday year",
        min_value=2000,
        max_value=2100,
        value=datetime.now().year,
        step=1,
        key="comparison_year",
    )

    if not st.button("Compare Countries", type="primary"):
        return

    code1 = countries[country1_name]
    code2 = countries[country2_name]

    try:
        validate_inputs(code1, int(year))
        validate_inputs(code2, int(year))

        with st.spinner("Loading holidays and comparing countries..."):
            holidays1 = load_holidays(code1, int(year))
            holidays2 = load_holidays(code2, int(year))

        first_country = Country(code1, country1_name)
        second_country = Country(code2, country2_name)

        for item in holidays1:
            normalised = _normalise_holiday(item, first_country)
            if normalised is not None:
                first_country.add_holiday(normalised)

        for item in holidays2:
            normalised = _normalise_holiday(item, second_country)
            if normalised is not None:
                second_country.add_holiday(normalised)

        comparison = ComparisonUI(first_country, second_country)
        summary = comparison.get_comparison_summary()

        st.success("Country comparison completed.")

        metric1, metric2 = st.columns(2)
        metric1.metric(
            f"{country1_name} holidays",
            summary["total_holidays_country1"],
        )
        metric2.metric(
            f"{country2_name} holidays",
            summary["total_holidays_country2"],
        )

        st.markdown("#### Shared holiday names")
        if summary["shared_holiday_names"]:
            for name in summary["shared_holiday_names"]:
                st.write(f"- {name}")
        else:
            st.info("No holidays with matching names were found.")

        st.markdown("#### Holidays on overlapping dates")
        if summary["overlapping_dates"]:
            st.dataframe(
                summary["overlapping_dates"],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No holidays fall on the same dates in both countries.")

        with st.expander("View comparison summary"):
            st.text(comparison.get_formatted_result())

    except Exception as error:
        st.error("We could not complete the country comparison.")
        st.caption(str(error))
