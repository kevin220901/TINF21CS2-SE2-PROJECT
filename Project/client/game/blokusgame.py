
from __future__ import annotations
import json
import threading
from typing import Dict
from PyQt6 import QtGui
from PyQt6.QtGui import QKeyEvent, QPainter, QPainterPath
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

##################################################
## Author: Kai Pistol, Luis Eckert
##################################################


'''
REMARK:
    Please do not take the developers notes to serious. 
    Its just their way of dealing with the frustration and euphoria experienced while development. 

    Also a return statement is used after each mehthod to make the code more readable and to make it easier to see where a method ends.

    hth and best regards: the DEVS
'''

# TODO: This whole document needs to be refactored.


# TODO: move the logger to a seperate file
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
    '''
    This is a decorator, it adds loggig to a method. 
    When the method is called, the decorator logs the method call and the return value each in seperate entries.

    PARAMETERS:
        logAttributes (bool): if True, the attributes of the object are logged.

    EXCEPTIONS:
        This may result in an SerializationError if an attribute of the object is not serializable.
        To resolve this issue, implement a to_dict() method in the object. or set logAttributes to False ... lol

    EXAMPLES:
        1.  loggin whitout attributes

            @log_method_call()
            def your_method(self, ...)->None:
                ...
                return

        2.  logging with attributes
            @log_method_call(logAttributes=True)
            def your_method(self, ...)->None:
                ...
                return

        3.  implementing a to_dict() method in the object
            class YourClass:
                def __init__(self, ...)->None:
                    self.attribute1 = ...
                    self.attribute2 = ...
                    self.some_non_serializable_attribute = ...
                    ...
                @log_method_call(logAttributes=True)
                def your_method(self, ...)->None:
                    ... do stuff wothy of logging ...
                    return
                
                ...
                def to_dict(self):
                    return {
                        'attribute1': self.attribute1,
                        'attribute2': self.attribute2,
                        'some_non_serializable_attribute': {
                            self.some_non_serializable_attribute.attribute1, 
                            self.some_non_serializable_attribute.attribute2,
                            ...
                        }
                        ...
                    }
                ... you get the idea ... have fun xD
        
    DEVELOPERS NOTE:
        The log entries are in json format and are written to the log file. 
        (While each entry is a valid json object, the whole file is not a valid json object since it expects an 'eof' after the first entry ...
        ... did not care for now since it works and fullfills its purpose)
            
    '''
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


# mhhh magic numbers, yummy
#TODO: move to config file
TILE_SIZE = 21       # represents the size of one tile in the game field in pixels (width and height)
GAME_FIELD_SIZE = 20 # represents the size of the game field in tiles (width and height)



class PlacePieceEvent:
    '''
    This is a plain data structure for the place piece Signal in the GameScene class.
    All the properties are READ ONLY.
    '''
    def __init__(self, piece_id:str, x:float, y:float, operations:str) -> None:
        self.__piece_id = piece_id
        self.__x = x
        self.__y = y
        self.__operations = operations

    @property  
    def piece_id(self):
        return self.__piece_id
    
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
    
    @property
    def operations(self):
        return self.__operations

class PieceClickedEvent:
    '''
    This is an othe data structure nedded for the pieceClickedEvent Signal in the GamePiece class.
    All the properties are READ ONLY.
    '''
    def __init__(self, piece:GamePiece, mouseEvent:QGraphicsSceneMouseEvent) -> None:
        self._piece = piece
        self._mouseEvent = mouseEvent

    @property
    def piece(self):
        return self._piece
    
    @property
    def mouseEvent(self):
        return self._mouseEvent



