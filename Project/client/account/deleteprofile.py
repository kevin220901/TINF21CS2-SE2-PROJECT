from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *


class DeleteProfile:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def deleteProfileFrame(self):
        popup = QDialog()
        popup.setWindowTitle("Delete Profile")
        popup.setFixedSize(600, 300)
        layout = QGridLayout()
        popup.setModal(True)
        popup.exec()