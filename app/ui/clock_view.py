from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from app.core.clock import Clock


class ClockView(QWidget):
  def __init__(self, clock: Clock | None = None, parent=None):
    super().__init__(parent)
    self.clock = clock or Clock()

    self._time_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
    self._date_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

    time_font = QFont("Inter", 96, QFont.Weight.Bold)
    time_font.setStyleHint(QFont.StyleHint.SansSerif)
    self._time_label.setFont(time_font)
    self._time_label.setStyleSheet("color: #F5F5F5;")

    date_font = QFont("Inter", 20)
    date_font.setStyleHint(QFont.StyleHint.SansSerif)
    self._date_label.setFont(date_font)
    self._date_label.setStyleSheet("color: #9E9E9E;")

    layout = QVBoxLayout(self)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.setSpacing(12)
    layout.addWidget(self._time_label)
    layout.addWidget(self._date_label)

    # self.setStyleSheet("background-color: #121212;")

    self._timer = QTimer(self)
    self._timer.timeout.connect(self._refresh)
    self._timer.start(1000)
    self._refresh()


  def _refresh(self) -> None:
    self._time_label.setText(self.clock.time_string())
    self._date_label.setVisible(self.clock.format.show_date)
    if self.clock.format.show_date:
        self._date_label.setText(self.clock.date_string())