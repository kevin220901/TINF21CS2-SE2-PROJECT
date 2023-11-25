


from networking.lobby import Lobby
from networking.socketwrapper import SocketWrapper
from networking import ServerEventHandler

class ServerEventHandler_LobbyJoin(ServerEventHandler):
    
    def handleEvent(self, context, eventData):
        conn:SocketWrapper = context['conn']
        lobby:Lobby = context['lobby']
        
        lobby.sendMessage(conn, eventData['message'])

        print(f'Message Broadcasted {eventData["message"]}')
        pass