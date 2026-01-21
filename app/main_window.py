"""
Main application window module
"""

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QFont,
    QIcon,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPalette,
    QPen,
    QPixmap,
)
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSystemTrayIcon,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .config import Config
from .settings_dialog import SettingsDialog
from .translate_thread import TranslateThread
from .translations import get_translation
from .utils import get_app_stylesheet


class GPTTranslator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.load_config()
        self.init_ui()
        self.apply_styles()
        self.setup_tray_icon()

    def load_config(self):
        """Load configuration"""
        self.config.load()
        self.api_key = self.config.api_key
        self.model = self.config.model
        self.ui_language = self.config.ui_language

    def t(self, key):
        """Get translation string"""
        return get_translation(self.ui_language, key)

    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle(self.t("title"))
        self.setGeometry(100, 100, 1100, 750)
        self.setMinimumSize(800, 600)

        # Central widget with scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #1a1a2e;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #3a3a5c;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #e94560;
            }
        """)

        central_widget = QWidget()
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Set minimum width for content
        central_widget.setMinimumWidth(750)

        # Header
        header_layout = QHBoxLayout()

        self.title_label = QLabel(self.t("title"))
        self.title_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header_layout.addWidget(self.title_label)

        header_layout.addStretch()

        self.settings_btn = QPushButton(self.t("settings"))
        self.settings_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_btn.clicked.connect(self.open_settings)
        header_layout.addWidget(self.settings_btn)

        main_layout.addLayout(header_layout)

        # Divider line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background: #3a3a5c;")
        main_layout.addWidget(line)

        # Language selection panel
        lang_layout = QHBoxLayout()
        lang_layout.setSpacing(20)

        # Source language (left)
        source_container = QVBoxLayout()
        self.source_label = QLabel(self.t("source_lang"))
        self.source_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        source_container.addWidget(self.source_label)

        self.source_lang = QComboBox()
        self.source_lang.addItems(
            [
                "Auto",
                "English",
                "Russian",
                "Español",
                "Français",
                "Deutsch",
                "中文",
                "日本語",
                "한국어",
                "Қазақша",
            ]
        )
        self.source_lang.setFont(QFont("Segoe UI", 10))
        source_container.addWidget(self.source_lang)

        lang_layout.addLayout(source_container, 1)

        # Swap button (center)
        self.swap_btn = QPushButton(self.t("swap"))
        self.swap_btn.setFont(QFont("Segoe UI", 10))
        self.swap_btn.setFixedHeight(40)
        self.swap_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.swap_btn.setStyleSheet("""
            QPushButton {
                background: #3a3a5c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #4a4a6c;
            }
        """)
        self.swap_btn.clicked.connect(self.swap_languages)
        lang_layout.addWidget(self.swap_btn, 0, Qt.AlignmentFlag.AlignBottom)

        # Target language (right)
        target_container = QVBoxLayout()
        self.target_label = QLabel(self.t("target_lang"))
        self.target_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        target_container.addWidget(self.target_label)

        self.target_lang = QComboBox()
        self.target_lang.addItems(
            [
                "Russian",
                "English",
                "Español",
                "Français",
                "Deutsch",
                "中文",
                "日本語",
                "한국어",
                "Қазақша",
            ]
        )
        self.target_lang.setFont(QFont("Segoe UI", 10))
        target_container.addWidget(self.target_lang)

        lang_layout.addLayout(target_container, 1)

        main_layout.addLayout(lang_layout)

        # Text fields
        text_layout = QHBoxLayout()
        text_layout.setSpacing(20)

        # Source text
        source_text_container = QVBoxLayout()
        self.input_label = QLabel(self.t("input_text"))
        self.input_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        source_text_container.addWidget(self.input_label)

        self.source_text = QTextEdit()
        self.source_text.setFont(QFont("Segoe UI", 12))
        self.source_text.setPlaceholderText(self.t("input_placeholder"))
        self.source_text.setMinimumHeight(200)
        source_text_container.addWidget(self.source_text, 1)

        text_layout.addLayout(source_text_container, 1)

        # Translated text
        target_text_container = QVBoxLayout()

        self.translation_label = QLabel(self.t("translation"))
        self.translation_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        target_text_container.addWidget(self.translation_label)

        self.target_text = QTextEdit()
        self.target_text.setFont(QFont("Segoe UI", 12))
        self.target_text.setReadOnly(True)
        self.target_text.setPlaceholderText(self.t("translation_placeholder"))
        self.target_text.setMinimumHeight(200)
        target_text_container.addWidget(self.target_text, 1)

        # Loading indicator
        self.loading_label = QLabel(self.t("translating") + "...")
        self.loading_label.setFont(QFont("Segoe UI", 11))
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet("""
            QLabel {
                color: #e94560;
                background: #2a2a4a;
                padding: 10px;
                border-radius: 8px;
                margin: 5px;
            }
        """)
        self.loading_label.hide()
        target_text_container.addWidget(self.loading_label)

        # Copy button at bottom
        self.copy_btn = QPushButton(self.t("copy"))
        self.copy_btn.setFont(QFont("Segoe UI", 10))
        self.copy_btn.setFixedHeight(40)
        self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background: #3a3a5c;
                color: white;
                border: none;
                padding: 10px 25px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #4a4a6c;
            }
        """)
        self.copy_btn.clicked.connect(self.copy_translation)
        target_text_container.addWidget(self.copy_btn)

        text_layout.addLayout(target_text_container, 1)

        main_layout.addLayout(text_layout, 1)

        # Alternative translations panel
        alternatives_frame = QFrame()
        alternatives_frame.setStyleSheet("""
            QFrame {
                background: #2a2a4a;
                border: 2px solid #3a3a5c;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        alternatives_layout = QVBoxLayout()

        self.alt_header = QLabel(self.t("alternatives"))
        self.alt_header.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        alternatives_layout.addWidget(self.alt_header)

        self.alternatives_container = QVBoxLayout()
        alternatives_layout.addLayout(self.alternatives_container)

        alternatives_frame.setLayout(alternatives_layout)
        alternatives_frame.hide()
        self.alternatives_frame = alternatives_frame

        main_layout.addWidget(alternatives_frame)

        # Translate button
        self.translate_btn = QPushButton(self.t("translate"))
        self.translate_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.translate_btn.setFixedHeight(55)
        self.translate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.translate_btn.clicked.connect(self.translate)
        main_layout.addWidget(self.translate_btn)

        # Status bar
        self.status_label = QLabel(self.t("ready"))
        self.status_label.setFont(QFont("Segoe UI", 10))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

        central_widget.setLayout(main_layout)

    def setup_tray_icon(self):
        """Setup system tray icon"""
        self.tray_icon = QSystemTrayIcon(self)

        # Create high-resolution icon
        size = 256
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        # Gradient circular background with shadow
        gradient = QLinearGradient(0, 0, size, size)
        gradient.setColorAt(0, QColor("#e94560"))
        gradient.setColorAt(0.5, QColor("#a83f5a"))
        gradient.setColorAt(1, QColor("#0f3460"))

        # Shadow
        painter.setBrush(QBrush(QColor(0, 0, 0, 40)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(12, 12, size - 20, size - 20)

        # Main circle
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(8, 8, size - 16, size - 16)

        # Inner light highlight
        inner_gradient = QLinearGradient(size * 0.3, size * 0.2, size * 0.7, size * 0.5)
        inner_gradient.setColorAt(0, QColor(255, 255, 255, 30))
        inner_gradient.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(inner_gradient))
        painter.drawEllipse(
            int(size * 0.15), int(size * 0.1), int(size * 0.6), int(size * 0.4)
        )

        # Letter "A" (left) with shadow
        font = QFont("Arial", int(size * 0.32), QFont.Weight.Bold)
        painter.setFont(font)

        # Shadow for "A"
        painter.setPen(QColor(0, 0, 0, 80))
        painter.drawText(int(size * 0.18), int(size * 0.62), "A")

        # Letter "A"
        painter.setPen(QColor("white"))
        painter.drawText(int(size * 0.17), int(size * 0.61), "A")

        # Shadow for "Я"
        painter.setPen(QColor(0, 0, 0, 80))
        painter.drawText(int(size * 0.67), int(size * 0.62), "Я")

        # Letter "Я" (right)
        painter.setPen(QColor("white"))
        painter.drawText(int(size * 0.66), int(size * 0.61), "Я")

        # Translation arrows
        pen = QPen(QColor("#4CC9F0"), int(size * 0.03))
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)

        # Arrow down-right
        arrow_path1 = QPainterPath()
        arrow_path1.moveTo(size * 0.52, size * 0.42)
        arrow_path1.lineTo(size * 0.62, size * 0.48)
        arrow_path1.lineTo(size * 0.52, size * 0.54)
        painter.drawPath(arrow_path1)

        # Arrow up-left
        arrow_path2 = QPainterPath()
        arrow_path2.moveTo(size * 0.48, size * 0.28)
        arrow_path2.lineTo(size * 0.38, size * 0.22)
        arrow_path2.lineTo(size * 0.48, size * 0.16)
        painter.drawPath(arrow_path2)

        # AI sparks
        painter.setPen(Qt.PenStyle.NoPen)

        spark_gradient = QLinearGradient(0, 0, size * 0.1, size * 0.1)
        spark_gradient.setColorAt(0, QColor("#FFD60A"))
        spark_gradient.setColorAt(1, QColor("#FFA500"))
        painter.setBrush(QBrush(spark_gradient))

        painter.drawEllipse(
            int(size * 0.18), int(size * 0.18), int(size * 0.06), int(size * 0.06)
        )
        painter.drawEllipse(
            int(size * 0.76), int(size * 0.18), int(size * 0.06), int(size * 0.06)
        )
        painter.drawEllipse(
            int(size * 0.46), int(size * 0.10), int(size * 0.05), int(size * 0.05)
        )

        # AI neural network
        painter.setBrush(QColor("#4CC9F0"))
        painter.setOpacity(0.8)

        node_size = int(size * 0.04)
        node1_x, node1_y = int(size * 0.28), int(size * 0.80)
        node2_x, node2_y = int(size * 0.48), int(size * 0.83)
        node3_x, node3_y = int(size * 0.68), int(size * 0.80)

        # Lines between nodes
        pen = QPen(QColor("#4CC9F0"), int(size * 0.01))
        painter.setPen(pen)
        painter.setOpacity(0.5)
        painter.drawLine(
            node1_x + node_size // 2,
            node1_y + node_size // 2,
            node2_x + node_size // 2,
            node2_y + node_size // 2,
        )
        painter.drawLine(
            node2_x + node_size // 2,
            node2_y + node_size // 2,
            node3_x + node_size // 2,
            node3_y + node_size // 2,
        )

        # Nodes
        painter.setOpacity(0.9)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(node1_x, node1_y, node_size, node_size)
        painter.drawEllipse(node2_x, node2_y, node_size, node_size)
        painter.drawEllipse(node3_x, node3_y, node_size, node_size)

        painter.end()

        # Scale to required sizes
        icon = QIcon(pixmap)
        icon.addPixmap(
            pixmap.scaled(
                64,
                64,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        icon.addPixmap(
            pixmap.scaled(
                32,
                32,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        icon.addPixmap(
            pixmap.scaled(
                128,
                128,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

        self.tray_icon.setIcon(icon)
        self.setWindowIcon(icon)

        # Create tray menu
        self.tray_menu = QMenu()

        self.show_action = QAction(self.t("show"), self)
        self.show_action.triggered.connect(self.show_window)
        self.tray_menu.addAction(self.show_action)

        self.quit_action = QAction(self.t("quit"), self)
        self.quit_action.triggered.connect(self.quit_application)
        self.tray_menu.addAction(self.quit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.setToolTip(self.t("tray_tooltip"))

        self.tray_icon.activated.connect(self.tray_icon_activated)

        self.tray_icon.show()

    def tray_icon_activated(self, reason):
        """Handle tray icon click"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window()

    def show_window(self):
        """Show window"""
        self.show()
        self.activateWindow()
        self.raise_()

    def quit_application(self):
        """Quit application completely"""
        self.tray_icon.hide()
        QApplication.quit()

    def closeEvent(self, event):
        """Handle window close event"""
        event.ignore()
        self.hide()
        if not hasattr(self, "_tray_notification_shown"):
            if self.ui_language == "ru":
                self.tray_icon.showMessage(
                    QSystemTrayIcon.MessageIcon.Information,
                    2000,
                )
            else:
                self.tray_icon.showMessage(
                    "GPT Translator",
                    "Application minimized to tray. Use tray menu to quit.",
                    QSystemTrayIcon.MessageIcon.Information,
                    2000,
                )
            self._tray_notification_shown = True

    def apply_styles(self):
        """Apply application styles"""
        self.setStyleSheet(get_app_stylesheet())

    def open_settings(self):
        """Open settings window"""
        dialog = SettingsDialog(self)
        if dialog.exec():
            old_lang = self.ui_language
            self.load_config()
            if old_lang != self.ui_language:
                self.update_ui_language()
        else:
            old_lang = self.ui_language
            self.load_config()
            if old_lang != self.ui_language:
                self.update_ui_language()

    def update_ui_language(self):
        """Update interface language"""
        self.setWindowTitle(self.t("title"))
        self.title_label.setText(self.t("title"))
        self.settings_btn.setText(self.t("settings"))
        self.source_label.setText(self.t("source_lang"))
        self.target_label.setText(self.t("target_lang"))
        self.swap_btn.setText(self.t("swap"))
        self.input_label.setText(self.t("input_text"))
        self.source_text.setPlaceholderText(self.t("input_placeholder"))
        self.translation_label.setText(self.t("translation"))
        self.target_text.setPlaceholderText(self.t("translation_placeholder"))
        self.copy_btn.setText(self.t("copy"))
        self.translate_btn.setText(self.t("translate"))
        self.status_label.setText(self.t("ready"))
        self.alt_header.setText(self.t("alternatives"))

        self.show_action.setText(self.t("show"))
        self.quit_action.setText(self.t("quit"))
        self.tray_icon.setToolTip(self.t("tray_tooltip"))

    def swap_languages(self):
        """Swap languages"""
        if self.source_lang.currentIndex() != 0:
            source_text = self.source_lang.currentText()
            target_text = self.target_lang.currentText()

            self.source_lang.setCurrentText(target_text)
            self.target_lang.setCurrentText(source_text)

            source_content = self.source_text.toPlainText()
            target_content = self.target_text.toPlainText()

            if target_content.strip():
                self.source_text.setPlainText(target_content)
                self.target_text.setPlainText(source_content)

                self.alternatives_frame.hide()
                self.clear_alternatives()

                self.status_label.setText(self.t("swapped"))

    def copy_translation(self):
        """Copy translation"""
        text = self.target_text.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.status_label.setText(self.t("copied"))
            QTimer.singleShot(2000, lambda: self.status_label.setText(self.t("ready")))

    def translate(self):
        """Translate text"""
        if not self.api_key:
            QMessageBox.warning(self, self.t("error"), self.t("error_no_key"))
            return

        text = self.source_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, self.t("error"), self.t("error_no_text"))
            return

        source = self.source_lang.currentText()
        target = self.target_lang.currentText()

        if source == "Auto":
            prompt = f"Translate the following text into the language '{target}'. Return only the translation without additional comments:\n\n{text}"
        else:
            prompt = f"Translate the following text from the language '{source}' to the language '{target}'. Return only the translation without additional comments:\n\n{text}"

        self.alternatives_frame.hide()
        self.clear_alternatives()

        self.loading_label.show()
        self.status_label.setText(self.t("translating") + "...")
        self.target_text.clear()
        self.target_text.setPlaceholderText(self.t("translating") + "...")

        self.dot_count = 0
        self.loading_timer = QTimer()
        self.loading_timer.timeout.connect(self.update_loading_animation)
        self.loading_timer.start(500)

        self.thread = TranslateThread(
            self.api_key, self.model, prompt, get_alternatives=True
        )
        self.thread.chunk_received.connect(self.on_chunk_received)
        self.thread.finished.connect(self.on_translation_finished)
        self.thread.alternatives_ready.connect(self.on_alternatives_ready)
        self.thread.error.connect(self.on_translation_error)
        self.thread.start()

    def clear_alternatives(self):
        """Clear alternative translations"""
        while self.alternatives_container.count():
            child = self.alternatives_container.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def on_alternatives_ready(self, alternatives):
        """Handle alternative translations received"""
        self.clear_alternatives()

        for i, alt in enumerate(alternatives, 1):
            alt_widget = QPushButton(f"{i}. {alt}")
            alt_widget.setFont(QFont("Segoe UI", 10))
            alt_widget.setCursor(Qt.CursorShape.PointingHandCursor)
            alt_widget.setStyleSheet("""
                QPushButton {
                    background: #1a1a2e;
                    color: white;
                    border: 2px solid #3a3a5c;
                    border-radius: 8px;
                    padding: 12px;
                    text-align: left;
                }
                QPushButton:hover {
                    background: #3a3a5c;
                    border: 2px solid #e94560;
                }
            """)
            alt_widget.clicked.connect(
                lambda checked, text=alt: self.use_alternative(text)
            )
            self.alternatives_container.addWidget(alt_widget)

        if alternatives:
            self.alternatives_frame.show()

    def use_alternative(self, text):
        """Use alternative translation"""
        self.target_text.setPlainText(text)
        self.status_label.setText(self.t("alternative_selected"))

    def update_loading_animation(self):
        """Update loading animation"""
        dots = "." * (self.dot_count % 4)
        self.loading_label.setText(f"{self.t('translating')}{dots}")
        self.dot_count += 1

    def on_chunk_received(self, chunk):
        """Handle translation chunk received"""
        self.target_text.setPlainText(chunk)
        cursor = self.target_text.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.target_text.setTextCursor(cursor)

    def on_translation_finished(self, translation):
        """Handle translation finished"""
        self.loading_timer.stop()
        self.loading_label.hide()
        self.target_text.setPlaceholderText(self.t("translation_placeholder"))
        self.status_label.setText(self.t("translation_ready"))

    def on_translation_error(self, error):
        """Handle translation error"""
        self.loading_timer.stop()
        self.loading_label.hide()
        self.target_text.setPlaceholderText(self.t("translation_placeholder"))
        QMessageBox.critical(self, self.t("error"), error)
        self.status_label.setText(self.t("error"))