class BlokusGame():
    '''
    This is the Main class of this module, it manages the whole game ui and contains all its ui elements.
    - the game field
    - the piece repository for each player: display of the player info and the available pieces
    - the chat: well its the chat ... 
    - the selected piece: the piece that is currently selected
    - the ghost piece: a ghost piece is a copy of the selected piece that is used to visualize the placement of the piece
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
        self.__register_ui_handlers()
        self.__add_menu_actions()
        self.__display_game_info()
        return
    

    def __add_menu_actions(self):
        self.mainWindow.leave_game_action.setVisible(True)
        self.mainWindow.leave_game_action.triggered.connect(self.__on_leave_game)
        return
    
    def __remove_menu_actions(self):
        self.mainWindow.leave_game_action.setVisible(False)
        self.mainWindow.leave_game_action.triggered.disconnect(self.__on_leave_game)
        
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
    

    def flipPieceY(self, piece:GamePiece):
        if piece:
            flipedGhost = GhostPiece(piece.player_id, 
                                          piece.piece_id, 
                                          piece.base_shape, 
                                          piece.x(), 
                                          piece.y(), 
                                          piece.width, 
                                          piece.height, 
                                          color=piece.color, 
                                          operations=piece.operations + 'y')
            flipedGhost.setVisible(True)
            self.ghostPiece = flipedGhost
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

        DEVELOPERS NOTE:
            nothing to say here but ... magic ... magic everywhere
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
        '''
        Handles the creation and deletion of the ghost piece.
        Also addes and removes the ghost piece from the games scene.

        DEVELOPERS NOTE:
            same note as in the selectedPiece setter ... 
        '''	

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
        self.blokus_widget = BlokusWidget(self)
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
                widget = PlayerAreaWidget(-1, self, False)
            else:
                playerId = playerInfo.get('playerId')
                isSelf = playerId == self.__network.api.accout_info.id
                widget = PlayerAreaWidget(playerInfo.get('playerId'), self, isSelf, color=QColor(playerInfo.get('color')))

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
        return
    
    # @log_method_call(logAttributes=False)
    def __unregisterNetworkEvents(self):
        '''
        Removes the network event handlers

        DEVELOPERS NOTE:
            This is especially needed when the game is closed and the user is redirected to the lobby.
            Dont want some scary ghostly network event handlers to lurk in the shadows and haunt the lobby. ;)
        '''
        self.__network.removeNetworkEventHandler(NetworkEvent.MESSAGE, self.__on_message)
        self.__network.removeNetworkEventHandler(NetworkEvent.GAME_UPDATE, self.__on_game_update)
        self.__network.removeNetworkEventHandler(NetworkEvent.GAME_INVALID_PLACEMENT, self.__on_game_invalid_placement)
        return

    # @log_method_call(logAttributes=False)
    def __register_ui_handlers(self):
        '''
        Initializes the ui event handlers and custom signals like:
        - button clicks 
        - key presses
        - piece placed
        '''
        #add button event handler
        self.chat_send_button.clicked.connect(self.__on_send_clicked)
        ##send message on enter
        self.chat_input.returnPressed.connect(self.chat_send_button.click)

        self.field_scene.piecePlacedEvent.connect(self.__on_place_piece)
        return
    
    def __unregister_ui_handlers(self):
        '''
        Removes the ui event handlers
        '''
        self.chat_send_button.clicked.disconnect(self.__on_send_clicked)
        self.chat_input.returnPressed.disconnect(self.chat_send_button.click)
        self.field_scene.piecePlacedEvent.disconnect(self.__on_place_piece)
        return
    
    def __on_leave_game(self, event=None):
        self.mainWindow.showAlert("You left the game")
        self.__unregisterNetworkEvents()
        self.__unregister_ui_handlers()
        self.__remove_menu_actions()
        
        #TODO: Unregister GamePieces
        self.__network.api.leaveLobby()

        self.blokus_widget.deleteLater()
        from lobby.lobbymenu import LobbyMenu
        self.lobbymenu = LobbyMenu(self.mainWindow, self.__network)
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
                tile = GameFieldElement(self, x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, QColor(255, 255, 255))
                self.field_scene.addItem(tile)
                row.append(tile)
            self.game_grid.append(row)

        
        
        self.central_layout.addWidget(self.field_view)

        return

    # @log_method_call(logAttributes=False)
    def __on_place_piece(self, event:PlacePieceEvent)->None:
        '''
        Notifies the Servere to place the piece

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
        return




