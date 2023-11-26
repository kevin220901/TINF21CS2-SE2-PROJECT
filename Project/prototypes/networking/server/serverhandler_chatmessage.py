


from networking.server.clientapi import ClientApi
from networking.networkevent import NetworkEvent
from networking.lobby import Lobby
from networking.socketwrapper import SocketWrapper
from networking import ServerEventHandler

class ServerEventHandler_ChatMessage(ServerEventHandler):
    
    def handleEvent(self, client:ClientApi, eventData):
        if 'message' not in eventData: 
            client.sendSysMessage('invalid message')
            return 
        
        client.sendMessage(eventData['message'])
        pass

