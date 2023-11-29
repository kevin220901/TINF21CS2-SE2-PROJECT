import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from menu import Menu
from settings import Settings

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
        self.settings = Settings(self)
        self.settings.settingsFrame()

    








if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = app.font()
    font.setPointSize(16)
    app.setFont(font)
    mainWindow = BlokusUtility()
    mainWindow.showMaximized()
    sys.exit(app.exec())
