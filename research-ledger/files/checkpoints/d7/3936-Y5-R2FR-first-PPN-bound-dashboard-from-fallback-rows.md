# 3936 - First PPN Bound Dashboard from Fallback Rows

Timestamp: `2026-07-01T12:03:55+00:00`

## Result

Built the first PPN bound dashboard.

The dashboard records:

- Private branch values: `gamma-1`, `beta-1`, `alpha1`, `alpha2`, `alpha3`, `xi`, `zeta_i`, and `Gdot/G` are zero inside the 3935 theorem branch.
- Fallback formulas: each parameter keeps its executable residual decomposition if the branch clause is revoked.
- Pass rules: current PPN limits and no-cancellation policy are explicit.
- Source status: fallback rows are not score-ready and cannot support a public PPN/local-GR claim yet.

## Claim Gate

The dashboard is useful because it separates theorem-zero from empirical scoring. It does not claim a PPN pass until every active fallback term is theorem-zero or source-backed numeric below bound.

## Source Register

- Source rows found: `10/10`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3936_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3936_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3936_PPN_BOUND_DASHBOARD.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3936_PPN_CLAIM_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3936_PPN_SOURCE_ACQUISITION_QUEUE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3936_DECISION_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3936_NEXT_TARGET.csv`

## Next Target

`3937-Y5-R2FR-R10-or-orbital-first-bound-dashboard.md`
