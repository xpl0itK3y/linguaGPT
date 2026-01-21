"""
Application settings dialog module
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
)

from .config import Config
from .translations import get_translation


class SettingsDialog(QDialog):
    """Settings dialog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.config = Config()
        self.setWindowTitle("" + parent.t("settings"))
        self.setFixedSize(500, 650)
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # API Key
        self.api_label = QLabel(self.parent_window.t("api_key_label"))
        self.api_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(self.api_label)

        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setPlaceholderText(
            self.parent_window.t("api_key_placeholder")
        )
        self.api_key_input.setFont(QFont("Segoe UI", 10))
        self.api_key_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #3a3a5c;
                border-radius: 8px;
                background: #2a2a4a;
                color: white;
            }
            QLineEdit:focus {
                border: 2px solid #e94560;
            }
        """)
        layout.addWidget(self.api_key_input)

        # UI Language selection
        self.ui_lang_label = QLabel(self.parent_window.t("ui_language_label"))
        self.ui_lang_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(self.ui_lang_label)

        self.ui_lang_combo = QComboBox()
        self.ui_lang_combo.addItem("English", "en")
        self.ui_lang_combo.addItem("Русский", "ru")
        self.ui_lang_combo.setFont(QFont("Segoe UI", 10))
        self.ui_lang_combo.setStyleSheet("""
            QComboBox {
                background: #2a2a4a;
                color: white;
                border: 2px solid #3a3a5c;
                border-radius: 8px;
                padding: 8px;
            }
            QComboBox:hover {
                border: 2px solid #e94560;
            }
            QComboBox QAbstractItemView {
                background: #2a2a4a;
                color: white;
                selection-background-color: #e94560;
            }
        """)
        self.ui_lang_combo.currentIndexChanged.connect(self.on_language_changed)
        layout.addWidget(self.ui_lang_combo)

        # Model selection
        self.model_label = QLabel(self.parent_window.t("select_model"))
        self.model_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(self.model_label)

        self.model_group = QButtonGroup()

        # Save references to radio buttons for text updates
        self.model_buttons = []

        models = [
            ("GPT-4o (Лучшее качество)", "gpt-4o"),
            ("GPT-4o Mini (Рекомендуется)", "gpt-4o-mini"),
            ("GPT-4 Turbo", "gpt-4-turbo"),
            ("GPT-3.5 Turbo (Экономный)", "gpt-3.5-turbo"),
        ]

        for text, value in models:
            rb = QRadioButton()
            rb.setFont(QFont("Segoe UI", 10))
            rb.setStyleSheet("QRadioButton { color: white; spacing: 8px; }")
            rb.setProperty("model_value", value)
            self.model_group.addButton(rb)
            self.model_buttons.append(rb)
            layout.addWidget(rb)

        # Set model texts
        self.update_model_texts()

        layout.addStretch()

        # Delete key button
        self.delete_key_btn = QPushButton(self.parent_window.t("delete_key"))
        self.delete_key_btn.setFont(QFont("Segoe UI", 9))
        self.delete_key_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_key_btn.setStyleSheet("""
            QPushButton {
                background: #6a2a3a;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #8a3a4a;
            }
        """)
        self.delete_key_btn.clicked.connect(self.delete_api_key)
        layout.addWidget(self.delete_key_btn)

        # Buttons
        btn_layout = QHBoxLayout()

        self.save_btn = QPushButton(self.parent_window.t("save"))
        self.save_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background: #e94560;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #d63850;
            }
        """)
        self.save_btn.clicked.connect(self.save_settings)

        self.cancel_btn = QPushButton(self.parent_window.t("cancel"))
        self.cancel_btn.setFont(QFont("Segoe UI", 11))
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background: #3a3a5c;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #4a4a6c;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_settings(self):
        """Load settings"""
        self.config.load()
        self.api_key_input.setText(self.config.api_key)
        model = self.config.model
        ui_lang = self.config.ui_language

        # Set interface language
        index = self.ui_lang_combo.findData(ui_lang)
        if index >= 0:
            self.ui_lang_combo.setCurrentIndex(index)

        for btn in self.model_group.buttons():
            if btn.property("model_value") == model:
                btn.setChecked(True)
                break

    def on_language_changed(self):
        """Handle language change"""
        new_lang = self.ui_lang_combo.currentData()
        if new_lang and new_lang != self.parent_window.ui_language:
            # Temporarily save new language
            self.parent_window.ui_language = new_lang
            # Update main window interface
            self.parent_window.update_ui_language()
            # Update settings dialog text
            self.update_dialog_language()

    def update_dialog_language(self):
        """Update settings dialog language"""
        self.setWindowTitle("" + self.parent_window.t("settings"))
        self.api_label.setText(self.parent_window.t("api_key_label"))
        self.api_key_input.setPlaceholderText(
            self.parent_window.t("api_key_placeholder")
        )
        self.ui_lang_label.setText(self.parent_window.t("ui_language_label"))
        self.model_label.setText(self.parent_window.t("select_model"))
        self.delete_key_btn.setText(self.parent_window.t("delete_key"))
        self.save_btn.setText(self.parent_window.t("save"))
        self.cancel_btn.setText(self.parent_window.t("cancel"))
        self.update_model_texts()

    def update_model_texts(self):
        """Update model texts"""
        lang = self.parent_window.ui_language

        if lang == "ru":
            model_texts = [
                "GPT-4o (Лучшее качество)",
                "GPT-4o Mini (Рекомендуется)",
                "GPT-4 Turbo",
                "GPT-3.5 Turbo (Экономный)",
            ]
        else:  # en
            model_texts = [
                "GPT-4o (Best Quality)",
                "GPT-4o Mini (Recommended)",
                "GPT-4 Turbo",
                "GPT-3.5 Turbo (Economical)",
            ]

        for i, btn in enumerate(self.model_buttons):
            btn.setText(model_texts[i])

    def save_settings(self):
        """Save settings"""
        api_key = self.api_key_input.text().strip()
        if not api_key:
            QMessageBox.warning(
                self,
                self.parent_window.t("error"),
                self.parent_window.t("error_enter_key"),
            )
            return

        model = None
        for btn in self.model_group.buttons():
            if btn.isChecked():
                model = btn.property("model_value")
                break

        if not model:
            QMessageBox.warning(
                self,
                self.parent_window.t("error"),
                self.parent_window.t("error_select_model"),
            )
            return

        ui_language = self.ui_lang_combo.currentData()

        self.config.save(api_key=api_key, model=model, ui_language=ui_language)

        QMessageBox.information(
            self,
            self.parent_window.t("success"),
            self.parent_window.t("settings_saved"),
        )
        self.accept()

    def delete_api_key(self):
        """Delete API key"""
        reply = QMessageBox.question(
            self,
            self.parent_window.t("confirm"),
            self.parent_window.t("delete_confirm"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.config.delete()

            self.api_key_input.clear()

            # Clear model selection
            for btn in self.model_group.buttons():
                btn.setAutoExclusive(False)
                btn.setChecked(False)
                btn.setAutoExclusive(True)

            QMessageBox.information(
                self, self.parent_window.t("done"), self.parent_window.t("deleted")
            )
            self.reject()
