from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class Login:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def loginFrame(self):
        self.mainWindow.loginFrame = QFrame(self.mainWindow.central_widget)
        self.mainWindow.loginFrame.setStyleSheet("QFrame { background-color: #E0E0E0; border: 2px solid black; }")
        layout = QGridLayout(self.mainWindow.loginFrame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_layout.addWidget(self.mainWindow.loginFrame)