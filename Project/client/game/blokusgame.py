import typing
from PyQt6 import QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent
import numpy as np

from qt6networkadapter import PyQt6_Networkadapter


##################################################
## Author: Kai Pistol
##################################################

class BlokusGame:
    def __init__(self, mainWindow, network: PyQt6_Networkadapter, gameInfo: dict):
        self.mainWindow = mainWindow
        self.__network = network
        self.selectedPiece: GamePiece = None
        self.ghostPiece: GamePiece = None
        self.gameInfo = gameInfo
        return

    def gameFrame(self):
        self.game = QWidget()
        self.game.layout = QHBoxLayout(self.game)
        self.game.setStyleSheet("background-color: #E0E0E0; border: 2px solid black;")

        self.mainWindow.central_layout.addWidget(self.game)

        self.__init_piece_repositories()
        self.__init_game_field()
        self.__init_chat()

        self.display_pieces(self.gameInfo)

        pass

    def display_pieces(self, gameInfo: dict):
        # Define the shapes of the Blokus pieces
        # piece_shapes = [
        #     np.array([[1]]),  # Single square
        #     np.array([[1, 1]]),  # Line of two squares
        #     np.array([[1, 1, 1]]),  # Line of three squares
        #     # ... add more shapes as needed ...
        # ]

        # Create and display the pieces for each player
        for i, scene in enumerate(self.piecesScenes):
            playerInfo = self.gameInfo['players'].get(f'{i+1}')
            if playerInfo is None: continue
            for j, shape in enumerate(playerInfo['pieces']):
                piece = GamePiece(self, np.array(shape), j * 30, 0, 20, 20)
                scene.addItem(piece)

    def __init_piece_repositories(self) -> None:
        self.piecesLayout = QVBoxLayout()

        # Create four widgets for the game pieces
        self.piecesWidgets = [QWidget() for _ in range(4)]
        self.piecesLayouts = [QVBoxLayout(widget) for widget in self.piecesWidgets]

        # Create four QGraphicsScenes and QGraphicsViews for the game pieces
        self.piecesScenes = [QGraphicsScene() for _ in range(4)]
        self.piecesViews = [QGraphicsView(scene) for scene in self.piecesScenes]

        # Add the QGraphicsViews and player name labels to the widgets' layouts
        for i, (layout, view) in enumerate(zip(self.piecesLayouts, self.piecesViews)):
            playerInfo = self.gameInfo['players'].get(f'{i+1}')
            if playerInfo is None: continue
            playerNameLabel = QLabel(playerInfo['playerName'])
            layout.addWidget(playerNameLabel)
            layout.addWidget(view)

        # Add the widgets to the main window's layout
        for widget in self.piecesWidgets:
            self.piecesLayout.addWidget(widget)

        self.game.layout.addLayout(self.piecesLayout)

        return

    def __init_game_field(self) -> None:
        self.scene = GameScene(self)
        self.view = GameView(self.scene, self)
        self.view.setMouseTracking(True)
        # Disable scroll bars
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # Add the QGraphicsView to the main window's layout
        self.game.layout.addWidget(self.view, alignment=Qt.AlignmentFlag.AlignCenter)

        self.grid = []
        for i in range(20):
            row = []
            for j in range(20):
                item = GameFieldElement(self, i * 20, j * 20, 20, 20, QColor(255, 255, 255))
                self.scene.addItem(item)
                row.append(item)
            self.grid.append(row)

        return

    def __init_chat(self):
        self.chatWidget = QWidget()
        self.chatWidget.layout = QVBoxLayout(self.chatWidget)

        self.chatTitleLabel = QLabel("Chat")
        self.chatWidget.layout.addWidget(self.chatTitleLabel)

        self.chat_output = QTextEdit()
        self.chat_output.setReadOnly(True)

        self.chat_input = QLineEdit()
        self.chat_input_layout = QHBoxLayout()
        self.chat_input.setPlaceholderText("Enter Message")

        self.chat_send_button = QPushButton('Send')
        # self.chat_send_button.setFixedSize(150, 40)
        self.chat_send_button.setStyleSheet(
            "QPushButton:hover { background-color: #70a8ff; }"
            "QPushButton:pressed { background-color: #1e90ff; }"
        )

        self.chat_input_layout.addWidget(self.chat_input)
        self.chat_input_layout.addWidget(self.chat_send_button)

        self.chatWidget.layout.addWidget(self.chat_output)
        self.chatWidget.layout.addLayout(self.chat_input_layout)

        self.game.layout.addWidget(self.chatWidget)
        return

    def placeSelectedPiece(self, piece, ghost, pos: QPointF):
        if piece is not None:
            if piece.isPlaced: return
            grid_x = int(pos.x() // 20) * 20
            grid_y = int(pos.y() // 20) * 20

            # Place the selected piece at this location
            piece.setPos(grid_x, grid_y)

            for item in piece.childItems():
                item.setPen(QPen(QColor(0, 0, 0), 0))  # Remove border

            del self.selectedPiece
            self.selectedPiece = None  # Deselect the piece

            # Remove the ghost piece
            if ghost is not None:
                self.scene.removeItem(ghost)
                del ghost
                ghost = None

            # Add the piece to the game grid scene
            piece.isPlaced = True
            self.scene.addItem(piece)
        return


class GameFieldElement(QGraphicsRectItem):
    def __init__(self, game, x, y, w, h, color):
        super().__init__(x, y, w, h)
        self.setBrush(QBrush(color))
        self.game = game
        return


class GamePiece(QGraphicsItemGroup):
    def __init__(self, game, shape, x, y, width, height, parent=None):
        super().__init__(parent)

        self.game = game
        self.shape = shape
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isPlaced = False

        # Create a QGraphicsRectItem for each 1 in the shape
        for i in range(shape.shape[0]):
            for j in range(shape.shape[1]):
                if shape[i][j] == 1:
                    rect = QGraphicsRectItem(i * width, j * height, width, height)
                    rect.setBrush(QBrush(QColor(255, 0, 0)))  # Set color to red
                    self.addToGroup(rect)

        # Set the position of the group
        self.setPos(x, y)
        return

    def mousePressEvent(self, event):
        if self.isPlaced: return
        if self.game.selectedPiece is self:
            # Deselect this piece
            for item in self.childItems():
                item.setPen(QPen(QColor(0, 0, 0), 0))  # Remove border

            # Remove the ghost piece
            if self.game.ghostPiece is not None:
                self.game.scene.removeItem(self.game.ghostPiece)
                self.game.ghostPiece = None

            self.game.selectedPiece = None
        else:
            # Deselect the previously selected piece
            if self.game.selectedPiece is not None:
                for item in self.game.selectedPiece.childItems():
                    item.setPen(QPen(QColor(0, 0, 0), 0))  # Remove border

                # Remove the previous ghost piece
                if self.game.ghostPiece is not None:
                    self.game.scene.removeItem(self.game.ghostPiece)
                    self.game.ghostPiece = None

            # Select this piece
            self.game.selectedPiece = self
            if self.game.ghostPiece is None:
                self.game.ghostPiece = GhostPiece(self.game, self.shape, self.x, self.y, self.width, self.height)
                self.game.scene.addItem(self.game.ghostPiece)

                for item in self.childItems():
                    item.setPen(QPen(QColor(0, 0, 255), 2))  # Add blue border
        return

    def clone(self):
        # Create a new GamePiece with the same properties
        clone = GamePiece(self.game, self.shape, self.x, self.y, self.width, self.height)
        return clone


class GameScene(QGraphicsScene):
    def __init__(self, game: BlokusGame, parent=None):
        super().__init__(parent)
        self.game = game

    def mouseMoveEvent(self, event):
        if self.game.ghostPiece is not None:
            pos = event.scenePos()
            if self.sceneRect().contains(pos):
                # Move the ghost piece to the mouse position
                grid_x = int(pos.x() // 20) * 20
                grid_y = int(pos.y() // 20) * 20

                self.game.ghostPiece.setPos(grid_x, grid_y)
        return

    def mousePressEvent(self, event):
        if self.game.ghostPiece:
            # Place the piece at the current position of the ghost piece
            self.game.placeSelectedPiece(self.game.selectedPiece,
                                         self.game.ghostPiece,
                                         event.scenePos())
        if self.game.selectedPiece is not None:
            self.game.selectedPiece.isPlaced = True
        return super().mousePressEvent(event)


class GameView(QGraphicsView):
    def __init__(self, scene, game, parent=None):
        super().__init__(scene, parent)
        self.game = game

    def leaveEvent(self, event):
        if self.game.ghostPiece is not None:
            self.game.ghostPiece.setVisible(False)  # Hide the ghost piece
        return super().leaveEvent(event)

    def enterEvent(self, event: QEnterEvent | None) -> None:
        if self.game.selectedPiece is not None and self.game.ghostPiece is not None:
            self.game.ghostPiece.setVisible(True)  # Show the ghost piece
        return super().enterEvent(event)


class GhostPiece(GamePiece):
    def __init__(self, game, shape, x, y, width, height, parent=None):
        super().__init__(game, shape, x, y, width, height, parent)
        self.setOpacity(0.5)  # Make the ghost piece semi-transparent
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setVisible(False)

        def mousePressEvent(self, event):
            return

        def mouseMoveEvent(self, event):
            return

        return
