# 328 — Topological / MTS Support-Projector Gate

Private derivation checkpoint. This is not a public local-GR, PPN, CMB, cosmology, amplitude, or unified-field claim.

## Purpose

Checkpoint 327 found the best current `J_C` bridge:

```text
J_C = det(P_coh[Q]) Omega_D/V_D
```

which conditionally owns the FLRW cubic hazard:

```text
integral_D J_C = (N/u3)^3.
```

But it also found the support problem:

```text
J_Qcoh leaks ordinary coherent baths and edge/horizon classes.
```

This checkpoint asks the next exact question:

```text
Can P_top and P_MTS be derived, or must they remain closure/theorem targets?
```

Short answer:

```text
P_top: conditional relative-cohomology route exists.
P_MTS: conditional spectral-projector route exists only if a parent sector charge is supplied.
parent promotion: no.
```

## Machine Artifact

Script:

```text
scripts/topological_mts_support_projector_gate.py
```

Run:

```text
runs/20260601-163000-topological-MTS-support-projector-gate
```

Status:

```text
Ptop_conditionally_relative_cohomology_PMTS_requires_parent_sector_charge
```

Claim ceiling:

```text
support_projector_contract_only_no_local_GR_PPN_Bmem_or_unification_promotion
```

## Projector Algebra

The artifact tests:

| Projector | Meaning | Trace | Rank | Status |
|---|---|---:|---:|---|
| `P_top` | relative cohomology projector onto non-exact domain classes | 2 | 2 | pass |
| `P_MTS` | spectral projector onto MTS sector if parent charge is supplied | 1 | 1 | pass |
| `P_MTS P_top` | repaired support projector for `J_C` | 1 | 1 | pass |
| singlet-like selector without sector | coherent selector without support charge | 3 | 3 | pass algebraically, fails physically |

All listed projectors are idempotent in the toy support algebra.

The important result is not that an idempotent can be written. That part is easy.

The important result is which idempotent has a parent route.

## `P_top` Result

`P_top` has the strongest current derivation route:

```text
metric-independent relative/topological chain projector
=> exact local representatives are quotient/null
=> non-exact domain classes survive.
```

In the toy support audit:

| State | Relative class | `P_top` | Meaning |
|---|---|---:|---|
| stationary local exact | exact | 0 | killed |
| tracefree shear exact | exact | 0 | killed |
| ordinary coherent exact | exact | 0 | killed if exactness holds |
| MTS FLRW top class | top | 1 | retained |
| edge/horizon top class | top | 1 | retained, leak |

So:

```text
P_top kills exact ordinary/local representatives.
```

But:

```text
P_top does not distinguish MTS top class from edge/horizon top class.
```

This is a genuine improvement over pure closure, but not the full projector.

## `P_MTS` Result

`P_MTS` can be written cleanly if the parent action supplies a conserved sector charge:

```text
Q_sector |MTS> = q_MTS |MTS>,
q_MTS != q_ordinary,
q_MTS != q_edge.
```

Then:

```text
P_MTS
```

is the spectral projector onto the unique `q_MTS` eigenspace.

The artifact tests three charge cases:

| Charge | Eigenvalues | Can define unique `P_MTS`? | Meaning |
|---|---|---:|---|
| good sector charge | `0;0;0;1;2` | yes | MTS uniquely labeled |
| degenerate top charge | `0;0;0;1;1` | no | MTS degenerate with edge |
| singlet-like charge | `0;0;1;1;1` | no | ordinary/edge leakage |

So the theorem route is exact:

```text
derive a nondegenerate conserved MTS sector charge.
```

But the current corpus does not yet derive such a charge.

## Support Audit

The repaired support is:

```text
P_support = P_MTS P_top.
```

State-level result:

| State | `P_top` | `P_MTS P_top` | Desired | Readout |
|---|---:|---:|---:|---|
| stationary local exact | 0 | 0 | 0 | pass |
| tracefree shear exact | 0 | 0 | 0 | pass |
| ordinary coherent exact | 0 | 0 | 0 | pass if exactness holds |
| MTS FLRW top class | 1 | 1 | 1 | pass |
| edge/horizon top class | 1 | 0 | 0 | `P_top` leaks; `P_MTS` fixes if supplied |

This tells us the exact structure needed by the parent action:

```text
J_C^phys =
P_MTS P_top det(P_coh[Q]) Omega_D/V_D.
```

