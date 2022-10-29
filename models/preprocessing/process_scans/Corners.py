import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


import math
import PIL
from tqdm import tqdm


def findCorners(file, HARRIS_THRESHOLD , HARRIS_SIZE,  DEBUG):
    img = cv.imread(file)

    height, width = img.shape[:2]
    # if width < 400:
    img = cv.resize(img, (width*2, height*2))
        # return False, False


    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    gray[gray<200] = 0 
    gray[gray>200] = 255 
    # notEroded = gray
    if DEBUG:
        plt.imshow(gray)
        plt.show()

    gray = 255 - gray
    notEroded = gray


    # gray = cv.dilate(gray,3)
    # gray = cv.medianBlur(gray,3)
    # gray = cv.GaussianBlur(gray,(3, 3), 10)
    kernel = np.ones((3,3),np.uint8)
    gray = cv.erode(gray,kernel,iterations = 1)
    # kernel = np.ones((15,15),np.float32)/15**2
    # gray = cv.filter2D(gray,-1,kernel)

    if DEBUG:
        plt.imshow(gray)
        plt.show()

    # gray = cv.Canny(gray, 100, 200)
    # gray[gray<=50] = 0
    # gray[gray>50] = 255
    gray = np.float32(gray)
  
    # gray = cv.GaussianBlur(gray,(5, 5), 10)
    

    
    dst = cv.cornerHarris(gray,HARRIS_SIZE,5,0.04)

    svgpoints = np.zeros(dst.shape).astype(np.uint8)
    svgpoints[dst>HARRIS_THRESHOLD*dst.max()] = 255
    # svgpoints[gray<50] = 0
    if DEBUG:
        plt.imshow(dst)
        plt.show()
    ret, thresh = cv.threshold(svgpoints, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    corners = []

    if DEBUG:
        plt.imshow(thresh)
        plt.show()


    for c in contours:
       M = cv.moments(c)
       if M["m00"] != 0:
           cX = int(M["m10"] / M["m00"])
           cY = int(M["m01"] / M["m00"])
           img[cY][cX] = [0,0,255]
           corners.append(np.array([cY, cX]))
    corners = np.array(corners)

    if DEBUG:
        plt.imshow(img)
        plt.show()



    style = {"fill": "gray", "stroke-width": "2", "stroke":"black"}

    points = []
    shapes = []

    gray[gray<50] = 0 
    gray[gray>50] = 255 
    if DEBUG:
        plt.imshow(gray)
        plt.show()
    if DEBUG:
        plt.imshow(notEroded)
        plt.show()

    return corners, notEroded