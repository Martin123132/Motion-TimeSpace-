# C_coh Bianchi Identity Attempt

## 1. Purpose

This file follows:

```text
75-Ccoh-parent-variation-contract.md
```

Checkpoint 75 wrote the dependency contract for:

```text
C_coh[D] =
<theta>_D^2 /
(<theta^2>_D + <sigma^2>_D + <omega^2>_D + eps_D).
```

This checkpoint asks:

```text
Can S_gate = integral sqrt(-g) C_coh L_mem satisfy a real Noether/Bianchi
identity?
```

Short answer:

```text
partially in formal structure, not in full closure.
```

The obstruction is now explicit:

```text
C_coh exchange can conserve only if parent equations for u, D, and Q exist.
```

## 2. Machine Run

Implemented:

```text
scripts/Ccoh_Bianchi_identity_attempt.py
```

Successful run:

```text
runs/20260531-114923-Ccoh-Bianchi-identity-attempt/status.json
```

Readout:

```text
partial_Noether_structure_but_no_full_closure
```

Generated:

```text
runs/20260531-114923-Ccoh-Bianchi-identity-attempt/results/source_checkpoint_register.csv
runs/20260531-114923-Ccoh-Bianchi-identity-attempt/results/noether_attempt_chain.csv
runs/20260531-114923-Ccoh-Bianchi-identity-attempt/results/branch_identity_tests.csv
runs/20260531-114923-Ccoh-Bianchi-identity-attempt/results/closure_options.csv
runs/20260531-114923-Ccoh-Bianchi-identity-attempt/results/gate_results.csv
runs/20260531-114923-Ccoh-Bianchi-identity-attempt/results/decision.csv
```

## 3. Noether Structure

Use:

```text
S_gate =
integral sqrt(-g) C_coh[g,u,D] L_mem[g,u,Q,...].
```

The stress is schematically:

```text
T_gate =
C_coh T_mem
+ L_mem T_Ccoh
+ mixed field-equation terms.
```

Under diffeomorphism variation:

```text
nabla_mu T_gate^munu =
E_Q L_xi Q
+ E_u L_xi u
+ E_D L_xi D
+ E_mem L_xi fields.
```

So the `delta C_coh` terms are not automatically anomalies.

They can be part of:

```text
E_u
E_D
boundary/exchange equations.
```

That is the partial success.

## 4. What Fails

The problem is:

```text
E_u and E_D are not derived.
```

The theory currently has no parent equations that fully own:

```text
observer congruence u
domain average D
boundary motion
Q/memory dynamics
```

So the Noether structure says:

```text
this could conserve if the missing parent system exists.
```

It does not say:

```text
this conserves now.
```

That distinction is the whole point.

## 5. Branch Tests

Quiet local bulk:

```text
C_coh = 0 constant.
```

Passes at contract level:

```text
S_gate = 0.
```

Stationary bound interior:

```text
C_coh low/constant.
```

Passes conditionally if:

```text
E_D holds and the domain average is stationary.
```

FLRW background:

```text
C_coh = 1 constant.
```

Passes background contract:

```text
S_gate = L_mem.
```

But:

```text
FLRW perturbations
local-to-FLRW boundaries
```

remain fail/open.

Those are exactly the branches that matter for real conservation and tests.

## 6. Closure Options

Best if available:

```text
full_variational_owner
```

Meaning:

```text
E_g, E_u, E_D, and E_Q jointly close the Noether identity.
```

Live but risky:

```text
constrained_auxiliary_owner
```

Meaning:

```text
multiplier equations absorb C_coh exchange.
```

Safe demotion:

```text
pure_diagnostic_Ccoh
```

Meaning:

```text
C_coh is used only after solving parent equations, not inside the action.
```

Rejected:

```text
frozen_action_Ccoh
```

because it gives fake conservation.

## 7. Gate Result

Gate result:

```text
Noether_structure_identified      pass
frozen_Ccoh_rejected_again        pass
quiet_bulk_identity               pass conditional
FLRW_background_identity          pass contract
boundary_identity                 fail open
perturbation_identity             fail open
full_Bianchi_closure              fail
local_GR_promoted                 fail
support_claim_allowed             fail
```

So:

```text
formal Noether route exists;
full Bianchi closure does not.
```

## 8. Decision

Decision:

```text
Ccoh_Bianchi_status =
partial_Noether_structure_but_no_full_closure
```

Meaning:

```text
C_coh exchange can be conserved only if u, D, and Q parent equations exist;
boundary and perturbation branches fail/open now;
local GR is not derived.
```

Decision:

```text
local_route_status =
demote_or_construct_parent_uD_owner
```

The local route is now at a fork:

```text
either build the parent u/D owner;
or demote this local route to closure-level support.
```

## 9. Next Target

Create:

```text
77-local-route-demote-or-continue-gate.md
```

Purpose:

```text
decide whether to keep pushing the local derivation by constructing a parent
u/D owner, or demote the local route to closure-only and move to another
critical blocker.
```

Pass condition:

```text
the next path has a clear derivation target and failure mode.
```

Fail condition:

```text
we keep treating conditional bulk silence as derived local GR.
```
