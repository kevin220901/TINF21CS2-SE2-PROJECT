from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

##################################################
## Author: Kevin Wagner
##################################################

class HowToPlay:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def h(self):
        popup = QDialog()
        popup.setWindowTitle("How To Play")
        popup.setFixedSize(800, 500)
        layout = QGridLayout()
        popup.setModal(True)
        popup.exec()
        
