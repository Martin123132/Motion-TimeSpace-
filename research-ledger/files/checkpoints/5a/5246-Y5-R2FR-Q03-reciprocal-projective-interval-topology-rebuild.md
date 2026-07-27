# 5246 — Q03 reciprocal-projective interval topology rebuild

## Method

Each Q03 state uses a shared homotopy mesh for the coupled collision roots and reciprocal chamber endpoints. The base 2048/4096 ladder is locally refined only where a boundary-pair half-step exceeds 0.025. Acceptance requires identical winding integers at consecutive base resolutions and every collision, boundary, reciprocal, polynomial, and step-ratio gate.

## Results

- Q03 material jobs rebuilt: `12`.
- Corrected interval rows: `32`.
- Corrected transition brackets: `20`.
- Legacy maps changed: `12/12`.
- Corrected multiplier measure: `{"-0": 7.5942511894263935, "0": 9.619370293615132, "1": 6.666378516958473}`.
- Job-cache hits: `4/12`.
- Runtime: `1958.120 s`.

## Decision

`ADOPT_Q03_RECIPROCAL_PROJECTIVE_INTERVAL_MAP__RUN_CORRECTED_INNER_SLICE`

## Claim boundary

This establishes only the corrected Q03 interval topology. It does not yet alter a published coefficient, rerun Q05, derive local GR, or validate full MTS.

## Next exact target

Use these exact Q03 interval rows to reclassify active poles, refit only the retained residues, rerun the regulated inner quadrature, and compare the corrected Q03 value with the 5241 fixed-resolution value.
