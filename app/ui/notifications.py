from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QWidget


def _generate_icon() -> QIcon:
    size = 64
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor("#0F766E"))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(0, 0, size, size)

    painter.setPen(QColor("#FFFFFF"))
    font = QFont("Inter", 28, QFont.Weight.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "T")
    painter.end()

    return QIcon(pixmap)


class Notifier:
    def __init__(self, parent: QWidget | None = None):
        self._tray_icon: QSystemTrayIcon | None = None
        if QSystemTrayIcon.isSystemTrayAvailable():
            self._tray_icon = QSystemTrayIcon(_generate_icon(), parent)
            self._tray_icon.setToolTip("Tiko")
            self._tray_icon.show()

    def notify(self, title: str, message: str) -> None:
        QApplication.beep()
        if self._tray_icon is not None:
            self._tray_icon.showMessage(
                title, message, QSystemTrayIcon.MessageIcon.Information, 5000
            )