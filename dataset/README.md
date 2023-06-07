# KiloGram Dataset
## ⚠️ Note: (v0.1.1)
- We found a few tangrams that are duplicates, so their annotations are similar, but their SVGs differ slighly due to artifacts of the vectorization process. We merged their annotations in the dataset. We merged their annotations and removed the SVG files of the duplicates.
	- page5-207, page6-51, and page6-66 -> page5-207 (30 annotations)
	- page2-189 and page4-170 -> page2-189 (20 annotations)

---
`full.json`: 1013 tangrams, at least 10 annotations each

`dense.json`: 74 tangrams, at least 50 annotations each

`dense10.json`: 74 tangrams sampled for dense annotations, 10 annotations each (from FULL set)

`/tangrams-svg`: 1013 tangrams in SVG format

JSON schema:
```
tangram
├── snd
├── pnd
├── psa
└── annotations (list)
    ├── whole
    │   ├── wholeAnnotation
    │   └── timestamp
    ├── part (corresponds to SVG polygon ids)
    │   ├── "1"
    │   ├── "2"
    │   ├── ...
    │   └── "7"
    ├── workerId
    └── metadata
        └── [actionIndex]
            ├── final (if the part annotation is in the final submission)
            ├── pieces
            ├── annotation
            └── timestamp
```
