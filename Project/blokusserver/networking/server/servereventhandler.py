


from venv import logger
from server.clientapi import ClientApi

##################################################
## Author: Luis Eckert
##################################################

class ServerEventHandler:

    def __init__(self, client:ClientApi) -> None:
        self._client:ClientApi = client

    def handleEvent(self, eventData):
        
        pass
    
    def _handleIvalidateAuthToken(self, token):
        if token != self._client.authToken or not token:
            logger.critical('access denied')
            self._client.connection.emit_SysMessage('access denied')
            return True
        return False