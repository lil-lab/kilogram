from collections import defaultdict
import numpy as np
import math
class cropGraph:
 
    # init function to declare class variables
    def __init__(self, V):
        self.V = V
        self.adj = [[] for i in range(V)]
 
    def DFSUtil(self, temp, v, visited):
 
        # Mark the current vertex as visited
        visited[v] = True
 
        # Store the vertex to list
        temp.append(v)
 
        # Repeat for all vertices adjacent
        # to this vertex v
        for i in self.adj[v]:
            if visited[i] == False:
 
                # Update the list
                temp = self.DFSUtil(temp, i, visited)
        return temp
 
    # method to add an undirected edge
    def addEdge(self, v, w):
        self.adj[v].append(w)
        self.adj[w].append(v)
 
    # Method to retrieve connected components
    # in an undirected graph
    def connectedComponents(self):
        visited = []
        cc = []
        for i in range(self.V):
            visited.append(False)
        for v in range(self.V):
            if visited[v] == False:
                temp = []
                cc.append(self.DFSUtil(temp, v, visited))
        return cc

class Graph:
 
    # Constructor
    def __init__(self,corners ):
 
        # default dictionary to store graph
        self.graph = defaultdict(list)
        self.level = []
        self.breadth =[]
        self.corners = corners
 
    # function to add an edge to graph
    def add_edge(self, u, v):
        self.graph[u].append(v)

    def hasEdge(self, u, v):
        # print(u)
        # print(v)
        # print(self.graph[u])
        if v in self.graph[u]:
            return True
        else:
            return False
    # A function used by DFS
    def DFSUtil(self, v, visited):
 
        # Mark the current node as visited
        # and print it
        visited.add(v)
        
        # Recur for all the vertices
        # adjacent to this vertex
        for neighbour in self.graph[v]:
            if neighbour not in visited:
                self.tiers.append(tier)
                self.DFSUtil(neighbour, visited)
        
            # else:
                # print("possible shape")
 
    # The function to do DFS traversal. It uses
    # recursive DFSUtil()
    def DFS(self, v):
 
        # Create a set to store visited vertices
        visited = set()
 
        # Call the recursive helper function
        # to print DFS traversal
        self.DFSUtil(v, visited)

    def BFS(self, s):
 
        # Mark all the vertices as not visited
        visited = [False] * (max(self.graph) + 1)
        self.level = [0] * (max(self.graph) + 1)
 
        # Create a queue for BFS
        queue = []
        self.level[s] = 0
        # Mark the source node as 
        # visited and enqueue it
        queue.append(s)
        visited[s] = True
 
        while queue:
 
            # Dequeue a vertex from 
            # queue and print it
            s = queue.pop(0)
            self.breadth.append(s)
 
            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            for i in self.graph[s]:
                if visited[i] == False:
                    self.level[i] = self.level[s] + 1
                    queue.append(i)
                    visited[i] = True


    def shapeSearch(self):
        # print(self.level)
        # print(self.graph)
        self.level = np.array(self.level)
        levels = np.max(np.array(self.level))
        # print(order)
        # print(self.graph[5])
        triangles = []
        quads = []
        # Triangles
        for tier in range(levels+1):
            tierPoints = np.ravel(np.argwhere(self.level == tier))
            for index, vertex in enumerate(tierPoints):
                for otherVertex in tierPoints[index+1:]:
                    if vertex != otherVertex:
                        if self.hasEdge(vertex, otherVertex):
                            if tier > 0:
                                tierPointsAbove = np.ravel(np.argwhere(self.level == tier -1))
                                for testPointAbove in tierPointsAbove:
                                    if self.hasEdge(vertex, testPointAbove) and self.hasEdge(otherVertex, testPointAbove):
                                        triangles.append((vertex, otherVertex, testPointAbove))
                            if tier < levels:
                                tierPointsBelow = np.ravel(np.argwhere(self.level == tier +1))
                                for testPointBelow in tierPointsBelow:
                                    if self.hasEdge(vertex, testPointBelow) and self.hasEdge(otherVertex, testPointBelow):
                                        triangles.append((vertex, otherVertex, testPointBelow))
                    else:
                        break
        # Quadrilaterals
        for tier in range(levels+1):
            tierPoints = np.ravel(np.argwhere(self.level == tier))
            for index, vertex in enumerate(tierPoints):
                for otherVertex in tierPoints[index+1:]:
                    if vertex != otherVertex:
                        if self.hasEdge(vertex, otherVertex):
                            # comes in in a line
                            if tier < levels:
                                tierPointsBelow = np.ravel(np.argwhere(self.level == tier +1))
                                for testPointBelow1 in tierPointsBelow:
                                    if self.hasEdge(vertex, testPointBelow1) and not self.hasEdge(otherVertex,testPointBelow1):
                                            for testPointBelow2 in tierPointsBelow:
                                                if self.hasEdge(otherVertex, testPointBelow2) and not self.hasEdge(vertex, testPointBelow2):
                                                        if self.hasEdge(testPointBelow1, testPointBelow2):
                                                            quads.append((vertex, otherVertex, testPointBelow2, testPointBelow1))
                        else:
                            quadsForThese = []
                            if tier < levels and tier >0:
                                tierPointsBelow = np.ravel(np.argwhere(self.level == tier +1))
                                tierPointsAbove= np.ravel(np.argwhere(self.level == tier -1))
                                for testPointBelow1 in tierPointsBelow:
                                    if self.hasEdge(vertex, testPointBelow1) and self.hasEdge(otherVertex,testPointBelow1):
                                        for testPointAbove in tierPointsAbove:
                                            if self.hasEdge(vertex, testPointAbove) and self.hasEdge(otherVertex,testPointAbove):
                                                if not self.hasEdge(testPointAbove, testPointBelow1):
                                                    newquad = (vertex, testPointAbove, otherVertex, testPointBelow1)
                                                    if len(quads)==0:
                                                        quads.append(newquad)
                                                    else:
                                                        subbedIn = False
                                                        for quadIndex, possquad in enumerate(quads):
                                                            countSame = 0
                                                            for valIndex,val in enumerate(possquad):
                                                                if val == newquad[valIndex]:
                                                                    countSame += 1
                                                            if countSame == 3:
                                                                subbedIn = True
                                                                newPerim = perim(self.corners[newquad[0]], self.corners[newquad[1]], self.corners[newquad[2]], self.corners[newquad[3]])
                                                                oldPerim = perim(self.corners[possquad[0]], self.corners[possquad[1]], self.corners[possquad[2]], self.corners[possquad[3]])
                                                                if newPerim < oldPerim:
                                                                    quads[quadIndex] = newquad
                                                        if not subbedIn:
                                                            quads.append(newquad)
                    
        return triangles, quads

