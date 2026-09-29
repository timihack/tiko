from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from app.core.appearance import DARK, Appearance
from app.core.duration import format_duration
from app.core.stopwatch import Stopwatch, StopwatchState
from app.ui.fitted_label import FittedLabel


class StopwatchView(QWidget):
    def __init__(
        self,
        stopwatch: Stopwatch | None = None,
        appearance: Appearance | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.stopwatch = stopwatch or Stopwatch()
        self.appearance = appearance or DARK

        self._display_label = FittedLabel()

        self._primary_button = QPushButton("Start")
        self._primary_button.setObjectName("controlButton")
        self._primary_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._primary_button.clicked.connect(self._on_primary_clicked)

        self._reset_button = QPushButton("Reset")
        self._reset_button.setObjectName("controlButton")
        self._reset_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._reset_button.clicked.connect(self._on_reset_clicked)

        controls_row = QHBoxLayout()
        controls_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_row.addWidget(self._primary_button)
        controls_row.addWidget(self._reset_button)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.addStretch(1)
        layout.addWidget(self._display_label)
        layout.addLayout(controls_row)
        layout.addStretch(1)

        self._ticker = QTimer(self)
        self._ticker.timeout.connect(self._refresh)
        self._ticker.start(1000)

        self.apply_appearance(self.appearance)
        self._refresh()

    def apply_appearance(self, appearance: Appearance) -> None:
        self.appearance = appearance

        display_font = QFont(appearance.font_family, appearance.time_font_size, QFont.Weight.Bold)
        display_font.setStyleHint(QFont.StyleHint.SansSerif)
        self._display_label.set_display_font(display_font)
        self._display_label.setStyleSheet(f"color: {appearance.accent_color};")

    def primary_action(self) -> None:
        self._on_primary_clicked()

    def reset(self) -> None:
        self._on_reset_clicked()

    def _on_primary_clicked(self) -> None:
        if self.stopwatch.state is StopwatchState.RUNNING:
            self.stopwatch.pause()
        else:
            self.stopwatch.start()
        self._refresh()

    def _on_reset_clicked(self) -> None:
        self.stopwatch.reset()
        self._refresh()

    def _refresh(self) -> None:
        self._display_label.setText(format_duration(self.stopwatch.elapsed()))
        if self.stopwatch.state is StopwatchState.RUNNING:
            self._primary_button.setText("Pause")
        elif self.stopwatch.state is StopwatchState.PAUSED:
            self._primary_button.setText("Resume")
        else:
            self._primary_button.setText("Start")