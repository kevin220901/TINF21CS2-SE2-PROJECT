

from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler

##################################################
## Author: Luis Eckert
##################################################

class ServerEventHandler_LobbyLeave(ServerEventHandler):

    def handleEvent(self, client:ClientApi, eventData):

        client.leaveLobby()
        pass
    
