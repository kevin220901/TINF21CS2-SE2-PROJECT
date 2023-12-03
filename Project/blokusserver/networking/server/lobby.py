from __future__ import annotations
import uuid

##################################################
## Author: Luis Eckert
##################################################

class Lobby:
    def __init__(self, lobbyId, lobbies:dict) -> None:
        self.__lobbies = lobbies
        self.__lobbyId = lobbyId
        self.__players = [] #later this might get changed to a dictionary to store mor info. REMEMBER TO update all loops accordingly!
        self.__canBeJoined:bool = True
        self.__isPrivate: bool = False #not yet needed 
        self.__ready = {}
        self.__host: ClientApi = None

        #WARNING: currently no checks are performed to ensure uniqueness of a lobbyId -> lobbies might get overwritten
        self.__lobbies[self.__lobbyId] = self

    def join(self, player:ClientApi):
        self.__players.append(player)
        self.__ready[player] = False
        if self.__players.count(player) > 1: 
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
    
    def __notifyAll(self, message):
        p:ClientApi
        for p in self.__players:
            p.connection.emit_SysMessage(message)
        pass

    def __handleLobbyAbbandoned(self):
        if self.playerCount == 0: 
                self.__lobbies[self] = None
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
            self.__notifyAll(f"{newHost.playerName} is now host.")
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