class BlokusWidget(QWidget):
    '''
    This is the main ui container widget of BlokusGame.
    

    DEVELOPERS NOTE:
        This class is only needed to override the keyReleaseEvent method. That triggeres the flipy operation on the selected piece.
        We could propably move some more logic here but meh ... deadline in less than 6 hours. *sigh*
    '''
    def __init__(self, game:BlokusGame, parent=None):
        super().__init__(parent)
        self.__game = game
        return

    def keyReleaseEvent(self, event: QKeyEvent | None) -> None:
        '''
        Handles the 'global' key release events.
        '''
        if event.key() == Qt.Key.Key_Space:
            piece: GhostPiece = None
            # Get the selected item
            if self.__game.ghostPiece:
                if self.__game.ghostPiece in self.__game.field_scene.items():
                    if self.__game.ghostPiece.isVisible():
                        piece = self.__game.ghostPiece
            if piece:
                self.__game.flipPieceY(piece)
            else:
                return super().keyPressEvent(event)
        return 


class GameFieldElement(QGraphicsRectItem):
    '''
    This class is used to represent/visualize/render a single tile in the game field.
    
    DEVELOPERS NOTE:
        a field usually consists of more than one tile ... the more u know
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
    Represents a single game piece (blokus piece). 
    It provides custom rendering and mouse event handling.

    DEVELOPERS NOTE:
        Serves as base class for the GhostPiece just so you know
    '''

    class Signals(QObject):
        '''
        Since QGraphicsItemGroup is no QObject, it is not possible to define signals in the GamePiece class.
        This class is a workaround to define signals in the GamePiece class and thus remove the previous dependecy on BlokusGame class.
        
        TODO: 
        Check if this can be refactored. Dependecies may be inconvenient but still less complex then emitting signals and connecting to them.
        -> code is not as readable as it could and should be
        '''
        pieceClickedEvent = pyqtSignal(PieceClickedEvent)

    # @log_method_call(logAttributes=False)
    def __init__(self, player_id:int, piece_id:str, shape_array:np.ndarray, x, y, width, height, operations:str='', parent=None, color=QColor('lightgray')):
        '''
        Initializes the game piece ... who would have thought
        
        Parameters:
            player_id (int): the id of the player the piece belongs to (values 1-4)
            shape_array (np.array): the shape of the piece (this will be used as base_shape)
            x (int): the x position of the piece (pixels)
            y (int): the y position of the piece (pixels)
            width (int): the width of the piece (pixels)
            height (int): the height of the piece (pixels)
            parent (QWidget): the parent widget
            operations (str): sequence of chars {'r', 'x', 'y'} representing the operations that will be applied to the base_shape to get the actual shape_array

        '''
        super().__init__(parent)
        # self.__game:BlokusGame = game
        self.__base_shape_array = shape_array
        self.shape_array = shape_array
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
                self.__rotate90()
            elif o == 'x':
                self.flipX()
            elif o == 'y':
                self.flipY()

        # Set the position of the group
        self.setPos(x, y)
        return
    
    '''
    >>>> Properties
    '''
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
    
    @property
    def base_shape(self) -> np.array:
        return self.__base_shape_array
    
    @color.setter
    # @log_method_call(logAttributes=False)
    def color(self, color: QColor):
        self.__color = color
        if self.isVisible():
            self.update()
        return
    
    @isSelected.setter
    # @log_method_call(logAttributes=False)
    def isSelected(self, value:bool):
        # if value == self.__isSelected: return
        if self.isPlaced: return

        self.__isSelected = value
        # self.update()
        return

    '''
    Properties <<<<
    '''

    def to_dict(self):
        '''
        this method is recuires to serialize the object and to avoid a SerializationError when logging the object (see log_method_call decorator)
        '''
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
    
    #TODO: check if this is needed -> (mabye deprecated)
    # @log_method_call(logAttributes=True)
    def shape(self) -> QPainterPath:
        '''
        Returns the shape of the piece
        Needed for for collision detection

        Returns:
            QPainterPath: the shape of the piece

        DEVELOPERS NOTE:
            actually i dont know if this method is needed or not ... but I wont deal with that for now
        '''
        path = QPainterPath()
        for i in range(self.shape_array.shape[0]):  # iterate over rows
            for j in range(self.shape_array.shape[1]):  # iterate over columns
                if self.shape_array[i, j] == 1:  # 1 represents a part of the piece
                    path.addRect(QRectF(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return path
    
    # @log_method_call(logAttributes=True)
    def boundingRect(self)->QRectF:
        '''
        Calculates the smalest possible bounding rect for the piece

        Returns:
            QRectF: the bounding rect of the piece

        DEVELOPERS NOTE:
            other than the shape method, this method is actually needed ...  
        '''
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
        '''
        This method overrides the paint method of the QGraphicsItemGroup class. 
        It provides custom redering logic for the piece. 

        Parameters:
            painter (QPainter): the painter object
            option (QStyleOptionGraphicsItem): the style options
            widget (QWidget): the widget
        
        Returns:
            None
        
        DEVELOPERS NOTE:
            No need to call this method yourself since PyQt will do the magic internally. <3
            If you stil want to force a repaint, call the update() method of the piece
        '''
        if self.scene() is None:
            return
        painter.setBrush(self.__color)
        
        brightness = self.__color.lightness()

        if self.isSelected:  
            if brightness < 128:
                # color is dark -> use lighter border color as higthlight
                painter.setPen(QPen(self.__color.lighter(250), 4)) 

            else:   
                # color is light -> use darker border color as higthlight
                painter.setPen(QPen(self.__color.darker(250), 4))
        else:
            painter.setPen(QPen(QColor(0, 0, 0), 2))

        # Draw the piece
        for i in range(self.shape_array.shape[0]):
            for j in range(self.shape_array.shape[1]):
                if self.shape_array[i, j] == 1:  # 1 represents a part of the piece
                    painter.drawRect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        return   
    
    # @log_method_call(logAttributes=False)
    def __rotate90(self, n_times=1) -> None:
        '''
        Rotates the piece 90 degrees counter clockwise

        Parameters:
            n_times (int): the number of times the piece will be rotated 90 degrees counter clockwise (default = 1)

        Returns:
            None

        DEVELOPERS NOTE:
            Since the rotation was such a pain in the a** we decided to make it private.
            For now its only called in the constructor of the GamePiece class.
        '''
        self._operations += 'r'*n_times
        self.shape_array = np.rot90(self.shape_array, n_times)
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
        '''
        Handles the mouse press event for the game piece and emits the pieceClickedEvent signal:
        '''
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
        Creates a ghost piece from the game piece with identical properties
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
        '''
        this method is recuires to serialize the object and to avoid a SerializationError when logging the object (see log_method_call decorator)
        '''
        return {
            'game': self._game.to_dict()
        }   
    
    

    # @log_method_call(logAttributes=True)
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        '''
        Handles the mouse move event for the game scene:
            -   Move the ghostPiece to the mouse position and snap the grid
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
    def mousePressEvent(self, event:QGraphicsSceneMouseEvent)->None:
        '''
        Handles the mouse press event for the game scene:
        - left button click: 
            place the selected piece at the ghost piece's position
        
        - right button click: 
            rotate the ghost piece 90 degrees counter clockwise
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
        - checks if the ghost piece is valid
        - places the ghostPiece at mouse position
        - emits the piecePlacedEvent

        DEVELOPERS NOTE:
            The ghost isn't really placed, its just used for visualization. 
            The actual placement is done in the BlokusGame when GAME_UPDATE event is recieved from the server.
        '''
        if self._game.ghostPiece is None: return    #TODO: why does the placement depend on the ghost piece? -> check this and leave a comment
        if self._game.ghostPiece not in self.items(): return
        if self._game.ghostPiece.isVisible() == False: return

        piece = self._game.ghostPiece

        pos = event.scenePos()
        pieceEvent = PlacePieceEvent(piece.piece_id, pos.x(), pos.y(), piece.operations)
        if piece:
            self.piecePlacedEvent.emit(pieceEvent)
        return
    
    # @log_method_call(logAttributes=False)
    def __on_right_click(self, event: QGraphicsSceneMouseEvent) -> None:
        '''
        Handles the mouse press event for the game scene:
        - if there is a ghost piece, rotate the ghost piece 90 degrees counter clockwise
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

    DEVELOPERS NOTE:
        mouse move event enter and leave events are needed to show and hide the ghost piece correctly
        maby not the most elegant solution but it works so ... well done me :D
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
    
    def enterEvent(self, event: QEvent) -> None:
        self.setFocus()

        if self.__game.selectedPiece:
            if self.__game.ghostPiece:
                if self.__game.ghostPiece in self.scene().items():
                    if self.__game.ghostPiece.isVisible() == False:
                        self.__game.ghostPiece.setVisible(True)

        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        if self.__game.selectedPiece:
            if self.__game.ghostPiece:
                if self.__game.ghostPiece in self.scene().items():
                    if self.__game.ghostPiece.isVisible():
                        self.__game.ghostPiece.setVisible(False)
        super().leaveEvent(event)
    
    def to_dict(self)->dict:
        return {
            'game': self.__game.to_dict()
        }

    # @log_method_call(logAttributes=True)
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        '''
        Handles the mouse move event for the game view:
        -   shows and hides the ghost piece if the mouse is within predifined borders

        DEVELOPERS NOTE:
            The predefined borders are not working correctly when resizing the window or when the window is NOT maximized.
        '''
        # Calling the original mouseMoveEvent to keep its functionality (moving the ghostPiece around)
        super().mouseMoveEvent(event)
        if self.__game.ghostPiece is None: return
        if self.__game.ghostPiece not in self.scene().items(): return

        # Get the mouse position in scene coordinates
        mouse_pos = self.mapToScene(event.pos())
        ghost = self.__game.ghostPiece

        # Check if the mouse is inside the GameFieldBorder
        if not self.field_border.contains(mouse_pos):
            # out of border, hide ghost piece
            if ghost is None: return
            if ghost not in self.scene().items(): return

            ghost.setVisible(False)
        else:
            # in border, show ghost piece
            if ghost is None: return
            if ghost not in self.scene().items(): return
            
            ghost.setVisible(True)
        return

    




class GhostPiece(GamePiece):
    '''
    Represents a ghost piece that is displayed when a piece is selected.
    
    The ghost piece is used to show the player where the piece will be placed.
    The ghost piece is not selectable and does not capture mouse events on its own.
    it has to be updated from the outside
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
        '''
        Overides the clone method of the GamePiece class
        
        Returns:
            GhostPiece: a (deep) copy of the ghost piece

        DEVELOPERS NOTE:
            not sure if actually needed ... more things to check later ... more like never lol; 
            Deadline is coming ... 
        '''
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
    '''
    Represents the player area and its ui elements
    - player name (Label)
    - piece repository (QGraphicsView)
    - available pieces (GamePieces)
    '''
    def __init__(self, player_id:int, game: BlokusGame, isSelf:bool, parent=None, color: QColor = QColor('lightgray')):
        super().__init__(parent=parent)
        self.__game:BlokusGame = game
        self.__color:QColor = color
        self.__piece_objects:Dict[str:GamePiece]
        self.player_id = player_id
        self.__isSelf = isSelf

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
        Updates the available pieces in the piece repository by showing or hiding the pieces based on the provided list of available pieces

        PARAMETERS:
            availablePieces (list): the list of available pieces
        
        RETURNS:
            None
        
        DEVELOPERS NOTE:
            This method is called when the game info is updated. It iterates over the internal kept list of pieces
            The initialization of the pieces has to be kept in sync with the server side implementation since the pieces ids and shapes corresponde
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
        Displays the piece repository in the QGraphicsView by adding the pieces to the scene

        RETURNS:
            None

        DEVELOPERS NOTE:
            for each piece in the repository a pieceClickedEvent signal is registered in the BlokusGame class.
            On handling the signal the selected piece is being managed.
            Could perhaps be done in a more elegant way ... but deadline is coming ... 
            ... and the rotation bug was one hell of a bug ... over 20h ... so ... yeah the code got a bit messy on the go 
            ... long live the refactoring *hurray*
        '''
        for key, piece in self.__piece_objects.items():
            piece.color = self.__color
            self.scene.addItem(piece)
            if self.__isSelf:
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

    @playerNameLabelText.setter
    # @log_method_call(logAttributes=False)
    def playerNameLabelText(self, text:str):
        new_text = text
        if self.__isSelf:
            new_text += ' (YOU)'

        self.__nameLabel.setText(new_text)


