from os import listdir
from os.path import isfile, join
import json
import re

dataset='val'

with open('./texts/cut_powerset_color_texts_'+dataset+'.json') as f:
    data = json.load(f)

mypath = "../tangrams-svg"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

pattern = r'id="(.*?)"'

n_files=0
n_svgs=0

for page, anns in data.items():
  
  n_files+=1

  file=page+'.svg'
  f = open(join(mypath, file),'r').read().replace("\n"," ")
  
  count=0
  for d in anns:
    n_svgs+=1

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

    new_file_name=page+'_'+str(count)+'.svg'
    with open('./images/cut_powerset_svg_'+dataset+'/'+new_file_name, 'w') as new_f:
      new_f.write(restored)
    count+=1

    print(n_svgs)
  # print(n_files)

print('#files: '+str(n_files) )

print('#svgs: '+str(n_svgs))