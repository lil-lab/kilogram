import os
import json
import argparse
import random
import copy
import numpy as np
from typing import Dict, List
from tqdm import tqdm

import torch
from torch.utils.data import Dataset, DataLoader, Sampler

from dataloader.preprocessor import _get_preprocessor

def load_filenames(file_to_anns, is_whole_image):
  '''
  [images_n]: list of png file names
  [texts_n]: list of annotations
  [is_whole_image]: true if using black tangram images
  '''
  images_n=[] #filenames
  texts_n=[] #annotations
  parts_count=[] #parts count of annotations
  tangrams_n=[] #tangrams
  max_len=0 #max length of annotations for a tangram

  for filename, anns in file_to_anns.items(): # take the ith annotation
    num_anns = len(anns)
    if num_anns>max_len:
      max_len = num_anns

    for i, ann in enumerate(anns):

      if is_whole_image:
        image_filename=filename+'.png'
      else:
        image_filename=filename+'_'+str(i)+'.png'
      
      pc = ann.count(',')+1 #dog#head#tail has 2 parts // a dog with a head, and a body has 2 parts

      images_n.append(image_filename) #['page1-1_2.png', ...]
      texts_n.append(ann) #[dog#head#tail, ...] // [a dog with a head, and a body, ...]
      tangrams_n.append(filename) # [page1-1,...]
      parts_count.append(pc) #[2, ...]

  return images_n, texts_n, tangrams_n, list(set(tangrams_n)), max_len, parts_count

# reference: https://github.com/lil-lab/ViLT-tangram/blob/master/vilt/datasets/tangram_dataset.py#L77
def chunk(indices, chunk_size):
  return torch.split(torch.tensor(indices), chunk_size)

