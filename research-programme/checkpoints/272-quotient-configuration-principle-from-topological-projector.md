# 272 - Quotient Configuration Principle from Topological Projector

Private derivation checkpoint. This is not a public local-GR, CMB, BAO, or unified-field claim.

## Purpose

Checkpoint 271 got us to:

```text
no-Cperp action skeleton works if physical configuration space is [C]=C/ker(P_D).
```

But it did not derive the quotient principle.

This checkpoint asks:

```text
Can the topological projector make [C]=C/ker(P_D) a reduced phase-space result?
```

## Machine Artifact

Script:

```text
scripts/quotient_configuration_principle_from_topological_projector.py
```

Run:

```text
runs/20260601-000090-quotient-configuration-principle-from-topological-projector
```

Status:

```text
quotient_principle_conditionally_derived_from_presymplectic_topological_projector_Cperp_exactness_open
```

Claim ceiling:

```text
quotient_principle_internal_only_no_local_GR_or_unification_promotion
```

## Main Result

The quotient principle now has a real conditional theorem shape.

If:

```text
Cperp residuals are relative-exact representatives,
```

and:

```text
their local boundary primitive is pure gauge / zero,
```

then a topological/relative action changes only by a boundary term:

```text
delta_eta S_top
= integral_D d_rel(... eta_perp ...)
= integral_boundaryD ...
```

For stationary compact local domains this boundary term vanishes.

Then the presymplectic potential has no bulk pairing:

```text
Theta(eta_perp) = boundary or 0
```

so:

```text
Omega(eta_perp, delta) = 0.
```

Therefore `eta_perp` is a null direction of the presymplectic form, and the reduced phase space quotients it:

```text
Phase_phys = ConstraintSurface / ker(Omega)
```

which gives:

```text
C ~ C + eta_perp
```

and:

```text
[C] = C / ker(P_D).
```

This is the first proper route from topological projector to quotient configuration space.

## What Is Conditionally Derived

| Step | Result | Status |
|---|---|---|
| metric-independent `P_D` | topological/relative chain data | conditional previous |
| exact residual shift | `eta_perp = d_rel alpha` or relative-trivial | open burden |
| topological action variation | boundary term only | conditional pass if exact |
| presymplectic degeneracy | `Omega(eta_perp,delta)=0` | conditional pass if exact |
| reduced phase space | quotient by `eta_perp` | conditional derivation |
| matter metric selector | `exp(P_D C)g` | conditional previous |

So:

```text
the quotient principle is no longer just an axiom.
```

It has a route:

```text
relative-exact residuals -> presymplectic null directions -> quotient phase space.
```

## What Still Fails

The missing theorem is now:

```text
Cperp exactness for the C-sector.
```

Checkpoint 231 showed a cohomology route for `J_rel`-style memory current exactness, but not yet for `Cperp` as a conformal/residual representative.

The required conditions are:

| Requirement | Status |
|---|---|
| C-sector is topological/class-valued, not ordinary scalar | not derived |
| local `Cperp` is relative-exact/trivial | supported by analogy, not proven |
| local boundary primitive vanishes | contract, not derived |
| FLRW boundary class survives | conditional shape bridge only |
| domain labels/boundaries varied | open |
| no Hodge/metric projector | conditional previous |
| `B_mem = 2/27` amplitude | not derived |

## Boundary Cases

| Case | Result |
|---|---|
| compact stationary local domain | conditional null residual |
| local exterior shell after mass projection | supports exactness analogy |
| FLRW coherent domain | nontrivial `C_D` may survive |
| dynamic merger/wall boundary | open, not safe to quotient blindly |
| BAO smooth subdomain | conditional same-domain projected metric route |

This is important because the quotient must not kill cosmology while silencing local systems.

## Decision

Decision:

```text
quotient_principle_conditionally_derived_from_presymplectic_topological_projector_Cperp_exactness_open
```

Meaning:

```text
The quotient configuration principle has a conditional topological/presymplectic
derivation route: if Cperp residuals are relative-exact representatives with
vanishing local boundary primitive, they are null directions of the
presymplectic form.
```

Then:

```text
the physical configuration space is [C]=C/ker(P_D).
```

But:

```text
Cperp exactness for the C-sector is not yet parent-derived.
```

Therefore:

```text
the projected matter metric remains a theorem target, not a promotion.
```

## Current Theory Status

This is real progress.

Before:

```text
quotient configuration space was assumed.
```

Now:

```text
quotient configuration space follows if Cperp is a relative-exact null direction.
```

The next burden is exactly:

```text
derive Cperp relative exactness for the C-sector.
```

If that works, the local branch becomes much less closure-like.

If that fails, the projected matter metric must be labelled as an effective closure.

## Next Target

Next:

```text
derive_Cperp_relative_exactness_for_C_sector_or_label_projected_metric_as_closure
```

Pass route:

```text
Cperp is shown to be exact/trivial in the same relative cohomology machinery
that handles local memory current exactness.
```

Fail route:

```text
exp(P_D C)g becomes explicit projected-metric closure.
```

## Claim Gates

| Gate | Result |
|---|---|
| topological presymplectic route | conditional pass |
| `Cperp` exactness for C-sector | not derived |
| boundary conditions | partial |
| Hamiltonian `Cperp` independence | conditional if exact |
| projected metric selector | conditional pass |
| FLRW/unification and `B_mem` | open |
| closure policy | explicit |
| local-GR/unification promotion | forbidden |

## Validation

- Script compiles in `.venv-score`.
- Run completed and wrote `DONE.txt`.
- CSV outputs parse cleanly.
- Cited source paths exist.
- No changes were made to `formalization-workbench`.
- Claim ceiling remains internal only; no local-GR or unification promotion is allowed.
