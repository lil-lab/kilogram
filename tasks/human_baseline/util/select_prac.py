import json
import random

random.seed(10)

with open('val-stimuli/whole+black_stimuli.json') as f:
  d = json.load(f)
  l = len(d)
  print('# stimuli: ', l)

idxs = random.sample(range(l),10) # sample 10 trials
print(idxs)

# stimuli:  236
#[146, 8, 109, 123, 147, 3, 52, 118, 208, 125]

rs={}

for cond in ['whole+black', 'whole+color', 'part+black', 'part+color'] :
  with open(f'val-stimuli/{cond}_stimuli.json') as f:
    d = json.load(f)
    rs[cond] = [d[i] for i in idxs]

with open('prac_trials.json', 'w') as f:
  json.dump(rs, f)