# 5226 - Physical permutation-chart bijection and Jacobian theorem

## Result

The first required part of the checkpoint-5225 ratio-free estimator is now
constructed rather than merely proposed. On the real massless three-body
phase space, the `g1<->g3` sequential-chart map is an explicit bijection with
the required Jacobian.

Decision:
`PHYSICAL_CHART_BIJECTION_CLOSED_EXTEND_DIRECTLY_TO_SLOT_AGNOSTIC_TOPOLOGY`.

## Explicit map

The working chart is

`q3=(x3,n3,nd)`,

where `p3=x3(1,n3)` and `p1,p2` are the boosted two-body decay of
`P-p3`. Given `q3`:

1. construct `(p1,p2,p3)`;
2. relabel it as `(p3,p2,p1)`;
3. set `x3'=E1` and `n3'=p1/E1`;
4. inverse-boost the new first momentum `p3` into the rest frame of
   `P-p1` to recover `nd'`.

This defines `T13(q3)`. Repeating the construction returns the original
chart point, so `T13^2=1`.

## Jacobian and measure

For the sequential coordinates,

`dPhi3 proportional to x3 dx3 dOmega3 dOmega_d`.

Permutation invariance therefore requires

`|det DT13| = x3/x3' = E3/E1`.

The finite-difference chart Jacobian was checked at `128`
pre-seeded interior points:

- maximum momentum reconstruction residual:
  `4.521e-11`;
- maximum involution coordinate residual:
  `2.816e-11`;
- maximum Jacobian relative residual:
  `1.691e-07`;
- maximum phase-space density residual:
  `1.691e-07`;
- maximum partition-weight permutation residual:
  `6.094e-11`.

One mapped event has recoil boost
`gamma=460.884`. The validation floor is therefore
set by the explicit float64 conditioning rule
`4 epsilon_machine gamma_max^2`, while the Jacobian step was selected from
its numerical convergence window. The earlier unconditioned development
gate is preserved in the checkpoint source directory rather than hidden.

The result also verifies

`w3(T13 q)=w1(q)`.

Thus the two directly evaluated chart channels have equal expectation
without inserting the unstable source-only ratio `w1/w3`.

## What this closes

The real physical phase-space bijection, its inverse, its Jacobian, measure
invariance, and soft-partition covariance are closed.

## What remains

This does not yet transport the complex relative-root topology. The next
implementation must:

- make event geometry and topology construction soft-slot agnostic;
- rebuild the slot-1 topology directly rather than transport a root;
- verify source, subtraction, chamber, winding, and reciprocal-pair
  covariance;
- establish a finite second-moment envelope;
- then freeze an independent paired-channel pilot.

Those are executable topology tasks, not a missing physical chart map.

## Claim boundary

No numerical UV coefficient, local-GR result, galaxy result, or full-MTS
claim follows. The physical chart theorem removes one concrete obstruction
to the next estimator; it does not complete the complex contour problem.

## Evidence

- Result: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5226\physical_permutation_chart_bijection_results.json`
- Sample rows: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5226\physical_permutation_chart_samples.csv`
- Topology-extension contract: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5226\topology_extension_contract.json`
- Validation: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_5226_VALIDATION.csv`
