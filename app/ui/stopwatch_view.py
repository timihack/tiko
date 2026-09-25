from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from app.core.duration import format_duration
from app.core.stopwatch import Stopwatch, StopwatchState


class StopwatchView(QWidget):
    def __init__(self, stopwatch: Stopwatch | None = None, parent=None):
        super().__init__(parent)
        self.stopwatch = stopwatch or Stopwatch()

        self._display_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        display_font = QFont("Inter", 72, QFont.Weight.Bold)
        display_font.setStyleHint(QFont.StyleHint.SansSerif)
        self._display_label.setFont(display_font)
        self._display_label.setStyleSheet("color: #F5F5F5;")

        self._primary_button = QPushButton("Start")
        self._primary_button.clicked.connect(self._on_primary_clicked)

        self._reset_button = QPushButton("Reset")
        self._reset_button.clicked.connect(self._on_reset_clicked)

        controls_row = QHBoxLayout()
        controls_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_row.addWidget(self._primary_button)
        controls_row.addWidget(self._reset_button)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(16)
        layout.addWidget(self._display_label)
        layout.addLayout(controls_row)

        self._ticker = QTimer(self)
        self._ticker.timeout.connect(self._refresh)
        self._ticker.start(1000)

        self._refresh()

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