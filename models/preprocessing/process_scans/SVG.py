import svgwrite
from svgwrite.extensions.shapes import ngon, rotate, translate, scale
import numpy as np
import math

def writeDebug( filename, corners, width, height):
	dwg = svgwrite.Drawing(filename.replace("jpg", "svg"), (width + 50, height + 50), debug=True)
	# print(corners)
	for index, corner in enumerate(corners):
		dwg.add(dwg.text(str(index), (corner[1], corner[0])))
	dwg.save()

def connectTangram(shapeDict, DEBUG, lines):

	# print(shapeDict)

	def checkForPointLock(shape):
		for index, vertex in enumerate(shape['vertices']):
			if vertex in locked_vertices:
				return vertex, shape['data'][index]
		return -1, -1

	def checkForLineLock(shape, lineLock2):
		lockPoints = 0
		for index, vertex in enumerate(shape['vertices']):
			for line in locked_lines:
				if vertex in line:
					if lineLock2:
						lockPoints+= 1
						if lockPoints ==2:
							return index, vertex, line
						break
					else:
						return index, vertex, line
		return -1, -1, -1


	locked_vertices = {}
	locked_lines = set()
	shapeDict['square']['vertices']
	for index, vertex in enumerate(shapeDict['square']['vertices']):
		locked_vertices[vertex] = shapeDict['square']['data'][index]
		
	# print(locked_vertices)
	for line in lines:
		locked = 0
		for point in line:
			if point in locked_vertices:
				locked += 1
		if locked == 2:
			locked_lines.add(line)
	count = 0
	lineLock2 = False
	lockshapes = ['square']
	while count<100:
		lineLock2 = not lineLock2
		# check point locks
		checkLines = True
		for key, value in shapeDict.items():
			if key not in lockshapes:
				vertex, data = checkForPointLock(value)
				if vertex != -1:
					checkLines = False
					transform = data - locked_vertices[vertex]
					for index, point in enumerate(value['data']):
						point = point - transform
						value['data'][index] = point
					for pointIndex, vertex in enumerate(value['vertices']):
						if vertex not in locked_vertices:
							locked_vertices[vertex] = value['data'][pointIndex]
					for line in lines:
						locked = 0
						for point in line:
							if point in locked_vertices:
								locked += 1
						if locked == 2:
							locked_lines.add(line)
					lockshapes.append(key)
		if checkLines:
			# check line locks
			for key, value in shapeDict.items():
				if key not in lockshapes:
						idx, vertex, line = checkForLineLock(value, lineLock2)

						if vertex != -1:
							if DEBUG:
								print("line lock debug")
								print(key)
								print(vertex)
								print(line)
								print(lockshapes)
							refPoint = value['data'][idx]
							# print(refPoint)
							line = list(line)
							line.remove(vertex)
							transform = []
							# print(locked_vertices[line[0]])
							if locked_vertices[line[0]][0] - locked_vertices[line[1]][0]  == 0:
								transform = refPoint - [locked_vertices[line[0]][0], 0]
								transform[1] = 0
							elif locked_vertices[line[0]][1] - locked_vertices[line[1]][1]  == 0:
								transform = refPoint - [0,locked_vertices[line[0]][1]]
								transform[0] = 0 
							else:

								a = math.dist(locked_vertices[line[0]], locked_vertices[line[1]])
								b = math.dist(locked_vertices[line[0]], refPoint)
								c = math.dist(locked_vertices[line[1]], refPoint)
								d = (a**2 + b**2 - c**2)/(2*a)
								vec = locked_vertices[line[1]] - locked_vertices[line[0]]

								newpt = locked_vertices[line[0]] + (d/a * vec)
								transform = refPoint - newpt
							if len(transform) == 2:
								for index, point in enumerate(value['data']):
									point = point - transform
									value['data'][index] = point
								for pointIndex, vertex in enumerate(value['vertices']):
									if vertex not in locked_vertices:
										locked_vertices[vertex] = value['data'][pointIndex]
								for line in lines:
									locked = 0
									for point in line:
										if point in locked_vertices:
											locked += 1
									if locked == 2:
										locked_lines.add(line)
							lockshapes.append(key)
							break
		# foundThing = False
		# for key, value in shapeDict.items():
		# 	for index, vertex in enumerate(value['vertices']):
		# 		if index == len(value['vertices']) - 1:
		# 			overtex = value['vertices'][0]
		# 			oindex=0
		# 		else:
		# 			oindex = index+1
		# 			overtex = value['vertices'][index+1]
		# 		for line in lines:
		# 			for sqpoint in locked_vertices:
		# 				if vertex in line and overtex in line and sqpoint in line:
		# 					transform = []

		# 					if value['data'][index][0] - value['data'][oindex][0] == 0:
		# 						transform = locked_vertices[sqpoint] - value['data'][index]
		# 						transform[1] = 0
		# 					if value['data'][index][1] - value['data'][oindex][1] == 0:
		# 						transform = locked_vertices[sqpoint] - value['data'][index]
		# 						transform[0] = 0
		# 					if len(transform) == 2:
		# 						for idx, point in enumerate(value['data']):
		# 							point = point + transform
		# 							value['data'][idx] = point
		# 						for pointIndex, vertex in enumerate(value['vertices']):
		# 							if vertex not in locked_vertices:
		# 								locked_vertices[vertex] = value['data'][pointIndex]
		# 						for line in lines:
		# 							locked = 0
		# 							for point in line:
		# 								if point in locked_vertices:
		# 									locked += 1
		# 							if locked == 2:
		# 								locked_lines.add(line)
		# 						lockshapes.append(key)
		# 						foundThing = True
		# 					break
		# 			if foundThing:
		# 				break
		# 		if foundThing:
		# 			break
		# 	if foundThing:
		# 		break



			
		count+=1
	# print(shapeDict)
	return shapeDict 

def cropToTangram(shapeDict, file, DEBUG):
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
	svgWidth = maxX - minX
	svgHeight = maxY - minY 

	for key, value in shapeDict.items():
		for point in value['data']:
			point[0] -= minY
			point[1] -= minX
	dwg = svgwrite.Drawing("bookscans/testSVGS/" + file.replace("jpg", "svg"), (int(svgWidth), int(svgHeight)), debug=True)
	return shapeDict, dwg

def drawShape(shapeDict, dwg):
	colors = ["red", "green", "blue", "yellow", "purple", "pink", "orange"]
	shapeCount = 0
	
	for key, value in shapeDict.items():
		# print("csc")
		points = value['data']
		points = np.flip(np.array(points).astype(np.float), axis=1)
		style = {"fill": colors[shapeCount%7], "fill-opacity" : "0.4"}
		polygon = dwg.polygon(points, **style, id=str(shapeCount+1))
		dwg.add(polygon)
		shapeCount+=1
		# if shapeCount == len(colors):
			# shapeCount = 0
	if shapeCount == 7:
		dwg.save()