from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from app.ui.clock_view import ClockView

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Tiko")
    self.resize(800, 480)
    self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
    self.setStyleSheet("background-color: #121212;")
    self.setCentralWidget(ClockView())
