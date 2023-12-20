import numpy as np
from unittest import TestCase
from numpy.testing import assert_array_equal
from ..blokuspiece import BlokusPiece
from ..game import Game


class Test_Blokus_Piece(TestCase):
    #Richtgies rotieren des Piece
    def test_rotate(self):
        #arrange
        piece = BlokusPiece(np.array([
            [0, 1, 0],
            [0, 1, 1],
            [1, 1, 0]
        ]))
        expected = np.array([[0,1,0],[1,1,1],[0,0,1]])
        #act
        result = piece.rotieren()
        #asert
        assert_array_equal(result, expected)

        pass

    #Spiegeln des Piece an der x-Achse
    def test_spiegel_x(self):
        #arrange
        piece = BlokusPiece(np.array([
            [0, 1, 0],
            [0, 1, 1],
            [1, 1, 0]
        ]))
        expected = np.array([
            [1, 1, 0],
            [0, 1, 1],
            [0, 1, 0]
        ])
        #act
        result = piece.xSpiegelung()
        #asert
        assert_array_equal(result, expected)

    # Spiegeln des Piece an der y-Achse
    def test_spiegel_y(self):
        #arrange
        piece = BlokusPiece(np.array([
            [0, 1, 0],
            [0, 1, 1],
            [1, 1, 0]
        ]))
        expected = np.array([
            [0, 1, 0],
            [1, 1, 0],
            [0, 1, 1]
        ])
        #act
        result = piece.ySpiegelung()
        #asert
        assert_array_equal(result, expected)

    #Rechts und links dürfen Pieces mit der selben Zahl liegen
    def test_same_piece_left_right(self):
        #arrange
        piece_1 = BlokusPiece(np.array([[1,1,1,1,1]]))
        piece_1.rotieren()
        game = Game(6)

        expected = np.array([
            [1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0]
        ])

        #act
        game.placeFirstPiece(piece_1, 5, 0, 1)
        game.__placePiece(piece_1, 0, 0, 1)

        #assert
        assert_array_equal(game.getFeld, expected)

    #erstes Piece muss in einer Ecke sein
    def test_first_in_corner(self):
        # arrange
        piece_1 = BlokusPiece(np.array([[1,1,1,1,1]]))
        game = Game(6)

        expected = np.array([
            [1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ])

        # act
        game.__placePiece(piece_1, 0, 0, 1)

        # assert
        assert_array_equal(game.getFeld, expected)

    #zwei pieces dürfen nicht Seite an Seite liegen
    def test_same_piece_seite_seite(self):
        # arrange
        piece_1 = BlokusPiece(np.array([[1,1,1,1,1]]))
        piece_1.rotieren()
        piece_2 = BlokusPiece(np.array([
            [1,1,1],
            [0,0,1]
        ]))
        game = Game(6)

        expected = np.array([
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ])

        # act
        game.__placePiece(piece_1, 0, 0, 1)
        game.__placePiece(piece_2, 1, 0, 1)

        # assert
        assert_array_equal(game.getFeld, expected)

    # zwei pieces dürfen nicht übereinander liegen
    def test_two_pieces_over_eachother(self):
        # arrange
        piece_1 = BlokusPiece(np.array([[1, 1, 1, 1, 1]]))
        piece_2 = BlokusPiece(np.array([[1,1,1],[0,0,1]]))
        piece_3 = BlokusPiece(np.array([[0,1],[1,1]]))
        game = Game(6)

        expected = np.array([
            [1, 1, 1, 1, 1, 4],
            [0, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 4, 4],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ])

        # act
        game.__placePiece(piece_1, 0, 0, 1)
        piece_2.rotieren()
        piece_2.rotieren()
        piece_2.rotieren()
        game.__placePiece(piece_2, 4, 0, 4)
        game.__placePiece(piece_3, 2, 0, 4)

        # assert
        assert_array_equal(game.getFeld, expected)



    # ToDo: Tests für das valiedieren schreiben, sobald die Funktion mit mehreren Farben arbeitet
    '''
    - liegen alle weiteren Teile mit der entsprechenden Zahl Ecke-an-Ecke
    ia - es dürfen sich KEINE Pieces überlappen
    - es dürfen Pieces unterschiedlicher Farben Seite an Seite liegen
    - beim Test der die Seiten checkt, darf keine Fehlermeldung kommen, wenn dedr Wert rechts/unten out of bounds geht
    - Es dürfen nicht eine Ecke zweimal belegt werden
    '''
    #ToDo: der überschreibt die pieces aus der Datei(Dictionary) noch = mal überarbeiten