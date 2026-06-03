# 276 - Coherent Domain Projector from Parent Variables

Private derivation checkpoint. This is not a public local-GR, CMB, BAO, or unified-field claim.

## Purpose

Checkpoint 275 found the exact pressure point:

```text
J_C can be built from coherent domain volume/load,
but only if D and Q_coh are honestly owned.
```

This checkpoint separates two questions that were previously tangled together:

```text
1. Given a physical domain D, can Q_coh be derived from Q?
2. Can the physical domain D itself be derived?
```

The answer is split:

```text
Q_coh can be mathematically derived for fixed D.
D is still not parent-derived.
```

## Machine Artifact

Script:

```text
scripts/coherent_domain_projector_from_parent_variables.py
```

Run:

```text
runs/20260601-000094-coherent-domain-projector-from-parent-variables
```

Status:

```text
fixed_D_Qcoh_projection_mathematically_derived_domain_selector_not_parent_derived
```

Claim ceiling:

```text
coherent_projection_sharpened_domain_selection_open_no_local_GR_promotion
```

## Fixed-Derivation Result

For a fixed domain `D`, take the accumulated load tensor:

```text
Q^i_j(x)
```

and project it onto the coherent isotropic subspace:

```text
S_D = { q delta^i_j : q is constant on D }.
```

Use the natural domain norm:

```text
E_D(q) = < || Q - q I ||^2 >_D.
```

Varying `q` gives:

```text
dE_D/dq = 0
```

so:

```text
q = (1/3) < Tr Q >_D.
```

Therefore:

```text
P_coh[Q]^i_j = (1/3) < Tr Q >_D delta^i_j.
```

That is a clean result:

```text
Q_coh is not arbitrary once D and the projection norm are given.
```

## Why This Matters

Checkpoint 275 found that unprojected `det(Q)` leaks tracefree shear:

```text
Q = X I + S
Tr(S) = 0
det(XI+S) = X^3 - (X/2)Tr(S^2) + det(S).
```

The fixed-`D` coherent projection removes that channel:

```text
P_coh[S] = 0
```

because tracefree shear is orthogonal to the isotropic constant subspace.

So the repaired `J_C` branch is:

```text
J_C = det(P_coh[Q]) Omega_D / V_D
```

not:

```text
J_C = det(Q) Omega_D / V_D.
```

This is a meaningful derivation step.

## Branch Readout

| Branch | Readout | Status |
|---|---|---|
| FLRW | `P_coh[Q]=Q=(N/u3)I` | pass conditional |
| Minkowski/inertial | `<Tr Q>_D=0` | pass conditional |
| stationary solar system | stable-volume `D` gives `P_coh[Q]=0` | conditional, not promoted |
| tracefree shear/GW | tracefree part removed by projection | projection passes, domain still open |
| collapse/merger | coherent trace can activate | open dynamic branch |
| virialized galaxy | averaged trace may vanish; galaxy pillar separate | open conditional |

This does not derive local GR.

It does remove one major local-hair mechanism from the projected branch.

## The Remaining Failure

The domain itself is still the hard problem.

The best live candidate remains:

```text
C_coh[D] =
<theta>_D^2 /
(<theta^2>_D + <sigma^2>_D + <omega^2>_D + eps_D).
```

This has the right classifier behaviour:

```text
FLRW -> high coherent expansion
stationary local systems -> low scalar volume channel
tracefree shear -> low scalar volume channel
```

But varying the domain gives:

```text
delta_D C_coh[D] = bulk average terms + boundary terms.
```

Those boundary terms are not yet closed by a parent Euler equation.

So:

```text
D is still a closure/theorem target.
```

## What Was Gained

| Piece | Status |
|---|---|
| `Q_coh` for fixed `D` | mathematically derived |
| tracefree shear removal from `J_C` | conditional pass |
| FLRW reduction | preserved |
| stationary local silence | conditional on stable physical `D` |
| domain selector | not derived |
| projection norm from parent action | natural but not parent-derived |
| Bianchi/boundary stress closure | open |

This is not a full win, but it is not cosmetic.

The branch has moved from:

```text
choose Q_coh because it helps
```

to:

```text
Q_coh is the orthogonal coherent-volume projection of Q, if D is physical.
```

That is a sharper mathematical object.

## Decision

Current status:

```text
fixed-D coherent projector derived;
physical D not derived;
no local-GR promotion.
```

The next gate is now brutally specific:

```text
derive the free-boundary/domain Euler equation for D.
```

If that succeeds, the local branch starts looking much more serious.

If it fails, the whole local-silence construction remains:

```text
effective closure with a clean internal projector.
```

## Output Files

```text
runs/20260601-000094-coherent-domain-projector-from-parent-variables/results/source_register.csv
runs/20260601-000094-coherent-domain-projector-from-parent-variables/results/fixed_domain_projection.csv
runs/20260601-000094-coherent-domain-projector-from-parent-variables/results/domain_selector_candidates.csv
runs/20260601-000094-coherent-domain-projector-from-parent-variables/results/variational_boundary_terms.csv
runs/20260601-000094-coherent-domain-projector-from-parent-variables/results/branch_tests.csv
runs/20260601-000094-coherent-domain-projector-from-parent-variables/results/gate_results.csv
runs/20260601-000094-coherent-domain-projector-from-parent-variables/results/decision.csv
```

## Next Step

Next target:

```text
277 - Domain Free-Boundary Euler Equation
```

Attempt:

```text
vary C_coh[D] or an equivalent chi_D action with respect to the domain boundary
and see whether stationary local domains and FLRW domains are selected without empirical thresholds.
```

Acceptance condition:

```text
the boundary condition must not choose the quiet domain by hand.
```

