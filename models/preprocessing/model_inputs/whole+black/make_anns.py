from collections import defaultdict
import json


with open('../database_raw.json') as f:
    data = json.load(f)

with open('../data_split.json') as f:
    split = json.load(f)

# ++++++json+++++++
d=defaultdict(list)
dataset='train'
# "pagex-x":["whole"]
for file, annotation in data['annotations'].items():
    if file in split[dataset]:
        for user, detail in annotation.items():
            d[file].append(detail['whole-annotation']['wholeAnnotation'])

with open('../../fine-tuning/data/whole-annotations/'+dataset+'_whole_clean.json','w') as f:
    json.dump(d,f)

print(len(d))


