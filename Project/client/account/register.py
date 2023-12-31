# Imports
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from network.networkevent import NetworkEvent

from qt6networkadapter import PyQt6_Networkadapter

##################################################
## Author: Kevin Wagner
##################################################


# Register Class for User Registration
class Register:
    def __init__(self, mainWindow, network: PyQt6_Networkadapter):
        self.__network = network
        self.mainWindow = mainWindow

        self.__init_ui()
        self.__registerNetworkEvents()
        return

    # Initilize Register Frame and Widget
    def __init_ui(self):
        register_widget = QWidget()
        register_widget.setStyleSheet("background-color: #E0E0E0; border: 2px solid black;")
        register_widget.setFixedSize(700, 300)

        # Add Grid Layout to Widget
        grid_layout = QGridLayout(register_widget)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWindow.central_layout.addWidget(register_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add Labels and Input for User Registration
        self.mainWindow.username_label = QLabel("Username                   :")
        self.mainWindow.password_label = QLabel("Password                    :")
        self.mainWindow.password_confirm_label = QLabel("Confirm Password      :")
        self.mainWindow.email_label = QLabel("E-Mail                         :")
        self.mainWindow.username_input = QLineEdit()
        self.mainWindow.password_input = QLineEdit()
        self.mainWindow.password_confirm_input = QLineEdit()
        self.mainWindow.email_input = QLineEdit()
        
        # Make Password Input unreadable
        self.mainWindow.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.mainWindow.password_confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Add Button for Registration Function
        self.mainWindow.register_button = QPushButton("Register")
        self.mainWindow.register_button.setStyleSheet(
            "QPushButton:hover { background-color: #70a8ff; }"
            "QPushButton:pressed { background-color: #1e90ff; }"
        )
        
        # Add Button for Back Function
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
        
        label_input_layout3 = QHBoxLayout()
        label_input_layout3.addWidget(self.mainWindow.password_confirm_label)
        label_input_layout3.addWidget(self.mainWindow.password_confirm_input)
        
        label_input_layout4 = QHBoxLayout()
        label_input_layout4.addWidget(self.mainWindow.email_label)
        label_input_layout4.addWidget(self.mainWindow.email_input)
        
        spacer_layout = QHBoxLayout()
        spacer = QSpacerItem(QSpacerItem(40, 30, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        spacer_layout.addSpacerItem(spacer)


        button_layout = QHBoxLayout()
        button_layout.addWidget(self.mainWindow.back_button)
        button_layout.addWidget(self.mainWindow.register_button)
        

        # Set Layout
        grid_layout.addLayout(label_input_layout, 0, 0, 1, 1)
        grid_layout.addLayout(label_input_layout2, 1, 0, 1, 1)
        grid_layout.addLayout(label_input_layout3, 2, 0, 1, 1)
        grid_layout.addLayout(label_input_layout4, 3, 0, 1, 1)
        grid_layout.addLayout(spacer_layout, 4, 0, 1, 1)
        grid_layout.addLayout(button_layout, 5, 0, 1, 1)

        #Add Button Functions
        self.mainWindow.register_button.clicked.connect(self.register)
        self.mainWindow.back_button.clicked.connect(self.back)
        return
    

    # Register User for Blokus Game
    #TODO Implementierung Register Function
    def register(self):
        username = self.mainWindow.username_input.text()
        password = self.mainWindow.password_input.text()
        password_confirm = self.mainWindow.password_confirm_input.text()
        email = self.mainWindow.email_input.text()

        #TODO: validate password and email

        self.__network.api.register(username, password, email)
        pass

    def __registerNetworkEvents(self):
        self.__network.addNetworkEventHandler(NetworkEvent.REGISTRATION_SUCCESS, self.__on_registration_successfull)
        return
    
    def __unregisterNetworkEvents(self):
        self.__network.removeNetworkEventHandler(NetworkEvent.REGISTRATION_SUCCESS, self.__on_registration_successfull)
        return

    def __on_registration_successfull(self, event):
        self.mainWindow.showAlert('Registration successful')
        from menu import Menu
        self.menu = Menu(self.mainWindow, self.__network)
        pass
    
    #Add Back Button Function
    def back(self):
        from menu import Menu
        self.menu = Menu(self.mainWindow, self.__network)
        pass