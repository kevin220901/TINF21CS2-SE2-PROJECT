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

class UpdatePassword:
    def __init__(self, mainWindow, network:PyQt6_Networkadapter):
        self.mainWindow = mainWindow
        self.__network = network
        self.__popup:QDialog = None

        self.__init_ui()
        self.__registerNetworkEvents()
        return

    def __init_ui(self):
        self.__popup = QDialog(self.mainWindow)
        self.__popup.setWindowTitle("Update Password")
        self.__popup.setFixedSize(600, 150)  # Increase the height of the dialog
        layout = QGridLayout()
        self.__popup.setModal(True)
        layout = QVBoxLayout()

        # Label
        label = QLabel("Enter new password:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Treat the input as a password
        layout.addWidget(self.password_input)

        h_layout = QHBoxLayout()
        button_cancel = QPushButton("Cancel")
        h_layout.addWidget(button_cancel)
        button_update = QPushButton("Update Password")
        h_layout.addWidget(button_update)
        button_update.clicked.connect(self.update_password)
        button_cancel.clicked.connect(self.__popup.close)
        layout.addLayout(h_layout)

        # Add spacer to reduce the distance between password input and label
        spacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

        self.__popup.setLayout(layout)
        self.__popup.exec()
        return
    
    def update_password(self):
        new_password = self.password_input.text()
        self.__network.api.updatePassword(new_password)
        self.__popup.close()
        pass

    def __registerNetworkEvents(self): 
        self.__network.addNetworkEventHandler(NetworkEvent.PROFILE_UPDATE_PASSWORD, self.__on_updatePasswordSuccess)
        pass

    def __unregisterNetworkEvents(self):
        self.__network.removeNetworkEventHandler(NetworkEvent.PROFILE_UPDATE_PASSWORD, self.__on_updatePasswordSuccess)
        pass


    def __on_updatePasswordSuccess(self, event:NetworkEventObject):
        self.mainWindow.showAlert("Password updated")
        self.__unregisterNetworkEvents()
        from lobby.lobbymenu import LobbyMenu
        self.menu = LobbyMenu(self.mainWindow, self.__network)
        pass