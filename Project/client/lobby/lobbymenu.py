from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from lobby.lobbyconfig import LobbyConfig
from lobby.searchlobby import SearchLobby
from account.userprofile import UserProfile
from network.networkevent import NetworkEvent
from qt6networkadapter import PyQt6_Networkadapter

##################################################
## Author: Kevin Wagner
##################################################

class LobbyMenu:
    def __init__(self, mainWindow, network:PyQt6_Networkadapter):
        self.mainWindow = mainWindow
        self.__network = network
        pass

    def lobbyMenuFrame(self):
        self.mainWindow.label = QLabel('Blokus', self.mainWindow)
        self.mainWindow.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_widget = QWidget(self.mainWindow)
        self.mainWindow.setCentralWidget(self.mainWindow.central_widget)
        self.mainWindow.lobbymenuFrame = QFrame(self.mainWindow.central_widget)
        self.mainWindow.lobbymenuFrame.setStyleSheet("QFrame { background-color: #E0E0E0; border: 2px solid black; }")
        layout = QGridLayout(self.mainWindow.lobbymenuFrame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_layout = QVBoxLayout(self.mainWindow.central_widget)
        self.mainWindow.central_layout.addWidget(self.mainWindow.lobbymenuFrame)
        self.mainWindow.central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_widget.setLayout(self.mainWindow.central_layout)
        layout.addWidget(self.mainWindow.label)
        self.mainWindow.button_register = QPushButton("Create Lobby", self.mainWindow)  
        self.mainWindow.button_register.setMinimumSize(500, 100)  
        self.mainWindow.button_register.setMaximumSize(600, 400)
        self.mainWindow.button_register.clicked.connect(self.create_lobby)
        layout.addWidget(self.mainWindow.button_register)
        self.mainWindow.button_login = QPushButton("Join Lobby", self.mainWindow)
        self.mainWindow.button_login.setMinimumSize(500, 100)  
        self.mainWindow.button_login.setMaximumSize(600, 400)
        self.mainWindow.button_login.clicked.connect(self.search_lobby)
        layout.addWidget(self.mainWindow.button_login)
        self.mainWindow.button_login = QPushButton("My Profile", self.mainWindow)
        self.mainWindow.button_login.setMinimumSize(500, 100)  
        self.mainWindow.button_login.setMaximumSize(600, 400)
        self.mainWindow.button_login.clicked.connect(self.my_profile)
        layout.addWidget(self.mainWindow.button_login)
        self.mainWindow.button_exit = QPushButton("Exit", self.mainWindow)
        self.mainWindow.button_exit.setMinimumSize(500, 100)  
        self.mainWindow.button_exit.setMaximumSize(600, 400)
        self.mainWindow.button_exit.clicked.connect(self.exit)
        layout.addWidget(self.mainWindow.button_exit)

    def create_lobby(self):
        self.mainWindow.lobbymenuFrame.deleteLater()
        self.create_lobby = LobbyConfig(self.mainWindow, self.__network)
        self.create_lobby.lobbyConfigFrame()

    def search_lobby(self):
        self.mainWindow.lobbymenuFrame.deleteLater()
        self.search_lobby = SearchLobby(self.mainWindow, self.__network)
        self.search_lobby.searchLobbyFrame()
    
    def my_profile(self):
        self.mainWindow.lobbymenuFrame.deleteLater()
        self.my_profile = UserProfile(self.mainWindow, self.__network)
        self.my_profile.userProfileFrame()

    def exit(self):
        self.mainWindow.close()