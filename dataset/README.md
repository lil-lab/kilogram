# KiloGram Dataset
## ⚠️ Note: 
- Tangrams page5-207, page6-51, and page6-66 are found to be duplicates, so their annotations are similar, but their SVGs differ slighly due to artifacts of the vectorization process.

[updated April 2023]

---
`full.json`: 1016 tangrams, at least 10 annotations each

`dense.json`: 74 tangrams, at least 50 annotations each

`dense10.json`: 74 tangrams sampled for dense annotations, 10 annotations each (from FULL set)

`/tangrams-svg`: 1016 tangrams in SVG format

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
