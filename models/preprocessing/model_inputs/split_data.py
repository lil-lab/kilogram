from collections import defaultdict
import json
import random
from random import sample

sampled = [
  "page2-34.svg",
  "page9-46.svg",
  "page3-85.svg",
  "page7-107.svg",
  "page8-159.svg",
  "page6-203.svg",
  "page2-112.svg",
  "page1-116.svg",
  "page1-69.svg",
  "page8-234.svg",
  "page8-21.svg",
  "page5-75.svg",
  "page1-0.svg",
  "page5-59.svg",
  "page3-121.svg",
  "page6-164.svg",
  "page4-128.svg",
  "page5-136.svg",
  "page6-99.svg",
  "page7-14.svg",
  "page5-128.svg",
  "page9-27.svg",
  "page7-105.svg",
  "page6-162.svg",
  "page9-13.svg",
  "page1-128.svg",
  "page5-186.svg",
  "page3-72.svg",
  "page4-157.svg",
  "page3-182.svg",
  "page7-197.svg",
  "page7-180.svg",
  "page6-143.svg",
  "page7-81.svg",
  "page3-136.svg",
  "page5-64.svg",
  "page7-218.svg",
  "page3-128.svg",
  "page7-26.svg",
  "page6-78.svg",
  "page4-24.svg",
  "page5-153.svg",
  "page7-248.svg",
  "page5-244.svg",
  "page4-93.svg",
  "page5-28.svg",
  "page8-235.svg",
  "page5-200.svg",
  "page2-131.svg",
  "page8-183.svg",
  "page1-119.svg",
  "page5-232.svg",
  "page1-129.svg",
  "page4-162.svg",
  "page3-41.svg",
  "page6-180.svg",
  "page6-149.svg",
  "page1-105.svg",
  "page4-10.svg",
  "page5-178.svg",
  "page2-137.svg",
  "page3-35.svg",
  "page-A.svg",
  "page-B.svg",
  "page-C.svg",
  "page-D.svg",
  "page-E.svg",
  "page-F.svg",
  "page-G.svg",
  "page-H.svg",
  "page-I.svg",
  "page-J.svg",
  "page-K.svg",
  "page-L.svg",
]

random.seed(0)
d=defaultdict(list)
# "pagex-x":["whole"]
flst=[]
for file, annotation in data['annotations'].items():
    if file+'.svg' not in sampled:
        flst.append(file)

dev_and_heldout=sample(flst, 250)
dev=sample(dev_and_heldout,125)
heldout=[ff for ff in dev_and_heldout if ff not in dev]

train_and_val=[ff for ff in flst if ff not in dev_and_heldout]
val=sample(train_and_val, 115)
train=[ff for ff in train_and_val if ff not in val]

d['train']=train
d['validation']=val
d['heldout']=heldout
d['development']=dev
d['dense']=[s.replace('.svg','') for s in sampled]

with open('../fine-tuning/data/data_split.json','w') as f:
    json.dump(d,f)
