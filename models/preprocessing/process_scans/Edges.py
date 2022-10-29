import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import random
import graph
import math
import PIL
from tqdm import tqdm

def testForBlack(image, windowSize, location, EDGETESTPARAM):
        x = location[1]
        y = location[0]
        window = image[y - windowSize:y+ windowSize+1,x - windowSize:x+ windowSize+1]
        # print(window)
        if np.sum(window) < EDGETESTPARAM:
            return False
        else:
            return True




def findEdges(corners, ref, window, edgeiter, EDGETESTPARAM):
    edges = {}
    for index, corner in enumerate(corners):
        # dwg.add(dwg.text(str(index), (corner[1], corner[0])))
        testCorner = corner
        for otherIndex, other in enumerate(corners):
            if otherIndex != index:
                vector = other - testCorner
                connected =True

                for x in range(edgeiter):
                    # print(x)
                    if not testForBlack(ref, window, (random.uniform(0.1,0.9) * vector + testCorner).astype(np.int), EDGETESTPARAM):
                        connected = False
                        break
                if connected:
                    if index in edges:
                        edges[index].append(otherIndex )
                    else:
                        edges[index] = []
                        edges[index].append(otherIndex)
    return edges

def getShapes(edges, corners):
    def cmp_to_key(mycmp):
        'Convert a cmp= function into a key= function'
        class K:
            def __init__(self, obj, *args):
                self.obj = obj
            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0
            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0
            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0
            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0
            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0
            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0
        return K

    def area_compare(x, y):
        a = corners[x[0]]
        b = corners[x[1]]
        c = corners[x[2]]

        d = corners[y[0]]
        e = corners[y[1]]
        f = corners[y[2]]
        return graph.triArea(a,b,c) - graph.triArea(d,e,f)


    tris = set()
    quads = set()
    for index, data in edges.items():
        for connection in data:
            if connection in edges:
                for backlink in edges[connection]:
                    if backlink in data:
                        tris.add(tuple(sorted((backlink, index, connection ))))
                    elif backlink != index:
                        if backlink in edges:
                            for doubleBackLink in edges[backlink]:
                                if doubleBackLink not in edges[connection] and doubleBackLink != connection and doubleBackLink != index:
                                    if doubleBackLink in data:
                                        quads.add(tuple(( index, connection, backlink, doubleBackLink)))

    triRank = []
    lines= []
    if len(tris) > 50:
        # print("TOO MANY TRIS")
        return False, False, False
    for index, shape in enumerate(tris):

            a = corners[shape[0]]
            b = corners[shape[1]]
            c = corners[shape[2]]

            angles = graph.printAngle(a,b,c)
            # print(shape)
            # print(graph.triArea(a,b,c))
            if max(angles) < 100 and graph.triArea(a,b,c) > 3000:
                triRank.append(shape)
            else:
                lines.append(shape)

            triRank = sorted(triRank, key=cmp_to_key(area_compare)) 
    # print(triRank)
    pointsUsed = []
    while len(triRank) > 5:
        # print("removing triangles")
        removed = False
        for idx, tri in enumerate(triRank):
            for otri in triRank[idx +1:]:
                # print(otri)
                tri = set(tri)
                otri = set(otri)
                intersect = tri.intersection(otri)
                if len(intersect) == 2:
                    diff = set()
                    diff = diff.union(tri.difference(otri))
                    diff = tuple(diff.union(otri.difference(tri)))
                    if math.dist(corners[diff[0]], corners[diff[1]]) < 50:
                        triRank.remove(tuple(sorted(tuple(otri))))
                        removed = True
                        # break
                    point = diff[1]
                    for itri in triRank[idx+2:]:
                        itri = set(itri)
                        if itri != otri:
                            test = itri.intersection(intersect)
                            test2 = itri.intersection(diff)
                            test = test.union(test2)
                            if len(test) == 3:
                                # print("new removal")
                                triRank.remove(tuple(sorted(tuple(itri))))
                                removed = True
                if removed:
                    break
            if removed:
                break
        break
    # print(triRank)
    while len(triRank) > 5:
        # print("removing triangles size") 

        if area_compare(triRank[5], triRank[4])> 4000:
            triRank.remove(triRank[5])
        else:
            break
    # print(len(triRank))

    if len(triRank) > 5:
        for tri in reversed(triRank):
            # print(tri)
            trilines = [(tri[0], tri[1]), (tri[1], tri[2]), (tri[0], tri[2])]
            for tri2 in triRank:
                if tri2 != tri:
                    closePts = 0
                    for point in tri2:
                        minDist = 100000000
                        for line in trilines:
                            a = math.dist(corners[line[0]], corners[line[1]])
                            b = math.dist(corners[line[0]], corners[point])
                            c = math.dist(corners[line[1]], corners[point])
                            d = (a**2 + b**2 - c**2)/(2*a)
                            vec = corners[line[1]] - corners[line[0]]
                            newpt = corners[line[0]] + (d/a * vec)
                            dist = math.dist(newpt, corners[point])
                            if dist < minDist:
                                minDist = dist
                        if minDist < 10:
                            closePts+= 1
                    if closePts == 3:
                        # print(tri)
                        # print(tri2)
                        triRank.remove(tri)
                        break
            if len(triRank) == 5:
                break
                        # print(minDist)




    # print(triRank)
    if len(triRank) ==0 :
        return False, False, False

    shape = triRank[0]
    a = corners[shape[0]]
    b = corners[shape[1]]
    c = corners[shape[2]]
    smallTriArea = graph.triArea(a,b,c)


    # print("Quads before filtering...")
    # print(quads)
    # print(lines)
    goodQuads = []
    for shape in quads:
        a = corners[shape[0]]
        b = corners[shape[1]]
        c = corners[shape[2]]
        d = corners[shape[3]]
        x = np.array([a[1], b[1], c[1], d[1]])
        y = np.array([a[0], b[0], c[0], d[0]])
        area = graph.PolyArea(x,y)
        inline = False
        for line in lines:
            inline = True
            for vertex in line:
                if vertex not in list(shape):
                    inline = False
        

        if not inline and abs(area - smallTriArea*2) < 4000:
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
    return triRank, quads, lines
