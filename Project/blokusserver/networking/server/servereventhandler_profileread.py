

from logger import logger
from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler


class ServerEventHandler_ProfileRead(ServerEventHandler):
    def __init__(self, client:ClientApi):
        super().__init__(client)
    
    def handleEvent(self, data):
        if 'token' not in data:
            logger.critical('access denied')
            self._client.connection.emit_SysMessage('access denied')
            return False

        self._client.readProfile(data['token'])