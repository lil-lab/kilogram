import argparse
from typing import Dict 
from collections import defaultdict
import clip
import torch
import json
from PIL import Image
import os

from models import *
from dataloader.dataloaders import *
from dataloader.preprocessor import _get_preprocessor

def _get_eval_paths(args: argparse.ArgumentParser) -> Dict:
  load_path=args.load_path
  if load_path is None or len(load_path)==0:
    print('Loading model out of the box...')
    # raise ValueError("missing load_path")

  if args.heldout:
    eval_folder='heldout'
    images_dir = 'heldout'
    print('Evaluate on HELDOUT set...')
  else:
    eval_folder = 'new-model-eval-random' if args.random else 'new-model-eval'
    images_dir = 'new-model-eval'
    print('Evaluate on DEV set: '+ eval_folder)

  if args.dataset_type == "aug_aug" or args.dataset_type == "part_color":
    image_path = './data/'+images_dir+'/images/color'   
    data_path = './data/'+eval_folder+'/texts/part+color_caption.json' 

  elif args.dataset_type == "part_black":
    image_path = './data/'+images_dir+'/images/black'
    data_path = './data/'+eval_folder+'/texts/part+black_caption.json'

  elif args.dataset_type == "whole_color":
    image_path = './data/'+images_dir+'/images/color'
    data_path = './data/'+eval_folder+'/texts/whole+color.json'

  elif args.dataset_type == "whole_black":
    image_path = './data/'+images_dir+'/images/black'
    data_path = './data/'+eval_folder+'/texts/whole+black.json'
  
  elif args.dataset_type == "aug_dev": # augmented dev set, for evaluation analysis
    image_path = '../make-data/make-png/augmented/dev/dev_images/new_dev_powerset_png'
    data_path = './data/dev/aug_dev_caption.json'

  else:
    raise ValueError("dataset type {} is not supported.".format(args.dataset_type))

  save_folder = './evaluation/'+args.model_type+'/'+args.dataset_type
  save_name = args.save_name

  if save_name is None:
    raise ValueError('missing save_name')

  os.makedirs(save_folder, exist_ok=True)
  save_path = os.path.join(save_folder, args.save_name+'.pth')

  print('load path: ', load_path) 
  print('image path: ', image_path)
  print('data path: ', data_path)
  print('saved to: ', save_path)

  return load_path, image_path, data_path, save_path

def evaluate(args, model):
  load_path, image_path, data_path, save_path = _get_eval_paths(args)
  # load model
  if load_path is not None and len(load_path)!=0:
    checkpoint = torch.load(load_path)
    model.load_state_dict(checkpoint['model_state_dict'])
  model.evaluation()

  # preprocessor
  preprocessor = _get_preprocessor(args)

  # load data
  with open(data_path) as f:
    eval_data = json.load(f)
  dseval = ValidationDataSet(image_path, eval_data, preprocessor)
  dleval = DataLoader(dseval, batch_size=args.batch_size, shuffle=False, drop_last=True)

  '''
  predictions = 
  {'page1-1_1_0': [tensor(10,10),...., *10 tensors/trials], ...}
  '''
  predictions = defaultdict(list)   

  with torch.no_grad():
    for encodings, targets in tqdm(dleval, mininterval=30):
      assert len(set(targets)) == 1 # this context is for the same target

      similarity = model(**encodings) 
      # predictions[targets[0]].append(similarity)
      predictions[targets[0]].append(similarity[0]) # save the first row (image probs for the target text)

  torch.save(predictions, save_path) 