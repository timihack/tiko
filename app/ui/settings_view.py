from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.core.appearance import (
    ACCENT_COLORS,
    AVAILABLE_FONTS,
    THEMES,
    Appearance,
    with_accent,
    with_font,
    with_time_font_size,
)
from app.core.clock import ClockFormat


class SettingsView(QWidget):
    clock_format_changed = Signal(object)
    appearance_changed = Signal(object)
    always_on_top_changed = Signal(bool)

    def __init__(
        self,
        clock_format: ClockFormat,
        appearance: Appearance,
        always_on_top: bool,
        parent=None,
    ):
        super().__init__(parent)

        self._time_format_combo = QComboBox()
        self._time_format_combo.addItem("12-hour", False)
        self._time_format_combo.addItem("24-hour", True)
        self._time_format_combo.setCurrentIndex(1 if clock_format.use_24_hour else 0)
        self._time_format_combo.currentIndexChanged.connect(self._on_clock_format_changed)

        self._seconds_checkbox = QCheckBox("Show seconds")
        self._seconds_checkbox.setChecked(clock_format.show_seconds)
        self._seconds_checkbox.toggled.connect(self._on_clock_format_changed)

        self._date_checkbox = QCheckBox("Show date")
        self._date_checkbox.setChecked(clock_format.show_date)
        self._date_checkbox.toggled.connect(self._on_clock_format_changed)

        self._theme_combo = QComboBox()
        for name in THEMES:
            self._theme_combo.addItem(name, name)
        self._theme_combo.setCurrentText(appearance.theme_name)
        self._theme_combo.currentIndexChanged.connect(self._on_appearance_changed)

        self._font_combo = QComboBox()
        for font in AVAILABLE_FONTS:
            self._font_combo.addItem(font, font)
        self._font_combo.setCurrentText(appearance.font_family)
        self._font_combo.currentIndexChanged.connect(self._on_appearance_changed)

        self._font_size_spin = QSpinBox()
        self._font_size_spin.setRange(48, 200)
        self._font_size_spin.setValue(appearance.time_font_size)
        self._font_size_spin.valueChanged.connect(self._on_appearance_changed)

        self._accent_combo = QComboBox()
        self._accent_combo.addItem("Theme default", None)
        for name, hex_color in ACCENT_COLORS.items():
            self._accent_combo.addItem(name, hex_color)
        self._accent_combo.currentIndexChanged.connect(self._on_appearance_changed)

        self._always_on_top_checkbox = QCheckBox("Always on top")
        self._always_on_top_checkbox.setChecked(always_on_top)
        self._always_on_top_checkbox.toggled.connect(self.always_on_top_changed)

        form = QFormLayout()
        form.addRow("Time format", self._time_format_combo)
        form.addRow(self._seconds_checkbox)
        form.addRow(self._date_checkbox)
        form.addRow("Theme", self._theme_combo)
        form.addRow("Font", self._font_combo)
        form.addRow("Font size", self._font_size_spin)
        form.addRow("Clock color", self._accent_combo)
        form.addRow(self._always_on_top_checkbox)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(48, 32, 48, 32)
        layout.addLayout(form)

    def _on_clock_format_changed(self, *_args) -> None:
        fmt = ClockFormat(
            use_24_hour=self._time_format_combo.currentData(),
            show_seconds=self._seconds_checkbox.isChecked(),
            show_date=self._date_checkbox.isChecked(),
        )
        self.clock_format_changed.emit(fmt)

    def _on_appearance_changed(self, *_args) -> None:
        appearance = THEMES[self._theme_combo.currentData()]
        appearance = with_font(appearance, self._font_combo.currentData())
        accent_override = self._accent_combo.currentData()
        if accent_override:
            appearance = with_accent(appearance, accent_override)
        appearance = with_time_font_size(appearance, self._font_size_spin.value())
        self.appearance_changed.emit(appearance)