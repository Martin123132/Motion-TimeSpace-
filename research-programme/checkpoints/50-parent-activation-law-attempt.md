# Parent Activation Law Attempt

## 1. Purpose

This file follows:

```text
49-C2-regularized-closure-ledger.md
```

The bottleneck is no longer whether the C2 repair is a useful internal closure
candidate. It is. The bottleneck is whether the activation law:

```text
F(N) = 1 - exp[-(N/u_3)^3]
```

can be derived from a parent memory/load mechanism rather than inserted because
it behaves nicely.

Short answer:

```text
p = 3 is now partially justified as the minimal regularity-selected endpoint
law and as the exact result of a quadratic memory hazard. It is not yet
parent-derived.
```

Tiny victory, still wearing a hard hat.

## 2. Machine Run

Implemented:

```text
scripts/parent_activation_law_attempt.py
```

Successful run:

```text
runs/20260531-032036-parent-activation-law-attempt/status.json
```

Readout:

```text
p3_activation_law_regularly_selected_not_parent_derived
```

Generated:

```text
runs/20260531-032036-parent-activation-law-attempt/results/source_checkpoint_register.csv
runs/20260531-032036-parent-activation-law-attempt/results/activation_law_equation_chain.csv
runs/20260531-032036-parent-activation-law-attempt/results/candidate_parent_derivation_routes.csv
runs/20260531-032036-parent-activation-law-attempt/results/parent_contract_requirements.csv
runs/20260531-032036-parent-activation-law-attempt/results/gate_results.csv
runs/20260531-032036-parent-activation-law-attempt/results/decision.csv
```

## 3. What Can Be Derived

The exact conditional chain is:

```text
F(N) = 1 - exp[-I(N)]
X_FLRW = N/u_3
I(N) = X_FLRW^3
J_M = dI/dN = 3 X_FLRW^2/u_3 = 3 N^2/u_3^3
dF/dN = (1 - F) J_M
```

For the retained C2 branch:

```text
u_3 = 0.2429466120286312
N50 = 0.21500703361675252
p = 3
F'(0) = 0
F''(0) = 0
F'''(0) = 418.426044777509
J_M(0) = 0
J_M'(0) = 0
```

So the p=3 law has a genuine double-zero source/current structure at the
present endpoint. This is not fluff: it is exactly the kind of smooth onset
needed to avoid the scalar regularity failure of the old fractional branch.

## 4. Why p = 3 Is The Minimal Repair

The old fitted fractional branch had:

```text
nu_act = 1.7500073382761008
```

That branch failed the regular scalar-action gate because the endpoint was too
sharp. The p=3 repair is the first no-new-continuous-knob law that gives:

```text
F(0) = 0
F'(0) = 0
F''(0) = 0
finite canonical scalar-potential slope
real branch-local odd-power behaviour
```

This means p=3 is not arbitrary anymore. It is the lowest regularity-safe
integer endpoint if the parent theory demands C2 onset and no extra shape knob.

But this is still a selection argument, not a parent-action derivation.

## 5. Candidate Parent Routes

The five routes tested are:

```text
minimal_regular_endpoint_power       partial selection, not parent derivation
quadratic_memory_hazard              conditional route
cubic_exposure_volume                conditional route
local_double_zero_analogy            analogy, not derivation
direct_parent_action_variation       missing
```

The strongest route is:

```text
J_M = 3 X_FLRW^2 dX_FLRW/dN
```

because integrating it gives:

```text
I = X_FLRW^3
F = 1 - exp[-X_FLRW^3]
```

exactly. The catch is brutal and important: the current itself has not yet been
derived from `psi`, `Gamma`, `C`, `S_memory`, a Noether current, a constraint, or
an action variation.

## 6. What Still Fails

The gate result is:

```text
regularity_selection_derives_p3       pass_partial
survival_law_chain_exact              pass_conditional
p3_parent_dynamics_derived            fail
u3_parent_predicted                   fail
bmem_parent_predicted                 fail
conservation_owner_defined            fail
closure_candidate_retained            pass
support_claim_allowed                 fail
```

So the branch is cleaner, but it is not promoted.

The parent contract still has to supply:

```text
X_FLRW as a real parent scalar;
J_M as a derived memory current;
u_3/N50 as a predicted scale;
b_mem as a predicted amplitude;
Bianchi/conservation ownership;
future-branch/time-arrow handling;
perturbation and lensing response;
local GR/PPN silence.
```

## 7. Decision

Decision:

```text
p3_activation_law_status = regularly_selected_not_parent_derived
```

Meaning:

```text
the p=3 law is no longer just a convenient patch;
it has a disciplined minimal-regularity reason;
it has a clean conditional memory-current equation chain;
it still does not have a parent derivation.
```

The live route is therefore:

```text
derive the FLRW memory current
```

not:

```text
run another nearby cosmology score and pretend that solved the mechanism.
```

The score already said the repaired branch survives well enough to deserve the
derivation attempt. The next job is to make the parent current earn its keep.

## 8. Next Target

Create:

```text
51-FLRW-memory-current-contract.md
```

Purpose:

```text
write the exact contract a parent FLRW memory current must satisfy to derive
J_M = 3 X_FLRW^2 dX_FLRW/dN, X_FLRW = N/u_3, and the branch-local activation law
F = 1 - exp[-X_FLRW^3].
```

Pass condition:

```text
the contract identifies a plausible parent scalar/current/conservation owner
that can later be derived from an action or constraint system.
```

Fail condition:

```text
if no parent current can be named without circularly inserting the answer, the
p=3 route remains an explicit regularized closure benchmark.
```
