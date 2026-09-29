from __future__ import annotations

from dataclasses import dataclass, replace

AVAILABLE_FONTS = ("Inter", "JetBrains Mono", "IBM Plex Mono", "Roboto Mono")

ACCENT_COLORS = {
    "Teal": "#0D9488",
    "Amber": "#D97706",
    "Coral": "#DC2626",
}


@dataclass(frozen=True)
class Appearance:
    theme_name: str
    background_color: str
    surface_color: str
    border_color: str
    text_color: str
    secondary_text_color: str
    accent_color: str
    font_family: str = "Inter"
    time_font_size: int = 96
    secondary_font_size: int = 20


DARK = Appearance(
    theme_name="Dark",
    background_color="#121212",
    surface_color="#1E1E1E",
    border_color="#3A3A3A",
    text_color="#E0E0E0",
    secondary_text_color="#9E9E9E",
    accent_color="#F5F5F5",
)

LIGHT = Appearance(
    theme_name="Light",
    background_color="#FAFAFA",
    surface_color="#FFFFFF",
    border_color="#CFCFCF",
    text_color="#212121",
    secondary_text_color="#616161",
    accent_color="#212121",
)

THEMES = {"Dark": DARK, "Light": LIGHT}


def theme_by_name(name: str) -> Appearance:
    try:
        return THEMES[name]
    except KeyError as exc:
        raise ValueError(f"unknown theme: {name!r}") from exc


def is_valid_accent(color: str) -> bool:
    return color.startswith("#") and len(color) == 7


def with_accent(appearance: Appearance, accent_color: str) -> Appearance:
    if not is_valid_accent(accent_color):
        raise ValueError(f"accent_color must be a '#rrggbb' hex string, got {accent_color!r}")
    return replace(appearance, accent_color=accent_color)


def with_font(appearance: Appearance, font_family: str) -> Appearance:
    if font_family not in AVAILABLE_FONTS:
        raise ValueError(f"unknown font: {font_family!r}")
    return replace(appearance, font_family=font_family)


def with_time_font_size(appearance: Appearance, size: int) -> Appearance:
    if size <= 0:
        raise ValueError("time_font_size must be positive")
    return replace(appearance, time_font_size=size)