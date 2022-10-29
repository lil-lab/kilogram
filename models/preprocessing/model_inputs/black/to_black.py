from os import listdir
from os.path import isfile, join

mypath = "./tangrams-svg"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for file in onlyfiles:
  if file.startswith('page'):

    f = open(join(mypath, file),'r').read().replace("\n"," ")
    f = f.replace('fill="lightgray"','fill="black"')
    # f = f.replace('stroke="white" strokewidth="1"','stroke="black" strokewidth="2"')
    # f = f.replace('stroke="white" strokewidth="1"','stroke="black" strokewidth="2"')
    with open("./square-black-border/"+file, 'w') as new_f:
      new_f.write(f)
