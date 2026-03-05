# -*- coding: utf-8 -*-
"""
@Project : Word_tools
@File    : app_doe_0
@Author  : lingxiao
@Date    : 2026-03-05 10:55
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

import sys
import yaml
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QListWidget, QTextEdit, QLabel, QMessageBox,
    QFileDialog, QPushButton
)
from PyQt6.QtCore import Qt
import os

class WordViewer(QWidget):
    def __init__(self, yaml_path=None):
        super().__init__()

        self.setWindowTitle("Word Viewer")
        self.resize(1000, 700)

        # with open(yaml_path, 'r', encoding='utf-8') as f:
        #     self.data = yaml.safe_load(f)
        self.current_file_path = yaml_path
        self.data = {}

        self.init_ui()

        if yaml_path:
            self.load_yaml_file(yaml_path)

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
        """load yaml file and populate word list"""
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                self.data = yaml.safe_load(f)

            self.current_file_path = yaml_path
            self.file_path_label.setText(f"📁 {self.current_file_path}")
            self.file_path_label.setToolTip(yaml_path)
            self.word_list.clear()
            self.word_list.addItems(self.data.keys())

            if self.data:
                first_word = list(self.data.keys())[0]
                self.word_list.setCurrentRow(0)

            file_name = os.path.basename(yaml_path)
            file_name_without_extension = os.path.splitext(file_name)[0]
            self.setWindowTitle(f"Word Viewer - {file_name_without_extension}")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Loading File",
                f'Failed to load YAML file:\n{str(e)}'
            )
            self.data = {}
            self.current_file_path = None
            self.file_path_label.setText("📁 No file loaded")
            self.word_list.clear()
            self.content_view.setHtml("")
            self.title_label.setText("Select a word")
            self.setWindowTitle("Word Viewer")


    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # Top bar with button and file path display
        top_bar = QHBoxLayout()
        self.open_button = QPushButton("📂 Open YAML File")
        self.open_button.setStyleSheet(
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
        self.open_button.clicked.connect(self.open_file_dialog)
        top_bar.addWidget(self.open_button)

        # File path display
        self.file_path_label = QLabel("📁 No file loaded")
        self.file_path_label.setStyleSheet(
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
        self.file_path_label.setWordWrap(False)
        top_bar.addWidget(self.file_path_label, 1)
        main_layout.addLayout(top_bar)


        content_layout = QHBoxLayout()

        # 左侧列表
        self.word_list = QListWidget()
        # self.word_list.addItems(self.data.keys())
        self.word_list.currentTextChanged.connect(self.display_word)

        # 右侧显示
        right_layout = QVBoxLayout()
        self.title_label = QLabel("Select a word")
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold;")

        self.content_view = QTextEdit()
        self.content_view.setReadOnly(True)

        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Enter your notes here...")
        self.input_box.setMaximumHeight(100)
        self.input_box.setMinimumHeight(100)

        right_layout.addWidget(self.title_label)
        right_layout.addWidget(self.content_view)
        right_layout.addWidget(self.input_box)

        content_layout.addWidget(self.word_list, 2)
        content_layout.addLayout(right_layout, 5)

        main_layout.addLayout(content_layout, 1)

    def display_word(self, word):
        if word not in self.data:
            return

        entry = self.data[word]
        title = entry.get("title", "")
        text = entry.get("text", "")
        example = entry.get("example", "")
        vocabulary = entry.get("vocabulary", [])

        self.title_label.setText(title)

        content = ""

        # text
        if text:
            content += f"<h3>Meaning</h3><p>{text}</p>"

        # example
        if example:
            content += "<h3>Example</h3>"
            if isinstance(example, list):
                for e in example:
                    content += f"<p>{e}</p>"
            else:
                content += f"<p>{example}</p>"

        # vocabulary
        if vocabulary:
            content += "<h3>Vocabulary</h3>"
            for v in vocabulary:
                content += f"<p>{v}</p>"

        self.content_view.setHtml(content)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = WordViewer()
    viewer.show()

    # Open file dialog after window shows
    # yaml_path, _ = QFileDialog.getOpenFileName(
    #     viewer,
    #     "Select YAML File",
    #     "",
    #     "YAML Files (*.yaml *.yml);;All Files (*)"
    # )
    #
    # if yaml_path:
    #     viewer.load_yaml_file(yaml_path)

    sys.exit(app.exec())