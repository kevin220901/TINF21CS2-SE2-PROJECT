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
        popup.setFixedSize(600, 250)
        layout = QGridLayout()
        popup.setModal(True)
        layout = QVBoxLayout()

        # Label
        label = QLabel("Bla Bla Bla")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        h_layout = QHBoxLayout()
        button_back_lobby = QPushButton("Back to Lobby")
        h_layout.addWidget(button_cancel)
        button_back_menu = QPushButton("Main Lobby Menu")
        h_layout.addWidget(button_back_lobby)
        button_back_lobby.clicked.connect(self.back_to_lobby)
        button_back_menu.clicked.connect(self.back_to_lobbymenu)
        layout.addLayout(h_layout)
        popup.setLayout(layout)
        popup.exec()
    
    def back_to_lobby(self):
        pass
    
    def back_to_lobbymenu(self):
        pass