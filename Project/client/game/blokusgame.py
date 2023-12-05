from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *
import pygame

from qt6networkadapter import PyQt6_Networkadapter

##################################################
## Author: Kevin Wagner
##################################################
class BlokusGame:
    def __init__(self, mainWindow, network:PyQt6_Networkadapter):
        self.mainWindow = mainWindow
        self.__network = network


    def gameFrame(self):
        
        self.game = QWidget()

        self.mainWindow.central_layout.addWidget(self.game, alignment=Qt.AlignmentFlag.AlignCenter)
        return 