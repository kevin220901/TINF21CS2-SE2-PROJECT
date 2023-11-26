from __future__ import annotations


class Lobby:
    def __init__(self, lobbyId, lobbies) -> None:
        self.__lobbies = lobbies
        self.__lobbyId = lobbyId#secrets.token_bytes(32)
        self.__players = set()
        self.__canBeJoined:bool = True
        self.__isPrivate: bool = False
        self.__ready = {}
        self.__host: ClientApi = None

    def join(self, player:ClientApi):
        self.__players.add(player)
        self.__ready[player] = False
    
        self.__handleHostGone()
        pass
        
    def leave(self, player:ClientApi):
        self.__players.remove(player)
        self.__ready.pop(player)
        if self.__handleLobbyAbbandoned(): return
        self.__handleHostGone()
        pass

    def toggleReady(self, player:ClientApi):
        self.__ready[player] = ~self.__ready[player]
        pass

        

    def getPlayers(self):
        return self.__players.copy()
    
    def getLobbyId(self):
        return self.__lobbyId
    
    def sendMessage(self, player:ClientApi, message):
        for p in self.__players:
            p.sendall(NetworkEvent.MESSAGE, {'message':message})

    def sendSysMessage(self, sysmessage):
        for p in self.__players:
            p.sendall(NetworkEvent.SYSMESSAGE, {'sysmessage':sysmessage})

    def __handleLobbyAbbandoned(self):
        if self.playerCount == 0: 
                self.__lobbies[self] = None
                return True
        return False

    def __handleHostGone(self):
        if not self.__host:
            #pick first next player and assign as new host
            newHost = next(iter(self.__players))
            self.__host = newHost
            return True
        return False





    @property
    def canBeJoined(self) -> bool:
        return self.__canBeJoined
    
    @property
    def cantBeJoined(self) -> bool:
        return not self.__canBeJoined
    
    @property
    def playerCount(self) -> int:
        return len(self.__players)


import secrets
from networking.server.clientapi import ClientApi

from networking.networkevent import NetworkEvent
