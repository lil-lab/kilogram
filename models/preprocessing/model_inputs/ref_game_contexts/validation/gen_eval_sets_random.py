'''
Validation reference games
  each context (10 annotations * 10 images):
 NO CONSTRAINTS

Use part text + color image to generate the full pairs, then use 'texts/make_dataset.py' to convert the val data to each setup
'''
from os import listdir
from os.path import isfile, join
import json
from random import sample
from collections import defaultdict
import random

is_whole_image = False
imgpath = '../../../make-data/make-png/coloring/border-colored-png/val'
datapath = './util_texts/part_val_part.json'
outpath = './texts/part_val_batch_data.json'

imgfilenames = [f.replace('.png','') for f in listdir(imgpath) if isfile(join(imgpath, f))] 

with open(datapath) as f: 
    data = json.load(f) #{page: {'0':[ann,ann,...],...}}

'''
{'page1-1': 

  { 
    0: [
    { target: ('page1-1_0','annotation'),
      distractors: 
      [ [('page2-1_0', 'annotation'),..., *10 distractors], ... *10 lists  ]
    },
    ... # all 0 part files
    ],

    1: .... 
  }
 
  ... #all tangrams
}
** Validation set: each tangram has exactly one annotation.
'''


def roll_distractors(num_distractors, tar, repeat, data=data): 
  '''
  Return a list of [repeat] lists of [num] distractors of [pc] pieces, against target as [tar] -- a list of [repeat] contexts
  
  each context (10 annotations * 10 images):

  '''
  available_pages = list(data.keys())
  lists_distractors=[]
  for i in range(repeat):
    distractor_filenames = sample([v for v in available_pages if v!=tar], num_distractors) # except target itself
    distractors = []
    for df in distractor_filenames:
      # get distractor pair
      ann_list = list(data[df].values())[0]# only 1
      assert len(ann_list) ==1
      # idx only 0 in validation
      pick_ann = ann_list[0]
      pick_ann_idx=0
      pick_img_filenname = df if is_whole_image else df+'_'+str(pick_ann_idx)
      assert pick_img_filenname in imgfilenames

      distractors.append((pick_img_filenname, pick_ann))
    
    lists_distractors.append(distractors)
  return lists_distractors



########### MAKE CONTEXTS #########

d={f:{} for f in data.keys()} 

for f, pc_to_anns in data.items(): #f:'page1-1'
  for part_count, anns in pc_to_anns.items(): 

    d[f][part_count] = [] # initialize parts count list under a tangram, e.g. all 0 parts for 'page1-1'

    for idx, ann in enumerate(anns):
      assert idx ==0 # validation set only
      target_fn = f if is_whole_image else f+'_'+str(idx)
      assert target_fn in imgfilenames
      file_dict = {
        'target': (target_fn, ann),
        'distractors': roll_distractors(num_distractors=9, tar=f, repeat=10)
      } 
      d[f][part_count].append(file_dict)

with open(outpath, 'w') as fp:
  json.dump(d,fp)