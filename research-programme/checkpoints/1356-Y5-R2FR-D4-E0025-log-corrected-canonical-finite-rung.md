# 5340 - D4 E0025 log-corrected canonical finite rung

Date: `2026-08-10`

Marker: `MTS_5340_D4_E0025_LOG_CORRECTED_CANONICALIZER`.

## Executive result

Checkpoint 5340 integrates the checkpoint-5339 source-owned E08 affine-log
subtraction into the complete checkpoint-5334 D4 outer leaf aggregation.  It
does so non-destructively: the historical raw checkpoint-5334 result remains
unchanged and non-claim, while the corrected canonical result is owned by this
checkpoint.

All `456/456` parent nodes remain complete inner-integral passes.  Exactly one
of the `32` adaptive leaves receives the validated correction.  Its local
Q4/Q8 relative change becomes

```text
P12S02LLLL = 1.7328781112775346e-5
limit       = 5.0e-3.
```

All `32/32` corrected leaves pass.  The complete canonical finite-regulator
value is

```text
I_D4(E0025; D4_OUTER)
 = 5.719956341116534 + 6.488343298361512 i,
|I| = 8.649653131870203.
```

Its conservative budget is

```text
outer Q4/Q8 error                 = 0.02126635857895909,
inner-energy error                = 0.0009969177859975975,
event-coordinate sensitivity     = 8.51655416291934e-5,
total absolute error              = 0.022348441906585883,
total relative error              = 0.002583738511344647.
```

The unchanged global limit is `0.01`.  All `14/14` checkpoint gates pass, so
the single D4 `E0025`, fixed-decay, finite-regulator rung is accepted.

This does not establish a regulator-zero limit or any broader theory claim.

## 1. Aggregation identity

The parent engine defines the complete high-order value and conservative
errors by

```text
I_high  = Sum over adaptive leaves of I_leaf,Q8,
E_outer = Sum over leaves of |I_leaf,Q8-I_leaf,Q4|,
E_inner = Sum over leaves of E_leaf,inner.
```

Checkpoint 5340 reproduces the saved raw parent values before applying a
correction:

```text
raw leaf-sum versus parent-result relative mismatch = 0.0.
```

It then applies the exact replacement identity

```text
I_corrected
 = I_raw - I_raw,target,Q8 + I_log-corrected,target,Q8.
```

An independent direct sum over all corrected leaf rows agrees with this
identity at relative error `1.0268370374617391e-16`.  It also agrees with the
checkpoint-5339 predicted complete value at the same level.

## 2. Single-leaf correction

The only modified leaf is

```text
adaptive_panel_id = P12S02LLLL,
event              = E08 SUPPORT_EXIT,
method             = E08_PARENT_AFFINE_COMPLEX_LOG_SUBTRACTION.
```

Its reconstructed panel values are

```text
Q4 = -0.5441165304264364 - 0.003960383383679034 i,
Q8 = -0.544107102810738  - 0.003960552142604931 i.
```

The absolute Q4/Q8 difference is `9.429126010956964e-6`.  All inner nodes and
the exact change-of-variables gate remain unchanged and pass.  The other `31`
leaf rows are copied without numerical alteration.

## 3. Conservative event-coordinate term

The old parent budget did not include uncertainty from the source-derived
support-exit coordinate.  Checkpoint 5340 adds

```text
E_event = |C0| |z1/z0| Delta x0
        = 8.51655416291934e-5,
```

using the parent event-coordinate error and the checkpoint-5339 endpoint
trace.  This term is added linearly to the outer and inner conservative
errors; it is not hidden inside the central value.

## 4. Acceptance and claim boundary

The following narrow flag is true:

```text
valid_for_D4_outer_E0025_fixed_decay_integral = true.
```

The following remain false:

```text
valid_for_D4_outer_regulator_zero_limit;
valid_for_decay_angle_integral;
valid_for_full_angular_convergence;
valid_for_full_phase_space_coefficient;
valid_for_numeric_UV_claim;
valid_for_local_GR_claim;
valid_for_full_MTS_claim.
```

One accepted finite-regulator value cannot establish a regulator limit.  The
raw checkpoint-5334 artifacts also remain non-claim so their unresolved
historical method is not silently rewritten.

## 5. Validation evidence

The acceptance gates prove

```text
all source paths exist and are hashed;
all checkpoint-5339 method gates pass;
the raw parent aggregation is exactly reproduced;
all 456 parent nodes pass;
exactly one leaf is corrected;
the corrected target passes the unchanged local gate;
all 32 corrected leaves pass;
the two complete-value reconstruction identities pass;
the corrected global budget passes;
only the narrow finite-rung claim is promoted;
all broader claims remain false;
the historical parent remains non-claim;
the formalization-workbench digest is unchanged;
no Python cache is left behind.
```

## 6. Artifacts and next action

The checkpoint artifacts are

```text
scripts/Y5_R2FR_5340_D4_E0025_log_corrected_canonicalizer.py
source-intake/functional_rg/5340/D4_E0025_log_corrected_adaptive_panels.csv
source-intake/functional_rg/5340/D4_E0025_log_corrected_leaf_audit.csv
source-intake/functional_rg/5340/D4_E0025_log_corrected_aggregation.csv
source-intake/functional_rg/5340/D4_E0025_log_corrected_finite_value.csv
source-intake/functional_rg/5340/D4_E0025_log_corrected_canonical_result.json
source-intake/mts_residuals/P8_Y5_BRR545_5340_VALIDATION.csv
```

The next target is the adjacent regulator `E00125`.  The endpoint subtraction
must be generalized from the E08 labels to any source-derived support-entry or
support-exit event before that run.  A second accepted rung is required before
any regulator-trend statement, and at least four accepted rungs remain
required for an overdetermined D4 contrast.

No GitHub action is taken.
