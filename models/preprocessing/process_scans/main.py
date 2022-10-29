def warn(*args, **kwargs): pass
import warnings; warnings.warn = warn
import os
from argparse import ArgumentParser
import Corners 
import Edges 
import Shapes 
import SVG
import math 

parser = ArgumentParser()

parser.add_argument("--debug", dest = "debug",
    required = True, help = "debug 1 for true 0 for false")

parser.add_argument("--folder", dest = "folder",
    required = True, help = "path to cropped files")

parser.add_argument("--file", dest = "file",
    required = False, help = "path to cropped files")

args = parser.parse_args()

DEBUG = int(args.debug)
FOLDER = args.folder
HARRIS_THRESHOLD = 0.2
EDGETESTPARAM = 800
EDGEWINDOW =7
EDGESAMPLES = 100
HARRIS_SIZE = 35
print(args.file)

for  filename in sorted(os.listdir(FOLDER)):
    if args.file != None:
        if filename != args.file:
            continue
    if ".jpg" not in filename:
        continue

    file = FOLDER + "/" +filename
    print(file)
    corners, gray = Corners.findCorners(file, HARRIS_THRESHOLD, HARRIS_SIZE, DEBUG)
    if isinstance(corners, bool):
        print("Image too small")
        continue
    
    height, width = gray.shape[:2]

    if DEBUG:
    	SVG.writeDebug( file, corners, width, height)

    edges = Edges.findEdges(corners, gray, EDGEWINDOW, EDGESAMPLES, EDGETESTPARAM)
    if DEBUG:
        print("EDGES:")
        print(edges)
    tris, quads, lines = Edges.getShapes(edges, corners)
    if not tris:
        print("Nothing Found")
        continue


    if DEBUG:
        print("Lines")
        print(lines)
        print("TRIS")
        print(tris)
        print(quads)
        print("+++++++++++++++++++++++++++++++++=")
        print("+++++++++++++++++++++++++++++++++=")

    shapeDict = {}
    for index, shape in enumerate(quads):
        Shapes.straighten(shape, corners)
        test, testLength, square = Shapes.testForSquare(shape, corners, DEBUG)
        if test:
            shapeDict['square'] = square
            sqLength = testLength

    if "square" not in shapeDict:
        print("can't identify square")
        continue

    triBase = math.sqrt(sqLength**2 + sqLength**2)
    triHeight = math.sqrt(sqLength**2 - (triBase/2)**2)
    smallTriCount = 0

    geom = {}
    geom['triBase'] = triBase
    geom['triHeight'] = triHeight
    geom['sqLength'] = sqLength

    

    for index, shape in enumerate(quads):
        if shape != shapeDict['square']['vertices']:
            para = Shapes.normalizeParallelagram(shape, geom, corners)
            shapeDict['para'] = para
    print(shapeDict)
    for index,shape in enumerate(tris):
        normTri = Shapes.normalizeTri(shape,index, geom, corners) 
        shapeDict['tri' + str(index)] = normTri

    if DEBUG:
        print(shapeDict)

    shapeDict = SVG.connectTangram(shapeDict, DEBUG, lines)
    # print(shapeDict)
    shapeDict, dwg = SVG.cropToTangram(shapeDict,filename,  DEBUG)

    if not DEBUG:
        SVG.drawShape(shapeDict, dwg)
        # os.remove(file)