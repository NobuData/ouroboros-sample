import pytest

from durations import parse


@pytest.mark.parametrize(
    ("text", "seconds"),
    [
        ("45s", 45),
        ("2m", 120),
        ("1h", 3600),
        ("1h 30m", 5400),
        ("1h30m", 5400),
        ("30m 1h", 5400),
        ("  1h   2m  3s ", 3723),
        ("90m", 5400),
        ("0s", 0),
    ],
)
def test_parses_components(text, seconds):
    assert parse(text) == seconds


@pytest.mark.parametrize("text", ["", "   ", "1", "h", "1x", "1h 2", "1h 1h", "-1h", "1.5h", "one hour"])
def test_refuses_what_is_not_a_duration(text):
    with pytest.raises(ValueError):
        parse(text)
