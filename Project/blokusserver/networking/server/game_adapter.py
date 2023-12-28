
from typing import Dict
from server.clientapi import ClientApi
from gamelogic import Game, BlokusPiece
import numpy as np
from server.logger import *


class GameAdapter:
    '''
    This class serves as an adapter between the game logic and the server.
    Its purpose is to decouple the game logic from the server. So developers can work independently on the game logic and the server.
    '''

    def __init__(self, lobbyId:str) -> None:
        self.__lobbyId = lobbyId
        self.__players:Dict[ClientApi:Dict[str:BlokusPiece]] = {}
        self.__game:Game = Game(20)
        self.__availablePlayerGameIds = [1,2,3,4]
        self.__currentPlayerTurn:ClientApi = None
        return

    
    def add_player(self, player:ClientApi):
        player.gamePlayerId = self.__availablePlayerGameIds.pop(0)
        self.__players[player] = self.__createPieces()
        return
    
    def remove_player(self, player:ClientApi):
        self.__availablePlayerGameIds.append(player.gamePlayerId)
        player.gamePlayerId = None
        self.__players.pop(player)
        return
    
    def start_game(self):
        #TODO: handle turn management
        self.__currentPlayerTurn = list(self.__players.keys())[0]
        return
    
    def place_piece(self, player:ClientApi, pieceId:str, x:int, y:int, rotation:int, flip:int):
        #TODO: check if player is current turn player
        #TODO: Rotation and flipping currently is not being used
        #TODO: instead of using the gamePlayerId, a player object should be used
        try:
            
            self.__game.placePieceByKey(pieceId, x, y, player.gamePlayerId, rotation=rotation, flip=flip)
            
        # except BlokusException as e:
        #     logger.info(f"piece could not be placed:")
        #     logger.error(e)
        except Exception as e:
            logger.critical(e)

        #TODO: determine player next turn
        #TODO: handle placement error/invalid placement
        p:ClientApi
        for p in self.__players:
            p.connection.emit_game_update(self.get_game_info())
        return


    # Helper Methods

    def get_game_info(self):
        return {
            'lobbyId': self.__lobbyId,
            'gameField': self.__game.getFeld.tolist(),
            'currentTurnPlayerId': self.__currentPlayerTurn.gamePlayerId,
            'players':{player.gamePlayerId: self.__get_player_info(player) for player,value in self.__players.items()}
        }

    def __get_player_info(self, player:ClientApi):
        playerInfo = player.get_player_Info()
        playerInfo['pieces'] = self.__game.getAvailablePieces(player.gamePlayerId)
        playerInfo['gamePlayerId'] = player.gamePlayerId
        return playerInfo

    def __createPieces(self):
        return {
            "1_0": BlokusPiece(np.array([[1]])),
            "2_0": BlokusPiece(np.array([[1, 1]])),
            "3_0": BlokusPiece(np.array([1, 1, 1])),
            "3_1": BlokusPiece(np.array([[0, 1], [1, 1]])),
            "4_0": BlokusPiece(np.array([[0, 1], [1, 1], [1, 0]])),
            "4_1": BlokusPiece(np.array([[1, 1], [1, 1]])),
            "4_2": BlokusPiece(np.array([[0, 1, 0], [1, 1, 1]])),
            "4_3": BlokusPiece(np.array([[1, 1, 1], [0, 0, 1]])),
            "4_4": BlokusPiece(np.array([[1, 1, 1, 1]])),
            "5_0": BlokusPiece(np.array([[0, 1], [1, 1], [1, 1]])),
            "5_1": BlokusPiece(np.array([[0, 1], [0, 1], [1, 1], [1, 0]])),
            "5_2": BlokusPiece(np.array([[1, 1, 1, 1], [0, 0, 0, 1]])),
            "5_3": BlokusPiece(np.array([[1, 1, 1, 1, 1]])),
            "5_4": BlokusPiece(np.array([[1, 1], [1, 0], [1, 1]])),
            "5_5": BlokusPiece(np.array([[0, 1, 1], [0, 1, 0], [1, 1, 0]])),
            "5_6": BlokusPiece(np.array([[0, 1, 1], [1, 1, 0], [1, 0, 0]])),
            "5_7": BlokusPiece(np.array([[0, 0, 1], [0, 0, 1], [1, 1, 1]])),
            "5_8": BlokusPiece(np.array([[0, 0, 1], [1, 1, 1], [0, 0, 1]])),
            "5_9": BlokusPiece(np.array([[0, 1, 0], [0, 1, 1], [1, 1, 0]])),
            "5_10": BlokusPiece(np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])),
            "5_11": BlokusPiece(np.array([[0, 1, 0, 0], [1, 1, 1, 1]]))
        }