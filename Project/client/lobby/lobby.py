import traceback
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
        self.__init_ui()
        self.__registerNetworkEvents()
        self.__registerUIEvents()

        if self.__lobbyInfo is None:
            self.__network.api.refresh_lobby()
        return
    
    def __registerUIEvents(self):

        #add button event handler
        self.button_ready.clicked.connect(self.__on_ready_clicked)
        self.button_start_game.clicked.connect(self.__on_start_game_clicked)
        self.button_leave.clicked.connect(self.__on_leave_clicked)
        self.chat_send_button.clicked.connect(self.__on_send_clicked)
        ##send message on enter
        self.chat_input.returnPressed.connect(self.chat_send_button.click)
        return

    def __init_ui(self):
        
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
        self.mainWindow.central_layout.addWidget(self.__lobby, alignment=Qt.AlignmentFlag.AlignCenter)
        return


    def __update_lobby(self, lobbyInfo):
        if lobbyInfo is None: return
        self.player_list.clear()
        lobbyHost = lobbyInfo['host']


        if lobbyHost.get('playerId') == self.__network.api.accout_info.id:
            self.button_start_game.setEnabled(True)
            self.player_list.addItem(lobbyHost['playerName'] + ' (YOU)' )
        else:
            self.button_start_game.setEnabled(False)
            self.player_list.addItem(lobbyHost['playerName'])

        if lobbyHost['isReady']:
            self.player_list.item(self.player_list.count()-1).setBackground(QColor(lobbyHost['color']))
            
        
        for player in lobbyInfo.get('players'):
            if player.get('playerId') == self.__network.api.accout_info.id:
                self.player_list.addItem(player['playerName'] + ' (YOU)' )
            else:
                self.player_list.addItem(player['playerName'])

            if player['isReady']:
                self.player_list.item(self.player_list.count()-1).setBackground(QColor(player['color']))

        self.__lobby_layout.addWidget(self.player_list, 0, 0)
        
        for message in lobbyInfo.get('messages'):
            self.chat_output.append(f'>>>>> {message}')
        pass

    def __init_players(self):
        self.player_list = QListWidget()
        self.__lobby_layout.addWidget(self.player_list, 0, 0)
        pass

    def __init_button_menu(self):
        self.button_layout = QVBoxLayout()

        self.button_ready = QPushButton('Ready')
        self.button_ready.setFixedSize(150, 40)
        self.button_ready.setStyleSheet(
                "QPushButton:hover { background-color: #70a8ff; }"
                "QPushButton:pressed { background-color: #1e90ff; }"
            )
        
        self.button_start_game = QPushButton('Start Game')
        self.button_start_game.setFixedSize(150, 40)
        self.button_start_game.setStyleSheet(
                "QPushButton:hover { background-color: #70a8ff; }"
                "QPushButton:pressed { background-color: #1e90ff; }"
            )

        self.button_leave = QPushButton('Leave Lobby')
        self.button_leave.setFixedSize(150, 40)
        self.button_leave.setStyleSheet(
                "QPushButton:hover { background-color: #70a8ff; }"
                "QPushButton:pressed { background-color: #1e90ff; }"
            )

        self.button_layout.addWidget(self.button_ready, alignment=Qt.AlignmentFlag.AlignCenter)
        self.button_layout.addWidget(self.button_start_game, alignment=Qt.AlignmentFlag.AlignCenter)
        self.button_layout.addWidget(self.button_leave, alignment=Qt.AlignmentFlag.AlignCenter)
            
        self.__lobby_layout.addLayout(self.button_layout, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        pass

    def __init_chat(self):
        self.chat = QWidget()
        self.chat_layout = QVBoxLayout(self.chat)
        
        self.chat_output = QTextEdit()
        self.chat_output.setReadOnly(True)

        self.chat_input = QLineEdit()
        self.chat_input_layout = QHBoxLayout()
        self.chat_input.setPlaceholderText("Enter Message")

        self.chat_send_button = QPushButton('Send')
        #self.chat_send_button.setFixedSize(150, 40)
        self.chat_send_button.setStyleSheet(
                "QPushButton:hover { background-color: #70a8ff; }"
                "QPushButton:pressed { background-color: #1e90ff; }"
            )
        
        self.chat_input_layout.addWidget(self.chat_input)
        self.chat_input_layout.addWidget(self.chat_send_button)
        
        self.chat_layout.addWidget(self.chat_output)
        self.chat_layout.addLayout(self.chat_input_layout)


        self.__lobby_layout.addWidget(self.chat, 1, 0, 1, 3)
        pass

    #NetworkEventHandler >>> 
    def __on_lobby_update(self, event:NetworkEventObject):
        self.__lobbyInfo = event.eventData
        self.__update_lobby(self.__lobbyInfo)
        #add payer to list
        #display message in chat
        return
    
    def __on_message(self, event:NetworkEventObject):
        #display message in chat
        self.chat_output.append(f'[{event.eventData["from"]}]: {event.eventData["message"]}')
        return

    def __registerNetworkEvents(self):
        self.__network.addNetworkEventHandler(NetworkEvent.LOBBY_UPDATE, self.__on_lobby_update)
        self.__network.addNetworkEventHandler(NetworkEvent.GAME_START, self.__on_game_started)
        self.__network.addNetworkEventHandler(NetworkEvent.MESSAGE, self.__on_message)
        return

    def __unregisterNetworkEvents(self):
        self.__network.removeNetworkEventHandler(NetworkEvent.LOBBY_UPDATE, self.__on_lobby_update)
        self.__network.removeNetworkEventHandler(NetworkEvent.GAME_START, self.__on_game_started)
        self.__network.removeNetworkEventHandler(NetworkEvent.MESSAGE, self.__on_message)
        return

    def __on_game_started(self, event:NetworkEventObject):
        try:
            self.mainWindow.showAlert(f"Game started")
            self.__unregisterNetworkEvents()
            from game.blokusgame import BlokusGame
            self.lobbymenu = BlokusGame(self.mainWindow, self.__network, event.eventData)
            self.__lobby.deleteLater()
        except Exception as e:
            print(f'{str(e)} \n {traceback.format_exc()}') #TODO: add logging
        return
    #<<< NetworkEventHandler


    #ButtonHandler >>>
    def __on_ready_clicked(self):
        #notify server
        self.__network.api.toggleReady()
        return

    def __on_send_clicked(self):
        #notify server
        self.__network.api.sendMessage(self.chat_input.text())
        self.chat_input.clear()
        return

    def __on_start_game_clicked(self):
        for player in self.__lobbyInfo.get('players'):
            if player.get('playerId') == self.__network.api.accout_info.id:
                if not player['isReady']:
                    self.mainWindow.showAlert("You are not ready")
                    return
            else:
                if not player['isReady']:
                    self.mainWindow.showAlert("Not all players are ready")
                    return
        self.__network.api.startGame()
        pass

    def __on_leave_clicked(self):
        #norify server
        self.mainWindow.showAlert("You left the lobby")
        self.__unregisterNetworkEvents()
        self.__network.api.leaveLobby()
        self.__lobby.deleteLater()
        from lobby.lobbymenu import LobbyMenu
        self.lobbymenu = LobbyMenu(self.mainWindow, self.__network)
        return
    #<<< ButtonHandler


