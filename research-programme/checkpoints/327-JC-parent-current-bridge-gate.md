# 327 — `J_C` Parent-Current Bridge Gate

Private derivation checkpoint. This is not a public local-GR, PPN, CMB, cosmology, amplitude, or unified-field claim.

## Purpose

Checkpoint 326 left one precise target:

```text
find a parent current J_C whose FLRW projection gives H(y)=(y/u3)^3
and whose local projection annihilates ordinary baths.
```

This checkpoint connects the earlier `J_C` work from checkpoints 274–276 to the locked `2/27` radial-memory branch.

Question:

```text
Can J_C now be made to own both the cubic FLRW hazard and the local/sector support?
```

Short answer:

```text
cubic FLRW hazard: conditionally yes
tracefree/local stationary silence: conditionally yes
ordinary/edge sector support: no, not without supplied projectors
promotion: no
```

## Machine Artifact

Script:

```text
scripts/JC_parent_current_bridge_gate.py
```

Run:

```text
runs/20260601-160000-JC-parent-current-bridge-gate
```

Status:

```text
JC_Qcoh_derives_FLRW_cubic_hazard_but_not_sector_support_or_local_PPN
```

Claim ceiling:

```text
conditional_JC_bridge_no_Bmem_local_GR_PPN_or_unification_promotion
```

## Candidate Current

The strongest compact candidate is:

```text
J_MTS = P_MTS P_top det(P_coh[Q]) Omega_D / V_D.
```

with pieces:

| Piece | Meaning | Current status |
|---|---|---|
| `Q` | accumulated load/volume-flow tensor | parent variable candidate |
| `P_coh[Q]` | fixed-domain coherent isotropic projection | mathematically derived for fixed `D` |
| `det(P_coh[Q])` | spatial 3-volume hazard density | conditional cubic origin |
| `P_top` | relative/topological class projection | not parent-derived |
| `P_MTS` | MTS-channel support projector | not parent-derived |
| `Omega_D/V_D` | normalized domain 3-form | conditional on physical domain |

This is not just notation. It separates exactly what we own from exactly what we do not own.

## FLRW Cubic Hazard

For FLRW:

```text
P_coh[Q]^i_j = (N/u3) delta^i_j.
```

Therefore:

```text
integral_D J_C = det(P_coh[Q]) = (N/u3)^3.
```

With:

```text
N = y = ln(1+z),
```

the survival activation is:

```text
A(y) = 1 - exp[-integral_D J_C]
     = 1 - exp[-(y/u3)^3].
```

The artifact verifies the equality numerically:

| `y=ln(1+z)` | `u3` | `integral_D J_C` | Expected `(y/u3)^3` | Error |
|---:|---:|---:|---:|---:|
| 0 | 0.25 | 0 | 0 | 0 |
| 0.01 | 0.25 | 0.000064 | 0.000064 | ~0 |
| 0.05 | 0.25 | 0.008 | 0.008 | ~0 |
| 0.25 | 0.25 | 1 | 1 | 0 |
| 1 | 0.25 | 64 | 64 | ~0 |

This is the best derivation gain of the checkpoint:

```text
p=3 can be read as a spatial determinant / domain 3-volume law.
```

That is not numerology.

But:

```text
u3=1/4
```

is still not parent-derived.

## Source-Support Audit

The artifact compares three current candidates:

```text
J_Qcoh = det(P_coh[Q]) Omega_D/V_D
J_top  = P_top det(P_coh[Q]) Omega_D/V_D
J_MTS  = P_MTS P_top det(P_coh[Q]) Omega_D/V_D
```

Result:

| Candidate | Active states | Leakage | Verdict |
|---|---|---|---|
| `J_Qcoh` | ordinary coherent bath, MTS FLRW, edge class | ordinary + edge | support leakage |
| `J_top` | MTS FLRW, edge class | edge | support leakage |
| `J_MTS` | MTS FLRW only | none in toy audit | conditional support pass |

State-level readout:

| State | `J_Qcoh` | `J_top` | `J_MTS` | Meaning |
|---|---:|---:|---:|---|
| stationary local domain | 0 | 0 | 0 | killed |
| tracefree shear wave | 0 | 0 | 0 | killed by `P_coh` |
| ordinary coherent IR relative bath | 0.008 | 0 | 0 | base leaks; top projection fixes if exactness holds |
| MTS FLRW memory class | 1 | 1 | 1 | survives |
| edge/horizon coherent class | 0.512 | 0.512 | 0 | top alone leaks; MTS support fixes if supplied |

This is the hard result:

```text
J_Qcoh owns the cubic hazard,
but it does not own the physical support.
```

