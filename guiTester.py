import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import numpy as np


class MyWindow(QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("Adhesive Tape Test")
        layout = QVBoxLayout()
        self.initUI(layout)

    def initUI(self, layout):
        self.btnBFile = QPushButton("Import Base Image")
        self.btnBFile.clicked.connect(self.getfile)
        self.btnBFile.clicked.connect(self.printer)

        self.btnAFile = QPushButton("Import After Image")
        self.btnAFile.clicked.connect(self.getfile)
        self.btnAFile.clicked.connect(self.printer)

        self.btnPrint = QPushButton('Printer Button')
        self.btnPrint.clicked.connect(self.printer)

        self.le = QLabel("Hello")

        layout.addWidget(self.btnBFile)
        layout.addWidget(self.btnAFile)
        layout.addWidget(self.btnPrint)
        layout.addWidget(self.le)

        self.setLayout(layout)

    def printer(self):
        self.le.setText('You Pressed the button')

    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'Documents\\', "Image files (*.jpg *.gif *.png)")

    def findRating(self):
        # img1 is baseline image with 0 peel off
        img1 = cv2.imread('img1B.jpg')  # open up baseline image

        grayImage = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)  # convert from color to gray
        (thresh, img1_bw) = cv2.threshold(grayImage, 127, 255,
                                          cv2.THRESH_BINARY)  # convert from gray to black and white
        # cv2.imshow('Baseline Image BW', img1_bw)  # display black and white image

        # Count number of black and white pixels in baseline image
        number_of_white_pix1 = np.sum(img1_bw == 255)
        number_of_black_pix1 = np.sum(img1_bw == 0)

        remaining_white1 = number_of_white_pix1 - number_of_white_pix1
        ratio1 = remaining_white1 / number_of_black_pix1

        # Loop through all images added (currently from 2-6)
        for i in range(1, 2):
            img_new = cv2.imread('img' + str(i) + 'A.jpg')  # Read the image
            grayImage = cv2.cvtColor(img_new, cv2.COLOR_BGR2GRAY)  # convert to gray
            (thresh, img_new_bw) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)  # convert to black and white
            # cv2.imshow('Image' + str(i) + 'BW', img_new_bw)  # display black and white image

            # Count number of black and white pixels in following images
            number_of_white_pix_new = np.sum(img_new_bw == 255)
            number_of_black_pix_new = np.sum(img_new_bw == 0)

            # Remaining black pixels are added ones not originally in the grid
            peeled = abs(number_of_white_pix1 - number_of_white_pix_new)
            ratio_new = peeled / number_of_white_pix1
            print("Rating for Image " + str(i) + ":", self.get_rating(ratio_new),
                  "with percent: %" + str(ratio_new * 100))

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def get_rating(ratio):
        if ratio < 0.01:  # If ratio is essentially 0
            rating = 5
        elif ratio < 0.05:  # less than 5%
            rating = 4
        elif ratio < 0.15:  # less than 15%
            rating = 3
        elif ratio < 0.35:  # less than 35%
            rating = 2
        elif ratio < 0.65:  # less than 65%
            rating = 1
        elif ratio > 0.65:  # greater than 65%
            rating = 0
        else:
            rating = "Error"
        # Return rating back
        return rating


def main():
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

