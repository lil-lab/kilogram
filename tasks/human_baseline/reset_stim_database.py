import pymongo as pm
import random
import json
from more_itertools import chunked

# this auth.json file contains credentials
with open('auth.json') as f :
    auth = json.load(f)

user = auth['user']
pswd = auth['password']

# initialize mongo connection
conn = pm.MongoClient('mongodb://{}:{}@127.0.0.1'.format(user, pswd))

# get database for this project
db = conn['kilogram']

# get stimuli collection from this database
print('possible collections include: ', db.collection_names())
stim_coll = db['stimuli']

# empty stimuli collection if already exists
# (note this destroys records of previous games)
if stim_coll.count() != 0 :
    stim_coll.drop()

# Loop through evidence and insert into collection
for cond in ['whole+black', 'whole+color', 'part+black', 'part+color'] :
    with open(f'./eval_data/{cond}_stimuli.json') as f:
        stimuli = json.load(f)
        random.shuffle(stimuli)
        for s in chunked(stimuli, 20) :
            packet = {'numGames': 0, 'games' : [], 'condition': cond, 'trial_sequence' : s}
            stim_coll.insert_one(packet)

print('checking one of the docs in the collection...')
print(stim_coll.find_one())
