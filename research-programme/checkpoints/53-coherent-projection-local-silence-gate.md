# Coherent Projection Local-Silence Gate

## 1. Purpose

This file follows:

```text
52-load-tensor-origin-attempt.md
```

The previous checkpoint found a partial kinematic origin for:

```text
Q^i_j = (1/u_3) integral_t^t0 Theta^i_j d tau.
```

That works beautifully in FLRW, but it is dangerous if full anisotropic local
deformation can enter `det(Q)`. This checkpoint asks:

```text
Can the theory keep coherent FLRW expansion memory while suppressing local
stationary, virialized, and shear-only hair?
```

Short answer:

```text
yes conditionally: keep only domain-averaged coherent volume expansion,
P_coh[Theta]^i_j = (1/3)<theta>_D delta^i_j, where <theta>_D=d ln V_D/dtau.
```

That is not a full derivation, but it is not random either. It is a real
candidate rule with teeth.

## 2. Machine Run

Implemented:

```text
scripts/coherent_projection_local_silence_gate.py
```

Successful run:

```text
runs/20260531-103107-coherent-projection-local-silence-gate/status.json
```

Readout:

```text
coherent_projection_retained_conditional_not_parent_derived
```

Generated:

```text
runs/20260531-103107-coherent-projection-local-silence-gate/results/source_checkpoint_register.csv
runs/20260531-103107-coherent-projection-local-silence-gate/results/projection_candidate_ledger.csv
runs/20260531-103107-coherent-projection-local-silence-gate/results/coherent_projection_equation_chain.csv
runs/20260531-103107-coherent-projection-local-silence-gate/results/local_silence_gate_tests.csv
runs/20260531-103107-coherent-projection-local-silence-gate/results/circularity_tests.csv
runs/20260531-103107-coherent-projection-local-silence-gate/results/gate_results.csv
runs/20260531-103107-coherent-projection-local-silence-gate/results/decision.csv
```

## 3. Best Projector

Decompose the spatial expansion tensor:

```text
Theta_ij = (1/3) theta h_ij + sigma_ij.
```

Use the domain-volume identity:

```text
<theta>_D = (1/V_D) dV_D/dtau = d ln V_D/dtau.
```

Then define:

```text
P_coh[Theta]^i_j = (1/3)<theta>_D delta^i_j.
```

and:

```text
Q_coh^i_j = (1/u_3) integral_t^t0 P_coh[Theta]^i_j d tau.
```

This means the memory determinant is not responding to arbitrary local shear.
It responds to coherent volume growth.

That is the right kind of object if MTS is supposed to distinguish:

```text
cosmological expansion memory
```

from:

```text
local bound-system motion.
```

## 4. FLRW Preservation

In FLRW:

```text
<theta>_D = 3H.
```

Therefore:

```text
Q_coh^i_j = (N/u_3) delta^i_j.
```

So the previous activation route survives:

```text
I_M = det(Q_coh) = (N/u_3)^3
J_M = dI_M/dN = 3N^2/u_3^3
F = 1 - exp[-(N/u_3)^3].
```

Good: the projector does not murder the cosmology branch in its sleep. Very
polite of it.

## 5. Local Silence

The local gate tests say:

```text
Minkowski patch                      pass
stationary solar-system domain       pass conditional
virialized galaxy domain             pass conditional
tracefree shear                      pass conditional
collapse or merger                   open
FLRW perturbations                   open
```

The key rule is:

```text
if dV_D/dtau = 0, then <theta>_D = 0, so Q_coh = 0.
```

That makes stationary and virialized systems plausibly silent in this memory
channel without needing to tune a PPN residual by hand.

But this is still conditional because the parent theory has not yet defined:

```text
the domain D;
the bound/unbound criterion;
the coarse-graining scale;
the action or conservation owner.
```

## 6. What This Fixes

This checkpoint rejects the dangerous option:

```text
use full accumulated Theta^i_j in det(Q).
```

Why?

```text
full Q can react to anisotropic shear, collapse, or local deformation and
therefore risks local PPN hair.
```

The retained option is narrower:

```text
volume-expansion memory only.
```

That preserves the FLRW route while giving a plausible reason local bound
systems do not activate the same memory determinant.

## 7. What Still Fails

Gate result:

```text
nonarbitrary_coherent_projection_identified   pass_partial
FLRW_activation_preserved                     pass
stationary_local_silence                      pass_conditional
anisotropic_tracefree_safety                  pass_conditional
bound_domain_D_parent_defined                 fail
dynamic_local_systems_safe                    open
u3_parent_predicted                           fail
parent_action_or_conservation_owner           fail
support_claim_allowed                         fail
```

So the local safety problem is reduced, not solved.

The two biggest missing pieces are now:

```text
derive the domain/coherence scale;
derive u_3 rather than inheriting it from the closure.
```

## 8. Decision

Decision:

```text
coherent_projection_status = conditional_projector_retained_not_parent_derived
```

Meaning:

```text
P_coh is physically motivated by domain-volume expansion;
it keeps FLRW memory;
it suppresses stationary and virialized local systems conditionally;
it blocks the worst full-Q local-hair route;
it still needs a parent-derived domain and scale.
```

This is good progress. The branch is not asking for magic silence anymore; it
is asking for a concrete coherence/domain theorem.

## 9. Next Target

Create:

```text
54-coherent-domain-and-u3-origin.md
```

Purpose:

```text
try to derive the coarse-graining domain D and the transition scale u_3 from a
parent coherence, cell-volume, horizon, or bound/unbound rule.
```

Pass condition:

```text
D and u_3 are predicted or tightly constrained by parent variables rather than
chosen to save the local tests or match the cosmology fit.
```

Fail condition:

```text
D and u_3 can only be selected after looking at the desired cosmology/local
outcome.
```
