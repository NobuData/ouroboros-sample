"""Parse and format human-readable durations.

    >>> parse("1h 30m")
    5400
    >>> format_duration(5400)
    '1h 30m'

Durations are whole seconds. The units are ``h`` (hours), ``m`` (minutes) and ``s``
(seconds), largest first.
"""

from durations.core import UNITS, format_duration, parse

__all__ = ["UNITS", "format_duration", "parse"]
__version__ = "0.1.0"
