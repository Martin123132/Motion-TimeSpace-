# 5349 - D4 three-regulator affine endpoint-coefficient gate

Date: `2026-08-11`

Marker: `MTS_5349_D4_THREE_REGULATOR_AFFINE_ENDPOINT_COEFFICIENT_GATE`.

## Result

The source-current all-eight endpoint-log coefficients are now available at
three finite regulators:

```text
A_E000625 = 0.00018863965656809473 + 0.47073737469194127 i,
r_E000625 = 4.543149992017568e-06;

A_E00125  = 0.00038006208677709226 + 0.47073718025727357 i,
r_E00125  = 2.8629739714438195e-06;

A_E005    = 0.0015055630379978706  + 0.4707349218820557 i,
r_E005    = 1.4207727216529068e-06.
```

The pairwise diagnostic disks are too narrow to overlap, so pairwise overlap
is not used as a false equality test. Instead this checkpoint tests the exact
three-rung consequence of a finite-regulator affine law.

## 1. Affine contrast

Let `h = 0.000625`. For

```text
A(epsilon) = A0 + c epsilon,
```

the values at `h`, `2h` and `8h` obey

```text
C_A = 6 A(h) - 7 A(2h) + A(8h) = 0.
```

The measured contrast and conservative propagated disk are

```text
C_A = -2.3033630033207023e-05 - 1.0917672114141297e-06 i;
|C_A| = 2.305948976344827e-05;
r_C = 4.872049047386505e-05;
|C_A| / r_C = 0.47330167531498857.
```

Zero lies inside the propagated contrast disk, so the three finite-rung data
are compatible with an affine regulator correction at the stated numerical
resolution.

## 2. Common affine intercept

The independent small-pair and wide-pair affine intercept disks overlap. Their
conservative common disk is

```text
A0,common = -2.7687333198180713e-06 + 0.4707375697921038 i;
r0,common = 1.196333003955526e-05;
|A0,common| = 0.4707375698002462.
```

This disk excludes zero by a wide margin. It is evidence for a nonzero affine
intercept conditional on the finite-rung affine model; it is not yet a theorem
that the coefficient has a regulator-zero limit.

## 3. Provenance and validation

The gate recursively validates every JSON source chain, rather than checking
only the three top-level coefficient files. The regenerated `E005` chain and
the `E000625` and `E00125` chains are source-current. The final result has

```text
8/8 validation gates passed;
all three input validations passed;
exact h, 2h, 8h geometry passed;
recursive source hashes current;
scripts/__pycache__ absent;
formalization-workbench modified-file count = 0.
```

## 4. Claim boundary

Only the following new finite-rung diagnostics are true:

```text
valid_for_D4_three_regulator_affine_endpoint_coefficient_stability;
valid_for_D4_three_regulator_nonzero_affine_endpoint_intercept.
```

The following remain false:

```text
valid_for_D4_endpoint_coefficient_regulator_zero_limit;
valid_for_D4_outer_regulator_zero_limit;
valid_for_decay_angle_integral;
valid_for_full_angular_convergence;
valid_for_full_phase_space_coefficient;
valid_for_numeric_UV_claim;
valid_for_local_GR_claim;
valid_for_full_MTS_claim.
```

## 5. Artifacts and next gate

```text
scripts/Y5_R2FR_5349_D4_three_regulator_endpoint_coefficient_gate.py
source-intake/functional_rg/5349/D4_three_regulator_coefficient_inputs.csv
source-intake/functional_rg/5349/D4_three_regulator_affine_contrast.csv
source-intake/functional_rg/5349/D4_three_regulator_coefficient_result.json
source-intake/functional_rg/5349/D4_three_regulator_coefficient_validation.csv
source-intake/functional_rg/5349/source_register.csv
```

Decision:

```text
D4_THREE_REGULATOR_AFFINE_COEFFICIENT_PASS__ACQUIRE_FOURTH_OR_REMAINDER_BOUND
```

The next honest route is either a source-current fourth coefficient regulator
outside the fitted three-point relation or a derivation of a uniform remainder
bound for `A(epsilon) = A0 + c epsilon + R(epsilon)`. Until one closes, no
regulator-zero coefficient claim is permitted.

## 6. Subsequent fourth-rung holdout

Checkpoints 5350--5354 preregister and evaluate the independent `E0025`
coefficient. All three frozen affine prediction disks contain the measured
coefficient disk; the maximum contrast-radius ratio is
`0.5466276259165949`. Therefore the fourth-rung holdout passes.

This closes the finite four-rung holdout requested here. It does not close the
regulator-zero limit: that still requires a source-derived uniform remainder
bound or two additional regulator rungs for an overdetermined second-order
family.

No GitHub action is taken.
