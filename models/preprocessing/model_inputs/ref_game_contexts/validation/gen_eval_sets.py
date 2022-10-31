'''
Validation reference games
  each context (10 annotations * 10 images):
  [1] no 2 annotations are for the same tangram
  [2] no 2 annotations are the same 
  [3] in each context annotations have the same number of parts

Validation set: each tangram has exactly one annotation.

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


def roll_distractors(pc, num_distractors, tar, tar_ann, repeat, available_pages, data=data): 
  '''
  Return a list of [repeat] lists of [num] distractors of [pc] pieces, against target as [tar] -- a list of [repeat] contexts
  
  each context (10 annotations * 10 images):
  [1] no 2 annotations are for the same tangram
  [2] no 2 annotations are the same 
  [3] in each context annotations have the same number of parts -- satisfied by [available_pages]

  '''
  lists_distractors=[]
  for i in range(repeat): # gen 1 context each iter
    distractor_filenames = [v for v in available_pages if v!=tar] # except target itself
    random.shuffle(distractor_filenames)

    distractors = []
    existing_whole_anns=[tar_ann.split('#')[0]]
    for df in distractor_filenames: # constraint [1]
      # get distractor pair
      ann_list = data[df][pc] # only 1 in val
      assert len(ann_list)==1

      pick_ann_idx = sample(list(range(len(ann_list))),1)[0] # pick ann idx to avoid indexing duplicated annotation; only 0 in validation
      assert pick_ann_idx==0

      pick_ann = ann_list[pick_ann_idx]
      pick_ann_whole = pick_ann.split('#')[0]
      if pick_ann_whole in existing_whole_anns:
        continue
      else:
        existing_whole_anns.append(pick_ann_whole) # constraint [2]

      pick_img_filenname = df if is_whole_image else df+'_'+str(pick_ann_idx)
      assert pick_img_filenname in imgfilenames

      distractors.append((pick_img_filenname, pick_ann)) # add a context
      if len(distractors) == num_distractors:
        break

    assert len(distractors) == num_distractors
    
    lists_distractors.append(distractors)
  return lists_distractors

########### CHECKING COUNTS #########
# check if there're enough *tangrams* (>=10) per part-count to make contexts
pc_to_tangrams=defaultdict(list)
for tangram, d in data.items():
  assert len(d)==1 #val set, 1 ann per tangram
  for pc, anns in d.items():
    pc_to_tangrams[pc].append(tangram)

dropping =[]
for pc, tangrams in pc_to_tangrams.items():
  if len(tangrams)<10:
    print('*** drop pc (not enough tangrams): ', pc)
    print(tangrams)
    dropping.append(pc)

# check if there're enough *non-duplicating WHOLE anns* per part-count to make contexts
# make sure for setups with whole anns
pc_to_whole_anns=defaultdict(list)
for tangram, d in data.items():
  assert len(d)==1 #val set, 1 ann per tangram
  for pc, anns in d.items():
    ann = anns[0].split('#')[0] # take whole ann
    pc_to_whole_anns[pc].append(ann)

for pc, whole_anns in pc_to_whole_anns.items():
  if len(set(whole_anns))<10:
    print('*** drop pc (not enough distinct anns): ', pc)
    print(whole_anns)
    dropping.append(pc)

# remove
for pc_to_drop in set(dropping):
  del pc_to_tangrams[pc_to_drop]
print(pc_to_tangrams.keys())


########### MAKE CONTEXTS #########

d={f:{} for f in data.keys()} 
for f, pc_to_anns in data.items(): #f:'page1-1'
  for part_count, anns in pc_to_anns.items(): 
   
    if part_count in dropping: # dropped parts count
      print('**skip: ', f, 'parts count: ', part_count)
      continue

    d[f][part_count] = [] # initialize parts count list under a tangram, e.g. all 0 parts for 'page1-1'

    for idx, ann in enumerate(anns):
      target_fn = f if is_whole_image else f+'_'+str(idx)
      assert target_fn in imgfilenames
      file_dict = {
        'target': (target_fn, ann),
        'distractors': roll_distractors(pc=part_count, num_distractors=9, tar=f, tar_ann=ann, repeat=10, available_pages=pc_to_tangrams[part_count]) # constraint[3]
      } 
      d[f][part_count].append(file_dict)

with open(outpath, 'w') as fp:
  json.dump(d,fp)