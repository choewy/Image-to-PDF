from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *
from src.ui.widget import Widget


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowIcon(QIcon("src/Icon.png"))
        self.setWindowTitle("Image to PDF")
        self.palette().setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(self.palette())
        Widget(self)
        self.setMinimumSize(800, 800)
