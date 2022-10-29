import json
import pandas as pd
from more_itertools import chunked

for cond in ['whole+black', 'whole+color', 'part+black', 'part+color'] :
    with open(f'{cond}.json') as f:
        trials_flat = json.load(f)
        trials_flat['targets'] = [c[0] for c in chunked(trials_flat['targets'], 10)]
        trials_flat['texts'] = [c[0] for c in chunked(trials_flat['texts'], 10)]
        trials_flat['images'] = list(chunked(trials_flat['images'], 10))
        pd.DataFrame(trials_flat).iloc[::10, :].to_json(
            f'{cond}_stimuli.json',
            orient="records",
            indent = 2
        )
