from os import listdir
from os.path import isfile, join
from datetime import datetime, timezone
from collections import defaultdict
import csv 
import json
from collections import defaultdict
import random
from random import sample
import os

# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')

# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# stop_words = set(stopwords.words('english'))

dataset='val'

# def clean(x): # lowercase, remove determiners
#     words = word_tokenize(x.lower())
#     wl = ' '.join([w for w in words if w not in stop_words and (w.islower() or w.isalnum())])
#     return wl

with open('./texts/cut_powerset_color_texts_'+dataset+'.json') as f:
    data = json.load(f)

d=defaultdict(list)

for p, ann_list in data.items():
    for a in ann_list:
        # text='#'.join([clean(t) for t in a['text'].split('#')])
        d[p].append(a['text'])

with open('../../../fine-tuning/data/cut-augmented-annotations/'+dataset+'_part_sw.json','w') as f:
    json.dump(d,f)

print(len(d))

