# 332 — Parent Hamiltonian Trace-Current Gate

Private derivation checkpoint. This is not a public cosmology, CMB, local-GR, PPN, perturbation-theory, or unified-field claim.

## Purpose

Checkpoint 331 reduced the locked-amplitude problem to:

```text
B_mem = q_trace epsilon_H (H_star/H0)^2.
```

with:

```text
q_trace = 2/27
```

conditionally supplied by the active trace contract.

The next missing lock is:

```text
epsilon_H = 1.
```

This checkpoint asks whether `epsilon_H=1` can be inherited from the parent Hamiltonian constraint, or whether it remains a free memory coupling.

Short answer:

```text
unit inheritance route: yes, conditionally and sharply;
parent derivation: no;
lambda-rescaling no-go: yes.
```

## Machine Artifact

Script:

```text
scripts/parent_Hamiltonian_trace_current_gate.py
```

Run:

```text
runs/20260601-183000-parent-Hamiltonian-trace-current-gate
```

Status:

```text
Hamiltonian_trace_current_unit_inheritance_conditional_lambda_rescaling_no_go_blocks_promotion
```

Claim ceiling:

```text
parent_Hamiltonian_trace_current_contract_no_Bmem_or_local_GR_promotion
```

## The Only Viable Unit Route

The clean route is:

```text
S_mem is not an added memory potential.
```

Instead:

```text
S_mem
```

must be the active trace subblock of the same already-normalized Hamiltonian constraint current that defines the FLRW background stress scale.

In words:

```text
do not add a new term with its own coefficient;
project the parent Hamiltonian current itself.
```

Then the unit coefficient is inherited:

```text
epsilon_H = 1.
```

But only if the parent action proves literal subblock inheritance.

The theorem target is:

```text
H_mem = Tr(P_active H_parent)/dim(V_cell) F(N),
```

with no independent:

```text
lambda_mem.
```

This is much better than vague “normalization by naturalness”, but it is not yet a completed derivation.

## Why Noether/Bianchi Alone Fails

If the memory density is added as:

```text
S_mem = - int N a^3 lambda_mem 3 M_Pl^2 H_star^2 q_trace F(N),
```

then:

```text
epsilon_H = lambda_mem.
```

Now rescale:

```text
lambda_mem -> c lambda_mem.
```

The stress form still varies consistently.

The Bianchi pressure law still works if pressure scales with the density.

A separately covariant or separately first-class term can still satisfy formal Noether/Dirac bookkeeping.

Therefore:

```text
Noether/Bianchi/constraint closure does not select c = 1.
```

That is the no-go.

The only way out is not:

```text
the term is covariant.
```

It is:

```text
the term is not independent.
```

## Route Table

| Route | Result | Status |
|---|---|---|
| projected EH/Hamiltonian subblock | `epsilon_H=1` if literal inheritance is proved | best conditional route |
| added FLRW memory potential | `epsilon_H=lambda_mem` | fails as derivation |
| Noether/Dirac closure only | coefficient remains rescalable | fails to select number |
| topological BF projector | owns projector/local silence, not stress units | supports projector only |
| multiplier setting `lambda=1` | imposes unit value | closure in disguise unless parent-owned |
| unit choice / renormalization | hides factor in notation | rejected |

## Conditional Theorem Contract

The parent action must prove all of:

| Condition | Required statement | Current status |
|---|---|---|
| `H1` same lapse generator | memory current is varied by the same lapse Hamiltonian constraint as the EH/FLRW background | not parent-derived |
| `H2` literal subblock inheritance | `S_mem` is the active trace component of the parent Hamiltonian current, not an added potential | missing core theorem |
| `H3` canonical trace measure | `Tr(P_active)/dim(V_cell)` uses the parent finite-cell trace measure | conditional from rank contract |
| `H4` no independent coupling | parent symmetry forbids `lambda_mem P_active H` as a separate invariant | not derived |
| `H5` scale lock | `H_star=H0` or equivalent is derived separately | closure-locked from 261–262 |
| `H6` local silence | same projector is topological/metric-independent in local exterior reductions | conditional from 252 |
| `H7` Bianchi accounting | projector/domain/boundary stresses are retained in total stress | conditional from 207 |

If these hold, then:

```text
epsilon_H = 1
```

is no longer a closure.

But they do not currently hold as parent-derived theorems.

## Empirical Corridor Imported From 331

The post-330 corrected release split still gives a useful private target corridor:

| Release | fitted `kappa` | if `H_star=H0`, `epsilon_H` | if `epsilon_H=1`, `H_star/H0` | locked-fitted BIC |
|---|---:|---:|---:|---:|
| DR2 | 1.0061980866 | 1.0061980866 | 1.0030942561 | -7.4004287836 |
| DR1 | 0.9911492352 | 0.9911492352 | 0.9955647820 | -7.3997256004 |

This says:

```text
the empirical target is close to unit inheritance.
```

It does not say:

```text
unit inheritance is derived.
```

The fitted amplitude is a clue. It is not a variation.

## Gate Results

| Gate | Result |
|---|---|
| source paths exist | pass |
| post-331 kappa corridor imported | pass |
| locked branch beats kappa-free by BIC | pass |
| unit inheritance route written | pass |
| lambda-rescaling counterexample | pass |
| Noether/Bianchi selects unit coefficient | fail |
| literal parent subblock inheritance derived | fail |
| `epsilon_H=1` parent-derived | fail |
| `B_mem=2/27` parent promotion | fail |

## What This Wins

This is a useful narrowing.

Before:

```text
derive epsilon_H=1.
```

was too vague.

Now the exact fork is:

```text
either memory is a literal projected subblock of the parent Hamiltonian current,
or epsilon_H is a coupling.
```

That is a serious field-theory gate.

It prevents this cheat:

```text
write any covariant memory stress,
set its coefficient to one,
call it natural.
```

No. If it is added, its coefficient is physical.

## What It Does Not Decide

This checkpoint does not derive:

```text
epsilon_H = 1,
B_mem = 2/27,
H_star = H0,
rank(P_active)=2,
dim(V_cell)=27,
local GR,
PPN silence,
CMB safety,
MTS perturbations.
```

It also does not demote the whole branch.

The fair standing is:

```text
the locked branch is empirically disciplined,
the amplitude factorization is exact,
the unit-current theorem target is sharp,
but parent ownership remains open.
```

## Next Derivation Target

The next step is:

```text
construct_or_reject_literal_projected_Hamiltonian_subblock_from_parent_action.
```

The test is:

```text
Can the parent action be written so that the memory term is not an added
sector, but the active trace of the same Hamiltonian constraint current?
```

If yes:

```text
epsilon_H=1
```

has a real route.

If no:

```text
epsilon_H
```

must remain closure/fitted, and `B_mem=2/27` remains an empirical theorem target rather than a derived amplitude.
