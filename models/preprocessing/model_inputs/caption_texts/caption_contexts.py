'''
Convert text data files from # catenated to english like language. Used for context formated jsons.
'''

import inflect
import json
p = inflect.engine()

text_path = '../../data/dev/aug_dev.json'
out_path = '../../data/dev/aug_dev_caption.json'

with open(text_path) as f:
    data = json.load(f)

rs = []
for text in data['texts']:
    whole_parts = text.split("#")
    whole_phrase = whole_parts[0]

    # check whole phrase is a singular and if so add a proper article if missing.
    last_word = whole_phrase.split(" ")[-1]
    if not p.singular_noun(last_word):
        whole_phrase = p.a(whole_phrase)

    # create a caption by iteratively adding part phrases
    caption = "{} with ".format(whole_phrase) if len(whole_parts) != 1 else whole_phrase

    for j in range(len(whole_parts[1:])):

        # check part phrase is a singular and if so add a proper article if missing.
        part_phrase = whole_parts[j+1]
        last_word = part_phrase.split(" ")[-1]
        if not p.singular_noun(last_word):
            part_phrase = p.a(part_phrase)

        # update a caption, tokens positive and a phrase list
        caption += part_phrase

        if j == len(whole_parts[1:]) - 1:
            # the last part phrase
            pass
        elif j == len(whole_parts[1:]) - 2:
            # the second last part phrase
            caption += ", and "
        else:   
            # part phrases coming in between
            caption += ", "

    rs.append(caption)

data['texts'] = rs
with open(out_path, 'w') as f:
    json.dump(data, f)