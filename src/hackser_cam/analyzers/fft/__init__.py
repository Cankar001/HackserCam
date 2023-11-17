import cv2
import imutils
import numpy as np

from .. import analyzer


class FFT_analyzer(analyzer):
    def __init__(self, ref_img):
        self.m = 0.0
        self.b = 0.0
        self.cleanest = calc_fft(ref_img)
        self.peakFuzzyInit(self.cleanest, 10)
        self.high = 25
        self.low = 5

    def run(self, img):
        mean = calc_fft(img)
        if 0 < mean < self.low:
            self.low = mean
        if mean > self.high:
            self.high = mean
        return 1 - ((mean - self.low) / (self.high - self.low))

    def peakFuzzyInit(self, highestPeak, lowestPeak):
        self.m = -1 / (highestPeak - lowestPeak)
        self.b = -self.m * highestPeak
        # print("H-Peak:",highestPeak," L-Peak:",lowestPeak)
        # print("M:",m," B:",b)


def calc_fft(img) -> float:
    size = 60
    threshold = 15
    img = imutils.resize(img, width=500)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    (height, width) = gray.shape
    (center_y, center_x) = (int(height / 2.0), int(width / 2.0))

    fft = np.fft.fft2(gray)
    fft_shift = np.fft.fftshift(fft)

    fft_shift[center_y - size : center_y + size, center_x - size : center_x + size] = 0
    fft_shift = np.fft.ifftshift(fft_shift)
    ifft = np.fft.ifft2(fft_shift)

    spectrum = 20 * np.log(np.abs(ifft))
    mean = np.mean(spectrum)
    return mean


def clamp(mean, max_num=1.0, min_num=0.0):
    return max(min(max_num, mean), min_num)
