from __future__ import annotations
import uuid
from server.logger import *

##################################################
## Author: Luis Eckert
##################################################

class Lobby:
    def __init__(self, lobbyId, lobbies:dict) -> None:
        self.__lobbies = lobbies
        self.__lobbyId = lobbyId
        self.__players = {}
        self.__canBeJoined:bool = True #TODO: redundand information -> replace with validation of playerCount and isPrivate
        self.__isPrivate: bool = False #not yet needed 
        self.__host: ClientApi = None
        self.__game: any = None #not yet needed

        #WARNING: currently no checks are performed to ensure uniqueness of a lobbyId -> lobbies might get overwritten
        self.__lobbies[self.__lobbyId] = self


    def get_lobby_info(self):
        return {
            'lobbyId': self.__lobbyId,
            'host': self.__players[self.__host],
            'players': [info for player, info in self.__players.items() if player != self.__host],
            'aiDifficulty': 'not yet implemented',
            'messages':[]            
        }

    def __createPlayerInfo(self, player:ClientApi):
        return {
            'playerId': player.playerId,
            'playerName': player.playerName,
            'isReady': False,
            'color': 'not yet implemented'
        }

    def join(self, player:ClientApi):
        self.__players[player] = self.__createPlayerInfo(player)
        
        if self.playerCount > 1: 
            lobbyInfo = self.get_lobby_info()
            lobbyInfo['messages'].append(f'{player.playerName} joined')

            if self.__handleHostGone():
                lobbyInfo['host'] = self.__players[self.__host]
                lobbyInfo['messages'].append(f'{self.__host.playerName} is the new host')
            
            #Notify all players in lobby about the change
            p: ClientApi
            for p in self.__players:
                if p == player:
                    p.connection.emit_LobbyJoin_success(lobbyInfo)
                else:
                    p.connection.emit_lobby_update(lobbyInfo)
        else:
            #first player to join is the host
            self.__host = player
        pass
        
    def leave(self, player:ClientApi):
        self.__players.pop(player)
        if self.__handleLobbyAbbandoned(): return
        if self.__host == player:
            self.__host = None
        
        if self.__handleHostGone():
            lobbyInfo = self.get_lobby_info()
            lobbyInfo['messages'].append(f'{player.playerName} left')
            lobbyInfo['messages'].append(f'{self.__host.playerName} is the new host')
        else:
            lobbyInfo = self.get_lobby_info()
            lobbyInfo['messages'].append(f'{player.playerName} left')

        #Notify all players in lobby about the change
        p: ClientApi
        for p in self.__players:
            p.connection.emit_lobby_update(lobbyInfo)
       
        pass

    def toggleReady(self, player:ClientApi):
        newReadyState = not self.__players[player]['isReady']
        self.__players[player]['isReady'] = newReadyState

        lobbyInfo = self.get_lobby_info()
        p: ClientApi
        for p in self.__players:
            p.connection.emit_lobby_update(lobbyInfo)
        pass

    def broadcastMessage(self, sender:ClientApi, message):
        p:ClientApi
        for p in self.__players:
            p.connection.emit_Message(sender.playerName, message)
        pass

    def startGame(self, player:ClientApi):
        if self.__handleMissingPermission(player): return
        if self.__handleLobbyIsNotReady(): return
        
        self.__canBeJoined = False
        #TODO: start game

        p:ClientApi
        for p in self.__players:
            p.connection.emit_start_game({'messages':'game started'})
        pass

    def __handleLobbyAbbandoned(self):
        if self.playerCount == 0: 
                self.__lobbies.pop(self.__lobbyId)
                logger.info(f"lobby '{self.__lobbyId}' abbandoned")
                return True
        return False

    def __handleHostGone(self):
        '''returns True if a new host was assigned else False'''
        if not self.__host:
            #pick first next player and assign as new host
            newHost:ClientApi = next(iter(self.__players))
            self.__host = newHost
            return True
        return False
    
    def __handleMissingPermission(self, player:ClientApi):
        '''returns True if the player is NOT the host else False'''
        if self.__host == player: return False

        player.connection.emit_SysMessage('only the host is permitted to start the game')
        return True 

    def __handleLobbyIsNotReady(self):
        '''
        returns
             True: if any one player has not jet been set to ready
            False: if all players are set to ready
        '''
        for p, info in self.__players.items():
            if info['isReady'] == False: return True

        return False

    def getLobbyInfo(self):
        return {
            'lobbyId': self.__lobbyId,
            'aiDifficulty': 'not yet implemented'            
        }

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


from server.clientapi import ClientApi
