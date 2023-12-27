import numpy as np
from .blokuspiece import BlokusPiece
from .gameeventcodes import GameEventCodes


class Game:
    def __init__(self, fieldsize:int):
        self.__fieldsize = fieldsize #für fieldsize <10 kann es zu Problemen geben, weil die firstPieces übereinander liegen können, für das eigentliche Spiel aber unrelevant, da fieldsize = 20
        self.__feld = np.zeros([fieldsize,fieldsize])
        self.__isFirstPiece = {1: True, 2: True, 3: True, 4: True}
        self.__availeblePieces = {
            1: self.__createPieces(),
            2: self.__createPieces(),
            3: self.__createPieces(),
            4: self.__createPieces()
        }
        self.__event = (int, str)

    def __createPieces(self):
        return {
            "1_0": BlokusPiece(np.array([[1]])),
            "2_0": BlokusPiece(np.array([[1, 1]])),
            "3_0": BlokusPiece(np.array([1, 1, 1])),
            "3_1": BlokusPiece(np.array([[0, 1], [1, 1]])),
            "4_0": BlokusPiece(np.array([[0, 1], [1, 1], [1, 0]])),
            "4_1": BlokusPiece(np.array([[1, 1], [1, 1]])),
            "4_2": BlokusPiece(np.array([[0, 1, 0], [1, 1, 1]])),
            "4_3": BlokusPiece(np.array([[1, 1, 1], [0, 0, 1]])),
            "4_4": BlokusPiece(np.array([[1, 1, 1, 1]])),
            "5_0": BlokusPiece(np.array([[0, 1], [1, 1], [1, 1]])),
            "5_1": BlokusPiece(np.array([[0, 1], [0, 1], [1, 1], [1, 0]])),
            "5_2": BlokusPiece(np.array([[1, 1, 1, 1], [0, 0, 0, 1]])),
            "5_3": BlokusPiece(np.array([[1, 1, 1, 1, 1]])),
            "5_4": BlokusPiece(np.array([[1, 1], [1, 0], [1, 1]])),
            "5_5": BlokusPiece(np.array([[0, 1, 1], [0, 1, 0], [1, 1, 0]])),
            "5_6": BlokusPiece(np.array([[0, 1, 1], [1, 1, 0], [1, 0, 0]])),
            "5_7": BlokusPiece(np.array([[0, 0, 1], [0, 0, 1], [1, 1, 1]])),
            "5_8": BlokusPiece(np.array([[0, 0, 1], [1, 1, 1], [0, 0, 1]])),
            "5_9": BlokusPiece(np.array([[0, 1, 0], [0, 1, 1], [1, 1, 0]])),
            "5_10": BlokusPiece(np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])),
            "5_11": BlokusPiece(np.array([[0, 1, 0, 0], [1, 1, 1, 1]]))
        }

    def __deleteAvaileblePiece(self, spielerID:int, pieceKey:str):
        del self.__availeblePieces[spielerID][pieceKey]

    def __isPieceAvaileble(self, spielerID:int, pieceKey:str):
        return pieceKey in self.__availeblePieces[spielerID] #String

    def print(self):
        print(self.__feld)

    def getAvailablePieces(self, spielerID:int):
        return list(self.__availeblePieces[spielerID].keys())

    @property
    def getFeld(self):
        return self.__feld

    def placePieceByKey(self, pieceKey:str, start_x, start_y, spielerID:int):
        piece = self.__availeblePieces[spielerID][pieceKey]
        if self.__isPieceAvaileble(spielerID, pieceKey) == True:
            if self.__placePiece(piece, start_x, start_y, spielerID) == True:
                self.__deleteAvaileblePiece(spielerID, pieceKey)
        else:
            self.__event = (GameEventCodes.SAME_PIECE, "Das Piece wurde bereits platziert")

    def __placePiece(self, piece:BlokusPiece, start_x, start_y, spielerID:int):
        if self.__isFirstPiece[spielerID] == True:
            return self.placeFirstPiece(piece, start_x, start_y, spielerID) #Funktion gibt einen boolschen Wert zurück
        else:
            return self.__placeValidatePiece(piece, start_x, start_y, spielerID) #Funktion gibt einen boolschen Wert zurück


    def placeFirstPiece(self, piece:BlokusPiece, start_x, start_y, spielerID:int)->bool:
        form = piece.getForm()

        if self.__validateFirstPiece(piece, start_x, start_y) == False:
            return False

        for y in range(len(form)):
            for x in range(len(form[y])):
                if form[y][x] == 1:
                    self.__feld[y + start_y, x + start_x] = spielerID

        self.__isFirstPiece[spielerID] = False
        return True


    def __placeValidatePiece(self, piece:BlokusPiece, start_x, start_y, spielerID:int)->bool: # spielerID = farbe
        form = piece.getForm()

        if self.__validatePiece(piece, start_x, start_y, spielerID) == False:
            return False

        for y in range(len(form)):
            for x in range(len(form[y])):
                if form[y][x] == 1:
                    self.__feld[y + start_y, x + start_x] = spielerID
        return True


    def __validatePiece(self, piece:BlokusPiece, start_x, start_y, spielerID): # spielerID = farbe
        form = piece.getForm()
        ecke = False

        #Out-of-Bounds
        if (start_x + len(form[0])) > self.__fieldsize or (start_y + len(form)) > self.__fieldsize or start_x < 0 or start_y < 0: #Out-of-bounds
            self.__event = (GameEventCodes.PIECE_OUT_OFF_BOUNDS, "Die Eingabe liegt nicht im Feld")
            return False

        for y in range(len(form)):
            for x in range(len(form[y])):

                # Ist an der Stelle schon ein Piece?
                if self.__feld[y + start_y, x + start_x] > 0: # Überprüfung ob an er Stelle schon ein Piece liegt, egal welcher Farbe (>0 = irgend ein piece
                    self.__event = (GameEventCodes.SPACE_OCCUPIED, "An der Stelle liegt schon ein Piece")
                    return False

        #Liegt es Seite an Seite zu einem anderen Piece der gleichen Farbe? Soll es nicht!
                if form[y][x] == 1:
                    if (x + start_x + 1) < self.__fieldsize:
                        if (self.__feld[y + start_y, x + start_x + 1] == spielerID): #gucke eins nach rechts und guck ob da nen piece ist, wenn ja, brich ab
                            self.__event = (GameEventCodes.PIECE_NEXT_TO_PIECE, "Das piece berührt mit einer Seite ein anderes Piece")
                            return False
                    if (x + start_x - 1) >= 0:
                        if (self.__feld[y + start_y, x + start_x - 1] == spielerID): #gucke eins nach links und guck ob da nen piece ist
                            self.__event = (GameEventCodes.PIECE_NEXT_TO_PIECE, "Das piece berührt mit einer Seite ein anderes Piece")
                            return False

                    if (y + start_y + 1) < self.__fieldsize:
                        if (self.__feld[y + start_y + 1, x + start_x] == spielerID): #gucke eins nach unten und guck ob da nen piece ist
                            self.__event = (GameEventCodes.PIECE_NEXT_TO_PIECE, "Das piece berührt mit einer Seite ein anderes Piece")
                            return False
                    if (self.__feld[y + start_y - 1, x + start_x] == spielerID): #gucke eins nach oben und guck ob da nen piece ist
                        self.__event = (GameEventCodes.PIECE_NEXT_TO_PIECE, "Das piece berührt mit einer Seite ein anderes Piece")
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
        if ecke == False:
            self.__event = (GameEventCodes.NO_CORNER_PIECE, "Das Piece muss mit einer Ecke an einer anderen liegen")
        return ecke


    def __validateFirstPiece(self, piece:BlokusPiece, start_x, start_y):
        form = piece.getForm()
        if (start_x + len(form[0])) > self.__fieldsize or (start_y + len(form)) > self.__fieldsize or start_x < 0 or start_y < 0: #Out-of-bounds
            self.__event = (GameEventCodes.PIECE_OUT_OFF_BOUNDS, "Die Eingabe liegt nicht im Feld")
            return False

        if (form[0][0] == 1) and (start_x == 0) and (start_y == 0): # Test für Ecke oben links / die Form hat immer den Wert 1, deswegen wird auf 1 geprüft und nicht die eigentliche Spielerzahl
            return True
        elif (form[0][-1] == 1) and ((start_x + len(form[0])) == self.__fieldsize) and (start_y == 0): # Test für Ecke oben rechts
            return True
        elif (form[-1][0] == 1) and (start_x == 0) and ((start_y + len(form)) == self.__fieldsize): # Test für Ecke unten links
            return True
        elif (form[-1][-1] == 1) and ((start_x + len(form[0])) == self.__fieldsize) and ((start_y + len(form)) == self.__fieldsize): # Test für Ecke unten rechts
            return True
        else:
            self.__event = (GameEventCodes.NO_CORNER_FIRST_PIECE, "Das erste Piece liegt in keiner Ecke")
            return False

