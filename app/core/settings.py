from __future__ import annotations

from PySide6.QtCore import QByteArray, QSettings

from app.core.appearance import (
    AVAILABLE_FONTS,
    THEMES,
    Appearance,
    theme_by_name,
    with_accent,
    with_font,
    with_time_font_size,
)
from app.core.clock import ClockFormat

ORGANIZATION = "Tiko"
APPLICATION = "Tiko"


class Settings:
    def __init__(self, backend: QSettings | None = None):
        self._settings = backend or QSettings(ORGANIZATION, APPLICATION)

    def load_clock_format(self) -> ClockFormat:
        return ClockFormat(
            use_24_hour=bool(self._settings.value("clock/use_24_hour", False, type=bool)),
            show_seconds=bool(self._settings.value("clock/show_seconds", True, type=bool)),
            show_date=bool(self._settings.value("clock/show_date", False, type=bool)),
        )

    def save_clock_format(self, fmt: ClockFormat) -> None:
        self._settings.setValue("clock/use_24_hour", fmt.use_24_hour)
        self._settings.setValue("clock/show_seconds", fmt.show_seconds)
        self._settings.setValue("clock/show_date", fmt.show_date)

    def load_appearance(self) -> Appearance:
        theme_name = str(self._settings.value("appearance/theme_name", "Dark", type=str))
        base = theme_by_name(theme_name) if theme_name in THEMES else THEMES["Dark"]

        font_family = str(self._settings.value("appearance/font_family", base.font_family, type=str))
        appearance = with_font(base, font_family) if font_family in AVAILABLE_FONTS else base

        accent = str(self._settings.value("appearance/accent_color", appearance.accent_color, type=str))
        appearance = with_accent(appearance, accent)

        time_font_size = int(self._settings.value("appearance/time_font_size", appearance.time_font_size, type=int))
        appearance = with_time_font_size(appearance, time_font_size)

        return appearance

    def save_appearance(self, appearance: Appearance) -> None:
        self._settings.setValue("appearance/theme_name", appearance.theme_name)
        self._settings.setValue("appearance/accent_color", appearance.accent_color)
        self._settings.setValue("appearance/font_family", appearance.font_family)
        self._settings.setValue("appearance/time_font_size", appearance.time_font_size)

    def load_always_on_top(self) -> bool:
        return bool(self._settings.value("window/always_on_top", False, type=bool))

    def save_always_on_top(self, value: bool) -> None:
        self._settings.setValue("window/always_on_top", value)

    def load_last_mode(self) -> int:
        return int(self._settings.value("window/last_mode", 0, type=int))

    def save_last_mode(self, index: int) -> None:
        self._settings.setValue("window/last_mode", index)

    def load_geometry(self) -> QByteArray | None:
        value = self._settings.value("window/geometry", QByteArray(), type=QByteArray)
        return value if value else None

    def save_geometry(self, geometry: QByteArray) -> None:
        self._settings.setValue("window/geometry", geometry)