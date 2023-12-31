
from enum import Enum

##################################################
## Author: Luis Eckert
##################################################

class NetworkEvent(Enum):

    LOBBY_JOIN = 1
    LOBBY_CREATE = 2
    LOBBY_LEAVE = 3
    LOBBY_READY = 4
    LOBBIES_GET = 5
    GAME_START = 6
    GAME_PLACE_PIECE = 7
    GAME_UPDATE = 8
    GAME_INVALID_PLACEMENT = 9
    GAME_CHANGE_ACTIVE_PLAYER = 10
    GAME_FINISH = 11
    MESSAGE = 12
    SYSMESSAGE = 13
    PICK_COLOR = 14
    LOGIN = 15
    LOGIN_SUCCESS = 16
    REGISTRATION = 17
    REGISTRATION_SUCCESS = 18
    PROFILE_READ = 19
    PROFILE_UPDATE = 20
    PROFILE_DELETE = 21
    LOBBY_UPDATE = 22
    PROFILE_UPDATE_PASSWORD = 23
    LOBBY_REFRESH = 24


    

    

