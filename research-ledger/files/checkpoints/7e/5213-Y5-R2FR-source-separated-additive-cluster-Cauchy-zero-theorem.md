# 5213 — Source-separated additive-cluster Cauchy zero theorem

## Decision

The first fresh `5212` topological failure is **not** repaired by loosening
the residue-stability tolerance. Its four unstable rows satisfy an exact,
guarded zero theorem. The repaired reciprocal-reduced gate converges, but
this remains a non-claim support checkpoint.

## Derivation

Write the finite integrand as

`I(z,q) = D(z,q) - S(z,q)`.

For one additive summand `X in {D,S}`, let `C_X` be a fixed union of small
global contours enclosing the causally selected poles. On a relative
`q`-disk containing no same-summand pole collision, chart origin, or
kinematic singularity,

`R_X(q) = (1/(2 pi i)) integral_(C_X) X(z,q) dz/z`

is holomorphic in `q` by the parameter-dependent Cauchy theorem. A pole of
`D` may coincide with a pole of `S` without singularizing either additive
summand. Therefore `R_D(q)-R_S(q)` remains holomorphic through every guarded
cross-additive cluster. Since the collision centre `q0` is nonzero,

`Res_(q=q0) [(R_D(q)-R_S(q))/q] = 0`.

This is the exact zero inserted by the repair. It is not a fitted value and
does not use the failed double-precision contour estimate.

## Fresh failure audit

- Unstable rows: `4`.
- Certified exact-zero rows: `4`.
- Largest grouped-root residual: `1.822903e-05`.
- Smallest same-summand margin in production contour radii:
  `4.660958e+03`.
- Historical stable-nonzero rows checked:
  `601`.
- In-scope historical counterexamples:
  `0`.
- Raw topological value:
  `{'real': -477514.87953278865, 'imaginary': 9436.525044458487}`.
- Certified repaired topological value:
  `{'real': -477514.88304560125, 'imaginary': 9436.522992478778}`.
- Repaired residue gate converged: `True`.

## Scope discipline

The theorem rejects same-summand pairs, the `direct:g3/subtraction:soft`
alias, chart-origin collisions, incomplete pair-root matches, insufficient
same-summand margins, irregular boundary kinematics, and any row outside
the finite-factor catalogue. The historical 601-row stable-nonzero corpus
contains no row in the authorized strict scope.

This proves only the four guarded local residue zeros and authorizes the
same complete on-demand guard set in the `5212` runner. It does **not**
complete the fresh coefficient pilot and does not support a numeric UV,
local-GR, or full-MTS claim.

## Machine-readable evidence

- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5213\source_separated_additive_cluster_cauchy_zero.json`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5213\source_separated_cluster_rows.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_5213_VALIDATION.csv`
- Source topology: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5212\runs\fresh_two_stratum_pilot_v2\topologies\S521213_N0000__E040_A00.json`
- Historical falsification corpus: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5084\stable_nonzero_falsification_audit.csv`
