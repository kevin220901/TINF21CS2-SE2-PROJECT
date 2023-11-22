

import pickle
import socket
from Project.prototypes.networking.socketwrapper import SocketWrapper
from networking import ServerEventHandler, Lobby, NetworkEvent


class ServerEventHandler_LobbyCreate(ServerEventHandler):
    
    def handleEvent(self, context, eventData):
        newLobby = Lobby()
        newLobby.join(context['playerId'])

        context['lobbies'][newLobby.getLobbyId()]

        conn:SocketWrapper = context['conn']
        
        eventData = {'eventData':'created'}

        conn.sendall(NetworkEvent.LOBBY_CREATE, eventData)

        print(f'Lobby created')