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

class DeleteProfile:
    def __init__(self, mainWindow, network:PyQt6_Networkadapter):
        self.mainWindow = mainWindow
        self.__network = network
        self.__popup:QDialog = None

    def deleteProfileFrame(self):
        self.__popup = QDialog()
        self.__popup.setWindowTitle("Delete Profile")
        self.__popup.setFixedSize(600, 250)
        layout = QGridLayout()
        self.__popup.setModal(True)
        layout = QVBoxLayout()

        # Label
        label = QLabel("Are you sure you want to delete this profile?")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        h_layout = QHBoxLayout()
        button_cancel = QPushButton("Cancel")
        h_layout.addWidget(button_cancel)
        button_delete = QPushButton("Delete")
        h_layout.addWidget(button_delete)
        button_delete.clicked.connect(self.delete_profile)
        button_cancel.clicked.connect(self.__popup.close)
        layout.addLayout(h_layout)
        self.__popup.setLayout(layout)
        self.__popup.exec()

        self.__network.addNetworkEventHandler(NetworkEvent.PROFILE_DELETE, self.__on_profileDeleteSuccess)
    
    def delete_profile(self):
        self.__network.api.deleteProfile()
        self.__popup.close()
        pass


    def __on_profileDeleteSuccess(self, event:NetworkEventObject):
        from menu import Menu
        self.menu = Menu(self.mainWindow, self.__network)
        self.menu.menuFrame()
        pass