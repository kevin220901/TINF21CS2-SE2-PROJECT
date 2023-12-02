from enum import Enum


class GameEventCodes(Enum):
    PIECE_OUT_OFF_BOUNDS = 1
    SPACE_OCCUPIED = 2
    PIECE_NEXT_TO_PIECE = 3
    NO_CORNER_PIECE = 4
    NO_CORNER_FIRST_PIECE = 5