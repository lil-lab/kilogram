import os
folder = "matchup/fail-w-svg/"

from bs4 import BeautifulSoup



for  idx, filename in enumerate(sorted(os.listdir(folder))):
    if ".svg" not in filename:
        continue


    file = folder + filename
    x = open(file).read()

    soup = BeautifulSoup(x, 'xml')
    svg = soup.find("svg")
    width = svg['width']
    height = svg['height']


    polys = soup.find_all("polygon")
    minX = 100000
    minY = 100000
    maxX = 0
    maxY = 0
    for poly in polys:
        # print(poly['points'])
        points=  poly['points']
        xs = [float(x.split(",")[0]) for x in points.split()]
        ys = [float(x.split(",")[1]) for x in points.split()]
        for y in ys:
            if y < minY:
                minY = y
            if y > maxY:
                maxY = y
        for x in xs:
            if x < minX:
                minX = x
            if x > maxX:
                maxX = x
    # print(minX)
    # print(minY)
    if minX == 0 and minY == 0:
        print("doing this")
        svg['width'] = str(maxX)
        svg['height'] = str(maxY)
        svg['viewBox'] = "0 0 " + svg['width'] + " " + svg['height']
    else:
        for poly in polys:
            points=  poly['points']
            xs = [float(x.split(",")[0]) - minX for x in points.split()]
            ys = [float(x.split(",")[1]) - minY for x in points.split()]
            ptsString = ""
            for i in range(len(xs)):
                ptsString += str(xs[i]) + "," + str(ys[i]) + " "
            poly['points'] = ptsString
        maxX = maxX - minX
        maxY = maxY - minY
        svg['width'] = str(maxX)
        svg['height'] = str(maxY)
        svg['viewBox'] = "0 0 " + svg['width'] + " " + svg['height']
       


# # print(x)
    svg['width'] = "100%"
    svg['height'] = "100%"

    with open(file, "w") as file1:
        file1.write(str(soup))

    # shapecount = 0
    # for idx2, shape in enumerate(data):
    #     if "polygon" not in shape:
    #         continue
    #     print(shape)
    # newData = "><".join(data)
    # print(newData)
    # f = open(folder + "fixed/" +filename, "w")
    # f.write(newData)
    # f.close()
# print(idx)