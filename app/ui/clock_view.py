from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from app.core.appearance import DARK, Appearance
from app.core.clock import Clock, ClockFormat
from app.ui.fitted_label import FittedLabel


class ClockView(QWidget):
    def __init__(
        self,
        clock: Clock | None = None,
        appearance: Appearance | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.clock = clock or Clock()
        self.appearance = appearance or DARK

        self._time_label = FittedLabel()
        self._date_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.addStretch(1)
        layout.addWidget(self._time_label)
        layout.addWidget(self._date_label)
        layout.addStretch(1)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(1000)

        self.apply_appearance(self.appearance)
        self._refresh()

    def apply_appearance(self, appearance: Appearance) -> None:
        self.appearance = appearance

        time_font = QFont(appearance.font_family, appearance.time_font_size, QFont.Weight.Bold)
        time_font.setStyleHint(QFont.StyleHint.SansSerif)
        self._time_label.set_display_font(time_font)
        self._time_label.setStyleSheet(f"color: {appearance.accent_color};")

        date_font = QFont(appearance.font_family, appearance.secondary_font_size)
        date_font.setStyleHint(QFont.StyleHint.SansSerif)
        self._date_label.setFont(date_font)
        self._date_label.setStyleSheet(f"color: {appearance.secondary_text_color};")

    def apply_clock_format(self, fmt: ClockFormat) -> None:
        self.clock.format = fmt
        self._refresh()

    def _refresh(self) -> None:
        self._time_label.setText(self.clock.time_string())
        self._date_label.setVisible(self.clock.format.show_date)
        if self.clock.format.show_date:
            self._date_label.setText(self.clock.date_string())