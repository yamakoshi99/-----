#!/usr/bin/env python3
# v1.0
import sys
import csv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QTextEdit, QFileDialog, QMessageBox, QListWidget,
                             QListWidgetItem, QDialog)
from PyQt5.QtCore import Qt
from gs1_utils import calculate_check_digit

class FunctionSelectionDialog(QDialog):  # 機能選択ダイアログ
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("機能選択")
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.list_widget.addItem("単一コード計算")
        self.list_widget.addItem("テキストエリア入力")
        self.list_widget.addItem("ファイルアップロード")

        select_button = QPushButton("選択")
        select_button.clicked.connect(self.accept)  # ダイアログを閉じる

        layout.addWidget(self.list_widget)
        layout.addWidget(select_button)
        self.setLayout(layout)

    def get_selected_function(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            return selected_items[0].text()
        return None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GS1 Check Digit Calculator")
        self.selected_function = None  # 選択された機能を格納
        self.initUI()
        self.show_function_selection_dialog()  # 起動時にダイアログを表示

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # 戻るボタンを作成
        self.back_button = QPushButton("戻る")
        self.back_button.clicked.connect(self.show_function_selection_dialog)
        self.back_button.hide()  # 初期状態では非表示
        self.main_layout.addWidget(self.back_button)

        # 各機能のUIを作成
        self.single_widget = self.create_single_input_ui()
        self.text_widget = self.create_text_input_ui()
        self.file_widget = self.create_file_upload_ui()

        # 初期状態では全て非表示
        self.single_widget.hide()
        self.text_widget.hide()
        self.file_widget.hide()

        self.main_layout.addWidget(self.single_widget)
        self.main_layout.addWidget(self.text_widget)
        self.main_layout.addWidget(self.file_widget)

    def create_single_input_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        single_layout = QHBoxLayout()
        single_label = QLabel("GS1コード:")
        self.single_input = QLineEdit()
        single_button = QPushButton("計算")
        single_button.clicked.connect(self.calculate_single)
        single_layout.addWidget(single_label)
        single_layout.addWidget(self.single_input)
        single_layout.addWidget(single_button)
        layout.addLayout(single_layout)

        self.single_result_label = QLabel("")
        layout.addWidget(self.single_result_label)
        return widget

    def create_text_input_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        text_label = QLabel("CSVデータを入力 (一行ずつ):")
        self.text_input = QTextEdit()
        text_button = QPushButton("計算")
        text_button.clicked.connect(self.calculate_from_text)

        layout.addWidget(text_label)
        layout.addWidget(self.text_input)
        layout.addWidget(text_button)
        return widget

    def create_file_upload_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        upload_button = QPushButton("CSVファイルから計算")
        upload_button.clicked.connect(self.calculate_from_file)
        layout.addWidget(upload_button)
        return widget

    def show_function_selection_dialog(self):
        self.dialog = FunctionSelectionDialog(self)
        if self.dialog.exec_() == self.dialog.Accepted:
            self.selected_function = self.dialog.get_selected_function()
            if self.selected_function:
                self.show_selected_function()

    def show_selected_function(self):
        selected_items = self.dialog.list_widget.selectedItems()
        if not selected_items:
            return

        selected_function = selected_items[0].text()
        self.hide_all_functions()
        self.back_button.show()  # 戻るボタンを表示

        if selected_function == "単一コード計算":
            self.single_widget.show()
        elif selected_function == "テキストエリア入力":
            self.text_widget.show()
        elif selected_function == "ファイルアップロード":
            self.file_widget.show()

    def hide_all_functions(self):
        self.single_widget.hide()
        self.text_widget.hide()
        self.file_widget.hide()

    def calculate_single(self):
        data = self.single_input.text()
        result = calculate_check_digit(data)
        self.single_result_label.setText(f"チェックデジット: {result}")

    def calculate_from_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if filename:
            try:
                with open(filename, 'r', newline='') as file:
                    self.calculate_and_display(csv.reader(file))
            except Exception as e:
                QMessageBox.critical(self, "エラー", str(e))

    def calculate_from_text(self):
        text = self.text_input.toPlainText()
        if text:
            try:
                reader = csv.reader(text.splitlines())
                self.calculate_and_display(reader)
            except Exception as e:
                QMessageBox.critical(self, "エラー", str(e))

    def calculate_and_display(self, reader):
        try:
            results = []
            for row in reader:
                if row:
                    data = row[0]
                    check_digit = calculate_check_digit(data)
                    results.append(f"{data}{check_digit}")
            QMessageBox.information(self, "結果", "\n".join(results))
        except Exception as e:
            QMessageBox.critical(self, "エラー", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
