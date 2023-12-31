from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from qt6networkadapter import PyQt6_Networkadapter

##################################################
## Author: Kevin Wagner
##################################################

class WinnerMessage:
    def __init__(self, mainWindow, network: PyQt6_Networkadapter):
        self.mainWindow = mainWindow
        self.__network = network
        self.__init_ui()

    def __init_ui(self):
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
        button_back_menu = QPushButton("Main Lobby Menu")
        h_layout.addWidget(button_back_lobby)
        button_back_lobby.clicked.connect(self.back_to_lobby)
        button_back_menu.clicked.connect(self.back_to_lobbymenu)
        layout.addLayout(h_layout)
        popup.setLayout(layout)
        popup.exec()
    
    def back_to_lobby(self):
        from lobby.lobby import Lobby
        self.lobby = Lobby(self.mainWindow, self.__network, None)
        pass
    
    def back_to_lobbymenu(self):
        self.__network.api.leaveLobby()

        from lobby.lobbymenu import LobbyMenu
        self.lobbymenu = LobbyMenu(self.mainWindow, self.__network)
        return