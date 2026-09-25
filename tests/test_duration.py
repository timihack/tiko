from app.core.duration import format_duration


def test_zero_seconds():
    assert format_duration(0) == "00:00"


def test_under_a_minute():
    assert format_duration(59) == "00:59"


def test_exactly_one_minute():
    assert format_duration(60) == "01:00"


def test_minutes_and_seconds():
    assert format_duration(125) == "02:05"


def test_over_an_hour_includes_hours():
    assert format_duration(3661) == "1:01:01"


def test_negative_values_clamp_to_zero():
    assert format_duration(-5) == "00:00"


def test_rounds_fractional_seconds():
    assert format_duration(59.6) == "01:00"