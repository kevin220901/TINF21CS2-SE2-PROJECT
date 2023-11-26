

import pickle
import socket
from networking.server.clientapi import ClientApi
from networking.socketwrapper import SocketWrapper
from networking import ServerEventHandler, Lobby, NetworkEvent

#do i need to make the handleEvent a critical section?
#maby use one set of ServerEventHandlers per connected client to prevent thread bleeding?
class ServerEventHandler_LobbyCreate(ServerEventHandler):
    
    def handleEvent(self, client:ClientApi, eventData):
        if not eventData: 
            client.sendSysMessage('server recieved invalid data')
            return
         
        if 'lobbyName' not in eventData: 
            client.sendSysMessage('server recieved invalid lobby name')
            return

        client.createLobby(eventData['lobbyName'])
        pass