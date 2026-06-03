# Auxiliary Selector Parent Contract

## 1. Purpose

This file follows:

```text
66-chiD-stress-and-scale-gate.md
```

Checkpoint 66 found:

```text
a dynamical chi_D scalar is not safe to promote yet.
```

The problem was not the branch split itself. The problem was:

```text
T_chi and ell_chi.
```

So this checkpoint asks:

```text
Can chi_D be a constrained auxiliary/topological selector rather than a new
gravitating scalar?
```

Short answer:

```text
yes as a clean parent contract, not yet as a complete conservation derivation.
```

## 2. Machine Run

Implemented:

```text
scripts/auxiliary_selector_parent_contract.py
```

Successful run:

```text
runs/20260531-112108-auxiliary-selector-parent-contract/status.json
```

Readout:

```text
minimal_no_stress_contract_written_memory_coupling_open
```

Generated:

```text
runs/20260531-112108-auxiliary-selector-parent-contract/results/source_checkpoint_register.csv
runs/20260531-112108-auxiliary-selector-parent-contract/results/parent_contract_obligations.csv
runs/20260531-112108-auxiliary-selector-parent-contract/results/candidate_parent_routes.csv
runs/20260531-112108-auxiliary-selector-parent-contract/results/variation_chain.csv
runs/20260531-112108-auxiliary-selector-parent-contract/results/gate_results.csv
runs/20260531-112108-auxiliary-selector-parent-contract/results/decision.csv
```

## 3. Contract Obligations

The selector must satisfy:

```text
1. no independent kinetic term;
2. no propagating local scalar degree of freedom;
3. chi_D follows C_coh or an equivalent monotone projector;
4. constraint stress vanishes on shell or is included as conserved boundary
   bookkeeping;
5. metric variation includes the C_coh dependence;
6. no empirical threshold C_star or per-system smoothing length.
```

This prevents the forbidden move:

```text
delete T_chi because it is annoying.
```

The stress has to vanish for a reason.

## 4. Minimal Algebraic Route

The cleanest minimal contract is:

```text
S_aux = integral sqrt(-g) lambda_chi (chi_D - C_coh).
```

Variations:

```text
delta_lambda:
chi_D = C_coh.
```

and:

```text
delta_chi:
lambda_chi = 0
```

if `chi_D` appears nowhere else.

That means:

```text
the direct constraint stress vanishes on shell.
```

This is exactly why the auxiliary route is safer than the phase-field route:

```text
no ell_chi;
no chi_D gradient stress;
no new local scalar force.
```

## 5. The Catch

The selector only matters if it enters the memory sector:

```text
S_mem[chi_D, C_coh, Q, ...].
```

Once that happens:

```text
delta_chi no longer gives lambda_chi = 0.
```

Instead:

```text
lambda_chi = -delta S_mem / delta chi_D.
```

Then the metric variation of:

```text
lambda_chi (chi_D - C_coh)
```

can matter through:

```text
delta_g C_coh.
```

So the next conservation check cannot freeze `C_coh` by hand.

The total identity must involve:

```text
nabla_mu(
  T_mem^munu[chi_D]
  + T_aux^munu
  + T_matter^munu
) = 0.
```

If this does not work, the auxiliary selector is just cleaner-looking
handwaving.

## 6. Candidate Parent Routes

Best minimal contract:

```text
algebraic_multiplier
```

Best long-term route:

```text
topological_boundary_projector
```

because the earlier relative-cohomology route wanted a class/projector object
anyway.

Rejected:

```text
nondynamical_background_window
```

because simply inserting:

```text
chi_D = C_coh
```

with no variation is not a field theory.

Deferred:

```text
small_stress_dynamic_scalar
```

because it keeps the hierarchy and scale problems from checkpoint 66.

## 7. Gate Result

Gate result:

```text
no_independent_kinetic_stress       pass
threshold_free_selection            pass
on_shell_constraint_stress_safe     pass conditional
memory_coupled_Bianchi_resolved     open
Ccoh_parent_derived                 fail
sharp_relative_boundary_derived     open
local_GR_promoted                   fail
support_claim_allowed               fail
```

So the auxiliary route improves the local branch:

```text
it removes ell_chi and independent T_chi.
```

But it does not promote the branch because:

```text
the memory coupling and Bianchi identity are now the real test.
```

## 8. Decision

Decision:

```text
auxiliary_selector_status =
minimal_no_stress_contract_written_memory_coupling_open
```

Meaning:

```text
an algebraic/topological selector can avoid the worst chi_D stress problem;
it still needs a conserved chi_D-gated memory sector;
C_coh itself still needs parent ownership.
```

Decision:

```text
local_GR_route_status = cleaner_but_still_unpromoted
```

This is honestly a decent narrowing:

```text
do not add a new scalar;
use chi_D as a constrained selector for the memory channel only.
```

## 9. Next Target

Create:

```text
68-chiD-gated-memory-conservation-contract.md
```

Purpose:

```text
derive the exact conservation contract for a chi_D-gated memory stress:
nabla_mu(T_mem[chi_D] + T_aux + T_matter)^munu = 0.
```

Pass condition:

```text
the memory channel can be locally silent and FLRW-active without violating the
Bianchi identity or hiding selector stress.
```

Fail condition:

```text
chi_D gating breaks conservation or requires freezing C_coh/metric variation
by hand.
```
