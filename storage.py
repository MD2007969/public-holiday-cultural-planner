
"""JSON file storage for favourites, cultural guides and comparisons."""

import json
from datetime import date, datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

FILES = {
    "favorites": DATA_DIR / "favorites.json",
    "guides": DATA_DIR / "guides.json",
    "comparisons": DATA_DIR / "comparisons.json",
}


class StorageError(Exception):
    """Raised when saved data cannot safely be read or written."""


def _make_serializable(item):
    """Convert Python objects into JSON-compatible values."""

    if item is None or isinstance(item, (str, int, float, bool)):
        return item

    if isinstance(item, (date, datetime)):
        return item.isoformat()

    if isinstance(item, dict):
        return {
            str(key): _make_serializable(value)
            for key, value in item.items()
        }

    if isinstance(item, (list, tuple, set)):
        return [_make_serializable(value) for value in item]

    if hasattr(item, "__dict__"):
        return {
            key: _make_serializable(value)
            for key, value in item.__dict__.items()
            if key != "country"
        }

    return str(item)


def _load_records(category):
    """Load records from a JSON file."""

    file_path = FILES[category]

    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            records = json.load(file)

    except json.JSONDecodeError as error:
        raise StorageError(
            f"{file_path.name} contains invalid JSON. "
            "The original file has been preserved."
        ) from error

    except OSError as error:
        raise StorageError(
            f"Could not read {file_path.name}: {error}"
        ) from error

    if not isinstance(records, list):
        raise StorageError(
            f"{file_path.name} must contain a JSON list."
        )

    return records


def _save_records(category, item):
    """Save a record safely using a temporary file."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    records = _load_records(category)
    records.append(_make_serializable(item))

    file_path = FILES[category]
    temporary_path = file_path.with_suffix(".tmp")

    try:
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(
                records,
                file,
                indent=4,
                ensure_ascii=False
            )

        temporary_path.replace(file_path)

    except (OSError, TypeError, ValueError) as error:
        if temporary_path.exists():
            temporary_path.unlink()

        raise StorageError(
            f"Could not save {category}: {error}"
        ) from error


def save_favorite(item):
    _save_records("favorites", item)


def load_favorites():
    return _load_records("favorites")


def save_guide(item):
    _save_records("guides", item)


def load_guides():
    return _load_records("guides")


def save_comparison(item):
    _save_records("comparisons", item)


def load_comparisons():
    return _load_records("comparisons")