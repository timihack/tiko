import pytest

from app.core.timer import CountdownTimer, TimerState


class FakeClock:
    def __init__(self, start: float = 0.0):
        self.now = start

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


def test_initial_state_is_idle_with_full_duration():
    timer = CountdownTimer(60, time_source=FakeClock())
    assert timer.state is TimerState.IDLE
    assert timer.remaining() == 60
    assert not timer.is_running
    assert not timer.is_paused
    assert not timer.is_finished


def test_start_transitions_to_running_and_counts_down():
    clock = FakeClock()
    timer = CountdownTimer(60, time_source=clock)
    timer.start()
    assert timer.is_running
    clock.advance(10)
    assert timer.remaining() == 50


def test_pause_freezes_remaining_time():
    clock = FakeClock()
    timer = CountdownTimer(60, time_source=clock)
    timer.start()
    clock.advance(10)
    timer.pause()
    assert timer.is_paused
    frozen = timer.remaining()
    clock.advance(30)
    assert timer.remaining() == frozen == 50


def test_resume_continues_from_paused_point():
    clock = FakeClock()
    timer = CountdownTimer(60, time_source=clock)
    timer.start()
    clock.advance(10)
    timer.pause()
    clock.advance(1000)
    timer.resume()
    assert timer.is_running
    clock.advance(5)
    assert timer.remaining() == 45


def test_reset_returns_to_idle_with_full_duration():
    clock = FakeClock()
    timer = CountdownTimer(60, time_source=clock)
    timer.start()
    clock.advance(45)
    timer.reset()
    assert timer.state is TimerState.IDLE
    assert timer.remaining() == 60


def test_remaining_clamps_at_zero_and_marks_finished():
    clock = FakeClock()
    timer = CountdownTimer(10, time_source=clock)
    timer.start()
    clock.advance(999)
    assert timer.remaining() == 0
    assert timer.is_finished


def test_start_is_a_no_op_once_already_running():
    clock = FakeClock()
    timer = CountdownTimer(60, time_source=clock)
    timer.start()
    clock.advance(10)
    timer.start()
    assert timer.remaining() == 50


def test_pause_is_a_no_op_when_idle():
    timer = CountdownTimer(60, time_source=FakeClock())
    timer.pause()
    assert timer.state is TimerState.IDLE


def test_resume_is_a_no_op_when_running():
    clock = FakeClock()
    timer = CountdownTimer(60, time_source=clock)
    timer.start()
    clock.advance(10)
    timer.resume()
    assert timer.remaining() == 50


def test_set_duration_while_idle_updates_remaining():
    timer = CountdownTimer(60, time_source=FakeClock())
    timer.set_duration(120)
    assert timer.remaining() == 120


def test_set_duration_raises_while_running():
    timer = CountdownTimer(60, time_source=FakeClock())
    timer.start()
    with pytest.raises(RuntimeError):
        timer.set_duration(120)


def test_set_duration_rejects_non_positive_value():
    timer = CountdownTimer(60, time_source=FakeClock())
    with pytest.raises(ValueError):
        timer.set_duration(0)


def test_constructor_rejects_non_positive_duration():
    with pytest.raises(ValueError):
        CountdownTimer(0, time_source=FakeClock())