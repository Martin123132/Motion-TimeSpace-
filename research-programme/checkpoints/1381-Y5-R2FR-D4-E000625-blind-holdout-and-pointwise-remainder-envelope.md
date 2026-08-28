# 5365 - D4 E000625 blind holdout and pointwise remainder envelope

## Decision

`D4_E000625_BLIND_HOLDOUT_COMPATIBLE__POINTWISE_REMAINDER_ENVELOPE_ONLY`

## Blind comparison

Checkpoint 5363 froze the complete fixed-A prediction from E00125, E0025, E005 and E010. Checkpoint 5364 proved the E000625 measurement was absent before launching its independent source-complete integration.

- frozen prediction: `5.7137147615280091 +6.4935296256232826 i`, disk `0.083463978151965684`;
- measured E000625: `5.7135913506908551 +6.4932128604453228 i`, disk `0.022650457948269555`;
- centre separation: `0.00033995648647287726`;
- combined disk radius: `0.10611443610023524`;
- compatibility: `True`.

## Remainder boundary

The measured-minus-frozen-prediction disk gives a valid pointwise defect envelope at epsilon=0.000625. Dividing it by `epsilon^3[1+|Log(epsilon/0.0025)|]` reports a sampled normalized envelope only.

- pointwise defect upper bound: `0.10645439258670812`;
- normalized pointwise upper bound: `182725651.59585911`.

This single holdout cannot promote that sampled number to a uniform `M_D4` over a regulator interval. No refit, regulator-zero, angular, UV, local-GR, or full-MTS claim is made.
