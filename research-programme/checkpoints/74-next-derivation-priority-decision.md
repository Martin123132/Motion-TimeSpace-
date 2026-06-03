# Next Derivation Priority Decision

## 1. Purpose

This file follows:

```text
73-local-route-blocker-ledger-and-promotion-gate.md
```

Checkpoint 73 found:

```text
the local route is not promoted.
```

It also named the critical blockers:

```text
bound_domain_rule
Ccoh_parent_ownership
Bianchi_conservation
amplitude_normalization
```

This checkpoint asks:

```text
which blocker should be attacked next?
```

Short answer:

```text
C_coh / Bianchi ownership goes first.
```

Reason:

```text
without it, local GR and perturbations are not credible.
```

## 2. Machine Run

Implemented:

```text
scripts/next_derivation_priority_decision.py
```

Successful run:

```text
runs/20260531-114253-next-derivation-priority-decision/status.json
```

Readout:

```text
next_priority_Ccoh_Bianchi_ownership_first
```

Generated:

```text
runs/20260531-114253-next-derivation-priority-decision/results/source_checkpoint_register.csv
runs/20260531-114253-next-derivation-priority-decision/results/priority_ranking.csv
runs/20260531-114253-next-derivation-priority-decision/results/decision_gates.csv
runs/20260531-114253-next-derivation-priority-decision/results/workplan.csv
runs/20260531-114253-next-derivation-priority-decision/results/decision.csv
```

## 3. Ranking

Rank 1:

```text
Ccoh_Bianchi_ownership
```

Why:

```text
highest promotion value;
clearest failure mode;
unlocks local GR and perturbation equations.
```

Rank 2:

```text
amplitude_normalization_p3_u3_bmem
```

Why second:

```text
critical, but less useful if conservation fails first.
```

Rank 3:

```text
perturbation_lensing_growth_contract
```

Why third:

```text
needed for tests, but premature without Bianchi/Ccoh ownership.
```

Rank 4:

```text
empirical_smoke_test_readiness
```

Why not now:

```text
valuable soon, but it would test a closure with unclear conservation.
```

Rank 5:

```text
more_topological_current_subbranches
```

Why last:

```text
checkpoint 73 already says topology is support, not the decisive blocker.
```

## 4. Decision

Decision:

```text
next_priority = Ccoh_Bianchi_ownership_first
```

Meaning:

```text
we should now attack whether C_coh can be a parent variational object and
whether S_gate = C_coh L_mem can satisfy a real Noether/Bianchi identity.
```

Defer:

```text
amplitude normalization
```

until after the conservation gate.

Defer:

```text
empirical tests
```

until we have equations whose failures can be interpreted.

## 5. Workplan

Next three checkpoints:

```text
75-Ccoh-parent-variation-contract.md
76-Ccoh-Bianchi-identity-attempt.md
77-local-route-demote-or-continue-gate.md
```

The point is not to keep the local route alive at all costs.

The point is:

```text
derive it or demote it cleanly.
```

## 6. Next Target

Create:

```text
75-Ccoh-parent-variation-contract.md
```

Purpose:

```text
write the exact parent-variable contract for theta, sigma, omega, domain
averages, observer congruence, eps_D, and metric variation inside C_coh.
```

Pass condition:

```text
all C_coh dependencies have variational owners or are explicitly demoted.
```

Fail condition:

```text
C_coh remains a frozen diagnostic inserted into the action by hand.
```
