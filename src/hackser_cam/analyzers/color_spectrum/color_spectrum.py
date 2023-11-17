import cv2 as cv
import numpy

from .. import analyzer


class color_spectrum(analyzer):
    def __init__(self):
        # verwendet als variablen deklaration
        self.img = None

    def run(self, img) -> float:
        # eigentlicher init
        self.img = img
        return 0.0

    def update(self):
        # refresht für jeden frame
        print(self.img.shape)
        pass
