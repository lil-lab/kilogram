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
from val import *

with open('../../database_raw.json') as f:
    data = json.load(f)

with open('../../data_split.json') as f:
    split = json.load(f)


colors=['coral','gold','lightskyblue','lightpink','mediumseagreen','darkgrey','lightgrey']
r=['1','2','3','4','5','6','7']

d=defaultdict(list)
# v=defaultdict(list)

dataset='heldout'

# "pagex-x":["whole"]
for file, annotation in data['annotations'].items():
    if file in split[dataset]:
        for k, (user, detail) in enumerate(annotation.items()):
            whole=detail['whole-annotation']['wholeAnnotation']
            piece_dict=detail['piece-annotation']
            random.shuffle(r)
            # print(r)
            ann_to_idx=defaultdict(list) # ann to indices, ann in random order
            for i in r:
                ann_to_idx[piece_dict[str(i)]].append(str(i))

            text=[whole]
            color_groups=[]
            idx_to_color={}

            for color_idx, (ann, indices) in enumerate(ann_to_idx.items()):
                text.append(ann)
                color_groups.append(indices)
                for t_idx in indices:
                    idx_to_color[t_idx]=colors[color_idx]
            text='#'.join(text)

            # if file in val_files and k==0: # is a val file
            #     v[file].append({'text':text, 'color_groups':color_groups,'idx_to_color':idx_to_color})
            # else:
            d[file].append({'text':text, 'color_groups':color_groups,'idx_to_color':idx_to_color})
           

with open('./texts/color_texts_'+dataset+'.json','w') as f:
    json.dump(d,f)

# with open('./texts/color_texts_val.json','w') as f:
#     json.dump(v,f)

print(len(d))

