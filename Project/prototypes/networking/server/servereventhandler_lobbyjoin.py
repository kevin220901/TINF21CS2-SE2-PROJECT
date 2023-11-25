

from networking.networkevent import NetworkEvent
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

        lobby.sendSysMessage('player has joined the lobby')

        print(f'Lobby joined {lobbyId}')
        pass