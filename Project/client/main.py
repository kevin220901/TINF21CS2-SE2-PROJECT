# Imports
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from menu import Menu
from settings import Settings


##################################################
## Author: Kevin Wagner
##################################################


# Main Window Class
class BlokusUtility(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.settings = Settings(self)
        self.settings.initBackgroundMusic()
        self.menu = Menu(self)
        self.menu.menuFrame()
        
    # Initilize Primary Screen
    def initUI(self):
        self.setWindowTitle('Blokus Game')
        self.primary_screen = QApplication.primaryScreen()
        self.setMinimumSize(1100, 800)
        self.screen_geometry = self.primary_screen.availableGeometry()
        self.setGeometry(self.screen_geometry)
        self._createMenuBar()
        
    
    # Creation Top Menu Bar of Primary Screen
    def _createMenuBar(self):
        menuBar = self.menuBar()
        menu = QMenu("&Menu", self)
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

    # Integration of Settings Popup and Background Music
    def settingsFrame(self):
        self.settings.settingsFrame()

    



# Initilize Main Window (Blokus Utility)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = app.font()
    font.setPointSize(16)
    app.setFont(font)
    mainWindow = BlokusUtility()
    mainWindow.showMaximized()
    sys.exit(app.exec())
