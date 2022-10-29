import json
import pandas as pd
from collections import defaultdict
import numpy as np
from tqdm import tqdm


'''columns: 
annotation:'dog#body'...,
full_annotation:'dog#head#body'...,
ann_num_parts: 1...,
full_ann_num_parts: 2...,
tangram: page1-1...,
image: page1-1_0_1...,
'''
df=pd.read_csv('./new_dev_df.csv') 
filenames=df['image'].to_list()
print(len(filenames))

# df=df.set_index('image') # set index to image

######CHANGE########
plot_model='mult'   ####CHANGE
plot_idx=1 #image
source_folder = 'caption-cont-vilt'  ####CHANGE

with open('./'+source_folder+'/probs_verbose.json') as f:
  data=json.load(f)
######CHANGE########

new_df={}

annotation_idxs=[]
probs=[]
ann_pc=[]
full_ann_pc=[]

for f in tqdm(filenames):
  if f not in data:
    print(f)
    continue
  probs.append(data[f][plot_model][plot_idx])
  t, ann_i, perm = f.split('_')
  annotation_idx = t+'_'+ann_i
  annotation_idxs.append(annotation_idx)
  ann_pc.append(df[df['image']==f]['ann_num_parts'].to_list()[0])
  full_ann_pc.append(df[df['image']==f]['full_ann_num_parts'].to_list()[0])

new_df['probability'] = probs
new_df['annotation_idx'] = annotation_idxs
new_df['ann_num_parts'] = ann_pc
new_df['full_ann_num_parts'] = full_ann_pc

plot_info= pd.DataFrame(new_df)
plot_info.to_csv('./'+source_folder+'/pred.csv') 
