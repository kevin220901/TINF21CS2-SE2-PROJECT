

import pickle
import socket
from networking import ServerEventHandler, Lobby, NetworkEvent


class ServerEventHandler_LobbyCreate(ServerEventHandler):
    
    def handleEvent(self, context, eventData):
        newLobby = Lobby()
        newLobby.join(context['player'])

        context['lobbies'][newLobby.getLobbyId()]

        conn:socket.socket = context['conn']

        conn.sendall(NetworkEvent.LOBBY_CREATE.value.to_bytes(1, 'big'))
        conn.sendall(pickle.dumps({'eventData':'created'}))

        print(f'Lobby created')