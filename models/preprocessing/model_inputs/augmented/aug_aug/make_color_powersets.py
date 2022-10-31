from os import listdir
from os.path import isfile, join
from datetime import datetime, timezone
from collections import defaultdict
import csv 
import json
from collections import defaultdict
import random
from random import sample
import os
from itertools import chain, combinations
from val import *

dataset='train'

def powerset(iterable):
    "returns non empty powerset([1,2,3]) --> shuffled each elt and whole list: [ list(1,) list(2,) list(3,) list(1,2) list(1,3) list(2,3) list(1,2,3)]"
    setsIter = chain.from_iterable(combinations(iterable, r) for r in range(1,len(iterable)+1))
    rs=[]
    for s in setsIter:
      l=list(s)
      random.shuffle(l)
      rs.append(l)
    random.shuffle(rs)
    return rs

with open('../../database_raw.json') as f:
    data = json.load(f)

with open('../../data_split.json') as f:
    split = json.load(f)

colors=['coral','gold','lightskyblue','lightpink','mediumseagreen','darkgrey','lightgrey']
r=['1','2','3','4','5','6','7']

d=defaultdict(list) # training
v=defaultdict(list) # validation
kp=1

# "pagex-x":["whole"]
for file, annotation in data['annotations'].items():
    if file in split[dataset]:
        k=0 # count for anns in this file
        for user, detail in annotation.items():
            
            whole=detail['whole-annotation']['wholeAnnotation']
            piece_dict=detail['piece-annotation']
            random.shuffle(r)
            # print(r)
            ann_to_idx=defaultdict(list) # ann to indices, ann in random order
            for i in r:
                ann_to_idx[piece_dict[str(i)]].append(str(i))

            psets = powerset(list(ann_to_idx.keys())) # all powersets of an ann

             #0 parts
            idx_to_color={}

            for iid in ['1','2','3','4','5','6','7']: # fill not selected piece with black
                idx_to_color[iid]='black'
            if file in val_files and k==0: # is a val file, k==0 bc its the first one
                v[file].append({'text':whole, 'color_groups':[],'idx_to_color':idx_to_color})
            else:
                d[file].append({'text':whole, 'color_groups':[],'idx_to_color':idx_to_color})


            for parts_set in psets: # parts_set = a subset of parts annotations
                text=[whole]
                color_groups=[]
                idx_to_color={}

                for color_idx, part in enumerate(parts_set):
                    text.append(part)
                    indices = ann_to_idx[part]
                    color_groups.append(indices)
                    for t_idx in indices:
                        idx_to_color[t_idx]=colors[color_idx]

                    for iid in ['1','2','3','4','5','6','7']: # fill not selected piece with black
                        if iid not in idx_to_color:
                            idx_to_color[iid]='black'

                text='#'.join(text)

                if file in val_files and k==0: # is a val file
                    v[file].append({'text':text, 'color_groups':color_groups,'idx_to_color':idx_to_color})
                else:
                    d[file].append({'text':text, 'color_groups':color_groups,'idx_to_color':idx_to_color})
            
            # shuffle within a file, make sure whole annotation is not always the first one
            if file in val_files and k==0: # is a val file
                random.shuffle(v[file])
            else:
                random.shuffle(d[file])

            k+=1
        
        print(kp)
        kp+=1

   
with open('./texts/new_powerset_color_texts_'+dataset+'.json','w') as f:
    json.dump(d,f)

with open('./texts/new_powerset_color_texts_val.json','w') as f:
    json.dump(v,f)

print(len(d))
print(len(v))

