# Binding-Invariant Domain Selector Attempt

## 1. Purpose

This file follows:

```text
63-chiD-variation-to-boundary-equation-attempt.md
```

Checkpoint 63 found:

```text
advection transports chi_D but does not select the physical domain.
```

It also found that the best surviving route needs:

```text
C_bind or C_coh
```

a parent binding/coherence invariant that can drive the domain selector without
importing Newtonian binding energy, GR turnaround, or a fitted data window.

Short answer:

```text
we found a useful coherent-expansion invariant, not a full binding derivation.
```

That is progress, but not promotion.

## 2. Machine Run

Implemented:

```text
scripts/binding_invariant_domain_selector_attempt.py
```

Successful run:

```text
runs/20260531-111219-binding-invariant-domain-selector-attempt/status.json
```

Readout:

```text
coherent_expansion_invariant_found_not_binding_derivation
```

Generated:

```text
runs/20260531-111219-binding-invariant-domain-selector-attempt/results/source_checkpoint_register.csv
runs/20260531-111219-binding-invariant-domain-selector-attempt/results/candidate_invariant_ledger.csv
runs/20260531-111219-binding-invariant-domain-selector-attempt/results/invariant_equation_chain.csv
runs/20260531-111219-binding-invariant-domain-selector-attempt/results/arena_separation_tests.csv
runs/20260531-111219-binding-invariant-domain-selector-attempt/results/nonimport_tests.csv
runs/20260531-111219-binding-invariant-domain-selector-attempt/results/gate_results.csv
runs/20260531-111219-binding-invariant-domain-selector-attempt/results/decision.csv
```

## 3. Rejected Binding Imports

Rejected:

```text
Newtonian_binding_energy
GR_turnaround_surface
empirical_domain_score
```

Why:

```text
Newtonian binding energy imports the lower-limit theory.
GR turnaround imports the reduction we are trying to derive.
empirical domain scoring is just data-tuned windowing.
```

Those routes may be useful later as comparison baselines. They cannot be the
parent selector.

## 4. Best Candidate

The best candidate is not literal binding energy.

It is:

```text
coherent_volume_flow_purity
```

Define the motion-congruence decomposition:

```text
Theta_ij = (1/3) theta h_ij + sigma_ij
```

with vorticity:

```text
omega_ij
```

Then define:

```text
C_coh[D] =
<theta>_D^2 / (<theta^2>_D + <sigma^2>_D + <omega^2>_D + eps_D).
```

Dynamic signed version:

```text
C_exp[D] = sign(<theta>_D) C_coh[D].
```

Interpretation:

```text
C_coh measures how much of the domain motion is coherent volume expansion
rather than shear, rotation, or virial/orbital internal motion.
```

This is attractive because it uses the MTS-style ingredients:

```text
motion
time
space
volume flow
coherence
```

rather than:

```text
Newtonian potential
GR turnaround radius
fitted observational residuals
```

Tiny gremlin note: this is the first local selector candidate that actually
looks like it belongs to the theory instead of being borrowed from the
neighbours.

## 5. Arena Separation

FLRW:

```text
sigma = 0
omega = 0
theta = 3H
```

so:

```text
C_coh approximately 1
C_exp approximately +1
```

Stationary local bound domain:

```text
<theta>_D approximately 0
```

even if:

```text
sigma and omega are nonzero.
```

So:

```text
C_coh low
```

Tracefree shear:

```text
theta = 0, sigma nonzero -> C_coh = 0.
```

Virialized galaxy:

```text
time-averaged <theta>_D approximately 0
```

so the local scalar volume-memory channel can remain inactive while the galaxy
empirical pillar is kept separate.

Collapse or merger:

```text
C_exp can become mixed or negative.
```

That branch remains open. It should not be forced into local silence.

## 6. What This Does and Does Not Prove

This does prove a useful kinematic separation:

```text
FLRW coherent expansion is high C_coh;
stationary local/virial/shear domains are low C_coh.
```

It avoids the worst imports:

```text
no Newtonian potential;
no GR turnaround radius;
no PPN residual tuning.
```

But it does not yet prove:

```text
the physical domain D;
the averaging rule;
the eps_D limiting prescription;
the phase-field potential U(chi_D,C_coh);
the Bianchi-compatible stress;
the memory amplitude.
```

Most importantly:

```text
C_coh classifies coherent expansion purity.
It does not yet derive gravitational binding.
```

That is the honest boundary.

## 7. Gate Result

Gate result:

```text
candidate_invariant_identified       pass
Newton_GR_import_avoided             pass partial
FLRW_local_separation                pass kinematic
binding_selector_derived             fail
chiD_drive_ready                     open
support_claim_allowed                fail
```

So the status is:

```text
candidate invariant found;
binding/domain derivation not complete.
```

This is a better failure mode than before. Instead of asking for a vague
domain selector, the theory can now test:

```text
can C_coh drive chi_D through a real phase-field action?
```

## 8. Decision

Decision:

```text
binding_invariant_status =
coherent_expansion_invariant_found_not_binding_derivation
```

Meaning:

```text
C_coh/C_exp distinguish FLRW coherent expansion from stationary local volume
flow without Newtonian potential or GR turnaround;
they do not yet derive bound domains or local GR.
```

Decision:

```text
local_GR_route_status = alive_with_new_bottleneck
```

This is the current shape of the branch:

```text
local silence -> volume-flow theorem -> chi_D action -> C_coh driver
```

The first two are conditionally good. The last two still need derivation.

## 9. Next Target

Create:

```text
65-Ccoh-phase-field-selector-attempt.md
```

Purpose:

```text
test whether a minimal phase-field action U(chi_D,C_coh) can produce bound
local inactive domains and FLRW active domains without a fitted threshold.
```

Pass condition:

```text
the action admits low-C_coh stationary domains with Q_coh = 0 and high-C_coh
FLRW domains with Q_coh active, using universal parameters only.
```

Fail condition:

```text
the phase-field potential simply hides a tunable empirical threshold.
```
