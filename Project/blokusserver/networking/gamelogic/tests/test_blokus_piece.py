import numpy as np
from unittest import TestCase
from numpy.testing import assert_array_equal
from ..blokuspiece import BlokusPiece
from ..game import Game, BlokusException


class Test_Blokus_Piece(TestCase):
    #Richtgies rotieren des Piece
    def test_rotate(self):
        #arrange
        g = Game(6)
        expected = np.array([
            [1, 1, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ])
        #act
        g.placePieceByKey("4_0", 0, 0, 1, 1)
        #asert
        assert_array_equal(g.getFeld, expected)

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
        g = Game(6)
        expected = np.array([
            [1, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ])
        #act
        g.placePieceByKey("4_0", 0, 0, 1, 0, 1)
        #asert
        assert_array_equal(g.getFeld, expected)

    #Rechts und links dürfen Pieces mit der selben Zahl liegen
    def test_same_piece_left_right(self):
        #arrange
        piece_1 = BlokusPiece(np.array([[1],[1],[1],[1],[1]]))
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
        game.placePieceByKey("5_3", 0, 0, 1, 1)

        #assert
        assert_array_equal(game.getFeld, expected)

    #erstes Piece muss in einer Ecke sein
    def test_first_in_corner(self):
        # arrange
        game_lo = Game(6)
        game_lu = Game(6)
        game_ro = Game(6)
        game_ru = Game(6)

        expected_lo = np.array([
            [1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ])
        expected_lu = np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0]
        ])
        expected_ro = np.array([
            [0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ])
        expected_ru = np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1]
        ])

        # act
        game_lo.placePieceByKey("5_3", 0, 0, 1)
        game_lu.placePieceByKey("5_3", 0, 5, 1)
        game_ro.placePieceByKey("5_3", 1, 0, 1)
        game_ru.placePieceByKey("5_3", 1, 5, 1)

        # assert
        assert_array_equal(game_lo.getFeld, expected_lo)
        assert_array_equal(game_lu.getFeld, expected_lu)
        assert_array_equal(game_ro.getFeld, expected_ro)
        assert_array_equal(game_ru.getFeld, expected_ru)

    def test_corner_aint_double(self):
        # arrange
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
        game.placePieceByKey("5_3", 0, 0, 1)
        game.placePieceByKey("5_4", 0, 0, 4)

        #assert
        assert_array_equal(game.getFeld, expected)

    #zwei pieces dürfen nicht Seite an Seite liegen
    def test_pieces_dont_touch(self):
        # arrange
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
        game.placePieceByKey("5_3", 0, 0, 1, 1)
        try:
            game.placePieceByKey("4_3", 1, 0, 1)
        except BlokusException as e:
            self.assertEqual(str(e), "Das piece berührt mit einer Seite ein anderes Piece")

        # assert
        assert_array_equal(game.getFeld, expected)

    # zwei pieces dürfen nicht übereinander liegen
    def test_two_diff_pieces_next_each_other(self):
        # arrange
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
        game.placePieceByKey("5_3", 0, 0, 1)
        game.placePieceByKey("4_3", 4, 0, 4, 3)

        # assert
        assert_array_equal(game.getFeld, expected)

    def test_two_pieces_dont_over_each_other(self):
        g = Game(6)

        expected = np.array([
            [1, 1, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ])

        g.placePieceByKey("4_2", 0, 0, 1, 2)
        try:
            g.placePieceByKey("5_4", 1, 1, 1, 1)
        except BlokusException as e:
            self.assertEqual(str(e), "An der Stelle liegt schon ein Piece")

        assert_array_equal(g.getFeld, expected)

    def test_pieces_corner_each_other(self):
        g = Game(6)

        expected = np.array([
            [1, 0, 1, 0, 0, 0],
            [1, 0, 1, 1, 0, 0],
            [1, 0, 0, 1, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [0, 1, 1, 0, 0, 0]
        ])

        #act
        g.placePieceByKey("5_3", 0, 0, 1, 1)
        g.placePieceByKey("4_3", 1, 3, 1, 3)
        g.placePieceByKey("4_0", 3, 0, 1, 0, 1)
        try:
            pass
        except BlokusException as e:
            pass

        #assert
        print(g.getFeld)
        print(expected)
        assert_array_equal(g.getFeld, expected)


    # ToDo: Tests für das valiedieren schreiben, sobald die Funktion mit mehreren Farben arbeitet
    #ToDo: Es dürfen nicht eine Ecke zweimal belegt werden (test steht schon, in Code einarbeiten)
    #ToDO: Vergleich der Ecken überprüfen: test_pieces_corner_each_other
'''
    - liegen alle weiteren Teile mit der entsprechenden Zahl Ecke-an-Ecke
    '''
    #ToDo: der überschreibt die pieces aus der Datei(Dictionary) noch = mal überarbeiten