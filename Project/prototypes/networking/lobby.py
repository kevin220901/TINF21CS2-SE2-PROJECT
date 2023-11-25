

import secrets

from networking.networkevent import NetworkEvent


class Lobby:
    def __init__(self, lobbyId) -> None:
        self.__lobbyId = lobbyId#secrets.token_bytes(32)
        self.__players = set()

    def join(self, player):
        self.__players.add(player)
        
    def leave(self, player):
        self.__players.remove(player)

    def getPlayers(self):
        return self.__players.copy()
    
    def getLobbyId(self):
        return self.__lobbyId
    
    def sendMessage(self, player, message):
        for p in self.__players:
            p.sendall(NetworkEvent.MESSAGE, {'message':message})
