from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class Login:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def loginFrame(self):
        login_widget = QWidget()
        login_widget.setStyleSheet("background-color: #E0E0E0; border: 2px solid black;")
        login_widget.setFixedSize(500, 200)

        grid_layout = QGridLayout(login_widget)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mainWindow.central_layout.addWidget(login_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        self.mainWindow.username_label = QLabel("Username :")
        self.mainWindow.password_label = QLabel("Password  :")
        self.mainWindow.username_input = QLineEdit()
        self.mainWindow.password_input = QLineEdit()
        self.mainWindow.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.mainWindow.login_button = QPushButton("Login")
        self.mainWindow.login_button.setStyleSheet(
            "QPushButton:hover { background-color: #70a8ff; }"
            "QPushButton:pressed { background-color: #1e90ff; }"
        )

        label_input_layout = QHBoxLayout()
        label_input_layout.addWidget(self.mainWindow.username_label)
        label_input_layout.addWidget(self.mainWindow.username_input)

        label_input_layout2 = QHBoxLayout()
        label_input_layout2.addWidget(self.mainWindow.password_label)
        label_input_layout2.addWidget(self.mainWindow.password_input)

        login_button_layout = QHBoxLayout()
        login_button_layout.addWidget(self.mainWindow.login_button)

        
        grid_layout.addLayout(label_input_layout, 0, 0, 1, 1)
        grid_layout.addLayout(label_input_layout2, 1, 0, 1, 1)
        grid_layout.addLayout(login_button_layout, 2, 0, 1, 1)

        self.mainWindow.login_button.clicked.connect(self.check_login)

    def check_login(self):
        username = self.mainWindow.username_input.text()
        password = self.mainWindow.password_input.text()
        print("Username:", username)
        print("Password:", password)