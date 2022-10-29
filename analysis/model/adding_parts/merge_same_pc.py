import json
import pandas as pd
from collections import defaultdict
import numpy as np
from tqdm import tqdm


#######CHANGE#######
'''columns: 
annotation:'dog#body'...,
full_annotation:'dog#head#body'...,
ann_num_parts: 1...,
full_ann_num_parts: 2...,
tangram: page1-1...,
image: page1-1_0_1...,
'''
source_folder = 'caption-rand-clip' ###CHANGE
df=pd.read_csv('./'+source_folder+'/pred.csv') 
filenames=df['annotation_idx'].to_list()
ann_idxs=list(set(filenames))
print(len(ann_idxs))

plot_model='mult' ##CHANGE
plot_idx=1 #image
######CHANGE########

info={
  "ann_num_parts":[], 
  "avg_probability":[], 
  "full_ann_num_parts":[], 
  "annotation_idx":[]
}

plot_info= pd.DataFrame(info)

for a in tqdm(ann_idxs): # one annotation example
  new_df=df[df['annotation_idx']==a]

  full_pc = new_df['full_ann_num_parts'].to_list()
  assert(len(set(full_pc))==1)
  full_pc=full_pc[0]

  means = new_df.groupby('ann_num_parts')['probability'].mean().to_list() # a list of acc grouped by parts added
  for i, avg_prob in enumerate(means):
    df2 = {"ann_num_parts":i, 
          "avg_probability":avg_prob, 
          "full_ann_num_parts":str(full_pc), 
          "annotation_idx":a}
    plot_info = plot_info.append(df2, ignore_index = True)

plot_info.to_csv('./'+source_folder+'/merged_pred.csv') 
