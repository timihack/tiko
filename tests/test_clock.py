import datetime as dt

from app.core.clock import Clock, ClockFormat, format_date, format_time

FIXED_MOMENT = dt.datetime(2026, 9, 25, 14, 5, 9)


def test_format_time_24_hour_with_seconds():
  fmt = ClockFormat(use_24_hour=True, show_seconds=True)
  assert format_time(FIXED_MOMENT, fmt) == "14:05:09"

def test_format_time_24_hour_without_seconds():
  fmt = ClockFormat(use_24_hour=True, show_seconds=False)
  assert format_time(FIXED_MOMENT, fmt) == "14:05"
 
 
def test_format_time_12_hour_with_seconds():
  fmt = ClockFormat(use_24_hour=False, show_seconds=True)
  assert format_time(FIXED_MOMENT, fmt) == "02:05:09 PM"


def test_format_time_12_hour_without_seconds():
  fmt = ClockFormat(use_24_hour=False, show_seconds=False)
  assert format_time(FIXED_MOMENT, fmt) == "02:05 PM"


def test_format_date():
  assert format_date(FIXED_MOMENT) == "Friday, September 25"


def test_default_format_matches_first_run_defaults():
  fmt = ClockFormat()
  assert fmt.use_24_hour is False
  assert fmt.show_seconds is True
  assert fmt.show_date is False

def test_clock_uses_injected_time_source():
  clock = Clock(ClockFormat(use_24_hour=True, show_seconds=True), time_source=lambda: FIXED_MOMENT)
  assert clock.time_string() == "14:05:09"
  assert clock.date_string() == "Friday, September 25"