# 368 - Common-Mode Class-Metric Clock / PPN Residual Gate

Private residual-gate checkpoint. This is not a public WEP, clock, PPN, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 367 demoted the local-GR route to:

```text
labelled class-metric closure plus residual testing.
```

This checkpoint turns that into a local scorecard.

The class-metric branch is:

```text
ghat_mn = exp(phi_C) g_mn
phi_C = lambda C_D or lambda P_D C.
```

The question is no longer:

```text
is local GR derived?
```

It is:

```text
what residuals must this labelled branch survive before we treat it as locally safe?
```

Answer:

```text
clock, PPN gamma/beta, WEP/species universality, fifth-force/domain channels,
preferred-frame markers, and the EH exterior operator all remain active gates.
```

No local-bound pass is claimed.

## 2. Machine Artifact

Script:

```text
scripts/common_mode_class_metric_clock_PPN_residual_gate.py
```

Run:

```text
runs/20260601-215000-common-mode-class-metric-clock-PPN-residual-gate
```

Outputs:

```text
results/source_register.csv
results/class_metric_model.csv
results/source_locked_targets.csv
results/residual_gate_matrix.csv
results/baseline_rules.csv
results/derivation_debts.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
class_metric_residual_gate_written_no_local_bound_pass_coefficients_and_source_locks_still_open
```

Claim ceiling:

```text
residual_gate_only_no_WEP_clock_PPN_EH_or_local_GR_promotion
```

Source paths missing:

```text
0
```

## 3. Class-Metric Residual Model

Use the branch:

```text
ghat_mn = exp(phi_C) g_mn.
```

Define a local common-mode pressure ratio:

```text
r_grad = |grad phi_C| / |grad U_GR|.
```

This is not a derived coefficient.

It is the object the branch has to make small, zero, or absorbed.

The dangerous possibilities are:

```text
local gradients of phi_C,
local drift of phi_C,
hidden species-specific F_A(C_D),
direct representative vertices,
domain marker / preferred-frame leakage,
non-EH exterior operators.
```

The representative-invariant branch forbids direct `B_perp/b_2/Cperp` vertices conditionally.

It does not automatically remove common-mode `phi_C` gradients.

That is the key local test pressure.

## 4. Source-Locked Targets

The ready internal target scales are inherited from checkpoints 354 and 359:

| Residual | Source-locked scale | Status |
|---|---:|---|
| `gamma_minus_1` | `2.3e-5` | ready internal target |
| `beta_minus_1` | `7.8e-5` | ready internal target |
| `eta_WEP` | `2.8e-15` | ready internal target |
| `alpha_clock_redshift` | `3.1e-5` | ready internal target |
| preferred-frame `alpha1/alpha2` | not locked here | quarantined |
| preferred-location / anisotropy `xi` | not locked here | quarantined |
| `delta_G` / fifth force | not locked here | quarantined |

The point is discipline:

```text
ready sectors get budgets,
quarantined sectors do not get fake scores.
```

## 5. Residual Gate Matrix

| Gate | Branch source | Target | Current status |
|---|---|---|---|
| common-mode clock/redshift | local drift/gradient of `phi_C` | `3.1e-5` | open, no pass |
| PPN `gamma` | class metric response relative to GR potential | `2.3e-5` | open, no pass |
| PPN `beta` | second-order `phi_C` and exterior operator terms | `7.8e-5` | open, no pass |
| WEP/species universality | hidden `F_A(C_D)` or representative vertices | `2.8e-15` | open, hardest ready gate |
| fifth force / `delta_G` | `grad phi_C`, boundary events, bulk/domain fields | quarantined | no numeric pass |
| preferred-frame / anisotropy | marker fields or noncovariant projector/domain selection | quarantined | no numeric pass |
| EH exterior operator | retained non-EH local dynamics | indirect | open |

This is the rule:

```text
if coefficients are missing, the row is a gate,
not a pass.
```

## 6. Baseline Rules

The branch must be compared properly:

| Baseline rule | Meaning |
|---|---|
| GR local baseline | `gamma=beta=1`, no WEP/clock violation is the comparison target, not proof MTS reaches it |
| closure vs GR | score the class-metric residual vector with closure labels visible |
| stress-test symmetry | if a stress test applies to GR/LCDM too, define the baseline result too |
| empirical survival is not derivation | fit success does not upgrade closure into local GR |

This matters because a failed stress pipeline can fool us both ways.

If the baseline fails too, the code/test is suspect.

If only MTS fails, the branch owes a repair or demotion.

## 7. Current Readout

The class-metric closure has useful structure:

```text
direct representative vertices can be forbidden by lifted-class symmetry.
```

But the local safety gates remain:

```text
derive or bound phi_C local gradients,
prove species universality,
source-lock quarantined sectors,
separate EH exterior residuals,
stress edge cases for local/FLRW class split.
```

So the readout is:

```text
not dead,
not promoted,
ready for a source-locked residual runner.
```

That is exactly where this branch should be now.

## 8. Derivation Debts

| Debt | Why |
|---|---|
| derive or bound `phi_C` local gradient | feeds clock, gamma, beta, fifth-force pressure |
| prove species universality | WEP scale is `2.8e-15`, brutally tight |
| source-lock quarantined sectors | preferred-frame, `xi`, and fifth-force need dedicated bounds |
| separate EH operator residual | matter selector does not prove Einstein-Hilbert dynamics |
| test class-split edge cases | horizons, galaxies, time-dependent local systems, ordinary baths can break the split |

This is no longer vague.

It is a worklist.

## 9. Decision

Decision:

```text
class_metric_residual_gate_written_no_local_bound_pass_coefficients_and_source_locks_still_open
```

Meaning:

```text
the labelled class-metric branch has a concrete local residual gate,
but every pass claim is blocked by missing coefficients,
common-mode bounds,
species universality,
quarantined source locks,
and EH operator debt.
```

No promotion:

```text
WEP/clock/PPN not passed,
fifth-force not scored,
Einstein-Hilbert exterior not derived,
local GR not derived.
```

## 10. Next Target

Next:

```text
369 - Source-Locked Closure-Branch Local-Bound Runner
```

Aim:

```text
turn this residual gate into a runner matrix:
ready sectors scored as budgets,
quarantined sectors retained,
missing coefficients blocking pass claims.
```

That is the right testing move.

The branch has left the “can we derive it today?” corner and entered the “can it survive a fair scorecard?” round.
