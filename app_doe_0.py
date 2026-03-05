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
    QListWidget, QTextEdit, QLabel
)
from PyQt6.QtCore import Qt

class WordViewer(QWidget):
    def __init__(self, yaml_path):
        super().__init__()

        self.setWindowTitle("Word Viewer")
        self.resize(1000, 700)

        with open(yaml_path, 'r', encoding='utf-8') as f:
            self.data = yaml.safe_load(f)

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        # 左侧列表
        self.word_list = QListWidget()
        self.word_list.addItems(self.data.keys())
        self.word_list.currentTextChanged.connect(self.display_word)

        # 右侧显示
        right_layout = QVBoxLayout()
        self.title_label = QLabel("Select a word")
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold;")

        self.content_view = QTextEdit()
        self.content_view.setReadOnly(True)

        right_layout.addWidget(self.title_label)
        right_layout.addWidget(self.content_view)

        main_layout.addWidget(self.word_list, 2)
        main_layout.addLayout(right_layout, 5)

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
    viewer = WordViewer("/Users/lingxiao/.personal/english/ielts-word-list-main/word-list-t.yaml")
    viewer.show()
    sys.exit(app.exec())