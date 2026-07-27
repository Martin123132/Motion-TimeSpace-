# 3912 — Source-Domain Connection from Product/Quotient Geometry or Bound Input

Timestamp: `2026-07-01T10:12:21+00:00`

## Result

This checkpoint derives the mass-flat connection for the source-silent branch instead of just declaring it.

Source quotient:
`Phi_src <-> (Q_pub, S_src=(M,s^a), R_ref=(tau,Sigma,H_ref), Y_loc, H_priv), q_src(Phi_src)=(Q_pub,S_src,R_ref)`

Source-silent vertical:
`X_v in ker(Dq_src) => D_X Q_pub=0, D_X M=0, D_X s^a=0, D_X tau=0, D_X Sigma=0, D_X H_ref=0`

Connection consequence:
`for source-silent vertical X_v, the product-chart horizontal lift has A_X^M=A_X^a=A_X^I=0, hence partial_M A_X^A=0`

PiM result:
`[D_Xv,Pi_M^H]H=0 and R_PiM=0 for the source-silent vertical class`

Failure class:
`source-active X not in ker(Dq_src) keeps R_PiM <= K_M|partial_M A_X^M|+K_shape||partial_M A_X^a||+K_ref||partial_M A_X^I||`

## Meaning

- For residual directions genuinely vertical to the public/source quotient, `R_PiM=0`.
- The proof is conditional on adopting `q_src`; it is not a public local-GR claim.
- Source-active coupling, support, reference/frame and dynamic-time directions are excluded and get coefficient-bound rows instead.
- The combined 3911 blocker reduces from `R_PiM+R_Htau` to `R_Htau` only in the source-silent stationary branch.

## Source Register

- Source rows found: `20/20`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3912_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3912_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3912_SOURCE_QUOTIENT_BUNDLE_PROOF.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3912_MASS_FLAT_CONNECTION_BRANCH_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3912_SOURCE_ACTIVE_EXCLUSION_ROWS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3912_CONNECTION_COEFFICIENT_BOUND_INPUT_ROWS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3912_LOCAL_ARENA_IMPACT.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3912_BRANCH_DECISION_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3912_NEXT_TARGET.csv`

## Next Target

`3913-Y5-R2FR-Htau-exact-symplectic-curl-from-EH-source-collar-or-bound.md`

Goal: derive `R_Htau=0` from EH/Iyer-Wald source-collar exactness plus extra-sector flux silence, or make the curl a source-backed numeric bound.
