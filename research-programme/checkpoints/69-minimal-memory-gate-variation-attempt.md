# Minimal Memory Gate Variation Attempt

## 1. Purpose

This file follows:

```text
68-chiD-gated-memory-conservation-contract.md
```

Checkpoint 68 said the memory gate must come from an action, not an external
switch.

This checkpoint actually varies the minimal candidate:

```text
S_gate =
integral sqrt(-g)[
  chi_D L_mem(Q,g,u,...)
  + lambda_chi(chi_D - C_coh)
].
```

Short answer:

```text
the variation works algebraically, but conservation is still incomplete.
```

The missing object is now very specific:

```text
delta_g C_coh and the associated boundary/exchange current.
```

## 2. Machine Run

Implemented:

```text
scripts/minimal_memory_gate_variation_attempt.py
```

Successful run:

```text
runs/20260531-112824-minimal-memory-gate-variation-attempt/status.json
```

Readout:

```text
variation_successful_but_conservation_completion_missing
```

Generated:

```text
runs/20260531-112824-minimal-memory-gate-variation-attempt/results/source_checkpoint_register.csv
runs/20260531-112824-minimal-memory-gate-variation-attempt/results/variation_results.csv
runs/20260531-112824-minimal-memory-gate-variation-attempt/results/conservation_terms.csv
runs/20260531-112824-minimal-memory-gate-variation-attempt/results/branch_variation_tests.csv
runs/20260531-112824-minimal-memory-gate-variation-attempt/results/gate_results.csv
runs/20260531-112824-minimal-memory-gate-variation-attempt/results/decision.csv
```

## 3. Variation Result

Use:

```text
S_gate =
integral sqrt(-g)[
  chi_D L_mem
  + lambda_chi(chi_D - C_coh)
].
```

Varying `lambda_chi` gives:

```text
chi_D = C_coh.
```

Good:

```text
threshold-free selection survives.
```

Varying `chi_D` gives:

```text
lambda_chi = -L_mem.
```

This is the important exchange relation.

On shell:

```text
S_gate -> integral sqrt(-g) C_coh L_mem.
```

So the metric variation is not:

```text
C_coh T_Lmem only.
```

It is schematically:

```text
T_gate_munu =
C_coh T_Lmem_munu
+ L_mem T_Ccoh_munu
+ Q/u/domain variation terms.
```

That second term is the whole game.

## 4. What Improved

This is better than an external switch because:

```text
T_mem = chi_D T_memory
```

was rejected.

The action-derived version automatically says:

```text
if C_coh varies, its metric variation contributes.
```

That is exactly what conservation needs.

So the gate is not cheating in the obvious way.

## 5. What Still Fails

The branch still fails promotion because:

```text
T_Ccoh_munu is not constructed.
```

And:

```text
the domain-boundary current is not constructed.
```

The Noether identity can only close if the following are included:

```text
E_Q L_xi Q
E_u L_xi u
E_domain L_xi domain
delta_g C_coh
boundary/relative-class exchange current
```

If any of those are silently frozen, conservation is fake.

## 6. Branch Readout

Quiet local bulk:

```text
C_coh = 0 constant -> S_gate = 0.
```

Conditional pass.

Stationary bound interior:

```text
C_coh low/constant -> memory suppressed.
```

Conditional pass.

FLRW:

```text
C_coh = 1 constant -> S_gate = L_mem.
```

Contract pass.

Transition boundary:

```text
C_coh varies.
```

Open.

That is the dangerous bit:

```text
the theory now lives or dies on the boundary/exchange current.
```

## 7. Gate Result

Gate result:

```text
minimal_variation_performed          pass
external_switch_avoided             pass
local_bulk_silence_retained         pass conditional
FLRW_branch_retained                pass contract
Bianchi_identity_completed          fail
boundary_exchange_resolved          open
Lmem_parent_derived                 fail
local_GR_promoted                   fail
support_claim_allowed               fail
```

So:

```text
algebra good;
conservation incomplete.
```

Again: not grim, but not claimable.

## 8. Decision

Decision:

```text
minimal_memory_gate_status =
variation_successful_but_conservation_completion_missing
```

Meaning:

```text
the minimal gate gives lambda_chi = -L_mem and on-shell C_coh L_mem;
local bulk and FLRW limits work at contract level;
Bianchi completion requires T_Ccoh and boundary-current derivation.
```

Decision:

```text
local_GR_route_status =
local_bulk_plausible_boundary_unresolved
```

The branch is now very sharply defined:

```text
quiet interiors are not the problem;
the local-to-FLRW boundary is the problem.
```

## 9. Next Target

Create:

```text
70-Ccoh-variation-and-boundary-current-audit.md
```

Purpose:

```text
audit whether C_coh can be varied locally/covariantly and whether its variation
defines a boundary/exchange current instead of breaking conservation.
```

Pass condition:

```text
delta_g C_coh and domain-boundary terms can be organized into a conserved
exchange current with no PPN-scale local source.
```

Fail condition:

```text
C_coh must be frozen by hand or produces an uncontrolled boundary stress.
```
