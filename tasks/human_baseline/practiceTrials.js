// practice trials from validation set
// same 10 trials for each condition
var practiceTrials = {
  "whole+black": [
    {
      "targets": "page3-12",
      "images": [
        "page3-12",
        "page1-110",
        "page3-4",
        "page1-183",
        "page3-39",
        "page1-168",
        "page3-110",
        "page1-88",
        "page1-45",
        "page2-4"
      ],
      "texts": "a jackhammer"
    },
    {
      "targets": "page1-113",
      "images": [
        "page1-113",
        "page1-151",
        "page4-127",
        "page3-67",
        "page3-39",
        "page3-30",
        "page2-40",
        "page3-133",
        "page2-107",
        "page1-109"
      ],
      "texts": "radar dish"
    },
    {
      "targets": "page2-183",
      "images": [
        "page2-183",
        "page4-142",
        "page1-118",
        "page3-3",
        "page2-91",
        "page1-72",
        "page2-77",
        "page2-36",
        "page3-92",
        "page3-170"
      ],
      "texts": "a dog"
    },
    {
      "targets": "page2-32",
      "images": [
        "page2-32",
        "page3-26",
        "page1-112",
        "page2-124",
        "page3-167",
        "page1-133",
        "page2-157",
        "page4-113",
        "page2-74",
        "page2-158"
      ],
      "texts": "cat"
    },
    {
      "targets": "page3-120",
      "images": [
        "page3-120",
        "page1-165",
        "page1-26",
        "page3-127",
        "page1-178",
        "page3-53",
        "page2-47",
        "page4-141",
        "page3-180",
        "page3-65"
      ],
      "texts": "a candy bar coming out of a wrapper"
    },
    {
      "targets": "page1-107",
      "images": [
        "page1-107",
        "page2-17",
        "page1-64",
        "page1-181",
        "page1-47",
        "page3-66",
        "page3-59",
        "page1-162",
        "page1-51",
        "page3-44"
      ],
      "texts": "cat face"
    },
    {
      "targets": "page1-47",
      "images": [
        "page1-47",
        "page4-148",
        "page1-151",
        "page3-193",
        "page3-52",
        "page1-33",
        "page3-40",
        "page1-107",
        "page1-64",
        "page3-43"
      ],
      "texts": "worm"
    },
    {
      "targets": "page2-20",
      "images": [
        "page2-20",
        "page1-5",
        "page1-162",
        "page3-4",
        "page2-65",
        "page3-193",
        "page2-181",
        "page3-99",
        "page3-45",
        "page1-108"
      ],
      "texts": "an angel in a skirt"
    },
    {
      "targets": "page3-64",
      "images": [
        "page3-64",
        "page1-103",
        "page3-206",
        "page3-31",
        "page2-166",
        "page3-205",
        "page3-50",
        "page4-0",
        "page3-47",
        "page1-78"
      ],
      "texts": "duck"
    },
    {
      "targets": "page2-37",
      "images": [
        "page2-37",
        "page3-184",
        "page3-198",
        "page3-168",
        "page2-138",
        "page3-8",
        "page2-185",
        "page3-127",
        "page3-70",
        "page1-96"
      ],
      "texts": "medieval knights helmet"
    }
  ],
  "whole+color": [
    {
      "targets": "page3-12_0",
      "images": [
        "page3-12_0",
        "page1-110_0",
        "page3-4_0",
        "page1-183_0",
        "page3-39_0",
        "page1-168_0",
        "page3-110_0",
        "page1-88_0",
        "page1-45_0",
        "page2-4_0"
      ],
      "texts": "a jackhammer"
    },
    {
      "targets": "page1-113_0",
      "images": [
        "page1-113_0",
        "page1-151_0",
        "page4-127_0",
        "page3-67_0",
        "page3-39_0",
        "page3-30_0",
        "page2-40_0",
        "page3-133_0",
        "page2-107_0",
        "page1-109_0"
      ],
      "texts": "radar dish"
    },
    {
      "targets": "page2-183_0",
      "images": [
        "page2-183_0",
        "page4-142_0",
        "page1-118_0",
        "page3-3_0",
        "page2-91_0",
        "page1-72_0",
        "page2-77_0",
        "page2-36_0",
        "page3-92_0",
        "page3-170_0"
      ],
      "texts": "a dog"
    },
    {
      "targets": "page2-32_0",
      "images": [
        "page2-32_0",
        "page3-26_0",
        "page1-112_0",
        "page2-124_0",
        "page3-167_0",
        "page1-133_0",
        "page2-157_0",
        "page4-113_0",
        "page2-74_0",
        "page2-158_0"
      ],
      "texts": "cat"
    },
    {
      "targets": "page3-120_0",
      "images": [
        "page3-120_0",
        "page1-165_0",
        "page1-26_0",
        "page3-127_0",
        "page1-178_0",
        "page3-53_0",
        "page2-47_0",
        "page4-141_0",
        "page3-180_0",
        "page3-65_0"
      ],
      "texts": "a candy bar coming out of a wrapper"
    },
    {
      "targets": "page1-107_0",
      "images": [
        "page1-107_0",
        "page2-17_0",
        "page1-64_0",
        "page1-181_0",
        "page1-47_0",
        "page3-66_0",
        "page3-59_0",
        "page1-162_0",
        "page1-51_0",
        "page3-44_0"
      ],
      "texts": "cat face"
    },
    {
      "targets": "page1-47_0",
      "images": [
        "page1-47_0",
        "page4-148_0",
        "page1-151_0",
        "page3-193_0",
        "page3-52_0",
        "page1-33_0",
        "page3-40_0",
        "page1-107_0",
        "page1-64_0",
        "page3-43_0"
      ],
      "texts": "worm"
    },
    {
      "targets": "page2-20_0",
      "images": [
        "page2-20_0",
        "page1-5_0",
        "page1-162_0",
        "page3-4_0",
        "page2-65_0",
        "page3-193_0",
        "page2-181_0",
        "page3-99_0",
        "page3-45_0",
        "page1-108_0"
      ],
      "texts": "an angel in a skirt"
    },
    {
      "targets": "page3-64_0",
      "images": [
        "page3-64_0",
        "page1-103_0",
        "page3-206_0",
        "page3-31_0",
        "page2-166_0",
        "page3-205_0",
        "page3-50_0",
        "page4-0_0",
        "page3-47_0",
        "page1-78_0"
      ],
      "texts": "duck"
    },
    {
      "targets": "page2-37_0",
      "images": [
        "page2-37_0",
        "page3-184_0",
        "page3-198_0",
        "page3-168_0",
        "page2-138_0",
        "page3-8_0",
        "page2-185_0",
        "page3-127_0",
        "page3-70_0",
        "page1-96_0"
      ],
      "texts": "medieval knights helmet"
    }
  ],
  "part+black": [
    {
      "targets": "page3-12",
      "images": [
        "page3-12",
        "page1-110",
        "page3-4",
        "page1-183",
        "page3-39",
        "page1-168",
        "page3-110",
        "page1-88",
        "page1-45",
        "page2-4"
      ],
      "texts": "a jackhammer#body#handle#drill"
    },
    {
      "targets": "page1-113",
      "images": [
        "page1-113",
        "page1-151",
        "page4-127",
        "page3-67",
        "page3-39",
        "page3-30",
        "page2-40",
        "page3-133",
        "page2-107",
        "page1-109"
      ],
      "texts": "radar dish#dish#base#electronics"
    },
    {
      "targets": "page2-183",
      "images": [
        "page2-183",
        "page4-142",
        "page1-118",
        "page3-3",
        "page2-91",
        "page1-72",
        "page2-77",
        "page2-36",
        "page3-92",
        "page3-170"
      ],
      "texts": "a dog#head#ears#body#tail"
    },
    {
      "targets": "page2-32",
      "images": [
        "page2-32",
        "page3-26",
        "page1-112",
        "page2-124",
        "page3-167",
        "page1-133",
        "page2-157",
        "page4-113",
        "page2-74",
        "page2-158"
      ],
      "texts": "cat#tail#legs#body#head"
    },
    {
      "targets": "page3-120",
      "images": [
        "page3-120",
        "page1-165",
        "page1-26",
        "page3-127",
        "page1-178",
        "page3-53",
        "page2-47",
        "page4-141",
        "page3-180",
        "page3-65"
      ],
      "texts": "a candy bar coming out of a wrapper#wrapper#candy bar"
    },
    {
      "targets": "page1-107",
      "images": [
        "page1-107",
        "page2-17",
        "page1-64",
        "page1-181",
        "page1-47",
        "page3-66",
        "page3-59",
        "page1-162",
        "page1-51",
        "page3-44"
      ],
      "texts": "cat face#face#ears#neck"
    },
    {
      "targets": "page1-47",
      "images": [
        "page1-47",
        "page4-148",
        "page1-151",
        "page3-193",
        "page3-52",
        "page1-33",
        "page3-40",
        "page1-107",
        "page1-64",
        "page3-43"
      ],
      "texts": "worm#segments#mouth#tail end"
    },
    {
      "targets": "page2-20",
      "images": [
        "page2-20",
        "page1-5",
        "page1-162",
        "page3-4",
        "page2-65",
        "page3-193",
        "page2-181",
        "page3-99",
        "page3-45",
        "page1-108"
      ],
      "texts": "an angel in a skirt#head#skirt#wings"
    },
    {
      "targets": "page3-64",
      "images": [
        "page3-64",
        "page1-103",
        "page3-206",
        "page3-31",
        "page2-166",
        "page3-205",
        "page3-50",
        "page4-0",
        "page3-47",
        "page1-78"
      ],
      "texts": "duck#body#neck#bill#tail#head"
    },
    {
      "targets": "page2-37",
      "images": [
        "page2-37",
        "page3-184",
        "page3-198",
        "page3-168",
        "page2-138",
        "page3-8",
        "page2-185",
        "page3-127",
        "page3-70",
        "page1-96"
      ],
      "texts": "medieval knights helmet#helmet#nose guard"
    }
  ],
  "part+color": [
    {
      "targets": "page3-12_0",
      "images": [
        "page3-12_0",
        "page1-110_0",
        "page3-4_0",
        "page1-183_0",
        "page3-39_0",
        "page1-168_0",
        "page3-110_0",
        "page1-88_0",
        "page1-45_0",
        "page2-4_0"
      ],
      "texts": "a jackhammer#body#handle#drill"
    },
    {
      "targets": "page1-113_0",
      "images": [
        "page1-113_0",
        "page1-151_0",
        "page4-127_0",
        "page3-67_0",
        "page3-39_0",
        "page3-30_0",
        "page2-40_0",
        "page3-133_0",
        "page2-107_0",
        "page1-109_0"
      ],
      "texts": "radar dish#dish#base#electronics"
    },
    {
      "targets": "page2-183_0",
      "images": [
        "page2-183_0",
        "page4-142_0",
        "page1-118_0",
        "page3-3_0",
        "page2-91_0",
        "page1-72_0",
        "page2-77_0",
        "page2-36_0",
        "page3-92_0",
        "page3-170_0"
      ],
      "texts": "a dog#head#ears#body#tail"
    },
    {
      "targets": "page2-32_0",
      "images": [
        "page2-32_0",
        "page3-26_0",
        "page1-112_0",
        "page2-124_0",
        "page3-167_0",
        "page1-133_0",
        "page2-157_0",
        "page4-113_0",
        "page2-74_0",
        "page2-158_0"
      ],
      "texts": "cat#tail#legs#body#head"
    },
    {
      "targets": "page3-120_0",
      "images": [
        "page3-120_0",
        "page1-165_0",
        "page1-26_0",
        "page3-127_0",
        "page1-178_0",
        "page3-53_0",
        "page2-47_0",
        "page4-141_0",
        "page3-180_0",
        "page3-65_0"
      ],
      "texts": "a candy bar coming out of a wrapper#wrapper#candy bar"
    },
    {
      "targets": "page1-107_0",
      "images": [
        "page1-107_0",
        "page2-17_0",
        "page1-64_0",
        "page1-181_0",
        "page1-47_0",
        "page3-66_0",
        "page3-59_0",
        "page1-162_0",
        "page1-51_0",
        "page3-44_0"
      ],
      "texts": "cat face#face#ears#neck"
    },
    {
      "targets": "page1-47_0",
      "images": [
        "page1-47_0",
        "page4-148_0",
        "page1-151_0",
        "page3-193_0",
        "page3-52_0",
        "page1-33_0",
        "page3-40_0",
        "page1-107_0",
        "page1-64_0",
        "page3-43_0"
      ],
      "texts": "worm#segments#mouth#tail end"
    },
    {
      "targets": "page2-20_0",
      "images": [
        "page2-20_0",
        "page1-5_0",
        "page1-162_0",
        "page3-4_0",
        "page2-65_0",
        "page3-193_0",
        "page2-181_0",
        "page3-99_0",
        "page3-45_0",
        "page1-108_0"
      ],
      "texts": "an angel in a skirt#head#skirt#wings"
    },
    {
      "targets": "page3-64_0",
      "images": [
        "page3-64_0",
        "page1-103_0",
        "page3-206_0",
        "page3-31_0",
        "page2-166_0",
        "page3-205_0",
        "page3-50_0",
        "page4-0_0",
        "page3-47_0",
        "page1-78_0"
      ],
      "texts": "duck#body#neck#bill#tail#head"
    },
    {
      "targets": "page2-37_0",
      "images": [
        "page2-37_0",
        "page3-184_0",
        "page3-198_0",
        "page3-168_0",
        "page2-138_0",
        "page3-8_0",
        "page2-185_0",
        "page3-127_0",
        "page3-70_0",
        "page1-96_0"
      ],
      "texts": "medieval knights helmet#helmet#nose guard"
    }
  ]
}
