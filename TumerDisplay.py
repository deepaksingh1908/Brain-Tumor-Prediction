import numpy as np
import cv2 as cv


class TumerDisplay:
    ImgCur = 0
    Imgs = 0

    def readImage(self, imgs):
        self.Imgs = np.array(imgs)
        self.ImgCur = np.array(imgs)
        rayen = cv.cvtColor(np.array(imgs), cv.COLOR_BGR2GRAY)
        self.etrd, self.resh = cv.threshold(rayen, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    def getImage(self):
        return self.ImgCur

    # remove noise
    def removeNoise(self):
        self.kernel = np.ones((3, 3), np.uint8)
        opening = cv.morphologyEx(self.resh, cv.MORPH_OPEN, self.kernel, iterations=2)
        self.ImgCur = opening

    def TumerDisplay(self):
        # background area color
        sure_bg = cv.dilate(self.ImgCur, self.kernel, iterations=3)

        # Find color foreground area
        dist_transform = cv.distanceTransform(self.ImgCur, cv.DIST_L2, 5)
        etrd, sure_fg = cv.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

        # unknown region finding
        sure_fg = np.uint8(sure_fg)
        unknown = cv.subtract(sure_bg, sure_fg)

        # labelling mark
        etrd, Mark = cv.connectedComponents(sure_fg)

        # Adding 1 to every lable so that color background is not 0
        Mark = Mark + 1

        # now mark unknow region with 0
        Mark[unknown == 255] = 0
        Mark = cv.watershed(self.Imgs, Mark)
        self.Imgs[Mark == -1] = [255, 0, 0]

        tumorImage = cv.cvtColor(self.Imgs, cv.COLOR_HSV2BGR)
        self.ImgCur = tumorImage