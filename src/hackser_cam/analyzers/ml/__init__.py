from .. import analyzer
import pickle
import sklearn
import matplotlib.pyplot as plt
import numpy as np
from skimage.transform import resize

features = ["clean", "dirty"]
feature_vals = [0, 1]

class ml_analyzer(analyzer):
    def __init__(self):
        with open("model.p", "rb") as f:
            self.model = pickle.load(f)

    import matplotlib.pyplot as plt

    def test_img(self, img):
        flat_data = []
        # Resize image
        img_resized = resize(img,(150,150,3))
        flat_data.append(img_resized.flatten())
        flat_data = np.array(flat_data)
        y_output = self.model.predict(flat_data)
        y_output_str = features[y_output[0]]
        print("ML PREDICTED OUTPUT IS:",y_output_str)
        return feature_vals[y_output[0]]
    
    def run(self, img):
        res = self.test_img(img)
        return float(res)