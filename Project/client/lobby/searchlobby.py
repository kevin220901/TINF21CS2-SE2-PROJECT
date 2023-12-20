from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *

from network.networkevent import NetworkEvent
from network.serverapi import NetworkEventObject
from qt6networkadapter import PyQt6_Networkadapter

##################################################
## Author: Kevin Wagner & Luis Eckert
##################################################

class SearchLobby:
    def __init__(self, mainWindow, network:PyQt6_Networkadapter):
        self.mainWindow = mainWindow
        self.__network = network

        self.__init_ui()
        self.__registerNetworkEvents()
        return

    def __init_ui(self):
        #setup searchable table
        self.__init_searchable_table()

        #setup button handlers
        self.search_button.clicked.connect(lambda: self.__network.api.getLobbies())
        self.return_button.clicked.connect(self.__on_return_clicked)

        #request available lobbies
        self.__network.api.getLobbies()
        return

    def __init_searchable_table(self):
        #setup seachable table
        self.searchable_table = QWidget()
        self.searchable_table.setFixedSize(700, 400)
        self.searchable_table.setStyleSheet("background-color: #E0E0E0; border: 2px solid black;")
        self.searchable_table_layout = QVBoxLayout(self.searchable_table)
        self.searchable_table_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        

        ##setup search bar
        self.search_layout = QHBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter Lobby ID here...")
        self.search_bar.textChanged.connect(self.filter_table)
        self.search_layout.addWidget(self.search_bar)

        self.search_button = QPushButton("Refresh Lobbies")
        self.search_layout.addWidget(self.search_button)
        
        self.search_button.setStyleSheet(
            "QPushButton:hover { background-color: #70a8ff; }"
            "QPushButton:pressed { background-color: #1e90ff; }"
        )
        
        self.searchable_table_layout.addLayout(self.search_layout)
        
        
        ##setup table
        self.table = QTableWidget(0, 4)
        self.table.setStyleSheet("background-color: #E0E0E0; border: 2px solid black;")
        self.table.setHorizontalHeaderLabels(["Loby ID", "Player Count", "Difficulty", ""])
        self.table.verticalHeader().setVisible(False)
        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(0, 250) #lobby id
        self.table.setColumnWidth(3, 150) #join button
        
        self.searchable_table_layout.addWidget(self.table)

        self.return_button = QPushButton("Return")
        self.return_button.setStyleSheet(
            "QPushButton:hover { background-color: #70a8ff; }"
            "QPushButton:pressed { background-color: #1e90ff; }"
        )

        # Add the button to the layout
        self.searchable_table_layout.addWidget(self.return_button)

        #add searchabe table to main window
        self.mainWindow.central_layout.addWidget(self.searchable_table, alignment=Qt.AlignmentFlag.AlignCenter)
        return


    def __updateTable(self, data):
        '''Update the serachable table with the data from the server'''
        self.__rows = data
        self.table.setRowCount(0)

        for row_data in self.__rows:
            row = self.table.rowCount()
            self.table.insertRow(row)

            for column, cell_data in enumerate(row_data.values()):
                self.table.setItem(row, column, QTableWidgetItem(str(cell_data)))

            join_button = QPushButton("Join")
            join_button.setStyleSheet(
                "QPushButton:hover { background-color: #70a8ff; }"
                "QPushButton:pressed { background-color: #1e90ff; }"
            )
            join_button.clicked.connect(lambda checked, row=row: self.join_lobby_clicked(self.__rows[row]))
            self.table.setCellWidget(row, 3, join_button)
            return
    
    def filter_table(self, text):
        ''''Filter the table based on the text (lobby id) in the search bar'''
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)  
            if item and text in item.text():
                self.table.showRow(i)
            else:
                self.table.hideRow(i)
        return

    def __registerNetworkEvents(self):
        self.__network.addNetworkEventHandler(NetworkEvent.LOBBIES_GET, self.__on_lobbies_get)
        self.__network.addNetworkEventHandler(NetworkEvent.LOBBY_JOIN, self.__on_lobby_join)
        return
    
    def __unregisterNetworkEvents(self):
        self.__network.removeNetworkEventHandler(NetworkEvent.LOBBIES_GET, self.__on_lobbies_get)
        self.__network.removeNetworkEventHandler(NetworkEvent.LOBBY_JOIN, self.__on_lobby_join)
        return

    #network handlers >>>
    def __on_lobby_join(self, event:NetworkEventObject):
        self.mainWindow.showAlert("Lobbies refreshed")
        self.__unregisterNetworkEvents()
        self.searchable_table.deleteLater()
        from lobby.lobby import Lobby
        self.lobby = Lobby(self.mainWindow, self.__network, event.eventData)
        pass

    def __on_lobbies_get(self, event:NetworkEventObject):
        self.mainWindow.showAlert("Lobbies refreshed")
        self.__updateTable(event.eventData)
        return
    #network handlers <<<


    #button handlers >>>
    def join_lobby_clicked(self, row):
        print(f'Joining lobby {row["lobbyId"]}')
        self.__network.api.joinLobby(row['lobbyId'])
        return
    
    def __on_return_clicked(self):
        self.__unregisterNetworkEvents()
        self.searchable_table.deleteLater()
        from lobby.lobbymenu import LobbyMenu
        self.lobbymenu = LobbyMenu(self.mainWindow, self.__network)
        pass
    #button handlers <<<

