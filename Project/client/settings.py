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

        # Volume Label
        volumeLabel = QLabel("Music Volume")
        volumeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        volumeLabel.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(volumeLabel, 0, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)  # Add the volume label to the layout, spanning 3 columns and centered

        # Volume Slider
        volumeSlider = QSlider(Qt.Orientation.Horizontal)
        volumeSlider.setMinimum(0)
        volumeSlider.setMaximum(100)
        volumeSlider.setValue(100)
        volumeSlider.setTickInterval(10)
        volumeSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        volumeSlider.setStyleSheet("QSlider::groove:horizontal {"
                                   "border: 1px solid #999999;"
                                   "height: 8px;"
                                   "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #B1B1B1, stop:1 #c4c4c4);"
                                   "margin: 2px 0;"
                                   "}"
                                   "QSlider::handle:horizontal {"
                                   "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b5b5b5, stop:1 #8f8f8f);"
                                   "border: 1px solid #5c5c5c;"
                                   "width: 18px;"
                                   "margin: -2px 0;"
                                   "border-radius: 3px;"
                                   "}")
        volumeSlider.setFixedWidth(200)  # Set the width of the volume slider
        volumeSlider.valueChanged.connect(self.setVolume)
        layout.addWidget(volumeSlider, 1, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)  # Add the volume slider to the layout, spanning 3 columns and centered

        # Add vertical spacer item
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacerItem, 2, 0, 1, 3)

        popup.setLayout(layout)
        popup.exec()

    def setVolume(self, volume):
        self.audioOutput.setVolume(volume / 100)

    def initBackgroundMusic(self):
        self.mediaPlayer = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.mediaPlayer.setSource(QUrl.fromLocalFile("never_gonna_give_you_up.mp3"))
        self.audioOutput.setVolume(1)
        self.mediaPlayer.mediaStatusChanged.connect(self.loopMusic)
        self.mediaPlayer.play()

    def loopMusic(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.mediaPlayer.setPosition(0)
            self.mediaPlayer.play()