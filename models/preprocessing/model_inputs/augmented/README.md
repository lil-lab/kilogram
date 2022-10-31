# Augmenting dataset
We augment the data by generating every possible subsets of the parts. E.g. "dog#head#tail" will generate "dog#head", "dog#tail", and "dog#head#tail".

## /aug_aug
Augmented training set.
1. Run `make_color_powersets.py` to make a dictionary of augmented data and color mapping information.
2. Run `make_part_anns.py` to generate annotation file.
3. Run `color.py` to color svgs.
4. Run `square.py` to square svgs.
5. Run `to_png.py` to convert to pngs.

## /aug_dev
Augmented development set. Used for evaluating model performance by gradually adding part information.

### images
1. Run `new_dev_make_color_powersets.py` to generate a list of dictionaries. Each dictionary corresponds to an example: for instance,
```
[{annotation:'dog#body',
full_annotation:'dog#head#body',
ann_num_parts: 1,
full_ann_num_parts: 2,
tangram: page1-1,
image: page1-1_0_1,
color_groups
idx_to_color}, ...]
```
2. Run `new_dev_color.py` to color svgs.
3. Run `square.py` to square svgs.
4. Run `to_png.py` to convert to pngs.

### texts/reference games
1. Run `make_df.py` to format the data from images step 1 to a dataframe. This is also used for ploting the results (see `analysis/model/adding_parts`).
2. Run `gen_eval_sets.py` to generate a json of reference games contexts with constraints.
3. Run `make_dataset.py` to format the reference games into model inputs.
