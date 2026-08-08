# 5119 - S507622 E020 projective-cluster argument independence

## Failure classified

At `E020__S507622_N0000__A00__primary24`, the adaptive integral already passes
its unchanged `5e-5` gate with residual `4.7579349808721275e-5`. The only
failure is one unstable cross-additive residue at the previously certified
projective root `q=-0.0933505726051442`. It contains matching
`direct:g2`/`subtraction:decay` factor suffixes with opposite ownership.

## Exact extension

At the projective collision, `p_g2=-sqrt(1-x) p_decay`. Every global factor
root is a ratio of momentum-linear forms of equal degree. Under
`p -> lambda p`, the common `lambda` therefore cancels from `plus_u`,
`plus_v`, `minus_u` and `minus_v`. Changing the finite external complex
argument, including `E040 -> E020`, cannot move the certified relative root.

All fifteen locked E020 arguments were scanned rather than certifying A00
alone:

- maximum direct/decay factor-root mismatch: `2.1965717747241423e-13`;
- minimum same-source factor separation: `0.003127198980147923`;
- required minimum separation: `1e-6`;
- finite external-factor modulus range: `0.447385..2.235210`;
- A00 unstable rows certified: `1/1`.

The gate authorizes only the fifteen S507622 E020-primary job keys and still
checks event, root, additive sources, factor suffixes and physical ownership
for each row. It is not a broad event or recoil-zero theorem.

The A00 replay converges, and the remaining fourteen rows subsequently
complete. The 5111 matrix is now `180/180` converged with no failed or
unconverged jobs.

## Outputs

- `scripts/Y5_R2FR_5119_S507622_E020_projective_cluster_argument_independence.py`
- `source-intake/functional_rg/5119/S507622_E020_projective_cluster_argument_independence.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5119_VALIDATION.csv`
