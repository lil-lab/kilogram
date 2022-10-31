'''
Make json with anns separated by pc. ({"tangram": {"0": [(ann, idx), (ann, idx), ...], "1":[...]}})
Takes in original colored dev json

**It also includes the annotation index, because image file name doesn't include pc info
'''
import json
from collections import defaultdict
#aug:
#'../new-augmented-annotations/val_part_sw.json'

#whole:
#../whole-annotations/val_whole.json

#part:
#'../../../make-data/make-png/coloring/texts/val_part_sw.json'

#####CHANGE######
loadpath = './util_texts/dev_colored.json'
savepath = './util_texts/colored_dev_part_with_idx.json'
#####CHANGE######

with open (loadpath) as f:
  data = json.load(f)


d=defaultdict(lambda: defaultdict(list)) #({"tangram": {"0": [(ann,idx), (ann,idx), ...], "1":[...]}})

for page, anns in data.items():
  for idx, ann in enumerate(anns):
    pc = ann.count('#')
    d[page][pc].append((ann,idx))

# sort by pc
sorted_d = {}
for page, pc_to_anns in d.items():
  sorted_d[page] = dict(sorted(pc_to_anns.items()))

with open(savepath,'w') as f:
    json.dump(sorted_d,f)
    
