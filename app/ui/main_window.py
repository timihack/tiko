from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.core.appearance import DARK, Appearance
from app.ui.clock_view import ClockView
from app.ui.stopwatch_view import StopwatchView
from app.ui.timer_view import TimerView


def _mode_button_stylesheet(appearance: Appearance) -> str:
    return (
        "QPushButton {"
        f" color: {appearance.secondary_text_color}; background: transparent; border: none;"
        " padding: 4px 10px; font-size: 13px;"
        "}"
        f"QPushButton:checked {{ color: {appearance.accent_color}; font-weight: 600; }}"
    )


class MainWindow(QMainWindow):
    def __init__(self, appearance: Appearance | None = None):
        super().__init__()
        self.setWindowTitle("Tiko")
        self.resize(800, 480)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.appearance = appearance or DARK

        self._clock_view = ClockView(appearance=self.appearance)
        self._timer_view = TimerView(appearance=self.appearance)
        self._stopwatch_view = StopwatchView(appearance=self.appearance)

        self._stack = QStackedWidget()
        self._stack.addWidget(self._clock_view)
        self._stack.addWidget(self._timer_view)
        self._stack.addWidget(self._stopwatch_view)

        self._mode_buttons: list[QPushButton] = []
        mode_row = QHBoxLayout()
        mode_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mode_row.setSpacing(24)
        for index, label in enumerate(("Clock", "Timer", "Stopwatch")):
            button = QPushButton(label)
            button.setFlat(True)
            button.setCheckable(True)
            button.clicked.connect(lambda _checked, i=index: self._switch_mode(i))
            mode_row.addWidget(button)
            self._mode_buttons.append(button)

        central = QWidget()
        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(0, 0, 0, 16)
        central_layout.addWidget(self._stack, 1)
        central_layout.addLayout(mode_row)

        self.setCentralWidget(central)
        self.apply_appearance(self.appearance)
        self._switch_mode(0)

        self._fullscreen_shortcut = QShortcut(QKeySequence("F"), self)
        self._fullscreen_shortcut.activated.connect(self._toggle_fullscreen)

        self._exit_fullscreen_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        self._exit_fullscreen_shortcut.activated.connect(self._exit_fullscreen)

    def apply_appearance(self, appearance: Appearance) -> None:
        self.appearance = appearance
        self.setStyleSheet(f"background-color: {appearance.background_color};")

        for button in self._mode_buttons:
            button.setStyleSheet(_mode_button_stylesheet(appearance))

        self._clock_view.apply_appearance(appearance)
        self._timer_view.apply_appearance(appearance)
        self._stopwatch_view.apply_appearance(appearance)

    def _switch_mode(self, index: int) -> None:
        self._stack.setCurrentIndex(index)
        for i, button in enumerate(self._mode_buttons):
            button.setChecked(i == index)

    def _toggle_fullscreen(self) -> None:
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def _exit_fullscreen(self) -> None:
        if self.isFullScreen():
            self.showNormal()