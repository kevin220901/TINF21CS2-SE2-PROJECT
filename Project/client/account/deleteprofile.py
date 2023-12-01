from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *

##################################################
## Author: Kevin Wagner
##################################################

class DeleteProfile:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

    def deleteProfileFrame(self):
        popup = QDialog()
        popup.setWindowTitle("Delete Profile")
        popup.setFixedSize(600, 250)
        layout = QGridLayout()
        popup.setModal(True)
        layout = QVBoxLayout()

        # Label
        label = QLabel("Are you sure you want to delete this profile?")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        h_layout = QHBoxLayout()
        button_cancel = QPushButton("Cancel")
        h_layout.addWidget(button_cancel)
        button_delete = QPushButton("Delete")
        h_layout.addWidget(button_delete)
        button_cancel.clicked.connect(self.delete_profile)
        button_cancel.clicked.connect(popup.close)
        layout.addLayout(h_layout)
        popup.setLayout(layout)
        popup.exec()
    
    def delete_profile(self):
        pass