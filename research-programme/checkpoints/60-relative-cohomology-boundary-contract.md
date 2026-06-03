# Relative Cohomology Boundary Contract

## 1. Purpose

This file follows:

```text
59-topological-cell-current-owner-attempt.md
```

The previous checkpoint found that a topological owner can conditionally remove
local propagating hair, but cannot yet select:

```text
p = 3
u_3 = 1/4
local zero class
FLRW nonzero class
```

This checkpoint asks:

```text
Can the local-zero / FLRW-nonzero split be stated as a non-arbitrary boundary
or relative cohomology contract?
```

Short answer:

```text
yes as a contract, not yet as a derivation.
```

The best contract is:

```text
stationary bound domains carry trivial relative memory class;
coherent FLRW expansion domains carry nontrivial expansion class.
```

That is sharper than “silence local, keep cosmology please”. It still needs a
parent boundary theorem.

## 2. Machine Run

Implemented:

```text
scripts/relative_cohomology_boundary_contract.py
```

Successful run:

```text
runs/20260531-105710-relative-cohomology-boundary-contract/status.json
```

Readout:

```text
relative_boundary_contract_written_not_derived
```

Generated:

```text
runs/20260531-105710-relative-cohomology-boundary-contract/results/source_checkpoint_register.csv
runs/20260531-105710-relative-cohomology-boundary-contract/results/boundary_rule_contract.csv
runs/20260531-105710-relative-cohomology-boundary-contract/results/local_FLRW_split_tests.csv
runs/20260531-105710-relative-cohomology-boundary-contract/results/cohomology_selection_requirements.csv
runs/20260531-105710-relative-cohomology-boundary-contract/results/gate_results.csv
runs/20260531-105710-relative-cohomology-boundary-contract/results/decision.csv
```

## 3. Boundary Rule

Use a relative memory class:

```text
[J_M] in H^3(D, boundary D)
```

or an equivalent relative cell-flux group.

The proposed split is:

```text
stationary local bound domain:
dV_D/dtau = 0
relative memory class = trivial
I_M = 0

coherent FLRW domain:
d ln V_D/dtau = 3H
relative memory class = nontrivial expansion class
Q_coh = (N/u_3) delta
I_M = det(Q_coh)
```

This turns the split into a boundary claim:

```text
volume-stable boundaries carry zero memory-cell class;
coherently expanding boundaries carry expansion memory class.
```

That is the best version of the idea so far.

## 4. What It Explains Conditionally

Conditional passes:

```text
Minkowski local patch:
stationary boundary -> trivial class.

stationary solar-system domain:
stable bound volume -> trivial class if bound-domain rule holds.

virialized galaxy domain:
time-averaged stable volume -> trivial local memory-channel class.

FLRW background:
coherent expanding boundary -> nontrivial expansion class.
```

Open:

```text
FLRW perturbations;
collapse/merger dynamic boundaries;
mapping galaxy empirical pillar without erasing it.
```

So this is a clean contract for the background/local split, not a complete
perturbation or galaxy theory.

## 5. What Still Fails

Gate result:

```text
relative_boundary_contract_written       pass
local_zero_class_nonarbitrary            pass conditional
FLRW_nonzero_class_nonarbitrary          pass conditional
bound_domain_rule_parent_derived         fail
p3_selected_by_cohomology                open
u3_quarter_selected_by_boundary_rule     open
bmem_amplitude_selected                  fail
support_claim_allowed                    fail
```

The biggest missing theorem is now:

```text
derive the bound/unbound boundary rule.
```

Without that, the relative class can still become a rescue choice:

```text
choose the boundary that makes local systems quiet.
```

That is not allowed.

## 6. Selection Requirements

Still required:

```text
zero local class:
prove stationary/virialized bound boundaries are the relevant relative
boundaries.

nonzero FLRW class:
prove coherent expansion boundary carries the expansion class before fitting.

p=3:
derive spatial triad/3-cycle class.

u_3=1/4:
derive 3+1 coherent coframe normalization.

b_mem:
map boundary class magnitude to memory stress amplitude.
```

The contract therefore narrows the branch again:

```text
the next bottleneck is not generic topology;
it is the bound-domain boundary theorem.
```

## 7. Decision

Decision:

```text
relative_cohomology_boundary_status = contract_written_not_derived
```

Meaning:

```text
the local-zero / FLRW-nonzero split now has a clean boundary contract;
the contract is not yet a theorem;
the topological owner remains live but unpromoted.
```

Decision:

```text
topological_owner_status = still_live_but_not_branch_derivation
```

So the quarter branch stays:

```text
less-free closure candidate pending cohomology/action owner.
```

## 8. Next Target

Create:

```text
61-bound-domain-boundary-theorem-attempt.md
```

Purpose:

```text
try to derive the boundary rule that says stationary/virialized bound domains
have trivial relative memory class while coherent FLRW domains do not.
```

Pass condition:

```text
the boundary is selected by a parent volume-flow, extremality, or conservation
condition rather than chosen to silence local tests.
```

Fail condition:

```text
the boundary rule is just a hand-selected local-silence switch.
```
