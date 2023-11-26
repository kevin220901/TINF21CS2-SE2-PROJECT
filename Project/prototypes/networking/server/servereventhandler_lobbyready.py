


from networking.server.clientapi import ClientApi
from networking.socketwrapper import SocketWrapper

from networking.networkevent import NetworkEvent


class ServerEventHandler_LobbyReady:

    def handleEvent(self, client:ClientApi, eventData):

        client.toggleReady()
        pass
    
