"""
LinguaGPT application entry point
"""

import sys

from PyQt6.QtWidgets import QApplication

from app.main_window import GPTTranslator
from app.utils import get_dark_palette


def main():
    """Main application entry function"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Set dark palette
    app.setPalette(get_dark_palette())

    translator = GPTTranslator()
    translator.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
