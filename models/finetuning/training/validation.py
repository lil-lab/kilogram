import encodings
from collections import defaultdict
import numpy as np
from IPython import embed

import torch
from tqdm import tqdm


def validation_epoch(model, dlval):
  model.evaluation()
  
  print('validation epoch')

  correct_t, correct_i = 0, 0
  total_loss, total_loss_i, total_loss_t = 0, 0, 0

  with torch.no_grad():
    for encodings, targets in tqdm(dlval, mininterval=60):
      assert len(set(targets)) == 1 # this context is for the same target

      similarity = model(**encodings) 
      
      labels = torch.tensor(np.arange(similarity.shape[0]))
      labels = labels.to(similarity.device)

      predicted_t = torch.argmax(similarity, dim=0).cpu()
      if predicted_t[0] == 0: # correctly predict target
        correct_t +=1

      predicted_i = torch.argmax(similarity, dim=-1).cpu()
      if predicted_i[0] == 0:
        correct_i +=1

      loss_t = model.compute_loss(similarity, labels)
      loss_i = model.compute_loss(similarity.t(), labels)

      loss = (loss_t+loss_i)/2
      total_loss_i += loss_i
      total_loss_t += loss_t
      total_loss += loss

    n_contexts = len(dlval)
    avg_loss_t = total_loss_t / n_contexts
    avg_loss_i =  total_loss_i / n_contexts
    avg_loss = total_loss / n_contexts
    acc_t = correct_t / n_contexts #because validation has exactly 1 annotation per tangram, 10 contexts per annotation, tangram-wise avg equivalent to global avg
    acc_i = correct_i / n_contexts
    avg_acc = (acc_t + acc_i)/2

    # print('validation text loss: ', loss_t)
    # print('validation image loss: ', loss_i)
    print('average validation loss: ', avg_loss)
    # print('validation text prediction accuracy: ', acc_t)
    # print('validation image prediction accuracy: ', acc_i)
    print('average validation accuracy: ', avg_acc)

    val_stats = {'val/loss_t': avg_loss_t, 'val/loss_i': avg_loss_i, 'val/avg_loss': avg_loss, 'val/acc_t': acc_t, 'val/acc_i': acc_i,'val/avg_acc': avg_acc}


  return val_stats

