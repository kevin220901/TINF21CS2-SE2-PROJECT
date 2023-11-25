

import pickle
import socket
from networking.socketwrapper import SocketWrapper
from networking import ServerEventHandler, Lobby, NetworkEvent

#do i need to make the handleEvent a critical section?
#maby use one set of ServerEventHandlers per connected client to prevent thread bleeding?
class ServerEventHandler_LobbyCreate(ServerEventHandler):
    
    def handleEvent(self, context, eventData):
        newLobby = Lobby(eventData['lobbyId'])
        conn:SocketWrapper = context['conn']

        newLobby.join(conn)
        context['lobby'] = newLobby
        context['lobbies'][newLobby.getLobbyId()] = newLobby
        
        newLobby.sendSysMessage(f'lobby "{newLobby.getLobbyId()}" created')

        print(f'Lobby created {newLobby.getLobbyId()}')