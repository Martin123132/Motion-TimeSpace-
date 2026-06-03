# chi_D Stress and Scale Gate

## 1. Purpose

This file follows:

```text
65-Ccoh-phase-field-selector-attempt.md
```

Checkpoint 65 found an explicit selector equation:

```text
ell_chi^2 D^2 chi - (chi - C_coh) = 0.
```

That was progress. But if `chi_D` is a real field, it carries stress.

This checkpoint asks:

```text
Does the selector field itself break local GR?
```

Short answer:

```text
a fully dynamical chi_D scalar cannot be promoted yet.
```

The safer route is:

```text
chi_D as an auxiliary/constrained/topological selector with no independent
local stress.
```

## 2. Machine Run

Implemented:

```text
scripts/chiD_stress_and_scale_gate.py
```

Successful run:

```text
runs/20260531-111832-chiD-stress-and-scale-gate/status.json
```

Readout:

```text
dynamic_selector_not_promoted_auxiliary_route_preferred
```

Generated:

```text
runs/20260531-111832-chiD-stress-and-scale-gate/results/source_checkpoint_register.csv
runs/20260531-111832-chiD-stress-and-scale-gate/results/stress_equation_chain.csv
runs/20260531-111832-chiD-stress-and-scale-gate/results/branch_stress_tests.csv
runs/20260531-111832-chiD-stress-and-scale-gate/results/scale_option_ledger.csv
runs/20260531-111832-chiD-stress-and-scale-gate/results/conservation_gate_tests.csv
runs/20260531-111832-chiD-stress-and-scale-gate/results/gate_results.csv
runs/20260531-111832-chiD-stress-and-scale-gate/results/decision.csv
```

## 3. Stress Accounting

Use the rescaled action:

```text
S_chi =
-1/2 integral sqrt(-g) rho_chi[
  ell_chi^2 h^munu nabla_mu chi nabla_nu chi
  + (chi - C_coh)^2
].
```

This separates:

```text
ell_chi  = selector transition width
rho_chi  = selector stress amplitude
```

The field equation is:

```text
ell_chi^2 D^2 chi - (chi - C_coh) = 0.
```

The overall amplitude `rho_chi` cancels from the selector equation if it is
nonzero, but it does not cancel from the metric stress:

```text
T_chi_munu ~ rho_chi[
  ell_chi^2 nabla_mu chi nabla_nu chi
  + metric terms
].
```

That means a small `rho_chi` could make the selector nearly stressless while
leaving the classical selector equation intact.

But that is not free:

```text
rho_chi must be parent-derived, constrained, or topological.
```

Otherwise it is just a new hierarchy knob.

## 4. Good News

On homogeneous ideal branches:

```text
chi = C_coh
nabla chi = 0
```

so:

```text
T_chi approximately 0.
```

This helps:

```text
Minkowski:
chi = C_coh = 0 -> no bulk chi stress.

stationary bound interior:
chi approximately 0 -> no bulk chi stress if C_coh is low.

FLRW:
chi = C_coh = 1 -> no bulk chi stress from the relaxation potential.
```

So the selector does not automatically become a new dark-energy fluid. The
cosmological signal must still come from the memory sector, not `T_chi`.

That is good. Very good, actually.

## 5. Bad News

The danger moves to transition layers:

```text
chi changes from low to high over ell_chi.
```

Then the stress is localized near the boundary.

Scaling:

```text
transition stress density ~ rho_chi
surface tension ~ rho_chi ell_chi (Delta chi)^2
```

For a local domain of size `R_D`, the rough local potential contribution is:

```text
Phi_chi ~ 4 pi G rho_chi R_D ell_chi (Delta chi)^2.
```

Local safety requires:

```text
Phi_chi << Phi_PPN_bound.
```

This is now a concrete inequality, but it is not yet satisfied by derivation.

So:

```text
local interiors look safe;
local boundaries are the unresolved danger.
```

## 6. Scale Options

Best if legal:

```text
auxiliary_zero_stress_selector
```

Meaning:

```text
chi_D is not a propagating gravitating scalar.
It is a constrained/topological/domain projector.
```

This is the cleanest local-GR route.

Conditional:

```text
small_rho_chi_universal
microscopic_ell_chi
```

Both can help, but both need parent derivation.

Risky:

```text
cosmological_ell_chi
```

because it can turn into a hidden MOND-like/coarse-graining scale.

Rejected:

```text
fit_ell_chi_per_system
```

That is just an empirical smoothing knob wearing a fake moustache.

## 7. Conservation Gate

The full conservation condition must eventually be:

```text
nabla_mu(
  T_chi^munu
  + T_mem^munu
  + T_matter^munu
) = 0.
```

This is not solved by treating `C_coh` as frozen.

Why:

```text
C_coh depends on theta, sigma, omega, the domain average, and the observer
congruence.
```

So varying the metric or motion variables must also vary `C_coh`.

If that is ignored, the Bianchi identity is fake.

## 8. Gate Result

Gate result:

```text
stress_tensor_identified            pass
bulk_background_safe                pass conditional
local_boundary_stress_bounded       open
ell_chi_parent_derived              fail
Bianchi_conservation_resolved       open
dynamic_scalar_promoted             fail
auxiliary_selector_route_open       pass conditional
support_claim_allowed               fail
```

So the verdict is:

```text
do not promote a dynamical chi_D scalar yet.
```

But:

```text
an auxiliary/constrained/topological selector route is now strongly preferred.
```

## 9. Decision

Decision:

```text
chiD_stress_scale_status =
dynamic_selector_not_promoted_auxiliary_route_preferred
```

Meaning:

```text
bulk stress can vanish on ideal local and FLRW branches;
transition-layer stress and ell_chi remain unbounded;
a freely dynamical selector would be dangerous for local GR;
the clean next route is a constrained no-independent-stress selector.
```

Decision:

```text
local_GR_route_status =
alive_but_dynamic_chiD_unsafe_until_bound
```

This is not a collapse. It is a refinement:

```text
make chi_D a selector, not a new fifth-force field.
```

## 10. Next Target

Create:

```text
67-auxiliary-selector-parent-contract.md
```

Purpose:

```text
state the exact parent contract for a chi_D/domain selector that has no
independent propagating local stress but still selects C_coh-driven local/FLRW
branches.
```

Pass condition:

```text
the selector contributes only constraint/topological/boundary bookkeeping stress
that is included in a conserved total system, not an unsuppressed local source.
```

Fail condition:

```text
the no-stress selector is just deleting T_chi by decree.
```
