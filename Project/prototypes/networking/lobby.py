from __future__ import annotations


class Lobby:
    def __init__(self, lobbyName, lobbies:dict) -> None:
        self.__lobbies = lobbies
        self.__lobbyName = lobbyName 
        self.__lobbyId = lobbyName #secrets.token_bytes(32)
        self.__players = []
        self.__canBeJoined:bool = True
        self.__isPrivate: bool = False
        self.__ready = {}
        self.__host: ClientApi = None

        #WARNING: currently no checks are performed to ensure uniqueness of a lobbyId -> lobbies might get overwritten
        self.__lobbies[self.__lobbyId] = self

    def join(self, player:ClientApi):
        self.__players.append(player)
        self.__ready[player] = False
        player.logger.info(f'"{player.playerName}" joined lobby "{self.lobbyId}"')
        self.__notifyAll(f"new player {player.playerName} has joined the lobby.")
        self.__handleHostGone()
        pass
        
    def leave(self, player:ClientApi):
        self.__players.remove(player)
        self.__ready.pop(player)
        if self.__handleLobbyAbbandoned(): return
        
        self.__notifyAll(f"{player.playerName} has left the lobby.")
        self.__handleHostGone()
        pass

    def toggleReady(self, player:ClientApi):
        ready = ~self.__ready[player]
        self.__ready[player] = ready
        self.__notifyAll(f"{player.playerName} is {'ready' if ready else 'not ready'}")
        pass

    def chatMessage(self, sender:ClientApi, message):
        for p in self.__players:
            p.recvMessage(sender.playerName, message)
        pass
    
    
   
    def sendSysMessage(self, sysmessage):
        for p in self.__players:
            p.sendSysMessage(sysmessage)

    def __notifyAll(self, message):
        self.sendSysMessage(message)
        pass

    def __handleLobbyAbbandoned(self):
        if self.playerCount == 0: 
                self.__lobbies[self] = None
                return True
        return False

    def __handleHostGone(self):
        if not self.__host:
            #pick first next player and assign as new host
            newHost:ClientApi = next(iter(self.__players))
            self.__host = newHost
            newHost.logger.info(f'"{newHost.playerName}" is now host of "{self.lobbyId}"')
            self.__notifyAll(f"{newHost.playerName} is now host.")
            return True
        return False



    @property
    def lobbyId(self) -> str:
        return self.__lobbyId

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
