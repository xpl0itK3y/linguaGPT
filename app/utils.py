"""
Application utilities and styles
"""

from PyQt6.QtGui import QColor, QPalette


def get_app_stylesheet() -> str:
    """Returns application stylesheet"""
    return """
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #1a1a2e, stop:1 #16213e);
        }
        QWidget {
            background: transparent;
            color: white;
        }
        QLabel {
            color: #e94560;
        }
        QComboBox {
            background: #2a2a4a;
            color: white;
            border: 2px solid #3a3a5c;
            border-radius: 8px;
            padding: 8px;
            min-width: 120px;
        }
        QComboBox:hover {
            border: 2px solid #e94560;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox QAbstractItemView {
            background: #2a2a4a;
            color: white;
            selection-background-color: #e94560;
        }
        QTextEdit {
            background: #2a2a4a;
            color: white;
            border: 2px solid #3a3a5c;
            border-radius: 12px;
            padding: 15px;
        }
        QTextEdit:focus {
            border: 2px solid #e94560;
        }
        QPushButton {
            background: #e94560;
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 8px;
        }
        QPushButton:hover {
            background: #d63850;
        }
        QPushButton:pressed {
            background: #c23040;
        }
    """


def get_dark_palette() -> QPalette:
    """Returns dark color palette for the application"""
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(26, 26, 46))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 74))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(58, 58, 92))
    palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Button, QColor(233, 69, 96))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    return palette
