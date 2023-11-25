

from Project.prototypes.networking.networkevent import NetworkEvent
from networking.lobby import Lobby
from networking.socketwrapper import SocketWrapper
from networking import ServerEventHandler

class ServerEventHandler_LobbyJoin(ServerEventHandler):
    
    def handleEvent(self, context, eventData):
        lobbyId = eventData['lobbyId']
        conn:SocketWrapper = context['conn']
        lobby:Lobby = context['lobbies'][lobbyId]
        lobby.join(conn)
        context['lobby'] = lobby

        eventData = {'sysmessage':f'lobby "{eventData["lobbyId"]}" created'}
        conn.sendall(NetworkEvent.LOBBY_JOIN, eventData)

        lobby.sendMessage()

        print(f'Lobby joined {lobbyId}')
        pass