# chi_D Variation to Boundary Equation Attempt

## 1. Purpose

This file follows:

```text
62-domain-field-chiD-action-contract.md
```

Checkpoint 62 wrote the contract:

```text
derive E_chi so the same parent rule gives local zero-flux bound domains and
active FLRW domains.
```

This checkpoint attempts that variation.

Short answer:

```text
the minimal chi_D variations do not yet derive the local boundary.
```

The route is not dead, but the bottleneck moved:

```text
chi_D needs a parent-derived binding/coherence invariant.
```

## 2. Machine Run

Implemented:

```text
scripts/chiD_variation_to_boundary_equation_attempt.py
```

Successful run:

```text
runs/20260531-110848-chiD-variation-to-boundary-equation-attempt/status.json
```

Readout:

```text
chiD_variation_fails_as_full_derivation_points_to_binding_invariant
```

Generated:

```text
runs/20260531-110848-chiD-variation-to-boundary-equation-attempt/results/source_checkpoint_register.csv
runs/20260531-110848-chiD-variation-to-boundary-equation-attempt/results/variation_identity_chain.csv
runs/20260531-110848-chiD-variation-to-boundary-equation-attempt/results/candidate_variation_ledger.csv
runs/20260531-110848-chiD-variation-to-boundary-equation-attempt/results/pass_fail_matrix.csv
runs/20260531-110848-chiD-variation-to-boundary-equation-attempt/results/no_go_findings.csv
runs/20260531-110848-chiD-variation-to-boundary-equation-attempt/results/gate_results.csv
runs/20260531-110848-chiD-variation-to-boundary-equation-attempt/results/decision.csv
```

## 3. Variation Identities

Start with:

```text
V_D = integral_Sigma chi_D dSigma.
```

Then:

```text
delta V_D = integral_Sigma delta chi_D dSigma.
```

The domain volume-flow identity is:

```text
dot V_D = integral_Sigma (L_u chi_D + chi_D theta) dSigma.
```

So:

```text
delta dot V_D =
integral_Sigma (L_u delta chi_D + theta delta chi_D) dSigma.
```

If the boundary is merely material/advected:

```text
L_u chi_D = 0,
```

then:

```text
dot V_D = integral_Sigma chi_D theta dSigma.
```

This preserves FLRW nicely:

```text
dot V_D / V_D = theta = 3H.
```

But it does not select which local domains are bound. It just transports the
domain you already chose.

That is the first hard failure:

```text
advection is not selection.
```

## 4. Candidate Variations

Candidate:

```text
pure_advection_window:
S_chi = integral sqrt(-g) lambda u^mu nabla_mu chi_D
```

Euler equation:

```text
u^mu nabla_mu chi_D = 0.
```

Verdict:

```text
useful transport, not a domain selector.
```

Candidate:

```text
divergence_constraint_current:
S_chi = integral sqrt(-g) lambda nabla_mu(chi_D u^mu)
```

Euler equation:

```text
nabla_mu(chi_D u^mu)=0
```

or:

```text
L_u chi_D + chi_D theta = 0.
```

Verdict:

```text
bad for FLRW memory.
```

It tends to absorb or kill the 3H volume growth rather than producing active
cosmological memory.

Candidate:

```text
quadratic_flux_extremal:
S_chi = integral d tau (kappa/2)(dot V_D)^2
```

Euler tendency:

```text
d/dtau(kappa dot V_D)=0.
```

Verdict:

```text
it makes zero flux natural, but FLRW needs an extra source.
```

Without a derived source, this is too engineered.

Candidate:

```text
phase_field_boundary:
S_chi = integral sqrt(-g)[-kappa/2 h^munu nabla_mu chi_D nabla_nu chi_D
                          - U(chi_D,C)]
```

Euler form:

```text
kappa D^2 chi_D - dU/dchi_D = source(C).
```

Verdict:

```text
best surviving route, but only if C is a derived binding/coherence invariant.
```

Candidate:

```text
topological_relative_pairing
```

Verdict:

```text
protects the class after D is known; does not choose D.
```

## 5. No-Go Findings

The attempt found five sharp lessons:

```text
1. Advection is not selection.
2. Current conservation overkills FLRW.
3. Flux-square actions prefer silence unless sourced.
4. Phase-field boundaries need a real binding/coherence invariant.
5. Topology protects the split but does not choose the domain.
```

That means the local branch has not got worse in a vague way. It got narrower.

The next missing object is not:

```text
a prettier boundary field.
```

It is:

```text
C_bind or C_coh
```

a physical invariant that can drive chi_D.

## 6. Gate Result

Gate result:

```text
variation_attempt_performed          pass
zero_flux_bound_boundary_derived     fail
FLRW_active_branch_preserved         pass conditional
noncircular_domain_selector_found    open
closure_promotion_allowed            fail
support_claim_allowed                fail
```

So the parent-action route does not promote yet.

The exact state is:

```text
local zero-volume memory remains conditionally possible;
the boundary selector is still missing;
the least bad next route is a phase-field/domain action driven by a derived
binding/coherence invariant.
```

## 7. Decision

Decision:

```text
chiD_variation_status =
fails_as_full_derivation_points_to_binding_invariant
```

Meaning:

```text
we did not derive the local boundary from chi_D alone;
we did identify the next necessary physical object;
the local-GR route is not dead, but it is not derived.
```

Decision:

```text
local_GR_route_status = not_dead_but_not_derived
```

This is the honest score. It is a miss, but it is a useful miss.

## 8. Next Target

Create:

```text
64-binding-invariant-domain-selector-attempt.md
```

Purpose:

```text
derive or reject a parent binding/coherence invariant C_bind or C_coh that can
drive chi_D without importing GR/Newton by hand.
```

Pass condition:

```text
C_bind/C_coh separates stationary bound local domains from coherent FLRW
domains before data fitting and without PPN tuning.
```

Fail condition:

```text
the invariant is just Newtonian binding energy, GR turnaround, or an empirical
window rule in disguise.
```
