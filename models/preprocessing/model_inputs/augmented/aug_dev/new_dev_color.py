from os import listdir
from os.path import isfile, join
import json
import re
'''
Uses new dev format: 

[{annotation:'dog#body',
full_annotation:'dog#head#body',
ann_num_parts: 1,
full_ann_num_parts: 2,
tangram: page1-1,
image: page1-1_0_1,
color_groups
idx_to_color}, ...]
'''

dataset='development'

with open('./dev_texts/new_powerset_color_texts_'+dataset+'.json') as f:
    data = json.load(f)

mypath = "../../tangrams-svg"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

pattern = r'id="(.*?)"'

n_svgs=0

for d in data:
  n_svgs+=1 #23618
  print(n_svgs)

  file=d['tangram']+'.svg'
  f = open(join(mypath, file),'r').read().replace("\n"," ")
  
  plist=f.split('polygon')
  idx_to_color=d['idx_to_color']
  new_plist=[]
  for i, s in enumerate(plist): 
    if i>0: #for each line of polygon
      piece_id=re.findall(pattern,s)[0] #piece id
      color=idx_to_color[piece_id]# find color
      s=s.replace('fill="lightgray"','fill="'+color+'"') #swap color
      # s=s.replace('stroke="white"','stroke="'+color+'"') #change border color
    new_plist.append(s) 
  restored='polygon'.join(new_plist)

  new_file_name=d['image']+'.svg'
  with open('./dev_images/new_dev_powerset_svg/'+new_file_name, 'w') as new_f:
    new_f.write(restored)

print('#svgs: '+str(n_svgs))