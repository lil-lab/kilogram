# Generating model inputs
## /whole+black, part+color
Scripts for generating whole shape and part annotations, as well as black and colored images.
## /augmented
`/aug_aug` contains scripts for generating augmented training set and `aug_dev` for generating augmented development set (for model analysis by adding parts).
## /ref_game_contexts
Scripts for generating reference game contexts used in validation and evaluation with development and heldout sets.
## /caption_texts
Scripts to tranform annotations from "#" concatenated format (<whole>#<part>#...#<part>) to natural language (<whole> with <part>, <part>, ..., and <part>).