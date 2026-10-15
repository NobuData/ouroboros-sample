import pytest

from durations import format_duration, parse


@pytest.mark.parametrize(
    ("seconds", "text"),
    [
        (0, "0s"),
        (45, "45s"),
        (60, "1m"),
        (3600, "1h"),
        (5400, "1h 30m"),
        (3723, "1h 2m 3s"),
        (86400, "24h"),
    ],
)
def test_formats_largest_first_without_zero_components(seconds, text):
    assert format_duration(seconds) == text


def test_refuses_a_negative_duration():
    with pytest.raises(ValueError):
        format_duration(-1)


@pytest.mark.parametrize("seconds", [0, 1, 59, 61, 3599, 3601, 7322, 86399])
def test_round_trips(seconds):
    assert parse(format_duration(seconds)) == seconds
