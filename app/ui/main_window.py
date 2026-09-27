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

from app.core.appearance import Appearance
from app.core.clock import Clock, ClockFormat
from app.core.settings import Settings
from app.ui.clock_view import ClockView
from app.ui.notifications import Notifier
from app.ui.settings_view import SettingsView
from app.ui.stopwatch_view import StopwatchView
from app.ui.timer_view import TimerView

_SETTINGS_INDEX = 3


def _mode_button_stylesheet(appearance: Appearance) -> str:
    return (
        "QPushButton {"
        f" color: {appearance.secondary_text_color}; background: transparent; border: none;"
        " padding: 4px 10px; font-size: 13px;"
        "}"
        f"QPushButton:checked {{ color: {appearance.accent_color}; font-weight: 600; }}"
    )


class MainWindow(QMainWindow):
    def __init__(self, settings: Settings | None = None):
        super().__init__()
        self.setWindowTitle("Tiko")
        self.resize(800, 480)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._settings = settings or Settings()

        clock_format = self._settings.load_clock_format()
        self.appearance = self._settings.load_appearance()
        always_on_top = self._settings.load_always_on_top()

        self._notifier = Notifier(self)

        self._clock_view = ClockView(clock=Clock(clock_format), appearance=self.appearance)
        self._timer_view = TimerView(appearance=self.appearance, notifier=self._notifier)
        self._stopwatch_view = StopwatchView(appearance=self.appearance)
        self._settings_view = SettingsView(clock_format, self.appearance, always_on_top)
        self._settings_view.clock_format_changed.connect(self._on_clock_format_changed)
        self._settings_view.appearance_changed.connect(self._on_appearance_changed)
        self._settings_view.always_on_top_changed.connect(self._on_always_on_top_changed)

        self._stack = QStackedWidget()
        self._stack.addWidget(self._clock_view)
        self._stack.addWidget(self._timer_view)
        self._stack.addWidget(self._stopwatch_view)
        self._stack.addWidget(self._settings_view)

        self._mode_buttons: list[QPushButton] = []
        mode_row = QHBoxLayout()
        mode_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mode_row.setSpacing(24)
        for index, label in enumerate(("Clock", "Timer", "Stopwatch")):
            button = QPushButton(label)
            button.setFlat(True)
            button.setCheckable(True)
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.clicked.connect(lambda _checked, i=index: self._switch_mode(i))
            mode_row.addWidget(button)
            self._mode_buttons.append(button)

        top_row = QHBoxLayout()
        top_row.addStretch(1)
        self._settings_button = QPushButton("\u2699")
        self._settings_button.setFlat(True)
        self._settings_button.setCheckable(True)
        self._settings_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._settings_button.clicked.connect(lambda: self._switch_mode(_SETTINGS_INDEX))
        top_row.addWidget(self._settings_button)

        central = QWidget()
        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(0, 8, 12, 16)
        central_layout.addLayout(top_row)
        central_layout.addWidget(self._stack, 1)
        central_layout.addLayout(mode_row)

        self.setCentralWidget(central)
        self.apply_appearance(self.appearance)

        self._last_content_mode = 0
        last_mode = self._settings.load_last_mode()
        self._switch_mode(last_mode if last_mode in (0, 1, 2) else 0)

        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, always_on_top)

        geometry = self._settings.load_geometry()
        if geometry:
            self.restoreGeometry(geometry)

        self._fullscreen_shortcut = QShortcut(QKeySequence("F"), self)
        self._fullscreen_shortcut.activated.connect(self._toggle_fullscreen)

        self._exit_fullscreen_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        self._exit_fullscreen_shortcut.activated.connect(self._exit_fullscreen)

        self._clock_shortcut = QShortcut(QKeySequence("C"), self)
        self._clock_shortcut.activated.connect(lambda: self._switch_mode_via_shortcut(0))

        self._timer_shortcut = QShortcut(QKeySequence("T"), self)
        self._timer_shortcut.activated.connect(lambda: self._switch_mode_via_shortcut(1))

        self._stopwatch_shortcut = QShortcut(QKeySequence("S"), self)
        self._stopwatch_shortcut.activated.connect(lambda: self._switch_mode_via_shortcut(2))

        self._space_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Space), self)
        self._space_shortcut.activated.connect(self._handle_space)

        self._reset_shortcut = QShortcut(QKeySequence("R"), self)
        self._reset_shortcut.activated.connect(self._handle_reset)

    def apply_appearance(self, appearance: Appearance) -> None:
        self.appearance = appearance
        self.setStyleSheet(f"background-color: {appearance.background_color};")

        for button in (*self._mode_buttons, self._settings_button):
            button.setStyleSheet(_mode_button_stylesheet(appearance))

        self._clock_view.apply_appearance(appearance)
        self._timer_view.apply_appearance(appearance)
        self._stopwatch_view.apply_appearance(appearance)

    def _switch_mode(self, index: int) -> None:
        self._stack.setCurrentIndex(index)
        for i, button in enumerate(self._mode_buttons):
            button.setChecked(i == index)
        self._settings_button.setChecked(index == _SETTINGS_INDEX)
        if index != _SETTINGS_INDEX:
            self._last_content_mode = index

    def _switch_mode_via_shortcut(self, index: int) -> None:
        if self._stack.currentIndex() == _SETTINGS_INDEX:
            return
        self._switch_mode(index)

    def _on_clock_format_changed(self, fmt: ClockFormat) -> None:
        self._clock_view.apply_clock_format(fmt)
        self._settings.save_clock_format(fmt)

    def _on_appearance_changed(self, appearance: Appearance) -> None:
        self.apply_appearance(appearance)
        self._settings.save_appearance(appearance)

    def _on_always_on_top_changed(self, value: bool) -> None:
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, value)
        self.show()
        self._settings.save_always_on_top(value)

    def _handle_space(self) -> None:
        index = self._stack.currentIndex()
        if index == 1:
            self._timer_view.primary_action()
        elif index == 2:
            self._stopwatch_view.primary_action()

    def _handle_reset(self) -> None:
        index = self._stack.currentIndex()
        if index == 1:
            self._timer_view.reset()
        elif index == 2:
            self._stopwatch_view.reset()

    def _toggle_fullscreen(self) -> None:
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def _exit_fullscreen(self) -> None:
        if self.isFullScreen():
            self.showNormal()
            return
        if self._stack.currentIndex() == _SETTINGS_INDEX:
            self._switch_mode(self._last_content_mode)

    def closeEvent(self, event) -> None:
        self._settings.save_geometry(self.saveGeometry())
        current_index = self._stack.currentIndex()
        if current_index in (0, 1, 2):
            self._settings.save_last_mode(current_index)
        super().closeEvent(event)