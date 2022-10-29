from genericpath import exists
from IPython  import embed
from dataloader import *
from training.train import *
from training.validation import *

def train_and_val(model, dltrain, dlval, optimizer, lr_scheduler, n_epochs, patience=None, save_folder=None, run=None, skip_first_eval: bool = False):
  if save_folder:
    print('Saving results to {}'.format(save_folder))

  # pretraining
  if not skip_first_eval:
    print('Pretraining: ')
    val_stats = validation_epoch(model, dlval)
    if run:
      val_stats['epoch']=0
      run.log(val_stats, step=0)

  min_val_loss=99
  count=0

  saved_train_loss=99
  saved_epoch=-1
  saved_accuracy=0

  for epoch in range(1,n_epochs+1):
    print('=======Epoch: ', epoch,'=======')
    train_data, val_stats = train_epoch(model, dltrain, dlval, optimizer, lr_scheduler, epoch, run)

    loss=train_data['train/avg_loss']
    val_loss=val_stats['val/avg_loss']
    acc=val_stats['val/acc_i']
    
    #check if accuracy continued to increase
    if saved_accuracy>=acc:
      count+=1
    else:
      count=0
      min_val_loss=val_loss
      saved_train_loss=loss
      saved_epoch=epoch
      saved_accuracy=acc
      if save_folder:
        os.makedirs(save_folder, exist_ok=True)
        model_path = os.path.join(save_folder, "epoch_" + str(epoch)+'.pth')
        model.save(model_path, epoch, optimizer, lr_scheduler, val_loss, loss, acc, count) # save improved model

    # print('***min val loss: ', min_val_loss)
    print('***saved training loss: ', saved_train_loss)
    print('***saved epoch: ', saved_epoch)
    print('***saved IMAGE accuracy: ', saved_accuracy)
    print('***patience counter: ', count)

    if patience:
      if count>=patience:
        print('pratience exceeded: training completed.')
        break 
      
  print('training completed.')
