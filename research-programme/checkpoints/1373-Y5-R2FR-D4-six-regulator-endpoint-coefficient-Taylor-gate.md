# 5357: D4 six-regulator endpoint-coefficient Taylor gate

Date: `2026-08-11`

Marker: `MTS_5357_D4_SIX_REGULATOR_ENDPOINT_COEFFICIENT_TAYLOR_GATE`.

## Result

Six independently accepted all-eight endpoint-log coefficient disks are now
available:

```text
epsilon = 0.000625, 0.00125, 0.0025, 0.005, 0.01, 0.02.
```

The source-derived coefficient family

```text
A(epsilon)
 = A0
 + A1 (epsilon/0.0025)
 + A2 (epsilon/0.0025)^2
 + O(epsilon^3)
```

is overdetermined by three complex residual degrees of freedom. The selected
inverse-disk-weighted quadratic fit gives

```text
A0 = 1.9794425833767675e-06
     + 0.4707373916054135 i;

input-disk propagation radius = 3.204621177211857e-06;
maximum normalized complex residual = 0.791311949593891.
```

Every selected-model residual therefore lies inside its input disk.

## Conservative intercept envelope

The checkpoint inherits the six diagnostics and `1%` threshold frozen in
checkpoint 5345. It adds, rather than maximizes, the following same-unit
contributions:

```text
largest analytic-fit input-disk propagation;
weighted/unweighted quadratic intercept shift;
six leave-one-out intercept shifts;
smallest-four-epsilon window shift;
affine/quadratic intercept shift;
largest selected-model absolute residual.
```

The resulting conservative radius and relative envelope are

```text
r_envelope = 1.9201925077212943e-05;
r_envelope / |A0| = 4.079116173787788e-05.
```

This is about 245 times below the frozen `1%` ceiling. The intercept envelope
also excludes zero by a wide margin. These are true finite-ladder stability
results.

## Model-boundary correction

Checkpoint 5345 derives the five-complex-parameter family

```text
I_D4(epsilon)
 = I0
 + A epsilon Log(epsilon/epsilon_ref)
 + B epsilon
 + C epsilon^2 Log(epsilon/epsilon_ref)
 + D epsilon^2
 + O(epsilon^3 Log epsilon)
```

for the integrated D4 quantity. The six values acquired in checkpoints
5346--5356 are endpoint-log coefficients, not integrated `I_D4` values. This
checkpoint therefore does not feed coefficient rows into the 5345 integral
family. Instead it derives the appropriate coefficient Taylor family from

```text
A_e(epsilon)
 = -s_e C0_e(epsilon) z0_e(epsilon)
   / [epsilon z1_e(epsilon)].
```

If `z0_e/epsilon`, `C0_e` and `1/z1_e` are analytic at zero, the displayed
quadratic coefficient family follows. This removes a category error that
would otherwise have produced a formally impressive but invalid fit.

## Half-power falsifier

The topology-excluded half-power diagnostic also fits the present disks:

```text
maximum normalized complex residual = 0.9483830786364228.
```

Consequently the six numerical rows alone do not distinguish the analytic
and half-power families. The analytic family is selected only by the simple,
transverse parent-root topology; it is not selected because it fits better.

## Provenance boundary

All six top-level coefficient results, validation tables and direct source
hashes are current. Strict recursive traversal is current for `E000625`,
`E00125` and `E005`. The refined `E0025`, `E010` and `E020` chains inherit the
same three older recursive records:

```text
stale checkpoint-5297 script hash;
stale checkpoint-5297 result hash;
legacy dictionary-form source_files in checkpoint-5224 frozen config.
```

The exact failures are recorded in the input ledger and result JSON. They are
not hidden or relabelled current. The accepted refined coefficients rely on
their current direct source chains and independently passing refinement/event
geometry validations.

## Claim boundary

The following finite-ladder claims are true:

```text
valid_for_D4_six_regulator_quadratic_endpoint_coefficient_stability;
valid_for_D4_six_regulator_nonzero_endpoint_intercept_diagnostic.
```

The following remain false:

```text
valid_for_D4_endpoint_coefficient_regulator_zero_limit;
valid_for_D4_integral_six_rung_complete_second_order_fit;
valid_for_D4_outer_regulator_zero_limit;
valid_for_decay_angle_integral;
valid_for_full_angular_convergence;
valid_for_full_phase_space_coefficient;
valid_for_numeric_UV_claim;
valid_for_local_GR_claim;
valid_for_full_MTS_claim.
```

The remaining coefficient-limit obstruction is no longer poor regulator
stability. It is the unsigned zero-regulator collision/event Jacobian required
by the analytic implicit-function theorem.

Decision:

```text
D4_SIX_RUNG_COEFFICIENT_TAYLOR_STABILITY_PASSES__PROVE_ZERO_COLLISION_JACOBIAN
```

## Artifacts

```text
scripts/Y5_R2FR_5357_D4_six_regulator_coefficient_taylor_gate.py
source-intake/functional_rg/5357/D4_six_regulator_coefficient_inputs.csv
source-intake/functional_rg/5357/D4_coefficient_integral_model_boundary_contract.csv
source-intake/functional_rg/5357/D4_six_regulator_coefficient_models.csv
source-intake/functional_rg/5357/D4_six_regulator_coefficient_residuals.csv
source-intake/functional_rg/5357/D4_six_regulator_coefficient_leave_one_out.csv
source-intake/functional_rg/5357/D4_six_regulator_intercept_envelope.csv
source-intake/functional_rg/5357/D4_six_regulator_coefficient_validation.csv
source-intake/functional_rg/5357/D4_six_regulator_coefficient_result.json
source-intake/functional_rg/5357/source_register.csv
source-intake/functional_rg/5357/status.json
```

No GitHub action is taken.
