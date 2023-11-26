


from networking.server.clientapi import ClientApi
from networking.socketwrapper import SocketWrapper

from networking.networkevent import NetworkEvent


class ServerEventHandler_GameStart:

    def handleEvent(self, client:ClientApi, eventData):
        
        client.currentLobby.startGame(client)
        
        pass
    
