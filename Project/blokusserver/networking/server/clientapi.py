
from __future__ import annotations
import json
import threading
import requests
import common.constants as NetworkConst
from server.logger import *

##################################################
## Author: Luis Eckert
##################################################


class ClientApi:
    def __init__(self, conn:socket, stopEvent:threading.Event, lobbies) -> None:
        self.__conn = SocketWrapper(conn)
        self.__currentLobby:Lobby = None
        self.__playerId:str = None
        self.__playerName:str = None
        self.lobbies:dict = lobbies
        self.__auth_token = None
        self.__stopEvent = stopEvent

    def login(self, username, password):
        auth_data = {'username':username,'password':password}
        response = requests.post(NetworkConst.URL_RESTAPI_LOGIN,data=auth_data)
        logger.info(response)
        if response.status_code != 200:
            self.__stopEvent.set()
            self.sendSysMessage('access denied')
            return False
        
        response_data = json.loads(response.content)

        self.__auth_token = response_data['token']
        self.__playerId = response_data['id']
        self.__playerName = response_data['username']

        self.sendSysMessage('login successful')

        return True




    def createLobby(self, lobbyName):
        if self.__handleAllreadyInLobby(): return
        if self.__handleLobbyExists(lobbyName): return

        #TODO:the LobbyName must replaced with an actual, UNIQUE lobby id
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
        if not self.__currentLobby: return ''   #TODO:This does not seem appropriate
        return self.__currentLobby.lobbyId

    @property
    def currentLobby(self):
        return self.__currentLobby
    
    @property
    def hasAuthToken(self):
        if not self.__auth_token:
            return False
        return True
    
    @property
    def authToken(self):
        return self.__auth_token
    

    
from socket import socket
from server.lobby import Lobby
from server.clientsocketwrapper import ClientSocketWrapper
from common.socketwrapper import SocketWrapper
from common.networkevent import NetworkEvent
