

import pickle
import socket
from networking.socketwrapper import SocketWrapper
from networking import ServerEventHandler, Lobby, NetworkEvent

#do i need to make the handleEvent a critical section?
#maby use one set of ServerEventHandlers per connected client to prevent thread bleeding?
class ServerEventHandler_LobbyCreate(ServerEventHandler):
    
    def handleEvent(self, client, eventData):
        if not eventData: client.sendSysMessage('server recieved invalid data')
        if 'lobbyName' not in eventData: client.sendSysMessage('server recieved invalid lobby name')
        
        lobby = client.createLobby(eventData['lobbyName'])

        print(f'Lobby created {lobby.getLobbyId()}')