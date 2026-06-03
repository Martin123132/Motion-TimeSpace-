# Bound-Domain Boundary Theorem Attempt

## 1. Purpose

This file follows:

```text
60-relative-cohomology-boundary-contract.md
```

Checkpoint 60 gave the best local/cosmology split so far:

```text
stationary bound domains carry trivial relative memory class;
coherent FLRW expansion domains carry nontrivial expansion class.
```

This checkpoint asks whether the local boundary can be selected by physics
rather than by the forbidden move:

```text
draw a boundary around the local system because that makes PPN quiet.
```

Short answer:

```text
partly, but not enough to promote the branch.
```

The volume-flow theorem gives a real, non-silly route:

```text
stationary/extremal volume-flow boundary -> local scalar volume-memory channel
is silent.
```

But the parent action still has to derive the boundary/domain selector.

## 2. Machine Run

Implemented:

```text
scripts/bound_domain_boundary_theorem_attempt.py
```

Successful run:

```text
runs/20260531-110230-bound-domain-boundary-theorem-attempt/status.json
```

Readout:

```text
bound_domain_boundary_theorem_partial_volume_extremum_not_parent_action
```

Generated:

```text
runs/20260531-110230-bound-domain-boundary-theorem-attempt/results/source_checkpoint_register.csv
runs/20260531-110230-bound-domain-boundary-theorem-attempt/results/boundary_theorem_chain.csv
runs/20260531-110230-bound-domain-boundary-theorem-attempt/results/domain_candidate_tests.csv
runs/20260531-110230-bound-domain-boundary-theorem-attempt/results/local_system_boundary_tests.csv
runs/20260531-110230-bound-domain-boundary-theorem-attempt/results/noncircularity_tests.csv
runs/20260531-110230-bound-domain-boundary-theorem-attempt/results/gate_results.csv
runs/20260531-110230-bound-domain-boundary-theorem-attempt/results/decision.csv
```

## 3. The Partial Theorem

Define the domain volume:

```text
V_D(tau) = integral_D dSigma.
```

The boundary-flux identity is:

```text
dV_D/dtau = integral_boundary(D) v_n dA = integral_D theta dSigma.
```

Therefore:

```text
<theta>_D = (1/V_D)dV_D/dtau = d ln V_D/dtau.
```

This is the important bit:

```text
if dV_D/dtau = 0,
then <theta>_D = 0,
then P_coh[Theta] = 0,
then Q_coh = 0
```

So a stationary or virialized bound domain is locally silent in the scalar
volume-memory channel if the theory has already selected that domain.

That is not a magic PPN patch. It is a physical condition:

```text
no coherent boundary volume flux -> no coherent volume memory.
```

## 4. Why FLRW Survives

For a coherent FLRW comoving domain:

```text
V_D proportional a^3
```

so:

```text
d ln V_D/dtau = 3H.
```

Then the previous coherent load survives:

```text
Q_coh^i_j = (N/u_3) delta^i_j.
```

This is good. The same boundary rule does not silence cosmology.

The split is therefore:

```text
zero boundary flux -> trivial local relative class
coherent expansion flux -> nontrivial FLRW relative class
```

That is the cleanest version of local-GR safety currently on the table.

## 5. Candidate Boundary Rules

Best candidate:

```text
volume_extremal_boundary
```

Meaning:

```text
select boundaries by extremal coherent volume-flow;
the stationary branch has dV_D/dtau = 0.
```

This is the strongest route because it defines the boundary by flux/extremality
before asking whether local tests pass.

Plausible but risky:

```text
turnaround_zero_expansion_surface
virial_time_averaged_boundary
```

They are physically meaningful, but they risk importing Newtonian/GR ideas
unless MTS derives its own bound-domain or averaging theorem.

Rejected:

```text
arbitrary_silencing_boundary
pointwise_no_boundary
```

The first is a rescue knob. The second does not give the relative class a
well-defined boundary object.

## 6. Local System Readout

Conditional passes:

```text
Minkowski patch:
dV_D/dtau = 0, Q_coh = 0.

stationary solar system:
bound domain has no coherent boundary volume flux if the parent rule selects it.

virialized galaxy:
time-averaged volume-memory channel can be silent while the galaxy empirical
pillar is kept separate.

tracefree shear:
theta averages to zero, so scalar volume memory is silent even with shear.
```

Open:

```text
collapse or merger:
dynamic boundary may activate memory.

FLRW perturbations:
background survives, perturbation response still needs a field equation.
```

## 7. Noncircularity Gate

Gate result:

```text
volume_flux_boundary_contract_written     pass
local_zero_boundary_nonarbitrary          pass conditional
FLRW_nonzero_boundary_preserved           pass
bound_domain_parent_variation_derived     fail
virial_average_parent_derived             fail
dynamic_systems_resolved                  open
support_claim_allowed                     fail
```

This is progress, but the red-team verdict is still sharp:

```text
the theorem is kinematic unless a parent action selects D.
```

The theory can now say:

```text
if the physical domain boundary is a stationary/extremal volume-flow boundary,
then local scalar volume memory vanishes.
```

It cannot yet say:

```text
the parent field equations force local bound domains to be exactly those
boundaries.
```

That missing sentence is the next wall.

## 8. Decision

Decision:

```text
bound_domain_boundary_status =
partial_volume_extremum_theorem_not_parent_action
```

Meaning:

```text
the local silence rule is no longer arbitrary at the kinematic level;
the exact domain selector is still not derived;
the local-GR branch remains alive but unpromoted.
```

Decision:

```text
topological_owner_status = still_live_pending_domain_action
```

So this route is neither dead nor claimable. It has narrowed to a very specific
parent-action demand.

## 9. Next Target

Create:

```text
62-domain-field-chiD-action-contract.md
```

Purpose:

```text
introduce the exact contract a domain selector/window field chi_D, boundary
current, or equivalent variational object must satisfy to derive the
volume-extremal boundary instead of assuming it.
```

Pass condition:

```text
chi_D or the boundary current selects dV_D/dtau = 0 for stationary bound
domains and d ln V_D/dtau = 3H for FLRW without referencing PPN residuals.
```

Fail condition:

```text
the boundary remains a closure-only rule chosen after local tests.
```
