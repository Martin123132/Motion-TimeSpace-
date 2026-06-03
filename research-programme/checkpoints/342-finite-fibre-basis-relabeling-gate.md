# 342 - Finite-Fibre Basis-Relabeling Gate

Private derivation checkpoint. This is not a public cosmology, CMB, local-GR, PPN, perturbation-theory, or unified-field claim.

## Purpose

Checkpoint 341 left the next exact target:

```text
derive the 27-cell structure as basis labels in a finite internal fibre.
```

This checkpoint tests whether that route can support the amplitude derivation.

Short answer:

```text
yes, conditionally.
```

Finite-fibre basis relabeling gives a clean mechanism:

```text
cell labels are basis choices,
trace/spectral data are physical,
fixed P_active is not a basis-free bulk observable,
P_active can only be a source/relational readout.
```

But it does not yet derive:

```text
the finite fibre itself,
dim(V_cell)=27,
rank(P_active)=2,
no marker extension,
H_star=H0,
or basis-invariant effective corrections.
```

## Machine Artifact

Script:

```text
scripts/finite_fibre_basis_relabeling_gate.py
```

Run:

```text
runs/20260601-210000-finite-fibre-basis-relabeling-gate
```

Status:

```text
finite_fibre_basis_relabeling_template_supported_dim_rank_origin_open
```

Claim ceiling:

```text
finite_fibre_gate_no_unconditional_epsilonH_Bmem_or_parent_action_promotion
```

## Basis-Invariant Tests

The verifier treats the parent current as an operator on:

```text
V_cell, dim(V_cell)=27.
```

Under basis relabeling/change:

```text
H -> U^T H U.
```

The trace and spectrum data are invariant:

```text
Tr(H)/27,
Tr((H-I)^2),
spectrum(H).
```

The trace action passes:

```text
S = 2.6171089118110563e-05
```

before and after basis relabeling.

So a trace/spectral parent action is a legitimate finite-fibre quotient action.

## Fixed Projector Failure

For a nontrivial parent current, a fixed active projector readout changes under basis change:

```text
1.00464856495626 -> 1.0000723727594134.
```

Therefore:

```text
fixed P_active is not basis-free.
```

This is good for the no-counterterm route:

```text
P_active cannot be a physical bulk tensor if basis relabeling is gauge.
```

## Relational Projector Pass

If the projector transforms with the reference frame:

```text
P_active -> U^T P_active U,
```

then the readout is invariant:

```text
1.00464856495626 -> 1.00464856495626.
```

This is the safe route:

```text
P_active as relational/source readout.
```

But the old danger remains:

```text
if the transformed projector is a physical marker field,
then marker-local counterterms are allowed.
```

So relational readout still needs the no-marker theorem.

## Identity Current Exception

For the identity current:

```text
H = I_cell,
```

any rank-2 projector gives:

```text
Tr(P_active I_cell)/27 = 2/27.
```

The verifier confirms:

```text
q_trace = 0.07407407407407407.
```

This is the exact reason the route is worth keeping:

```text
identity current + dim 27 + rank 2
=> 2/27.
```

But that is a conditional theorem, not the whole derivation.

## Dimension/Rank Audit

| Item | Possible route | Status |
|---|---|---|
| `dim(V_cell)=27` | three ternary finite-fibre factors, `3*3*3` | conditional template |
| `rank(P_active)=2` | rank-2 source/readout plane | assumed readout rank |
| `q_trace=2/27` | identity current on dim-27 fibre read by rank-2 projector | conditional |
| `epsilon_H=1` | trace-normalized identity Hamiltonian current | conditional |

So:

```text
2/27 is algebraically sharp,
but the parent still has to own the 27 and the 2.
```

## Route Audit

| Route | Counterterm status | Amplitude status |
|---|---|---|
| labelled component vector | allowed after active selection | closure/fitted |
| finite-fibre operator modulo `S27` | forbidden if labels are unphysical | conditional theorem |
| finite-fibre operator modulo `O(27)` | stronger basis gauge | conditional theorem for identity current |
| tensor fibre `3x3x3` | dimension route possible | rank-2 still open |
| marker-extended fibre | marker-local invariants allowed | closure/fitted |

The best live route is:

```text
basis-free finite fibre + trace/spectral action + source/relational rank-2 readout.
```

The dangerous route is:

```text
marker-extended fibre.
```

## Finite-Fibre Contract

The exact contract is now:

| Condition | Requirement | Status |
|---|---|---|
| `F1` | parent object is basis-free fibre current | not yet parent-derived |
| `F2` | `dim(V_cell)=27` from parent finite fibre | conditional template |
| `F3` | physical action is trace/spectral | tree-level template verified |
| `F4` | rank-2 projector is source/readout, not marker | open |
| `F5` | no marker-extended fibre | open |
| `F6` | effective action preserves basis gauge | open |

This is the cleanest internal-fibre statement so far.

## Gate Results

| Gate | Result |
|---|---|
| source paths exist | pass |
| trace action is basis invariant | pass |
| spectrum is basis invariant | pass |
| fixed `P_active` is not basis invariant | pass |
| relational transformed projector readout is basis invariant | pass |
| identity current rank readout gives `2/27` | pass |
| `dim=27` from `3x3x3` template | pass |
| `dim=27` parent-derived | fail |
| `rank=2` parent-derived | fail |
| parent object proves basis-free fibre | fail |
| parent theory forbids marker-extended fibre | fail |
| effective action basis-invariant derived | fail |
| `epsilon_H` parent-derived unconditionally | fail |
| `B_mem` parent promotion allowed | fail |
| finite-fibre basis-relabeling contract available | pass |

## What This Means

This route has real value:

```text
finite-fibre basis relabeling can make cell labels gauge.
```

It explains why:

```text
fixed P_active should not appear in the physical bulk action.
```

It also shows why:

```text
identity current + rank 2 / dimension 27
```

naturally gives:

```text
B_mem = 2/27
```

provided:

```text
epsilon_H = 1,
H_star = H0.
```

But this checkpoint does not derive the parent finite fibre or the rank-2 readout.

## Standing

The fair status is:

```text
finite-fibre basis relabeling is a precise conditional mechanism.
```

Not:

```text
B_mem = 2/27 is parent-derived.
```

So:

```text
epsilon_H = 1
```

remains conditionally derived, and:

```text
B_mem = 2/27
```

remains the locked empirical lead/theorem target.

## Next Derivation Target

Next:

```text
derive_dim27_rank2_finite_fibre_origin_or_demote_amplitude_to_closure.
```

Acceptance rule:

```text
The parent theory must derive both dim(V_cell)=27 and rank(P_active)=2,
while keeping P_active as source/readout rather than marker.
```

If that cannot be done soon, the honest move is:

```text
freeze epsilon_H as explicit closure/fitted,
keep 2/27 as empirical lead,
and stop promoting the amplitude as parent-derived.
```
