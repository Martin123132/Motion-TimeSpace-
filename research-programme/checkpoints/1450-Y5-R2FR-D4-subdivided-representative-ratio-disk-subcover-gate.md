# 5434: subdivided representative ratio-disk subcover gate

## Decision

**NO UNIFORM EDGE SUBCOVER AT THE TESTED DEPTH.**

At least one LR/R cell still misses a strict unit-disk margin. The parent must remain unchanged and the failed cell becomes the next derivation target.

## Broad-box summaries

- `LR`: subdivisions `32 x 32`, max `|R|=0.84589207383629605`, max `|qR|=1.0574373004133952`, min external01 edge `0.17437224258410766`, min `|1+qR|=0`, max external41 reciprocal `inf`; pass `False`.
- `R`: subdivisions `32 x 32`, max `|R|=0.85534440690488711`, max `|qR|=1.0692575886920674`, min external01 edge `0.16724907941759273`, min `|1+qR|=0`, max external41 reciprocal `inf`; pass `False`.

## Claim boundary

No parent code is changed here. Right-connector, W3, UV, local-GR, and full-MTS claims remain false.
