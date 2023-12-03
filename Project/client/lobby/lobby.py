from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *

from network.networkevent import NetworkEvent
from network.serverapi import NetworkEventObject
from qt6networkadapter import PyQt6_Networkadapter

##################################################
## Author: Kevin Wagner
##################################################

class Lobby:
    def __init__(self, mainWindow, network:PyQt6_Networkadapter, lobbyInfo):
        self.mainWindow = mainWindow
        self.__network = network
        self.__lobbyInfo = lobbyInfo
        pass
    
    def lobbyFrame(self):
        lobby_widget = QWidget()
        lobby_widget.setStyleSheet("background-color: #E0E0E0; border: 2px solid black;")
        lobby_widget.setFixedSize(1000, 750)
        
        grid_layout = QGridLayout(lobby_widget)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_layout.addWidget(lobby_widget, alignment=Qt.AlignmentFlag.AlignCenter)