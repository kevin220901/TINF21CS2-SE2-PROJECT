from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from account.login import Login
from account.register import Register

class Menu:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def menuFrame(self):
        self.mainWindow.label = QLabel('Blokus', self.mainWindow)
        self.mainWindow.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_widget = QWidget(self.mainWindow)
        self.mainWindow.setCentralWidget(self.mainWindow.central_widget)
        self.mainWindow.menuFrame = QFrame(self.mainWindow.central_widget)
        self.mainWindow.menuFrame.setStyleSheet("QFrame { background-color: #E0E0E0; border: 2px solid black; }")
        layout = QGridLayout(self.mainWindow.menuFrame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_layout = QVBoxLayout(self.mainWindow.central_widget)
        self.mainWindow.central_layout.addWidget(self.mainWindow.menuFrame)
        self.mainWindow.central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_widget.setLayout(self.mainWindow.central_layout)
        layout.addWidget(self.mainWindow.label)
        self.mainWindow.button_register = QPushButton("Registrieren", self.mainWindow)  
        self.mainWindow.button_register.setMinimumSize(500, 100)  
        self.mainWindow.button_register.setMaximumSize(600, 400)
        self.mainWindow.button_register.clicked.connect(self.register)
        layout.addWidget(self.mainWindow.button_register)
        self.mainWindow.button_login = QPushButton("Anmelden", self.mainWindow)
        self.mainWindow.button_login.setMinimumSize(500, 100)  
        self.mainWindow.button_login.setMaximumSize(600, 400)
        self.mainWindow.button_login.clicked.connect(self.login)
        layout.addWidget(self.mainWindow.button_login)
        self.mainWindow.button_exit = QPushButton("Exit", self.mainWindow)
        self.mainWindow.button_exit.setMinimumSize(500, 100)  
        self.mainWindow.button_exit.setMaximumSize(600, 400)
        self.mainWindow.button_exit.clicked.connect(self.exit)
        layout.addWidget(self.mainWindow.button_exit)

    def register(self):
        self.mainWindow.menuFrame.deleteLater()
        self.register = Register(self.mainWindow)
        self.register.registerFrame()

    def login(self):
        self.mainWindow.menuFrame.deleteLater()
        self.login = Login(self.mainWindow)
        self.login.loginFrame()
        

    def exit(self):
        self.mainWindow.close()