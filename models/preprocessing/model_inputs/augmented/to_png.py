import os
from os import listdir
from os.path import isfile, join

# dataset="val"
mypath= "./dev/dev_images/new_dev_powerset_svg/"
save_path="./dev/dev_images/new_dev_powerset_png"
k=0
for file in listdir(mypath):
  svg_file=join(mypath, file)
  if isfile(svg_file):
      if file.startswith('page'):
        png_file = join(save_path,file.replace('svg','png'))
        os.system("convert "+svg_file+" -resize 224x224 "+png_file)
        # os.system("convert "+svg_file+" "+png_file)
        k+=1
        print(k)


#train
#files: 692
#svgs: 128949
#with 0 parts
#files: 692
#svgs: 135638

#val       
#files: 240
#svgs: 3558
#eval_svgs: 3798
#with 0 parts
#files: 240
#svgs: 3798

#dev       
#files: 125
#svgs: 23618
