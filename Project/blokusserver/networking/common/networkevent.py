
from enum import Enum


class NetworkEvent(Enum):

    LOBBY_JOIN = 1
    LOBBY_CREATE = 2
    LOBBY_LEAVE = 3
    LOBBY_READY = 4
    LOBBIES_GET = 5
    GAME_START = 6
    GAME_MOVE = 7
    GAME_UPDATE = 8
    GAME_INVALID_MOVE = 9
    GAME_CHANGE_ACTIVE_PLAYER = 10
    GAME_FINISH = 11
    MESSAGE = 12
    SYSMESSAGE = 13
    PICK_COLOR = 14


    
    
