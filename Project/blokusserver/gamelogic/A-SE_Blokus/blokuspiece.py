import numpy as np

##################################################
## Author: Cynthia Winkler
##################################################

class BlokusPiece:
    def __init__(self, form:np.array):
        self.__formbasic = form
        self.__form = form

    # Drehen gegen den Uhrzeiger
    def rotieren(self):
        rotated = list(zip(*self.__form))[::-1]
        self.__form = np.array(rotated)
        return self.__form

    def xSpiegelung(self):
        self.__form = self.__form[::-1]
        return self.__form

    def ySpiegelung(self):
        self.__form = self.xSpiegelung()
        self.__form = self.rotieren()
        rot2 = self.rotieren()
        self.__form = np.array(rot2)
        return self.__form

    def getForm(self):
        return self.__form

    def print(self):
        print(self.__form)