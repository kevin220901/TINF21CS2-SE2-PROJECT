from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class Settings:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def settingsFrame(self):
        popup = QDialog()
        popup.setWindowTitle("Popup")
        popup.setMinimumSize(300, 200)
        layout = QVBoxLayout()