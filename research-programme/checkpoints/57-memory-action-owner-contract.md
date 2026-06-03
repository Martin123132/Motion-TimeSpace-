# Memory Action-Owner Contract

## 1. Purpose

This file follows:

```text
56-u3-quarter-parent-cell-theorem-attempt.md
```

The previous checkpoint gave a conditional route:

```text
p = 3 from spatial coherent-load determinant;
u_3 = 1/4 from 3+1 coherent-cell normalization.
```

But it also exposed the real bottleneck:

```text
what parent action/current owns this split?
```

This checkpoint writes the contract for the missing owner.

Short answer:

```text
the owner contract can be stated, but it is not yet satisfied.
```

The central missing object is:

```text
S_cell[e,u,Q,lambda_cell] plus S_stress[M,e].
```

Translation: the branch now has a proper job advert for the parent theory. It
does not yet have the employee.

## 2. Machine Run

Implemented:

```text
scripts/memory_action_owner_contract.py
```

Successful run:

```text
runs/20260531-104702-memory-action-owner-contract/status.json
```

Readout:

```text
memory_action_owner_contract_written_not_satisfied
```

Generated:

```text
runs/20260531-104702-memory-action-owner-contract/results/source_checkpoint_register.csv
runs/20260531-104702-memory-action-owner-contract/results/owner_field_contract.csv
runs/20260531-104702-memory-action-owner-contract/results/action_term_contract.csv
runs/20260531-104702-memory-action-owner-contract/results/equation_ownership_contract.csv
runs/20260531-104702-memory-action-owner-contract/results/risk_register.csv
runs/20260531-104702-memory-action-owner-contract/results/gate_results.csv
runs/20260531-104702-memory-action-owner-contract/results/decision.csv
```

## 3. Required Owner Fields

The owner contract needs:

```text
e^A_mu:
observer coframe and metric carrier.

u^mu or clock-flow field:
time-flow congruence defining Theta^i_j and the clock/coherence leg.

D or chi_D:
coherent-domain selector/window field.

Q_coh^i_j:
coherent accumulated spatial load tensor.

C4:
3+1 coherent cell normalization.

I_M:
cumulative memory exposure.

T^mu_nu_M or E^mu_nu_M:
memory stress/geometric owner.

lambda_M or lambda_cell:
constraint/current multiplier selecting the memory-cell rule.
```

The most dangerous missing ones are:

```text
u^mu;
D;
S_cell;
S_stress.
```

Without them, the branch is still a disciplined closure chain.

## 4. Minimal Action Contract

The schematic action must contain:

```text
S = S_geom
  + S_flow[e,u,lambda_u]
  + S_domain[u,chi_D]
  + S_Q[Q,u,chi_D]
  + S_cell[e,u,Q,lambda_cell]
  + S_memory[I_M,F,lambda_M]
  + S_stress[M,e]
  + S_matter[e,Psi].
```

The central term is:

```text
S_cell[e,u,Q,lambda_cell].
```

It must derive:

```text
spatial determinant exposure: I_M = det(Q_coh);
3+1 cell normalization: X_FLRW = 4N;
therefore p = 3 and u_3 = 1/4.
```

It also has to explain why:

```text
the determinant is spatial/coherent-load cubic;
the normalization cell is 3+1.
```

That is the exact split a future parent theorem has to own.

## 5. Equation Ownership

The contract assigns ownership like this:

```text
p=3:
I_M=det(Q_coh), owned by S_cell or S_Q.

u_3=1/4:
d ln C4/dtau=4H -> X_FLRW=4N, owned by S_cell.

domain D:
volume-flow extremality or boundary condition, owned by S_domain.

local silence:
dV_D/dtau=0 -> Q_coh=0 -> I_M=0, owned by S_domain plus S_Q.

b_mem:
memory stress amplitude, owned by S_stress.

Bianchi/conservation:
covariant memory exchange or geometric owner, owned by S_geom plus S_stress.

perturbations/lensing:
delta T_M, c_s^2, pi_M, Phi/Psi response, owned by S_stress.
```

This is useful because it stops the work from drifting into five separate
stories that only look unified from far away in bad lighting.

## 6. Gate Verdict

Gate result:

```text
single_owner_contract_written              pass
p3_and_u3_owned_by_same_sector             pass conditional
owner_action_derived                       fail
domain_D_parent_derived                    fail
bmem_amplitude_derived                     fail
Bianchi_conservation_owner_defined         fail
perturbation_lensing_owner_defined         fail
support_claim_allowed                      fail
```

So:

```text
contract written;
contract not satisfied;
quarter branch retained as less-free closure candidate only.
```

No public support language. No victory lap. We are still in the forge.

## 7. Risk Register

High-severity risks:

```text
split-owner problem;
4D-vs-3D inconsistency;
domain rescue knob;
amplitude free parameter;
CMB perturbation import.
```

Medium risk:

```text
local GR branch not unified with cosmology memory branch.
```

The central mitigation is:

```text
make S_cell and S_stress own the whole structure, or demote the branch to an
explicit closure benchmark.
```

## 8. Decision

Decision:

```text
memory_action_owner_status = contract_written_not_satisfied
```

Meaning:

```text
the branch has a single-owner contract;
the branch does not yet have a single-owner derivation;
the next move is to try the S_cell variation directly.
```

Decision:

```text
quarter_branch_status = retained_less_free_closure_candidate_pending_owner
```

Meaning:

```text
u_3=1/4 survived smoke and has a conditional cell route;
it remains closure-level until S_cell owns it.
```

## 9. Next Target

Create:

```text
58-S-cell-variation-attempt.md
```

Purpose:

```text
attempt the minimal variational mechanism for S_cell that selects spatial
determinant exposure and 3+1 normalization without inserting p=3 or u_3=1/4 by
hand.
```

Pass condition:

```text
variation of a legitimate cell/current term produces the p=3/u_3=1/4 split.
```

Fail condition:

```text
S_cell can only be written as a multiplier that directly imposes the desired
answer.
```
