
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
        self.__conn = ClientSocketWrapper(conn)
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
            self.__conn.emit_Login_fail()
            return False
        
        response_data = json.loads(response.content)

        self.__auth_token = response_data['token']
        self.__playerId = response_data['id']
        self.__playerName = response_data['username']

        self.__conn.emit_Login_success(self.__auth_token)

        return True

    def register(self, username, password, email):
        auth_data = {'username':username,'password':password, 'email':email}
        response = requests.post(NetworkConst.URL_RESTAPI_REGISTER,data=auth_data)
        logger.info(response)
        if response.status_code != 201:
            self.__conn.emit_SysMessage('registration failed')
            return False

        self.__conn.emit_Registration_success()

        return True
    
    def readProfile(self, token):
        response = requests.get(NetworkConst.URL_RESTAPI_PROFILE, headers={'Authorization': f'Token {token}'})

        if response.status_code == 401:
            logger.critical('access denied')
            self.__conn.emit_SysMessage('access denied')
            return False
        elif response.status_code != 200:
            logger.critical('failed to read profile')
            self.__conn.emit_SysMessage('failed to read profile')
            return False

        response_data = json.loads(response.content)

        self.__conn.emit_Profile_read(response_data)

        return True
    
    def updateProfile(self, token, username, email):
        data = {'username':username,'email':email}
        response = requests.put(url=NetworkConst.URL_RESTAPI_PROFILE, 
                                headers={'Authorization': f'Token {token}'}, 
                                data=data)
        
        if response.status_code == 401:
            logger.critical('access denied')
            self.__conn.emit_SysMessage('access denied')
            return False
        elif response.status_code != 200:
            logger.critical('failed to update profile')
            self.__conn.emit_SysMessage('failed to update profile')
            return False
        self.__conn.emit_SysMessage('profile updated')

        return True
        
    def deleteProfile(self, token):
        response = requests.delete(url=NetworkConst.URL_RESTAPI_PROFILE, 
                                   headers={'Authorization': f'Token {token}'})
        
        if response.status_code == 401:
            logger.critical('access denied')
            self.__conn.emit_SysMessage('access denied')
            return False
        elif response.status_code != 204:
            logger.critical('failed to delete profile')
            self.__conn.emit_SysMessage('failed to delete profile')
            return False
        self.__auth_token = None
        self.__conn.emit_profile_deleted()

        return True

    def createLobby(self, lobbyId):
        if self.__handleAllreadyInLobby(): return
        if self.__handleLobbyExists(lobbyId): return

        newLobby = Lobby(lobbyId, self.lobbies)
        self.__currentLobby = newLobby
        logger.info(f"lobby {newLobby.lobbyId} created")
        newLobby.join(self)
        lobbyInfo = newLobby.get_lobby_info()
        self.__conn.emit_LobbyCreate_success(lobbyInfo)
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

    def toggleReady(self):
        if self.__handleNotInLobby(): return
        self.__currentLobby.toggleReady(self)
        pass
    
    def __handleAllreadyInLobby(self) -> bool:
        if self.__currentLobby:
            self.__conn.emit_SysMessage('allready in a lobby')
            return True
        return False
    
    def __handleLobbyExists(self, lobbyId):
        if lobbyId in self.lobbies:
            self.__conn.emit_SysMessage('lobby allready exists')
            return True
        return False
    
    def __handleLobbyNotFound(self, lobbyId):
        if lobbyId not in self.lobbies:
            self.__conn.emit_SysMessage('lobby not found')
            return True
        return False
    
    def __handleLobbyNotJoinable(self, lobby:Lobby):
        if lobby.cantBeJoined:
            self.__conn.emit_SysMessage('lobby not joinable')
            return True
        return False
    
    def __handleNotInLobby(self):
        if not self.__currentLobby:
            #check connection still open
            self.__conn.emit_SysMessage('not in a lobby')
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
    
    @property
    def connection(self):
        return self.__conn

    
from socket import socket
from server.lobby import Lobby
from server.clientsocketwrapper import ClientSocketWrapper
from common.socketwrapper import SocketWrapper
from common.networkevent import NetworkEvent
