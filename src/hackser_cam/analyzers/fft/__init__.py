import numpy as np
import cv2
import imutils

from .. import analyzer

class FFT_analyzer(analyzer):
    def run(self, img):
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

        return map_fft_to_float(mean)

def map_fft_to_float(mean, max_num=30.0, min_num=10.0):
    mean_clamp = max(min(max_num, mean), min_num)
    # return mean_clamp * -0.1 + 2.0
    return 1.0 - ( ( mean_clamp - min_num ) / ( max_num - min_num ) )