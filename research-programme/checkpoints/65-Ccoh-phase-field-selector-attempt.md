# C_coh Phase-Field Selector Attempt

## 1. Purpose

This file follows:

```text
64-binding-invariant-domain-selector-attempt.md
```

Checkpoint 64 found a useful invariant:

```text
C_coh[D] =
<theta>_D^2 / (<theta^2>_D + <sigma^2>_D + <omega^2>_D + eps_D).
```

It separates coherent FLRW expansion from stationary/virialized local
volume-flow, but does not yet derive binding.

This checkpoint asks:

```text
Can C_coh drive chi_D without hiding a fitted threshold?
```

Short answer:

```text
yes at the level of an explicit selector equation, but not yet at the level of
a complete local-GR derivation.
```

The new problem is:

```text
the selector introduces chi_D stress and a transition length ell_chi.
```

Tiny monster defeated; larger monster unlocked. Standard theory dungeon.

## 2. Machine Run

Implemented:

```text
scripts/Ccoh_phase_field_selector_attempt.py
```

Successful run:

```text
runs/20260531-111502-Ccoh-phase-field-selector-attempt/status.json
```

Readout:

```text
explicit_selector_equation_found_but_new_scale_and_stress_open
```

Generated:

```text
runs/20260531-111502-Ccoh-phase-field-selector-attempt/results/source_checkpoint_register.csv
runs/20260531-111502-Ccoh-phase-field-selector-attempt/results/phase_action_candidates.csv
runs/20260531-111502-Ccoh-phase-field-selector-attempt/results/homogeneous_branch_tests.csv
runs/20260531-111502-Ccoh-phase-field-selector-attempt/results/variation_chain.csv
runs/20260531-111502-Ccoh-phase-field-selector-attempt/results/parameter_risk_register.csv
runs/20260531-111502-Ccoh-phase-field-selector-attempt/results/gate_results.csv
runs/20260531-111502-Ccoh-phase-field-selector-attempt/results/decision.csv
```

## 3. Best Candidate Action

Avoid a hard threshold:

```text
chi_D = Heaviside(C_coh - C_star)
```

because that just moves the handwave into:

```text
C_star.
```

Instead use threshold-free relaxation:

```text
S_chi =
integral sqrt(-g)[
  -kappa_chi/2 h^munu nabla_mu chi nabla_nu chi
  -m_chi^2/2 (chi - C_coh)^2
].
```

Varying chi gives:

```text
kappa_chi D^2 chi - m_chi^2(chi - C_coh) = 0.
```

In the homogeneous limit:

```text
chi = C_coh.
```

This is the important gain:

```text
local/FLRW separation comes from the invariant value, not from a fitted cut.
```

## 4. Branch Tests

Minkowski:

```text
C_coh = 0 -> chi = 0.
```

Stationary local bound domain:

```text
C_coh low -> chi low.
```

Tracefree shear:

```text
theta = 0 -> C_coh = 0 -> chi = 0.
```

FLRW:

```text
sigma = omega = 0
theta = 3H
C_coh = 1
```

so:

```text
chi = 1.
```

This is exactly the branch split we wanted:

```text
stationary local scalar volume-memory suppressed;
coherent FLRW scalar volume-memory active.
```

But collapse/merger remains:

```text
dynamic/open.
```

That is acceptable. It should not be silently folded into PPN.

## 5. New Cost

The action introduces:

```text
ell_chi = sqrt(kappa_chi) / m_chi.
```

This is a transition width.

If:

```text
ell_chi
```

is arbitrary or fitted per system, the route collapses into another smoothing
knob.

The action also introduces:

```text
T_chi_munu.
```

That matters because local GR reduction is not just about suppressing
Q_coh. The new field cannot carry stress that breaks PPN/conservation.

So the current status is:

```text
selector equation exists;
stress and scale are not safe yet.
```

## 6. Gate Result

Gate result:

```text
explicit_variation_obtained          pass
threshold_avoided                    pass
local_FLRW_branch_split              pass kinematic
binding_domain_fully_derived         fail
new_scale_removed                    fail
Bianchi_stress_checked               open
support_claim_allowed                fail
```

This is a real improvement over checkpoint 63:

```text
we now have an actual E_chi candidate.
```

But it is still not enough:

```text
E_chi introduces a new field scale and stress tensor.
```

That is the next red-team gate.

## 7. Decision

Decision:

```text
Ccoh_phase_field_status =
explicit_selector_equation_found_but_new_scale_and_stress_open
```

Meaning:

```text
threshold-free chi=C_coh relaxation separates homogeneous local/FLRW branches;
the mechanism is not yet a local-GR derivation because ell_chi and T_chi are
unbounded.
```

Decision:

```text
local_transition_route_status = improved_but_not_promoted
```

This is the best local route so far:

```text
coherent volume-flow invariant -> threshold-free chi_D equation -> conditional
local silence and FLRW activity.
```

It now has a very specific danger:

```text
does chi_D itself gravitate too much?
```

## 8. Next Target

Create:

```text
66-chiD-stress-and-scale-gate.md
```

Purpose:

```text
derive or bound T_chi and ell_chi so the new selector does not break local GR.
```

Pass condition:

```text
chi_D gradients/source stress are locally negligible or constrained by a
parent conservation identity, while FLRW activation remains possible.
```

Fail condition:

```text
the selector field adds unsuppressed local stress, an arbitrary transition
scale, or a hidden MOND-like length.
```
