import os
from os import listdir
from os.path import isfile, join

dataset="heldout"
mypath= "./border-colored-svg/"+dataset
save_path='../../../fine-tuning/data/heldout/images/color' #"./border-colored-png/"+dataset
k=0
for file in listdir(mypath):
  svg_file=join(mypath, file)
  if isfile(svg_file):
    if file.startswith('page') and file.endswith('.svg'):
      png_file = join(save_path,file.replace('svg','png'))
      os.system("convert "+svg_file+" -resize 224x224 "+png_file)
      # os.system("convert "+svg_file+" "+png_file)
      k+=1
      print(k)



