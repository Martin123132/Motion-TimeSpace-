# C_coh Variation and Boundary Current Audit

## 1. Purpose

This file follows:

```text
69-minimal-memory-gate-variation-attempt.md
```

Checkpoint 69 found:

```text
S_gate on shell becomes integral sqrt(-g) C_coh L_mem.
```

That is good because the gate is action-derived, not an external switch.

But it also means:

```text
delta_g C_coh
```

cannot be frozen by hand.

This checkpoint asks:

```text
Can C_coh be varied covariantly without producing an uncontrolled local
boundary source?
```

Short answer:

```text
the dependencies are identifiable, but the boundary/exchange current is not
yet derived.
```

## 2. Machine Run

Implemented:

```text
scripts/Ccoh_variation_and_boundary_current_audit.py
```

Successful run:

```text
runs/20260531-113126-Ccoh-variation-and-boundary-current-audit/status.json
```

Readout:

```text
dependencies_identified_boundary_current_not_derived
```

Generated:

```text
runs/20260531-113126-Ccoh-variation-and-boundary-current-audit/results/source_checkpoint_register.csv
runs/20260531-113126-Ccoh-variation-and-boundary-current-audit/results/variation_dependencies.csv
runs/20260531-113126-Ccoh-variation-and-boundary-current-audit/results/boundary_current_candidates.csv
runs/20260531-113126-Ccoh-variation-and-boundary-current-audit/results/branch_audits.csv
runs/20260531-113126-Ccoh-variation-and-boundary-current-audit/results/gate_results.csv
runs/20260531-113126-Ccoh-variation-and-boundary-current-audit/results/decision.csv
```

## 3. What Varies

The invariant is:

```text
C_coh =
<theta>_D^2 /
(<theta^2>_D + <sigma^2>_D + <omega^2>_D + eps_D).
```

It varies through:

```text
theta
sigma
omega
h_ij
u^mu
domain average D
volume measure
boundary motion
eps_D
```

So this is not a harmless scalar knob.

The dangerous piece is the domain average:

```text
<theta>_D = (1/V_D) integral_D theta dSigma.
```

Varying the domain creates a boundary term.

That boundary term is exactly what checkpoint 69 could not close.

## 4. Current Candidates

Candidate:

```text
bulk_variation_current
```

Meaning:

```text
integrate by parts the variations of theta, sigma, and omega.
```

Risk:

```text
higher-derivative local stress.
```

Candidate:

```text
domain_boundary_current
```

Meaning:

```text
local-to-FLRW transition exchange lives on the boundary of the coherent domain.
```

Risk:

```text
PPN-sized surface stress.
```

Best long-term candidate:

```text
relative_topological_current
```

Meaning:

```text
a closed relative current with trivial stationary local class and nontrivial
FLRW expansion class.
```

This best matches the earlier topology route.

Rejected:

```text
freeze_Ccoh.
```

That would be fake conservation.

## 5. Branch Audit

Quiet local bulk:

```text
C_coh = 0 constant.
```

Conditional pass:

```text
no bulk exchange current.
```

Stationary bound interior:

```text
C_coh low/constant after averaging.
```

Conditional pass:

```text
interior exchange small or absent.
```

FLRW background:

```text
C_coh = 1 by homogeneity.
```

Background pass:

```text
no exchange current in the homogeneous background.
```

But FLRW perturbations are not solved.

Local-to-FLRW boundary:

```text
C_coh varies.
```

Open danger:

```text
exchange current required.
```

This is now the exact obstruction.

## 6. Gate Result

Gate result:

```text
Ccoh_variation_dependencies_identified   pass
freezing_Ccoh_rejected                   pass
quiet_bulk_safe                          pass conditional
FLRW_background_safe                     pass background only
boundary_exchange_current_derived        fail
perturbation_conservation_resolved       open
local_GR_promoted                        fail
support_claim_allowed                    fail
```

So:

```text
bulk looks manageable;
boundary current is missing.
```

The local-GR route cannot promote until this is constructed or replaced.

## 7. Decision

Decision:

```text
Ccoh_variation_status =
dependencies_identified_boundary_current_not_derived
```

Meaning:

```text
C_coh can be constant-safe in ideal local/FLRW bulk branches;
varying boundaries and perturbations require an explicit exchange current;
freezing C_coh is rejected.
```

Decision:

```text
local_GR_route_status =
bulk_safe_boundary_current_bottleneck
```

This is the cleanest statement of where we are:

```text
quiet interiors are plausible;
boundaries and perturbations carry the unsolved conservation load.
```

## 8. Next Target

Create:

```text
71-relative-boundary-current-construction-attempt.md
```

Purpose:

```text
attempt to construct a closed relative boundary current J_rel with trivial
stationary local class and nontrivial FLRW expansion class.
```

Pass condition:

```text
J_rel closes the local-to-FLRW exchange without PPN-sized local boundary stress
and without freezing C_coh.
```

Fail condition:

```text
the current is only a renamed boundary assumption and does not follow from a
conservation/topological identity.
```
