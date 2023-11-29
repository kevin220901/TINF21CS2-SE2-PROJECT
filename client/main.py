import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class BlokusUtility(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.menu = Menu(self)
        self.menu.menuFrame()

    def initUI(self):
        self.setWindowTitle('Blokus Game')
        self.primary_screen = QApplication.primaryScreen()
        self.setMinimumSize(1100, 800)
        self.screen_geometry = self.primary_screen.availableGeometry()
        self.setGeometry(self.screen_geometry)
        self._createMenuBar()

    def _createMenuBar(self):
        menuBar = self.menuBar()
        menu = QMenu("&Menü", self)
        menuBar.addMenu(menu)
        settings_action = QAction("Settings", self)
        exit_action = QAction("Exit", self)
        exit_action.setShortcut('Ctrl+Q')
        settings_action.triggered.connect(self.settingsFrame)
        exit_action.triggered.connect(self.close)
        menu.addAction(settings_action)
        menu.addSeparator()
        menu.addAction(exit_action)
        font = menu.font()
        font.setPointSize(10)
        menu.setFont(font)

    def settingsFrame(self):
        print("Launch Settings")

    def loginFrame(self):
        # Your loginFrame method content goes here
        pass

    def test(self):
        # Your test method content goes here
        pass


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

    def login(self):
        self.mainWindow.menuFrame.deleteLater()

    def exit(self):
        self.mainWindow.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = app.font()
    font.setPointSize(16)
    app.setFont(font)
    mainWindow = BlokusUtility()
    mainWindow.showMaximized()
    sys.exit(app.exec())
