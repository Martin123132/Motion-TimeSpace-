# 5214 - A00 identical-graviton permutation control variate

## Decision

The dominant `A00` source-pole fluctuation now has a derived, coefficient-free
control variate. On the locked twelve-event `5212` sample it cuts the real
topological-local standard deviation by a factor
`0.365206413` and passes the retrospective design
gate. This authorizes a fresh independent pilot; it does not establish the UV
coefficient.

## Exact identity

The identical-graviton cut is partitioned by

`w_i = E_i^-2 / sum_j E_j^-2`

and the working chart carries `3 w_3`. The dominant direct source family

`Y_13 = Y[g1+,g3-]`

is mapped by the exact `g1 <-> g3` permutation to

`Y_31 = Y[g1-,g3+]`.

The physical phase-space measure is invariant. In the sequential chart,
`x_3'=E_1` and the induced coordinate Jacobian obeys
`dq'=(E_3/E_1)dq`; hence the exchanged soft-energy factor and Jacobian return
the original `x_3` measure. The only remaining local reweighting is

`w_1/w_3 = (E_3/E_1)^2`.

Therefore

`C_13 = Y_13 - (w_1/w_3) Y_31`, with `E[C_13]=0`.

The coefficient is fixed to one by permutation symmetry; it is not fitted to
the twelve events. Both families are direct terms, so the soft subtraction is
not imported into the identity. The imaginary component remains uncontrolled
because the earlier imaginary-reflection proposal was rejected.

## Reciprocal-root implementation

The ratio `(E_3/E_1)^2` is inserted before residue summation. Each reciprocal
root receives its own analytic ratio and winding:

`R_w = kappa_R [r_+ n_+ Res_+ + r_- n_- Res_-]`.

This avoids the invalid shortcut of multiplying an already reciprocal-reduced
pair by only one root's ratio. All `4`
permuted-family rows and `10` dominant-family
rows are reciprocal-safe, direct, and finite.

## Locked retrospective result

- Replayed A00 jobs: `24/24`.
- Maximum replay residual: `0.000e+00`.
- Source-family count: `26`.
- Dominant-family covariance fraction: `0.971889386`.
- A00 real SD ratio: `0.217186772`.
- Full `z=-0.6` real SD ratio: `0.217007226`.
- Topological-local real SD ratio: `0.365206413`.
- Topological-local variance reduction: `7.49761627`.
- Control mean in standard errors: `0.286408526`.
- Leave-one-event-out source-family selection unanimous:
  `True`.
- Retrospective candidate:
  `K_mu=-15.7083742`
  `-54.3540163 i`
  with real standard error
  `580.609411`.

The candidate shift is diagnostic only. A control with exactly zero ensemble
mean can move a small retrospective sample substantially; the fresh pilot is
the required bias and efficiency test.

## Claim boundary

This checkpoint proves the control identity and demonstrates retrospective
variance reduction. It does not prove tail convergence, a numerical
two-loop coefficient, local GR, the galaxy branch, or full MTS. Numeric-UV,
local-GR and full-MTS claim flags remain false.

## Next experiment

Freeze the source signatures, rootwise ratio, coefficient `1`, real-only
application, and acceptance thresholds before drawing fresh topological
seeds. Run a small independent pilot first; scale only if it reproduces the
variance reduction without a detectable nonzero control mean.

## Machine-readable evidence

- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5214\A00_source_pole_family_audit.json`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5214\A00_pair_contributions.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5214\A00_event_family_contributions.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5214\A00_event_decomposition.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_5214_VALIDATION.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5214\PROVENANCE.md`