Adding `P_top` can kill ordinary exact/local baths if relative exactness is a theorem.

But `P_top` alone does not distinguish MTS FLRW memory from edge/horizon top classes.

So the fully repaired branch still needs:

```text
P_MTS
```

or an equivalent parent-derived channel support.

## Kernel-Commutation Audit

For supplied support:

```text
A_D = C_D^\dagger C_D,
S_D = support(A_D).
```

The artifact verifies:

| Kernel | Commutator norm | Status |
|---|---:|---|
| `K=f(A_D)` | 0 | pass |
| ordinary/MTS mixing kernel | 0.2828427 | fail |
| edge/MTS mixing kernel | 0.2828427 | fail |

So checkpoint 324 still stands:

```text
[K_boundary,A_D]=0
```

must be parent-derived. It cannot be assumed.

## Gate Results

| Gate | Status |
|---|---|
| source paths exist | pass |
| `J_C` constructed from `Q_coh` | pass |
| FLRW cubic hazard | pass |
| tracefree shear killed by `Q_coh` | pass |
| stationary local killed | pass |
| ordinary coherent leakage detected in base `J_Qcoh` | pass |
| ordinary exact bath killed if `P_top` supplied | pass |
| edge top-class leakage detected without `P_MTS` | pass |
| `P_MTS` repaired support passes if supplied | pass |
| `K=f(A_D)` commutes | pass |
| generic kernel mixing counterexample | pass |
| relative exactness parent-derived | fail |
| `P_MTS` parent-derived | fail |
| `u3=1/4` parent-derived | fail |
| `B_mem=2/27` parent-derived | fail |
| local PPN residual zero derived | fail |
| promotion allowed | fail |

## What This Wins

This checkpoint does improve the theory spine.

The radial memory kernel can now be written as:

```text
H_D = integral_D J_C,
J_C = det(P_coh[Q]) Omega_D/V_D,
```

so that:

```text
H_D = (N/u3)^3
```

in FLRW.

That means:

```text
p=3
```

has a conditional geometric origin:

```text
three spatial coherent load directions.
```

This is a real derivation gain.

## What Still Fails

The current cannot yet carry the whole theory.

Still missing:

```text
derive P_top / relative exactness,
derive P_MTS / channel support,
derive the physical domain D,
derive u3=1/4,
derive B_mem=2/27 and kappa_mem=1,
derive [K_boundary,A_D]=0,
derive local PPN silence without a plateau axiom.
```

The concise failure is:

```text
J_C can explain the cubic shape,
but not yet the sector ownership.
```

## Decision

Decision:

```text
JC_Qcoh_derives_FLRW_cubic_hazard_but_not_sector_support_or_local_PPN
```

Allowed language:

```text
MTS has a conditional parent-current route for the cubic radial memory hazard.
```

Stronger but still private/internal language:

```text
The p=3 kernel is no longer a naked fit choice; it can be produced by a coherent 3-volume determinant current.
```

Forbidden language:

```text
MTS derives local GR.
MTS passes PPN.
MTS derives B_mem=2/27.
MTS derives the full local/cosmological sector split.
```

## Boxing Readout

This is a clean point win on one narrow card:

```text
p=3 is now much less mysterious.
```

But the championship lock is still:

```text
who is allowed to source J_C?
```

If ordinary coherent/edge classes can source it, the local branch leaks.

If the parent action derives `P_top` and `P_MTS`, the branch becomes serious.

## Next Target

Two honest options remain:

```text
Route A: derive P_top and P_MTS from a parent boundary/cohomology action.
Route B: stop spending derivation tokens here and run growth/fsigma8 as the next empirical judge.
```

Recommendation:

```text
one final narrow derivation attempt:
P_top / P_MTS from relative cohomology and boundary-sector superselection.
```

If that fails:

```text
move to growth.
```

## Output Files

```text
runs/20260601-160000-JC-parent-current-bridge-gate/status.json
runs/20260601-160000-JC-parent-current-bridge-gate/results/source_register.csv
runs/20260601-160000-JC-parent-current-bridge-gate/results/source_state_support.csv
runs/20260601-160000-JC-parent-current-bridge-gate/results/FLRW_kernel_projection.csv
runs/20260601-160000-JC-parent-current-bridge-gate/results/candidate_current_comparison.csv
runs/20260601-160000-JC-parent-current-bridge-gate/results/kernel_commutation.csv
runs/20260601-160000-JC-parent-current-bridge-gate/results/theorem_clauses.csv
runs/20260601-160000-JC-parent-current-bridge-gate/results/gate_results.csv
runs/20260601-160000-JC-parent-current-bridge-gate/results/decision.csv
```
