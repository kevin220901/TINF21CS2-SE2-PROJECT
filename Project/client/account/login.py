# Imports
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
from network.networkevent import NetworkEvent
from network.serverapi import NetworkEventObject
from qt6networkadapter import PyQt6_Networkadapter
sys.path.append('./lobby')

##################################################
## Author: Kevin Wagner
##################################################

# Login Class for User Login
class Login:
    def __init__(self, mainWindow, network:PyQt6_Networkadapter):
        self.mainWindow = mainWindow
        self.__network = network

        self.__network.addNetworkEventHandler(NetworkEvent.LOGIN_SUCCESS, self.__on_login)
        
    # Initilize Login Frame and Widget
    def loginFrame(self):
        login_widget = QWidget()
        login_widget.setStyleSheet("background-color: #E0E0E0; border: 2px solid black;")
        login_widget.setFixedSize(500, 200)
        
        # Create Layout for Login Mask
        grid_layout = QGridLayout(login_widget)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_layout.addWidget(login_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Create Label and Input for Username and Password
        self.mainWindow.username_label = QLabel("Username :")
        self.mainWindow.password_label = QLabel("Password  :")
        self.mainWindow.username_input = QLineEdit()
        self.mainWindow.password_input = QLineEdit()
        
        # Make Password unreadable
        self.mainWindow.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Create and Add Login Button to Layout 
        self.mainWindow.login_button = QPushButton("Login")
        self.mainWindow.login_button.setStyleSheet(
            "QPushButton:hover { background-color: #70a8ff; }"
            "QPushButton:pressed { background-color: #1e90ff; }"
        )
        
        # Create and Add Back Button to Layout
        self.mainWindow.back_button = QPushButton("Back")
        self.mainWindow.back_button.setStyleSheet(
            "QPushButton:hover { background-color: #70a8ff; }"
            "QPushButton:pressed { background-color: #1e90ff; }"
        )
        
        # Layout for Label and Input inside of Grid Layout
        label_input_layout = QHBoxLayout()
        label_input_layout.addWidget(self.mainWindow.username_label)
        label_input_layout.addWidget(self.mainWindow.username_input)

        label_input_layout2 = QHBoxLayout()
        label_input_layout2.addWidget(self.mainWindow.password_label)
        label_input_layout2.addWidget(self.mainWindow.password_input)
        
        spacer_layout = QHBoxLayout()
        spacer = QSpacerItem(QSpacerItem(40, 30, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        spacer_layout.addSpacerItem(spacer)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.mainWindow.back_button)
        button_layout.addWidget(self.mainWindow.login_button)
        
        
        

        # Set Layout
        grid_layout.addLayout(label_input_layout, 0, 0, 1, 1)
        grid_layout.addLayout(label_input_layout2, 1, 0, 1, 1)
        grid_layout.addLayout(spacer_layout, 2, 0, 1, 1)
        grid_layout.addLayout(button_layout, 3, 0, 1, 1)
        

        # Add Button Functions
        self.mainWindow.login_button.clicked.connect(self.check_login)
        self.mainWindow.back_button.clicked.connect(self.back)
        
    # Check Login Data and User Login for Game Menu
    #TODO Implementierung Login Function
    def check_login(self):
        username = self.mainWindow.username_input.text()
        password = self.mainWindow.password_input.text()

        self.__network.api.login(username, password)
        #api.events.login.connect(self.__on_connect)
        #send Auth Request to socket server 
        #api.login(username, password)

        #print("Username:", username)
        #print("Password:", password)
        
    
    
    def __on_login(self, eventObj:NetworkEventObject):
        print(eventObj)
        from lobby.lobbymenu import LobbyMenu
        self.lobbymenu = LobbyMenu(self.mainWindow)
        self.lobbymenu.lobbyMenuFrame()
        pass

    # Add Back Button Function
    def back(self):
        self.__network.removeNetworkEventHandler(NetworkEvent.LOGIN_SUCCESS, self.__on_login)
        from menu import Menu
        self.menu = Menu(self.mainWindow, self.__network)
        self.menu.menuFrame()