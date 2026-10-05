from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QIcon, QPainter, QPixmap

BACKGROUND_COLOR = "#0F766E"
FOREGROUND_COLOR = "#FFFFFF"


def render_icon_pixmap(size: int = 256) -> QPixmap:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor(BACKGROUND_COLOR))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(0, 0, size, size)

    painter.setPen(QColor(FOREGROUND_COLOR))
    font = QFont("Inter", int(size * 0.44), QFont.Weight.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "T")
    painter.end()

    return pixmap


def generate_icon(size: int = 64) -> QIcon:
    return QIcon(render_icon_pixmap(size))