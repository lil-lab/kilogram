import argparse
from PIL import Image

import torch
import clip
from transformers import ViltProcessor

device = "cuda" if torch.cuda.is_available() else "cpu"

class CLIPPreprocessor():
  def __init__(self) -> None:
    _, self._image_preprocess = clip.load("ViT-B/32", device=device, jit=False)
    self._tokenizer = clip.tokenize

  def preprocess(self, image_path: str, text: str):
    processed_image = self._image_preprocess(Image.open(image_path).convert("RGB"))
    tokenized_text = self._tokenizer([text])[0]
    encodings = {
      "images": processed_image, 
      "texts": tokenized_text
    }
    return encodings

class ViLTPreprocessor():
  def __init__(self) -> None:
    self._preprocessor = ViltProcessor.from_pretrained("dandelin/vilt-b32-mlm")

  def preprocess(self, image_path: str, text: str):
    encodings = self._preprocessor(Image.open(image_path).convert("RGB"), text, return_tensors="pt", padding="max_length", truncation=True, max_length=40, return_special_tokens_mask=False)
    for k in encodings.keys():
      encodings[k] = encodings[k].squeeze(0)
    """
    import os
    from IPython import embed
    embed()
    """
    return encodings

def _get_preprocessor(args: argparse.ArgumentParser):
    if args.model_type == "clip":
      return CLIPPreprocessor()
    elif args.model_type == "vilt":
      return ViLTPreprocessor()
    else:
      raise ValueError("model type {} is not supported.".format(args.model_type))
