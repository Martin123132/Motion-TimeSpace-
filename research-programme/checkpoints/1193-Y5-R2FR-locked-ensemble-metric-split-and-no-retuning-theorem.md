# 5177 - Locked ensemble metric split and no-retuning theorem

Marker: `MTS_5177_LOCKED_ENSEMBLE_METRIC_SPLIT_NO_RETUNING_THEOREM`.

Date: 2026-07-23.

## Question and discipline

Checkpoint 5176 completed its frozen twelve-seed comparison with a significant
MTS-directed q-band-distance component but no RMSE or joint-win preference.
This checkpoint does not retune either model and does not run another
trajectory. It reconstructs all 24 scored profiles from the frozen phase and
evolution caches, reproduces every recorded q and RMSE, and asks what the split
means mathematically.

All diagnostics below are post hoc unless they quote checkpoint 5176's locked
confirmatory result. They cannot be used to promote the 5176 outcome.

## Two different estimands

The q statistic is a five-point local logarithmic slope around
`R_tr=36.43917542575495 kpc`:

```text
q[V^2] = 2 d ln(V^2) / d ln R.
```

Its exact stencil is
`[33.689357475553784,
42.522489842557555] kpc`.
The RMSE instead uses 42 scored radii:

```text
e_i = log10(V_i^2/V_target,i^2),
RMSE^2 = mean_i(e_i^2).
```

Checkpoint 5176's immutable result remains:

```text
mean D_q = -0.0392272547258426;
bootstrap95 D_q =
  [-0.06256573517896083,
   -0.01672942342481484];
exact sign-flip p(D_q) =
  0.01171875;

mean D_RMSE = 0.0006039774233205624 dex;
bootstrap95 D_RMSE =
  [-0.0012737960786308275,
   0.002521414183604568] dex;
exact sign-flip p(D_RMSE) =
  0.560546875;

MTS joint wins = 3;
CDM joint wins = 0;
joint sign p = 0.25.
```

The frozen verdict is therefore
`STATISTICAL_DRAW_OR_METRIC_SPLIT_WITHIN_THIS_LOCKED_FORMATION_GATE`.

## Exact amplitude-shape decomposition

For a positive constant normalization `A`,

```text
e_i(A) = e_i + log10(A),
q[A V^2] = q[V^2],
A_best = 10^(-mean e),
min_A RMSE^2 = Var(e).
```

Thus a constant source or gravity normalization cannot alter q. The
reconstruction verifies this for all 24 profiles with maximum numerical error
`5.81756864903582e-14`.

Across the twelve paired seeds,

```text
mean MTS log residual = -0.2221188237108832 dex;
mean CDM log residual = -0.2216728662459643 dex;

mean MTS centered-shape RMSE =
  0.11944836417592654 dex;
mean CDM centered-shape RMSE =
  0.11899649748138023 dex;

mean Delta MSE(MTS-CDM) = 0.00029622652052732683 dex^2
  = Delta bias^2 0.00019599784333573038
  + Delta centered variance 0.00010022867719160092.
```

The bias-squared contribution is
`0.6616485350022859` of the mean MSE difference and
the centered-shape contribution is
`0.33835146499772917`. Even after granting each
profile its own post-hoc best normalization, MTS has no mean centered-shape
advantage. This diagnostic normalization is not a permitted fit.

The radial identity is also exact:

```text
inner-of-stencil contribution =
  0.0001483585718298592;
q-stencil contribution =
  0.00013516699608762489;
outer-of-stencil contribution =
  1.2700952609843115e-05;
sum = 0.00029622652052732683.
```

The q advantage is therefore a local slope result, not evidence that the
global profile amplitude or centered shape is already solved.

## Constant-coupling no-go survives the ensemble

Let `T` be the transition velocity-squared ratio and `E` the edge mass ratio.
A constant normalization that matches the transition requires `A_tr=1/T`;
one that matches the edge requires `A_edge=1/E`. Across all 24 profiles,

```text
A_tr range =
  [1.996571072859183,
   2.4329313339375127];
A_edge range =
  [0.8319960735500093,
   0.8433622899779304].
```

These ranges are disjoint. For every profile the best log-minimax compromise

```text
A_2anchor = 1/sqrt(T E)
```

still leaves an unavoidable multiplicative mismatch
`sqrt(E/T)` in
`[1.545843908012368,
  1.7025847793359408]`.

Checkpoint 4960 independently fixes the same `G_N=1/(8 pi M_R^2)` in the
Einstein, Poisson, Newton, lensing and matter-source residues and forbids
arena retuning. Checkpoint 5170 already rejected a constant source multiplier
for the earlier formation state. The completed stochastic ensemble strengthens
that result: changing a universal coupling cannot explain the q signal, and a
galaxy-only amplitude fit would both conflict with local calibration and fail
the transition/edge shape test.

## Consequence

The result does not identify a new free coupling. It excludes that shortcut.
The surviving mechanism must be nonmultiplicative and parent-derived: a
conserved, compensated, scale-dependent occupied-state or motion-sector stress
that changes radial structure while remaining silent on the checkpoint-4960
local GR/Newton/Maxwell branch. The classical Vlasov density response rejected
at checkpoint 5171 may not be added again.

Route decision:
`THE_LOCKED_MTS_Q_ADVANTAGE_IS_A_LOCAL_TRANSITION_SLOPE_EFFECT_WHILE_GLOBAL_AMPLITUDE_AND_CENTERED_SHAPE_REMAIN_UNRESOLVED_AND_NO_CONSTANT_SOURCE_NORMALIZATION_CAN_MATCH_TRANSITION_AND_EDGE_OR_REPLACE_THE_CALIBRATED_GN_RETURN_TO_A_PARENT_DERIVED_NONMULTIPLICATIVE_CONSERVED_STATE_STRESS_BEFORE_A_NEW_PREREGISTERED_GATE`.

The next theory calculation must return to the parent motion-sector
Hessian/current and derive such an operator, or prove that the current
occupied-state branch cannot supply one. Only after that derivation may a new
cross-galaxy discrimination gate be preregistered. No parameter may be fitted
to this UGC09133 residual.

## Audit

All `22/22` validations
pass. The 5176 tree is unchanged at
`254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b`. The protected
`formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. Every new row remains
`valid_for_claim=false`, and no GitHub action occurred.
