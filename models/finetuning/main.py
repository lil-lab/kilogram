import argparse
from args import get_args_parser
from IPython import embed
import torch

from models import _get_model, _get_optimizer, _get_lr_scheduler, _load_from_checkpoint
from dataloader import _get_dataset_pathes, _get_dataloaders
from training import train_and_val
from evaluate import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Tangram training and evaluation script", parents=[get_args_parser()])
    args = parser.parse_args()
    print(args)

    print(torch.__version__)

    # get the model
    model = _get_model(args)

    if args.eval:
        # evaluate model, save the prediction results
        evaluate(args, model)
        # pass
    else:
        # get the dataloader
        dpathes = _get_dataset_pathes(args)
        dataloaders = _get_dataloaders(dpathes, args)

        # get the optimizer
        optimizer = _get_optimizer(model, args)

        # get the learning rate scheduler
        num_training_steps = len(dataloaders['train_loader']) * args.max_epochs
        lr_scheduler = _get_lr_scheduler(optimizer, args, num_training_steps)

        if args.checkpoint_path:
            # TODO: does not support the recovery from training yet.
            #   need to pass patience and val_accuracy to train_and_val
            _load_from_checkpoint(model, optimizer, lr_scheduler, args.checkpoint_path)

        # get the wandb logger
        if not args.not_logging:
            import wandb
            if args.debug:
                run = wandb.init(project='tangram-debug', entity='lil', name=args.exp_name, config=args)
            else:
                run = wandb.init(project='tangram-clip', entity='lil', name=args.exp_name, config=args)
        else:
            run = None

        # launch traning and validation
        train_and_val(model, dataloaders['train_loader'], dataloaders['val_loader'], optimizer, lr_scheduler, \
        args.max_epochs, args.patience, args.save_folder, run)


    
