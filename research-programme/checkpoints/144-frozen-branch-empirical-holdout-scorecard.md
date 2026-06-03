# 144 - Frozen Branch Empirical Holdout Scorecard

Private empirical checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 143 fenced the clean theory-promotion route:

```text
D is not yet selected by a zero-knob parent action.
```

So this checkpoint pivots to the fair boxing-card question:

```text
If B_mem = 2/27 is frozen and not refit, how many empirical rounds does the branch actually survive?
```

Short answer:

```text
late-time evidence survives as a competitive empirical closure.
CMB bridge evidence is unresolved / not promoted.
```

This is not a knockout claim. It is a judge's-card checkpoint.

## 2. Machine Artifact

Script:

```text
research-programme\scripts\frozen_branch_empirical_holdout_scorecard.py
```

Run:

```text
research-programme\runs\20260531-214500-frozen-branch-empirical-holdout-scorecard
```

Generated:

```text
source_register.csv
evidence_scorecard.csv
baseline_fairness_ledger.csv
claim_limited_scorecard.csv
holdout_gates.csv
gate_results.csv
next_holdout_queue.csv
decision.csv
status.json
```

Status:

```text
frozen_branch_empirical_scorecard_late_time_survives_CMB_bridge_unresolved
```

Claim ceiling:

```text
frozen_locked_branch_empirical_scorecard_no_theory_promotion
```

## 3. Frozen Branch Rule

This scorecard treats:

```text
B_mem = 2/27 = 0.07407407407407407
```

as frozen.

That means:

```text
no branch-by-branch amplitude refit.
no promotion to derived amplitude.
no hiding failed CMB bridge checks.
```

This is the correct discipline if the branch is meant to become a serious theory candidate rather than a flexible curve fit.

## 4. Evidence Card

| Arena | Result | Primary Metric |
|---|---|---|
| SN+BAO full-cov robustness | survives matrix | `DeltaBIC_vs_LCDM=-5.259466877748764` |
| BAO-only release holdout | pass | DR2 `DeltaBIC=-2.108368627321081`; DR1 `DeltaBIC=-0.8483738675035859` |
| BAO+H(z), no CMB | stable draw | 10/10 production branches draw; `DeltaBIC` range `[-1.9014668577456,-0.5803932783513801]` |
| growth `f_sigma8` | preferred/draw | primary all-data proxy `delta_chi2=-2.30357028036` |
| subhorizon correction bound | conditionally negligible | worst listed `k=0.02`, safety `100`, chi2 impact `0.0004978706239791267` |
| CMB compressed distance | diagnostic draw/survival | 4 draw-or-better; 0 edge flags |
| late-to-CMB transfer | fail | 4 fail; 0 pass |
| joint late+CMB calibration | mixed, not promoted | 3 competitive draws; 1 hard loss; strict LCDM late penalty `6.515760594759968` |

## 5. Judge's Card

Late-time background:

```text
good.
```

The frozen branch is not just surviving one hand-picked SN+BAO fit. It survives non-SN BAO-only checks and BAO+H(z) robustness without needing an amplitude refit.

Growth:

```text
useful but conditional.
```

The branch survives the current effective subhorizon growth gate, but this remains a proxy-level result. It is not a derived perturbation theory.

CMB:

```text
not promoted.
```

The compressed CMB distance score is a draw/survival diagnostic, but the late-to-CMB transfer fails and the joint bridge has one mandatory hard loss.

Overall:

```text
MTS is still in the fight on late-time data.
It has not won the CMB / parent-action / local-GR rounds.
```

## 6. Claim Control

Allowed internal claim:

```text
The frozen B_mem=2/27 branch is a competitive late-time empirical EFT closure candidate.
```

Allowed internal claim:

```text
It deserves stricter independent holdout tests because it survives several no-refit late-time checks.
```

Forbidden:

```text
MTS derives B_mem=2/27.
MTS passes CMB.
MTS derives perturbations.
MTS derives local GR.
MTS is a completed unified field theory.
```

## 7. Gates

| Gate | Status | Evidence |
|---|---|---|
| frozen branch no refit | pass | `B_mem` fixed at `0.07407407407407407` |
| late-time empirical survival | pass | 4 late-time arenas retained as preferred/draw/stress-pass |
| CMB bridge promoted | fail | late-to-CMB transfer fails and joint bridge is mixed |
| growth promoted to perturbation theory | fail | still GR-proxy / high-sound-speed EFT target |
| public support claim allowed | fail | empirical EFT closure only |
| hard failures preserved | pass | late-to-CMB transfer failure retained |

## 8. Next Target

Best next empirical move:

```text
choose_new_independent_holdout_or_official_perturbation_pipeline
```

Practical recommendation:

```text
Do one stricter independent late-time non-SN holdout next.
```

Reason:

```text
The late-time card is where the branch is actually scoring.
Official CMB perturbations are the real title fight, but the equations are not ready yet.
```

The clean next step is therefore either:

```text
independent H(z) / cosmic-chronometer compilation cross-check
```

or:

```text
official/full-likelihood BAO+SN+growth reimplementation
```

with the same rule:

```text
B_mem stays frozen.
baselines take the same punches.
no CMB/public promotion from a late-time scorecard.
```
