# Topological Cell-Current Owner Attempt

## 1. Purpose

This file follows:

```text
58-S-cell-variation-attempt.md
```

The previous checkpoint showed that direct scalar multipliers can impose:

```text
I_M = det(Q)
X = 4N
```

but do not derive them. This checkpoint asks:

```text
Can a topological/nonpropagating cell-current owner protect the memory-cell
structure without allowing ordinary conserved-current hair?
```

Short answer:

```text
topology can conditionally remove local propagating hair, but it does not yet
derive the quarter branch.
```

So the beast did not escape. It did change cages.

## 2. Machine Run

Implemented:

```text
scripts/topological_cell_current_owner_attempt.py
```

Successful run:

```text
runs/20260531-105343-topological-cell-current-owner-attempt/status.json
```

Readout:

```text
topological_owner_conditions_local_hair_not_branch_derivation
```

Generated:

```text
runs/20260531-105343-topological-cell-current-owner-attempt/results/source_checkpoint_register.csv
runs/20260531-105343-topological-cell-current-owner-attempt/results/topological_candidate_ledger.csv
runs/20260531-105343-topological-cell-current-owner-attempt/results/topological_variation_chain.csv
runs/20260531-105343-topological-cell-current-owner-attempt/results/no_charge_tests.csv
runs/20260531-105343-topological-cell-current-owner-attempt/results/branch_selection_tests.csv
runs/20260531-105343-topological-cell-current-owner-attempt/results/gate_results.csv
runs/20260531-105343-topological-cell-current-owner-attempt/results/decision.csv
```

## 3. What Topology Can Do

The useful topological template is:

```text
S_BF = integral B wedge F[A].
```

The variations give:

```text
delta B -> F[A] = 0
delta A -> d_A B = 0
```

Meaning:

```text
the cell connection is locally flat;
the cell flux is covariantly closed;
local propagating cell curvature/hair is removed.
```

This is better than ordinary current conservation because ordinary conservation
gave:

```text
Q_cell = constant
```

and did not prove:

```text
Q_cell = 0.
```

A flat/topological owner can at least move the dangerous local hair into global
cohomology/boundary data.

## 4. What Topology Does Not Yet Do

The topological route does not yet select:

```text
p = 3;
u_3 = 1/4;
I_M = det(Q_coh);
X_FLRW = 4N.
```

BF flatness alone says:

```text
F[A] = 0.
```

It does not say:

```text
the relevant invariant is the spatial coherent-load determinant;
the normalization is the 3+1 coframe cell;
the local bound-domain class is zero;
the FLRW class is nonzero with the quarter-locked value.
```

So this is not yet a derivation of the branch.

## 5. Best Remaining Route

The best remaining contract is:

```text
relative cohomology boundary lock.
```

Schematic idea:

```text
S = integral_M B wedge F[A] + boundary pairing
```

with the allowed memory class fixed by:

```text
local bound domains: trivial relative class;
FLRW coherent domain: nontrivial coherent expansion class.
```

This could, in principle, do the job:

```text
kill local hair;
allow cosmological memory;
replace arbitrary integration constants with boundary/cohomology data.
```

But it still needs an actual boundary/cohomology theorem.

## 6. Branch Selection Tests

Status:

```text
p=3:
can be protected conditionally, not selected yet.

u_3=1/4:
can be protected conditionally, not selected yet.

local silence:
partial; flat local connection helps, but zero class is not proven.

Bianchi/conservation:
partial; closed flux helps bookkeeping, but stress-energy owner is missing.

b_mem:
not selected.
```

This means the topological route is useful, but not enough.

## 7. Gate Verdict

Gate result:

```text
topological_owner_attempted             pass
local_propagating_hair_removed          pass conditional
zero_charge_theorem_derived             fail
p3_selected_by_topology                 fail
u3_quarter_selected_by_topology         fail
local_silence_FLRW_activity_split       open
support_claim_allowed                   fail
```

Interpretation:

```text
topology improves the hair problem;
topology does not yet solve the selection problem.
```

## 8. Decision

Decision:

```text
topological_cell_owner_status =
protects_against_local_hair_conditionally_not_branch_derivation
```

Meaning:

```text
the topological route is still live;
it is not a derivation;
the precise missing theorem is now a relative cohomology/boundary rule.
```

Decision:

```text
quarter_branch_status =
retained_less_free_closure_candidate_pending_cohomology_owner
```

So the quarter branch survives as the cleaner closure candidate, but still
does not graduate.

## 9. Next Target

Create:

```text
60-relative-cohomology-boundary-contract.md
```

Purpose:

```text
define the boundary/cohomology rule that would make local bound domains carry
zero memory-cell class while FLRW coherent domains carry the nonzero class
needed for det(Q_coh) and u_3=1/4.
```

Pass condition:

```text
the local-zero/FLRW-nonzero split follows from a non-fitted boundary or
cohomology rule.
```

Fail condition:

```text
the split is chosen by hand to silence local tests while preserving cosmology.
```
