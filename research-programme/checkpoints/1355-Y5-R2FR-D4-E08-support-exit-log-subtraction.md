# 5339 - D4 E08 support-exit logarithm subtraction

Date: `2026-08-10`

Marker: `MTS_5339_D4_E08_SUPPORT_EXIT_LOG_SUBTRACTION`.

## Executive result

Checkpoint 5339 derives and tests the source-owned endpoint subtraction that
checkpoint 5338 required.  It does not raise the adaptive depth and does not
relax the local `0.5%` or global `1%` numerical gates.

The parent material-simple-pole energy primitive is

```text
I_p(x)=mu R(x)[Log(E_U(x)-p(x))-Log(E_L(x)-p(x))].
```

At support-exit event `E08`, the rapidly varying term is therefore the lower
logarithm already present in the parent integrator.  Five direct parent fits
around the source-derived crossing establish its one-sided coefficient and
complex gap.  Subtracting this logarithm from the saved Q4/Q8 outer nodes and
restoring its exact analytic outer primitive changes the target-panel
disagreement from

```text
raw P12S02LLLL Q4/Q8 change       = 0.006405449614157091
log-subtracted reconstructed change = 1.7328781112775346e-5.
```

The unchanged local limit is `0.005`, so the endpoint method passes by a
factor of about `288`.  The regular remainder itself has Q4/Q8 relative change

```text
2.41360507907169e-6.
```

All `15/15` checkpoint gates pass.  This validates the E08 parent endpoint
coefficients and logarithmic subtraction method.  The full finite `E0025`
rung remains non-claim until the method is integrated into and canonicalized
by the parent D4 engine.

## 1. Parent endpoint traces

The event coordinate and regulator-scale complex gap are

```text
x0 = 0.8708639328146937,
z0 = E_L(x0)-p(x0)
   = -7.77140946039978e-9 - 1.3713700792385614e-4 i.
```

The five source evaluations use offsets

```text
-h, -h/2, 0, +h/2, +h,
h = 9.77362038362816e-7.
```

Every Laurent fit satisfies the parent fit-residual, residue-scale,
second-order suppression and mask-identity contracts.  The independently
extrapolated left and right traces agree at

```text
lower-gap trace relative mismatch    = 2.123513428451736e-9,
coefficient trace relative mismatch  = 9.846291845134188e-10.
```

Their averaged source-owned coefficients are

```text
z1 = d(E_L-p)/dx at x0
   = 35.05105469756951 - 0.021504993382700874 i,

C0 = lim[x->x0+ or x0-] mu R(x)
   = -173.66882781327922 + 0.44369081371557983 i,

C1 = d(mu R)/dx at x0
   = -62902.91789041482 + 169.77412640827592 i.
```

Full-step and half-step derivatives agree to

```text
z1 relative change = 4.250333771974738e-9,
C1 relative change = 1.3907150643325776e-6.
```

These numbers are produced by the parent pole geometry and unmasked Laurent
evaluator.  They are not fitted to the final outer integral.

## 2. The exact-crossing selector is not the trace

At exactly `x=x0`, the discrete mask selector returns an almost-zero residue.
Its magnitude relative to the agreed one-sided trace is

```text
2.4101560060486643e-13.
```

All four nonzero-offset evaluations instead converge smoothly to the same
nonzero coefficient.  The exact-point selector is therefore a measure-zero
mask convention at the crossing, not the limit entering an integral.  Using
it would contradict both one-sided parent traces and would erase the material
pole at one point only.

Checkpoint 5339 does not choose a preferred side by hand.  It requires the
left and right extrapolated traces to agree before averaging them.  Failure of
that gate would block the subtraction.

## 3. Derived affine logarithmic normal form

With `delta=x-x0`, the parent endpoint trace gives

```text
C(delta)=C0+C1 delta,
z(delta)=z0+z1 delta,
I_fast(delta)=-C(delta) Log[z(delta)].
```

Define

```text
A=C0-C1 z0/z1,
B=C1/z1.
```

