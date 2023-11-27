
from __future__ import annotations





class ClientApi:
    def __init__(self, conn:socket, playerId, playerName, lobbies, logger) -> None:
        self.__conn = SocketWrapper(conn)
        self.__currentLobby:Lobby = None
        self.__playerId:str = playerId
        self.__playerName:str = playerName
        self.lobbies:dict = lobbies
        self.logger:Logger = logger

    def createLobby(self, lobbyName):
        if self.__handleAllreadyInLobby(): return
        if self.__handleLobbyExists(lobbyName): return

        #TODO:the LobbyName must replaced with an actual, UNIQUE lobby id
        self.logger.info(f'created lobby "{lobbyName}"')
        newLobby = Lobby(lobbyName, self.lobbies)
        self.__currentLobby = newLobby
        newLobby.join(self)
        return newLobby

    def joinLobby(self, lobbyId):
        if self.__handleAllreadyInLobby(): return
        if self.__handleLobbyNotFound(lobbyId): return
        
        selectedLobby:Lobby = self.lobbies[lobbyId]
        
        if self.__handleLobbyNotJoinable(selectedLobby): return

        self.__currentLobby = selectedLobby
        self.__currentLobby.join(self)

        return selectedLobby

    def leaveLobby(self):
        if self.__handleNotInLobby(): return
        self.__currentLobby.leave(self)
        self.__currentLobby = None
        pass

    def sendMessage(self, message):
        if self.__handleNotInLobby(): return

        self.__currentLobby.broadcastMessage(self, message)

        pass

    def sendSysMessage(self, message):
        self.__conn.sendall(NetworkEvent.SYSMESSAGE, {'message':message})
        pass

    def sendLobbyBrowsingResult(self, joinableLobbies):
        self.__conn.sendall(NetworkEvent.LOBBIES_GET, joinableLobbies)

    def recvMessage(self, sender:str, message):
        self.__conn.sendall(NetworkEvent.MESSAGE, {'from':sender, 'messsage':message})
        pass

    def toggleReady(self):
        if self.__handleNotInLobby(): return
        self.__currentLobby.toggleReady(self)
        pass

    def notifyGameStarted(self):
        #TODO: transmitt who plays first
        self.__conn.sendall(NetworkEvent.GAME_START, {'turn':'dummy info :P'})
        pass
    

    def __handleAllreadyInLobby(self) -> bool:
        if self.__currentLobby:
            self.sendSysMessage('allready in a lobby')
            return True
        return False
    
    def __handleLobbyExists(self, lobbyName):
        if lobbyName in self.lobbies:
            self.sendSysMessage('lobby allready exists')
            return True
        return False
    
    def __handleLobbyNotFound(self, lobbyName):
        if lobbyName not in self.lobbies:
            self.sendSysMessage('lobby not found')
            return True
        return False
    
    def __handleLobbyNotJoinable(self, lobby:Lobby):
        if lobby.cantBeJoined:
            self.sendSysMessage('lobby not joinable')
            return True
        return False
    
    def __handleNotInLobby(self):
        if not self.__currentLobby:
            #check connection still open
            self.sendSysMessage('not in a lobby')
            return True
        return False


    @property
    def playerName(self):
        return self.__playerName
    
    @property
    def playerId(self):
        return self.__playerId
    
    @property
    def currentLobbyId(self):
        if not self.__currentLobby: return ''
        return self.__currentLobby.lobbyId

    @property
    def currentLobby(self):
        return self.__currentLobby
    
from socket import socket
from networking.lobby import Lobby
from networking.server.clientsocketwrapper import ClientSocketWrapper
from networking.socketwrapper import SocketWrapper
from networking.networkevent import NetworkEvent
from logging import Logger
