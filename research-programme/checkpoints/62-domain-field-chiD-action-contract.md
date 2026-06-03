# Domain Field chi_D Action Contract

## 1. Purpose

This file follows:

```text
61-bound-domain-boundary-theorem-attempt.md
```

Checkpoint 61 found a real partial theorem:

```text
zero coherent boundary volume flux -> zero local scalar volume-memory channel.
```

But it also found the main gap:

```text
the theory has not derived which domain D is physical.
```

This checkpoint writes the exact contract a future parent action must satisfy.
It does not pretend the action has already been derived.

Short answer:

```text
chi_D makes the missing obligation precise, but the branch remains
closure-level until chi_D is actually varied.
```

## 2. Machine Run

Implemented:

```text
scripts/domain_field_chiD_action_contract.py
```

Successful run:

```text
runs/20260531-110553-domain-field-chiD-action-contract/status.json
```

Readout:

```text
chiD_action_contract_written_not_varied
```

Generated:

```text
runs/20260531-110553-domain-field-chiD-action-contract/results/source_checkpoint_register.csv
runs/20260531-110553-domain-field-chiD-action-contract/results/chiD_object_register.csv
runs/20260531-110553-domain-field-chiD-action-contract/results/action_contract.csv
runs/20260531-110553-domain-field-chiD-action-contract/results/candidate_action_routes.csv
runs/20260531-110553-domain-field-chiD-action-contract/results/selection_gate_tests.csv
runs/20260531-110553-domain-field-chiD-action-contract/results/falsification_tests.csv
runs/20260531-110553-domain-field-chiD-action-contract/results/gate_results.csv
runs/20260531-110553-domain-field-chiD-action-contract/results/decision.csv
```

## 3. Required Objects

Introduce:

```text
chi_D
```

as a covariant domain selector, smooth window field, phase field, or equivalent
boundary-current representation.

Its job is to define:

```text
V_D = integral chi_D dSigma
<theta>_D = d ln V_D/dtau
Q_coh
the relative memory class
```

The associated boundary object is:

```text
Sigma_D = boundary/level set of chi_D.
```

The associated flux/current object is:

```text
J_D^mu
```

whose normal flux controls:

```text
dV_D/dtau.
```

The key equation must be:

```text
E_chi = delta S_D / delta chi_D = 0
```

or the equivalent boundary-current Euler equation.

Forbidden:

```text
choose chi_D after seeing PPN, SPARC, Pantheon, BAO, CMB, or growth residuals.
```

That would make chi_D a rescue knob, not a theory field.

## 4. Action Contract

The parent action must provide:

```text
S_D[chi_D, J_D, u, h, Q, lambda_D, ...]
```

or an equivalent boundary action.

It must satisfy six obligations:

```text
1. Covariant domain definition:
   D is the support or level-set of chi_D.

2. Volume-flux variation:
   varying chi_D or Sigma_D yields an extremal coherent volume-flow equation.

3. FLRW active solution:
   homogeneous FLRW admits d ln V_D/dtau = 3H.

4. Bound stationary solution:
   stationary/virialized bound systems admit dV_D/dtau = 0.

5. Bianchi-compatible stress:
   the chi_D/domain sector does not leak energy-momentum.

6. Universal parameters:
   no object-by-object fitted smoothing lengths or empirical switches.
```

The central pass/fail sentence is:

```text
E_chi = 0 must give dV_D/dtau = 0 for stationary bound domains and
d ln V_D/dtau = 3H for coherent FLRW.
```

If it cannot do both, this route fails.

## 5. Candidate Action Routes

Best next variation attempt:

```text
constraint_current_action:
S_D = integral sqrt(-g) lambda_D nabla_mu J_D^mu plus boundary term.
```

Why it is attractive:

```text
it can turn domain flux into an Euler-Lagrange/conservation statement.
```

Risk:

```text
it may merely impose the boundary instead of deriving why that boundary is
physical.
```

Other live routes:

```text
phase_field_boundary_action
volume_flux_extremal_action
relative_boundary_topological_pairing
```

Rejected route:

```text
empirical_window_function
```

because it can fit or silence almost anything.

## 6. Selection Gates

The required outcomes are:

```text
Minkowski:
constant/stationary chi_D gives dV_D/dtau = 0 and Q_coh = 0.

stationary solar system:
E_chi selects a closed or asymptotically stationary bound boundary.

virialized galaxy:
E_chi supports time-averaged volume stability without erasing the separate
galaxy empirical pillar.

FLRW:
E_chi admits coherent comoving domains with d ln V_D/dtau = 3H.

collapse/merger:
dynamic boundaries are not forced to zero; they need their own field equation.
```

This is the correct attitude:

```text
local quiet is not universal quiet.
```

The scalar volume-memory channel can vanish in stationary bound systems while
dynamic/strong-field systems remain open.

## 7. Falsification Conditions

This route must be demoted if any of these happen:

```text
chi_D depends on observed residuals;
no covariant E_chi exists;
FLRW active domains are not solutions;
stationary bound zero-flux domains are not solutions;
domain/memory stress is not conserved.
```

The most important one is:

```text
no covariant E_chi -> no derived local boundary.
```

No field equation, no promotion. Harsh but fair.

## 8. Gate Result

Gate result:

```text
chiD_object_defined                 pass
action_contract_written             pass
stationary_bound_boundary_derived   fail
FLRW_active_solution_preserved      pass conditional
Bianchi_conservation_resolved       open
no_empirical_window_tuning          pass conditional
support_claim_allowed               fail
```

So the status is:

```text
contract written, not varied.
```

This is useful because it prevents the next derivation attempt from being vague.
The branch now has a precise demand:

```text
derive E_chi and show it selects the right boundaries.
```

## 9. Decision

Decision:

```text
chiD_action_status = contract_written_not_varied
```

Meaning:

```text
the future parent action obligations are explicit;
the boundary selector is not yet derived;
local-GR safety remains closure-level until the variation succeeds.
```

Decision:

```text
local_transition_route_status = alive_but_closure_until_variation
```

That is honestly not grim. It is narrow. Narrow is where theories either die
properly or become real.

## 10. Next Target

Create:

```text
63-chiD-variation-to-boundary-equation-attempt.md
```

Purpose:

```text
take the least-engineered chi_D/J_D action candidate and vary it.
```

Pass condition:

```text
the variation gives a boundary equation whose stationary branch is
dV_D/dtau = 0 and whose homogeneous FLRW branch permits d ln V_D/dtau = 3H.
```

Fail condition:

```text
the action only restates the desired boundary condition as a multiplier
constraint with no physical selector.
```
