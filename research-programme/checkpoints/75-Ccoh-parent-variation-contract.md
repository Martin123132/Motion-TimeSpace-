# C_coh Parent Variation Contract

## 1. Purpose

This file follows:

```text
74-next-derivation-priority-decision.md
```

Checkpoint 74 selected:

```text
C_coh / Bianchi ownership
```

as the next highest-value blocker.

This checkpoint asks:

```text
what must be varied if C_coh appears inside the action?
```

Short answer:

```text
all C_coh dependencies can be named, but the variation is not computed yet.
```

That means checkpoint 76 has a precise target instead of a fog bank.

## 2. Machine Run

Implemented:

```text
scripts/Ccoh_parent_variation_contract.py
```

Successful run:

```text
runs/20260531-114606-Ccoh-parent-variation-contract/status.json
```

Readout:

```text
contract_written_variation_not_computed
```

Generated:

```text
runs/20260531-114606-Ccoh-parent-variation-contract/results/source_checkpoint_register.csv
runs/20260531-114606-Ccoh-parent-variation-contract/results/dependency_contract.csv
runs/20260531-114606-Ccoh-parent-variation-contract/results/variation_obligations.csv
runs/20260531-114606-Ccoh-parent-variation-contract/results/owner_options.csv
runs/20260531-114606-Ccoh-parent-variation-contract/results/gate_results.csv
runs/20260531-114606-Ccoh-parent-variation-contract/results/decision.csv
```

## 3. Dependency Contract

The invariant is:

```text
C_coh[D] =
<theta>_D^2 /
(<theta^2>_D + <sigma^2>_D + <omega^2>_D + eps_D).
```

If this enters:

```text
S_gate = integral sqrt(-g) C_coh L_mem,
```

then the following cannot be frozen:

```text
observer congruence u^mu
spatial metric h_munu
theta
sigma
omega
domain average D
volume measure dSigma
eps_D quiet-limit prescription
boundary motion
```

Each one needs a parent owner.

Otherwise:

```text
C_coh is a diagnostic, not an action variable.
```

## 4. Required Variations

Required:

```text
delta_g C_coh
delta_u C_coh
delta_D C_coh
```

The metric variation must include:

```text
h_munu
dSigma
theta/sigma/omega norms
boundary support
```

The congruence variation must include:

```text
u^mu
normalization constraint
observer/frame equation
```

The domain variation must produce:

```text
boundary/exchange current
```

not:

```text
frozen D by hand.
```

## 5. Owner Options

Best if successful:

```text
full_variational_u_chiD_owner
```

Meaning:

```text
u_mu, chi_D/domain, and g_munu are all varied;
C_coh is composite but fully variational.
```

Live but risky:

```text
constrained_auxiliary_owner
```

Meaning:

```text
u_mu and chi_D are constrained/nonpropagating variables.
```

Demotion option:

```text
pure_diagnostic_Ccoh
```

Meaning:

```text
C_coh is used only after solving the parent equations.
```

Rejected:

```text
frozen_Ccoh_in_action
```

because that gives a fake Bianchi identity.

## 6. Gate Result

Gate result:

```text
dependencies_listed           pass
frozen_Ccoh_rejected          pass
parent_owners_available       open
local_bulk_limit_specified    pass conditional
FLRW_limit_specified          pass contract
metric_variation_ready        fail
Bianchi_attempt_ready         pass
local_GR_promoted             fail
support_claim_allowed         fail
```

So:

```text
we are ready to attempt the Bianchi identity;
we have not solved it.
```

## 7. Decision

Decision:

```text
Ccoh_parent_variation_status =
contract_written_variation_not_computed
```

Meaning:

```text
all C_coh dependencies and required variations are named;
no full delta_g/delta_u/delta_D calculation exists yet;
local GR is not promoted.
```

Decision:

```text
local_route_status =
eligible_for_Bianchi_attempt_not_promotion
```

This is the right state:

```text
the next step is a real conservation attempt, not more scaffolding.
```

## 8. Next Target

Create:

```text
76-Ccoh-Bianchi-identity-attempt.md
```

Purpose:

```text
attempt Noether/Bianchi closure for S_gate = C_coh L_mem with C_coh variation
included.
```

Pass condition:

```text
exchange terms organize into a conserved total stress or fail cleanly.
```

Fail condition:

```text
C_coh cannot appear in the action without freezing variables or generating
uncontrolled local exchange stress.
```
