from app.core.stopwatch import Stopwatch, StopwatchState


class FakeClock:
    def __init__(self, start: float = 0.0):
        self.now = start

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


def test_initial_state_is_idle_with_zero_elapsed():
    stopwatch = Stopwatch(time_source=FakeClock())
    assert stopwatch.state is StopwatchState.IDLE
    assert stopwatch.elapsed() == 0
    assert not stopwatch.is_running
    assert not stopwatch.is_paused


def test_start_transitions_to_running_and_counts_up():
    clock = FakeClock()
    stopwatch = Stopwatch(time_source=clock)
    stopwatch.start()
    assert stopwatch.is_running
    clock.advance(10)
    assert stopwatch.elapsed() == 10


def test_pause_freezes_elapsed_time():
    clock = FakeClock()
    stopwatch = Stopwatch(time_source=clock)
    stopwatch.start()
    clock.advance(10)
    stopwatch.pause()
    assert stopwatch.is_paused
    frozen = stopwatch.elapsed()
    clock.advance(30)
    assert stopwatch.elapsed() == frozen == 10


def test_start_after_pause_resumes_instead_of_restarting():
    clock = FakeClock()
    stopwatch = Stopwatch(time_source=clock)
    stopwatch.start()
    clock.advance(10)
    stopwatch.pause()
    clock.advance(1000)
    stopwatch.start()
    assert stopwatch.is_running
    clock.advance(5)
    assert stopwatch.elapsed() == 15


def test_reset_returns_to_idle_with_zero_elapsed():
    clock = FakeClock()
    stopwatch = Stopwatch(time_source=clock)
    stopwatch.start()
    clock.advance(45)
    stopwatch.reset()
    assert stopwatch.state is StopwatchState.IDLE
    assert stopwatch.elapsed() == 0


def test_reset_while_running_still_zeroes_out():
    clock = FakeClock()
    stopwatch = Stopwatch(time_source=clock)
    stopwatch.start()
    clock.advance(20)
    stopwatch.reset()
    assert stopwatch.elapsed() == 0
    assert not stopwatch.is_running


def test_start_is_a_no_op_once_already_running():
    clock = FakeClock()
    stopwatch = Stopwatch(time_source=clock)
    stopwatch.start()
    clock.advance(10)
    stopwatch.start()
    assert stopwatch.elapsed() == 10


def test_pause_is_a_no_op_when_idle():
    stopwatch = Stopwatch(time_source=FakeClock())
    stopwatch.pause()
    assert stopwatch.state is StopwatchState.IDLE


def test_multiple_pause_resume_cycles_accumulate_correctly():
    clock = FakeClock()
    stopwatch = Stopwatch(time_source=clock)
    stopwatch.start()
    clock.advance(5)
    stopwatch.pause()
    clock.advance(100)
    stopwatch.start()
    clock.advance(5)
    stopwatch.pause()
    clock.advance(100)
    stopwatch.start()
    clock.advance(5)
    assert stopwatch.elapsed() == 15