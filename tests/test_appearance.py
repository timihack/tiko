import pytest

from app.core.appearance import (
    ACCENT_COLORS,
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


def _luminance(hex_color):
    hex_color = hex_color.lstrip("#")
    channels = [int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(foreground, background):
    lighter, darker = sorted((_luminance(foreground), _luminance(background)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


@pytest.mark.parametrize("theme", [DARK, LIGHT], ids=["dark", "light"])
@pytest.mark.parametrize("name, color", sorted(ACCENT_COLORS.items()))
def test_accent_presets_are_readable_as_large_text_on_every_theme(theme, name, color):
    assert contrast_ratio(color, theme.background_color) >= 3.0, f"{name} on {theme.theme_name}"


@pytest.mark.parametrize("theme", [DARK, LIGHT], ids=["dark", "light"])
def test_ui_text_meets_normal_text_contrast_on_every_surface(theme):
    assert contrast_ratio(theme.text_color, theme.background_color) >= 4.5
    assert contrast_ratio(theme.text_color, theme.surface_color) >= 4.5
    assert contrast_ratio(theme.secondary_text_color, theme.background_color) >= 4.5


@pytest.mark.parametrize("theme", [DARK, LIGHT], ids=["dark", "light"])
def test_default_accent_is_readable_as_large_text(theme):
    assert contrast_ratio(theme.accent_color, theme.background_color) >= 3.0