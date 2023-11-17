import numpy as np
import cv2
import imutils

from .. import analyzer

class FFT_analyzer(analyzer):
    def __init__(self, ref_img):
        self.cleanest = calc_fft(ref_img)
        peakFuzzyInit(self.cleanest, 12)


    def run(self, img):
        self.m=0.0
        self.b=0.0
        mean = 1.0
        mean = calc_fft(img)
        if mean > self.cleanest:
            self.cleanest = mean
            peakFuzzyInit(self.cleanest, 12)

        return self.m * mean + self.b
        #return map_fft_to_float(mean)

def calc_fft(img)->float:
    size = 60
    threshold = 15
    img = imutils.resize(img, width=500)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    (height, width) = gray.shape
    (center_y, center_x) = (int(height / 2.0), int(width / 2.0))

    fft = np.fft.fft2(gray)
    fft_shift = np.fft.fftshift(fft)

    fft_shift[center_y - size: center_y + size, center_x - size: center_x + size] = 0
    fft_shift = np.fft.ifftshift(fft_shift)
    ifft = np.fft.ifft2(fft_shift)

    spectrum = 20 * np.log(np.abs(ifft))
    mean = np.mean(spectrum)
    return mean


def map_fft_to_float(mean, max_num=30.0, min_num=10.0):
    mean_clamp = max(min(max_num, mean), min_num)
    # return mean_clamp * -0.1 + 2.0
    return 1.0 - ( ( mean_clamp - min_num ) / ( max_num - min_num ) )

def peakFuzzyInit(highestPeak, lowestPeak):
    self.m = -1/(highestPeak-lowestPeak)
    self.b = -m*highestPeak
    #print("H-Peak:",highestPeak," L-Peak:",lowestPeak)
    #print("M:",m," B:",b)
