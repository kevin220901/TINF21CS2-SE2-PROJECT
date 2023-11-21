

import secrets


class Lobby:
    def __init__(self) -> None:
        self.__lobbyId = secrets.token_bytes(32)
        self.__players = set()

    def join(self, player):
        self.__players.add(player)
        
    def leave(self, player):
        self.__players.remove(player)

    def getPlayers(self):
        return self.__players.copy()
    
    def getLobbyId(self):
        return self.__lobbyId

