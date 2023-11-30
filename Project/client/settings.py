from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *

##################################################
## Author: Kevin Wagner
##################################################

class Settings:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def settingsFrame(self):
        popup = QDialog()
        popup.setWindowTitle("Settings")
        popup.setFixedSize(800, 500)
        layout = QGridLayout()
        popup.setModal(True)
        popup.exec()
        
        
    
    def initBackgroundMusic(self):
        self.mediaPlayer = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.mediaPlayer.setSource(QUrl.fromLocalFile("jinglebells.mp3"))
        self.audioOutput.setVolume(1)
        self.mediaPlayer.mediaStatusChanged.connect(self.loopMusic)
        self.mediaPlayer.play()
    
    def loopMusic(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.mediaPlayer.setPosition(0)
            self.mediaPlayer.play()