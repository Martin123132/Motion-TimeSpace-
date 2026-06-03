# 90 - Cosmology Model-Selection Stability Ledger

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 89 made the no-SH0ES/full-covariance branch runnable and found:

```text
MTS_fixed_p3_u3quarter remains non-edge;
full-sample no-SH0ES DR2 is close to wCDM/CPL;
preference language is still blocked by branch dependence and amplitude derivation.
```

This checkpoint changes the judging frame from "knockout or failure" to a proper model-selection scorecard.

## 2. Short Verdict

```text
model_selection_status =
MTS_survives_on_points_but_not_promoted
```

```text
stable_evidence_allowed =
false
```

Plain English:

```text
MTS is not getting battered. It is slipping, countering, and staying on the cards. The current cosmology result is a close-points survival/win in some branches, not a knockout and not a field-theory proof.
```

## 3. Scoring Philosophy

The old binary question was too crude:

```text
Does MTS annihilate LCDM/wCDM/CPL?
```

The correct internal question is:

```text
Can MTS remain edge-free, competitive, and structurally cleaner while the baselines spend extra phenomenological freedom?
```

Scorecard language:

| Verdict | Meaning |
|---|---|
| `clear_points_win` | MTS beats by enough to matter on fit/statistical criteria. |
| `clean_points_win` | MTS beats the baseline without edge flags. |
| `style_points_win_information_criteria` | MTS may not have lowest chi2, but wins AIC/BIC through efficiency. |
| `respectable_draw` | Differences are too small to call as a decisive empirical loss. |
| `narrow_loss_keep_working` | Baseline edges the round, but not enough to kill the branch. |
| `unclean_round_baseline_edge_hit` | Baseline is boundary-running; do not award a clean decision. |
| `real_trouble` | MTS edge-hits, fails convergence, or loses badly under fair rules. |

## 4. Ledger Artifact

Script:

```text
research-programme\scripts\cosmo_model_selection_stability_ledger.py
```

Run:

```text
research-programme\runs\20260531-131611-cosmo-model-selection-stability-ledger
```

Generated:

```text
model_rankings.csv
mts_fixed_round_scorecard.csv
branch_summary.csv
status.json
```

Status:

```text
model_selection_stability_ledger_written
```

Source runs requested/found:

```text
8 / 8
```

## 5. Branch Summary

| Branch | Edge issue | MTS chi2 rank | MTS AIC rank | MTS BIC rank | Readout |
|---|---|---:|---:|---:|---|
| SH0ES diagonal 250-row DR2 default | CPL edge | 1 | 1 | 3 | MTS leads edge-free chi2/AIC, LCDM wins BIC. |
| SH0ES diagonal CPL-wa narrow | CPL edge | 1 | 1 | 3 | Same MTS fixed result; CPL edge moves with prior. |
| SH0ES diagonal CPL-wa wide | CPL edge | 1 | 1 | 3 | Same; baseline degeneracy persists. |
| SH0ES diagonal MTS ablations | CPL edge | 3 | 1 | 3 | fitted-u3 improves chi2 but fixed branch wins AIC. |
| no-SH0ES full-cov 250-row DR2 | CPL and fitted-u3 edge | 2 | 1 | 3 | fixed MTS survives; fitted-u3 is not stable. |
| no-SH0ES full-cov 250-row DR1 | CPL and fitted-u3 edge | 2 | 3 | 3 | DR1 weakens the fixed branch versus LCDM. |
| no-SH0ES diagonal full-sample DR2 | none | 1 | 1 | 1 | cleanest points win, but diagonal covariance only. |
| no-SH0ES full-cov full-sample DR2 | none | 2 | 1 | 3 | close clean round: MTS wins AIC, not BIC versus LCDM. |

## 6. Cleanest Full-Covariance Round

Branch:

```text
no-SH0ES full-cov full-sample DR2
```

Fit table:

| Model | chi2 | AIC | BIC | Edge |
|---|---:|---:|---:|---:|
| `LCDM` | 1470.527873 | 1476.527873 | 1492.729734 | no |
| `wCDM` | 1465.437415 | 1473.437415 | 1495.039897 | no |
| `CPL` | 1465.100678 | 1475.100678 | 1502.103781 | no |
| `MTS_fixed_p3_u3quarter` | 1465.268214 | 1473.268214 | 1494.870696 | no |
| `MTS_Bmem_zero` | 1470.527873 | 1476.527873 | 1492.729734 | no |

Judge cards for fixed MTS:

| Baseline | Delta chi2 | Delta AIC | Delta BIC | Verdict |
|---|---:|---:|---:|---|
| `LCDM` | -5.259659 | -3.259659 | +2.140962 | `narrow_loss_keep_working` because BIC stays with LCDM. |
| `wCDM` | -0.169201 | -0.169201 | -0.169201 | `clean_points_win`. |
| `CPL` | +0.167536 | -1.832464 | -7.233085 | `style_points_win_information_criteria`. |

This is the key scorecard result: MTS does not need a knockout here. Against flexible dark-energy baselines it is at least live on points, and against CPL it loses tiny chi2 but wins AIC/BIC because it is more efficient.

## 7. Why This Is Not Promotion Yet

Promotion is still blocked by:

```text
B_mem/b_mem is fitted, not parent-derived;
p=3 and u3=1/4 still need stronger parent ownership;
the 250-row ablation branch can edge-hit;
DR1 weakens the fixed branch against LCDM;
perturbation/CMB consistency is not settled by background SN+BAO.
```

So the correct status is:

```text
empirically_competitive_closure_candidate
```

not:

```text
derived_unified_field_theory
```

## 8. Fair Interpretation

Allowed statement:

```text
On the current SN+BAO scorecard, fixed MTS is not being ruled out by fair baselines. In the clean full-sample full-covariance branch it is competitive with wCDM/CPL and wins information-criterion rounds against them, while remaining non-edge.
```

Forbidden statement:

```text
MTS has beaten cosmology.
```

Reason:

```text
The closure amplitude is not derived, LCDM still wins one BIC card in the cleanest branch, and background expansion alone cannot validate the field theory.
```

## 9. Decision

More brute-force cosmology fitting is no longer the highest-value next step.

The next physics bottleneck is:

```text
derive or tightly constrain the amplitude/shape ownership of B_mem, p, and u3.
```

Second priority:

```text
perturbation/CMB consistency under the same closure, not a separately tuned branch.
```

Wider robustness remains useful, but only after the amplitude route is less free.

## 10. Next Target

Create:

```text
91-Bmem-p-u3-parent-ownership-gate.md
```

Purpose:

```text
Turn the cosmology closure from "good counter-punching phenomenology" into a derivation target.
```

Acceptance:

```text
Either B_mem, p, and u3 get a parent-action/coarse-graining ownership route, or the cosmology branch remains explicitly closure-only no matter how good the scorecard looks.
```
