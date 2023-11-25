

import pickle
import socket
from networking.socketwrapper import SocketWrapper
from networking import ServerEventHandler, Lobby, NetworkEvent


class ServerEventHandler_LobbyCreate(ServerEventHandler):
    
    def handleEvent(self, context, eventData):
        newLobby = Lobby(eventData['lobbyId'])
        conn:SocketWrapper = context['conn']

        newLobby.join(conn)

        context['lobbies'][newLobby.getLobbyId()] = newLobby

        
        
        eventData = {'sysmessage':f'lobby "{eventData["lobbyId"]}" created'}

        conn.sendall(NetworkEvent.LOBBY_CREATE, eventData)

        print(f'Lobby created {newLobby.getLobbyId()}')