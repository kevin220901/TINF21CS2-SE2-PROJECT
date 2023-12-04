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
        self.__table: SearchableTable = None
        pass

    def searchLobbyFrame(self):
        self.__table = SearchableTable()
        self.__table.setStyleSheet("background-color: #E0E0E0; border: 2px solid black;")
        self.__table.setFixedSize(700, 400)
        
        grid_layout = self.__table.layout
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_layout.addWidget(self.__table, alignment=Qt.AlignmentFlag.AlignCenter)
        self.__network.addNetworkEventHandler(NetworkEvent.LOBBIES_GET, self.on_lobbies_get)
        self.__network.api.getLobbies()
        pass

    def on_lobbies_get(self, event:NetworkEventObject):
        print(f'{str(event)}')
        self.__table.updateTable(event.eventData)
        pass

class SearchableTable(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.search_layout = QHBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter Lobby ID")
        self.search_bar.textChanged.connect(self.filter_table)
        self.search_bar.returnPressed.connect(self.searchbar_on_return_pressed)
        self.search_layout.addWidget(self.search_bar)

        self.search_button = QPushButton("Refresh Lobbies")
        self.search_layout.addWidget(self.search_button)
        
        self.search_button.setStyleSheet(
            "QPushButton:hover { background-color: #70a8ff; }"
            "QPushButton:pressed { background-color: #1e90ff; }"
        )

        self.layout.addLayout(self.search_layout)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Loby ID", "Player Count", "Difficulty", ""])
        self.table.verticalHeader().setVisible(False)
        self.layout.addWidget(self.table)
        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(0, 250) #lobby id
        self.table.setColumnWidth(3, 150) #join button


        #self.refresh_button = QPushButton("Refresh")
        #self.refresh_button.clicked.connect(self.refresh_table)
        #self.layout.addWidget(self.refresh_button)
        #self.table.horizontalHeader().setStretchLastSection(True)
        #self.table.verticalHeader().setStretchLastSection(True)
        pass

    def updateTable(self, data):
        self.table.setRowCount(0)

        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)

            for column, cell_data in enumerate(row_data.values()):
                self.table.setItem(row, column, QTableWidgetItem(str(cell_data)))

            join_button = QPushButton("Join")
            join_button.setStyleSheet(
                "QPushButton:hover { background-color: #70a8ff; }"
                "QPushButton:pressed { background-color: #1e90ff; }"
            )
            join_button.clicked.connect(lambda checked, row=row: self.join_lobby(row))
            self.table.setCellWidget(row, 3, join_button)
            pass

    def filter_table(self, text):
        ''''Filter the table based on the text (lobby id) in the search bar'''
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)  
            if item and text in item.text():
                self.table.showRow(i)
            else:
                self.table.hideRow(i)

    def join_lobby(self, row):
        print(f"Joining lobby {row}")

    def searchbar_on_return_pressed(self):
        print("Enter key pressed")