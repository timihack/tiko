from PySide6.QtCore import QByteArray, QSettings

from app.core.appearance import DARK, with_accent
from app.core.clock import ClockFormat
from app.core.settings import Settings


def make_settings(tmp_path, name="settings.ini"):
    backend = QSettings(str(tmp_path / name), QSettings.Format.IniFormat)
    return Settings(backend)


def test_clock_format_defaults_match_first_run_defaults(tmp_path):
    settings = make_settings(tmp_path)
    fmt = settings.load_clock_format()
    assert fmt == ClockFormat(use_24_hour=False, show_seconds=True, show_date=False)


def test_clock_format_round_trips(tmp_path):
    settings = make_settings(tmp_path)
    fmt = ClockFormat(use_24_hour=True, show_seconds=False, show_date=True)
    settings.save_clock_format(fmt)
    assert settings.load_clock_format() == fmt


def test_appearance_defaults_to_dark_theme(tmp_path):
    settings = make_settings(tmp_path)
    assert settings.load_appearance() == DARK


def test_appearance_round_trips(tmp_path):
    settings = make_settings(tmp_path)
    appearance = with_accent(DARK, "#14B8A6")
    settings.save_appearance(appearance)
    assert settings.load_appearance() == appearance


def test_always_on_top_round_trips(tmp_path):
    settings = make_settings(tmp_path)
    assert settings.load_always_on_top() is False
    settings.save_always_on_top(True)
    assert settings.load_always_on_top() is True


def test_last_mode_round_trips(tmp_path):
    settings = make_settings(tmp_path)
    assert settings.load_last_mode() == 0
    settings.save_last_mode(2)
    assert settings.load_last_mode() == 2


def test_geometry_round_trips(tmp_path):
    settings = make_settings(tmp_path)
    assert settings.load_geometry() is None
    geometry = QByteArray(b"fake-geometry-bytes")
    settings.save_geometry(geometry)
    assert bytes(settings.load_geometry()) == bytes(geometry)


def test_settings_survive_a_simulated_restart(tmp_path):
    path = tmp_path / "settings.ini"
    first = Settings(QSettings(str(path), QSettings.Format.IniFormat))
    fmt = ClockFormat(use_24_hour=True, show_seconds=True, show_date=True)
    first.save_clock_format(fmt)

    second = Settings(QSettings(str(path), QSettings.Format.IniFormat))
    assert second.load_clock_format() == fmt