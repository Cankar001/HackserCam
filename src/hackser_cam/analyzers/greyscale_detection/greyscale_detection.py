from .. import analyzer
import cv2 as cv
from matplotlib import pyplot as plt


def normalize(img, val):
    for col in range(0, len(img)):
        for row in range(0, len(img[col])):
            img[col, row] += val
    return img

def getPixelDistance(pix1, pix2):
    distance = pix1 - pix2
    if distance < 0:
        return -distance
    else:
        return distance

def findPeakIndex(toSearch):
    momMax = 0
    for i in range(1, len(toSearch)):
        if toSearch[i][0] > toSearch[momMax][0]: momMax = i
    return [momMax, toSearch[momMax][0]]

def peakFuzzyInit(highestPeak, lowestPeak):
    m = -1/(highestPeak-lowestPeak)
    b = -m*highestPeak
    print("H-Peak:",highestPeak," L-Peak:",lowestPeak)
    print("M:",m," B:",b)
    return [m, b]


class greyscale_detector(analyzer):
    referenceOverall = 0
    highestPeak = 0
    lowestPeak = 0

    leftestPeak = 0
    rightestPeak = 0

    lastImg = None

    def __init__(self, img):
        self.generateReference(img)
        print()

    def generateReference(self, img):  # Used to generate a reference value for testing
        cropped = img[100:len(img), 60:len(img[0]) - 60]
        greyscaleimg = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
        numPixels = 0
        pixelSum = 0

        for col in range(0, len(greyscaleimg)):
            for row in range(0, len(greyscaleimg[col])):
                pixelSum += greyscaleimg[col, row]; numPixels += 1

        hist = cv.calcHist([greyscaleimg], [0], None, [256], [0, 256])
        peak = findPeakIndex(hist)
        self.highestPeak = peak[1]
        self.leftestPeak = 35
        self.lowestPeak = self.highestPeak*0.57
        self.rightestPeak = 65

        self.referenceOverall = pixelSum/numPixels
        print("Set reference Overall to:", self.referenceOverall)

    def run(self, img) -> float:
        if self.referenceOverall == 0: self.generateReference(img); return 0.0
        greyscaleimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY); self.lastImg = greyscaleimg
        numPixels = 0
        pixelSum = 0

        for col in range(0, len(greyscaleimg)):
            for row in range(0, len(greyscaleimg[col])):
                pixelSum += greyscaleimg[col, row]; numPixels += 1

        newReference = pixelSum/numPixels
        greyscaleimg = normalize(greyscaleimg, self.referenceOverall-newReference)
        print("New reference Overall:",newReference)

        # Plot histogram
        hist = cv.calcHist([greyscaleimg], [0], None, [256], [0, 256])
        peak = findPeakIndex(hist)
        if peak[1] > 28000: print("WRONG DATA"); return -1

        correctionMargin = 0.40
        if peak[1] > self.highestPeak:
            if peak[1] < self.highestPeak*(1+correctionMargin):
                self.highestPeak = peak[1]
            else: print("WRONG DATA"); return -1
        #if peak[0] > self.rightestPeak: # Fixed rightest Peak to a set value
        #    if peak[0] < self.rightestPeak*(1+correctionMargin):
        #        self.rightestPeak = peak[0]
        #    else: print("WRONG DATA"); return -1

        if peak[1] < self.lowestPeak:
            if peak[1] > self.lowestPeak*(1-correctionMargin):
                self.lowestPeak = peak[1]
            else: print("WRONG DATA"); return -1
        if peak[0] < self.leftestPeak:
            if peak[0] > self.leftestPeak*(1-correctionMargin):
                self.leftestPeak = peak[0]
            else: print("WRONG DATA"); return -1

        print("peak:",peak[0]," val:",peak[1])

        func = peakFuzzyInit(self.highestPeak, self.lowestPeak)
        fuzzyval = func[0]*peak[1]+func[1]

        func = peakFuzzyInit(self.leftestPeak, self.rightestPeak)
        fuzzyval2 = func[0]*peak[0]+func[1]

        midfuzzy = (fuzzyval+fuzzyval2)/2
        print("high-fuzzy:",fuzzyval)
        print("side-fuzzy:",fuzzyval2)

        return midfuzzy

    def update(self):
        plt.figure(200, figsize=(2.5,2.5))
        plt.ion()
        plt.xlim([0, 256])
        plt.clf()

        hist = cv.calcHist([self.lastImg], [0], None, [256], [0, 256])

        plt.plot(hist)
        plt.show()
        plt.pause(0.01)