def lengthSquare(X, Y):  
    xDiff = X[0] - Y[0]  
    yDiff = X[1] - Y[1]  
    return xDiff * xDiff + yDiff * yDiff 


def printAngle(A, B, C):  
      
    # Square of lengths be a2, b2, c2  
    a2 = lengthSquare(B, C)  
    b2 = lengthSquare(A, C)  
    c2 = lengthSquare(A, B)  
  
    # length of sides be a, b, c  
    a = math.sqrt(a2);  
    b = math.sqrt(b2);  
    c = math.sqrt(c2);  
  
    # From Cosine law  
    alpha = math.acos(max( min((b2 + c2 - a2) / (2 * b * c), 1) , -1));  
    betta = math.acos(max( min((a2 + c2 - b2) / (2 * a * c), 1), -1));  
    gamma = math.acos(max( min((a2 + b2 - c2) / (2 * a * b), 1), -1));  
  
    # Converting to degree  
    alpha = alpha * 180 / math.pi;  
    betta = betta * 180 / math.pi;  
    gamma = gamma * 180 / math.pi;  
  
    return alpha, betta, gamma

def perim(a,b,c,d):
    return math.dist(a,b) + math.dist(b,c) + math.dist(c,d) + math.dist(d, a)
def triArea(a,b,c):
    x1, y1 = a
    x2, y2 = b
    x3, y3 = c

    l1 = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    l2 = math.sqrt((x2 - x3)**2 + (y2 - y3)**2)
    l3 = math.sqrt((x3 - x1)**2 + (y3 - y1)**2)

    p = (l1 + l2 + l3)/2
    if p * (p - l1) * (p - l2) * (p - l3) <= 0:
        return 0
    area = math.sqrt(p * (p - l1) * (p - l2) * (p - l3))

    return area

def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))