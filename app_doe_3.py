"""
@Project : Word_tools
@File    : app_doe_3
@Author  : lingxiao
@Date    : 2026-03-05 16:42
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""


import sys
from fileinput import filename

import yaml
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QListWidget, QTextEdit, QLabel, QMessageBox,
    QFileDialog, QPushButton
)
from PyQt6.QtCore import Qt
import os

class YAMLFileManager:
    """Manages YAML file operations"""
    def __init__(self):
        self.current_file_path = None
        self.data = {}

    def load_file(self, yaml_path):
        """
        Load YAML file and return data
        :param yaml_path: yaml file path
        :return: Flag, Msg
        """
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                self.data = yaml.safe_load(f)

            self.current_file_path = yaml_path
            return True, None
        except Exception as e:
            return False, str(e)

    def get_word_entries(self):
        """
        Get list of words in the YAML data
        :return: list of words
        """

        # Ternary Operator in Python, if self.data is True then return `list(self.data.keys())`, otherwise return  `[]`
        return list(self.data.keys()) if self.data else []  # tree formular in Python

    def get_word_data(self, word):
        return self.data.get(word, {}) if self.data else {}

    def clear(self):
        self.data = {}
        self.current_file_path = None

    def get_filename_without_extension(self):
        """
        Get file name without extension
        :return:
        """
        if self.current_file_path:
            filename_ext = os.path.basename(self.current_file_path)
            filename_no_ext = os.path.splitext(filename_ext)[0]
            return filename_no_ext
        return None


class UIComponents:
    """Creates and manages UI components"""

    @staticmethod
    def create_open_button():
        """Create styled open file button"""
        button = QPushButton("📂 Open YAML File")
        button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
            """
        )
        return button

    @staticmethod
    def create_file_path_label(txt = "📁 No file loaded"):
        """Create file path display label"""
        label = QLabel(txt)
        label.setStyleSheet(
            """
            QLabel {
                background-color: #f0f0f0;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
                color: #333;
            }
            """
        )
        label.setWordWrap(False)
        return label

    @staticmethod
    def create_title_label():
        """Create title label"""
        label = QLabel("Select a word")
        label.setStyleSheet("font-size: 22px; font-weight: bold;")
        return label

    @staticmethod
    def create_content_view():
        """Create read-only content view"""
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        return text_edit

    @staticmethod
    def create_input_box():
        """Create multi-line input box with fixed height"""
        input_box = QTextEdit()
        input_box.setPlaceholderText("Enter your notes here...")
        input_box.setMaximumHeight(100)
        input_box.setMinimumHeight(100)
        return input_box

    @staticmethod
    def create_word_list():
        """Create word list widget"""
        return QListWidget()


class ContentFormatter:
    """Formats word content for display"""

    @staticmethod
    def format_word_entry(word_data):
        """Format word entry data into HTML"""
        if not word_data:
            return ""

        content = ""

        text = word_data.get("text", "")
        example = word_data.get("example", "")
        vocabulary = word_data.get("vocabulary", [])

        if text:
            content += f"<h3>Meaning</h3><p>{text}</p>"

        if example:
            content += "<h3>Example</h3>"
            if isinstance(example, list):
                for e in example:
                    content += f"<p>{e}</p>"
            else:
                content += f"<p>{example}</p>"

        if vocabulary:
            content += "<h3>Vocabulary</h3>"
            for v in vocabulary:
                content += f"<p>{v}</p>"

        return content


class WordViewer(QWidget):
    """Main Word Viewer Application"""

    def __init__(self, yaml_path=None):
        super().__init__()

        self.file_manager = YAMLFileManager()
        self.ui_components = UIComponents()
        self.formatter = ContentFormatter()

        self._setup_window()
        self._init_ui()

        if yaml_path:
            self.load_yaml_file(yaml_path)

    def _setup_window(self):
        """Setup window properties"""
        self.setWindowTitle("Word Viewer")
        self.resize(1000, 700)

    def _init_ui(self):
        """Initialize user interface"""
        main_layout = QVBoxLayout(self)

        top_bar = self._create_top_bar()
        main_layout.addLayout(top_bar)

        content_layout = self._create_content_area()
        main_layout.addLayout(content_layout, 1)

    def _create_top_bar(self):
        """Create top bar with button and file path"""
        top_bar = QHBoxLayout()

        self.open_button = UIComponents.create_open_button()
        self.open_button.clicked.connect(self.open_file_dialog)
        top_bar.addWidget(self.open_button)

        self.file_path_label = UIComponents.create_file_path_label()
        top_bar.addWidget(self.file_path_label, 1)

        self.total_number_label = UIComponents.create_file_path_label(txt="Word count:")
        top_bar.addWidget(self.total_number_label)

        return top_bar

    def _create_content_area(self):
        """Create main content area"""
        content_layout = QHBoxLayout()

        self.word_list = UIComponents.create_word_list()
        self.word_list.currentTextChanged.connect(self.display_word)

        right_layout = QVBoxLayout()
        self.title_label = UIComponents.create_title_label()
        self.content_view = UIComponents.create_content_view()
        self.input_box = UIComponents.create_input_box()

        right_layout.addWidget(self.title_label)
        right_layout.addWidget(self.content_view)
        right_layout.addWidget(self.input_box)

        content_layout.addWidget(self.word_list, 2)
        content_layout.addLayout(right_layout, 5)

        return content_layout

    def open_file_dialog(self):
        """Open file dialog to select YAML file"""
        yaml_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select YAML File",
            "",
            "YAML Files (*.yaml *.yml);;All Files (*)"
        )

        if yaml_path:
            self.load_yaml_file(yaml_path)

    def load_yaml_file(self, yaml_path):
        """Load YAML file and update UI"""
        success, error = self.file_manager.load_file(yaml_path)

        if success:
            self._update_ui_for_new_file()
            self._update_window_title()
        else:
            self._handle_load_error(error)

    def _update_ui_for_new_file(self):
        """Update UI components after loading new file"""
        self.file_path_label.setText(f"📁 {self.file_manager.current_file_path}")
        self.file_path_label.setToolTip(self.file_manager.current_file_path)

        self.word_list.clear()
        word_entries = self.file_manager.get_word_entries()
        self.word_list.addItems(word_entries)
        self.total_number_label.setText(f"Word count: {len(word_entries)}")

        if word_entries:
            self.word_list.setCurrentRow(0)

    def _update_window_title(self):
        """Update window title with filename"""
        file_name = self.file_manager.get_filename_without_extension()
        if file_name:
            self.setWindowTitle(f"Word Viewer - {file_name}")

    def _handle_load_error(self, error):
        """Handle file loading error"""
        QMessageBox.critical(
            self,
            "Error Loading File",
            f'Failed to load YAML file:\n{error}'
        )

        self.file_manager.clear()
        self.file_path_label.setText("📁 No file loaded")
        self.word_list.clear()
        self.content_view.setHtml("")
        self.title_label.setText("Select a word")
        self.setWindowTitle("Word Viewer")

    def display_word(self, word):
        """Display word content"""
        word_data = self.file_manager.get_word_data(word)

        if not word_data:
            return

        title = word_data.get("title", "")
        self.title_label.setText(title)

        content = self.formatter.format_word_entry(word_data)
        self.content_view.setHtml(content)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = WordViewer()
    viewer.show()
    sys.exit(app.exec())