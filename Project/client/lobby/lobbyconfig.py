from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *

##################################################
## Author: Kevin Wagner
##################################################

class LobbyConfig:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
    def lobbyConfigFrame(self):
        lobbyConfig_widget = QWidget()
        lobbyConfig_widget.setStyleSheet("background-color: #E0E0E0; border: 2px solid black;")
        lobbyConfig_widget.setFixedSize(700, 400)
    
        grid_layout = QGridLayout(lobbyConfig_widget)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_layout.addWidget(lobbyConfig_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.lobby_name_label = QLabel("Lobby Name           :")
        self.mainWindow.ai_difficulty_label = QLabel("AI Difficulty             :")
        self.mainWindow.lobby_name_input = QLineEdit()
        self.mainWindow.ai_difficulty_choice = QComboBox()
        self.mainWindow.ai_difficulty_choice.addItem("Easy")
        self.mainWindow.ai_difficulty_choice.addItem("Hard")
        
        
        self.mainWindow.create_lobby_button = QPushButton("Create Lobby")
        self.mainWindow.create_lobby_button.setStyleSheet(
            "QPushButton:hover { background-color: #70a8ff; }"
            "QPushButton:pressed { background-color: #1e90ff; }"
        )
        
        label_input_layout = QHBoxLayout()
        label_input_layout.addWidget(self.mainWindow.lobby_name_label)
        label_input_layout.addWidget(self.mainWindow.lobby_name_input)
        
        select_box_layout = QHBoxLayout()
        select_box_layout.addWidget( self.mainWindow.ai_difficulty_label)
        select_box_layout.addWidget( self.mainWindow.ai_difficulty_choice)
        self.mainWindow.ai_difficulty_choice.setMinimumWidth(475)
        
        spacer_layout = QHBoxLayout()
        spacer = QSpacerItem(QSpacerItem(40, 60, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        spacer_layout.addSpacerItem(spacer)
        
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.mainWindow.create_lobby_button)
        
        
        grid_layout.addLayout(label_input_layout, 0, 0, 1, 1)
        grid_layout.addLayout(select_box_layout, 1, 0, 1, 1)
        grid_layout.addLayout(spacer_layout, 2, 0, 1, 1)
        grid_layout.addLayout(button_layout, 3, 0, 1, 1)
        
        self.mainWindow.create_lobby_button.clicked.connect(self.lobby_create)
        
        
    def lobby_create(self):
        lobby_name = self.mainWindow.lobby_name_input.text()
        ai_difficulty = self.mainWindow.ai_difficulty_choice.currentText()
        print("Lobby Name:", lobby_name)
        print("AI Difficulty:", ai_difficulty)