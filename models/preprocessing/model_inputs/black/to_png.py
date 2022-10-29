import os
from os import listdir
from os.path import isfile, join
import json

dataset="heldout"
mypath= './square-black-border'
save_path='../../fine-tuning/data/images-border/border-'+dataset+'/'

with open('../dense_final3.json') as f:
    data = json.load(f)

with open('../data_split.json') as f:
    split = json.load(f)


k=0
for file in split[dataset]:
  svg_file=join(mypath, file+'.svg')
  png_file=join(save_path, file+'.png')

  os.system("convert "+svg_file+" -resize 224x224 "+png_file)
  k+=1
  print(k)

