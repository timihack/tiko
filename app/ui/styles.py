from PySide6.QtGui import QColor, QPalette

from app.core.appearance import Appearance


def build_stylesheet(appearance: Appearance) -> str:
    a = appearance
    return f"""
QMainWindow {{ background-color: {a.background_color}; }}
QWidget {{ color: {a.text_color}; }}
QLabel {{ background: transparent; }}
QCheckBox {{ spacing: 8px; }}
QComboBox, QSpinBox {{
    background-color: {a.surface_color};
    color: {a.text_color};
    border: 1px solid {a.border_color};
    border-radius: 6px;
    padding: 4px 10px;
    min-height: 22px;
}}
QComboBox:disabled, QSpinBox:disabled {{ color: {a.secondary_text_color}; }}
QScrollArea {{ background: transparent; border: none; }}
QScrollArea > QWidget > QWidget {{ background: transparent; }}
QScrollBar:vertical {{ background: transparent; width: 10px; margin: 0; }}
QScrollBar::handle:vertical {{
    background: {a.border_color};
    border-radius: 5px;
    min-height: 24px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: transparent; }}
QPushButton#controlButton {{
    background-color: {a.surface_color};
    color: {a.text_color};
    border: 1px solid {a.border_color};
    border-radius: 6px;
    padding: 8px 22px;
    min-width: 64px;
}}
QPushButton#controlButton:hover {{ border-color: {a.secondary_text_color}; }}
QPushButton#controlButton:disabled {{ color: {a.secondary_text_color}; }}
"""


def build_palette(appearance: Appearance) -> QPalette:
    a = appearance
    palette = QPalette()
    active_roles = {
        QPalette.ColorRole.Window: a.background_color,
        QPalette.ColorRole.WindowText: a.text_color,
        QPalette.ColorRole.Base: a.surface_color,
        QPalette.ColorRole.AlternateBase: a.surface_color,
        QPalette.ColorRole.Text: a.text_color,
        QPalette.ColorRole.Button: a.surface_color,
        QPalette.ColorRole.ButtonText: a.text_color,
        QPalette.ColorRole.BrightText: a.text_color,
        QPalette.ColorRole.Highlight: a.border_color,
        QPalette.ColorRole.HighlightedText: a.text_color,
        QPalette.ColorRole.PlaceholderText: a.secondary_text_color,
        QPalette.ColorRole.ToolTipBase: a.surface_color,
        QPalette.ColorRole.ToolTipText: a.text_color,
    }
    for role, color in active_roles.items():
        palette.setColor(role, QColor(color))
    for role in (
        QPalette.ColorRole.WindowText,
        QPalette.ColorRole.Text,
        QPalette.ColorRole.ButtonText,
    ):
        palette.setColor(QPalette.ColorGroup.Disabled, role, QColor(a.secondary_text_color))
    return palette