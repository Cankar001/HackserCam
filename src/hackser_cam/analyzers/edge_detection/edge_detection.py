import cv2 as cv

from .. import analyzer

class edge_detector(analyzer):
    def __init__(self):
        self.edges = None

    def run(self, img) -> float:
        self.edges = cv.Canny(img, 80, 80)
        return 0.0
    
    def update(self):
        cv.imshow('Edges', self.edges)
        #for edge in self.edges:
        #    print(edge)
    