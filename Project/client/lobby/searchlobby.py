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
        self.table = SearchableTable()
        self.table.setStyleSheet("background-color: #E0E0E0; border: 2px solid black;")
        self.table.setFixedSize(1000, 750)
        
        grid_layout = QGridLayout(self.table)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_layout.addWidget(self.table, alignment=Qt.AlignmentFlag.AlignCenter)
        self.__network.addNetworkEventHandler(NetworkEvent.LOBBIES_GET, self.on_lobbies_get)
        pass

    def on_lobbies_get(self, event:NetworkEventObject):
        self.__table.updateTable(event.eventData)
        pass

class SearchableTable(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.search_bar = QLineEdit()
        self.search_bar.textChanged.connect(self.filter_table)
        self.layout.addWidget(self.search_bar)

        self.table = QTableWidget(5, 4)
        self.table.setHorizontalHeaderLabels(["Loby ID", "Player Count", "Difficulty", ""])
        self.table.verticalHeader().setVisible(False)
        self.layout.addWidget(self.table)

        #self.refresh_button = QPushButton("Refresh")
        #self.refresh_button.clicked.connect(self.refresh_table)
        #self.layout.addWidget(self.refresh_button)
        pass

    def updateTable(self, data):
        self.table.setRowCount(0)

        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)

            for column, cell_data in enumerate(row_data):
                self.table.setItem(row, column, QTableWidgetItem(str(cell_data)))

            join_button = QPushButton("Join")
            join_button.clicked.connect(lambda checked, row=row: self.join_lobby(row))
            self.table.setCellWidget(row, 3, join_button)
            pass

    def filter_table(self, text):
        for i in range(self.table.rowCount()):
            match = False
            for j in range(3):  # Only check the first three columns
                item = self.table.item(i, j)
                if item and text in item.text():
                    match = True
                    break
            if match:
                self.table.showRow(i)
            else:
                self.table.hideRow(i)

    def join_lobby(self, row):
        print(f"Joining lobby {row}")