class TrainingSampler(Sampler):
  '''
  For training:
  each context (10 annotations * 10 images):
  [1] no 2 annotations are for the same tangram
  [2] no 2 annotations are the same 
  [3] in each context annotations have the same number of parts

  shuffle after each epoch
  '''
  def __init__(self, batch_size, tangrams_n, texts_n, tangrams_set, max_len, parts_count):
    self._batch_size = batch_size

    self._idx2tangrams: List = np.array(tangrams_n)
    self._idx2texts: List = np.array(texts_n)
    self._idx2parts: List = np.array(parts_count)

    self._parts2idx: Dict = {} # parts count to a list indices
    for idx, p in enumerate(self._idx2parts):
      self._parts2idx.setdefault(p, [])
      self._parts2idx[p].append(idx)
    
    self._tangrams2idx: Dict = {} # tangram to a list indices
    for idx, p in enumerate(self._idx2tangrams):
      self._tangrams2idx.setdefault(p, [])
      self._tangrams2idx[p].append(idx)

    self._texts2idx: Dict = {} # text to a list indices
    for idx, p in enumerate(self._idx2texts):
      self._texts2idx.setdefault(p, [])
      self._texts2idx[p].append(idx)
    
    self._pc2tangrams2idx: Dict = {} # parts count to (unique) tangrams to a list indices 
    for p, idxs in self._parts2idx.items(): # for a certain parts count
      self._pc2tangrams2idx[p]={}
      for idx in idxs:
        tangram=self._idx2tangrams[idx]
        self._pc2tangrams2idx[p].setdefault(tangram,[])
        self._pc2tangrams2idx[p][tangram].append(idx)

    # self.tangrams_set = tangrams_set # a list of tangrams (no duplicates)

    self._reset_batches()
  
  def __iter__(self):
    """
    Batches look like this
        [[bb00, ... bb03], [bb00, ... bb03], [td0], [bb10, ... bb13] ...]
    """
    self._reset_batches()
    return iter(self.indicies)
  
  def __len__(self):
    return len(self.indicies)

  def _reset_batches(self): # shuffling indices while fulfilling constraints
    self.indicies = []

    for p in tqdm(self._parts2idx.keys()): # for a certain parts count # constraint [3]
      print('part count: ', p)
      available_idxs=self._parts2idx[p].copy()
      random.shuffle(available_idxs) # shuffle the order of examples having the same number of parts.

      available_tangrams2idx = copy.deepcopy(self._pc2tangrams2idx[p]) # dict of tangrams to idxs of the same # of parts, remove the tangram when annotations are all picked

      temp_batch = []
      temp_batch_texts = []
      temp_batch_tangrams = []
      idx_to_remove = [] # idx already selected for batch after an iteration of available_idx

      while len(available_tangrams2idx) >= self._batch_size: # there are at least 10 different tangrams/idxs to choose from
        for example_idx in available_idxs: # loop thru all idxs of same # of parts
          
          #check constraints
          new_tangram=self._idx2tangrams[example_idx]
          if new_tangram in temp_batch_tangrams:
            continue # constraint [1]
          new_text=self._idx2texts[example_idx]
          if new_text in temp_batch_texts:
            continue # constraint [2]

          #append idx, text, tangram
          temp_batch.append(example_idx)
          temp_batch_texts.append(new_text)
          temp_batch_tangrams.append(new_tangram)
          idx_to_remove.append(example_idx)

          #check & add batch
          if len(temp_batch)==self._batch_size: # reached batch size
            self.indicies.append(torch.tensor(temp_batch)) # add a batch
            temp_batch=[]
            temp_batch_texts=[]
            temp_batch_tangrams=[]

          #remove tangram whose annotations are all used
          # print('available: ', len(available_tangrams2idx))
          if len(available_tangrams2idx[new_tangram]) == 1:
            del available_tangrams2idx[new_tangram]
            #check if there are still at least 10 different tangrams to choose from
            if len(available_tangrams2idx)<self._batch_size:
              print('not selected: ', available_tangrams2idx)
              break
          else:
            #otherwise remove the idx from that tangram
            available_tangrams2idx[new_tangram].remove(example_idx)
        
        # next parts count: < 10 different tangrams to choose from
        if len(available_tangrams2idx)<self._batch_size:
          print('move to next parts count: < 10 different tangrams to choose from')
          break
        # if after this iteration over all idx, no idx was chosen, i.e. none of them satisfy constraints, move on to the next parts count
        print('to remove (added to new batch): ', len(idx_to_remove), '; availble: ', len(available_idxs))
        if len(idx_to_remove) ==0:
          print('not selected: ', available_tangrams2idx)
          print('move to next parts count: none of the available tangrams satisfies constraints')
          break
        #otherwise, update available_idx, remove ones already used in batches
        available_idxs=[i for i in available_idxs if i not in idx_to_remove]
        idx_to_remove=[] # removed from available idxs, enter next loop through all available examples

    # shuffle batches
    random.shuffle(self.indicies)

    print(len(self.indicies))


class TrainingDataSet(Dataset):
    def __init__(self, image_path, images_n, texts, preprocessor):
      '''
      Requires:
      [image_n]: ['page1-1_2.png', ...]
      [text]: [dog#head#tail, ... ] (corresponds to image)
      '''
      self.image_path = image_path
      self.images_n = images_n
      self.texts = texts
      self._preprocessor = preprocessor 

    def __len__(self):
      '''__len__ returns the number of samples in the dataset.
      :returns: number of (image, annotation) pairs in dataset
      :rtype: int
      '''
      return len(self.texts) 

    def __getitem__(self, idx):
      '''
      __getitem__ returns the tensor, output pair for a given index

        :param idx: index within dataset to return
        :type idx: int
        :returns: encodings
      '''
      image_file = self.images_n[idx]
      image_path = os.path.join(self.image_path, image_file)
      encodings = self._preprocessor.preprocess(image_path, self.texts[idx])
      return encodings


