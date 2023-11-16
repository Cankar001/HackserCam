import cv2 as cv
from .. import analyzer
import numpy

class color_spectrum (analyzer):

    def __init__(self):
        #verwendet als variablen deklaration
        self.img = None
        self.width = 0
        self.height = 0
        self.bgr_spectrum = [0, 0, 0]
        threshold =[]


    def run(self, img) -> float:
        #eigentlicher analyser mit fuzzy-wert(0 bis 1) als rückgabe
        self.img = img
        self.create_spec()
        return 0.0

    def create_spec(self):

        self.height = len(self.img[0])
        self.width = len(self.img)

        # Summen Spektrum
        for color in range(0, 3):
            self.bgr_spectrum[color]=0
            for x in range(0, self.width):
                for y in range(0, self.height):
                    self.bgr_spectrum[color] += self.img[x][y][color]

        print(self.bgr_spectrum[0])
        print(self.bgr_spectrum[1])
        print(self.bgr_spectrum[2])

    def update(self):
        #für einen seperaten view



        pass