import numpy as np
import pieces
from blokuspiece import BlokusPiece

##################################################
## Author: Cynthia Winkler
##################################################

class Game:
    def __init__(self, fieldsize:int):
        self.__fieldsize = fieldsize # für fieldsize <10 kann es zu Problemen geben, weil die firstPieces übereinander liegen können, für das eigentliche Spiel aber unrelevant, da fieldsize = 20
        self.__feld = np.zeros([fieldsize,fieldsize])
        self.__isFirstPiece = {1: True, 2: True, 3: True, 4: True}

    def print(self):
        print(self.__feld)

    @property
    def getFeld(self):
        return self.__feld

    def placePiece(self, piece:BlokusPiece, start_x, start_y, spielerID:int):
        if self.__isFirstPiece[spielerID] == True:
            self.placeFirstPiece(piece, start_x, start_y, spielerID)
            self.__isFirstPiece[spielerID] = False
        else:
            self.__placeValidatePiece(piece, start_x, start_y, spielerID)

    def placeFirstPiece(self, piece:BlokusPiece, start_x, start_y, spielerID:int):
        form = piece.getForm()

        if self.__validateFirstPiece(piece, start_x, start_y) == False:
            return

        for y in range(len(form)):
            for x in range(len(form[y])):
                if form[y][x] == 1:
                    self.__feld[y + start_y, x + start_x] = spielerID

    def __placeValidatePiece(self, piece:BlokusPiece, start_x, start_y, spielerID:int): # spielerID = farbe
        form = piece.getForm()

        if self.__validatePiece(piece, start_x, start_y, spielerID) == False:
            return

        for y in range(len(form)):
            for x in range(len(form[y])):
                if form[y][x] == 1:
                    self.__feld[y + start_y, x + start_x] = spielerID

    def __validatePiece(self, piece:BlokusPiece, start_x, start_y, spielerID): # spielerID = farbe
        form = piece.getForm()
        ecke = False

        #Out-of-Bounds
        if (start_x + len(form[0])) > self.__fieldsize or (start_y + len(form)) > self.__fieldsize or start_x < 0 or start_y < 0: #Out-of-bounds
            print("Die Eingabe liegt nicht im Feld")
            return False

        for y in range(len(form)):
            for x in range(len(form[y])):

                # Ist an der Stelle schon ein Piece?
                if self.__feld[y + start_y, x + start_x] > 0: # Überprüfung ob an er Stelle schon ein Piece liegt, egal welcher Farbe (>0 = irgend ein piece
                    print("An der Stelle liegt schon ein Piece")
                    return False

        #Liegt es Seite an Seite zu einem anderen Piece der gleichen Farbe? Soll es nicht!
                if form[y][x] == 1:
                    if (x + start_x + 1) < self.__fieldsize:
                        if (self.__feld[y + start_y, x + start_x + 1] == spielerID): #gucke eins nach rechts und guck ob da nen piece ist, wenn ja, brich ab
                            print("Das piece berührt mit einer Seite ein anderes Piece")
                            return False
                    if (x + start_x - 1) >= 0:
                        if (self.__feld[y + start_y, x + start_x - 1] == spielerID): #gucke eins nach links und guck ob da nen piece ist
                            print("Das piece berührt mit einer Seite ein anderes Piece")
                            return False

                    if (y + start_y + 1) < self.__fieldsize:
                        if (self.__feld[y + start_y + 1, x + start_x] == spielerID): #gucke eins nach unten und guck ob da nen piece ist
                            print("Das piece berührt mit einer Seite ein anderes Piece")
                            return False
                    if (self.__feld[y + start_y - 1, x + start_x] == spielerID): #gucke eins nach oben und guck ob da nen piece ist
                        print("Das piece berührt mit einer Seite ein anderes Piece")
                        return False

        #Eckt es an ein anderes an? Soll es!
                if form[y][x] == 1 and ecke == False: #ToDo: soll es hier auch den Fall für links mit -1 abfangen?
                    if (self.__feld[y + start_y - 1, x + start_x - 1] == spielerID and ecke == False): #gucke ob Ecke oben links ne 1 ist, wenn ja = gut
                        ecke = True

                    if ((x + start_x + 1) < self.__fieldsize) and ecke == False:
                        if (self.__feld[y + start_y - 1, x + start_x + 1] == spielerID): #gucke ob Ecke oben rechts ne 1 ist, wenn ja = gut
                            ecke = True

                    if ((y + start_y + 1) < self.__fieldsize and (x + start_x + 1) < self.__fieldsize) and ecke == False:
                        if (self.__feld[y + start_y + 1, x + start_x - 1] == spielerID): #gucke ob Ecke unten links ne 1 ist, wenn ja = gut
                            ecke = True
                        if (self.__feld[y + start_y + 1, x + start_x + 1] == spielerID): #gucke ob Ecke unten rechts ne 1 ist, wenn ja = gut
                            ecke = True
        #print("Das Piece muss mit einer Ecke an einer anderen liegen")
        return ecke


    def __validateFirstPiece(self, piece:BlokusPiece, start_x, start_y):
        form = piece.getForm()
        if (start_x + len(form[0])) > self.__fieldsize or (start_y + len(form)) > self.__fieldsize or start_x < 0 or start_y < 0: #Out-of-bounds
            print("Das Piece ist Out-of-Bounds")
            return False

        if (form[0][0] == 1) and (start_x == 0) and (start_y == 0): # Test für Ecke oben links / die Form hat immer den Wert 1, deswegen wird auf 1 geprüft und nicht die eigentliche Spielerzahl
            print("Das Piece liegt oben links")
            return True
        elif (form[0][-1] == 1) and ((start_x + len(form[0])) == self.__fieldsize) and (start_y == 0): # Test für Ecke oben rechts
            print("Das Piece liegt oben rechts")
            return True
        elif (form[-1][0] == 1) and (start_x == 0) and ((start_y + len(form)) == self.__fieldsize): # Test für Ecke unten links
            print("Das Piece unten links")
            return True
        elif (form[-1][-1] == 1) and ((start_x + len(form[0])) == self.__fieldsize) and ((start_y + len(form)) == self.__fieldsize): # Test für Ecke unten rechts
            print("Das Piece liegt unten rechts")
            return True
        else:
            print("Das Piece liegt in keiner Ecke")
            return False


"""

piece_1 = pieces.PIECES["5_9"]
piece_2 = pieces.PIECES["4_3"]
piece_3 = pieces.PIECES["5_3"]
piece_4 = pieces.PIECES["4_0"]
piece_5 = pieces.PIECES["1_0"]

piece_1.print()

test_feld = Game(20)
piece_2.rotieren()
piece_2.ySpiegelung()
#piece_3.rotieren()

test_feld.placeFirstPiece(piece_3, 0, 19, 1)

test_feld.placePiece(piece_2, 0, 0, 1)
test_feld.placePiece(piece_3, 2, 3, 1)


#test_feld.placePiece(piece_4, 18, 0, 4)
#test_feld.placePiece(piece_5, 17, 0, 4)

test_feld.print()

"""