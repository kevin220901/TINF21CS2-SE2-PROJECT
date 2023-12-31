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

class LobbyConfig:
    def __init__(self, mainWindow, network:PyQt6_Networkadapter):
        self.mainWindow = mainWindow
        self.__network = network
        self.__registerNetworkEvents()
        self.__init_ui()
        pass

    def __init_ui(self):
        self.lobbyConfig_widget = QWidget(self.mainWindow)
        self.lobbyConfig_widget.setStyleSheet("background-color: #E0E0E0; border: 2px solid black;")
        self.lobbyConfig_widget.setFixedSize(700, 400)
    
        grid_layout = QGridLayout(self.lobbyConfig_widget)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_layout.addWidget(self.lobbyConfig_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.lobby_name_label = QLabel("Lobby Name           :")
        self.mainWindow.ai_difficulty_label = QLabel("AI Difficulty             :")
        self.mainWindow.lobby_name_input = QLineEdit()
        self.mainWindow.ai_difficulty_choice = QComboBox()
        self.mainWindow.ai_difficulty_choice.addItem("Easy")
        self.mainWindow.ai_difficulty_choice.addItem("Hard")
        
        
        self.mainWindow.create_lobby_button = QPushButton("Create Lobby")
        self.mainWindow.create_lobby_button.setStyleSheet(
            "QPushButton:hover { background-color: #70a8ff; }"
            "QPushButton:pressed { background-color: #1e90ff; }"
        )
        
        self.mainWindow.back_button = QPushButton("Back")
        self.mainWindow.back_button.setStyleSheet(
            "QPushButton:hover { background-color: #70a8ff; }"
            "QPushButton:pressed { background-color: #1e90ff; }"
        )
        
        label_input_layout = QHBoxLayout()
        label_input_layout.addWidget(self.mainWindow.lobby_name_label)
        label_input_layout.addWidget(self.mainWindow.lobby_name_input)
        
        select_box_layout = QHBoxLayout()
        select_box_layout.addWidget( self.mainWindow.ai_difficulty_label)
        select_box_layout.addWidget( self.mainWindow.ai_difficulty_choice)
        self.mainWindow.ai_difficulty_choice.setMinimumWidth(475)
        
        spacer_layout = QHBoxLayout()
        spacer = QSpacerItem(QSpacerItem(40, 60, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        spacer_layout.addSpacerItem(spacer)
        
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.mainWindow.back_button)
        button_layout.addWidget(self.mainWindow.create_lobby_button)
        
        
        
        grid_layout.addLayout(label_input_layout, 0, 0, 1, 1)
        grid_layout.addLayout(select_box_layout, 1, 0, 1, 1)
        grid_layout.addLayout(spacer_layout, 2, 0, 1, 1)
        grid_layout.addLayout(button_layout, 3, 0, 1, 1)
        
        self.mainWindow.create_lobby_button.clicked.connect(self.lobby_create)
        self.mainWindow.back_button.clicked.connect(self.back)

        pass
    
    def __registerNetworkEvents(self):
        self.__network.addNetworkEventHandler(NetworkEvent.LOBBY_CREATE, self.__on_lobby_created)
        pass

    def __unregisterNetworkEvents(self):
        self.__network.removeNetworkEventHandler(NetworkEvent.LOBBY_CREATE, self.__on_lobby_created)
        pass


    def __on_lobby_created(self, event:NetworkEventObject):
        self.mainWindow.showAlert("Lobby created")
        self.__unregisterNetworkEvents()
        from lobby.lobby import Lobby
        self.lobby = Lobby(self.mainWindow, self.__network, event.eventData)
        pass
        
    def lobby_create(self):
        lobby_name = self.mainWindow.lobby_name_input.text()
        ai_difficulty = self.mainWindow.ai_difficulty_choice.currentText()
        self.__network.api.createLobby(lobby_name, ai_difficulty)
        self.lobbyConfig_widget.deleteLater()
        pass

    
    def back(self):
        self.__unregisterNetworkEvents()
        from lobby.lobbymenu import LobbyMenu
        self.lobbymenu = LobbyMenu(self.mainWindow, self.__network)
        