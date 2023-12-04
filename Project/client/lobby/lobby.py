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

        self.__lobby = QWidget()
        self.__lobby.setStyleSheet("background-color: #E0E0E0; border: 2px solid black;")
        self.__lobby_layout = QGridLayout(self.__lobby)

        # Set the stretch factors for the columns
        self.__lobby_layout.setColumnStretch(0, 0)  # Player list
        self.__lobby_layout.setColumnStretch(1, 1)  # Buttons
        self.__init_players()
        self.__init_button_menu()
        self.__init_chat()

        self.__update_lobby(self.__lobbyInfo)

        self.__network.addNetworkEventHandler(NetworkEvent.LOBBY_UPDATE, self.__on_lobby_update)

        
        self.mainWindow.central_layout.addWidget(self.__lobby, alignment=Qt.AlignmentFlag.AlignCenter)
        pass


    def __update_lobby(self, lobbyInfo):
        if lobbyInfo is None: return
        self.player_list.clear()
        self.player_list.addItem(lobbyInfo['host']['playerName'])
        
        for player in lobbyInfo.get('players'):
            self.player_list.addItem(player['playerName'])

        self.__lobby_layout.addWidget(self.player_list, 0, 0)
        pass

#TODO: remove dummy data
    def __init_players(self):
        # 1. List of players
        self.player_list = QListWidget()
        pass

    def __init_button_menu(self):
        # 2. Four buttons
        self.button_layout = QVBoxLayout()

        self.button_ready = QPushButton('Ready')
        self.button_ready.setFixedSize(150, 40)
        self.button_ready.setStyleSheet(
                "QPushButton:hover { background-color: #70a8ff; }"
                "QPushButton:pressed { background-color: #1e90ff; }"
            )
        self.button_ready.clicked.connect(self.__on_game_started)

        self.button_start_game = QPushButton('Start Game')
        self.button_start_game.setFixedSize(150, 40)
        self.button_start_game.setStyleSheet(
                "QPushButton:hover { background-color: #70a8ff; }"
                "QPushButton:pressed { background-color: #1e90ff; }"
            )
        self.button_start_game.clicked.connect(self.__on_start_game_clicked)

        self.button_leave = QPushButton('Leave Lobby')
        self.button_leave.setFixedSize(150, 40)
        self.button_leave.setStyleSheet(
                "QPushButton:hover { background-color: #70a8ff; }"
                "QPushButton:pressed { background-color: #1e90ff; }"
            )
        self.button_leave.clicked.connect(self.__on_leave_clicked)

        self.button_layout.addWidget(self.button_ready, alignment=Qt.AlignmentFlag.AlignCenter)
        self.button_layout.addWidget(self.button_start_game, alignment=Qt.AlignmentFlag.AlignCenter)
        self.button_layout.addWidget(self.button_leave, alignment=Qt.AlignmentFlag.AlignCenter)
            
        self.__lobby_layout.addLayout(self.button_layout, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        pass

    def __init_chat(self):
        
        # 3. Chat window
        self.chat_window = QTextEdit()
        self.__lobby_layout.addWidget(self.chat_window, 1, 0, 1, 3)
        pass
    

    #NetworkEventHandler >>> 
    def __on_lobby_update(self, event:NetworkEventObject):
        print(event.eventData)
        self.__lobbyInfo = event.eventData
        self.__update_lobby(self.__lobbyInfo)
        #add payer to list
        #display message in chat
        pass

    def __on_game_started(self, event:NetworkEventObject):
        #switch to game ui
        pass
    #<<< NetworkEventHandler


    #ButtonHandler >>>
    def __on_ready_clicked(self):
        #notify server
        self.__network.api.ready()
        pass

    def __on_start_game_clicked(self):
        #notify server
        pass

    def __on_leave_clicked(self):
        #norify server
        self.__network.api.leaveLobby()
        from lobby.lobbymenu import LobbyMenu
        self.lobbymenu = LobbyMenu(self.mainWindow, self.__network)
        self.lobbymenu.lobbyMenuFrame()
        pass
    #<<< ButtonHandler