class ValidationDataSet(Dataset):
  def __init__(self, image_path, data, preprocessor):
    '''
    Requires:
    [image_path]: path to images folder
    [data]: contains targets, texts, image filenames
    '''
    self.image_path = image_path
    self.images_n = data['images']
    self.texts = data['texts']
    self.targets = data['targets'] 
    self._preprocessor = preprocessor 

  def __len__(self):
    '''__len__ returns the number of samples in the dataset.
    :returns: number of (image, annotation) pairs in dataset
    :rtype: int
    '''
    return len(self.texts) 

  def __getitem__(self, idx):
    '''
    __getitem__ returns the tensor, output pair for a given index

      :param idx: index within dataset to return
      :type idx: int
      :returns: image tensor, text tensor
      :rtype: tensor, tensor
      
    '''
    image_file = self.images_n[idx]
    image_path = os.path.join(self.image_path, image_file) + '.png' if not image_file.endswith('.png') else os.path.join(self.image_path, image_file)
    encodings = self._preprocessor.preprocess(image_path, self.texts[idx])
    target = self.targets[idx]

    return encodings, target

def _get_dataloaders(dpathes: Dict, args: argparse.ArgumentParser) -> Dict:
  loaders = {}
  
  #load annotations
  f = open(dpathes['train_text_path'])
  file_to_anns_train = json.load(f)

  f = open(dpathes['val_data_path'])
  val_data = json.load(f)

  # load training data
  train_images_n, train_texts_n, train_tangrams_n, train_tangrams_set, train_max_len, train_parts_count = load_filenames(file_to_anns_train, dpathes['is_whole_image'])

  # load preprocessors 
  preprocessor = _get_preprocessor(args)

  # make dataloaders
  if args.overfit_debug:
    inds = random.sample([i for i in range(len(train_images_n))], args.overfit_size)
    train_images_n = list(np.array(train_images_n)[inds])
    train_texts_n = list(np.array(train_texts_n)[inds])
    dstrain = TrainingDataSet(dpathes['train_image_path'], train_images_n, train_texts_n, preprocessor)
    dltrain = DataLoader(dstrain, batch_size=args.batch_size, shuffle=True)
    data = {
      "images":train_images_n,
      "texts": train_texts_n,
      "targets": ["" for _ in range(args.overfit_size)],
    }
    dsval = ValidationDataSet(dpathes['train_image_path'], data, preprocessor)
    dlval = DataLoader(dsval, batch_size=args.batch_size, shuffle=False, drop_last=True)

  elif args.random: # random contexts
    dstrain = TrainingDataSet(dpathes['train_image_path'], train_images_n, train_texts_n, preprocessor)
    dltrain = DataLoader(dstrain, batch_size=args.batch_size, shuffle=True, drop_last=True)
    dsval = ValidationDataSet(dpathes['val_image_path'], val_data, preprocessor)
    dlval = DataLoader(dsval, batch_size=args.batch_size, shuffle=False, drop_last=True)

    print('train data len: ', len(train_images_n),len(train_texts_n))
    print('val data len: ', len(val_data['images']),len(val_data['texts']))
    print('# of train, val batches: ', len(dltrain),len(dlval))

  else: # controlled contexts
    dstrain = TrainingDataSet(dpathes['train_image_path'], train_images_n, train_texts_n, preprocessor)
    sptrain = TrainingSampler(batch_size=args.batch_size, tangrams_n=train_tangrams_n, \
    texts_n=train_texts_n, tangrams_set=train_tangrams_set, max_len=train_max_len, \
    parts_count=train_parts_count) 
    dltrain = DataLoader(dstrain, batch_sampler=sptrain)
    dsval = ValidationDataSet(dpathes['val_image_path'], val_data, preprocessor)
    dlval = DataLoader(dsval, batch_size=args.batch_size, shuffle=False, drop_last=True)

    print('train data len: ', len(train_images_n),len(train_texts_n))
    print('val data len: ', len(val_data['images']),len(val_data['texts']))
    print('# of train, val batches: ', len(dltrain),len(dlval))

  loaders = {
    "train_loader": dltrain,
    "val_loader": dlval
  }
  return loaders
