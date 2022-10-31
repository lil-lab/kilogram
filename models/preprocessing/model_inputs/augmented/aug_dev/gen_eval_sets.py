'''
Generate eval sets
each context: (10texts*10images)
1) no 2 annotations are for the same tangram/shape
2) all annotations are different
3) annotations have the same number of parts (e.g. dog#head#tail, desk#surface#legs)
4) the original annotations have the same number of parts

Using new augmented dev data from make-data/make-png/augmented/dev/new_...
'''
from os import listdir
from os.path import isfile, join
import json
import random
from random import sample
from collections import defaultdict
import pandas as pd

outpath='./dev_batch_data.json'

imgpath = "../../../make-data/make-png/augmented/dev/dev_images/new_dev_powerset_png"

imgfilenames = [f.replace('.png','') for f in listdir(imgpath) if isfile(join(imgpath, f))] 

'''columns: 
annotation:'dog#body'...,
full_annotation:'dog#head#body'...,
ann_num_parts: 1...,
full_ann_num_parts: 2...,
tangram: page1-1...,
image: page1-1_0_1...,
'''
data=pd.read_csv('../../../make-data/make-png/augmented/dev/dev_texts/new_dev_df.csv') 

    
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
'''


def roll_distractors(pc, num_distractors, tar, tar_ann, tar_ori_pc, repeat, data=data): 
  '''
  [tar]: target tangram, e.g. page1-1
  ---
  Return a list of [repeat] lists of [num] distractors of [pc] pieces, against target as [tar] -- a list of [repeat] contexts
  
  each context (10 annotations * 10 images):
  [1] no 2 annotations are for the same tangram
  [2] no 2 annotations are the same 
  [3] in each context annotations have the same number of parts
  [4] the original annotations have the same number of parts

  '''
  lists_distractors=[]
  available_rows = data.loc[(data['tangram']!=tar) & \
                (data['ann_num_parts']==pc) & \
                (data['full_ann_num_parts']==tar_ori_pc)] # constraint [3]&[4] # available_rows=all examples with same parts count + same original parts count
  distractor_tangrams = list(set(available_rows['tangram'].to_list())) # except the target tangram

  for i in range(repeat): # gen 1 context each iter
    random.shuffle(distractor_tangrams)

    distractors = []
    existing_anns=[tar_ann]
    for df in distractor_tangrams: # constraint [1]
      # get distractor pair
      distractor_rows = available_rows.loc[data['tangram']==df] # rows of this distractor tangram
      num_examples = distractor_rows.shape[0]

      pick_idx = sample(list(range(num_examples)),1)[0] # pick a random example

      pick_dist = distractor_rows.iloc[[pick_idx]].to_dict('records')[0] # dictionary of distractor info

      pick_ann = pick_dist['annotation']
      pick_img_filenname = pick_dist['image']
    
      if pick_ann in existing_anns:
        continue 
        #TODO: it skips the tangram if the randomly picked example exists in the picked annotations. 
        # should be able to check others under this tangram, but it works for now...
      else:
        existing_anns.append(pick_ann) # constraint [2]

      assert pick_img_filenname in imgfilenames

      distractors.append((pick_img_filenname, pick_ann)) # add a context
      if len(distractors) == num_distractors:
        break

    assert len(distractors) == num_distractors
    
    lists_distractors.append(distractors)
  return lists_distractors

########### CHECKING COUNTS #########
# check if there're enough *tangrams* (>=10) per part-count per full-ann part-count to make contexts
# ann_num_parts: 0-7, full: 1-7
print('# examples: ', data.shape[0])
assert data.shape[0] == len(imgfilenames)

for full_ann_pc in range(1, 8):
  for ann_pc in range(full_ann_pc+1):
    available_rows = data.loc[(data['ann_num_parts']==ann_pc) & \
                    (data['full_ann_num_parts']==full_ann_pc)]
    distinct_tangrams = list(set(available_rows['tangram'].to_list()))
    num_available_tangrams = len(distinct_tangrams)
    if num_available_tangrams<10:
      print('drop ann pc: ', ann_pc, 'of full pc: ', full_ann_pc)
      data.drop(data[(data['ann_num_parts']==ann_pc) & (data['full_ann_num_parts']==full_ann_pc)].index, inplace=True)

print('# examples after dropped: ', data.shape[0])

# TODO: check if there're enough *non-duplicating anns* per part-count to make contexts
# make sure for setups with whole anns

# ########### MAKE CONTEXTS #########
count=0
d={}
examples = data['image'].to_list() # e.g. page1-1_0_1 # excluding dropped
for f in examples:
  print(count, f)
  count+=1
  d.setdefault(f, {}) # entry for a tangram

  info = data.loc[data['image']==f].to_dict('records')
  assert len(info)==1
  info = info[0]

  part_count = info['ann_num_parts']

  d[f].setdefault(part_count,[]) # entry for parts count list under a tangram, e.g. all 0 parts for 'page1-1'

  target_fn = f
  ann = info['annotation']

  assert target_fn in imgfilenames
  file_dict = {
    'target': (target_fn, ann),
    'distractors': roll_distractors(pc=part_count, num_distractors=9, tar=f, tar_ann=ann, tar_ori_pc=info['full_ann_num_parts'], repeat=10)
  } 
  d[f][part_count].append(file_dict)


with open(outpath, 'w') as fp:
  json.dump(d,fp)