import numpy as np
import cv2
import imutils

from .. import analyzer

class FFT_analyzer(analyzer):
    def run(self, img):
        size = 60
        threshold = 20

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