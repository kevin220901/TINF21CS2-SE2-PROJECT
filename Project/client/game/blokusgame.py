import typing
from PyQt6 import QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent
import numpy as np
from network.networkevent import NetworkEvent
from network.serverapi import NetworkEventObject

from qt6networkadapter import PyQt6_Networkadapter

TILE_SIZE = 21

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
        self.blokus_widget = QWidget()
        self.blokus_widget.layout = QHBoxLayout(self.blokus_widget)
        self.blokus_widget.setStyleSheet("background-color: #E0E0E0; border: 2px solid black;")

        self.left_layout = QVBoxLayout()
        self.central_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.__init_piece_repositoryA()
        self.__init_piece_repositoryB()
        self.blokus_widget.layout.addLayout(self.left_layout)

        self.__init_game_field()
        self.__init_chat()
        self.blokus_widget.layout.addLayout(self.central_layout)
        
        self.__init_piece_repositoryC()
        self.__init_piece_repositoryD()
        self.blokus_widget.layout.addLayout(self.right_layout)

        self.piecesScenes = [self.pieceRepositorySceneA, self.pieceRepositorySceneB, self.pieceRepositorySceneC, self.pieceRepositorySceneD]

        self.mainWindow.central_layout.addWidget(self.blokus_widget)

        self.display_pieces(self.gameInfo)
        
        #add network event handler
        self.__network.addNetworkEventHandler(NetworkEvent.MESSAGE, self.__on_message)
        self.__network.addNetworkEventHandler(NetworkEvent.GAME_UPDATE, self.__on_game_update)
        #add button event handler
        self.chat_send_button.clicked.connect(self.__on_send_clicked)
        ##send message on enter
        self.chat_input.returnPressed.connect(self.chat_send_button.click)
        return

    def __init_chat(self):
        self.chat = QWidget()
        self.chat_layout = QVBoxLayout(self.chat)
        
        self.chat_output = QTextEdit()
        self.chat_output.setReadOnly(True)

        self.chat_input = QLineEdit()
        self.chat_input_layout = QHBoxLayout()
        self.chat_input.setPlaceholderText("Enter Message")

        self.chat_send_button = QPushButton('Send')
        #self.chat_send_button.setFixedSize(150, 40)
        self.chat_send_button.setStyleSheet(
                "QPushButton:hover { background-color: #70a8ff; }"
                "QPushButton:pressed { background-color: #1e90ff; }"
            )
        
        self.chat_input_layout.addWidget(self.chat_input)
        self.chat_input_layout.addWidget(self.chat_send_button)
        
        self.chat_layout.addWidget(self.chat_output)
        self.chat_layout.addLayout(self.chat_input_layout)


        self.central_layout.addWidget(self.chat)
        pass


    def __on_send_clicked(self):
        message = self.chat_input.text()
        self.chat_input.clear()
        self.__network.api.sendMessage(message)
        return
    
    def __on_message(self, event:NetworkEventObject):
        self.chat_output.append(f'[{event.eventData["from"]}]: {event.eventData["message"]}')
        return
    
    def __on_game_update(self, event:NetworkEventObject):
        self.gameInfo = event.eventData
        # TODO: update game field
        # TODO: update piece repository
        self.display_pieces(self.gameInfo)
        return

    def display_pieces(self, gameInfo: dict):
        # Create and display the pieces for each player
        for i, scene in enumerate(self.piecesScenes):
            playerInfo = self.gameInfo['players'].get(f'{i+1}')
            if playerInfo is None: continue
            for j, shape in enumerate(playerInfo['pieces']):
                piece = GamePiece(self, np.array(shape), j * 30, 0, 20, 20)
                scene.addItem(piece)
        return
    
    def display_player_info(self, gameInfo: dict):
        #TODO: display player info
        return

    def __init_piece_repositoryA(self)->None:
        self.pieceRepositoryWidgetA = QWidget()
        self.pieceRepositoryWidgetA.layout = QVBoxLayout(self.pieceRepositoryWidgetA)

        self.pieceRepositorySceneA = QGraphicsScene()
        self.pieceRepositoryViewA = QGraphicsView(self.pieceRepositorySceneA)
        playerNameLabelA = QLabel('Player A')
        self.pieceRepositoryWidgetA.layout.addWidget(playerNameLabelA)
        self.pieceRepositoryWidgetA.layout.addWidget(self.pieceRepositoryViewA)

        # Add the widgets to the main window's layout
        self.left_layout.addWidget(self.pieceRepositoryWidgetA)
        return
    

    def __init_piece_repositoryB(self)->None:
        self.pieceRepositoryWidgetB = QWidget()
        self.pieceRepositoryWidgetB.layout = QVBoxLayout(self.pieceRepositoryWidgetB)

        self.pieceRepositorySceneB = QGraphicsScene()
        self.pieceRepositoryViewB = QGraphicsView(self.pieceRepositorySceneB)
        playerNameLabelB = QLabel('Player B')
        self.pieceRepositoryWidgetB.layout.addWidget(playerNameLabelB)
        self.pieceRepositoryWidgetB.layout.addWidget(self.pieceRepositoryViewB)

        self.left_layout.addWidget(self.pieceRepositoryWidgetB)
        return
    
    def __init_piece_repositoryC(self)->None:
        self.pieceRepositoryWidgetC = QWidget()
        self.pieceRepositoryWidgetC.layout = QVBoxLayout(self.pieceRepositoryWidgetC)

        self.pieceRepositorySceneC = QGraphicsScene()
        self.pieceRepositoryViewC = QGraphicsView(self.pieceRepositorySceneC)
        playerNameLabelC = QLabel('Player C')
        self.pieceRepositoryWidgetC.layout.addWidget(playerNameLabelC)
        self.pieceRepositoryWidgetC.layout.addWidget(self.pieceRepositoryViewC)

        self.right_layout.addWidget(self.pieceRepositoryWidgetC)
        return
    
    def __init_piece_repositoryD(self)->None:
        self.pieceRepositoryWidgetD = QWidget()
        self.pieceRepositoryWidgetD.layout = QVBoxLayout(self.pieceRepositoryWidgetD)

        self.pieceRepositorySceneD = QGraphicsScene()
        self.pieceRepositoryViewD = QGraphicsView(self.pieceRepositorySceneD)
        playerNameLabelD = QLabel('Player D')
        self.pieceRepositoryWidgetD.layout.addWidget(playerNameLabelD)
        self.pieceRepositoryWidgetD.layout.addWidget(self.pieceRepositoryViewD)
        
        self.right_layout.addWidget(self.pieceRepositoryWidgetD)
        return

    def __init_game_field(self) -> None:
        self.game_scene = GameScene(self)
        self.game_view = GameView(self.game_scene, self)
        self.game_view.setMouseTracking(True)
        # Disable scroll bars
        self.game_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.game_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # create game grid
        self.game_grid = []
        for i in range(20):
            row = []
            for j in range(20):
                item = GameFieldElement(self, i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE, QColor(255, 255, 255))
                self.game_scene.addItem(item)
                row.append(item)
            self.game_grid.append(row)
        
        self.central_layout.addWidget(self.game_view)
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
                self.game_scene.removeItem(ghost)
                del ghost
                ghost = None

            # Add the piece to the game grid scene
            piece.isPlaced = True
            self.game_scene.addItem(piece)
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
