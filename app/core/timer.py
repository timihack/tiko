from __future__ import annotations

import time
from collections.abc import Callable
from enum import Enum, auto


class TimerState(Enum):
    IDLE = auto()
    RUNNING = auto()
    PAUSED = auto()


class CountdownTimer:
    def __init__(
        self,
        duration_seconds: float,
        time_source: Callable[[], float] = time.perf_counter,
    ):
        self._validate_duration(duration_seconds)
        self.duration = duration_seconds
        self._time_source = time_source
        self.state = TimerState.IDLE
        self._start_time: float | None = None
        self._elapsed_before_pause = 0.0

    def start(self) -> None:
        if self.state != TimerState.IDLE:
            return
        self._start_time = self._time_source()
        self._elapsed_before_pause = 0.0
        self.state = TimerState.RUNNING

    def pause(self) -> None:
        if self.state != TimerState.RUNNING:
            return
        self._elapsed_before_pause = self._elapsed()
        self._start_time = None
        self.state = TimerState.PAUSED

    def resume(self) -> None:
        if self.state != TimerState.PAUSED:
            return
        self._start_time = self._time_source()
        self.state = TimerState.RUNNING

    def reset(self) -> None:
        self.state = TimerState.IDLE
        self._start_time = None
        self._elapsed_before_pause = 0.0

    def set_duration(self, duration_seconds: float) -> None:
        if self.state != TimerState.IDLE:
            raise RuntimeError("cannot change duration while running or paused")
        self._validate_duration(duration_seconds)
        self.duration = duration_seconds

    def remaining(self) -> float:
        if self.state == TimerState.IDLE:
            return self.duration
        return max(0.0, self.duration - self._elapsed())

    @property
    def is_running(self) -> bool:
        return self.state == TimerState.RUNNING

    @property
    def is_paused(self) -> bool:
        return self.state == TimerState.PAUSED

    @property
    def is_finished(self) -> bool:
        return self.state == TimerState.RUNNING and self.remaining() <= 0.0

    def _elapsed(self) -> float:
        if self.state == TimerState.RUNNING and self._start_time is not None:
            return self._elapsed_before_pause + (self._time_source() - self._start_time)
        return self._elapsed_before_pause

    @staticmethod
    def _validate_duration(duration_seconds: float) -> None:
        if duration_seconds <= 0:
            raise ValueError("duration_seconds must be positive")