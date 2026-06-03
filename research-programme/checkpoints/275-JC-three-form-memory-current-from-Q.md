# 275 - `J_C` Three-Form Memory Current from `Q`

Private derivation checkpoint. This is not a public local-GR, CMB, BAO, or unified-field claim.

## Purpose

Checkpoint 274 identified the best live route:

```text
lift the scalar C-sector into a domain 3-form / boundary-class memory current.
```

The danger was obvious:

```text
J_C could just become a newly named repair field.
```

This checkpoint asks whether `J_C` can instead be built from the already-existing MTS load geometry:

```text
Q^i_j
det(Q)
coherent domain volume load
```

## Machine Artifact

Script:

```text
scripts/JC_three_form_memory_current_from_Q.py
```

Run:

```text
runs/20260601-000093-JC-three-form-memory-current-from-Q
```

Status:

```text
JC_three_form_has_conditional_kinematic_Q_origin_not_parent_action_projector_and_domain_still_closure
```

Claim ceiling:

```text
shape_origin_strengthened_no_local_GR_or_unification_promotion
```

## Main Result

`J_C` does not have to be an independent magic field.

There is a conditional kinematic construction:

```text
N_D = (1/3) ln(V_D0 / V_D)
Q_coh^i_j = (N_D / u3) delta^i_j
J_C = det(Q_coh) Omega_D / V_D
```

Therefore:

```text
integral_D J_C = det(Q_coh) = (N_D / u3)^3.
```

This means the cubic law is no longer just inserted if the coherent-domain route is accepted:

```text
p = 3
```

comes from the determinant / volume form of a 3D spatial domain.

That is a real strengthening.

But it is conditional, not a completed parent-action derivation.

## FLRW Reduction

For FLRW:

```text
V_D proportional a^3
N_D = (1/3) ln(V_D0 / V_D) = ln(a0/a) = N
```

so:

```text
Q_coh^i_j = (N/u3) delta^i_j
integral_D J_C = (N/u3)^3
F_D = 1 - exp[-(N/u3)^3].
```

The endpoint regularity follows immediately:

```text
F_D(0) = 0
F_D'(0) = 0
F_D''(0) = 0
```

and:

```text
d/dN integral_D J_C = 3N^2/u3^3
```

so the current has the double zero:

```text
J_M(0) = 0
J_M'(0) = 0.
```

## The Local-Silence Catch

The full unprojected determinant is not locally safe.

For:

```text
Q = X I + S
Tr(S) = 0
```

the determinant expands as:

```text
det(X I + S) = X^3 - (X/2) Tr(S^2) + det(S).
```

So tracefree shear leaks into unprojected `det(Q)` at second order.

That kills the naive route:

```text
J_C = det(Q) Omega_D / V_D
```

as a local-GR-safe parent object.

The only live version is:

```text
J_C = det(Q_coh) Omega_D / V_D
```

where:

```text
Q_coh
```

means the parent-owned coherent volume-flow projection, not a post-hoc smoothing knob.

## What Was Derived

Within the conditional coherent-domain branch:

| Item | Status |
|---|---|
| `J_C` as independent repair field | avoided |
| `p=3` shape | conditionally derived from 3D determinant / volume form |
| FLRW activation shape | conditionally derived |
| endpoint regularity | derived once `u3` is given |
| stationary local silence | conditional on stable domain volume |
| unprojected local shear silence | failed |

This is better than closure-only, but not promotion.

## What Is Still Missing

The blockers are now sharper:

| Missing piece | Current status |
|---|---|
| physical domain selector `D` | not parent-derived |
| coherent projection `Q -> Q_coh` | not parent-derived |
| boundary primitive / exactness law `delta J_C = dB_C` | not derived |
| `u3 = 1/4` or empirical `u3` | not parent-derived |
| `B_mem = 2/27` | not parent-derived |
| matter coupling `bar_g = exp(B_mem F_D)g` | not parent-derived |

So the win is:

```text
the shape can be owned by geometry.
```

The fail is:

```text
the selector/projection/amplitude/coupling are still not owned by a parent action.
```

## Decision

The route survives, but only as a sharpened theorem target.

The current status is:

```text
conditional kinematic origin for J_C;
no parent-action promotion;
projector and domain still closure/theorem targets.
```

This is not grim. It is actually cleaner than the previous state:

```text
we no longer need to invent a 3-form by hand,
but we do need to derive the coherent-domain projector honestly.
```

In boxing terms: not a knockout, but we slipped the worst punch. The opponent now has to answer one very specific counter:

```text
derive D and Q_coh from the parent motion-time-space variables.
```

## Output Files

```text
runs/20260601-000093-JC-three-form-memory-current-from-Q/results/source_register.csv
runs/20260601-000093-JC-three-form-memory-current-from-Q/results/construction_candidates.csv
runs/20260601-000093-JC-three-form-memory-current-from-Q/results/determinant_audit.csv
runs/20260601-000093-JC-three-form-memory-current-from-Q/results/derivation_chain.csv
runs/20260601-000093-JC-three-form-memory-current-from-Q/results/gate_results.csv
runs/20260601-000093-JC-three-form-memory-current-from-Q/results/numeric_locks.csv
runs/20260601-000093-JC-three-form-memory-current-from-Q/results/decision.csv
```

## Next Step

Next target:

```text
276 - Coherent Domain Projector from Parent Variables
```

Attempt:

```text
derive the domain selector and Q_coh projection from an action / variational stability rule,
not from "choose the quiet domain".
```

Acceptance condition:

```text
stationary bound systems select trivial class;
FLRW selects nonzero coherent expansion class;
tracefree local shear does not leak into J_C;
no tuned smoothing scale enters.
```

