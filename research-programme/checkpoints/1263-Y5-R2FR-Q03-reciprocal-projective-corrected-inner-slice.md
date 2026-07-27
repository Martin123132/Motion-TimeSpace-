# 5247 — Q03 reciprocal-projective corrected inner slice

## Calculation

The 5246 interval map is used without reinterpretation to classify every geometric pole. Only poles in a nonzero corrected winding interval remain active; those residues are refitted before the regulated inner quadrature and E020/E040 extrapolation are rerun.

## Results

- Geometric poles: `8`.
- Corrected active poles/fits: `0/0`.
- Fixed Q03 order-512 subtracted value: `(274.9820027716404+0.000634794066302506j)`.
- Corrected Q03 order-512 subtracted value: `(252.15977839895186+0.0006007742174577774j)`.
- Corrected-minus-fixed value: `(-22.822224372688538-3.40198488447286e-05j)`.
- Relative change: `0.0829953383953`.
- Low/mid extrapolation errors: `3.23759575591e-08`, `6.57241053102e-09`.
- Runtime: `165.289 s`.

## Decision

`ADOPT_CORRECTED_Q03_INNER_SLICE__REBUILD_Q05_RECIPROCAL_PROJECTIVE_MAP`

## Claim boundary

This is one corrected outer node, not the full order-9 angular result. It cannot support a numeric UV, local-GR, or full-MTS claim until Q05 and the remaining affected outer nodes are treated under the same transport law.

## Next exact target

Apply the 5245 reciprocal-projective transport and 5246 adaptive mesh contract to all twelve Q05 jobs, rebuild its interval map, and rerun its corrected inner slice.
