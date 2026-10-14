"""The parser and the formatter."""

from __future__ import annotations

import re

#: The units, largest first, as (suffix, seconds).
UNITS: tuple[tuple[str, int], ...] = (("h", 3600), ("m", 60), ("s", 1))

_SECONDS = dict(UNITS)

#: One component: a whole number followed by a unit suffix, e.g. ``90m``.
_COMPONENT = re.compile(r"(\d+)([hms])")


def parse(text: str) -> int:
    """Parse a duration such as ``"1h 30m"`` or ``"45s"`` into whole seconds.

    Components may be separated by spaces or written together (``"1h30m"``). Each unit
    may appear once, in any order.

    Args:
        text: The duration.

    Returns:
        The duration in seconds.

    Raises:
        ValueError: The text is empty, or is not made of ``<number><unit>`` components.
    """
    compact = "".join(text.split())
    if not compact:
        raise ValueError("empty duration")

    total = 0
    seen: set[str] = set()
    position = 0
    for match in _COMPONENT.finditer(compact):
        if match.start() != position:
            raise ValueError(f"invalid duration: {text!r}")
        amount, unit = match.groups()
        if unit in seen:
            raise ValueError(f"unit {unit!r} given twice in {text!r}")
        seen.add(unit)
        total += int(amount) * _SECONDS[unit]
        position = match.end()

    if position != len(compact):
        raise ValueError(f"invalid duration: {text!r}")
    return total


def format_duration(seconds: int) -> str:
    """Format whole seconds as a duration such as ``"1h 30m"``.

    Zero components are left out: ``3600`` is ``"1h"``, not ``"1h 0m 0s"``.

    Args:
        seconds: A non-negative number of seconds.

    Returns:
        The duration, largest unit first.

    Raises:
        ValueError: ``seconds`` is negative.
    """
    if seconds < 0:
        raise ValueError("a duration cannot be negative")

    parts = []
    remaining = seconds
    for unit, size in UNITS:
        amount, remaining = divmod(remaining, size)
        if amount:
            parts.append(f"{amount}{unit}")
    return " ".join(parts)
