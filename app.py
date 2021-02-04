from PyQt5.QtWidgets import QApplication
from src.ui.window import Window
from sys import argv


app = QApplication(argv)
window = Window()
window.show()
app.exec_()
