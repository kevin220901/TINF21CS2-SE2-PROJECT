

from networking import ServerEventHandler

class ServerEventHandler_LobbyJoin(ServerEventHandler):
    
    def handleEvent(self, context, eventData):
        lobbyId = eventData['lobbyId']
        pass