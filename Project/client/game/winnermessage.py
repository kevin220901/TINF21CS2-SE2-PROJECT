from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from qt6networkadapter import PyQt6_Networkadapter

##################################################
## Author: Kevin Wagner
##################################################

class WinnerMessage:
    def __init__(self, mainWindow, network: PyQt6_Networkadapter, winnerInfo:list):
        self.mainWindow = mainWindow
        self.__network = network
        self.__winnerInfo = winnerInfo
        self.__init_ui()

    def __init_ui(self):
        
        self._popup = QDialog(self.mainWindow)
        self._popup.setWindowTitle("Game Finished")
        self._popup.setFixedSize(600, 250)
        layout = QGridLayout()
        self._popup.setModal(True)
        layout = QVBoxLayout()

        # Label
        winner_list = QListWidget()
        if len(self.__winnerInfo) > 0:
            # at least one winner -> show list
            label = QLabel("Winner:")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            for winner in self.__winnerInfo:
                winner_name = winner['playerName']
                if winner.get('playerId') == self.__network.api.accout_info.id:
                    winner_name += " (You)"
                winner_list.addItem(f"{winner_name}")

            layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(winner_list, alignment=Qt.AlignmentFlag.AlignCenter)
        else:
            
            label = QLabel("No winner")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        h_layout = QHBoxLayout()
        button_back_lobby = QPushButton("Back to Lobby")
        button_back_menu = QPushButton("Main Lobby Menu")
        h_layout.addWidget(button_back_lobby)
        h_layout.addWidget(button_back_menu)
        button_back_lobby.clicked.connect(self.back_to_lobby)
        button_back_menu.clicked.connect(self.back_to_lobbymenu)
        layout.addLayout(h_layout)
        self._popup.setLayout(layout)
        self._popup.exec()
    
    def back_to_lobby(self):
        from lobby.lobby import Lobby
        self.lobby = Lobby(self.mainWindow, self.__network, None)
        self._popup.close()
        pass
    
    def back_to_lobbymenu(self):
        self.__network.api.leaveLobby()

        from lobby.lobbymenu import LobbyMenu
        self.lobbymenu = LobbyMenu(self.mainWindow, self.__network)
        self._popup.close()
        return