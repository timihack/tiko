from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QWidget

from app.ui.icon import generate_icon


class Notifier(QObject):
    open_requested = Signal()
    start_timer_requested = Signal()
    pause_timer_requested = Signal()
    quit_requested = Signal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._tray_icon: QSystemTrayIcon | None = None
        if QSystemTrayIcon.isSystemTrayAvailable():
            self._tray_icon = QSystemTrayIcon(generate_icon(), parent)
            self._tray_icon.setToolTip("Tiko")
            self._tray_icon.setContextMenu(self._build_menu(parent))
            self._tray_icon.activated.connect(self._on_activated)
            self._tray_icon.show()

    def _build_menu(self, parent: QWidget | None) -> QMenu:
        menu = QMenu(parent)

        open_action = menu.addAction("Open")
        open_action.triggered.connect(lambda: self.open_requested.emit())

        start_action = menu.addAction("Start timer")
        start_action.triggered.connect(lambda: self.start_timer_requested.emit())

        pause_action = menu.addAction("Pause timer")
        pause_action.triggered.connect(lambda: self.pause_timer_requested.emit())

        menu.addSeparator()

        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(lambda: self.quit_requested.emit())

        return menu

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.open_requested.emit()

    def notify(self, title: str, message: str) -> None:
        QApplication.beep()
        if self._tray_icon is not None:
            self._tray_icon.showMessage(
                title, message, QSystemTrayIcon.MessageIcon.Information, 5000
            )