It is precise.

It is not yet parent-derived.

## Kernel-Commutation Result

For the full support projector:

| Kernel | Commutator norm | Status |
|---|---:|---|
| sector-block / functional kernel | 0 | pass |
| ordinary/MTS mixing kernel | 0.212132 | fail |
| edge/MTS mixing kernel | 0.212132 | fail |

So the old gate remains:

```text
[K_boundary, P_MTS P_top] = 0
```

must be a parent-action result. It cannot be imposed after the fact.

## Gate Results

| Gate | Status |
|---|---|
| source paths exist | pass |
| `P_top` idempotent relative projector | pass |
| `P_top` kills exact local states | pass |
| `P_top` retains FLRW memory | pass |
| `P_top` edge leak detected | pass |
| `P_MTS` spectral projector possible if good charge supplied | pass |
| degenerate charge counterexample | pass |
| singlet-like charge counterexample | pass |
| full support retains only MTS sample | pass |
| kernel commutes if block/functional | pass |
| kernel mixing counterexample | pass |
| local exactness parent-derived | fail |
| boundary primitive parent-derived | fail |
| sector charge parent-derived | fail |
| `B_mem=2/27` parent-derived | fail |
| local PPN residual zero derived | fail |
| promotion allowed | fail |

## What This Wins

The local/projector branch is now sharper.

Before:

```text
P_top and P_MTS were vague missing filters.
```

Now:

```text
P_top = relative cohomology / quotient projector,
P_MTS = spectral projector of a nondegenerate sector charge.
```

So the parent-action burden is exact:

```text
derive local exactness,
derive vanishing local boundary primitive,
derive nondegenerate MTS sector charge,
derive kernel commutation.
```

This is real progress because it prevents fuzzy projector language.

## What Still Fails

The current branch still does not derive:

```text
full C/J_C local exactness,
vanishing local boundary primitive,
the MTS sector charge,
u3=1/4,
B_mem=2/27,
kappa_mem=1,
local PPN silence.
```

The key failure is:

```text
P_top can separate exact from topological,
but it cannot separate MTS from edge.
```

That is why `P_MTS` remains necessary.

## Decision

Decision:

```text
Ptop_conditionally_relative_cohomology_PMTS_requires_parent_sector_charge
```

Allowed language:

```text
The support-projector route has a clean conditional structure:
P_top from relative cohomology, P_MTS from a future parent sector charge.
```

Forbidden language:

```text
MTS derives the full support projector.
MTS derives local GR.
MTS passes PPN.
MTS derives B_mem=2/27.
```

## Boxing Readout

This is the bell on the projector round.

We landed a clean technical point:

```text
P_top is not handwaving anymore.
```

But the title shot still needs:

```text
P_MTS from a parent conserved charge.
```

Without that charge, the edge/top-class leak is still live.

## Next Target

Default next:

```text
move to growth/fsigma8 as the next empirical judge.
```

Reason:

```text
the local/projector branch has reached a clean conditional contract,
but another derivation turn without a genuinely new parent sector charge would mostly circle the same lock.
```

The derivation theorem target remains:

```text
find a parent boundary/cohomology charge Q_sector
such that q_MTS is nondegenerate,
P_MTS = spectral projector onto q_MTS,
[K_boundary,P_MTS P_top]=0.
```

If that new idea appears, reopen the derivation route.

Otherwise:

```text
test the locked background against growth.
```

## Output Files

```text
runs/20260601-163000-topological-MTS-support-projector-gate/status.json
runs/20260601-163000-topological-MTS-support-projector-gate/results/source_register.csv
runs/20260601-163000-topological-MTS-support-projector-gate/results/basis_states.csv
runs/20260601-163000-topological-MTS-support-projector-gate/results/projector_algebra.csv
runs/20260601-163000-topological-MTS-support-projector-gate/results/support_action.csv
runs/20260601-163000-topological-MTS-support-projector-gate/results/sector_charge_spectral_tests.csv
runs/20260601-163000-topological-MTS-support-projector-gate/results/kernel_commutation.csv
runs/20260601-163000-topological-MTS-support-projector-gate/results/theorem_clauses.csv
runs/20260601-163000-topological-MTS-support-projector-gate/results/gate_results.csv
runs/20260601-163000-topological-MTS-support-projector-gate/results/decision.csv
```
