import numpy as np
import cv2 as cv
filename = 'book scans/sections/section6.jpg'
# filename = 'test0.jpg'

from matplotlib import pyplot as plt
from tqdm import tqdm
import svgwrite
from svgwrite.extensions.shapes import ngon, rotate, translate, scale
import math
import graph
import copy
import random
from PIL import Image 
import PIL 
import os
FILES = 9
count = 0
for file in tqdm(range(1, FILES+1)):

    filename = 'bookscans/sections/Page1/section' + str(file) +'.jpg'
    print(filename)
    img = cv.imread(filename)
    # img = cv.filter2D(img, -1, kernel)

    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    # plt.imshow(img)
    # plt.show()
    height,width = gray.shape[:2]
    gray[gray<200] = 0
    gray[gray>200] = 255
    img = cv.resize(img, (int(width*1.5), int(height*1.5)), interpolation = cv.INTER_AREA)
    gray = cv.resize(gray, (int(width*1.5), int(height*1.5)), interpolation = cv.INTER_AREA)


    

    # gray = cv.medianBlur(gray,3)
    dst = cv.cornerHarris(gray,6,5,0.04)


    HARRIS_THRESHOLD = 0.1


    svgpoints = np.zeros(dst.shape).astype(np.uint8)
    # img = cv.medianBlur(img,3)
    svgpoints[dst>HARRIS_THRESHOLD*dst.max()] = 255



    ret, thresh = cv.threshold(svgpoints, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    corners = []
    for c in contours:

       M = cv.moments(c)
       if M["m00"] != 0:
           cX = int(M["m10"] / M["m00"])
           cY = int(M["m01"] / M["m00"])
           # img[cY][cX] = [0,0,255]
           corners.append(np.array([cY, cX]))
    corners = np.array(corners)



    # corners = np.argwhere(svgpoints==255)

    # plt.imshow(img)
    # plt.show()



    gray[gray<200] = 0 
    gray[gray>200] = 255 
    # plt.imshow(gray)
    # plt.show()

    height, width = img.shape[:2]

    windowSize = 3
    def testForBlack(image, windowSize, location):
        x = location[1]
        y = location[0]
        window = image[y - windowSize:y+ windowSize+1,x - windowSize:x+ windowSize+1]
        if np.sum(window) < (2*windowSize +1 ) **2 * 255 - 600:
            # print(window)
            # print(np.sum(window))
            return True
        else:
            return False



     



    g = graph.cropGraph(len(corners))
    edges =[]
    dists = 0
    print("detecting Lines")
    for index, corner in tqdm(enumerate(corners)):
        # dwg.add(dwg.text(str(index), (corner[1], corner[0])))
        testCorner = corner
        for otherIndex, other in enumerate(corners):
            if index != otherIndex:
                midpoint = ((other + testCorner) / 2).astype(np.int)
                vector = other - testCorner
                connected =True

                for x in range(500):
                    # print(x)
                    if not testForBlack(gray, 3, (random.uniform(0,1) * vector + testCorner).astype(np.int)):
                        connected = False
                        break
                if connected:
                    edges.append([(index,otherIndex), math.dist(corners[index], corners[otherIndex])]) 
                    # dists += math.dist(corners[index], corners[otherIndex])
                    # g.addEdge(index, otherIndex)

    avg = dists/len(edges)

    # print(edges)
    maxdist = 0
    for x in edges:
        # print(x[1]-avg)
        # if x[1] < 3*avg:
        g.addEdge(x[0][0], x[0][1])

    # print(maxdist)
    ccs = g.connectedComponents()
    print("Following are connected components")
    print(ccs)

    print((width,height))
    for index, cc in enumerate(ccs):
        minX =width
        minY= height
        maxY = 0
        maxX = 0
        for vertex in cc:
                point = corners[vertex]
                if point[0] < minY:
                    minY = point[0]
                if point[0] > maxY:
                    maxY = point[0]
                if point[1] < minX:
                    minX = point[1]
                if point[1] > maxX:
                    maxX = point[1]

        print((max(0,minX -50), max(0,minY-50), min(maxX +50, width), min(maxY +50, height)))
        im = Image.fromarray(np.uint8(img))
        im1 = im.crop((max(0,minX -20), max(0,minY-20), min(maxX +20, width), min(maxY +20, height)))
        directory = "bookscans/cropped/Page1/section" + str(file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        im1.save(directory + "/gram" +str(index) +".jpg")
        im1.save("bookscans/allCropped/page1-" + str(count) +".jpg")

        count+= 1
