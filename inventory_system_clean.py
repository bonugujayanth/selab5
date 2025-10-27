"""Cleaned inventory system for Lab 5 (fixed common static-analysis issues).

Fixes applied (high level):
- Removed mutable default arguments
- Replaced bare excepts with specific exceptions
- Removed eval usage
- Added input validation and type hints
- Used context managers for file I/O and JSON error handling
- Guarded main with if __name__ == '__main__'
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Simple in-memory stock mapping: item name -> quantity
stock_data: Dict[str, int] = {}

logger = logging.getLogger(__name__)


def add_item(item: str, qty: int, logs: Optional[List[str]] = None) -> None:
    """Add qty of item to stock. Raises on invalid types/values.

    Args:
        item: item name (str)
        qty: positive integer quantity to add
        logs: optional list to append a human-readable log line
    """
    if logs is None:
        logs = []
    if not isinstance(item, str):
        raise TypeError("item must be a string")
    if not isinstance(qty, int):
        raise TypeError("qty must be an int")
    if qty <= 0:
        raise ValueError("qty must be a positive integer")

    stock_data[item] = stock_data.get(item, 0) + qty
    timestamp = datetime.now().isoformat()
    line = f"{timestamp}: Added {qty} of {item}"
    logs.append(line)
    logger.info(line)


def remove_item(item: str, qty: int) -> None:
    """Remove qty of item from stock. If item not present, nothing happens.

    Args:
        item: item name
        qty: positive integer quantity to remove
    """
    if not isinstance(item, str):
        raise TypeError("item must be a string")
    if not isinstance(qty, int):
        raise TypeError("qty must be an int")
    if qty <= 0:
        raise ValueError("qty must be a positive integer")

    if item not in stock_data:
        logger.warning("Attempted to remove non-existent item: %s", item)
        return

    current = stock_data[item]
    if qty >= current:
        del stock_data[item]
        logger.info("Removed item %s entirely", item)
    else:
        stock_data[item] = current - qty
        logger.info("Removed %d of %s", qty, item)


def get_qty(item: str) -> int:
    """Return quantity for item; return 0 when item not found."""
    if not isinstance(item, str):
        raise TypeError("item must be a string")
    return stock_data.get(item, 0)


def load_data(file: str = "inventory.json") -> None:
    """Load stock data from JSON file. Invalid content is ignored."""
    try:
        with open(file, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            # coerce keys to str and values to int when possible
            cleaned: Dict[str, int] = {}
            for k, v in data.items():
                try:
                    cleaned[str(k)] = int(v)
                except (TypeError, ValueError):
                    logger.warning(
                        "Skipping invalid value for key %s: %r", k, v
                    )
            # mutate the existing dict to avoid rebinding the global name
            stock_data.clear()
            stock_data.update(cleaned)
        else:
            logger.warning(
                "Data in %s is not a JSON object; starting empty", file
            )
            stock_data.clear()
    except FileNotFoundError:
        logger.info(
            "Data file %s not found; starting with empty stock", file
        )
        stock_data.clear()
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse JSON in %s: %s", file, exc)
        stock_data.clear()


def save_data(file: str = "inventory.json") -> None:
    """Save stock data to JSON file. Logs on error."""
    try:
        with open(file, "w", encoding="utf-8") as fh:
            json.dump(stock_data, fh, indent=2, sort_keys=True)
    except OSError as exc:
        logger.error("Failed to save data to %s: %s", file, exc)


def print_data() -> None:
    """Print a simple items report to stdout."""
    print("Items Report")
    for name in sorted(stock_data):
        print(name, "->", stock_data[name])


def check_low_items(threshold: int = 5) -> List[str]:
    """Return list of item names whose quantity is below threshold."""
    if not isinstance(threshold, int):
        raise TypeError("threshold must be an int")
    return [name for name, qty in stock_data.items() if qty < threshold]


def main() -> None:
    """Run a small example of inventory operations (used when executed).

    Exceptions raised by the example operations are logged. Specific
    exception types are handled rather than catching Exception broadly.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    logger.info("Starting inventory example")

    # Example usage (kept minimal and safe)
    try:
        add_item("apple", 10)
        add_item("banana", 2)
        remove_item("apple", 3)
        print("Apple stock:", get_qty("apple"))
        print("Low items:", check_low_items())
        save_data()
        load_data()
        print_data()
    except (TypeError, ValueError, OSError, json.JSONDecodeError) as exc:
        logger.exception("Example raised an error: %s", exc)


if __name__ == "__main__":
    main()
