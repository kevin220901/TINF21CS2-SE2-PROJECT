import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *



class BlokusUtility(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.menuFrame()
        #time.sleep(10)
        
        


    def initUI(self):
        self.setWindowTitle('Blokus Game')
        self.primary_screen = QApplication.primaryScreen()
        self.setMinimumSize(1100, 800)
        self.screen_geometry = self.primary_screen.availableGeometry()
        self.setGeometry(self.screen_geometry)
        self._createMenuBar()
    
    def _createMenuBar(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
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
        font.setPointSize(10)  # Setze die Schriftgröße
        menu.setFont(font)
    
    def settingsFrame(self):
        print("Launch Settings")
        

    def menuFrame(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.menuFrame = QFrame(self.central_widget)
        self.menuFrame.setStyleSheet("QFrame { background-color: #E0E0E0; border: 2px solid black; }")
        self.layout = QGridLayout(self.menuFrame)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.menuFrame)
        self.central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.central_widget.setLayout(self.central_layout)
        self.button = QPushButton("Button1")  
        self.button.setMinimumSize(400, 100)  
        self.button.setMaximumSize(600, 400)
        self.button.clicked.connect(self.test)
        self.layout.addWidget(self.button)
        self.button2 = QPushButton("Button2")
        self.button2.setMinimumSize(400, 100)  
        self.button2.setMaximumSize(600, 400)
        self.layout.addWidget(self.button2)
    
    def loginFrame(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.loginFrame = QFrame(self.central_widget)
        self.loginFrame.setStyleSheet("QFrame { background-color: #E0E0E0; border: 2px solid black; }")
        self.layout = QGridLayout(self.loginFrame)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.loginFrame)
        self.central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.central_widget.setLayout(self.central_layout)
        self.button = QPushButton("Login")  
        self.button.setMinimumSize(400, 100)  
        self.button.setMaximumSize(600, 400)
        self.button.clicked.connect(self.test)
        self.layout.addWidget(self.button)
        self.button2 = QPushButton("Login")
        self.button2.setMinimumSize(400, 100)  
        self.button2.setMaximumSize(600, 400)
        self.layout.addWidget(self.button2)
        
    def test(self):
        self.menuFrame.deleteLater()
        QTimer.singleShot(3000, self.loginFrame)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = BlokusUtility()
    mainWindow.showMaximized()
    sys.exit(app.exec())
