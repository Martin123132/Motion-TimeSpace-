# 5342 - D4 E00125 generic support-endpoint normal form

Date: `2026-08-10`

Marker: `MTS_5342_D4_E00125_GENERIC_SUPPORT_ENDPOINT_NORMAL_FORM`.

## Executive result

Checkpoint 5342 derives the parent-owned affine complex-log normal form for
all four `E00125` support contacts:

```text
E01, E02, E03 = SUPPORT_ENTRY,
E08           = SUPPORT_EXIT.
```

Each contact is a lower-boundary term of the exact material-pole primitive

```text
I_p = mu R [Log(E_U-p)-Log(E_L-p)].
```

Thus, with `delta=x-x0`, each fast contribution has the same derived form

```text
I_fast(delta)
 = -(C0+C1 delta) Log(z0+z1 delta),
z = E_L-p.
```

All `20/20` direct parent Laurent fits pass.  The four independently derived
coefficient contracts pass, as do all `12/12` checkpoint gates.  This closes
the coefficient/input problem for the E00125 endpoint subtraction; it does
not yet claim the fixed-decay integral.

## 1. Adaptive stencil derivation

The first uniform quarter-boundary-scale stencil exposed one unstable
inside-support half-step at every contact.  The repeated pattern was numerical:
the same near-boundary Laurent-fit location failed while the center and more
distant points passed.  No tolerance was relaxed.

The stencil was expanded using only source fits that already passed:

```text
E01, E02: full boundary-layer scale,
E03, E08: half boundary-layer scale.
```

Previously accepted center and half-step evaluations were reused by exact
coordinate identity; only the new outer evaluations were computed.  The final
one-sided trace mismatches are

```text
event   gap z0 mismatch       coefficient C0 mismatch
E01     6.765387355e-8        5.002635438e-8
E02     2.863742129e-8        6.211808636e-7
E03     3.988797820e-6        7.007202660e-6
E08     4.091723812e-7        1.366798888e-6
```

All remain below the unchanged `1.0e-5` trace limit.  Full-step/half-step
coefficient derivatives also pass the unchanged `2.5e-2` stability limit;
the maximum is `0.01752217981725521`.

## 2. Selector and regulator checks

At every exact contact, the discrete support selector suppresses the residue.
The independently agreeing one-sided traces remain nonzero.  All four centers
are therefore classified as

```text
MASK_SUPPRESSED_MEASURE_ZERO.
```

The exact-point selector is not substituted for the one-sided integral trace.
Every complex endpoint gap remains nonzero and regulator-resolved relative to
the `1.0e-11` event-coordinate error.

The derived boundary-layer scales are

```text
E01 = 3.6791106455283004e-6,
E02 = 9.819658441953708e-7,
E03 = 8.382226746255886e-7,
E08 = 1.956245511578858e-6.
```

## 3. Generic exact primitive

For a lower or upper support boundary, define `s=-1` or `s=+1` and

```text
I_fast(delta)=s(C0+C1 delta) Log(z0+z1 delta).
```

Writing

```text
B=C1/z1,
A=C0-B z0,
```

gives

```text
P(z)=s/z1 {
  A[z Log(z)-z]
  +B[(z^2/2)Log(z)-z^2/4]
}.
```

Hence any event-adjacent interval `[a,b]` has exact model integral

```text
P(z0+z1 b)-P(z0+z1 a).
```

Finite-difference differentiation of this generic primitive reproduces the
integrand at maximum relative error `2.26862965267203e-11`, far below the
`2.5e-6` gate.

## 4. Conservative coordinate term

Each event carries the explicit sensitivity

```text
E_x,event = |C0| |z1/z0| Delta x0.
```

The four-event linear sum is

```text
0.001319687531993736.
```

This term must be added to the E00125 outer and inner numerical errors.  It is
not hidden in the central value and cannot be omitted by the runner.

## 5. Claim boundary

The following narrow flag is true:

```text
valid_for_D4_E00125_support_endpoint_coefficients = true.
```

The fixed-decay E00125 integral, regulator-zero limit, decay-angle integral,
phase-space coefficient, UV, local-GR and full-MTS claims remain false.

## 6. Artifacts and next action

The checkpoint artifacts are

```text
scripts/Y5_R2FR_5342_D4_E00125_generic_support_endpoint_normal_form.py
source-intake/functional_rg/5342/D4_E00125_support_endpoint_stencil.csv
source-intake/functional_rg/5342/D4_E00125_support_endpoint_coefficients.csv
source-intake/functional_rg/5342/D4_E00125_support_endpoint_normal_form_result.json
source-intake/functional_rg/5342/source_register.csv
source-intake/mts_residuals/P8_Y5_BRR545_5342_VALIDATION.csv
```

Next, wrap the parent adaptive panel evaluator with an exact add-and-subtract
endpoint correction.  A correction may be selected only when it improves the
raw Q4/Q8 result, its regular remainder passes, and its affine gap path does
not cross the principal-log cut.  Run one BelowNormal worker in resumable
four-hour chunks without changing the local `0.005` or global `0.01` gates.

No GitHub action is taken.  The protected `formalization-workbench` digest is
unchanged.