Since `C(delta)=A+B z(delta)`, an exact primitive is

```text
P(z)=-(1/z1) {
       A [z Log(z)-z]
       + B [(z^2/2)Log(z)-z^2/4]
     }.
```

Therefore

```text
Integral_0^H I_fast(delta) ddelta
 = P(z0+z1 H)-P(z0).
```

The nonzero imaginary regulator gap keeps the integration path away from the
logarithmic branch point.  The resulting boundary-layer scale is

```text
|Im z0|/|Re z1| = 3.91249305069743e-6.
```

The subtraction is an exact add-and-subtract identity.  Linearization error
does not bias the integral: whatever part of the parent integrand is not
captured by `I_fast` remains in the numerically integrated regular remainder.
The Q4/Q8 gate directly tests whether that remainder is smooth enough.

## 4. Reconstructed target panel

The saved raw target-panel values are reproduced with zero recorded relative
error.  The decomposition is

```text
order  raw panel                 quadrature model             regular remainder
Q4     -0.5473984694019233       -4.454038199845243            3.90663973044332
       -0.004002132149858013 i   +0.003580278461780977 i       -0.007582410611638989 i

Q8     -0.543905244649969        -4.450554402708987            3.906649158059018
       -0.004306124455927323 i   +0.003276454914637563 i       -0.007582579370564887 i.
```

The exact analytic model integral is

```text
-4.450756260869756 + 0.0036220272279599555 i.
```

Adding that exact value to each regular quadrature gives

```text
reconstructed Q4 = -0.5441165304264364 - 0.003960383383679034 i,
reconstructed Q8 = -0.544107102810738  - 0.003960552142604931 i.
```

Their relative change is `1.7328781112775346e-5`.  The Q8 quadrature error of
the removed model is independently `8.991921049395414e-5`, confirming that
the subtraction removes the feature that the old nested rule was resolving
unevenly.

## 5. Corrected diagnostic budget

Replacing only the blocked target leaf by the reconstructed Q8 diagnostic
would give

```text
fixed-decay integral real       = 5.719956341116533,
fixed-decay integral imaginary  = 6.488343298361512,
total relative conservative error = 0.002583738511344648.
```

This remains below the global `0.01` limit after adding the event-coordinate
sensitivity bound.  It is not yet written into the checkpoint-5334 canonical
result.  That deliberate separation prevents a method smoke test from
silently promoting a parent numerical claim.

## 6. Claim boundary

Checkpoint 5339 sets only

```text
valid_for_E08_parent_endpoint_coefficients = true,
valid_for_E08_log_subtraction              = true.
```

It keeps false

```text
valid_for_D4_outer_E0025_fixed_decay_integral;
valid_for_D4_outer_regulator_zero_limit;
valid_for_decay_angle_integral;
valid_for_full_angular_convergence;
valid_for_full_phase_space_coefficient;
valid_for_numeric_UV_claim;
valid_for_local_GR_claim;
valid_for_full_MTS_claim.
```

No GitHub action is taken and the protected `formalization-workbench` digest
is unchanged.

## 7. Artifacts and next action

The checkpoint artifacts are

```text
scripts/Y5_R2FR_5339_D4_E08_support_exit_log_subtraction.py
source-intake/functional_rg/5339/E08_parent_endpoint_coefficient_stencil.csv
source-intake/functional_rg/5339/E08_parent_endpoint_coefficients.csv
source-intake/functional_rg/5339/E08_log_subtraction_node_audit.csv
source-intake/functional_rg/5339/E08_log_subtracted_quadrature.csv
source-intake/functional_rg/5339/D4_E08_support_exit_log_subtraction_result.json
source-intake/mts_residuals/P8_Y5_BRR545_5339_VALIDATION.csv
```

The next action is to integrate the validated affine-log subtraction into the
parent E0025 adaptive engine, canonicalize the complete D4 result, and rerun
all parent and checkpoint gates before promoting the single finite-regulator
fixed-decay claim.
