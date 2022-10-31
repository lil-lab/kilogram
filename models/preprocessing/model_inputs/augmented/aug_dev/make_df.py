import pandas as pd
import json

with open('./new_powerset_color_texts_development.json') as f:
  data = json.load(f)

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

rs = {'annotation':[],
'full_annotation':[],
'ann_num_parts': [],
'full_ann_num_parts': [],
'tangram': [],
'image': []}

for d in data:
  rs['annotation'].append(d['annotation'])
  rs['full_annotation'].append(d['full_annotation'])
  rs['ann_num_parts'].append(d['ann_num_parts'])
  # assert d['ann_num_parts']==d['annotation'].count('#')
  rs['full_ann_num_parts'].append(d['full_ann_num_parts'])
  # assert d['full_ann_num_parts']==d['full_annotation'].count('#')
  rs['tangram'].append(d['tangram'])
  rs['image'].append(d['image'])

df = pd.DataFrame.from_dict(rs)
df.to_csv('./new_dev_df.csv')