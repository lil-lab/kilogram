from tqdm import tqdm
import torch
import os
from IPython import embed

from training.validation import *

def train_epoch(model, dltrain, dlval, optim, lr_scheduler, epoch, run=None):
  model.train()
  epoch_training_step = len(dltrain)

  for i, (encodings) in enumerate(tqdm(dltrain, mininterval=60)):
    optim.zero_grad()

    similarity = model(**encodings) 


    labels = torch.tensor(np.arange(similarity.shape[0])) #[0,1,2,3,...]
    labels = labels.to(similarity.device)

    predicted_t = torch.argmax(similarity, dim=0)
    batch_correct_t = torch.sum(predicted_t==labels).item()

    predicted_i = torch.argmax(similarity, dim=-1)
    batch_correct_i = torch.sum(predicted_i==labels).item()

    batch_total = len(predicted_t)

    loss_t = model.compute_loss(similarity, labels)
    loss_i = model.compute_loss(similarity.t(), labels)

    loss = (loss_t + loss_i) / 2

    acc_t = batch_correct_t / batch_total
    acc_i = batch_correct_i / batch_total
    avg_acc = (acc_t + acc_i) / 2
    train_stats = {'train/loss_t': loss_t, 'train/loss_i': loss_i, 'train/avg_loss':loss, 'train/acc_t': acc_t, 'train/acc_i': acc_i,'train/avg_acc': avg_acc}

    # backward pass
    loss.backward()
    optim.step()

    if lr_scheduler is not None:
      lr_scheduler.step()
      train_stats["utils/lr"] = optim.param_groups[0]["lr"]
  
    # logging
    if run:
      train_stats['utils/epoch'] = epoch
      step = (epoch - 1) * epoch_training_step + i + 1
      run.log(train_stats, step=step)

  # validate after all minibatches
  val_stats = validation_epoch(model, dlval)
  if run:
    val_stats['utils/epoch']=epoch
    step = epoch * epoch_training_step
    run.log(val_stats, step=step)
  
  return train_stats, val_stats