# Imports
from __future__ import annotations
import os
import sys
import threading
import typing
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from qt6networkadapter import PyQt6_Networkadapter

from menu import Menu
from settings import Settings
from how_to_play import HowToPlay
from network.serverapi import NetworkEventObject, ServerApi, NetworkEvent
from network import constants as NetworkConst


##################################################
## Author: Kevin Wagner
##################################################


# Main Window Class
class BlokusUtility(QMainWindow):
    def __init__(self):
        super().__init__()

        self.network = PyQt6_Networkadapter(self, 'localhost', 6666)    # WARNING hardcoded values
        self.network.addNetworkEventHandler(NetworkEvent.SYSMESSAGE, self.__on_sys_message)

        self.initUI()
        self.settings = Settings(self)
        self.settings.initBackgroundMusic()

        self.menu = Menu(self, self.network)
        return
    
    def __on_sys_message(self, event:NetworkEventObject):
        self.showAlert(event.eventData["message"], timer_seconds=4)
        return
    
    def showAlert(self, message, timer_seconds=2):
        self.alertWidget.showAlert(message, timer_seconds)
        return

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.network.stop()
        a0.accept()
        return
        
    # Initilize Primary Screen
    def initUI(self):
        self.setWindowTitle('Blokus Game')
        self.primary_screen = QApplication.primaryScreen()
        self.setMinimumSize(1100, 800)
        self.screen_geometry = self.primary_screen.availableGeometry()
        self.setGeometry(self.screen_geometry)
        self._createMenuBar()
        self.alertWidget = AlertWidget(self)
        return

        
    
    # Creation Top Menu Bar of Primary Screen
    def _createMenuBar(self):
        menuBar = self.menuBar()
        menu = QMenu("&Menu", self)
        menuBar.addMenu(menu)
        # settings_action = QAction("Settings", self)
        self.leave_lobby_action = QAction("Leave Lobby", self)
        self.leave_lobby_action.setVisible(False)

        self.leave_game_action = QAction("Leave Game", self)
        self.leave_game_action.setVisible(False)

        self.lobby_create_action = QAction("Create Lobby", self)
        self.lobby_create_action.setVisible(False)

        self.join_lobby_action = QAction("Join Lobby", self)
        self.join_lobby_action.setVisible(False)
        
        self.settings = QAction("Settings", self)
        self.settings.setShortcut('Ctrl+S')
        self.settings.triggered.connect(self.settingsFrame)

        self.how_to_play_action = QAction("How to Play", self)
        self.how_to_play_action.setShortcut('Ctrl+H')
        self.how_to_play_action.triggered.connect(self.how_to_playFrame)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut('Ctrl+Q')
        # settings_action.triggered.connect(self.settingsFrame)
        exit_action.triggered.connect(self.close)
        # menu.addAction(settings_action)
        menu.addAction(self.how_to_play_action)
        menu.addAction(self.lobby_create_action)
        menu.addAction(self.join_lobby_action)
        menu.addAction(self.leave_lobby_action)
        menu.addAction(self.leave_game_action)
        menu.addSeparator()
        menu.addAction(self.settings)
        menu.addSeparator()
        menu.addAction(exit_action)
        font = menu.font()
        font.setPointSize(10)
        menu.setFont(font)

    # Integration of Settings Popup and Background Music
    def settingsFrame(self):
        self.settings.settingsFrame()

    pass

    def how_to_playFrame(self):
        self.how_to_play = HowToPlay(self)
        self.how_to_play.how_to_playFrame()
    
    pass


class AlertWidget(QWidget):
    def __init__(self, parent:QWidget=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.hide()

        self.setGeometry(self.parent().geometry().x() + int(self.parent().geometry().width()*0.1),
                                    self.parent().geometry().y() + 50,
                                    int(self.parent().geometry().width() * 0.8),
                                    50)

        return
    
    def showAlert(self, message, timer_seconds=3):
        alertBox = AlertBoxWidget(message, parent=self)
        self.layout.addWidget(alertBox)

        # grow the widget to fit multiple alerts
        new_height = self.size().height() + 100
        self.resize(self.size().width(), new_height)

        if self.layout.count() == 1:
            self.show()

        # setup the timer for closing the alert
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self.__on_timeout(alertBox))
        timer.start(1000 * timer_seconds)  # Time in milliseconds
        self.raise_()   # this enshures the alert widget is on top of all other widgets
        return
    

    def __on_timeout(self, alertBox:AlertBoxWidget) -> None:
        alertBox.close()
        self.layout.removeWidget(alertBox)

        # shrink the widget
        new_height = self.size().height() - 100
        self.resize(self.size().width(), new_height)

        if self.layout.count() == 0:
            self.hide()
        return

class AlertBoxWidget(QWidget):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.container = QWidget(self)
        self.container.setStyleSheet("background-color: rgba(100, 200, 255, 128); border-radius: 10px; font-weight: bold; border: 2px solid black;")
        self.container.layout = QVBoxLayout(self.container)


        self.label = QLabel(f'{message}')
        self.label.setStyleSheet("background-color: rgba(0,0,0,0); border: 0px;")
        self.container.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

            
        layout = QVBoxLayout()
        layout.addWidget(self.container)
        self.setLayout(layout)
        #self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Resize the widget to fill the entire available space
        if parent is not None:
            self.resize(parent.size())
        return


def excepthook(type, value, traceback):
        print(f'Unhandled Exception:\n{str(value)} \n {traceback.format_exc()}') # crash intendet gives more info ... 

sys.excepthook = excepthook

# Initilize Main Window (Blokus Utility)
if __name__ == '__main__':

    app = QApplication(sys.argv)
    font = app.font()
    font.setPointSize(16)
    app.setFont(font)
    mainWindow = BlokusUtility()
    mainWindow.showMaximized()
    sys.exit(app.exec())