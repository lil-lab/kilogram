from os import listdir
from os.path import isfile, join
import re

mypath = "./border-colored-svg/heldout/"
savepath= "./border-colored-svg/heldout/"
pattern = r'viewBox="(.*?)"'

i=0
for file in listdir(mypath): 
  if isfile(join(mypath, file)) and file.startswith('page'):
    f = open(join(mypath, file),'r').read().replace("\n"," ")
    viewBox_st = re.findall(pattern, f)[0]
    viewBox=viewBox_st.split(' ')
    min_x=float(viewBox[0])
    min_y=float(viewBox[1])
    width=float(viewBox[2])
    height=float(viewBox[3])
    viewBox_rp='viewBox="'+viewBox_st+'"'

    if height>width:
      min_x=(width-height)/2
      viewBox_new=' '.join([str(min_x), str(min_y), str(height), str(height)])
      viewBox_new='viewBox="'+viewBox_new+'"'
      f = f.replace(viewBox_rp,viewBox_new)
    elif height<width:
      min_y=(height-width)/2
      viewBox_new=' '.join([str(min_x), str(min_y), str(width), str(width)])
      viewBox_new='viewBox="'+viewBox_new+'"'
      f = f.replace(viewBox_rp,viewBox_new)

    with open(savepath+file, 'w') as new_f:
      new_f.write(f)

    i+=1
    print(i)
