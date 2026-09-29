from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import QLabel, QSizePolicy

_MIN_POINT_SIZE = 12
_HORIZONTAL_MARGIN = 24


class FittedLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self._requested_font = QFont(self.font())

    def set_display_font(self, font: QFont) -> None:
        self._requested_font = QFont(font)
        self._fit()

    def setText(self, text: str) -> None:
        super().setText(text)
        self._fit()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._fit()

    def minimumSizeHint(self) -> QSize:
        return QSize(0, super().minimumSizeHint().height())

    def _fit(self) -> None:
        font = QFont(self._requested_font)
        available = self.width() - 2 * _HORIZONTAL_MARGIN
        if available > 0 and self.text():
            needed = QFontMetrics(font).horizontalAdvance(self.text())
            if needed > available:
                font.setPointSize(max(_MIN_POINT_SIZE, int(font.pointSize() * available / needed)))
        if font != self.font():
            self.setFont(font)