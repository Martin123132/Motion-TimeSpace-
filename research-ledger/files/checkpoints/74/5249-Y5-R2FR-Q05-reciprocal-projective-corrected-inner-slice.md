# 5249 — Q05 reciprocal-projective corrected inner slice

## Calculation

The accepted 5248 interval map directly classifies Q05 geometric poles. Retained residues are refitted, then the regulated inner quadrature and E020/E040 extrapolation are rerun under the same gates as Q03.

## Results

- Geometric poles: `8`.
- Corrected active poles/fits: `0/0`.
- Fixed Q05 order-512 subtracted value: `(-141.4775803303836-0.0005548604602885521j)`.
- Corrected Q05 order-512 subtracted value: `(-160.8231942911625-0.0006217358495971361j)`.
- Corrected-minus-fixed value: `(-19.345613960778905-6.687538930858405e-05j)`.
- Relative change: `0.136739785311`.
- Low/mid extrapolation errors: `4.81219502288e-08`, `6.28243220362e-08`.
- Runtime: `171.907 s`.

## Decision

`ADOPT_CORRECTED_Q05_INNER_SLICE__ASSESS_TWO_NODE_OUTER_IMPACT`

## Claim boundary

Q03 and Q05 are corrected nodes, but the order-9 outer sum still contains inherited values at the other seven nodes. No numeric UV or broader MTS claim follows yet.

## Next exact target

Insert the corrected Q03 and Q05 values into the locked order-9 outer rule, quantify their weighted change, and determine which remaining nodes require the paired topology rebuild before a corrected cubature can close.
