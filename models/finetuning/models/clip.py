import torch
import torch.nn as nn
import clip
import numpy as np

class FTCLIP(nn.Module):
  def __init__(self):
    super(FTCLIP, self).__init__()
    self._device = "cuda" if torch.cuda.is_available() else "cpu"

    model, _ = clip.load("ViT-B/32", device=self._device, jit=False)
    model = model.float()
    self.model = model
    self.encode_image = model.encode_image
    self.encode_text = model.encode_text

    self.logit_scale = nn.Parameter(torch.ones([]) * np.log(1 / 0.07))

    self.loss = nn.CrossEntropyLoss()
    
  def compute_loss(self, predicted, gold_label):
    return self.loss(predicted, gold_label)	

  def compute_norm(self, features):
    return features / features.norm(dim=-1, keepdim=True).float()

  def compute_similarity(self, texts_features, images_features):
    return texts_features @ images_features.t()

  def forward(self, images, texts):
    # Generate train and text features
    I_e=self.encode_image(images.to(self._device)).float()
    T_e=self.encode_text(texts.to(self._device)).float()

    # Normalize features
    images_features = self.compute_norm(I_e)
    texts_features = self.compute_norm(T_e)

    logit_scale = self.logit_scale.exp()
    similarity = logit_scale * images_features @ texts_features.t()
    
    return similarity
  
  def load(self, state_dict):
    self.load_state_dict(state_dict)

  def save(self, model_path, epoch, optim, lr_scheduler, val_loss, loss, acc, count):
    save_dict = {
      'epoch': epoch,
      'model_state_dict': self.state_dict(),
      'optimizer_state_dict': optim.state_dict(),
      'val_loss': val_loss,
      'loss': loss,
      'val_accuracy': acc,
      'patience': count
    }
    if lr_scheduler is not None:
      save_dict["lr_scheduler_state_dict"] = lr_scheduler.state_dict()
    torch.save(save_dict, model_path)

  def train(self):
    self.model.train()
  
  def evaluation(self):
    self.model.eval()
  
  def get_device(self):
    return self._device
