# 180 - CMB Kill-Screen or Parent Amplitude Owner Decision

Private route-selection checkpoint. This is not a public claim.

## 1. Trigger

Checkpoints 178 and 179 changed the blocker map:

```text
P06 perturbation outputs:
partial effective owner now exists.

P08 local GR / PPN silence:
screened effective local safety now exists.
```

Neither is parent-promoted, but both are now fenced well enough to ask the next
question:

```text
Do we pressure-test the effective scalar route through CMB spectra,
or return to the parent amplitude problem B_mem = 2/27?
```

## 2. Machine Artifact

Script:

```text
scripts/CMB_kill_screen_or_parent_amplitude_owner_decision.py
```

Run:

```text
runs/20260531-235959-CMB-kill-screen-or-parent-amplitude-owner-decision
```

Command:

```text
python scripts/CMB_kill_screen_or_parent_amplitude_owner_decision.py --timestamp 20260531-235959
```

Status:

```text
decision_prioritize_CMB_engine_readiness_then_kill_screen_keep_amplitude_as_theorem_debt
```

Claim ceiling:

```text
decision_gate_no_CMB_run_no_amplitude_promotion
```

## 3. Decision

Selected next route:

```text
CMB engine readiness, then CMB kill-screen.
```

Deferred route:

```text
another B_mem = 2/27 parent-amplitude derivation attempt.
```

Reason:

```text
P07 is now the next highest-value pressure test because the effective scalar
route has a perturbation owner and local PPN fence, but it has still never faced
TT/TE/EE/lensing/ISW spectra.
```

The amplitude problem is more fundamental, but checkpoint 140 already hit the
current wall:

```text
the endpoint quadratic is clean,
but the charge unit, endpoint arrow, Ward-fixed coefficients, and density
amplitude map are not derived.
```

Without a genuinely new boundary-charge mechanism, another amplitude attempt
risks becoming a numerology loop.

## 4. Current Blocker State

| gate | current status after 179 |
|---|---|
| P04 parent perturbation action | blocking |
| P06 perturbation outputs | partial effective, not parent-cleared |
| P07 CMB Boltzmann interface / spectra | blocking |
| P08 local GR / PPN silence | screened effective, not parent-cleared |
| P09 zero-knob domain selector | blocking |
| P10 `B_mem = 2/27` amplitude owner | blocking |

So the situation is not:

```text
the theory is promoted.
```

It is:

```text
the effective branch is now coherent enough to be stress-tested harder.
```

## 5. Option Scorecard

| option | theory value | empirical falsification value | readiness | decision |
|---|---:|---:|---:|---|
| CMB engine readiness then kill-screen | `8` | `10` | `4` | selected next |
| parent `B_mem = 2/27` amplitude owner | `10` | `4` | `3` | defer until new mechanism |
| broader late-time scoring | `3` | `5` | `8` | defer |
| reopen old local selector route | `5` | `2` | `2` | reject |

The CMB route is selected even though readiness is low, because low readiness
is exactly what checkpoint 181 should fix:

```text
build or fail-cleanly preflight the CMB engine/wrapper.
```

## 6. Environment Snapshot

Current CMB execution readiness:

| item | status |
|---|---|
| `camb` Python module | missing |
| `classy` Python module | missing |
| `class` executable | missing |
| `cobaya` Python module | missing |
| `cmb_kill_screen_long_run.py` | missing |

Therefore:

```text
no CMB spectra run was attempted.
```

The next step is tooling/readiness, not a long run.

## 7. Selected CMB Work Contract

Checkpoint 181 must produce or fail-cleanly on:

| step | required artifact | pass condition |
|---|---|---|
| engine readiness | `181-CMB-engine-readiness-and-dryrun-wrapper.md` | detects available CLASS/CAMB route or writes clean missing-engine status |
| long-run wrapper | `scripts/cmb_kill_screen_long_run.py` | supports `--dry-run`, logs status, enforces locks |
| baseline parity | `baseline_reproduction.csv` | LCDM baseline reproduced before reading MTS |
| MTS kill-screen | `likelihood_scorecard.csv` and `claim_gate_results.csv` | fixed MTS branches scored with no rescue knobs |

The fixed locks remain:

```text
B_mem = 2/27,
p = 3,
u3 = 1/4,
c_s_eff^2 = 1 for high-c_s route,
sigma_mem = 0.
```

## 8. Deferred Amplitude Debt

`B_mem = 2/27` remains:

```text
empirical locked closure and theorem target.
```

It can be reopened only with a new mechanism for:

| debt | needed |
|---|---|
| boundary charge unit | derive `Q_*` before data scoring |
| endpoint coefficients | derive `27` and `12` in `27R^2 - 12R + 1 = 0` |
| endpoint arrow | derive `1/3 -> 1/9` rather than assuming the direction |
| density amplitude map | derive `B_mem = DeltaR/3` from stress or conserved charge |

Until then, amplitude agreement is not a field-theory proof.

## 9. Gate Results

All decision gates passed:

| gate | result |
|---|---|
| all cited sources exist | pass |
| single next option selected | pass |
| `P07` remains blocking | pass |
| `P10` deferred, not promoted | pass |
| no CMB run performed | pass |
| claim ceiling preserved | pass |

## 10. Decision Readout

Decision:

```text
decision_prioritize_CMB_engine_readiness_then_kill_screen_keep_amplitude_as_theorem_debt
```

Meaning:

```text
The next move is to make the CMB kill-screen executable or fail-cleanly
preflighted. The amplitude problem stays on the theorem-debt board, but another
2/27 derivation attempt is not the best next move without a new boundary-charge
idea.
```

Boxing-card readout:

```text
We have the jab legal and the local defence up. Now the fighter has to step
into the CMB round. Not to claim the belt — to see if the footwork still works
when the hardest judge starts scoring.
```

## 11. Next Target

Create:

```text
181-CMB-engine-readiness-and-dryrun-wrapper.md
```

Next task:

```text
Inspect whether CLASS/CAMB/Cobaya can be used locally. If not, create a
fail-clean dry-run wrapper and status workflow. Do not run long spectra until
baseline reproduction and engine readiness pass.
```
