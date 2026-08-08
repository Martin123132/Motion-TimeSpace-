# 3944 - MHref Source-Energy Comparator and Residual Lower-Bound Row

Timestamp: `2026-07-01T13:01:46+00:00`

## Result

3944 turns the `M_H_ref>0` problem into a source-energy comparator problem.

The comparator is:

`M_EH := c^-2 E_total[tau,W_source]`

in the same tau/coframe/worldtube/surface branch as `M_H_ref`.

It is not orbital `GM`.

## Lower-Bound Law

The same-frame charge decomposition is:

`G_* M_H_ref = G_* M_EH + sum_i Delta_i`.

Therefore:

`M_H_ref >= M_EH*(1-epsilon_abs)`,

where:

`epsilon_abs = sum_i |Delta_i|/(G_* M_EH)`.

If `M_EH>0` and `epsilon_abs<1`, then `M_H_ref>0` without denominator laundering.

## Comparator Route

The route to `M_EH` is Komar/Tolman plus closed-system virial discipline:

- stationary EH source charge gives a Komar/Tolman active mass;
- closed stationary total stress reduces active mass to total energy over `c^2`;
- pressure/stress terms are not dropped unless the total-system virial cancellation or finite bound is supplied.

## Current Verdict

- Progress: the positivity gate is now exact and source-row ready.
- Blocker: no claim-grade `M_EH>0` row exists yet.
- Blocker: the residual envelope `Delta_i` is not filled/theorem-zero.
- Public claim: blocked.

## Source Register

- Source rows found: `17/17`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3944_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3944_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3944_MEH_COMPARATOR_THEOREM.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3944_MHREF_LOWER_BOUND_RESIDUAL_ENVELOPE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3944_MHREF_LOWER_BOUND_CANDIDATE_ROW.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3944_POSITIVITY_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3944_CLAIM_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3944_NEXT_TARGET.csv`

## Next Target

`3945-Y5-R2FR-MEH-total-energy-positive-comparator-or-first-source-row.md`
