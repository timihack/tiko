import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

from app.core.settings import APPLICATION, ORGANIZATION
from app.ui.main_window import MainWindow


def main():
    QCoreApplication.setOrganizationName(ORGANIZATION)
    QCoreApplication.setApplicationName(APPLICATION)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()