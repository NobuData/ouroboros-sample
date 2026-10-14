"""``python -m durations`` — convert between durations and seconds.

    $ python -m durations 1h 30m
    5400
    $ python -m durations --format 5400
    1h 30m
"""

from __future__ import annotations

import argparse
import sys

from durations.core import format_duration, parse


def main(argv: list[str] | None = None) -> int:
    """Run the command line.

    Args:
        argv: The arguments, without the program name. Defaults to ``sys.argv[1:]``.

    Returns:
        The exit status: 0 on success, 2 when the input could not be read.
    """
    parser = argparse.ArgumentParser(prog="durations", description=__doc__.splitlines()[0])
    parser.add_argument("value", nargs="+", help="a duration such as 1h 30m, or seconds with --format")
    parser.add_argument("--format", action="store_true", help="read seconds and print a duration")
    args = parser.parse_args(argv)

    text = " ".join(args.value)
    try:
        if args.format:
            print(format_duration(int(text)))
        else:
            print(parse(text))
    except ValueError as error:
        print(f"durations: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
