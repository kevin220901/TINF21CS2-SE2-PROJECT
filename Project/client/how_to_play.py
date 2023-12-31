from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

##################################################
## Author: Kevin Wagner
##################################################

class HowToPlay:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def how_to_playFrame(self):
        popup = QDialog()
        popup.setWindowTitle("How To Play")
        popup.setFixedSize(600, 600)
        layout = QGridLayout()
        popup.setModal(True)
        image_label = QLabel()
        pixmap = QPixmap("./assets/how_to_play.png")
        if pixmap.isNull():
            failed_label = QLabel("Failed to load image")
            layout.addWidget(failed_label)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center alignment
        else:
            pixmap = pixmap.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio)
            image_label.setPixmap(pixmap)
            layout.addWidget(image_label)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center alignment
        popup.setLayout(layout)
        popup.exec()
