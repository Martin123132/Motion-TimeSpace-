# chi_D-Gated Memory Conservation Contract

## 1. Purpose

This file follows:

```text
67-auxiliary-selector-parent-contract.md
```

Checkpoint 67 made the selector cleaner:

```text
chi_D can be auxiliary/constrained rather than a new propagating scalar.
```

But the selector only matters if it gates the memory sector:

```text
S_mem[chi_D, C_coh, Q, ...].
```

This checkpoint asks:

```text
Can a chi_D-gated memory stress be conserved?
```

Short answer:

```text
yes as an action-level contract, not yet as a derived Bianchi identity.
```

The external-switch version is rejected.

## 2. Machine Run

Implemented:

```text
scripts/chiD_gated_memory_conservation_contract.py
```

Successful run:

```text
runs/20260531-112455-chiD-gated-memory-conservation-contract/status.json
```

Readout:

```text
contract_written_not_derived_boundary_exchange_open
```

Generated:

```text
runs/20260531-112455-chiD-gated-memory-conservation-contract/results/source_checkpoint_register.csv
runs/20260531-112455-chiD-gated-memory-conservation-contract/results/conservation_contract_obligations.csv
runs/20260531-112455-chiD-gated-memory-conservation-contract/results/noether_identity_chain.csv
runs/20260531-112455-chiD-gated-memory-conservation-contract/results/candidate_couplings.csv
runs/20260531-112455-chiD-gated-memory-conservation-contract/results/branch_conservation_tests.csv
runs/20260531-112455-chiD-gated-memory-conservation-contract/results/gate_results.csv
runs/20260531-112455-chiD-gated-memory-conservation-contract/results/decision.csv
```

## 3. Conservation Contract

The total action must be:

```text
S_total =
S_GR_like
+ S_matter
+ S_mem[g,u,Q,chi_D,...]
+ S_aux[chi_D,C_coh,lambda_chi].
```

The total conservation identity must be:

```text
nabla_mu T_total^munu = 0
```

on the full equations of motion.

That means:

```text
nabla_mu(
  T_mem^munu[chi_D]
  + T_aux^munu
  + T_matter^munu
) = 0
```

or else matter exchange must be explicitly derived.

Forbidden:

```text
T_mem^munu = chi_D T_memory^munu
```

inserted directly into the field equations.

That is generally not conserved:

```text
nabla_mu(chi_D T_memory^munu)
= chi_D nabla_mu T_memory^munu
 + T_memory^munu nabla_mu chi_D.
```

The second term is the Bianchi gremlin. It does not go away because we ask
nicely.

## 4. Noether Chain

If the memory and selector pieces come from an action, then under a
diffeomorphism:

```text
delta S_total = 0
```

gives:

```text
nabla_mu T_total^munu =
sum_fields E_field L_xi(field).
```

On shell:

```text
E_field = 0
```

so:

```text
nabla_mu T_total^munu = 0.
```

For the auxiliary selector:

```text
E_lambda = 0 -> chi_D = C_coh.
```

But once `S_mem` depends on `chi_D`:

```text
E_chi = 0 -> lambda_chi = -delta S_mem / delta chi_D.
```

Therefore:

```text
T_aux
```

is not automatically zero.

It can carry the exchange required to make the gated memory source conserved.

That is the correct way to think about it:

```text
auxiliary selector stress is not independent scalar stress;
it is conservation bookkeeping for the memory gate.
```

## 5. Candidate Couplings

Best minimal test:

```text
S_mem = integral sqrt(-g) chi_D L_mem(Q,C2,...).
```

Local branch:

```text
chi_D = 0 -> scalar memory bulk source off.
```

FLRW branch:

```text
chi_D = 1 -> memory branch recovered.
```

Catch:

```text
lambda_chi = -L_mem
```

and:

```text
delta_g C_coh
```

terms enter through `S_aux`.

So the minimal gate is testable, but not automatically safe.

Best long-term route:

```text
boundary_only_gate
```

where memory lives on the relative boundary/cohomology class selected by
`chi_D`. That may fit the earlier topology route better, but it needs a real
boundary-current construction.

Rejected:

```text
external_switch
```

because it is not action-derived.

## 6. Branch Readout

Minkowski / quiet local bulk:

```text
chi_D = C_coh = 0.
```

Result:

```text
scalar memory bulk off.
```

Stationary bound local interior:

```text
chi_D low or zero.
```

Result:

```text
scalar coherent memory suppressed.
```

FLRW:

```text
chi_D = C_coh = 1.
```

Result:

```text
active memory branch recovered.
```

Main danger:

```text
local-to-FLRW boundary.
```

There:

```text
exchange current is likely nonzero
```

and the conservation bookkeeping must actually work.

## 7. Gate Result

Gate result:

```text
action_based_conservation_contract   pass
external_switch_rejected             pass
local_bulk_silence_possible          pass conditional
FLRW_activity_possible               pass contract
Bianchi_identity_derived             fail
boundary_exchange_current_resolved   open
local_GR_promoted                    fail
support_claim_allowed                fail
```

So:

```text
the conservation structure is now correctly framed;
it is not yet derived.
```

This blocks promotion, but it also stops the theory from cheating.

## 8. Decision

Decision:

```text
chiD_gated_memory_conservation_status =
contract_written_not_derived_boundary_exchange_open
```

Meaning:

```text
action-based gating can plausibly give local bulk silence and FLRW activity;
external switching is rejected;
explicit Bianchi identity and boundary exchange current are still missing.
```

Decision:

```text
local_GR_route_status = consistent_contract_but_unpromoted
```

This is not a defeat. It is a proper gate:

```text
derive the memory gate or demote the route.
```

## 9. Next Target

Create:

```text
69-minimal-memory-gate-variation-attempt.md
```

Purpose:

```text
actually vary S_mem = integral sqrt(-g) chi_D L_mem plus
S_aux = integral sqrt(-g) lambda_chi(chi_D - C_coh).
```

Pass condition:

```text
the lambda_chi relation and metric variation terms can be organized into a
conserved local-bulk-silent / FLRW-active memory sector.
```

Fail condition:

```text
the multiplicative memory gate creates an unavoidable nonconserved boundary
exchange term or requires freezing C_coh by hand.
```
