from collections import defaultdict
import json
from collections import defaultdict
import random
from itertools import chain, combinations

dataset='development'
'''
Groups by the total number of parts in ANNOTATION, instead of SOURCE TANGRAM parts
'''

def powerset(iterable):
    '''
    [iterable]: a list of strings
    returns a dict:
    {1: [['tail'], ['body'], ['head']], 2: [['body', 'tail'], ['head', 'tail'], ['body', 'head']], 3: [['body', 'head', 'tail']]})
    '''
    setsIter = {r:combinations(iterable, r) for r in range(1,len(iterable)+1)}
    rs=defaultdict(list)
    for num, s in setsIter.items():
      for ss in s:
        l=list(ss)
        random.shuffle(l)
        rs[num].append(l)
    # random.shuffle(rs)
    return rs

with open('../../../database_raw.json') as f:
    data = json.load(f)

with open('../../../data_split.json') as f:
    split = json.load(f)

colors=['coral','gold','lightskyblue','lightpink','mediumseagreen','darkgrey','lightgrey']
r=['1','2','3','4','5','6','7']

# d=defaultdict(lambda: defaultdict(list)) # training
rs = [] 
'''
[{annotation:'dog#body',
full_annotation:'dog#head#body',
ann_num_parts: 1,
full_ann_num_parts: 2,
tangram: page1-1,
image: page1-1_0_1,
color_groups
idx_to_color}, ...]
'''

kp=1

# "pagex-x":["whole"]
for file, annotation in data['annotations'].items():
    if file in split[dataset]:
        for tangram_ann_idx, (user, detail) in enumerate(annotation.items()):
            # an annotation
            image_file_counter = 0 # count for image files for this annotation

            whole=detail['whole-annotation']['wholeAnnotation']
            piece_dict=detail['piece-annotation']
            random.shuffle(r)
            # print(r)
            ann_to_idx=defaultdict(list) # ann to indices, ann in random order
            for i in r:
                ann_to_idx[piece_dict[str(i)]].append(str(i)) # part ann to the tangram piece indices
            
            parts_no_dup = list(ann_to_idx.keys())
            max_num_parts = len(parts_no_dup) # number of parts of this ann
            psets = powerset(parts_no_dup) # all powersets of an ann

            full_ann = '#'.join([whole] + psets[max_num_parts][0]) # the full annotation

            ### Start building result dicts ###

            #0 parts
            idx_to_color={}

            for iid in ['1','2','3','4','5','6','7']: # fill not selected piece with black
                idx_to_color[iid]='black'
            
            rs.append({
                'annotation': whole,
                'full_annotation': full_ann,
                'ann_num_parts': 0,
                'full_ann_num_parts': max_num_parts,
                'tangram': file,
                'image': file+'_'+str(tangram_ann_idx)+'_'+str(image_file_counter), # tangram_0_0: the 0th annotation of tangram, the 0th subset
                'color_groups':[],
                'idx_to_color':idx_to_color
            })
            image_file_counter+=1
            # d[file][0].append({'text':whole, 'color_groups':[],'idx_to_color':idx_to_color})

            #powersets
            for piece_count, parts_sets in psets.items(): # parts_set = a subset of parts annotations
                for parts_set in parts_sets: 
                    text=[whole]
                    color_groups=[]
                    idx_to_color={}
                    for color_idx, part in enumerate(parts_set):
                        text.append(part)
                        indices = ann_to_idx[part]
                        color_groups.append(indices)
                        for t_idx in indices:
                            idx_to_color[t_idx]=colors[color_idx] # all pieces in the same part are colored the same 

                        for iid in ['1','2','3','4','5','6','7']: # fill not selected piece with black
                            if iid not in idx_to_color:
                                idx_to_color[iid]='black'

                    text='#'.join(text)
                    
                    rs.append({
                        'annotation': text,
                        'full_annotation': full_ann,
                        'ann_num_parts': text.count('#'),
                        'full_ann_num_parts': max_num_parts,
                        'tangram': file,
                        'image': file+'_'+str(tangram_ann_idx)+'_'+str(image_file_counter), # tangram_0_1: the 0th annotation of tangram, the 1st subset
                        'color_groups':color_groups,
                        'idx_to_color':idx_to_color
                    })

                    image_file_counter+=1

                    #d[file][piece_count].append({'text':text, 'color_groups':color_groups,'idx_to_color':idx_to_color})
        
        print(kp)
        kp+=1

   
with open('./dev_texts/new_powerset_color_texts_'+dataset+'.json','w') as f:
    json.dump(rs,f)

print(len(rs))