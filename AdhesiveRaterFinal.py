import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import numpy as np
import os


class MyWindow(QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setGeometry(500, 200, 800, 600)
        self.setWindowTitle("Adhesive Tape Test")
        self.setStyleSheet("background-color: lightgreen;")
        layout = QVBoxLayout()
        self.initUI(layout)

    def initUI(self, layout):
        font = 'Arial'
        self.title = QLabel("Adhesive Test Rater")
        self.title.setAlignment(Qt.AlignHCenter)
        self.title.setFont(QFont(font, 25))

        self.author = QLabel("by: Rishabh Kanodia and Dylan Winer")
        self.author.setAlignment(Qt.AlignHCenter)
        self.author.setFont(QFont(font, 10))

        self.btnBFile = QPushButton("Import Base Image")
        self.btnBFile.setFixedSize(600,100)
        self.btnBFile.setStyleSheet("QPushButton{background-color : lightblue;} QPushButton::pressed{background-color : blue;} QPushButton::hover{background-color : blue;}")
        self.btnBFile.setFont(QFont(font, 15))
        self.fileBName = 'none'
        self.Bpressed = False
        self.btnBFile.clicked.connect(self.getBfile)

        self.btnAFile = QPushButton("Import After Image")
        self.btnAFile.setFixedSize(600,100)
        self.btnAFile.setStyleSheet("QPushButton{background-color : lightblue;} QPushButton::pressed{background-color : blue;} QPushButton::hover{background-color : blue;}")
        self.btnAFile.setFont(QFont(font, 15))
        self.fileAName = 'none'
        self.Apressed = False
        self.btnAFile.clicked.connect(self.getAfile)

        self.btnPrint = QPushButton('Run Analysis')
        self.btnPrint.setStyleSheet("QPushButton{background-color : lightblue;} QPushButton::pressed{background-color : blue;} QPushButton::hover{background-color : blue;}")
        self.btnPrint.setFixedSize(600,100)
        self.btnPrint.setFont(QFont(font, 15))
        self.btnPrint.clicked.connect(self.printer)

        self.le = QLabel("Output")
        self.le.setAlignment(Qt.AlignCenter)
        self.le.setFont(QFont(font, 15))
        self.output = QLabel('...')
        self.output.setAlignment(Qt.AlignHCenter)
        self.output.setFont(QFont(font, 15))

        layout.addWidget(self.title)
        layout.addWidget(self.author)
        layout.addWidget(self.btnBFile)
        layout.addWidget(self.btnAFile)
        layout.addWidget(self.btnPrint)
        layout.addWidget(self.le)
        layout.addWidget(self.output)
        layout.setAlignment(Qt.AlignHCenter)

        self.setLayout(layout)


    def printer(self):
        print('Run Analysis was pressed')
        if self.Apressed and self.Bpressed:
            self.findRating()
            self.le.setText('Calculating ASTM Rating...')
        else:
            self.le.setText('Please select BOTH a base image and after image.')

    def getAfile(self):
        path = QFileDialog.getOpenFileName(self, 'Open file', 'Documents\\', "Image files (*.jpg *.gif *.png)")
        path = path[0]
        fname = os.path.basename(path)
        self.fileAName = fname
        self.Apressed = True
        print('Get \'A\' File was pressed. File chosen is: ', fname)

    def getBfile(self):
        path = QFileDialog.getOpenFileName(self, 'Open file', 'Documents\\', "Image files (*.jpg *.gif *.png)")
        path = path[0]
        fname = os.path.basename(path)
        self.fileBName = fname
        self.Bpressed = True
        print('Get \'B\' File was pressed. File chosen is: ', fname)

    def findRating(self):
        # img1 is baseline image with 0 peel off
        img1 = cv2.imread(self.fileBName)  # open up baseline image

        grayImage = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)  # convert from color to gray
        (thresh, img1_bw) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)  # convert from gray to black and white
        # cv2.imshow('Baseline Image BW', img1_bw)  # display black and white image

        number_of_white_pix1 = np.sum(img1_bw == 255)
        number_of_black_pix1 = np.sum(img1_bw == 0)

        for i in range(1, 2):
            img_new = cv2.imread(self.fileAName)  # Read the image
            grayImage = cv2.cvtColor(img_new, cv2.COLOR_BGR2GRAY)  # convert to gray
            (thresh, img_new_bw) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)  # convert to black and white
            # cv2.imshow('Image' + str(i) + 'BW', img_new_bw)  # display black and white image

            number_of_white_pix_new = np.sum(img_new_bw == 255)

            # Remaining black pixels are added ones not originally in the grid
            peeled = abs(number_of_white_pix1 - number_of_white_pix_new)
            ratio_new = peeled / number_of_white_pix1
            outRating = 'Rating for Image ' + str(i) + ': ' + str(self.get_rating(ratio_new)) + ' with ' + str(round(ratio_new * 100, 3)) + '% removed.'
            print(outRating)
            if ratio_new > 1:
                self.output.setText('Images might be flipped. Please reselect correct images.')
            else:
                self.output.setText(outRating)

    def get_rating(self, ratio):
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
        return rating

def main():
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

