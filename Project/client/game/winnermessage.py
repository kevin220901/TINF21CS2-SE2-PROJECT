from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

##################################################
## Author: Kevin Wagner
##################################################

class WinnerMessage:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def winnerMessageFrame(self):
        popup = QDialog()
        popup.setWindowTitle("Game Finished")
        popup.setFixedSize(800, 500)
        layout = QGridLayout()
        popup.setModal(True)
        popup.exec()