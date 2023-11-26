



import socket
from networking.networkevent import NetworkEvent
from networking.socketwrapper import SocketWrapper


class ClientSocketWrapper(SocketWrapper):
    def __init__(self, conn: socket) -> None:
        super().__init__(conn)


    def sendSysMessage(self, message):
        eventId = NetworkEvent.SYSMESSAGE
        eventData = {
            'message':message
        }
        self.sendall(eventId, eventData)


    def sendMessage(self, sender:str, message:str):
        eventId = NetworkEvent.MESSAGE
        eventData = {
            'from':sender, 
            'message':message
        }
        self.sendall(eventId, eventData)


    def notifyLobbyCreated(self, lobbyId, lobbyName):
        self.sendSysMessage(f'Lobby {lobbyName}@{lobbyId} created')

    def notifyPlyerJoined(self, player):
        pass

    def notifyPlayerLeft(self, player):
        pass

    def notifyReady(self, player):
        pass

    def notifyGameStarted(self):
        pass
    
    def notifyGameEnded(self, winner:str):
        pass

    def notifyPlayerTurnChaged(self, currentPlayer):
        pass

    def notifyPlayerMove(self, player, piece):
        pass
    