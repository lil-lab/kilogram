import os
folder = "bookscans/finished/"
for  idx, filename in enumerate(sorted(os.listdir(folder))):
    if ".svg" not in filename:
        continue
    file = folder + filename
    x = open(file).read()

    # print(x)
    x = x.replace('stroke="black" stroke-width="2"', '')
    x = x.replace('stroke="black"', '')

    data = x.split("><")

    print(data)


    colors = ["red", "green", "blue", "yellow", "purple", "pink", "orange"]
    data = [line for line in data if "text" not in line]
    shapecount = 0
    for idx2, shape in enumerate(data):
        if "polygon" not in shape:
            continue
        shape = shape.replace('fill="'+colors[shapecount] + '"', 'fill="lightgray"' )
        shape = shape.replace('fill-opacity="0.4"', '')
        shape = shape.replace('fill-opacity = "0.4"', '')

        data[idx2] = shape.replace('/', 'stroke = "white" strokewidth = "1" /')
        shapecount += 1
        if shapecount == len(colors):
            shapecount = 0
    newData = "><".join(data)
    print(newData)
    f = open(folder + "fixed/" +filename, "w")
    f.write(newData)
    f.close()
print(idx)