# 371 - WEP Species Universality Or Active eta Runner

Private WEP-gate checkpoint. This is not a public WEP, clock, PPN, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 370 mapped common-mode `phi_C`.

That helped clock, gamma, and fifth-force pressure.

But it did not solve the hardest ready local gate:

```text
eta_WEP = 2.8e-15.
```

The WEP question is:

```text
does the parent theory force all species to see the same class function F(C_D),
or can species see F_A(C_D)?
```

Answer:

```text
representative invariance forbids direct representative vertices,
but it does not derive species universality.
```

Therefore:

```text
eta_WEP remains active as the hardest ready local gate.
```

## 2. Machine Artifact

Script:

```text
scripts/WEP_species_universality_or_active_eta_runner.py
```

Run:

```text
runs/20260601-225000-WEP-species-universality-or-active-eta-runner
```

Outputs:

```text
results/source_register.csv
results/universality_routes.csv
results/WEP_vertex_audit.csv
results/eta_runner_update.csv
results/active_eta_formulas.csv
results/failure_modes.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
species_universality_not_parent_derived_eta_WEP_remains_active_hardest_ready_gate
```

Claim ceiling:

```text
WEP_species_gate_only_no_WEP_clock_PPN_EH_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. Main Result

Lifted-`C` representative invariance gives:

```text
matter cannot depend on B_perp, b_2, scalar Cperp, or local representative data
```

if that symmetry is parent-owned.

That is a real improvement.

But species-dependent class functions:

```text
F_A(C_D)
```

are still representative-invariant.

So representative invariance alone does not force:

```text
F_A(C_D) = F_B(C_D)
```

for all species.

That is the missing WEP theorem.

## 4. Route Audit

| Route | Result | Why |
|---|---|---|
| representative invariance | conditional pass but insufficient | permits species-specific `F_A(C_D)` |
| single observed coframe | conditional pass if parent-selected | kills species split but is not derived |
| minimal metric coupling | closure/external principle | powerful but not an MTS derivation yet |
| species charge forbidden | required rule | no parent symmetry forbids all labels yet |
| common-mode `phi_C` silence | irrelevant to species split | helps clock/gamma, not WEP universality |

This is the key distinction:

```text
common-mode silence is not the same as species universality.
```

Even if local `phi_C` is perfectly constant, WEP still fails if different species carry different class functions.

## 5. WEP Vertex Audit

| Vertex | Representative invariant? | WEP status |
|---|---|---|
| `ghat_A = exp(F_A(C_D))g` | yes | fails unless `F_A` is universal |
| `m_A(C_D)` | yes | fails unless no species-dependent class mass response |
| `alpha_EM,A(C_D)` | yes | clock/composition risk |
| `B_perp O_A`, `b_2 O_A`, `Cperp O_A` | no | conditionally forbidden by lifted-`C` symmetry |
| universal `sum_A S_A[psi_A, exp(F(C_D))g]` | yes | conditional direct-WEP safe branch |

This means the lifted symmetry kills one class of WEP dangers:

```text
representative vertices.
```

But it does not kill:

```text
species-specific class response.
```

## 6. Active eta Runner

The active symbolic row is:

```text
eta_WEP ~ c_AB Delta F_AB + c_rep eps_rep + c_m Delta m_A(C_D).
```

where:

```text
Delta F_AB = F_A(C_D) - F_B(C_D).
```

The source-locked budget is:

```text
eta_WEP <= 2.8e-15.
```

If three unit-scale unknown terms share the budget:

```text
each term must sit below 9.33e-16.
```

That is not a pass.

It is a pressure estimate.

Current runner status:

```text
active_hardest_ready_gate_no_pass.
```

## 7. Failure Modes

The main traps are:

| Failure | Consequence |
|---|---|
| treating representative invariance as WEP | false WEP pass |
| assuming one metric instead of deriving it | closure hidden as theorem |
| allowing clock constants to depend on `C_D` | clock/redshift and composition residuals return |
| treating local `phi_C=0` as species universality | eta_WEP remains unsolved |

This checkpoint prevents the most dangerous overclaim:

```text
we killed Cperp vertices, therefore WEP is safe.
```

No.

Only one part of the WEP problem is conditionally killed.

## 8. Decision

Decision:

```text
species_universality_not_parent_derived_eta_WEP_remains_active_hardest_ready_gate
```

Meaning:

```text
representative invariance forbids direct representative vertices,
but does not derive universal F(C_D) across species.
```

Therefore:

```text
eta_WEP stays active at the 2.8e-15 source-locked scale.
```

No promotion:

```text
WEP not passed,
clock not passed,
PPN not passed,
Einstein-Hilbert exterior not derived,
local GR not derived.
```

## 9. Next Target

Next:

```text
372 - Local phi_C Zero Theorem Or Gradient Bound
```

Aim:

```text
derive strict local class silence grad(phi_C)=0,
or bound r_grad against clock/gamma budgets.
```

WEP remains active either way.

But the next fair round is:

```text
can the common-mode class metric survive clock and gamma pressure?
```
