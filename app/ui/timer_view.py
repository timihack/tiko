from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.core.appearance import DARK, Appearance
from app.core.duration import format_duration
from app.core.timer import CountdownTimer, TimerState
from app.ui.notifications import Notifier

_PRESET_MINUTES = [1, 5, 10, 25, 30, 45, 60]


class TimerView(QWidget):
    def __init__(
        self,
        timer: CountdownTimer | None = None,
        appearance: Appearance | None = None,
        notifier: Notifier | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.timer = timer or CountdownTimer(_PRESET_MINUTES[0] * 60)
        self.appearance = appearance or DARK
        self._notifier = notifier or Notifier(self)
        self._has_notified_finished = False

        self._display_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        self._duration_combo = QComboBox()
        for minutes in _PRESET_MINUTES:
            label = f"{minutes} minute" + ("s" if minutes != 1 else "")
            self._duration_combo.addItem(label, minutes)
        self._duration_combo.addItem("Custom…", None)
        self._duration_combo.currentIndexChanged.connect(self._on_preset_changed)

        self._custom_spinbox = QSpinBox()
        self._custom_spinbox.setRange(1, 180)
        self._custom_spinbox.setSuffix(" min")
        self._custom_spinbox.setValue(1)
        self._custom_spinbox.setVisible(False)
        self._custom_spinbox.valueChanged.connect(self._on_custom_minutes_changed)

        duration_row = QHBoxLayout()
        duration_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        duration_row.addWidget(self._duration_combo)
        duration_row.addWidget(self._custom_spinbox)

        self._primary_button = QPushButton("Start")
        self._primary_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._primary_button.clicked.connect(self._on_primary_clicked)

        self._reset_button = QPushButton("Reset")
        self._reset_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._reset_button.clicked.connect(self._on_reset_clicked)

        controls_row = QHBoxLayout()
        controls_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_row.addWidget(self._primary_button)
        controls_row.addWidget(self._reset_button)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(16)
        layout.addWidget(self._display_label)
        layout.addLayout(duration_row)
        layout.addLayout(controls_row)

        self._ticker = QTimer(self)
        self._ticker.timeout.connect(self._refresh)
        self._ticker.start(1000)

        self.apply_appearance(self.appearance)
        self._refresh()

    def apply_appearance(self, appearance: Appearance) -> None:
        self.appearance = appearance

        display_font = QFont(appearance.font_family, appearance.time_font_size, QFont.Weight.Bold)
        display_font.setStyleHint(QFont.StyleHint.SansSerif)
        self._display_label.setFont(display_font)
        self._display_label.setStyleSheet(f"color: {appearance.accent_color};")

    def primary_action(self) -> None:
        if self.timer.is_finished:
            return
        self._on_primary_clicked()

    def reset(self) -> None:
        self._on_reset_clicked()

    def start_or_resume(self) -> None:
        if self.timer.state is TimerState.IDLE:
            self.timer.start()
            self._refresh()
        elif self.timer.state is TimerState.PAUSED:
            self.timer.resume()
            self._refresh()

    def pause(self) -> None:
        if self.timer.state is TimerState.RUNNING:
            self.timer.pause()
            self._refresh()

    def _on_preset_changed(self, index: int) -> None:
        minutes = self._duration_combo.itemData(index)
        is_custom = minutes is None
        self._custom_spinbox.setVisible(is_custom)
        if not is_custom and self.timer.state is TimerState.IDLE:
            self.timer.set_duration(minutes * 60)
            self._refresh()

    def _on_custom_minutes_changed(self, minutes: int) -> None:
        if self.timer.state is TimerState.IDLE:
            self.timer.set_duration(minutes * 60)
            self._refresh()

    def _on_primary_clicked(self) -> None:
        if self.timer.state is TimerState.RUNNING:
            self.timer.pause()
        elif self.timer.state is TimerState.PAUSED:
            self.timer.resume()
        else:
            self.timer.start()
        self._refresh()

    def _on_reset_clicked(self) -> None:
        self.timer.reset()
        self._has_notified_finished = False
        self._refresh()

    def _refresh(self) -> None:
        self._display_label.setText(format_duration(self.timer.remaining()))

        if self.timer.is_finished:
            self._primary_button.setText("Done")
            self._primary_button.setEnabled(False)
            if not self._has_notified_finished:
                self._has_notified_finished = True
                self._notifier.notify("Tiko", "Timer finished")
        elif self.timer.state is TimerState.RUNNING:
            self._primary_button.setText("Pause")
            self._primary_button.setEnabled(True)
        elif self.timer.state is TimerState.PAUSED:
            self._primary_button.setText("Resume")
            self._primary_button.setEnabled(True)
        else:
            self._primary_button.setText("Start")
            self._primary_button.setEnabled(True)

        is_idle = self.timer.state is TimerState.IDLE
        self._duration_combo.setEnabled(is_idle)
        self._custom_spinbox.setEnabled(is_idle)