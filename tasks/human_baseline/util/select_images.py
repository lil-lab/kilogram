import json
import shutil

with open('prac_trials.json') as f:
  data = json.load(f)

black = set()
color = set()
for cond in ['whole+black', 'whole+color']:
  trials = data[cond]
  for t in trials:
    images = t['images']
    for img in images:
      if cond == 'whole+black':
        black.add(img)
      if cond == 'whole+color':
        color.add(img)

assert len(black) == len(color)

for img in black:
  shutil.copyfile(f'val-images-black/{img}.png', f'../images/{img}.png')

for img in color:
  shutil.copyfile(f'val-images/{img}.png', f'../images/{img}.png')
  
