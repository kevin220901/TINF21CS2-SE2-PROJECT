
from ast import Tuple
import random
import traceback
from typing import Dict, List
from server.clientapi import ClientApi
from gamelogic import Game, BlokusPiece, BlokusException
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
        self.__currentTurnPlayer:ClientApi = None
        self.__turnOrder:List[ClientApi] = []
        self.__hasEnded = False
        self.winners:List[ClientApi] = []
        return

    
    def add_player(self, player:ClientApi):
        player.gamePlayerId = self.__availablePlayerGameIds.pop(0)
        self.__players[player] = self.__createPieces()
        self.__turnOrder.append(player)
        return
    
    def remove_player(self, player:ClientApi):
        self.__availablePlayerGameIds.append(player.gamePlayerId)
        player.gamePlayerId = None
        self.__players.pop(player)
        self.__turnOrder.remove(player)
        return
    
    def start_game(self):
        random.shuffle(self.__turnOrder)
        self.__currentTurnPlayer = self.__turnOrder[0]
        return
    
    def __change_turn(self):
        currentTurn = self.__turnOrder.pop(0)
        self.__turnOrder.append(currentTurn)
        self.__currentTurnPlayer = self.__turnOrder[0]
        return
    
    def place_piece(self, player:ClientApi, pieceId:str, x:int, y:int, operations:bytes):
        try:
            if player != self.__currentTurnPlayer:
                raise BlokusException('it is not your turn')

            self.__game.placePieceByKey(pieceId, x, y, player.gamePlayerId, operations)


            self.__hasEnded = self.__game.getAvailablePieces(player.gamePlayerId) == []
                
            if self.__hasEnded:
                self.winners.append(player)
            else:
                self.__change_turn()
                p:ClientApi
                for p in self.__players:
                    p.connection.emit_game_update(self.get_game_info())
           
        except BlokusException as e:
            player.connection.emit_game_invalidPlacement(str(e))
            player.connection.emit_game_update(self.get_game_info())
            logger.debug(e)
        except Exception as e:
            logger.critical(f'{str(e)} \n {traceback.format_exc()}')
            # notify players (in this game/lobby) about the error
            for p in self.__players:
                p.connection.emit_SysMessage(f'Internal server error occured')
        return


    # Helper Methods

    def get_game_info(self):
        return {
            'lobbyId': self.__lobbyId,
            'gameField': self.__game.getFeld.tolist(),
            'currentTurnPlayer': self.__currentTurnPlayer.get_player_Info(),
            'players':{player.gamePlayerId: self.__get_player_info(player) for player,value in self.__players.items()},
            'messages':[]
        }

    def __get_player_info(self, player:ClientApi):
        playerInfo = player.get_player_Info()
        playerInfo['pieces'] = self.__game.getAvailablePieces(player.gamePlayerId)
        playerInfo['gamePlayerId'] = player.gamePlayerId
        return playerInfo
    
    def __createPieces(self):
        #TODO: Refactor, only the keys are needed
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
    

    @property
    def hasEnded(self):
        return self.__hasEnded
