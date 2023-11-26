
from __future__ import annotations

class ClientApi:
    def __init__(self, conn:socket, playerId, playerName, lobbies) -> None:
        self.__conn = ClientSocketWrapper(conn)
        self.__lobby:Lobby = None
        self.__playerId:str = playerId
        self.__playerName:str = playerName
        self.__lobbies:[str,Lobby] = lobbies

    def createLobby(self, lobbyName):
        if self.__handleAllreadyInLobby(): return
        if self.__handleLobbyExists(lobbyName): return

        #TODO:the LobbyName must replaced with an actual, UNIQUE lobby id
        newLobby = Lobby(lobbyName)
        newLobby.join(self)
        return newLobby

    def joinLobby(self, lobbyId):
        if self.__handleAllreadyInLobby(): return
        if self.__handleLobbyNotFound(lobbyId): return
        
        selectedLobby:Lobby = self.__lobbies[lobbyId]
        
        if self.__handleLobbyNotJoinable(selectedLobby): return

        self.__lobby = selectedLobby
        self.__lobby.join(self)
        pass

    def leaveLobby(self):
        if self.__handleNotInLobby(): return
        self.__lobby.leave(self)
        self.__lobby = None
        pass

    def sendMessage(self, message):
        if self.__handleNotInLobby(): return
        self.__lobby.sendMessage(self, message)
        pass

    def sendSysMessage(self, message):
        self.__conn.sendSysMessage(message)
        pass

    def recvMessage(self, message):
        if not self.__lobby: pass #player is currently not in a lobby -> abbort recv
        pass

    def toggleReady(self):
        if self.__handleNotInLobby(): return
        self.__lobby.toggleReady(self)
        pass


    def __handleAllreadyInLobby(self) -> bool:
        if self.__lobby:
            self.__conn.sendSysMessage('can not create lobby')
            return True
        return False
    
    def __handleLobbyExists(self, lobbyName):
        if lobbyName in self.__lobbies:
            self.__conn.sendSysMessage('lobby allready exists')
            return True
        return False
    
    def __handleLobbyNotFound(self, lobbyName):
        if lobbyName not in self.__lobbies:
            self.__conn.sendSysMessage('lobby not found')
            return True
        return False
    
    def __handleLobbyNotJoinable(self, lobby:Lobby):
        if lobby.cantBeJoined:
            self.__conn.sendSysMessage('lobby not joinable')
            return True
        return False
    
    def __handleNotInLobby(self):
        if not self.__lobby:
            self.__conn.sendSysMessage('can not leave')
            return True
        return False
    


    @property
    def playerName(self):
        return self.__playerName
    
    @property
    def playerId(self):
        return self.__playerId
    

from socket import socket
from networking.lobby import Lobby
from networking.server.clientsocketwrapper import ClientSocketWrapper

