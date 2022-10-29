import argparse

def get_args_parser():
    parser = argparse.ArgumentParser("Set transformer detector", add_help=False)

    # model
    parser.add_argument("--model_type", default="clip", type=str)

    # dataset
    parser.add_argument("--dataset_type", default="aug_aug", type=str)
    
    # experiments  
    parser.add_argument("--exp_name", default="clip", type=str)
    parser.add_argument("--not_logging", action='store_true')
    parser.add_argument("--save_folder", type=str)
    parser.add_argument("--debug", action='store_true')
    parser.add_argument("--overfit_debug", action='store_true')
    parser.add_argument("--overfit_size", default=10, type=int)
    parser.add_argument("--checkpoint_path", type=str)

    # optimizer 
    parser.add_argument("--optimizer", default="Adam", type=str)
    parser.add_argument("--learning_rate", default="5e-8", type=float)
    parser.add_argument("--weight_decay", default="1e-6", type=float)
    parser.add_argument("--lr_mult", default="10", type=float)

    # lr_scheduler
    parser.add_argument("--lr_scheduler", default="", type=str)
    parser.add_argument("--warmup_epochs", default=1.0, type=float)

    # training
    parser.add_argument("--batch_size", default="10", type=int)
    parser.add_argument("--max_epochs", default="200", type=int)
    parser.add_argument("--patience", default="50", type=int)

    # setup: random or controlled
    parser.add_argument("--random", action='store_true')

    # eval
    parser.add_argument("--eval", action='store_true')
    parser.add_argument("--load_path", default="", type=str)
    parser.add_argument("--save_name", default="", type=str)

    # heldout
    parser.add_argument("--heldout", action='store_true')

    return parser

