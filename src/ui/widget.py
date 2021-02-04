from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *
from PIL import Image
import os

style = open("src/style.qss", "r").read()

default = "Image to PDF"
user_path = os.path.expanduser('~').replace('\\', '/') + "/Desktop"

if default not in os.listdir(user_path):
    os.makedirs(f"{user_path}/{default}", exist_ok=False)


class Widget(QWidget):
    def __init__(self, window):
        QWidget.__init__(self)
        self.window = window
        self.palette().setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(self.palette())

        self.btn_input = QPushButton("폴더 선택")
        self.btn_input.setCursor(Qt.PointingHandCursor)
        self.btn_input.clicked.connect(self.btn_input_clicked)

        self.btn_output = QPushButton("저장 위치 설정")
        self.btn_output.setCursor(Qt.PointingHandCursor)
        self.btn_output.clicked.connect(self.btn_output_clicked)

        self.btn_convert_all = QPushButton("전체 변환")
        self.btn_convert_all.setCursor(Qt.PointingHandCursor)
        self.btn_convert_all.clicked.connect(self.btn_convert_all_clicked)

        self.btn_convert = QPushButton("선택 파일 변환")
        self.btn_convert.setCursor(Qt.PointingHandCursor)
        self.btn_convert.clicked.connect(self.btn_convert_clicked)

        self.btn_remove = QPushButton("파일 제거")
        self.btn_remove.setCursor(Qt.PointingHandCursor)
        self.btn_remove.clicked.connect(self.btn_remove_clicked)

        self.lst_img = QListWidget()
        self.lst_img.setSelectionMode(QAbstractItemView.MultiSelection)

        self.lst_pdf = QListWidget()
        self.lst_pdf.path = f"{user_path}/{default}"
        self.lst_pdf.itemClicked.connect(self.lst_pdf_item_clicked)

        self.log = QTextBrowser()

        btns = QHBoxLayout()
        btns.addWidget(self.btn_input)
        btns.addWidget(self.btn_output)
        btns.addWidget(QLabel(), 10)
        btns.setContentsMargins(0, 0, 0, 0)

        runs = QHBoxLayout()
        runs.addWidget(self.btn_convert_all)
        runs.addWidget(self.btn_convert)
        runs.addWidget(self.btn_remove)
        runs.addWidget(QLabel(), 10)
        runs.setContentsMargins(0, 0, 0, 0)

        lsts = QHBoxLayout()
        lsts.addWidget(self.lst_img)
        lsts.addWidget(self.lst_pdf)
        lsts.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.addLayout(btns, 0)
        layout.addLayout(lsts, 10)
        layout.addLayout(runs, 0)
        layout.addWidget(self.log)
        layout.setContentsMargins(5, 5, 5, 5)

        self.setLayout(layout)
        self.setStyleSheet(style)
        self.window.setCentralWidget(self)

    def btn_input_clicked(self):
        path = QFileDialog.getExistingDirectory(self, caption="폴더 선택", directory=user_path)

        if path:
            files = os.listdir(path)
            self.lst_img.clear()
            self.lst_img.path = path
            self.lst_img.addItems(files)
            self.lst_pdf.clear()

    def btn_output_clicked(self):
        path = QFileDialog.getExistingDirectory(self, caption="폴더 선택", directory=f"{user_path}/{default}")

        if path:
            self.lst_pdf.path = path

    def btn_remove_clicked(self):
        files = []
        for row in range(self.lst_img.count()):
            item = self.lst_img.item(row)
            if not item.isSelected():
                files.append(item.text())

        self.lst_img.clear()
        self.lst_img.addItems(files)

    def btn_convert_all_clicked(self):
        fail, success = [], []

        self.log.clear()
        for row in range(self.lst_img.count()):
            item = self.lst_img.item(row)
            file = item.text()
            try:
                self.method_convert(file)
                success.append(f"{''.join(file.split('.')[:-1])}.pdf")
            except Exception as e:
                self.log.insertPlainText(f"[!] {file} : {e}\n")
                fail.append(file)

        self.lst_img.clear()
        self.lst_img.addItems(fail)

        self.lst_pdf.clear()
        self.lst_pdf.addItems(success)

    def btn_convert_clicked(self):
        fail, success = [], []

        self.log.clear()
        for row in range(self.lst_img.count()):
            item = self.lst_img.item(row)
            file = item.text()
            if item.isSelected():
                try:
                    self.method_convert(file)
                    success.append(f"{''.join(file.split('.')[:-1])}.pdf")
                except Exception as e:
                    self.log.insertPlainText(f"[!] {file} : {e}\n")
                    fail.append(file)

        self.lst_img.clear()
        self.lst_img.addItems(fail)

        self.lst_pdf.clear()
        self.lst_pdf.addItems(success)

    def method_convert(self, file):
        with Image.open(f"{self.lst_img.path}/{file}", "r") as img:
            img = img.convert("RGB")
            img.save(f"{self.lst_pdf.path}/{''.join(file.split('.')[:-1])}.pdf")
            self.log.insertPlainText(f"Success! : {file}\n")

    def lst_pdf_item_clicked(self, item):
        file = item.text()
        os.startfile(f"{self.lst_pdf.path}/{file}")
