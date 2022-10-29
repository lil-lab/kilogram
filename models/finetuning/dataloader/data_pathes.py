import argparse
from typing import Dict 

def _get_dataset_pathes(args: argparse.ArgumentParser) -> Dict:
    _whole_text_train = './data/whole-annotations/train_whole.json'
    _whole_image_train = './data/images-border/border-train'

    _whole_image_val = './data/images-border/border-val'

    _part_text_train = '../make-data/make-png/coloring/texts/train_part_caption.json' #'../make-data/make-png/coloring/texts/train_part_sw.json'
    _part_image_train = '../make-data/make-png/coloring/border-colored-png/train'

    _part_image_val = '../make-data/make-png/coloring/border-colored-png/val'

    if args.dataset_type == "aug_aug":
        IS_WHOLE_IMAGE=False
        TRAIN_TEXT_PATH='./data/new-augmented-annotations/train_part_caption.json' #'./data/new-augmented-annotations/train_part_sw.json'
        TRAIN_IMAGE_PATH= '../make-data/make-png/augmented/images/new_powerset_png_train'
        if args.random:
            VAL_DATA_PATH='./data/new-val-random/texts/part+color_caption.json' #'./data/new-val-random/texts/part+color.json'
        else:
            VAL_DATA_PATH='./data/new-val-controlled/texts/part+color_caption.json' #'./data/new-val-controlled/texts/part+color.json'
        VAL_IMAGE_PATH=_part_image_val

    elif args.dataset_type == "part_color":
        IS_WHOLE_IMAGE=False
        TRAIN_TEXT_PATH=_part_text_train
        TRAIN_IMAGE_PATH=_part_image_train
        if args.random:
            VAL_DATA_PATH='./data/new-val-random/texts/part+color_caption.json' #'./data/new-val-random/texts/part+color.json'
        else:
            VAL_DATA_PATH='./data/new-val-controlled/texts/part+color_caption.json' #'./data/new-val-controlled/texts/part+color.json'
            
        VAL_IMAGE_PATH=_part_image_val

    elif args.dataset_type == "part_black":
        IS_WHOLE_IMAGE=True
        TRAIN_TEXT_PATH=_part_text_train
        TRAIN_IMAGE_PATH=_whole_image_train
        if args.random:
            VAL_DATA_PATH='./data/new-val-random/texts/part+black_caption.json' #'./data/new-val-random/texts/part+black.json'
        else:
            VAL_DATA_PATH='./data/new-val-controlled/texts/part+black_caption.json' #'./data/new-val-controlled/texts/part+black.json'
        VAL_IMAGE_PATH=_whole_image_val

    elif args.dataset_type == "whole_color":
        IS_WHOLE_IMAGE=False
        TRAIN_TEXT_PATH=_whole_text_train
        TRAIN_IMAGE_PATH=_part_image_train
        if args.random:
            VAL_DATA_PATH='./data/new-val-random/texts/whole+color.json'
        else:
            VAL_DATA_PATH='./data/new-val-controlled/texts/whole+color.json'
        VAL_IMAGE_PATH=_part_image_val

    elif args.dataset_type == "whole_black":
        IS_WHOLE_IMAGE=True
        TRAIN_TEXT_PATH=_whole_text_train
        TRAIN_IMAGE_PATH=_whole_image_train
        if args.random:
            VAL_DATA_PATH='./data/new-val-random/texts/whole+black.json'
        else:
            VAL_DATA_PATH='./data/new-val-controlled/texts/whole+black.json'
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
