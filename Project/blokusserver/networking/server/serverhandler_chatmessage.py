


from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler

class ServerEventHandler_ChatMessage(ServerEventHandler):
    
    def handleEvent(self, client:ClientApi, eventData):
        if 'message' not in eventData: 
            client.sendSysMessage('invalid message')
            return 
        
        client.sendMessage(eventData['message'])
        pass

