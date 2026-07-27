# 3955 - Observable Metric Z Linear Coefficient Or Source-Current Bound

Timestamp: `2026-07-01T14:28:42+00:00`

## Result

3955 derives the clean coupling theorem:

`C_A_mu_nu := partial g_obs_mu_nu / partial Z^A = D gbar_mu_nu[Dq(Z_A)] + C_A^direct`.

Therefore:

`Z_A in ker(Dq)` and `g_obs=q^*gbar` and `C_A^direct=0` imply `C_A=0`.

This is the exact source-current silence path:

`J_A^obs = 1/2 T_obs^mu_nu C_A_mu_nu = 0`.

## Current MTS Verdict

The theorem is real, but it is not yet a live MTS claim. The actual normal-form `Z^A` variables have not been mapped into `ker(Dq)`.

So the current branch remains:

`||C_A|| <= ||Dgbar|| ||Dq(Z_A)|| + ||C_A^direct|| + ||C_A^coeff|| + ||C_A^readout|| + ||C_A^boundary||`.

and:

`|J_A^obs| <= 1/2 ||T_obs|| ||C_A||`.

## Why This Matters

The coupling gap is now one precise computation:

declare `q`, declare `Z^A`, compute `Dq[Z_A]`.

If it vanishes, the source-current theorem advances. If not, the nonzero part becomes a local PPN/source-normalization residual.

## Source Register

- Source rows found: `19/19`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3955_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3955_VALIDATION.csv`

## Next Target

`3956-Y5-R2FR-Z-verticality-map-computation-or-CA-bound-values.md`
