from __future__ import annotations

import datetime as dt
from collections.abc import Callable
from dataclasses import dataclass

@dataclass
class ClockFormat:
  use_24_hour: bool = False
  show_seconds: bool = True
  show_date: bool = False


def format_time(moment: dt.datetime, fmt: ClockFormat) -> str:
  if fmt.use_24_hour:
    pattern = "%H:%M:%S" if fmt.show_seconds else "%H:%M"
  else:
    pattern = "%I:%M:%S %p" if fmt.show_seconds else "%I:%M %p"

  return moment.strftime(pattern)


def format_date(moment: dt.datetime) -> str:
  return moment.strftime("%A, %B %d")


class Clock:
  def __init__(
      self,
      fmt: ClockFormat | None = None,
      time_source: Callable[[], dt.datetime] = dt.datetime.now
  ):
    self.format = fmt or ClockFormat()
    self._time_source = time_source

  def time_string(self) -> str:
    return format_time(self._time_source(), self.format)
  
  def date_string(self) -> str:
    return format_date(self._time_source())
