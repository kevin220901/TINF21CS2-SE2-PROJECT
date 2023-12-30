
from __future__ import annotations
import json
import threading
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
import functools
from datetime import datetime

import logging
from sys import stdout

from qt6networkadapter import PyQt6_Networkadapter

import contextvars


LOG_FORMAT = "%(message)s"   
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

logging.basicConfig(handlers=[logging.StreamHandler(stdout), logging.FileHandler(f'client{timestamp}.log.json')],
                    level = logging.DEBUG,
                    format= LOG_FORMAT,
                    datefmt='%H:%M:%S')

logger:logging.Logger = logging.getLogger()



# Create a ContextVar to store the nesting level
nesting_level_var = contextvars.ContextVar('nesting_level', default=0)

def log_method_call(logAttributes:bool=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            class_name = args[0].__class__.__name__
            thread_name = threading.current_thread().name
            in_timestamp = datetime.now().isoformat()
            # Get the current nesting level
            nesting_level = nesting_level_var.get()
            # Get a dump of the object's attributes
            if logAttributes:
                obj = args[0]
                attributes = obj.to_dict() if hasattr(obj, 'to_dict') else vars(obj)
            else:
                attributes = 'not logged'
            log_entry = {
                "timestamp": in_timestamp,
                "thread": thread_name,
                "class": class_name,
                "method": func.__name__,
                "event": "call",
                "level": nesting_level,
                "attributes": attributes
            }
            logger.debug(json.dumps(log_entry))
            # Increment the nesting level
            nesting_level_var.set(nesting_level + 1)

            result = func(*args, **kwargs)      # the actual method call

            # Decrement the nesting level
            nesting_level_var.set(nesting_level)
            out_timestamp = datetime.now().isoformat()
            if logAttributes:
                obj = args[0]
                attributes = obj.to_dict() if hasattr(obj, 'to_dict') else vars(obj)
            else:
                attributes = 'not logged'
            log_entry = {
                "timestamp": out_timestamp,
                "thread": thread_name,
                "class": class_name,
                "method": func.__name__,
                "event": "return",
                "level": nesting_level,
                "attributes": attributes
            }
            logger.debug(json.dumps(log_entry))
            return result
        return wrapper
    return decorator


TILE_SIZE = 21
GAME_FIELD_SIZE = 20 # 20x20 tiles

##################################################
## Author: Kai Pistol
##################################################

class PlacePieceEvent:
    def __init__(self, piece_id:str, x:float, y:float, operations:str) -> None:
        self.piece_id = piece_id
        self.x = x
        self.y = y
        self.operations = operations

class PieceClickedEvent:
    def __init__(self, piece:GamePiece, mouseEvent:QGraphicsSceneMouseEvent) -> None:
        self._piece = piece
        self._mouseEvent = mouseEvent

    @property
    def piece(self):
        return self._piece
    
    @property
    def mouseEvent(self):
        return self._mouseEvent

class BlokusGame:
    '''
    Contains the ui elements for the blokus game
    - the game field
    - the piece repository for each player
    - the chat
    '''
    # @log_method_call(logAttributes=False)
    def __init__(self, mainWindow, network: PyQt6_Networkadapter, gameInfo: dict):
        self.mainWindow = mainWindow
        self.__network = network
        self.__selectedPiece: GamePiece = None
        self.__ghostPiece: GamePiece = None
        self.gameInfo = gameInfo


        self.__init_ui()
        self.__registerNetworkEvents()
        self.__init_ui_handlers()
        self.__display_game_info()
        return
    
    def registerPieceClickedEvent(self, piece:GamePiece):
        piece.signals.pieceClickedEvent.connect(self.__on_piece_clicked)
        return
    
    def __on_piece_clicked(self, event:PieceClickedEvent):
        if isinstance(event.piece, GamePiece): 
            self.selectedPiece = event.piece
        return

    def rotatePiece(self, piece:GamePiece, times=1):
        if piece:
            rotatedGhost = GhostPiece(piece.player_id, 
                                         piece.piece_id, 
                                         piece.base_shape, 
                                         piece.x(), 
                                         piece.y(), 
                                         piece.width, 
                                         piece.height, 
                                         color=piece.color, 
                                         operations=piece.operations + 'r'*times)
            rotatedGhost.setVisible(True)
            self.ghostPiece = rotatedGhost
        return

    def to_dict(self):
        return {
            'selectedPiece': self.__selectedPiece.to_dict() if self.__selectedPiece else None,
            'ghostPiece': self.__ghostPiece.to_dict() if self.__ghostPiece else None,
            'gameInfo': self.gameInfo
        }
    
    @property
    def selectedPiece(self):
        return self.__selectedPiece
    
    @selectedPiece.setter
    # @log_method_call(logAttributes=False)
    def selectedPiece(self, piece: GamePiece | None):
        '''
        Handles the selection and deselection of a piece.
        Also triggers the creation and deletion of the ghost piece.
        '''

        #Case 1: previous piece is None and new piece is None -> do nothing
        #Case 2: previous piece is None and new piece is not None -> select new piece, create ghost

        #Case 3: previous piece is not None and new piece is None -> deselect previous piece, delete ghost
        #Case 4 previous piece == new piece -> deselect previous piece, delete ghost
        #Case 5: previous piece is not None and new piece is not None -> deselect previous piece, select new piece, create ghost
        
        if self.__selectedPiece is None and piece is None: 
            # Case 1	
            return   
        
        elif self.__selectedPiece is None and piece:
            # Case 2
            self.__selectedPiece = piece
            self.__selectedPiece.isSelected = True  # Highlight the piece
            self.__selectedPiece.update()
            self.ghostPiece = self.__selectedPiece.createGhostPiece()

        elif self.__selectedPiece and piece is None:
            # Case 3
            self.__selectedPiece.isSelected = False
            self.__selectedPiece.update()
            self.__selectedPiece = None
            self.ghostPiece = None
        elif self.__selectedPiece == piece:
            # Case 4
            self.__selectedPiece.isSelected = False
            self.__selectedPiece.update()
            self.__selectedPiece = None
            self.ghostPiece = None

        elif self.__selectedPiece and piece:
            # Case 5
            self.__selectedPiece.isSelected = False
            self.__selectedPiece.update()
            self.__selectedPiece = piece
            self.__selectedPiece.isSelected = True  # Highlight the piece
            self.__selectedPiece.update()
            self.ghostPiece = self.__selectedPiece.createGhostPiece()
        
        else:
            raise Exception('BlokusGame::selectedPiece.setter >> Unknown case occoured')    # WARNING: contains no helpful information
        return

    @property
    def ghostPiece(self):
        return self.__ghostPiece

    @ghostPiece.setter
    # @log_method_call(logAttributes=False)
    def ghostPiece(self, piece: GhostPiece | None):

        #Case 1: previous piece is None and new piece is None -> do nothing
        #Case 2: previous piece is None and new piece is not None -> create ghost

        #Case 3: previous piece is not None and new piece is None -> delete ghost
        #Case 4: previous piece is not None and new piece is not None -> delete ghost, create ghost

        if self.__ghostPiece is None and piece is None: 
            # Case 1	
            return
        elif self.__ghostPiece is None and piece:
            # Case 2
            self.__ghostPiece = piece
            self.field_scene.addItem(self.__ghostPiece)
        elif self.__ghostPiece and piece is None:
            # Case 3
            self.field_scene.removeItem(self.__ghostPiece)
            self.__ghostPiece = None
        elif self.__ghostPiece and piece:
            # Case 4
            self.field_scene.removeItem(self.__ghostPiece)
            self.__ghostPiece = piece
            self.field_scene.addItem(self.__ghostPiece)
        else:
            raise Exception('BlokusGame::ghostPiece.setter >> Unknown case occoured') # WARNING contains no helpful information
        return
    
    # @log_method_call(logAttributes=False)
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
    
    # @log_method_call(logAttributes=False)
    def __init_player_area_widgets(self):
        # this is needed to be able to iterate over ther player info in the gameInfo dict and access the corresponding piece repository scene
        self.player_area_widgets = []
    	
        # create a plyaer area widget for each player
        for i in range(4):
            
            playerInfo = self.gameInfo['players'].get(f'{i+1}')     # players is a dict so the key is a string. therefore the i+1 is converted to a string
            if not playerInfo: 
                widget = PlayerAreaWidget(i+1, self)
            else:
                widget = PlayerAreaWidget(i+1, self, color=QColor(playerInfo.get('color')))

            # add the widget to the coresponding layouts
            if i < 2:
                self.left_layout.addWidget(widget)
            else:
                self.right_layout.addWidget(widget)
            
            # add the widget to the list
            self.player_area_widgets.append(widget)
        return
    
    # @log_method_call(logAttributes=False)
    def __display_game_info(self):
        '''
        Displays the game info in the ui.
        - player info
            - player name
            - available pieces
            - color (not implemented yet)
        - game field
        '''

        player_area: PlayerAreaWidget
        # display player info in corresponding widget
        for i, player_area in enumerate(self.player_area_widgets):
            playerInfo = self.gameInfo['players'].get(f'{i+1}')
            self.__display_player_info(playerInfo, player_area)
            self.__display_player_available_pieces(playerInfo, player_area)
            
        
        # display game field
        self.__display_game_field()
        return
    
    # @log_method_call(logAttributes=False)
    def __registerNetworkEvents(self):
        '''
        Initializes the network event handlers
        '''
        #add network event handler
        self.__network.addNetworkEventHandler(NetworkEvent.MESSAGE, self.__on_message)
        self.__network.addNetworkEventHandler(NetworkEvent.GAME_UPDATE, self.__on_game_update)
        self.__network.addNetworkEventHandler(NetworkEvent.GAME_INVALID_PLACEMENT, self.__on_game_invalid_placement)
        # TODO: add network event handler for invalid action
        return
    
    # @log_method_call(logAttributes=False)
    def __unregisterNetworkEvents(self):
        '''
        Removes the network event handlers
        '''
        self.__network.removeNetworkEventHandler(NetworkEvent.MESSAGE, self.__on_message)
        self.__network.removeNetworkEventHandler(NetworkEvent.GAME_UPDATE, self.__on_game_update)
        self.__network.removeNetworkEventHandler(NetworkEvent.GAME_INVALID_PLACEMENT, self.__on_game_invalid_placement)
        return

    # @log_method_call(logAttributes=False)
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

        self.field_scene.piecePlacedEvent.connect(self.__on_place_piece)
        return
    
    # @log_method_call(logAttributes=False)
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

    # @log_method_call(logAttributes=False)
    def __on_send_clicked(self)->None:
        '''
        Sends the message in the chat input to the server
        '''
        message = self.chat_input.text()
        self.chat_input.clear()
        self.__network.api.sendMessage(message)
        return
    
    # @log_method_call(logAttributes=False)
    def __on_message(self, event:NetworkEventObject)->None:
        '''
        On receiving a message from the server, display it in the chat output
        '''
        self.chat_output.append(f'[{event.eventData["from"]}]: {event.eventData["message"]}')
        return
    
    # @log_method_call(logAttributes=True)
    def __on_game_update(self, event:NetworkEventObject)->None:
        '''
        On receiving a game update from the server, update the game field and piece repository
        '''
        self.gameInfo = event.eventData
        self.__display_game_info()
        return
    
    # @log_method_call(logAttributes=False)
    def __on_game_invalid_placement(self, event:NetworkEventObject)->None:
        '''
        On receiving a game invalid placement from the server, display the message as Alert
        '''
        message = event.eventData
        self.mainWindow.alertWidget.showAlert(message)
        return
    
    
    # @log_method_call(logAttributes=False)
    def __display_player_info(self, playerInfo: dict, widget: PlayerAreaWidget)->None:
        '''
        Displays the player info in the given widget
        - player name
        '''
        if not playerInfo: return
        # TODO: check if the a players color has changed and update if needed
        widget.playerNameLabelText = playerInfo.get('playerName')
        return
    
    # @log_method_call(logAttributes=False)
    def __display_game_field(self)->None:
        newGameField = self.gameInfo['gameField']
        for i in range(len(self.game_grid)):
            for j in range(len(self.game_grid)):
                #TODO: only update if changes have been made
                if newGameField[i][j] == 0: 
                    self.game_grid[i][j].color = QColor(255, 255, 255)
                else:
                    gamePlayerId = str(int(newGameField[i][j]))

                    color = self.gameInfo['players'][gamePlayerId]['color']
                    self.game_grid[i][j].color = QColor(color)
                    self.game_grid[i][j].setPen(QPen(QColor(0, 0, 0), 2))
        return
    
    # @log_method_call(logAttributes=False)
    def __display_player_available_pieces(self, playerInfo: dict, widget: PlayerAreaWidget)->None:
        '''
        Shows or hides the given players available pieces. 
        Does nothing if the playerInfo is None


        Parameters: 
            playerInfo (dict): the player info dict
            widget (PlayerAreaWidget): the widget to display the pieces in

        Returns:
            None
        '''
        if not playerInfo: return
        availablePieces = playerInfo.get('pieces')
        widget.update_available_pieces(availablePieces)

        return

    # @log_method_call(logAttributes=False)
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

    # @log_method_call(logAttributes=False)
    def __on_place_piece(self, event:PlacePieceEvent)->None:
        '''
        Places the piece at the given position

        Parameters:
            event (PlacePieceEvent): the event containing the piece id, the position and the operations (rotation and flip)

        Returns:
            None
        '''
        if event:
            # self.selectedPiece = None

            if self.__ghostPiece is None: return
            if self.__ghostPiece not in self.field_scene.items(): return

            self.selectedPiece = None
            
            # calculate the grid local position of the mouse
            field_x = int(event.x // TILE_SIZE)
            field_y = int(event.y // TILE_SIZE)

            self.__network.api.placePiece(event.piece_id, 
                                          field_x, 
                                          field_y, 
                                          event.operations)         # since the ghost piece is used to visualize the placement, its rotation and flip value are used to place the piece 
            
            # self.selectedPiece.setVisible(False)
           
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

    class Signals(QObject):
        pieceClickedEvent = pyqtSignal(PieceClickedEvent)

    # @log_method_call(logAttributes=False)
    def __init__(self, player_id:int, piece_id:str, shape:np.ndarray, x, y, width, height, operations:str='', parent=None, color=QColor('lightgray')):
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
        # self.__game:BlokusGame = game
        self.__base_shape_array = shape
        self.shape_array = shape
        self.width = width
        self.height = height
        self.isPlaced = False
        self._operations = ''
        self.__color = color
        self.__piece_id = piece_id
        self.__isSelected: bool = False
        self.player_id = player_id
        self._isGhost = False
        self._signals = GamePiece.Signals()


        #rotete and flip the shape before the piece is constructed
        for o in operations:
            if o == 'r':
                self.rotate90()
            elif o == 'x':
                self.flipX()
            elif o == 'y':
                self.flipY()

        # Set the position of the group
        self.setPos(x, y)
        
        return
    
    @property
    def signals(self) -> GamePiece.Signals:
        return self._signals

    @property
    def color(self):
        return self.__color

    @property
    def piece_id(self):
        return self.__piece_id
    
    @property
    def operations(self):
        return self._operations
    
    @property
    def isSelected(self):
        return self.__isSelected
    
    
    @color.setter
    # @log_method_call(logAttributes=False)
    def color(self, color: QColor):
        self.__color = color
        if self.isVisible():
            self.update()
        return
    
    @property
    def base_shape(self) -> np.array:
        return self.__base_shape_array
    
    @isSelected.setter
    # @log_method_call(logAttributes=False)
    def isSelected(self, value:bool):
        # if value == self.__isSelected: return
        if self.isPlaced: return

        self.__isSelected = value
        # self.update()
        return

    def to_dict(self):
        return {
            'player_id': self.player_id,
            'piece_id': self.piece_id,
            'shape_array': self.shape_array.tolist(),
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'color': self.color.name(),
            'operations': self.operations
        }
    
    
    # @log_method_call(logAttributes=True)
    def shape(self) -> QPainterPath:
        path = QPainterPath()
        for i in range(self.shape_array.shape[0]):  # iterate over rows
            for j in range(self.shape_array.shape[1]):  # iterate over columns
                if self.shape_array[i, j] == 1:  # 1 represents a part of the piece
                    path.addRect(QRectF(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return path
    
    # @log_method_call(logAttributes=True)
    def boundingRect(self)->QRectF:
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')

        for i in range(self.shape_array.shape[0]):
            for j in range(self.shape_array.shape[1]):
                if self.shape_array[i, j] == 1:  # 1 represents a part of the piece
                    min_x = min(min_x, j * TILE_SIZE)
                    min_y = min(min_y, i * TILE_SIZE)
                    max_x = max(max_x, (j + 1) * TILE_SIZE)
                    max_y = max(max_y, (i + 1) * TILE_SIZE)
        return QRectF(min_x, min_y, max_x - min_x, max_y - min_y)
    
    # @log_method_call(logAttributes=True)
    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        if self.scene() is None:
            return
        painter.setBrush(self.__color)

        if self.isSelected:  
            painter.setPen(QPen(QColor(0, 0, 255), 2))  
        else:
            painter.setPen(QPen(QColor(0, 0, 0), 2))  

        # Draw the piece
        for i in range(self.shape_array.shape[0]):
            for j in range(self.shape_array.shape[1]):
                if self.shape_array[i, j] == 1:  # 1 represents a part of the piece
                    painter.drawRect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        return   
    
    # @log_method_call(logAttributes=False)
    def rotate90(self, times=1) -> None:
        '''
        Rotates the piece 90 degrees clockwise
        '''
        self._operations += 'r'*times
        self.shape_array = np.rot90(self.shape_array, times)
        return
    # @log_method_call(logAttributes=False)
    def flipX(self) -> None:
        '''
        Flips the piece along the x axis
        '''
        self._operations += 'x'
        self.shape_array = np.flip(self.shape_array, 0) # 0 = flip along x axis
        return
    
    # @log_method_call(logAttributes=False)
    def flipY(self) -> None:
        '''
        Flips the piece along the y axis
        '''
        self._operations += 'y'
        self.shape_array = np.flip(self.shape_array, 1) # 1 = flip along y axis
        return
    
    # @log_method_call(logAttributes=False)
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        clickedEvent = PieceClickedEvent(self, event)
        self.signals.pieceClickedEvent.emit(clickedEvent)
        return
    
    # for now deprecated
    # @log_method_call(logAttributes=False)
    def clone(self) -> GamePiece:
        '''
        Creates a deep copy of the game piece
        '''
        # Create a new GamePiece with the same properties
        clone = GamePiece(self.piece_id,
                          self.shape_array, 
                          self.x(), 
                          self.y(), 
                          self.width, 
                          self.height, 
                          color=self.color,
                          operations=self.operations)
        return clone

    # @log_method_call(logAttributes=False)
    def createGhostPiece(self) -> GhostPiece:
        '''
        Creates a ghost piece from the game piece
        '''
        ghost = GhostPiece(self.player_id,
                           self.piece_id,
                           self.__base_shape_array, 
                           self.x(), 
                           self.y(), 
                           self.width, 
                           self.height, 
                           color=self.color,
                           operations=self.operations)
        
        # ghost.update()
                           
        return ghost
class GameScene(QGraphicsScene):
    '''
    Represents the game field ui
    '''

    piecePlacedEvent = pyqtSignal(PlacePieceEvent)

    def __init__(self, game: BlokusGame, parent=None) -> None:
        '''
        Initializes the game scene
        
        Parameters:
            game (BlokusGame): the game ui instance
            parent (QWidget): the parent widget
        '''
        super().__init__(parent)
        self._game = game
        
        return
    
    def to_dict(self)->dict:
        return {
            'game': self._game.to_dict()
        }
    
    # @log_method_call(logAttributes=True)
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        '''
        Handles the mouse move event for the game scene:
        - if there is a ghost piece, move it to the mouse position
        '''
        if self._game.ghostPiece is not None:
            if self._game.ghostPiece not in self.items(): return

            pos = event.scenePos()
            if self.sceneRect().contains(pos):
                # Move the ghost piece to the mouse position
                grid_x = int(pos.x() // TILE_SIZE) * TILE_SIZE
                grid_y = int(pos.y() // TILE_SIZE) * TILE_SIZE

                self._game.ghostPiece.setPos(grid_x, grid_y)
        return
    
    # @log_method_call(logAttributes=True)
    def mousePressEvent(self, event):
        '''
        Handles the mouse press event for the game scene:
        '''

        super().mousePressEvent(event)

        mouseButton = event.button()
        if self._game.ghostPiece is None: return
        if self._game.ghostPiece not in self.items(): return

        if Qt.MouseButton.LeftButton == mouseButton:
            # left button click
            self.__on_left_click(event) 
        elif Qt.MouseButton.RightButton == mouseButton:
            # right button click
            self.__on_right_click(event)

        return
    
    # @log_method_call(logAttributes=False)
    def __on_left_click(self, event: QGraphicsSceneMouseEvent) -> None:
        '''
        Handles the mouse press event for the game scene:
        - if there is a ghost piece, place the selected piece at the ghost piece's position
        '''
        if self._game.ghostPiece is None: return    #TODO: why does the placement depend on the ghost piece? -> check this and leave a comment
        if self._game.ghostPiece not in self.items(): return
        if self._game.ghostPiece.isVisible() == False: return

        piece = self._game.ghostPiece
        #self._game.selectedPiece = None
        self._game.selectedPiece.isSelected = False
        self._game.ghostPiece.setVisible(False)

        # self.game.placeSelectedPiece(piece, event.scenePos())
        pos = event.scenePos()
        pieceEvent = PlacePieceEvent(piece.piece_id, pos.x(), pos.y(), piece.operations)
        # self.game.selectedPiece = None
        if piece:
            self.piecePlacedEvent.emit(pieceEvent)
        return
    
    # @log_method_call(logAttributes=False)
    def __on_right_click(self, event: QGraphicsSceneMouseEvent) -> None:
        '''
        Handles the mouse press event for the game scene:
        - if there is a ghost piece, rotate the ghost piece 90 degrees clockwise
        '''
        if self._game.ghostPiece is None: return
        if self._game.ghostPiece not in self.items(): return
            
        # Rotate the ghost piece 90 degrees clockwise
        self._game.rotatePiece(self._game.ghostPiece)
        return



class GameView(QGraphicsView):
    '''
    I don't know what exacly the View is for but it is needed for the scene to work ... lol
    The subclassing is needed to customice the mouse events
    '''
    def __init__(self, scene, game:BlokusGame, parent=None):
        super().__init__(scene, parent)
        self.__game = game

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
    
    def to_dict(self)->dict:
        return {
            'game': self.__game.to_dict()
        }

    # @log_method_call(logAttributes=True)
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        # Call the original mouseMoveEvent to keep its functionality
        super().mouseMoveEvent(event)
        if self.__game.ghostPiece is None: return
        if self.__game.ghostPiece not in self.scene().items(): return

        # Get the mouse position in scene coordinates
        mouse_pos = self.mapToScene(event.pos())

        # Check if the mouse is inside the GameFieldBorder
        if not self.field_border.contains(mouse_pos):
            # If it's not, hide the ghost piece
            ghost = self.__game.ghostPiece
            if ghost:
                ghost.setVisible(False)
        else:
            # If it is, show the ghost piece
            ghost = self.__game.ghostPiece
            if ghost:
                ghost.setVisible(True)
        return

class GhostPiece(GamePiece):
    '''
    Represents a ghost piece that is displayed when a piece is selected.
    
    The ghost piece is used to show the player where the piece will be placed.
    The ghost piece is not selectable and not movable.
    '''
    def __init__(self, player_id:int, pieceId:str, shape, x, y, width, height, parent=None, color=QColor('lightgray'), operations:str=''):
        super().__init__(player_id, pieceId,shape, x, y, width, height, parent=parent, color=color, operations=operations)
        self._isGhost = True
        self.setOpacity(0.5)  # Make the ghost piece semi-transparent
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setVisible(False)
        return

    def mouseMoveEvent(self, event):
        '''
        Overwritten to prevent the ghost piece from being selected
        '''
        return

    def mousePressEvent(self, event):
        '''
        Overwritten to prevent the ghost piece from being moved? sounds fishy -> TODO: check this
        '''
        return
    
    def clone(self):
        newGhost = GhostPiece(self.player_id, 
                              self.piece_id, 
                              self.base_shape, 
                              self.x, 
                              self.y, 
                              self.width, 
                              self.height, 
                              color=self.color, 
                              operations=self.operations)
        
        return newGhost
        

class PlayerAreaWidget(QWidget):
    def __init__(self, player_id:int, game: BlokusGame, parent=None, color: QColor = QColor('lightgray')):
        super().__init__(parent=parent)
        self.__game:BlokusGame = game
        self.__color:QColor = color
        self.__piece_objects:Dict[str:GamePiece]
        self.player_id = player_id

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
    
    # @log_method_call(logAttributes=False)
    def update_available_pieces(self, availablePieces: list):
        '''
        Updates the available pieces in the piece repository
        '''
        piece: GamePiece
        keys = self.__piece_objects.keys()
        for key in keys:
            piece = self.__piece_objects[key]
            if key in availablePieces:
                # piece is available
                piece.setVisible(True)
            else:
                # piece is not available
                piece.setVisible(False)
        return
    # @log_method_call(logAttributes=False)
    def __init_piece_objects(self):
        #TODO: refactor hard coded values and move them somewhere else
        o = TILE_SIZE//2 #used as spacing between the pieces
        p = TILE_SIZE #the size of the pieces
        self.__piece_objects = {
            "1_0": GamePiece(self.player_id, '1_0', np.array([[1]]), 7*p, 0, p, p, 'y'),
            "2_0": GamePiece(self.player_id, '2_0', np.array([[1, 1]]), 10*p+o, 2*p+o, p, p, 'y'),
            "3_0": GamePiece(self.player_id, '3_0', np.array([[1, 1, 1]]), 0, 11*p+o, p, p, 'y'),
            "3_1": GamePiece(self.player_id, '3_1', np.array([[0, 1], [1, 1]]), 9*p, 10*p, p, p, 'ry'),
            "4_0": GamePiece(self.player_id, '4_0', np.array([[0, 1], [1, 1], [1, 0]]), 3*p+o, 10*p+o, p, p, 'ry'),
            "4_1": GamePiece(self.player_id, '4_1', np.array([[1, 1], [1, 1]]), 0, 3*p+2*o, p, p, ''),
            "4_2": GamePiece(self.player_id, '4_2', np.array([[0, 1, 0], [1, 1, 1]]), 5*p+o, 5, p, p, 'ry'), 
            "4_3": GamePiece(self.player_id, '4_3', np.array([[1, 1, 1], [0, 0, 1]]), 10*p+o, 9*p+o, p, p, 'rrr'), 
            "4_4": GamePiece(self.player_id, '4_4', np.array([[1, 1, 1, 1]]), 2*p+o, 5*p, p, p, 'y'),
            "5_0": GamePiece(self.player_id, '5_0', np.array([[0, 1], [1, 1], [1, 1]]), 0, 8*p, p, p, 'y'),
            "5_1": GamePiece(self.player_id, '5_1', np.array([[0, 1], [0, 1], [1, 1], [1, 0]]), 6*p+o, 8*p, p, p, 'rry'),
            "5_2": GamePiece(self.player_id, '5_2', np.array([[1, 1, 1, 1], [0, 0, 0, 1]]), 8*p+o, 0, p, p, ''),
            "5_3": GamePiece(self.player_id, '5_3', np.array([[1, 1, 1, 1, 1]]), 0, 0, p, p, 'y'),
            "5_4": GamePiece(self.player_id, '5_4', np.array([[1, 1], [1, 0], [1, 1]]), 0, p+o, p, p, 'rrry'),
            "5_5": GamePiece(self.player_id, '5_5', np.array([[0, 1, 1], [0, 1, 0], [1, 1, 0]]), 5*p, 5*p+o, p, p, 'ry'),
            "5_6": GamePiece(self.player_id, '5_6', np.array([[0, 1, 1], [1, 1, 0], [1, 0, 0]]), 9*p+o, 4*p, p, p, ''),
            "5_7": GamePiece(self.player_id, '5_7', np.array([[0, 0, 1], [0, 0, 1], [1, 1, 1]]), 3*p+o, p+o, p, p, 'y'),
            "5_8": GamePiece(self.player_id, '5_8', np.array([[0, 0, 1], [1, 1, 1], [0, 0, 1]]), 3*p, 8*p, p, p, 'rr'),
            "5_9": GamePiece(self.player_id, '5_9', np.array([[0, 1, 0], [0, 1, 1], [1, 1, 0]]), 9*p, 6*p+o, p, p, 'rrry'),
            "5_10": GamePiece(self.player_id, '5_10', np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]), 7*p, 2*p, p, p, 'y'),
            "5_11": GamePiece(self.player_id, '5_11', np.array([[0, 1, 0, 0], [1, 1, 1, 1]]), o, 6*p+o, p, p, 'rry')
        }
        return
    
    # @log_method_call(logAttributes=False)
    def __display_piece_repository(self)->None:
        '''
        '''
        for key, piece in self.__piece_objects.items():
            piece.color = self.__color
            self.scene.addItem(piece)
            self.__game.registerPieceClickedEvent(piece)
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
    # @log_method_call(logAttributes=False)
    def playerNameLabelText(self, text:str):
        self.__nameLabel.setText(text)

    @property
    def color(self) -> QColor:
        return self.__color
    
    @color.setter
    # @log_method_call(logAttributes=False)
    def color(self, color: QColor):
        self.__color = color
        for piece in self.__piece_objects.values():
            piece.color = color
        return



