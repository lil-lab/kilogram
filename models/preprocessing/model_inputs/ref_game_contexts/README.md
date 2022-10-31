# Reference game contexts
Used for validation and evaluation on development and heldout sets.
## /validation
1. Run `gen_eval_sets.py` to generate controlled contexts, or `gen_eval_sets_random.py` to generate random contexts.
2. Run `make_dataset.py` to format the contexts into model inputs for different conditions (whole/part, black/color).

## /dev+heldout
Same scripts for development and heldout sets.
1. Follow `models/preprocessing/model_inputs/part+color/README.md` to generate a json of part annotations of development or heldout set.
2. Run `make_pc_to_files_colored.py` to generate json with annotations separated by pc, which also includes the annotation index, because image file name doesn't include pc info. Output format:
```
{"tangram": {"0": [(ann, idx), (ann, idx), ...], "1":[...]}})
```
3. Run `gen_eval_sets.py` to generate controlled contexts, or `gen_eval_sets_random.py` to generate random contexts.
4. Run `make_dataset.py` to format the contexts into model inputs for different conditions (whole/part, black/color).