


from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler

class ServerEventHandler(ServerEventHandler):

    def handleEvent(self, client:ClientApi, eventData):

        raise NotImplemented(f'{__class__}.handleEvent(...)')
        pass
    
