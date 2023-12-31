import fnmatch
import random
import numpy as np
import copy
from .blokuspiece import BlokusPiece


class BlokusException(Exception):
    def init(self, args: object) -> None:
        super().init(args)


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
        self.__is_player_ai = {1: False, 2: False, 3: False, 4: False}
        self.__corners = {"ol": False, "or": False, "ul": False, "ur": False} # corners zum  checken
        self.__temp_poss_place_dict = {}
        self.__ai_possible_places = {}
        self.__ai_tryed_pieces = []
        self.__ai_available_pieces_to_try = {1: [], 2: [], 3: [], 4: []}
        self.__ai_possible_places_counter = 0
        self.currentPlayer = 1

    def __createPieces(self):
        return {
            "1_0": BlokusPiece(np.array([[1]])),
            "2_0": BlokusPiece(np.array([[1, 1]])),
            "3_0": BlokusPiece(np.array([[1, 1, 1]])),
            "3_1": BlokusPiece(np.array([[0, 1],
                                         [1, 1]])),
            "4_0": BlokusPiece(np.array([[0, 1],
                                         [1, 1],
                                         [1, 0]])),
            "4_1": BlokusPiece(np.array([[1, 1],
                                         [1, 1]])),
            "4_2": BlokusPiece(np.array([[0, 1, 0],
                                         [1, 1, 1]])),
            "4_3": BlokusPiece(np.array([[1, 1, 1],
                                         [0, 0, 1]])),
            "4_4": BlokusPiece(np.array([[1, 1, 1, 1]])),
            "5_0": BlokusPiece(np.array([[0, 1],
                                         [1, 1],
                                         [1, 1]])),
            "5_1": BlokusPiece(np.array([[0, 1],
                                         [0, 1],
                                         [1, 1],
                                         [1, 0]])),
            "5_2": BlokusPiece(np.array([[1, 1, 1, 1],
                                         [0, 0, 0, 1]])),
            "5_3": BlokusPiece(np.array([[1, 1, 1, 1, 1]])),
            "5_4": BlokusPiece(np.array([[1, 1],
                                         [1, 0],
                                         [1, 1]])),
            "5_5": BlokusPiece(np.array([[0, 1, 1],
                                         [0, 1, 0],
                                         [1, 1, 0]])),
            "5_6": BlokusPiece(np.array([[0, 1, 1],
                                         [1, 1, 0],
                                         [1, 0, 0]])),
            "5_7": BlokusPiece(np.array([[0, 0, 1],
                                         [0, 0, 1],
                                         [1, 1, 1]])),
            "5_8": BlokusPiece(np.array([[0, 0, 1],
                                         [1, 1, 1],
                                         [0, 0, 1]])),
            "5_9": BlokusPiece(np.array([[0, 1, 0],
                                         [0, 1, 1],
                                         [1, 1, 0]])),
            "5_10": BlokusPiece(np.array([[0, 1, 0],
                                          [1, 1, 1],
                                          [0, 1, 0]])),
            "5_11": BlokusPiece(np.array([[0, 1, 0, 0],
                                          [1, 1, 1, 1]]))
        }

    def printPiece(self, spielerID:int, pieceKey:str):
        print(self.__availeblePieces[spielerID][pieceKey].getForm())

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

    def __ai_get_first_piece_key(self, spielerID:int):
        # Erstellung einer Liste mit allen höchsten verfügbaren Keys, angefangen bei 5
        int_suche = 5
        keys_list = fnmatch.filter(self.__availeblePieces[spielerID], f"{int_suche}*") #Liste mit allen Keys die mit 5 anfangen
        while len(keys_list) == 0:
            int_suche -= 1
            if int_suche == 0:
                raise BlokusException("Keine Pieces könenn platzier werden")
                return False # später nochmal gucken, wenn ich weiß wie das klappt
            keys_list = fnmatch.filter(self.__availeblePieces[spielerID], f"{int_suche}*")

        # Random Auswahl aus der Liste
        piece_key = random.choice(keys_list)

        return piece_key

    def __ai_get_piece_key(self, spielerID:int):
        # Erstellung einer Liste mit allen höchsten verfügbaren Keys, angefangen bei 5
        int_suche = 5
        keys_list = fnmatch.filter(self.__ai_available_pieces_to_try, f"{int_suche}*") #Liste mit allen Keys die mit 5 anfangen
        while len(keys_list) == 0:
            int_suche -= 1
            if int_suche == 0:
                raise BlokusException("Keine Pieces könenn platzier werden")
                return False # später nochmal gucken, wenn ich weiß wie das klappt
            keys_list = fnmatch.filter(self.__availeblePieces[spielerID], f"{int_suche}*")

        # Random Auswahl aus der Liste
        piece_key = random.choice(keys_list)

        return piece_key

    def ai_place_piece(self, spielerID:int):
        #Angabe das es sich dabei um einen AI-Spieler handelt
        if self.__is_player_ai[spielerID] == False:
            self.__is_player_ai[spielerID] = True

        # Platzierung des ersten Pieces
        if self.__isFirstPiece[spielerID] == True:
            piece_key = self.__ai_get_first_piece_key(spielerID)
            while piece_key == "5_10":
                piece_key = self.__ai_get_first_piece_key(spielerID)
            self.__ai_place_first_piece(spielerID, piece_key)
            self.__ai_get_possible_places(spielerID)

        else:
            poss_places_list = self.__ai_possible_places[spielerID]
            poss_place = random.choice(poss_places_list)

            #clonen der availeblePieces für den Fall, dass das Piece nicht platziert werden kann
            self.__ai_available_pieces_to_try = copy.deepcopy(self.__availeblePieces[spielerID])

            while len(self.__ai_tryed_pieces) != len(self.__availeblePieces[spielerID]): # solange noch nicht alle Pieces ausprobiert wurden

                # Holen des Pieces und Bestimmung der Länge und Höhe
                piece_key = self.__ai_get_piece_key(spielerID)
                piece_by_key = self.__availeblePieces[spielerID][piece_key]
                piece_form = piece_by_key.getForm()
                lenght = len(piece_form[0]) - 1
                height = len(piece_form) - 1

                bew = ""

                if poss_place[2] == "ol": # die Ecke ist oben links über dem Teil, das Teil muss unten rechts dran passen
                    if piece_key == "5_10": # das Piece hat keine Ecke von selbst aus und muss deswegen verschoben werden
                        try: # schiebt das Piece nach rechts
                            self.placePieceByKey(piece_key, (poss_place[1] - lenght) + 1, poss_place[0]- height, spielerID, bew)
                            self.__ai_possible_places[spielerID].remove(poss_place)
                            self.__ai_get_possible_places(spielerID)
                            return
                        except BlokusException:
                            continue

                        try: # schiebt das Piece nach unten
                            self.placePieceByKey(piece_key, poss_place[1] - lenght, (poss_place[0] - height) + 1, spielerID, bew)
                            self.__ai_possible_places[spielerID].remove(poss_place)
                            self.__ai_get_possible_places(spielerID)
                            return
                        except BlokusException:
                            continue

                    for flip in range(2):
                        for rot in range(4):
                            try:
                                self.placePieceByKey(piece_key, poss_place[1] - lenght, poss_place[0] - height, spielerID, bew)
                                self.__ai_possible_places[spielerID].remove(poss_place)
                                self.__ai_get_possible_places(spielerID)
                                return
                            except BlokusException:
                                bew += "r"
                                continue
                        bew = "y"
                elif poss_place[2] == "or": # die Ecke ist oben rechts über dem Teil, das Teil muss unten links dran passen
                    for flip in range(2):
                        for rot in range(4):
                            try:
                                self.placePieceByKey(piece_key, poss_place[1], poss_place[0] - height, spielerID, bew)
                                self.__ai_possible_places[spielerID].remove(poss_place)
                                self.__ai_get_possible_places(spielerID)
                                return
                            except BlokusException:
                                continue
                            bew += "r"
                        bew = "y"
                elif poss_place[2] == "ul": # die Ecke ist unten links unter dem Teil, das Teil muss oben rechts dran passen
                    for flip in range(2):
                        for rot in range(4):
                            try:
                                self.placePieceByKey(piece_key, poss_place[1] - lenght, poss_place[0], spielerID, bew)
                                self.__ai_possible_places[spielerID].remove(poss_place)
                                self.__ai_get_possible_places(spielerID)
                                return
                            except BlokusException:
                                continue
                            bew += "r"
                        bew = "y"
                elif poss_place[2] == "ur": # die Ecke ist unten rechts unter dem Teil, das Teil muss oben links dran passen
                    for flip in range(2):
                        for rot in range(4):
                            try:
                                self.placePieceByKey(piece_key, poss_place[1], poss_place[0], spielerID, bew)
                                self.__ai_possible_places[spielerID].remove(poss_place)
                                self.__ai_get_possible_places(spielerID)
                                return
                            except BlokusException:
                                continue
                            bew += "r"
                        bew = "y"
                else:
                    self.__ai_tryed_pieces.append(piece_key)

            raise BlokusException("Es kann kein Teil mehr platziert werden")


    def __ai_get_possible_places(self, spielerID:int):
        for i in self.__temp_poss_place_dict:
            koord = self.__temp_poss_place_dict[i]
            # nach oben gucken
            if (self.__feld[koord[0] - 1][koord[1]] == 0) and (koord[0] - 1 >= 0):
                # nach links gucken
                if (self.__feld[koord[0]][koord[1] - 1] == 0) and (koord[1] - 1 >= 0):
                    # nach schräg links oben gucken
                    if self.__feld[koord[0] - 1][koord[1] - 1] == 0:
                        # Ecke ist mögliche Stelle, abspeichern in das richtige dict
                        self.__ai_possible_places[spielerID].append([koord[0] - 1, koord[1] - 1, "ol"])

                # nach rechts gucken
                elif (koord[1] + 1 < self.__fieldsize) and (self.__feld[koord[0]][koord[1] + 1] == 0):
                    # nach schräg rechts oben gucken
                    if self.__feld[koord[0] - 1][koord[1] + 1] == 0:
                        # Ecke ist mögliche Stelle, abspeichern in das richtige dict
                        self.__ai_possible_places[spielerID].append([koord[0] - 1, koord[1] + 1, "or"])

            # nach unten gucken
            elif ((koord[0] + 1) < self.__fieldsize) and (self.__feld[koord[0] + 1][koord[1]] == 0):
                # nach links gucken
                if (self.__feld[koord[0]][koord[1] - 1] == 0) and (koord[1] - 1 >= 0):
                    # nach schräg links unten gucken
                    if self.__feld[koord[0] + 1][koord[1] - 1] == 0:
                        # Ecke ist mögliche Stelle, abspeichern in das richtige dict
                        self.__ai_possible_places[spielerID].append([koord[0] + 1, koord[1] - 1, "ul"])

                # nach rechts gucken
                elif (koord[1] + 1 < self.__fieldsize) and (self.__feld[koord[0]][koord[1] + 1] == 0):
                    # nach schräg rechts unten gucken
                    if self.__feld[koord[0] + 1][koord[1] + 1] == 0:
                        # Ecke ist mögliche Stelle, abspeichern in das richtige dict
                        self.__ai_possible_places[spielerID].append([koord[0] + 1, koord[1] + 1, "ur"])

        else:
            # es gibt keine möglichen Ecken
            #raise BlokusException("Es gibt keine möglichen Ecken")
            pass

        # Zurücksetzen der temporären Sachen
        self.__temp_poss_place_dict = {}
        self.__ai_possible_places_counter = 0

    def __ai_place_first_piece(self, spielerID:int, piece_key:str):
        # Initialisierung des Dic für possible Places für spätere Pieces
        self.__ai_possible_places[spielerID] = []

        # Holen des Pieces und Bestimmung der Länge und Höhe
        piece_by_key = self.__availeblePieces[spielerID][piece_key]
        piece_form = piece_by_key.getForm()
        lenght = len(piece_form[0])
        height = len(piece_form)

        # Auswahl der Ecke die genutzt werden soll
        corner_list = [key for key, value in self.__corners.items() if not value]
        corner = random.choice(corner_list)

        # Bestimmung Start Koordinaten
        if corner == "ol":
            start_x = 0
            start_y = 0
        elif corner == "or":
            start_x = self.__fieldsize - lenght
            start_y = 0
        elif corner == "ul":
            start_x = 0
            start_y = self.__fieldsize - height
        elif corner == "ur":
            start_x = self.__fieldsize - lenght
            start_y = self.__fieldsize - height

        # Platzierung des ersten Pieces
        rot = "" # Variable um die Rotation durchführen zu können
        for r in range(4):
            try:
                self.placePieceByKey(piece_key, start_x, start_y, spielerID, rot)
                if self.__corners[corner] == True:
                    break
            except BlokusException:
                rot += "r"
                continue



    def placePieceByKey(self, pieceKey:str, start_x, start_y, spielerID:int, operations:str = ''):
        piece = self.__availeblePieces[spielerID][pieceKey]
        cloned_piece = copy.copy(piece)
        if self.__isPieceAvaileble(spielerID, pieceKey) == True:

            for o in operations:
                if o == 'r':
                    cloned_piece.rotate(1)
                elif o == 'x':
                    cloned_piece.flip(0)
                elif o == 'y':
                    cloned_piece.flip(1)
                elif o == '':
                    continue
                else:
                    raise BlokusException("Die Operation ist nicht bekannt")

            if self.__placePiece(cloned_piece, start_x, start_y, spielerID) == True:
                self.__deleteAvaileblePiece(spielerID, pieceKey)
        else:
            raise BlokusException("Das Piece wurde bereits platziert")

    def __placePiece(self, piece:BlokusPiece, start_x, start_y, spielerID:int):
        if self.__isFirstPiece[spielerID] == True:
            return self.__placeFirstPiece(piece, start_x, start_y, spielerID) #Funktion gibt einen boolschen Wert zurück
        else:
            return self.__placeValidatePiece(piece, start_x, start_y, spielerID) #Funktion gibt einen boolschen Wert zurück


    def __placeFirstPiece(self, piece:BlokusPiece, start_x, start_y, spielerID:int)->bool:
        form = piece.getForm()

        if self.__validateFirstPiece(piece, start_x, start_y) == False:
            return False

        for y in range(len(form)):
            for x in range(len(form[y])):
                if form[y][x] == 1:
                    self.__feld[y + start_y, x + start_x] = spielerID

                    # Speichern der möglichen Plätze für das nächste Piece für AI-Spieler
                    if self.__is_player_ai[spielerID] == True:
                        self.__temp_poss_place_dict[self.__ai_possible_places_counter] = [y + start_y, x + start_x]
                        self.__ai_possible_places_counter += 1

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

                    # Speichern der möglichen Plätze für das nächste Piece für AI-Spieler
                    if self.__is_player_ai[spielerID] == True:
                        self.__temp_poss_place_dict[self.__ai_possible_places_counter] = [y + start_y, x + start_x]
                        self.__ai_possible_places_counter += 1
        return True


    def __validatePiece(self, piece:BlokusPiece, start_x, start_y, spielerID): # spielerID = farbe
        form = piece.getForm()
        ecke = False

        #Out-of-Bounds
        if (start_x + len(form[0])) > self.__fieldsize or (start_y + len(form)) > self.__fieldsize or start_x < 0 or start_y < 0: #Out-of-bounds
            raise BlokusException("Die Eingabe liegt nicht im Feld")
            return False

        for y in range(len(form)):
            for x in range(len(form[y])):

                # Ist an der Stelle schon ein Piece?
                if form[y][x] == 1:
                    if self.__feld[y + start_y, x + start_x] > 0: # Überprüfung ob an er Stelle schon ein Piece liegt, egal welcher Farbe (>0 = irgend ein piece
                        raise BlokusException("An der Stelle liegt schon ein Piece")
                        return False

        #Liegt es Seite an Seite zu einem anderen Piece der gleichen Farbe? Soll es nicht!
                if form[y][x] == 1:
                    if (x + start_x + 1) < self.__fieldsize:
                        if (self.__feld[y + start_y, x + start_x + 1] == spielerID): #gucke eins nach rechts und guck ob da nen piece ist, wenn ja, brich ab
                            raise BlokusException("Das piece berührt mit einer Seite ein anderes Piece")
                            return False
                    if (x + start_x - 1) >= 0: # Soll nur checken wenn es nicht negativ  wird
                        if (self.__feld[y + start_y, x + start_x - 1] == spielerID): #gucke eins nach links und guck ob da nen piece ist
                            raise BlokusException("Das piece berührt mit einer Seite ein anderes Piece")
                            return False
                    if (y + start_y + 1) < self.__fieldsize:
                        if (self.__feld[y + start_y + 1, x + start_x] == spielerID): #gucke eins nach unten und guck ob da nen piece ist
                            raise BlokusException("Das piece berührt mit einer Seite ein anderes Piece")
                            return False
                    if (y + start_y - 1) >= 0: # Soll nur checken wenn es nicht negativ  wird
                        if (self.__feld[y + start_y - 1, x + start_x] == spielerID): #gucke eins nach oben und guck ob da nen piece ist
                            raise BlokusException("Das piece berührt mit einer Seite ein anderes Piece")
                            return False

        #Eckt es an ein anderes an? Soll es!
                if form[y][x] == 1 and ecke == False: #ToDo: soll es hier auch den Fall für links mit -1 abfangen?
                    if ((y + start_y - 1) >= 0) and ((x + start_x - 1) >= 0):
                        if (self.__feld[y + start_y - 1, x + start_x - 1] == spielerID and ecke == False): #gucke ob Ecke oben links ne 1 ist, wenn ja = gut
                            ecke = True

                    if ((y + start_y - 1) >= 0):
                        if ((x + start_x + 1) < self.__fieldsize) and ecke == False:
                            if (self.__feld[y + start_y - 1, x + start_x + 1] == spielerID): #gucke ob Ecke oben rechts ne 1 ist, wenn ja = gut
                                ecke = True

                    if ((x + start_x - 1) >= 0):
                        if ((y + start_y + 1) < self.__fieldsize and (x + start_x + 1) < self.__fieldsize) and ecke == False:
                            if (self.__feld[y + start_y + 1, x + start_x - 1] == spielerID): #gucke ob Ecke unten links ne 1 ist, wenn ja = gut
                                ecke = True
                            if (self.__feld[y + start_y + 1, x + start_x + 1] == spielerID): #gucke ob Ecke unten rechts ne 1 ist, wenn ja = gut
                                ecke = True
        if ecke == False:
            raise BlokusException("Das Piece muss mit einer Ecke an einer anderen liegen")
        return ecke


    def __validateFirstPiece(self, piece:BlokusPiece, start_x, start_y):
        form = piece.getForm()
        if (start_x + len(form[0])) > self.__fieldsize or (start_y + len(form)) > self.__fieldsize or start_x < 0 or start_y < 0: #Out-of-bounds
            raise BlokusException("Die Eingabe liegt nicht im Feld")
            return False

        if (form[0][0] == 1) and (start_x == 0) and (start_y == 0): # Test für Ecke oben links / die Form hat immer den Wert 1, deswegen wird auf 1 geprüft und nicht die eigentliche Spielerzahl
            if self.__corners["ol"] == True:
                raise BlokusException("Die Ecke oben links ist nicht frei")
                return False
            self.__corners["ol"] = True
            return True
        elif (form[0][-1] == 1) and ((start_x + len(form[0])) == self.__fieldsize) and (start_y == 0): # Test für Ecke oben rechts
            if self.__corners["or"] == True:
                raise BlokusException("Die Ecke oben rechts ist nicht frei")
                return False
            self.__corners["or"] = True
            return True
        elif (form[-1][0] == 1) and (start_x == 0) and ((start_y + len(form)) == self.__fieldsize): # Test für Ecke unten links
            if self.__corners["ul"] == True:
                raise BlokusException("Die Ecke unten links ist nicht frei")
                return False
            self.__corners["ul"] = True
            return True
        elif (form[-1][-1] == 1) and ((start_x + len(form[0])) == self.__fieldsize) and ((start_y + len(form)) == self.__fieldsize): # Test für Ecke unten rechts
            if self.__corners["ur"] == True:
                raise BlokusException("Die Ecke unten rechts ist nicht frei")
                return False
            self.__corners["ur"] = True
            return True
        else:
            raise BlokusException("Das erste Piece liegt in keiner Ecke")
            return False

