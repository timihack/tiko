from __future__ import annotations

import time
from collections.abc import Callable
from enum import Enum, auto


class StopwatchState(Enum):
    IDLE = auto()
    RUNNING = auto()
    PAUSED = auto()


class Stopwatch:
    def __init__(self, time_source: Callable[[], float] = time.perf_counter):
        self._time_source = time_source
        self.state = StopwatchState.IDLE
        self._start_time: float | None = None
        self._elapsed_before_pause = 0.0

    def start(self) -> None:
        if self.state == StopwatchState.RUNNING:
            return
        self._start_time = self._time_source()
        self.state = StopwatchState.RUNNING

    def pause(self) -> None:
        if self.state != StopwatchState.RUNNING:
            return
        self._elapsed_before_pause = self._elapsed()
        self._start_time = None
        self.state = StopwatchState.PAUSED

    def reset(self) -> None:
        self.state = StopwatchState.IDLE
        self._start_time = None
        self._elapsed_before_pause = 0.0

    def elapsed(self) -> float:
        return self._elapsed()

    @property
    def is_running(self) -> bool:
        return self.state == StopwatchState.RUNNING

    @property
    def is_paused(self) -> bool:
        return self.state == StopwatchState.PAUSED

    def _elapsed(self) -> float:
        if self.state == StopwatchState.RUNNING and self._start_time is not None:
            return self._elapsed_before_pause + (self._time_source() - self._start_time)
        return self._elapsed_before_pause