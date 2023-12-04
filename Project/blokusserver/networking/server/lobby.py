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
        self.__players = [ ] #later this might get changed to a dictionary to store mor info. REMEMBER TO update all loops accordingly!
        self.__canBeJoined:bool = True
        self.__isPrivate: bool = False #not yet needed 
        self.__ready = {}
        self.__host: ClientApi = None

        #WARNING: currently no checks are performed to ensure uniqueness of a lobbyId -> lobbies might get overwritten
        self.__lobbies[self.__lobbyId] = self


    def get_lobby_info(self):
        return {
            'lobbyId': self.__lobbyId,
            'host': {'playerId':self.__host.playerId, 'playerName':self.__host.playerName},
            'players': [{'playerId':player.playerId, 'playerName':player.playerName} for player in self.__players if player != self.__host],
            'aiDifficulty': 'not yet implemented',
            'messages':[]            
        }

    def join(self, player:ClientApi):
        self.__players.append(player)
        self.__ready[player] = False
        
        if len(self.__players) > 1: 
            logger.info(f'{player.playerName} joining Step A1')
            lobbyInfo = self.get_lobby_info()
            lobbyInfo['messages'].append(f'{player.playerName} joined')

            if self.__handleHostGone():
                logger.info(f'{player.playerName} joining Step A2')
                lobbyInfo['host'] = {'playerId':self.__host.playerId, 'playerName':self.__host.playerName}
                lobbyInfo['messages'].append(f'{self.__host.playerName} is the new host')
            
            #Notify all players in lobby about the change
            p: ClientApi
            for p in self.__players:
                if p == player:
                    logger.info(f'{player.playerName} joining Step A3')
                    p.connection.emit_LobbyJoin_success(lobbyInfo)
                else:
                    logger.info(f'{player.playerName} joining Step A4')
                    p.connection.emit_lobby_update(lobbyInfo)
        else:
            #first player to join is the host
            logger.info(f'{player.playerName} joining Step B1')
            self.__host = player
        pass
        
    def leave(self, player:ClientApi):
        self.__players.remove(player)
        self.__ready.pop(player)
        if self.__handleLobbyAbbandoned(): return

        lobbyInfo = self.get_lobby_info()
        lobbyInfo['messages'].append(f'{player.playerName} left')

        if self.__handleHostGone():
            lobbyInfo['host'] = {'playerId':self.__host.playerId, 'playerName':self.__host.playerName}
            lobbyInfo['messages'].append(f'{self.__host.playerName} is the new host')    

        #Notify all players in lobby about the change
        p: ClientApi
        for p in self.__players:
            p.connection.emit_lobby_update(lobbyInfo)
       
        pass

    def toggleReady(self, player:ClientApi):
        ready = ~self.__ready[player]
        self.__ready[player] = ready

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
        if self.__handlePlayerIsNotHost(self, player): return
        if self.__handleLobbyIsNotReady(self): return
        
        p:ClientApi
        for p in self.__players:
            p.connection.emit_SysMessage('game started') #TODO: replace with own emit to transmit initial game info
        pass

    def __handleLobbyAbbandoned(self):
        if self.playerCount == 0: 
                self.__lobbies.pop(self.__lobbyId)
                logger.info(f"lobby '{self.__lobbyId}' abbandoned")
                return True
        return False

    def __handleHostGone(self):
        '''
        returns
             True: if there currently is no host
            False: if the lobby has a host
        '''
        if not self.__host:
            #pick first next player and assign as new host
            newHost:ClientApi = next(iter(self.__players))
            self.__host = newHost
            return True
        return False
    
    def __handlePlayerIsNotHost(self, player:ClientApi):
        '''
        returns
             True: if the player is NOT the host
            False: if the player is the host
        '''
        if self.__host == player: return False

        player.connection.emit_SysMessage('only the host is permitted to start the game')
        return True 

    def __handleLobbyIsNotReady(self):
        '''
        returns
             True: if any one player has not jet been set to ready
            False: if all players are set to ready
        '''
        for p,ready in self.__ready.items():
            if ready == False: return True

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
