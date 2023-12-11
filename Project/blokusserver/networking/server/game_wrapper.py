
from server.clientapi import ClientApi
from gamelogic import Game


class GameWrapper:

    def __create_player_game_info(self, player:ClientApi):
        return {
            'playerId': player.playerId,
            'playerName': player.playerName,
            'pieces': player.pieces,
            'color': player.color
        }

    def __get_game_info(self):
        return {
            'lobbyId': self.__lobbyId,
            'gameField': self.__game.get_game_field(),
            'currentTurnPlayerId': self.__game.get_current_turn_player_id(),
            'players':[
                {
                    'playerId': player.playerId,
                    'playerName': player.playerName,
                    'pieces': player.pieces,
                    'color': player.color
                } for player in self.__players
            ]
        }