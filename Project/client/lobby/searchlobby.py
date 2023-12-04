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
        self.__network = network
        return

    def searchLobbyFrame(self):
        #setup searchable table
        self.__init_searchable_table()

        #setup button handlers
        self.search_button.clicked.connect(lambda: self.__network.api.getLobbies())

        #setup network handlers
        self.__network.addNetworkEventHandler(NetworkEvent.LOBBIES_GET, self.on_lobbies_get)

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
        self.search_bar.setPlaceholderText("Enter Lobby ID")
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

        #add searchabe table to main window
        self.mainWindow.central_layout.addWidget(self.searchable_table, alignment=Qt.AlignmentFlag.AlignCenter)
        return




    def __updateTable(self, data):
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

    def on_lobbies_get(self, event:NetworkEventObject):
        print(f'{str(event)}')
        self.__updateTable(event.eventData)
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

    def join_lobby_clicked(self, row):
        self.__network.api.joinLobby(row['lobbyId'])
        return
