import numpy as np
from blokuspiece import BlokusPiece

# 1 = rot - r
# 2 = gelb - ge
# 3 = blau - b
# 4 = grün - gr


PIECES = {
    "1_0": BlokusPiece(np.array([[1]])),
    "2_0": BlokusPiece(np.array([[1,1]])),
    "3_0": BlokusPiece(np.array([1,1,1])),
    "3_1": BlokusPiece(np.array([[0,1],[1,1]])),
    "4_0": BlokusPiece(np.array([[0,1],[1,1],[1,0]])),
    "4_1": BlokusPiece(np.array([[1,1],[1,1]])),
    "4_2": BlokusPiece(np.array([[0,1,0],[1,1,1]])),
    "4_3": BlokusPiece(np.array([[1,1,1],[0,0,1]])),
    "4_4": BlokusPiece(np.array([[1,1,1,1]])),
    "5_0": BlokusPiece(np.array([[0,1],[1,1],[1,1]])),
    "5_1": BlokusPiece(np.array([[0,1],[0,1],[1,1],[1,0]])),
    "5_2": BlokusPiece(np.array([[1,1,1,1],[0,0,0,1]])),
    "5_3": BlokusPiece(np.array([[1,1,1,1,1]])),
    "5_4": BlokusPiece(np.array([[1,1],[1,0],[1,1]])),
    "5_5": BlokusPiece(np.array([[0,1,1],[0,1,0],[1,1,0]])),
    "5_6": BlokusPiece(np.array([[0,1,1],[1,1,0],[1,0,0]])),
    "5_7": BlokusPiece(np.array([[0,0,1],[0,0,1],[1,1,1]])),
    "5_8": BlokusPiece(np.array([[0,0,1],[1,1,1],[0,0,1]])),
    "5_9": BlokusPiece(np.array([[0,1,0],[0,1,1],[1,1,0]])),
    "5_10": BlokusPiece(np.array([[0,1,0],[1,1,1],[0,1,0]])),
    "5_11": BlokusPiece(np.array([[0,1,0,0],[1,1,1,1]]))
}