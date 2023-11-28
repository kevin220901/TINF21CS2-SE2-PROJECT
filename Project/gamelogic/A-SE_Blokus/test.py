import numpy as np
import pieces
from blokuspiece import BlokusPiece
from game import Game

piece_meh = BlokusPiece(np.array([
    [0,1,0],
    [0,1,1],
    [1,1,0]
]))

piece = pieces.PIECES["5_9"]
piece.print()
expected = np.array([
    [0, 1, 0],
    [1, 1, 0],
    [0, 1, 1]
])
#act
piece.ySpiegelung()
piece.print()