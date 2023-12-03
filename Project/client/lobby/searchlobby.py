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

class SearchLobby:
    def __init__(self, mainWindow, network:PyQt6_Networkadapter):
        self.mainWindow = mainWindow
    def searchLobbyFrame(self):
        lobbyConfig_widget = QWidget()
        lobbyConfig_widget.setStyleSheet("background-color: #E0E0E0; border: 2px solid black;")
        lobbyConfig_widget.setFixedSize(1000, 750)
        
        grid_layout = QGridLayout(lobbyConfig_widget)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_layout.addWidget(lobbyConfig_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        