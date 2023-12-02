


from server.clientapi import ClientApi

##################################################
## Author: Luis Eckert
##################################################

class ServerEventHandler:

    def __init__(self, client:ClientApi) -> None:
        self._client:ClientApi = client

    def handleEvent(self, eventData):
        
        pass
    
