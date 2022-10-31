'''
Make validation dataset with contexts.
{
  'targets': ['page', ...],
  'images': ['target_page', 'distractor page', ...*9, 'target_page', ...],
  'texts': ['ann', ...]
}

'''
import json

is_whole_text = False
is_black_image = False
savepath = './part+color.json'
print(savepath)

with open('./eval_batch_data.json') as f:
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
      
      new_target_i = target_i.split('_')[0] if is_black_image else target_i
      new_target_ann = target_ann.split('#')[0] if is_whole_text else target_ann

      dist_sets = trial['distractors']
      new_dist_sets = []

      for dist_set in dist_sets:
        new_dist_i_set = []
        new_dist_ann_set = []

        for dist_i, dist_ann in dist_set:
          new_dist_i = dist_i.split('_')[0] if is_black_image else dist_i
          new_dist_ann = dist_ann.split('#')[0] if is_whole_text else dist_ann
          new_dist_i_set.append(new_dist_i)
          new_dist_ann_set.append(new_dist_ann)

        #one context completed, add to dataset
        dataset['targets']+=[new_target_i]*10
        dataset['images'].append(new_target_i)
        dataset['images']+=new_dist_i_set
        dataset['texts'].append(new_target_ann)
        dataset['texts']+=new_dist_ann_set

[print(len(v)) for v in dataset.values()]
print(len(data.keys()))

with open(savepath, 'w') as f:
  json.dump(dataset, f)


    


           
