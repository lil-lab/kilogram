'''
VERBOSE: Outputs results for every single example/annotation.
'''
import torch
import json
import numpy as np
import torch.nn.functional as F

with open('../data/dev/file_sep_by_part_counts.json') as f:
    data = json.load(f)

########CHANGE##########
loadpaths=['./vilt/aug_dev/random_model1.pth',\
'./vilt/aug_dev/random_model2.pth',\
'./vilt/aug_dev/random_model3.pth']
dict_keys=['model1','model2','model3']+['mult', 'sum']

save_path = './vilt/random_analysis.json'
########CHANGE##########

'''
  predictions = [
  [
    {'page1-1_1_0': [tensor(10,10),...., *10 tensors/trials], ...}, 
    {'page1-1_1_1': [tensor(10,10),...., *10 tensors/trials], ...}
  ],
  ...
  ]
'''
predictions = [torch.load(loadpath) for loadpath in loadpaths]
set_len = 10 #################### num of target/distractor sets per file ################

'''
  probabilities = {
    'page1-1_1_0': 
    { 'model8': [0.8(text), 0.9(image)],
      ...
    },
    ...
  }
'''
probabilities = {}
files = list(data.keys())
print('total files: ', len(files))

for f in files:
  print('filename: ', f)
  # for a file of that count
  file_corrects = np.zeros((len(dict_keys),2)) # each model, mult, sum; each element (text pred, image pred)
  trials_total = set_len # [set_len] trials per file

  probabilities[f] = {}

  for i in range(set_len):
    # the ith trial of that file; e.g. with distractors set #4
    mult_sim_t = torch.ones((10,10)).cpu()
    sum_sim_t = torch.zeros((10,10)).cpu()
    mult_sim_i = torch.ones((10,10)).cpu()
    sum_sim_i = torch.zeros((10,10)).cpu()

    for idx, similarities in enumerate(predictions):
      similarity = similarities[f][i].cpu() # the ith pred matrix of that file

      # softmax over dim that its predicting
      pred_t_softmax = F.softmax(similarity, dim=0) # along cols, pred text
      predicted_t = torch.argmax(pred_t_softmax, dim=0).cpu() # ----using correct count ----
      pred_i_softmax = F.softmax(similarity, dim=-1)
      predicted_i = torch.argmax(pred_i_softmax, dim=-1).cpu() # ----using correct count ----

      # ----using correct count ---- 
      if predicted_t[0] == 0:
        file_corrects[idx][0] +=1 

      if predicted_i[0] == 0:
        file_corrects[idx][1] +=1

      # ----using prob ---- 
      # file_corrects[idx][0] +=pred_t_softmax[0][0] 
      # file_corrects[idx][1] +=pred_i_softmax[0][0]

      # multiplication
      mult_sim_t=torch.mul(mult_sim_t, pred_t_softmax)
      mult_sim_i=torch.mul(mult_sim_i, pred_i_softmax)
      
      # sum, add
      sum_sim_t=torch.add(sum_sim_t, pred_t_softmax)
      sum_sim_i=torch.add(sum_sim_i, pred_i_softmax)

    # ----using correct counts ---- 
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

    # ----using prob instead---- 
    # L1 normalization
    # mult_pred_t_normalize = F.normalize(mult_sim_t, p=1, dim=0)
    # mult_pred_i_normalize = F.normalize(mult_sim_i, p=1, dim=-1)
    # sum_pred_t_normalize = F.normalize(sum_sim_t, p=1, dim=0)
    # sum_pred_i_normalize = F.normalize(sum_sim_i, p=1, dim=-1)

    # file_corrects[-2][0] +=mult_pred_t_normalize[0][0]
    # file_corrects[-2][1] +=mult_pred_i_normalize[0][0]
    # file_corrects[-1][0] +=sum_pred_t_normalize[0][0]
    # file_corrects[-1][1] +=sum_pred_i_normalize[0][0]

  file_acc = file_corrects/trials_total # avg acc over trials on the same target
  print('***correct: ', file_corrects)
  print('***acc: ', file_acc)

  for idd, dict_key in enumerate(dict_keys):
    probabilities[f][dict_key] = (file_acc[idd]).tolist()


with open(save_path, 'w') as fp:
  json.dump(probabilities,fp)