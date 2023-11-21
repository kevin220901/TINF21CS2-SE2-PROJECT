

import pickle
import socket
from networking import ServerEventHandler, Lobby, NetworkEvent


class ServerEventHandler_LobbyCreate(ServerEventHandler):
    
    def handleEvent(self, context, eventData):
        newLobby = Lobby()
        newLobby.join(context['playerId'])

        context['lobbies'][newLobby.getLobbyId()]

        conn:socket.socket = context['conn']
        
        eventData = pickle.dumps({'eventData':'created'})
        eventHead = (len(eventData) << 8 + NetworkEvent.LOBBY_CREATE.value ).to_bytes(3, 'big')

        conn.sendall()
        conn.sendall()

        print(f'Lobby created')