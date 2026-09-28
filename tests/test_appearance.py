import pytest

from app.core.appearance import (
    DARK,
    LIGHT,
    with_accent,
    with_font,
    with_time_font_size,
    theme_by_name,
)


def test_theme_by_name_returns_known_themes():
    assert theme_by_name("Dark") is DARK
    assert theme_by_name("Light") is LIGHT


def test_theme_by_name_rejects_unknown_theme():
    with pytest.raises(ValueError):
        theme_by_name("Solarized")


def test_dark_and_light_have_distinct_high_contrast_defaults():
    assert DARK.background_color != LIGHT.background_color
    assert DARK.accent_color != LIGHT.accent_color


def test_with_accent_overrides_only_accent_color():
    updated = with_accent(DARK, "#14B8A6")
    assert updated.accent_color == "#14B8A6"
    assert updated.background_color == DARK.background_color
    assert updated.theme_name == DARK.theme_name


def test_with_accent_rejects_invalid_hex():
    with pytest.raises(ValueError):
        with_accent(DARK, "teal")


def test_with_font_overrides_only_font_family():
    updated = with_font(DARK, "JetBrains Mono")
    assert updated.font_family == "JetBrains Mono"
    assert updated.accent_color == DARK.accent_color


def test_with_font_rejects_unknown_font():
    with pytest.raises(ValueError):
        with_font(DARK, "Comic Sans")


def test_with_time_font_size_overrides_only_size():
    updated = with_time_font_size(DARK, 120)
    assert updated.time_font_size == 120
    assert updated.font_family == DARK.font_family


def test_with_time_font_size_rejects_non_positive():
    with pytest.raises(ValueError):
        with_time_font_size(DARK, 0)


def test_with_accent_rejects_wrong_length_hex():
    with pytest.raises(ValueError):
        with_accent(DARK, "#12345")
    with pytest.raises(ValueError):
        with_accent(DARK, "#1234567")