from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class Settings:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def settingsFrame(self):
        popup = QDialog()
        popup.setWindowTitle("Settings")
        popup.setFixedSize(800, 500)
        layout = QGridLayout()
        popup.setModal(True)
        popup.exec()