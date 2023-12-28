
from __future__ import annotations
from typing import Dict
from PyQt6 import QtGui
from PyQt6.QtGui import QPainter, QPainterPath
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent, QStyleOptionGraphicsItem, QWidget
import numpy as np
from network.networkevent import NetworkEvent
from network.serverapi import NetworkEventObject

from qt6networkadapter import PyQt6_Networkadapter

TILE_SIZE = 21
GAME_FIELD_SIZE = 20 # 20x20 tiles

##################################################
## Author: Kai Pistol
##################################################

class BlokusGame:
    '''
    Contains the ui elements for the blokus game
    - the game field
    - the piece repository for each player
    - the chat
    '''
    def __init__(self, mainWindow, network: PyQt6_Networkadapter, gameInfo: dict):
        self.mainWindow = mainWindow
        self.__network = network
        self.selectedPiece: GamePiece = None
        self.__ghostPiece: GamePiece = None
        self.gameInfo = gameInfo

        self.__init_ui()
        self.__registerNetworkEvents()
        self.__init_ui_handlers()
        self.__display_game_info()
        return
    
    @property
    def ghostPiece(self):
        return self.__ghostPiece
    
    @ghostPiece.setter
    def ghostPiece(self, piece: GhostPiece | None):
        if piece is None:
            if self.__ghostPiece is not None:
                self.field_scene.removeItem(self.__ghostPiece)
        else:
            if self.__ghostPiece is not None:
                self.field_scene.removeItem(self.__ghostPiece)

            self.field_scene.addItem(piece)
            piece.update()

        self.__ghostPiece = piece
        return

    def __init_ui(self):
        # main widget
        self.blokus_widget = QWidget()
        self.blokus_widget.layout = QHBoxLayout(self.blokus_widget)
        self.blokus_widget.setStyleSheet("background-color: #E0E0E0; border: 2px solid black;")

        # main layouts
        self.left_layout = QVBoxLayout()
        self.central_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.blokus_widget.layout.addLayout(self.left_layout)
        self.blokus_widget.layout.addLayout(self.central_layout)
        self.blokus_widget.layout.addLayout(self.right_layout)

        # ui elements
        self.__init_player_area_widgets()
        self.__init_game_field()
        self.__init_chat()
        
        # add the main widget to the main window
        self.mainWindow.central_layout.addWidget(self.blokus_widget)
        return
    
    def __init_player_area_widgets(self):
        # this is needed to be able to iterate over ther player info in the gameInfo dict and access the corresponding piece repository scene
        self.player_area_widgets = []
    	
        # create a plyaer area widget for each player
        for i in range(4):
            playerInfo = self.gameInfo['players'].get(f'{i+1}')
            if not playerInfo: 
                widget = PlayerAreaWidget(self)
            else:
                widget = PlayerAreaWidget(self, color=QColor(playerInfo.get('color')))

            # add the widget to the coresponding layouts
            if i < 2:
                self.left_layout.addWidget(widget)
            else:
                self.right_layout.addWidget(widget)
            
            # add the widget to the list
            self.player_area_widgets.append(widget)
        return

    def __display_game_info(self):
        widget: PlayerAreaWidget
        # display player info in corresponding widget
        for i, widget in enumerate(self.player_area_widgets):
            playerInfo = self.gameInfo['players'].get(f'{i+1}')
            self.__display_player_info(playerInfo, widget)
            
            # self.__display_piece_repository(playerInfo, widget)
        
        # display game field
        self.__display_game_field()
        return
    
    def __registerNetworkEvents(self):
        '''
        Initializes the network event handlers
        '''
        #add network event handler
        self.__network.addNetworkEventHandler(NetworkEvent.MESSAGE, self.__on_message)
        self.__network.addNetworkEventHandler(NetworkEvent.GAME_UPDATE, self.__on_game_update)
        self.__network.addNetworkEventHandler(NetworkEvent.GAME_INVALID_PLACEMENT, self.__on_game_invalid_placement)
        return
    
    def __unregisterNetworkEvents(self):
        '''
        Removes the network event handlers
        '''
        self.__network.removeNetworkEventHandler(NetworkEvent.MESSAGE, self.__on_message)
        self.__network.removeNetworkEventHandler(NetworkEvent.GAME_UPDATE, self.__on_game_update)
        self.__network.removeNetworkEventHandler(NetworkEvent.GAME_INVALID_PLACEMENT, self.__on_game_invalid_placement)
        return

    def __init_ui_handlers(self):
        '''
        Initializes the ui event handlers like:
        - button clicks 
        - key presses
        - ...
        '''
        #add button event handler
        self.chat_send_button.clicked.connect(self.__on_send_clicked)
        ##send message on enter
        self.chat_input.returnPressed.connect(self.chat_send_button.click)
        return

    def __init_chat(self) -> None:
        '''
        Initializes the chat widget and adds it to the central layout
        '''
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


    def __on_send_clicked(self)->None:
        '''
        Sends the message in the chat input to the server
        '''
        message = self.chat_input.text()
        self.chat_input.clear()
        self.__network.api.sendMessage(message)
        return
    
    def __on_message(self, event:NetworkEventObject)->None:
        '''
        On receiving a message from the server, display it in the chat output
        '''
        self.chat_output.append(f'[{event.eventData["from"]}]: {event.eventData["message"]}')
        return
    
    def __on_game_update(self, event:NetworkEventObject)->None:
        '''
        On receiving a game update from the server, update the game field and piece repository
        '''
        self.gameInfo = event.eventData
        #TODO: clear game pieces
        # TODO: update game field
        # TODO: update piece repository
        #self.__display_piece_repository(self.gameInfo)
        self.__display_game_field()
        return
    
    def __on_game_invalid_placement(self, event:NetworkEventObject)->None:
        '''
        On receiving a game invalid placement from the server, display the message as Alert
        '''
        message = event.eventData
        self.mainWindow.alertWidget.showAlert(message)
        return
    
    
    
    def __display_player_info(self, playerInfo: dict, widget: PlayerAreaWidget)->None:
        '''
        Displays the player info in the given widget
        - player name
        '''
        if not playerInfo: return
        widget.playerNameLabelText = playerInfo.get('playerName')
        return
    
    def __display_game_field(self)->None:
        newGameField = self.gameInfo['gameField']
        for i in range(len(self.game_grid)):
            for j in range(len(self.game_grid)):
                if newGameField[i][j] == self.game_grid[i][j]: continue
                if newGameField[i][j] == 0: 
                    self.game_grid[i][j].color = QColor(255, 255, 255)
                else:
                    gamePlayerId = str(int(newGameField[i][j]))

                    color = self.gameInfo['players'][gamePlayerId]['color']
                    self.game_grid[i][j].color = QColor(color)
                    self.game_grid[i][j].setPen(QPen(QColor(0, 0, 0), 2))

                

        return

    def __init_game_field(self) -> None:
        '''
        Initializes the game field and adds it to the central layout
        '''
        self.field_scene = GameScene(self)
        
        self.field_view = GameView(self.field_scene, self)
        self.field_view.setMouseTracking(True)
        # Disable scroll bars
        self.field_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.field_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # create game grid
        self.game_grid = []
        for y in range(GAME_FIELD_SIZE):
            row = []
            for x in range(GAME_FIELD_SIZE):
                item = GameFieldElement(self, x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, QColor(255, 255, 255))
                self.field_scene.addItem(item)
                row.append(item)
            self.game_grid.append(row)

        
        
        self.central_layout.addWidget(self.field_view)

        return


    def placeSelectedPiece(self, piece:GamePiece, ghost:GhostPiece, pos: QPointF)->None:
        '''
        Places the selected piece at the given position

        Parameters:
            piece (GamePiece): the piece to place
            ghost (GhostPiece): the ghost piece
            pos (QPointF): the position to place the piece at

        Returns:
            None
        '''
        if piece is not None:
            if piece.isPlaced: return

            field_x = int(pos.x() // TILE_SIZE)
            field_y = int(pos.y() // TILE_SIZE)
            grid_x = field_x * TILE_SIZE
            grid_y = field_y * TILE_SIZE

            newPiece = piece.clone()

            # Place the selected piece at this location
            newPiece.setPos(grid_x, grid_y)

            self.selectedPiece.setVisible(False)
            # self.selectedPiece = None  # Deselect the piece
            self.ghostPiece = None

            # Add the piece to the game grid scene
            # newPiece.isPlaced = True
            # self.field_scene.addItem(newPiece)

            # notify the server about the placement
            
            self.__network.api.placePiece(newPiece.piece_id, field_x, field_y, newPiece.rotation, newPiece.flip)
        return


class GameFieldElement(QGraphicsRectItem):
    '''
    Represents a single element in the game field ui
    '''
    def __init__(self, game, x, y, w, h, color):
        super().__init__(x, y, w, h)
        self.setBrush(QBrush(color))
        self.game = game
        return

    @property
    def color(self):
        return self.brush().color()
    
    @color.setter
    def color(self, color):
        self.setBrush(QBrush(QColor(color)))
        self.update()
        return

class GamePiece(QGraphicsItemGroup):
    '''
    Represents a single game piece (blokus piece)
    '''
    def __init__(self, piece_id:str, game:BlokusGame, shape, x, y, width, height, rotation=0, flip=0, parent=None, color=QColor('lightgray')):
        '''
        Initializes the game piece
        
        Parameters:
            game (BlokusGame): the game ui instance
            shape (np.array): the shape of the piece
            x (int): the x position of the piece
            y (int): the y position of the piece
            width (int): the width of the piece
            height (int): the height of the piece
            parent (QWidget): the parent widget
        '''
        super().__init__(parent)
        self.__rotation = rotation
        self.game = game
        self.shape_array = shape
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isPlaced = False
        self.__flip = flip
        self.__color = color
        self.__piece_id = piece_id

        #rotete the shape before the piece is constructed
        self.__init_placement()

        # Set the position of the group
        self.setPos(x, y)
        
        return
    
    @property
    def color(self):
        return self.__color
    
    @property
    def piece_id(self):
        return self.__piece_id
    
    @property
    def flip(self) -> int: #TODO: maby a bool would be better suited
        return self.__flip
    
    @property
    def rotation(self) -> int:
        return self.__rotation
    
    @color.setter
    def color(self, color: QColor):
        self.__color = color
        self.update()
        return
    
    def shape(self):
        path = QPainterPath()
        for i in range(self.shape_array.shape[0]):  # iterate over rows
            for j in range(self.shape_array.shape[1]):  # iterate over columns
                if self.shape_array[i, j] == 1:  # Assuming 1 represents a part of the piece
                    path.addRect(QRectF(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return path
    
    def boundingRect(self)->QRectF:
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')

        for i in range(self.shape_array.shape[0]):
            for j in range(self.shape_array.shape[1]):
                if self.shape_array[i, j] == 1:  # Assuming 1 represents a part of the piece
                    min_x = min(min_x, j * TILE_SIZE)
                    min_y = min(min_y, i * TILE_SIZE)
                    max_x = max(max_x, (j + 1) * TILE_SIZE)
                    max_y = max(max_y, (i + 1) * TILE_SIZE)
        return QRectF(min_x, min_y, max_x - min_x, max_y - min_y)

    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        painter.setBrush(self.__color)

        if self.game.selectedPiece == self:  
            painter.setPen(QPen(QColor(0, 0, 255), 2))  
        else:
            painter.setPen(QPen(QColor(0, 0, 0), 2))  

        # Draw the piece
        for i in range(self.shape_array.shape[0]):
            for j in range(self.shape_array.shape[1]):
                if self.shape_array[i, j] == 1:  # Assuming 1 represents a part of the piece
                    painter.drawRect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        return super().paint(painter, option, widget)  
    
    def __init_placement(self) -> None:
        self.shape_array = np.rot90(self.shape_array, self.__rotation)

        if self.__flip != 0:
            self.shape_array = np.flip(self.shape_array, self.__flip)	
        return

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # only react to left mouse button clicks if the piece is not placed and available
            if not self.isPlaced: 
                if self.game.selectedPiece is self:
                    
                    self.game.ghostPiece = None
                    self.game.selectedPiece = None
                else:
                    prevSelection = self.game.selectedPiece

                    self.game.selectedPiece = self
                    self.game.ghostPiece = GhostPiece(self.game, self.shape_array, self.x, self.y, self.width, self.height, color=self.color)

                    # Update the ghost piece
                    if self.game.ghostPiece is not None:
                        self.game.ghostPiece.update()

                    if prevSelection is not None:
                        prevSelection.update()  # Update the previously selected piece
        
        self.update()
        # Call the base class implementation to handle other mouse buttons
        super().mousePressEvent(event)

    def clone(self) -> GamePiece:
        '''
        Creates a deep copy of the game piece
        '''
        # Create a new GamePiece with the same properties
        clone = GamePiece(self.piece_id,
                          self.game, 
                          self.shape_array, 
                          self.x, 
                          self.y, 
                          self.width, 
                          self.height, 
                          color=self.color,
                          rotation=self.rotation,
                          flip=self.flip)
        return clone


class GameScene(QGraphicsScene):
    '''
    Represents the game field ui
    '''
    def __init__(self, game: BlokusGame, parent=None) -> None:
        '''
        Initializes the game scene
        
        Parameters:
            game (BlokusGame): the game ui instance
            parent (QWidget): the parent widget
        '''
        super().__init__(parent)
        self.game = game

    def mouseMoveEvent(self, event):
        '''
        Handles the mouse move event for the game scene:
        - if there is a ghost piece, move it to the mouse position
        '''
        if self.game.ghostPiece is not None:
            pos = event.scenePos()
            if self.sceneRect().contains(pos):
                # Move the ghost piece to the mouse position
                grid_x = int(pos.x() // TILE_SIZE) * TILE_SIZE
                grid_y = int(pos.y() // TILE_SIZE) * TILE_SIZE

                self.game.ghostPiece.setPos(grid_x, grid_y)
        return

    def mousePressEvent(self, event):
        '''
        Handles the mouse press event for the game scene:
        - if there is a ghost piece, place the selected piece at the ghost piece's position
        '''
        if self.game.ghostPiece:
            # Place the piece at the current position of the ghost piece
            self.game.placeSelectedPiece(self.game.selectedPiece,
                                         self.game.ghostPiece,
                                         event.scenePos())
        if self.game.selectedPiece is not None:
            self.game.selectedPiece.isPlaced = True
        return super().mousePressEvent(event)


class GameView(QGraphicsView):
    '''
    I don't know what exacly the View is for but it is needed for the scene to work ... lol
    The subclassing is needed to customice the mouse events
    '''
    def __init__(self, scene, game:BlokusGame, parent=None):
        super().__init__(scene, parent)
        self.game = game

        self.__init_ui()
        return
    
    def __init_ui(self):
        self.setSceneRect(0, 0, GAME_FIELD_SIZE * TILE_SIZE, GAME_FIELD_SIZE * TILE_SIZE)

        # create border to for handling the mouse leaves or enters the game field
        self.field_border = QGraphicsRectItem()
        self.field_border.setPen(QPen(QColor(255, 255, 0), 0))
        self.field_border.setRect(0, 0, GAME_FIELD_SIZE * TILE_SIZE, GAME_FIELD_SIZE * TILE_SIZE)
        self.scene().addItem(self.field_border)
        return

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        # Call the original mouseMoveEvent to keep its functionality
        super().mouseMoveEvent(event)

        # Get the mouse position in scene coordinates
        mouse_pos = self.mapToScene(event.pos())

        # Check if the mouse is inside the GameFieldBorder
        if not self.field_border.contains(mouse_pos):
            # If it's not, hide the ghost piece
            ghost = self.game.ghostPiece
            if ghost:
                ghost.setVisible(False)
        else:
            # If it is, show the ghost piece
            ghost = self.game.ghostPiece
            if ghost:
                ghost.setVisible(True)
        return

class GhostPiece(GamePiece):
    '''
    Represents a ghost piece that is displayed when a piece is selected.
    
    The ghost piece is used to show the player where the piece will be placed.
    The ghost piece is not selectable and not movable.
    '''
    def __init__(self, game:BlokusGame, shape, x, y, width, height, parent=None, color=QColor('lightgray')):
        super().__init__('', game, shape, x, y, width, height, parent=parent, color=color)
        self.setOpacity(0.5)  # Make the ghost piece semi-transparent
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setVisible(False)

        def mousePressEvent(self, event):
            '''
            Overwritten to prevent the ghost piece from being selected
            '''
            return

        def mouseMoveEvent(self, event):
            '''
            Overwritten to prevent the ghost piece from being moved? sounds fishy -> TODO: check this
            '''
            return

        return

class PlayerAreaWidget(QWidget):
    def __init__(self, game: BlokusGame, parent=None, color: QColor = QColor('lightgray')):
        super().__init__(parent=parent)
        self.__game = game
        self.__color = color

        self.__init_ui()
        return
    
    def __init_ui(self):
        self.layout = QVBoxLayout(self)

        self.__scene = QGraphicsScene()
        self.__view = QGraphicsView(self.__scene)
        self.__nameLabel = QLabel('Player Name')
        self.__nameLabel.setStyleSheet('font-weight: bold;')
        self.layout.addWidget(self.__nameLabel)
        self.layout.addWidget(self.__view)

        self.__init_piece_objects()
        self.__display_piece_repository()
        return
    

    def __init_piece_objects(self):
        #TODO: refactor hard coded values and move them somewhere else
        o = TILE_SIZE//2 #the min spacing between the pieces
        p = TILE_SIZE #the size of the pieces
        self.__piece_objects:Dict[str:GamePiece] = {
            "1_0": GamePiece('1_0',self.__game, np.array([[1]]), 7*p, 0, p, p),
            "2_0": GamePiece('2_0',self.__game, np.array([[1, 1]]), 10*p+o, 2*p+o, p, p),
            "3_0": GamePiece('3_0',self.__game, np.array([[1, 1, 1]]), 0, 11*p+o, p, p),
            "3_1": GamePiece('3_1',self.__game, np.array([[0, 1], [1, 1]]), 9*p, 10*p, p, p, rotation=1, flip=1),
            "4_0": GamePiece('4_0',self.__game, np.array([[0, 1], [1, 1], [1, 0]]), 3*p+o, 10*p+o, p, p, rotation=1, flip=1),
            "4_1": GamePiece('4_1',self.__game, np.array([[1, 1], [1, 1]]), 0, 3*p+2*o, p, p),
            "4_2": GamePiece('4_2',self.__game, np.array([[0, 1, 0], [1, 1, 1]]), 5*p+o, 5, p, p, rotation=1, flip=1), 
            "4_3": GamePiece('4_3',self.__game, np.array([[1, 1, 1], [0, 0, 1]]), 10*p+o, 9*p+o, p, p, rotation=3), 
            "4_4": GamePiece('4_4',self.__game, np.array([[1, 1, 1, 1]]), 2*p+o, 5*p, p, p),
            "5_0": GamePiece('5_0',self.__game, np.array([[0, 1], [1, 1], [1, 1]]), 0, 8*p, p, p, flip=1),
            "5_1": GamePiece('5_1',self.__game, np.array([[0, 1], [0, 1], [1, 1], [1, 0]]), 6*p+o, 8*p, p, p, rotation=2, flip=1),
            "5_2": GamePiece('5_2',self.__game, np.array([[1, 1, 1, 1], [0, 0, 0, 1]]), 8*p+o, 0, p, p),
            "5_3": GamePiece('5_3',self.__game, np.array([[1, 1, 1, 1, 1]]), 0, 0, p, p),
            "5_4": GamePiece('5_4',self.__game, np.array([[1, 1], [1, 0], [1, 1]]), 0, p+o, p, p, rotation=3),
            "5_5": GamePiece('5_5',self.__game, np.array([[0, 1, 1], [0, 1, 0], [1, 1, 0]]), 5*p, 5*p+o, p, p, rotation=1, flip=1 ),
            "5_6": GamePiece('5_6',self.__game, np.array([[0, 1, 1], [1, 1, 0], [1, 0, 0]]), 9*p+o, 4*p, p, p, rotation=0, flip=0),
            "5_7": GamePiece('5_7',self.__game, np.array([[0, 0, 1], [0, 0, 1], [1, 1, 1]]), 3*p+o, p+o, p, p, flip=1),
            "5_8": GamePiece('5_8',self.__game, np.array([[0, 0, 1], [1, 1, 1], [0, 0, 1]]), 3*p, 8*p, p, p, rotation=2),
            "5_9": GamePiece('5_9',self.__game, np.array([[0, 1, 0], [0, 1, 1], [1, 1, 0]]), 9*p, 6*p+o, p, p, rotation=3, flip=1),
            "5_10": GamePiece('5_10',self.__game, np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]), 7*p, 2*p, p, p),
            "5_11": GamePiece('5_11',self.__game, np.array([[0, 1, 0, 0], [1, 1, 1, 1]]), o, 6*p+o, p, p, rotation=2, flip=1),
        }
        return

    def __display_piece_repository(self)->None:
        '''
        '''
        for key, piece in self.__piece_objects.items():
            piece.color = self.__color
            self.scene.addItem(piece)
        return

    @property
    def view(self)->QGraphicsView:
        return self.__view
    
    @property
    def scene(self)->QGraphicsScene:
        return self.__scene
    
    @property
    def playerNameLabelText(self):
        return self.__nameLabel.text()

    @playerNameLabelText.setter
    def playerNameLabelText(self, text:str):
        self.__nameLabel.setText(text)
