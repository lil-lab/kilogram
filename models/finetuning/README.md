# Finetuning CLIP and ViLT on KiloGram dataset
## Requirements
1. Run `pip install` to install all dependencies. Training ViLT model requires higher GPU memory than CLIP. We trained ViLT models on a 24GB memory GPU, and CLIP can be run on a 11GB memory GPU.

2. Download preprocessed data at: https://huggingface.co/datasets/lil-lab/kilogram/tree/main and create `./data/` to place all the downloaded files.
You can also configure the data paths in `./dataloader/data_pathes.py` and `./evaluate.py`.

## Arguments
| Parameter                 | Default       | Description   |	
| :------------------------ |:-------------:| :-------------|
| \-\-model_type 	       |	clip           |clip or vilt
| \-\-dataset_type          | aug_aug           |dataset variants: whole_black, whole_color, part_black, part_color, aug_aug, aug_dev (augmented development set, for by-part analysis)
| \-\-not_logging	       | /	           | if set, no logging; otherwise, logs data on Weights & Biases
| \-\-exp_name 	       |	clip	            |experiment name shown on Weights & Biases logging dashboard
| \-\-save_folder 		           | /             | relative path to the folder for saving models
| \-\-batch_size		      | 10     	   |
| \-\-max_epochs		      | 200     	   | maximum number of epochs for training
| \-\-patience		      | 50     	   | number of epochs without improvement in validation accuracy until stopping
| \-\-random		      | /     	   | if set, use random context; otherwise controlled by constraints

### Optimizer
| Parameter                 | Default       | Description   |	
| :------------------------ |:-------------:| :-------------|
| \-\-learning_rate    | 5e-8         | 
| \-\-optimizer       | Adam  |  
| \-\-weight_decay			             | 1e-6 	           | 
| \-\-lr_mult			     | 10         | scalar constant for learning rate of ViLT

### Scheduler
| Parameter                 | Default       | Description   |	
| :------------------------ |:-------------:| :-------------|
| \-\-lr_scheduler			             | /     	     | if set, use a scheduler for learning rate; otherwise constant learning rate 
| \-\-warmup_epochs		    | 1.0     	     | 

### Evaluation
| Parameter                 | Default       | Description   |	
| :------------------------ |:-------------:| :-------------|
| \-\-eval		      | /     	   | if set, evaluate model; otherwise train
| \-\-load_path		      | /    	   | if set, load saved model from relative path; otherwise initialize out-of-box pretrained model
| \-\-save_name		      | /     	   | file name without extension to save the model evaluation outputs (prediction matrices)
| \-\-heldout		      | /    	   | if set, use heldout set; otherwise use developent set

### Debugging
| Parameter                 | Default       | Description   |	
| :------------------------ |:-------------:| :-------------|
| \-\-debug 	        | /          | 
| \-\-overfit_debug	         | /             | 
| \-\-overfit_size         | 10           |  batch size for debugging overfit
| \-\-checkpoint_path         | /          | 


## Usage
Example for CLIP training:
```
CUDA_VISIBLE_DEVICES=0 \
python3 -m main \
--model_type clip \
--dataset_type part_black \
--optimizer Adam \
--exp_name CLIP_p+b_1_controlled \
--save_folder saved/part+black/model1
```
Example for ViLT training:
```
CUDA_VISIBLE_DEVICES=0 \
python3 -m main \
--model_type vilt \
--dataset_type part_black \
--optimizer AdamW \
--lr_scheduler cosine_warmup \
--max_epochs 30  \
--patience 10 \
--learning_rate 1e-4 \
--weight_decay 0.01 \
--exp_name vilt_p+b_6_random \
--save_folder saved/vilt-random/part_black_6 \
--random
```

Example for evaluation:
```
CUDA_VISIBLE_DEVICES=0 \
python3 -m main \
--model_type clip \
--dataset_type aug_aug \
--eval \
--load_path ./saved/augmented_32/model12/epoch_17.pth \
--save_name random_model12
```
