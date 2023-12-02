# Imports
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from account.login import Login
from account.register import Register

from network.networkevent import NetworkEvent
from network.serverapi import NetworkEventObject
from qt6networkadapter import PyQt6_Networkadapter

##################################################
## Author: Kevin Wagner
##################################################


# Main Menu Class
class Menu:
    def __init__(self, mainWindow, network:PyQt6_Networkadapter):
        self.mainWindow = mainWindow
        self.network = network

    # Menu Frame and Widget inside Main Window
    def menuFrame(self):
        
        # Create Basic Frame and Widget
        self.mainWindow.label = QLabel('Welcome to Blokus', self.mainWindow)
        self.mainWindow.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_widget = QWidget(self.mainWindow)
        self.mainWindow.setCentralWidget(self.mainWindow.central_widget)
        self.mainWindow.menuFrame = QFrame(self.mainWindow.central_widget)
        self.mainWindow.menuFrame.setStyleSheet("QFrame { background-color: #E0E0E0; border: 2px solid black; }")
        # Create Layout and Add Label Blokus
        layout = QGridLayout(self.mainWindow.menuFrame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_layout = QVBoxLayout(self.mainWindow.central_widget)
        self.mainWindow.central_layout.addWidget(self.mainWindow.menuFrame)
        self.mainWindow.central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_widget.setLayout(self.mainWindow.central_layout)
        layout.addWidget(self.mainWindow.label)
        # Add Button Register to Layout
        self.mainWindow.button_register = QPushButton("Register", self.mainWindow)  
        self.mainWindow.button_register.setMinimumSize(500, 100)  
        self.mainWindow.button_register.setMaximumSize(600, 400)
        self.mainWindow.button_register.clicked.connect(self.register)
        layout.addWidget(self.mainWindow.button_register)
        # Add Button Login to Layout
        self.mainWindow.button_login = QPushButton("Login", self.mainWindow)
        self.mainWindow.button_login.setMinimumSize(500, 100)  
        self.mainWindow.button_login.setMaximumSize(600, 400)
        self.mainWindow.button_login.clicked.connect(self.login)
        layout.addWidget(self.mainWindow.button_login)
        # Add Button Exit to Layout
        self.mainWindow.button_exit = QPushButton("Exit", self.mainWindow)
        self.mainWindow.button_exit.setMinimumSize(500, 100)  
        self.mainWindow.button_exit.setMaximumSize(600, 400)
        self.mainWindow.button_exit.clicked.connect(self.exit)
        layout.addWidget(self.mainWindow.button_exit)

    # Menu Function Register (Destroy Widget Menu and Create Widget Register inside Main Window)
    def register(self):
        self.mainWindow.menuFrame.deleteLater()
        self.register = Register(self.mainWindow)
        self.register.registerFrame()

    # Menu Function Login (Destroy Widget Menu and Create Widget Login inside Main Window)
    def login(self):
        self.mainWindow.menuFrame.deleteLater()
        self.login = Login(self.mainWindow, self.network)
        self.login.loginFrame()
        
    # Menu Function Exit (Destroy Main Window)
    def exit(self):
        self.mainWindow.close()