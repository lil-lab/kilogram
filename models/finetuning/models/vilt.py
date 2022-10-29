import torch
import torch.nn as nn
import numpy as np

from transformers import ViltModel, ViltForImageAndTextRetrieval, ViltConfig

from IPython import embed


# Note: copied from https://github.com/dandelin/ViLT
class ITMHead(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.fc = nn.Linear(hidden_size, 2)

    def forward(self, x):
        x = self.fc(x)
        return x
class ViltForImageAndTextMatching(ViltForImageAndTextRetrieval):
  def __init__(self, config):
    super().__init__(config)
    self.itm_score = ITMHead(config.hidden_size)
  
  def _initialize_rank_output(self):
    self.rank_output.weight.data = self.itm_score.fc.weight.data[1:, :]
    self.rank_output.bias.data = self.itm_score.fc.bias.data[1:]
    self.margin = 0.2
    for p in self.itm_score.parameters():
        p.requires_grad = False

class FTViLT(nn.Module):
  def __init__(self, use_logit_scale: bool = False):
    super(FTViLT, self).__init__()
    self._device = "cuda" if torch.cuda.is_available() else "cpu"
    configuration = ViltConfig()
    self.model = ViltForImageAndTextMatching.from_pretrained("dandelin/vilt-b32-mlm-itm") 
    self.model._initialize_rank_output()
    #self.model = ViltForImageAndTextRetrieval.from_pretrained("dandelin/vilt-b32-mlm-itm") 
    self.model.to(self._device)
    self._use_logit_scale = use_logit_scale
    if self._use_logit_scale:
      self.logit_scale = nn.Parameter(torch.ones([]) * np.log(1 / 0.07))
      self.logit_scale.to(self._device)
    self.loss = nn.CrossEntropyLoss()
    
    
  def compute_loss(self, predicted, gold_label):
    #softmax on predicted - prob in one dim
    #torch.select
    return self.loss(predicted, gold_label)	

  def forward(self, **kwargs):
    encodings = {}
    pixel_values, pixel_mask, input_ids, token_type_ids, attention_mask = kwargs["pixel_values"], kwargs["pixel_mask"], kwargs["input_ids"], kwargs["token_type_ids"], kwargs["attention_mask"]
    batch_size = pixel_values.shape[0]

    # repeat pixel_values: [bs x 3 x H x W] ==> [bs ** 2 x 3 x H x W]
    repeated_pixel_values = pixel_values.repeat(batch_size,1,1,1)
    encodings["pixel_values"] = repeated_pixel_values.to(self._device)

    # repeat pixel_mask: [bs x 3 x H x W] ==> [bs ** 2 x H x W]
    repeated_pixel_mask = pixel_mask.repeat(batch_size,1,1)
    encodings["pixel_mask"] = repeated_pixel_mask.to(self._device)

    # repeat input_ids: [bs x 40] ==> [bs ** 2 x 40] 
    repeated_input_ids = input_ids.unsqueeze(1).repeat(1, batch_size,1)
    repeated_input_ids = repeated_input_ids.view(batch_size*batch_size, -1)
    encodings["input_ids"] = repeated_input_ids.to(self._device)

    # repeat token_type_ids: [bs x 40] ==> [bs ** 2 x 40] 
    repeated_token_type_ids = token_type_ids.unsqueeze(1).repeat(1, batch_size,1)
    repeated_token_type_ids = repeated_token_type_ids.view(batch_size*batch_size, -1)
    encodings["token_type_ids"] = repeated_token_type_ids.to(self._device)

    # repeat attention_mask: [bs x 40] ==> [bs ** 2 x 40] 
    repeated_attention_mask = attention_mask.unsqueeze(1).repeat(1, batch_size,1)
    repeated_attention_mask = repeated_attention_mask.view(batch_size*batch_size, -1)
    encodings["attention_mask"] = repeated_attention_mask.to(self._device)

    # get text and image features from ViLT
    # calculae similarity logtis using pretrained head  
    score = self.model(**encodings)["logits"]

    # reshape the ligts and get the similarity matrix
    similarity = score.view(batch_size, batch_size) # [100 x 1] ==> [10 x 10]
    if self._use_logit_scale:
      logit_scale = self.logit_scale.exp()
      similarity = logit_scale * similarity

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
