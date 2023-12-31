
from __future__ import annotations
import json
import threading
from typing import Set
import requests
import common.constants as NetworkConst
from server.logger import *

##################################################
## Author: Luis Eckert
##################################################


class ClientApi:
    def __init__(self, conn:socket, stopEvent:threading.Event, lobbies, loggedInPlayers:Set) -> None:
        self.__conn = ClientSocketWrapper(conn)
        self.__currentLobby:Lobby = None
        self.__playerId:str = None
        self.__playerName:str = None
        self.lobbies:dict = lobbies
        self.__auth_token = None
        self.__stopEvent = stopEvent
        self.__gamePlayerId = None
        self.__colorName:str = None # name of the color
        self.__isReady = False
        self.__currentGame:GameAdapter = None
        self.__loggedInPlayers = loggedInPlayers
        return

    

    def login(self, username, password):
        auth_data = {'username':username,'password':password}
        response = requests.post(NetworkConst.URL_RESTAPI_LOGIN,data=auth_data)
        logger.info(response)
        if response.status_code != 200:
            self.__conn.emit_Login_fail()
            return False
        
        response_data = json.loads(response.content)

        player_id:str =  response_data['id']

        if player_id in self.__loggedInPlayers:

            self.__conn.emit_Login_fail('sombody is allready logged in with this account')
            return False
        
        self.__loggedInPlayers.add(player_id)

        self.__auth_token = response_data['token']
        self.__playerId = player_id
        self.__playerName = response_data['username']


        self.__conn.emit_Login_success(self.__auth_token, self.__playerId, self.__playerName)

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
        self.__conn.emit_profile_updated('profile updated')

        return True
    
    def updateProfilePassword(self, token, new_password):
        data = {'new_password':new_password}
        response = requests.put(url=NetworkConst.URL_RESTAPI_PROFILE_UPDATE_PASSWORD, 
                                headers={'Authorization': f'Token {token}'}, 
                                data=data)
        
        if response.status_code == 401:
            logger.critical(f'access denied for user:{self.playerId}')
            self.__conn.emit_SysMessage('access denied')
            return False
        elif response.status_code != 200:
            logger.critical(f'failed to update password for user:{self.playerId}')
            self.__conn.emit_SysMessage('failed to update password')
            return False
        response_data = json.loads(response.content)

        self.__auth_token = response_data['token']
        self.__playerId = response_data['id']
        self.__playerName = response_data['username']
        
        self.__conn.emit_profile_updated_password(self.__auth_token, self.__playerId, self.__playerName)

        return True
        
    def deleteProfile(self, token):
        response = requests.delete(url=NetworkConst.URL_RESTAPI_PROFILE, 
                                   headers={'Authorization': f'Token {token}'})
        
        if response.status_code == 401:
            logger.critical('access denied')
            self.__conn.emit_SysMessage('access denied')
            return False
        elif response.status_code != 200:
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
        # cleanup after leaving the lobby
        self.__currentLobby = None
        self.__colorName = None
        self.__isReady = False
        pass

    def toggleReady(self, emitUpdate=True):
        if self.__handleNotInLobby(): return
        self.__isReady = not self.__isReady
        self.__currentLobby.toggleReady(self,emitUpdate)
        return
    
    def startGame(self):
        if self.__handleNotInLobby(): return
        game = self.__currentLobby.startGame(self)
        return
    
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
        if lobby.playerCount >= NetworkConst.MAX_PLAYERS_PER_LOBBY:
            self.__conn.emit_SysMessage('lobby full')
            return True

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
    
    def get_player_Info(self) -> dict:
        return {
            'playerId': self.playerId,  # TODO: should be named id or user_id
            'playerName': self.playerName,
            'isReady': self.isReady,
            'color': self.colorName
        }

    @property
    def playerName(self)->str:
        return self.__playerName
    
    @property
    def playerId(self)->str:
        return self.__playerId
    
    @property
    def currentLobbyId(self)->str:
        if not self.__currentLobby: return ''   #TODO:This does not seem appropriate
        return self.__currentLobby.lobbyId

    @property
    def currentLobby(self)->Lobby:
        return self.__currentLobby
    
    @property
    def currentGame(self)->GameAdapter:
        return self.__currentGame
    
    @currentGame.setter
    def currentGame(self, game:GameAdapter)->None:
        self.__currentGame = game
        return

    @property
    def hasAuthToken(self)->bool:
        if not self.__auth_token:
            return False
        return True
    
    @property
    def authToken(self) -> str:
        return self.__auth_token
    
    @property
    def connection(self)->ClientSocketWrapper:
        return self.__conn

    @property
    def gamePlayerId(self)->int:
        return self.__gamePlayerId
    
    @gamePlayerId.setter
    def gamePlayerId(self, id) -> None:
        self.__gamePlayerId = id
        return
    
    @property
    def isReady(self)->bool:
        return self.__isReady
    
    @property
    def colorName(self)->str:
        return self.__colorName
    
    @colorName.setter
    def colorName(self, colorName:str)->None:
        self.__colorName = colorName
        return

    
from socket import socket
from server.lobby import Lobby
from server.clientsocketwrapper import ClientSocketWrapper
from server.game_adapter import GameAdapter

