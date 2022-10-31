'''
Make aug dev dataset with contexts.
{
  'targets': ['page', ...],
  'images': ['target_page', 'distractor page', ...*9, 'target_page', ...],
  'texts': ['ann', ...]
}

'''
import json

savepath = './aug_dev.json'

with open('./dev_batch_data.json') as f:
  data=json.load(f)

dataset = {
  'targets': [],
  'images': [],
  'texts': []
}

for page, pc_to_trials in data.items():
  for pc, trials in pc_to_trials.items():
    for trial in trials:
      target_i, target_ann = trial['target']

      dist_sets = trial['distractors']
      new_dist_sets = []

      for dist_set in dist_sets:
        new_dist_i_set = []
        new_dist_ann_set = []

        for dist_i, dist_ann in dist_set:
          new_dist_i_set.append(dist_i)
          new_dist_ann_set.append(dist_ann)

        #one context completed, add to dataset
        dataset['targets']+=[target_i]*10
        dataset['images'].append(target_i)
        dataset['images']+=new_dist_i_set
        dataset['texts'].append(target_ann)
        dataset['texts']+=new_dist_ann_set

[print(len(v)) for v in dataset.values()]
print(len(data.keys()))

with open(savepath, 'w') as f:
  json.dump(dataset, f)


    


           
