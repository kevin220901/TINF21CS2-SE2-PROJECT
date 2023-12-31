import numpy as np

class BlokusPiece:
    def __init__(self, form:np.array):
        self.__formbasic = form
        self.__form = form

    # Drehen gegen den Uhrzeiger
    def rotate(self, k:int):
        self.__form = np.rot90(self.__form, k)
        return self.__form
    
    # Flip ist an der y-Achse
    def flip(self, axis:int):
        self.__form = np.flip(self.__form, axis)
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

    def serialize(self):
        return self.__form.tolist()