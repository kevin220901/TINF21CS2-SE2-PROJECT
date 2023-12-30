

from server.lobby import Lobby
from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler
from server.logger import logger


##################################################
## Author: Luis Eckert
##################################################

class ServerEventHandler_GamePlacePiece(ServerEventHandler):
    def __init__(self, client: ClientApi) -> None:
        super().__init__(client)
        return

    def handleEvent(self, eventData):
        if self._handleIvalidateAuthToken(eventData.get('token')): return
        if self._handleNotInLobby(): return
        # TODO: should be in game
        logger.info(f"place piece {eventData}")
        self._client.currentGame.place_piece(self._client, 
                                             eventData.get('pieceId'), 
                                             eventData.get('x'), 
                                             eventData.get('y'), 
                                             eventData.get('operations'))
        return