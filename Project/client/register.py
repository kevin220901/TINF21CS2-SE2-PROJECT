from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class Register:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def registerFrame(self):
        register_widget = QWidget()
        register_widget.setStyleSheet("background-color: #E0E0E0; border: 2px solid black;")
        register_widget.setFixedSize(700, 300)

        grid_layout = QGridLayout(register_widget)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mainWindow.central_layout.addWidget(register_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        self.mainWindow.username_label = QLabel("Username                   :")
        self.mainWindow.password_label = QLabel("Password                    :")
        self.mainWindow.password_confirm_label = QLabel("Password bestätigen  :")
        self.mainWindow.email_label = QLabel("E-Mail                         :")
        self.mainWindow.username_input = QLineEdit()
        self.mainWindow.password_input = QLineEdit()
        self.mainWindow.password_confirm_input = QLineEdit()
        self.mainWindow.email_input = QLineEdit()
        self.mainWindow.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.mainWindow.password_confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.mainWindow.register_button = QPushButton("Registrieren")
        self.mainWindow.register_button.setStyleSheet(
            "QPushButton:hover { background-color: #70a8ff; }"
            "QPushButton:pressed { background-color: #1e90ff; }"
        )
        self.mainWindow.back_button = QPushButton("Zurück")
        self.mainWindow.back_button.setStyleSheet(
            "QPushButton:hover { background-color: #70a8ff; }"
            "QPushButton:pressed { background-color: #1e90ff; }"
        )

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

        register_button_layout = QHBoxLayout()
        register_button_layout.addWidget(self.mainWindow.register_button)
        
        back_button_layout = QHBoxLayout()
        back_button_layout.addWidget(self.mainWindow.back_button)

        
        grid_layout.addLayout(label_input_layout, 0, 0, 1, 1)
        grid_layout.addLayout(label_input_layout2, 1, 0, 1, 1)
        grid_layout.addLayout(label_input_layout3, 2, 0, 1, 1)
        grid_layout.addLayout(label_input_layout4, 3, 0, 1, 1)
        grid_layout.addLayout(register_button_layout, 4, 0, 1, 1)
        grid_layout.addLayout(back_button_layout, 5, 0, 1, 1)

        self.mainWindow.register_button.clicked.connect(self.register)
        self.mainWindow.back_button.clicked.connect(self.back)

    def register(self):
        username = self.mainWindow.username_input.text()
        password = self.mainWindow.password_input.text()
        password_confirm = self.mainWindow.password_confirm_input.text()
        email = self.mainWindow.email_input.text()
        print("Username:", username)
        print("Password:", password)
        print("Username:", password_confirm)
        print("E-Mail:", email)
    
    def back(self):
        from menu import Menu
        self.menu = Menu(self.mainWindow)
        self.menu.menuFrame()