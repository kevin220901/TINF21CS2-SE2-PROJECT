from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from network.serverapi import NetworkEventObject
from network.networkevent import NetworkEvent
from qt6networkadapter import PyQt6_Networkadapter

##################################################
## Author: Kevin Wagner
##################################################

class UserProfile:
    def __init__(self, mainWindow, network:PyQt6_Networkadapter):
        self.mainWindow = mainWindow
        self.__network = network

    def userProfileFrame(self):
        userProfile_widget = QWidget()
        userProfile_widget.setStyleSheet("background-color: #E0E0E0; border: 2px solid black;")
        userProfile_widget.setFixedSize(700, 400)
        
        grid_layout = QGridLayout(userProfile_widget)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_layout.addWidget(userProfile_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.mainWindow.username_label = QLabel("Username                   :")
        self.mainWindow.email_label = QLabel("E-Mail                         :")
        self.mainWindow.color_choice_label = QLabel("Preffered Color           :")
        self.mainWindow.username_input = QLineEdit()
        self.mainWindow.email_input = QLineEdit()
        self.mainWindow.color_choice = QComboBox()
        self.mainWindow.color_choice.addItem("Blue")
        self.mainWindow.color_choice.addItem("Green")
        self.mainWindow.color_choice.addItem("Orange")
        self.mainWindow.color_choice.addItem("Red")
        self.mainWindow.color_choice.addItem("Yellow")
        
        # Add Button for Save Function
        self.mainWindow.save_button = QPushButton("Save")
        self.mainWindow.save_button.setStyleSheet(
            "QPushButton:hover { background-color: #70a8ff; }"
            "QPushButton:pressed { background-color: #1e90ff; }"
        )
        
        # Add Button for Back Function
        self.mainWindow.back_button = QPushButton("Back")
        self.mainWindow.back_button.setStyleSheet(
            "QPushButton:hover { background-color: #70a8ff; }"
            "QPushButton:pressed { background-color: #1e90ff; }"
        )
        
        # Add Button for Delete Profile Function
        self.mainWindow.delete_profile_button = QPushButton("Delete Profile")
        self.mainWindow.delete_profile_button.setStyleSheet(
            "QPushButton:hover { background-color: #70a8ff; }"
            "QPushButton:pressed { background-color: #1e90ff; }"
        )

         # Layout for Label and Input inside of Grid Layout
        label_input_layout = QHBoxLayout()
        label_input_layout.addWidget(self.mainWindow.username_label)
        label_input_layout.addWidget(self.mainWindow.username_input)

        
        label_input_layout2 = QHBoxLayout()
        label_input_layout2.addWidget(self.mainWindow.email_label)
        label_input_layout2.addWidget(self.mainWindow.email_input)
        
        select_box_layout = QHBoxLayout()
        select_box_layout.addWidget(self.mainWindow.color_choice_label)
        select_box_layout.addWidget(self.mainWindow.color_choice)
        self.mainWindow.color_choice.setMinimumWidth(455)
        
        spacer_layout = QHBoxLayout()
        spacer = QSpacerItem(QSpacerItem(40, 60, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        spacer_layout.addSpacerItem(spacer)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.mainWindow.back_button)
        button_layout.addWidget(self.mainWindow.save_button)
        button_layout.addWidget(self.mainWindow.delete_profile_button)
        
        #back_button_layout = QHBoxLayout()
        #back_button_layout.addWidget(self.mainWindow.back_button)

        # Set Layout
        grid_layout.addLayout(label_input_layout, 0, 0, 1, 1)
        grid_layout.addLayout(label_input_layout2, 1, 0, 1, 1)
        grid_layout.addLayout(select_box_layout, 2, 0, 1, 1)
        grid_layout.addLayout(spacer_layout, 3, 0, 1, 1)
        grid_layout.addLayout(button_layout, 4, 0, 1, 1)
        

        #Add Button Functions
        self.mainWindow.save_button.clicked.connect(self.save)
        self.mainWindow.back_button.clicked.connect(self.back)
        self.mainWindow.delete_profile_button.clicked.connect(self.delete_profile)

        self.__network.addNetworkEventHandler(NetworkEvent.PROFILE_READ, self.__onProfileReadSuccess)
        self.__network.addNetworkEventHandler(NetworkEvent.PROFILE_UPDATE, self.__onProfileUpdateSuccess)
        self.__network.api.requestProfile()


    def __onProfileReadSuccess(self, event:NetworkEventObject):
        self.mainWindow.username_input.setText(event.eventData['username'])
        self.mainWindow.email_input.setText(event.eventData['email'])
        pass

    def __onProfileUpdateSuccess(self, event:NetworkEventObject):
        self.__network.api.requestProfile()
        pass

    # Register User for Blokus Game
    def save(self):
        username = self.mainWindow.username_input.text()
        email = self.mainWindow.email_input.text()
        selected_color = self.mainWindow.color_choice.currentText()
        self.__network.api.updateProfile(username, email)
        pass

    #Add Back Button Function
    def back(self):
        from lobby.lobbymenu import LobbyMenu
        self.lobbymenu = LobbyMenu(self.mainWindow, self.__network)
        self.lobbymenu.lobbyMenuFrame()
        pass

    def delete_profile(self):
        from account.deleteprofile import DeleteProfile
        self.deleteProfile = DeleteProfile(self.mainWindow, self.__network)
        self.deleteProfile.deleteProfileFrame()
        pass