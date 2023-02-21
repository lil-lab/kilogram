import argparse
from typing import Dict 

def _get_dataset_pathes(args: argparse.ArgumentParser) -> Dict:
    # NOTE: Download data at: https://huggingface.co/datasets/lil-lab/kilogram/tree/main and create `./data/` to place all the downloaded files.

    _whole_text_train = './data/training/texts/train_whole.json'
    _whole_image_train = './data/training/images/train-black'

    _whole_image_val = './data/training/images/val-black'

    _part_text_train = './data/training/texts/train_part.json'
    _part_image_train = './data/training/images/train-color'

    _part_image_val = './data/training/images/val-color'

    if args.dataset_type == "aug_aug":
        IS_WHOLE_IMAGE=False
        TRAIN_TEXT_PATH='./data/training/texts/train_augmented_part.json'
        TRAIN_IMAGE_PATH= './data/training/images/augmented'
        if args.random:
            VAL_DATA_PATH='./data/training/texts/validation/random/part+color.json'
        else:
            VAL_DATA_PATH='./data/training/texts/validation/controlled/part+color.json'
        VAL_IMAGE_PATH=_part_image_val

    elif args.dataset_type == "part_color":
        IS_WHOLE_IMAGE=False
        TRAIN_TEXT_PATH=_part_text_train
        TRAIN_IMAGE_PATH=_part_image_train
        if args.random:
            VAL_DATA_PATH='./data/training/texts/validation/random/part+color.json'
        else:
            VAL_DATA_PATH='./data/training/texts/validation/controlled/part+color.json'
            
        VAL_IMAGE_PATH=_part_image_val

    elif args.dataset_type == "part_black":
        IS_WHOLE_IMAGE=True
        TRAIN_TEXT_PATH=_part_text_train
        TRAIN_IMAGE_PATH=_whole_image_train
        if args.random:
            VAL_DATA_PATH='./data/training/texts/validation/random/part+black.json'
        else:
            VAL_DATA_PATH='./data/training/texts/validation/controlled/part+black.json'
        VAL_IMAGE_PATH=_whole_image_val

    elif args.dataset_type == "whole_color":
        IS_WHOLE_IMAGE=False
        TRAIN_TEXT_PATH=_whole_text_train
        TRAIN_IMAGE_PATH=_part_image_train
        if args.random:
            VAL_DATA_PATH='./data/training/texts/validation/random/whole+color.json'
        else:
            VAL_DATA_PATH='./data/training/texts/validation/controlled/whole+color.json'
        VAL_IMAGE_PATH=_part_image_val

    elif args.dataset_type == "whole_black":
        IS_WHOLE_IMAGE=True
        TRAIN_TEXT_PATH=_whole_text_train
        TRAIN_IMAGE_PATH=_whole_image_train
        if args.random:
            VAL_DATA_PATH='./data/training/texts/validation/random/whole+black.json'
        else:
            VAL_DATA_PATH='./data/training/texts/validation/controlled/whole+black.json'
        VAL_IMAGE_PATH=_whole_image_val

    else:
      raise ValueError("dataset type {} is not supported.".format(args.dataset_type))
    
    pathes = {
      "is_whole_image": IS_WHOLE_IMAGE,
      "train_text_path": TRAIN_TEXT_PATH,
      "train_image_path": TRAIN_IMAGE_PATH,
      "val_data_path": VAL_DATA_PATH,
      "val_image_path": VAL_IMAGE_PATH
    }
    
    print(pathes)

    return pathes
