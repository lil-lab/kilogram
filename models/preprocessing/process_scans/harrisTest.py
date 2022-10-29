import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from argparse import ArgumentParser

import svgwrite
from svgwrite.extensions.shapes import ngon, rotate, translate, scale
import math
import graph
import copy
import networkx as nx
import random
import PIL
from tqdm import tqdm
import os
filename = 'test0.jpg'
filename = 'test1.jpg'

# filename = 'book scans/cropped2.jpg'
# filename = 'test4.jpg'
# filename = 'test5.jpg'
# filename = 'test6.jpg'
# filename = 'test7.jpg'


def warn(*args, **kwargs): pass
import warnings; warnings.warn = warn


parser = ArgumentParser()

parser.add_argument("--debug", dest = "debug",
    required = True, help = "debug 1 for true 0 for false")

parser.add_argument("--folder", dest = "folder",
    required = True, help = "path to cropped files")



args = parser.parse_args()

DEBUG = int(args.debug)
FOLDER = args.folder
HARRIS_THRESHOLD = 0.1
EDGETESTPARAM = 200
EDGEWINDOW =3

fileidx = 0
for  filename in sorted(os.listdir(FOLDER)):
    if ".jpg" not in filename:
        continue

    print(filename)

    file = FOLDER + "/" +filename
    img = cv.imread(file)
    height, width = img.shape[:2]
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    gray = cv.medianBlur(gray,3)
    gray[gray<200] = 0
    gray[gray>200] = 255
    # gray = cv.GaussianBlur(gray,(5, 5), 10)
    if DEBUG:
        plt.imshow(gray)
        plt.show()
    
    dst = cv.cornerHarris(gray,12,11,0.04)


    

    # svgpoints = np.zeros(dst.shape).astype(np.uint8)
    # svgpoints[dst>HARRIS_THRESHOLD*dst.max()] = 255



    ret, thresh = cv.threshold(dst, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    corners = []
    for c in contours:

       M = cv.moments(c)
       if M["m00"] != 0:
           cX = int(M["m10"] / M["m00"])
           cY = int(M["m01"] / M["m00"])
           img[cY][cX] = [0,0,255]
           corners.append(np.array([cY, cX]))
    corners = np.array(corners)



    # corners = np.argwhere(svgpoints==255)
    if DEBUG:
        plt.imshow(img)
        plt.show()



    style = {"fill": "gray", "stroke-width": "2", "stroke":"black"}


    points = []
    shapes = []

    gray[gray<200] = 0 
    gray[gray>200] = 255 
    if DEBUG:
        plt.imshow(gray)
        plt.show()


    # findTriangles
    windowSize = 3
    def testForBlack(image, windowSize, location):
        x = location[1]
        y = location[0]
        window = image[y - windowSize:y+ windowSize+1,x - windowSize:x+ windowSize+1]
        # print(window)
        if np.sum(window) == (2*windowSize +1 ) ** 2 * 255 :
            # print(window)
            # print(np.sum(window))
            return False
        else:
            return True


    



    
     
    if DEBUG:
        dwg = svgwrite.Drawing(FOLDER + "/" + filename.replace("jpg", "svg"), (width + 50, height + 50), debug=True)
        # print(width+50)

        for index, corner in enumerate(corners):
            # print(corner[1])
            dwg.add(dwg.text(str(index), (corner[1], corner[0])))
        dwg.save()



    edges = {}
    for index, corner in enumerate(corners):
        # dwg.add(dwg.text(str(index), (corner[1], corner[0])))
        testCorner = corner
        for otherIndex, other in enumerate(corners):
            if otherIndex != index:
                vector = other - testCorner
                connected =True

                for x in range(100):
                    # print(x)
                    if not testForBlack(gray, EDGEWINDOW, (random.uniform(0,1) * vector + testCorner).astype(np.int)):
                        connected = False
                        break
                if connected:
                    if index in edges:
                        edges[index].append(otherIndex )
                    else:
                        edges[index] = []
                        edges[index].append(otherIndex)
    if DEBUG:
        print(edges)
    # print(corners)
    tris = set()
    quads = set()
    for index, data in edges.items():
        # print(data)
        # if len(data) == 2:
        #     tris.add(tuple(sorted((index, data[0], data[1]))))
        #     continue
        for connection in data:
            # print(connection)

            for backlink in edges[connection]:
                if backlink in data:
                    tris.add(tuple(sorted((backlink, index, connection ))))
                elif backlink != index:
                    for doubleBackLink in edges[backlink]:
                        if doubleBackLink not in edges[connection] and doubleBackLink != connection and doubleBackLink != index:
                            if doubleBackLink in data:
                                quads.add(tuple(( index, connection, backlink, doubleBackLink)))




    # print(trueTris)
    # print(quads)

  

    triRank = []
    for index, shape in enumerate(tris):

            a = corners[shape[0]]
            b = corners[shape[1]]
            c = corners[shape[2]]

            angles = graph.printAngle(a,b,c)
            if max(angles) < 120 and graph.triArea(a,b,c) > 500:
                triRank.append(shape)
            else:
                lines.append(shape)
            triRank = sorted(triRank, key=cmp_to_key(area_compare)) 
    # print(lines)
    print(triRank)
    if len(triRank) == 6:
        if area_compare(triRank[5], triRank[4])> 4000:
            triRank.remove(triRank[5])
        

    count = 0
    while len(triRank) > 5 and count<1000:

        for idx, tri in enumerate(triRank):
            for idx2, elem in enumerate(tri):
                for idx3, tri2 in enumerate(triRank[idx+1:]):
                    if elem == tri2[idx2]:
                        a, b, c = (corners[tri[0]], corners[tri[1]], corners[tri[2]])
                        angles1 = np.array([math.atan((b-a)[0]/ (b-a)[1]), math.atan((c-b)[0]/ (c-b)[1]), math.atan((a-c)[0]/ (a-c)[1])])
                        a, b, c  = (corners[tri2[0]], corners[tri2[1]], corners[tri2[2]])
                        angles2 = np.array([math.atan((b-a)[0]/ (b-a)[1]), math.atan((c-b)[0]/ (c-b)[1]), math.atan((a-c)[0]/ (a-c)[1])])
                        # print(np.sum(np.abs(angles1- angles2)))
                        if np.sum(np.abs(angles1- angles2)) < 0.5:
                            # print(tri2)
                            triRank.remove(tri2)
        for idx, tri in enumerate(triRank):
            for idx2, tri2 in enumerate(triRank[idx+1:]):
                if tri[:2] == tri2[:2]:
                    triRank.remove(tri2)
                    if len(triRank) == 5:
                        break

                elif tri[1:] == tri2[1:]:
                    triRank.remove(tri2)
                    if len(triRank) == 5:
                        break
                elif tri[0] == tri2[0] and tri[2] == tri[2]:
                    triRank.remove(tri2)
                    if len(triRank) == 5:
                        break
        count+=1
    if len(triRank) > 5:
        print("too many tris")
        continue
    if DEBUG:
        print(triRank)

    # print(triRank)

    if len(triRank) == 0:
        print("No tris")
        continue
    shape = triRank[0]
    a = corners[shape[0]]
    b = corners[shape[1]]
    c = corners[shape[2]]
    smallTriArea = graph.triArea(a,b,c)
    # print(shape)
    # print(smallTriArea)

    goodQuads = []
    for shape in quads:
        a = corners[shape[0]]
        b = corners[shape[1]]
        c = corners[shape[2]]
        d = corners[shape[3]]
        x = np.array([a[1], b[1], c[1], d[1]])
        y = np.array([a[0], b[0], c[0], d[0]])
        area = graph.PolyArea(x,y)
        # print(shape)
        # print(area)
        if abs(area - smallTriArea*2) < 2000:
            # print(shape)
            if len(goodQuads) == 0:
                goodQuads.append(shape)
            else:
                unique = True
                for x in goodQuads:
                    if set(shape) == set(x):
                        unique = False
                if unique:
                    goodQuads.append(shape)
    # print(goodQuads)
    quads = goodQuads
    print(quads)

    if len(quads) == 1:



    corners[:,0] = corners[:,0] - np.min(corners[:,0]) + 10
    corners[:,1] =corners[:,1] - np.min(corners[:,1]) +10 
    
    # style = {"fill": "white", "stroke": "black", "stroke-width": "0"}
# 
    # for index, corner in enumerate(corners):
    #     dwg.add(dwg.text(str(index), (corner[1], corner[0])))



    def straighten(shape):
        

        for index, vertex in enumerate(shape):
            if index != len(shape)-1:
                o_vertex = shape[index+1]
            else:
                o_vertex = shape[0] 
            x1, y1 = corners[vertex]
            x2, y2 = corners[o_vertex]
            if abs(y1- y2) < 10:
                y2 = y1
                corners[o_vertex][1] = y1
            if abs(x1- x2) < 10:
                x2 = x1
                corners[o_vertex][0] = x1


    def normalizeTri(shape, index):

    # /    print(smallTriCount)
        smallTri = False
        medTri = False
        largeTri = False
        if index <2:
            smallTri =True
            hypot = triBase
            sides = sqLength
            height = triHeight
        elif index == 2:
            medTri = True
            hypot = 2 * sqLength
            sides = triBase
            height = sqLength
        else:
            largeTri = True
            hypot = math.sqrt((2*sqLength)**2 + (2*sqLength)**2)
            sides = 2 * sqLength
            height = triBase



        a = copy.copy(corners[shape[0]])
        b = copy.copy(corners[shape[1]])
        c = copy.copy(corners[shape[2]])
        
        normalized = [a,b,c]
        maxDist= 0
        for vertindex,vertex in enumerate(normalized):
            if vertindex == 2:
                f_vertex = normalized[0]
            else:
                f_vertex = normalized[vertindex +1]
            if math.dist(vertex, f_vertex) > maxDist:
                maxDist = math.dist(vertex, f_vertex)
                centerVertex = vertindex
        vertex = normalized[centerVertex]
        if centerVertex == 1:
            f_vertex = normalized[2]
            b_vertex = normalized[0]
        elif centerVertex ==0:
            f_vertex = normalized[1]
            b_vertex = normalized[2]  
        elif centerVertex ==2:
            f_vertex = normalized[0]
            b_vertex = normalized[1]   

        y1, x1 = vertex
        y2, x2 = f_vertex
        if abs(y1- y2) < 20:
            y2 = y1
            x2 = x1 + math.copysign(hypot,x2-x1)
            f_vertex[0] = y2
            f_vertex[1] = x2
        elif abs(x1- x2) < 20:
            x2 = x1
            y2 = y1 + math.copysign(hypot,y2-y1)
            f_vertex[0] = y2
            f_vertex[1] = x2
        else:
            x2 = x1 + math.copysign(sides,x2-x1)
            y2 = y1 + math.copysign(sides,y2-y1)
            f_vertex[0] = y2
            f_vertex[1] = x2

        y1, x1 = vertex
        y2, x2 = b_vertex
        if abs(y1- y2) < 20:
            y2 = y1
            x2 = x1 + math.copysign(sides,x2-x1)
            b_vertex[0] = y2
            b_vertex[1] = x2
        elif abs(x1- x2) < 20:
            x2 = x1
            y2 = y1 + math.copysign(sides,y2-y1)
            b_vertex[0] = y2
            b_vertex[1] = x2
        else:
            x2 = x1 + math.copysign(hypot/2,x2-x1)
            y2 = y1 + math.copysign(height,y2-y1)
            b_vertex[0] = y2
            b_vertex[1] = x2

        shapeDict['Tri' + str(index)] = {}
        shapeDict['Tri' + str(index)]['vertices'] = shape
        shapeDict['Tri' + str(index)]['data'] = normalized



    def normalizeParallelagram(shape):
        # print("norm para")
        horiz = True
        ready = False

        for index, vertex in enumerate(shape):

            if index != len(shape)-1:
                o_vertex = shape[index+1]
            else:
                o_vertex = shape[0] 
            y1,x1 = corners[vertex]
            y2, x2 = corners[o_vertex]
            # print(corners[vertex])
            if abs(y1- y2) < 10:
                horiz=True
                break
            if abs(x1- x2) < 10:
                horiz=False
                break
        

        a = copy.deepcopy(corners[shape[0]])
        b = copy.deepcopy(corners[shape[1]])
        c = copy.deepcopy(corners[shape[2]])
        d = copy.deepcopy(corners[shape[3]])
        normalized = [a,b,c,d]
        for index, vertex in enumerate(normalized):
            if index != 0:
                b_vertex = normalized[index-1]
            else:
                b_vertex = normalized[3]
            if index != 3:
                o_vertex = normalized[index+1]
            else:
                break

            y1, x1 = vertex
            y2, x2 = o_vertex

            if index == 0:
                longSide = math.dist(vertex, o_vertex) > math.dist(vertex, b_vertex)
                longSideFlat = True
                if longSide:
                    if abs(y1- y2) < 10:
                        longSideFlat = True
                    elif abs(x1- x2) < 10:
                        longSideFlat = True
                    else:
                        longSideFlat = False
                else:
                    if abs(y1- y2) < 10:
                        longSideFlat = False
                    elif abs(x1- x2) < 10:
                        longSideFlat = False
                    else:
                        longSideFlat = True
            else:
                longSide = not longSide


            y1, x1 = vertex
            y2, x2 = o_vertex


            if horiz and longSideFlat: 
                if longSide:
                    x2 = x1 + math.copysign(triBase,x2-x1)
                    o_vertex[1] = x2
                    o_vertex[0] = y1
                else:
                    y2 = y1 + math.copysign(triHeight,y2-y1)
                    x2 = x1 + math.copysign(triBase/2,x2-x1)
                    o_vertex[1] = x2
                    o_vertex[0] = y2
            elif horiz and not longSideFlat:
                if longSide:
                    y2 = y1 + math.copysign(sqLength,y2-y1)
                    x2 = x1 + math.copysign(sqLength,x2-x1)
                    o_vertex[1] = x2
                    o_vertex[0] = y2
                else:
                    x2 = x1 + math.copysign(sqLength,x2-x1)
                    o_vertex[1] = x2
                    o_vertex[0] = y1
            elif not horiz and longSideFlat:
                if longSide:
                    y2 = y1 + math.copysign(triBase,y2-y1)
                    o_vertex[1] = x1
                    o_vertex[0] = y2
                else:
                    y2 = y1 + math.copysign(triBase/2,y2-y1)
                    x2 = x1 + math.copysign(triHeight,x2-x1)
                    o_vertex[1] = x2
                    o_vertex[0] = y2
            elif not horiz and not longSideFlat:
                if longSide:
                    y2 = y1 + math.copysign(sqLength,y2-y1)
                    x2 = x1 + math.copysign(sqLength,x2-x1)
                    o_vertex[1] = x2
                    o_vertex[0] = y2
                else:
                    y2 = y1 + math.copysign(sqLength,y2-y1)
                    o_vertex[1] = x1
                    o_vertex[0] = y2

        shapeDict['para'] = {}
        shapeDict['para']['vertices'] = shape
        shapeDict['para']['data'] = normalized


    def testForSquare(shape):
        # get after straightened

            a = copy.copy(corners[shape[0]])
            b = copy.copy(corners[shape[1]])
            c = copy.copy(corners[shape[2]])
            d = copy.copy(corners[shape[3]])



            normalized = [a,b,c,d]
            offDist = 0
            angle1 = graph.printAngle(a,b,c)
            angle2 = graph.printAngle(b,c,d)

            # if DEBUG:
            #     print(angle1)
            #     print(angle2)





            # Normalizing the square
            # print(offDist)
            # print(angles)
            for angle in angle1:
                if abs(angle-90) <12:
                    for ang in angle2:
                        if abs(ang-90) <12:
                            if DEBUG:
                                print("SQUARE")
                                print(shape)
                            # print("SQUARE")
                            canonLength = math.dist(a,b)
                            #straight sqaure
                            
                            for idx, vertex in enumerate(normalized):
                                if idx == 3:
                                    break
                                f_vertex = normalized[idx+1]

                                triSides = math.sqrt(canonLength**2 + canonLength**2) / 2

                                y1, x1 = vertex
                                y2, x2 = f_vertex
                                if abs(y1- y2) < 20:
                                    y2 = y1
                                    x2 = x1 + math.copysign(canonLength,x2-x1)
                                    f_vertex[0] = y2
                                    f_vertex[1] = x2
                                elif abs(x1- x2) < 20:
                                    x2 = x1
                                    y2 = y1 + math.copysign(canonLength,y2-y1)
                                    f_vertex[0] = y2
                                    f_vertex[1] = x2
                                else:
                                    x2 = x1 + math.copysign(triSides,x2-x1)
                                    y2 = y1 + math.copysign(triSides,y2-y1)
                                    f_vertex[0] = y2
                                    f_vertex[1] = x2


                            shapeDict['square'] = {}
                            shapeDict['square']['vertices'] = shape
                            shapeDict['square']['data'] = normalized
                            return True, canonLength
            return False, 0
    corners = corners.astype(np.float)

    shapeDict = {}
    # print(quads)
    for index, shape in enumerate(quads):

            straighten(shape)
            test, testLength = testForSquare(shape)
            if test:
                sqLength = testLength


    triBase = math.sqrt(sqLength**2 + sqLength**2)
    triHeight = math.sqrt(sqLength**2 - (triBase/2)**2)
    smallTriCount = 0
    if "square" not in shapeDict:
        print("can't identify square")
        continue
    for index, shape in enumerate(quads):
        if shape != shapeDict['square']['vertices']:
            normalizeParallelagram(shape)
            
    # print(shapeDict)




    for index,shape in enumerate(triRank):
        normalizeTri(shape,index)  
                    

    def checkForLock(shape):
        for index, vertex in enumerate(shape['vertices']):
            if vertex in locked_vertices:
                return vertex, shape['data'][index]
        return -1, -1

    # # stitching
    locked_vertices = {}
    shapeDict['square']['vertices']
    for index, vertex in enumerate(shapeDict['square']['vertices']):
        locked_vertices[vertex] = shapeDict['square']['data'][index]

    if DEBUG:
        print(shapeDict)


    # Locking Function
    count = 0
    while count<10:
        
        for key, value in shapeDict.items():
            if key != "square":
                vertex, data = checkForLock(value)
                if vertex != -1:
                    transform = data - locked_vertices[vertex]
                    # print(transform)
                    for index, point in enumerate(value['data']):
                        point = point - transform
                        value['data'][index] = point
                    for pointIndex, vertex in enumerate(value['vertices']):
                        if vertex not in locked_vertices:
                            locked_vertices[vertex] = value['data'][pointIndex]
            
        count+=1
        # break
                # moveToPosition()

    minX =100000
    minY= 100000
    maxX= 0
    maxY = 0
    for key, value in shapeDict.items():
        for point in value['data']:
            if point[0] < minY:
                minY = point[0]
            if point[0] > maxY:
                maxY = point[0]

            if point[1] < minX:
                minX = point[1]
            if point[1] > maxX:
                maxX = point[1]
    print(minY)

    svgWidth = maxX - minX
    svgHeight = maxY - minY 
    for key, value in shapeDict.items():
        for point in value['data']:
            point[0] -= minY
            point[1] -= minX

    


    dwg = svgwrite.Drawing(FOLDER + "/"+ filename.replace("jpg", "svg"), (svgWidth, svgHeight), debug=True)
    colors = ["red", "green", "blue", "yellow", "purple", "pink", "orange"]





    shapeCount = 0

    if not DEBUG:
        for key, value in shapeDict.items():
                    points = value['data']
                    # style["fill"] = colors[shapeCount]
                    points = np.flip(np.array(points).astype(np.float), axis=1)
                    # print(style)
                    polygon = dwg.polygon(points, **style, id=str(shapeCount+1))
                    dwg.add(polygon)
                    lastShape = shape
                    shapeCount+=1

        dwg.save()
    fileidx += 1
# # dwg = svgwrite.Drawing("Test.svg", (svgWidth, svgHeight), debug=True)












# # for key, value in shapeDict.items():
# #         points = value['data']
# #         # points = []
# #         # points.append(corners[shape[0]])
# #         # points.append(corners[shape[1]])
# #         # points.append(corners[shape[2]])
# #         # points.append(corners[shape[3]])
# #         style["fill"] = colors[shapeCount]
# #         points = np.flip(np.array(points).astype(np.float), axis=1)
# #         polygon = dwg.polygon(points, **style)
# #         dwg.add(polygon)
# #         lastShape = shape
# #         shapeCount+=1


# # # # dwg.add(polygon)
# dwg.save()


# # cv.imwrite("test.png", img)
# # plt.imshow(gray)
# # plt.show()