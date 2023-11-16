import cv2 as cv
import diplib as dip
import numpy as np

from .. import analyzer

class edge_detector(analyzer):
    def __init__(self):
        self.edges = None
        self.filtered_edges = None
        self.apply_filter = True
        self.threshold = 10

    def convertToNumpyArr(self, obj):
        edges_np = np.array(self.filtered_edges)
            
        # Ensure the data type is uint8
        edges_np = edges_np.astype(np.uint8)

        # If the image is binary, rescale it to 0-255
        if edges_np.max() == 1:
            edges_np *= 255

        return edges_np

    def run(self, img) -> float:
        # get all edges
        self.edges = cv.Canny(img, 80, 80)

        # minify edges
        min_threshold = 100
        self.filtered_edges = dip.BinaryAreaOpening(self.edges > 0, min_threshold)

        # Convert BinaryAreaOpening output to numpy array
        self.filtered_edges = self.convertToNumpyArr(self.filtered_edges)
        
        # Count the edges
        contours, _ = cv.findContours(self.filtered_edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        number_of_edges = len(contours)

        print(f'COUNT: {number_of_edges}')

        return 0.0
    
    def update(self):
        if self.apply_filter:
            cv.imshow('Edges', self.filtered_edges)
        else:
            cv.imshow('Edges', self.edges)
            