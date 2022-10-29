import torch
import json
import numpy as np
import torch.nn.functional as F
from collections import defaultdict
from os import listdir
from os.path import join, isfile

'''
Calculate model accuracy by 
loading all predictions and average accuracy (1/0 per context) over all contexts for each EXAMPLE
'''

########CHANGE##########
image_path='../data/heldout/images/black' ### 1
image_files = [f.replace('.png','') for f in listdir(image_path) if isfile(join(image_path, f) and f.endswith('.png'))]

loadpaths=['./vilt/part_black/heldout_p+b1.pth','./vilt/part_black/heldout_p+b2.pth','./vilt/part_black/heldout_p+b3.pth'] ### 2
dict_keys=['model1','model2','model3']+['mult', 'sum']

save_path = './vilt/accuracies/heldout_p+b.json' ### 3

print(image_path)
print(loadpaths)
print(save_path)
########CHANGE##########

'''
  predictions = [
    {<image_file_name>: [tensor(10,10),...., *10 tensors/trials], ...}, 
    {<image_file_name>: [tensor(10,10),...., *10 tensors/trials], ...}
  ]
<image_file_name>: page1-1 for black, page1-1_0 for color
'''
predictions = [torch.load(loadpath) for loadpath in loadpaths]

'''
accuracies:
{
  'page1-1_0':{
      'model2': [0.2,0.1], # [t-probs, i-probs]
      'model3': [0.2,0.1],
      'mult':[0.2,0.1],
      'sum': [0.2,0.1]
    },
  ...,
  }
}
'''
corrects = defaultdict(lambda: defaultdict(dict)) # same w accuracies, but with correct counts
tangram_to_contexts_count = defaultdict(int)

for imgfile in image_files:
  print('tangram image: ', imgfile)

  # set up arrays for this file
  file_corrects = np.zeros((len(dict_keys),2)) # each model, mult, sum; each element (text pred, image pred)
  
  # how many contexts - 10 for color, 10*#annotations for black
  trials_total = len(predictions[0][imgfile]) 
  print('total contexts for that target:', trials_total)
  if trials_total==0:
    print('skip ', imgfile)
    continue # skip tangrams with no contexts
  tangram_to_contexts_count[imgfile]+=trials_total

  # for each trial/context
  for i in range(trials_total):
    # the ith trial of that file; e.g. with distractors set #4
    mult_sim_t = torch.ones((10,10)).cpu()
    sum_sim_t = torch.zeros((10,10)).cpu()
    mult_sim_i = torch.ones((10,10)).cpu()
    sum_sim_i = torch.zeros((10,10)).cpu()

    # for each model
    for idx, similarities in enumerate(predictions):
      similarity = similarities[imgfile][i].cpu() # the ith pred matrix of that file

      # softmax over dim that its predicting
      pred_t_softmax = F.softmax(similarity, dim=0) # along cols, pred text
      predicted_t = torch.argmax(pred_t_softmax, dim=0).cpu()
      pred_i_softmax = F.softmax(similarity, dim=-1)
      predicted_i = torch.argmax(pred_i_softmax, dim=-1).cpu()

      if predicted_t[0] == 0:
        file_corrects[idx][0] +=1 

      if predicted_i[0] == 0:
        file_corrects[idx][1] +=1

      # multiplication
      mult_sim_t=torch.mul(mult_sim_t, pred_t_softmax)
      mult_sim_i=torch.mul(mult_sim_i, pred_i_softmax)
      
      # sum, add
      sum_sim_t=torch.add(sum_sim_t, pred_t_softmax)
      sum_sim_i=torch.add(sum_sim_i, pred_i_softmax)

    # check prediction of mult and sum
    mult_predicted_t = torch.argmax(mult_sim_t, dim=0).cpu()
    mult_predicted_i = torch.argmax(mult_sim_i, dim=-1).cpu()

    sum_predicted_t = torch.argmax(sum_sim_t, dim=0).cpu()
    sum_predicted_i = torch.argmax(sum_sim_i, dim=-1).cpu()

    if mult_predicted_t[0] == 0:
        file_corrects[-2][0] +=1
    if mult_predicted_i[0] == 0:
        file_corrects[-2][1] +=1
    if sum_predicted_t[0] == 0:
        file_corrects[-1][0] +=1
    if sum_predicted_i[0] == 0:
        file_corrects[-1][1] +=1

    print('*** trial '+str(i)+' cumulative correct: ', file_corrects)
  
  # for this image file / target, add counts to tangram
  for idd, dict_key in enumerate(dict_keys):
    if len(corrects[imgfile][dict_key]) == 0:
      corrects[imgfile][dict_key] = file_corrects[idd]
    else:
      corrects[imgfile][dict_key] += file_corrects[idd]

# print(corrects)
# print(tangram_to_contexts_count)

accuracies = defaultdict(lambda: defaultdict(dict)) 
for imgfile, model_to_counts in corrects.items():
  for model, counts in model_to_counts.items():
    #counts: [3,4], np.array
    accuracies[imgfile][model] = (counts/tangram_to_contexts_count[imgfile]).tolist()

with open(save_path, 'w') as fp:
    json.dump(accuracies,fp)