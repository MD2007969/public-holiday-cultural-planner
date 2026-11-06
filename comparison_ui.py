# comparison_ui.py
# Comparison UI helpers for the Public Holiday & Cultural Awareness Planner
# Made by Favour Onu

from models import Country, Holiday
from datetime import datetime

class ComparisonUI:
    """
    Simple class to help with comparing holidays between two countries
    and preparing the result for the UI.
    """
    def __init__(self, country1, country2):
        self.country1 = country1
        self.country2 = country2

    def find_shared_holidays(self):
        """Find holidays that have the same name in both countries."""
        shared = []
        names1 = {h.name.lower() for h in self.country1.holidays}
        for h2 in self.country2.holidays:
            if h2.name.lower() in names1:
                shared.append(h2.name)
        return shared

    def find_overlapping_dates(self):
        """Find holidays that fall on the same date in both countries."""
        overlaps = []
        dates1 = {h.date.date(): h for h in self.country1.holidays}
        for h2 in self.country2.holidays:
            date_key = h2.date.date()
            if date_key in dates1:
                h1 = dates1[date_key]
                overlaps.append({
                    "date": date_key.strftime("%d %B %Y"),
                    "country1_holiday": h1.name,
                    "country2_holiday": h2.name
                })
        return overlaps

    def get_comparison_summary(self):
        """Return a simple dictionary with comparison results for the UI."""
        shared = self.find_shared_holidays()
        overlaps = self.find_overlapping_dates()

        summary = {
            "country1": str(self.country1),
            "country2": str(self.country2),
            "shared_holiday_names": shared,
            "overlapping_dates": overlaps,
            "total_holidays_country1": len(self.country1.holidays),
            "total_holidays_country2": len(self.country2.holidays)
        }
        return summary

    def get_formatted_result(self):
        """Return a nice text version of the comparison (useful for UI or saving)."""
        summary = self.get_comparison_summary()
        lines = []
        lines.append(f"Comparison: {summary['country1']} vs {summary['country2']}")
        lines.append("-" * 50)
        lines.append(f"Total holidays: {summary['total_holidays_country1']} vs {summary['total_holidays_country2']}")
        lines.append("")

        if summary["shared_holiday_names"]:
            lines.append("Shared holiday names:")
            for name in summary["shared_holiday_names"]:
                lines.append(f"  - {name}")
        else:
            lines.append("No shared holiday names found.")

        lines.append("")
        if summary["overlapping_dates"]:
            lines.append("Overlapping dates:")
            for item in summary["overlapping_dates"]:
                lines.append(f"  {item['date']}: {item['country1_holiday']} | {item['country2_holiday']}")
        else:
            lines.append("No overlapping dates found.")

        return "\n".join(lines)
