

# Co-Author: Dylan Winer
# Co-Author: Rishabh Kanodia
# Date 07/05/2022
# Version 1.2
# Supervisor: Sean Psulkowski
# Supervisor: Bryant Rodriguez
# Sponsor: Dr. Dickens


# Import opencv and numpy
import cv2
import numpy as np
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# matplotlib for any graphs
# import matplotlib.pyplot as plt


# Function takes in ratio and outputs a rating
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

# img1 is baseline image with 0 peel off
img1 = cv2.imread('img1B.jpg')  # open up baseline image

grayImage = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)  # convert from color to gray
(thresh, img1_bw) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)  # convert from gray to black and white
cv2.imshow('Baseline Image BW', img1_bw)  # display black and white image


# Count number of black and white pixels in baseline image
number_of_white_pix1 = np.sum(img1_bw == 255)
number_of_black_pix1 = np.sum(img1_bw == 0)

print("White in baseline:", number_of_white_pix1)
print("Black in baseline:", number_of_black_pix1)

# Calculate number of added black pixels by subtracting the black ones from original (eliminates black from grid)
remaining_white1 = number_of_white_pix1 - number_of_white_pix1
# Take ratio of added black pixels divided by total available pixels, which is white ones from baseline
ratio1 = remaining_white1 / number_of_black_pix1

# Print out the ratio of the baseline, which should be 0 with approximately 0%
print("Rating for baseline:", get_rating(ratio1), "with percent %"+str(ratio1*100))

# Loop through all images added (currently from 2-6)
for i in range(1, 2):
    img_new = cv2.imread('img'+str(i)+'A.jpg')  # Read the image
    grayImage = cv2.cvtColor(img_new, cv2.COLOR_BGR2GRAY)  # convert to gray
    (thresh, img_new_bw) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)  # convert to black and white
    cv2.imshow('Image' + str(i) + 'BW', img_new_bw)  # display black and white image

    # Count number of black and white pixels in following images
    number_of_white_pix_new = np.sum(img_new_bw == 255)
    number_of_black_pix_new = np.sum(img_new_bw == 0)
    # Could optionally print out number of black and white pixels if needed for future tests
    print("White in new img:", number_of_white_pix_new)
    print("Black in new img:", number_of_black_pix_new)

    # Remaining black pixels are added ones not originally in the grid
    peeled = abs(number_of_white_pix1 - number_of_white_pix_new)
    # Get ratio of black added to white area originally available
    ratio_new = peeled / number_of_white_pix1
    # Print out rating to terminal along with percent ratio
    print("Rating for Image "+str(i)+":", get_rating(ratio_new), "with percent: %" + str(ratio_new * 100))

# waitKey and destroyWindows so the images can be opened and closed
cv2.waitKey(0)
cv2.destroyAllWindows()
