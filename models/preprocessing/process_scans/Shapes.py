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



def straighten(shape, corners):
        

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


def normalizeTri(shape, index, geom, corners):

        triBase = geom['triBase']
        triHeight = geom['triHeight']
        sqLength = geom['sqLength']

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



        a = copy.copy(corners[shape[0]]).astype(np.float)
        b = copy.copy(corners[shape[1]]).astype(np.float)
        c = copy.copy(corners[shape[2]]).astype(np.float)
        
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
        
        tri =  {}
        tri['vertices'] = shape
        tri['data'] = normalized
        return tri




def normalizeParallelagram(shape, geom, corners):

        triBase = geom['triBase']
        triHeight = geom['triHeight']
        sqLength = geom['sqLength']


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
        

        a = copy.deepcopy(corners[shape[0]]).astype(np.float)
        b = copy.deepcopy(corners[shape[1]]).astype(np.float)
        c = copy.deepcopy(corners[shape[2]]).astype(np.float)
        d = copy.deepcopy(corners[shape[3]]).astype(np.float)
        normalized = [a,b,c,d]

        for index, vertex in enumerate(normalized):
            if index != 0:
                b_vertex = normalized[index-1]
            else:
                b_vertex = normalized[3]
            if index != 3:
                o_vertex = normalized[index+1]
            else:
                o_vertex = normalized[0]
                # break

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
                    print(o_vertex[1])
                else:
                    x2 = x1 + math.copysign(sqLength,x2-x1)
                    o_vertex[1] = x2
                    o_vertex[0] = y1
            elif not horiz and longSideFlat:
                if longSide:
                    y2 = y1 + math.copysign(triBase,y2-y1)
                    o_vertex[1] = x1
                    o_vertex[0] = y2
                    print(o_vertex[1])
                    
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
        para = {}

        para['vertices'] = shape
        para['data'] = normalized

        return para


def testForSquare(shape, corners, DEBUG):
        # get after straightened

            a = copy.copy(corners[shape[0]]).astype(np.float)
            b = copy.copy(corners[shape[1]]).astype(np.float)
            c = copy.copy(corners[shape[2]]).astype(np.float)
            d = copy.copy(corners[shape[3]]).astype(np.float)



            normalized = [a,b,c,d]
            offDist = 0
            angle1 = graph.printAngle(a,b,c)
            angle2 = graph.printAngle(b,c,d)
            if DEBUG:
                print("Square Test Angles")
                print(angle1)
                print(angle2)


            for angle in angle1:
                if abs(angle-90) <10:
                    for ang in angle2:
                        if abs(ang-90) <12:

                            # print("SQUARE")
                            canonLength = math.dist(a,b)
                            #straight sqaure
                            
                            for idx, vertex in enumerate(normalized):
                                if idx == 3:
                                    f_vertex = normalized[0]
                                else:
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

                            square = {}
                            # shapeDict['square'] = {}
                            square['vertices'] = shape
                            square['data'] = normalized
                            print(square)
                            return True, canonLength, square
            return False, 0, {}