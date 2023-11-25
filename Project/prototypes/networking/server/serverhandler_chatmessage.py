


from networking.networkevent import NetworkEvent
from networking.lobby import Lobby
from networking.socketwrapper import SocketWrapper
from networking import ServerEventHandler

class ServerEventHandler_ChatMessage(ServerEventHandler):
    
    def handleEvent(self, context, eventData):
        conn:SocketWrapper = context['conn']
        lobby:Lobby = context['lobby']

        if not lobby:
            conn.sendall(NetworkEvent.SYSMESSAGE, {'sysmessage':'you can only send messages if you are part of a lobby'})
            return
        
        lobby.sendMessage(conn, eventData['message'])

        print(f'Message boradcasted {eventData["message"]}')
        pass

