# 277 - Domain Free-Boundary Euler Equation

Private derivation checkpoint. This is not a public local-GR, CMB, BAO, or unified-field claim.

## Purpose

Checkpoint 276 derived the coherent projector for a fixed domain:

```text
P_coh[Q]^i_j = (1/3)<Tr Q>_D delta^i_j.
```

The remaining problem was the physical domain itself:

```text
derive D, or admit the local branch still uses a closure.
```

This checkpoint varies the domain boundary directly for the current best selector:

```text
C_coh[D] =
<theta>_D^2 /
(<theta^2>_D + <sigma^2>_D + <omega^2>_D + eps_D).
```

## Machine Artifact

Script:

```text
scripts/domain_free_boundary_Euler_equation.py
```

Run:

```text
runs/20260601-000095-domain-free-boundary-Euler-equation
```

Status:

```text
Ccoh_free_boundary_Euler_equation_derived_but_degenerate_domain_not_parent_selected
```

Claim ceiling:

```text
domain_shape_derivative_derived_no_domain_selection_or_local_GR_promotion
```

## Shape Derivative

For a domain average:

```text
<f>_D = V_D^-1 integral_D f dV
```

and an outward normal boundary displacement `eta`:

```text
delta_eta V_D = integral_boundaryD eta dSigma
```

the average varies as:

```text
delta_eta <f>_D =
V_D^-1 integral_boundaryD eta (f - <f>_D) dSigma.
```

Set:

```text
a = <theta>_D
b = <R>_D
R = theta^2 + sigma^2 + omega^2 + eps_D
C_coh = a^2 / b.
```

Then:

```text
delta_eta C_coh =
V_D^-1 integral_boundaryD eta [
  (2a/b)(theta-a)
  - (a^2/b^2)(R-b)
] dSigma.
```

That is the clean result. The boundary problem is now explicit.

## Euler Condition

For arbitrary boundary displacement:

```text
(2a/b)(theta-a) - (a^2/b^2)(R-b) = 0
```

on `boundary D`.

For `a != 0`, this can be written:

```text
2b(theta-a) - a(R-b) = 0.
```

With a fixed-volume constraint:

```text
(2a/b)(theta-a) - (a^2/b^2)(R-b) = lambda.
```

So yes:

```text
the free-boundary Euler equation has been derived.
```

But this is not yet enough.

## Degeneracy Problem

The branches we most need are exactly the degenerate ones.

For FLRW:

```text
theta = a
R = b
```

everywhere, so the boundary integrand vanishes for any comoving homogeneous domain.

That means:

```text
FLRW is stationary, but not uniquely selected.
```

For stationary local systems:

```text
a = <theta>_D = 0
```

so:

```text
delta C_coh = 0
```

at first order.

That means:

```text
local scalar silence is stationary, but not uniquely selected.
```

This is the central result:

```text
the Euler equation exists, but it is too degenerate to own D by itself.
```

## Branch Readout

| Branch | Euler readout | Verdict |
|---|---|---|
| FLRW | boundary integrand zero | stationary but not unique |
| Minkowski / inertial local | `a=0` degeneracy | silent but not selected |
| stationary bound system | first variation vanishes if `<theta>=0` | conditional local silence |
| tracefree shear | scalar channel remains zero | not selected into memory |
| collapse / merger | nontrivial boundary balance | dynamic branch open |
| virialized galaxy | averaged trace may vanish | not a binding derivation |

This is a useful derivation, but not the full domain theorem.

## What This Proves

| Item | Status |
|---|---|
| shape derivative of `C_coh[D]` | derived |
| free-boundary Euler equation | derived |
| FLRW is an extremal domain class | yes, degenerate |
| stationary local systems are extremal/silent | yes, degenerate |
| physical domain selected uniquely | no |
| quiet-domain hand choice removed | not yet |
| Bianchi/boundary exchange closed | no |

## Decision

The result is good but not sufficient.

We can now say:

```text
the domain selector problem is not vague anymore.
```

But we cannot say:

```text
the physical domain D is derived.
```

The free-boundary equation admits the desired local and FLRW branches, but it does not choose them uniquely. To promote the branch, the parent theory still needs an admissible-domain principle:

```text
which boundaries are allowed,
which relative class they carry,
and how boundary exchange conserves stress-energy.
```

Without that, the branch remains:

```text
effective closure with a derived fixed-D projector and a derived but degenerate Euler condition.
```

## Output Files

```text
runs/20260601-000095-domain-free-boundary-Euler-equation/results/source_register.csv
runs/20260601-000095-domain-free-boundary-Euler-equation/results/shape_derivative.csv
runs/20260601-000095-domain-free-boundary-Euler-equation/results/euler_conditions.csv
runs/20260601-000095-domain-free-boundary-Euler-equation/results/branch_tests.csv
runs/20260601-000095-domain-free-boundary-Euler-equation/results/gate_results.csv
runs/20260601-000095-domain-free-boundary-Euler-equation/results/route_policy.csv
runs/20260601-000095-domain-free-boundary-Euler-equation/results/decision.csv
```

## Next Step

Next target:

```text
278 - Admissible Domain Class / Boundary Current Owner
```

Attempt:

```text
derive which boundary displacements eta are admissible from a relative current,
Noether identity, or boundary class condition.
```

The acceptance condition is brutal:

```text
the rule must break the Euler degeneracy without adding a fitted smoothing scale
or a new surface-tension stress.
```

