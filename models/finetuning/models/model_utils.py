import argparse
import torch
import transformers

from models.clip import FTCLIP
from models.vilt import FTViLT

def _get_model(args: argparse.ArgumentParser):
    if args.model_type == "clip":
        model = FTCLIP()
    elif args.model_type == "vilt":
        model = FTViLT()
    else:
        raise ValueError("model type {} is not supported.".format(args.model_type))
    return model

def _get_optimizer(model, args: argparse.ArgumentParser):
    # Note: the majority of code here is copied from https://github.com/dandelin/ViLT
    # TODO: learing rate schedule
    optimizer_cls = None
    if args.model_type == "vilt":
        assert(args.optimizer == "AdamW")
        no_decay = [
            "bias",
            "LayerNorm.bias",
            "LayerNorm.weight",
            "norm.bias",
            "norm.weight",
            "norm1.bias",
            "norm1.weight",
            "norm2.bias",
            "norm2.weight",
        ]
        head_names = ["vqa_classifier", "nlvr2_classifier"]
        lr_mult = args.lr_mult
        lr=args.learning_rate
        wd=args.weight_decay
        optimizer_grouped_parameters = [
            {
                "params": [
                    p
                    for n, p in model.named_parameters()
                    if not any(nd in n for nd in no_decay)
                    and not any(bb in n for bb in head_names)
                ],
                "weight_decay": wd,
                "lr": lr,
            },
            {
                "params": [
                    p
                    for n, p in model.named_parameters()
                    if any(nd in n for nd in no_decay)
                    and not any(bb in n for bb in head_names)
                ],
                "weight_decay": 0.0,
                "lr": lr,
            },
            {
                "params": [
                    p
                    for n, p in model.named_parameters()
                    if not any(nd in n for nd in no_decay)
                    and any(bb in n for bb in head_names)
                ],
                "weight_decay": wd,
                "lr": lr * lr_mult,
            },
            {
                "params": [
                    p
                    for n, p in model.named_parameters()
                    if any(nd in n for nd in no_decay) and any(bb in n for bb in head_names)
                ],
                "weight_decay": 0.0,
                "lr": lr * lr_mult,
            },
        ]
        optim = torch.optim.AdamW(
            optimizer_grouped_parameters, lr=lr, eps=1e-8, betas=(0.9, 0.98)
        )
    elif args.model_type == "clip":
        assert(args.optimizer == "Adam")
        if args.optimizer == "Adam":
            optimizer_cls = torch.optim.Adam
        else:
            raise ValueError("clip optimizer: Adam")
    
        optim = optimizer_cls(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
    else:
        raise ValueError("model type {} is not supported.".format(args.model_type))

    return optim


def _get_lr_scheduler(optimizer, args: argparse.ArgumentParser, num_training_steps: int):
    scheduler = None
    if args.lr_scheduler == "cosine_warmup":
        # Cosine warmup
        #   HF doc: https://huggingface.co/docs/transformers/main_classes/optimizer_schedules#transformers.get_cosine_schedule_with_warmup.num_training_steps
        num_warmup_steps = int(num_training_steps * (args.warmup_epochs / args.max_epochs))
        scheduler = transformers.get_cosine_schedule_with_warmup(optimizer, num_warmup_steps = num_warmup_steps, num_training_steps = num_training_steps)
    else:
        pass
    
    return scheduler

def _load_from_checkpoint(model, optimizer, lr_scheduler, checkpoint_path: str):
    chpt = torch.load(checkpoint_path)

    # load model
    model.load(chpt["model_state_dict"])

    # load optimizer
    optimizer.load_state_dict(chpt["optimizer_state_dict"])

    # load learning rate scheduler
    if lr_scheduler is not None and "lr_scheduler_state_dict" in chpt:
      lr_scheduler.load_state_dict(chpt["lr_scheduler_state_dict"])



