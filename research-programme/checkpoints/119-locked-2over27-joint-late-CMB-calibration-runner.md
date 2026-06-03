# 119 - Locked 2/27 Joint Late-CMB Calibration Runner

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 118 declared the joint calibration contract:

```text
one shared Omega_m0;
one shared h;
one shared r_d;
BAO alpha = c/(100 h r_d);
one profiled SN offset;
compressed CMB distance prior scored with the same h and Omega_m0.
```

This checkpoint implements and runs the first guarded joint calibration score.

## 2. Short Verdict

```text
broad_r_d_joint_status =
locked_2over27_joint_late_CMB_calibration_hard_loss
```

```text
physical_r_d_sensitivity_status =
locked_2over27_joint_late_CMB_calibration_mixed_or_narrow
```

```text
theory_promotion_allowed =
false
```

Plain English:

```text
The joint bridge is much better than the simple late-to-CMB transfer, but it
does not cleanly pass the predeclared joint gate.
```

It lands in an awkward but informative place:

```text
3 of 4 broad-r_d primary gates are competitive draws;
1 of 4 is a hard loss by the predeclared sector-degradation threshold.
```

The hard-loss gate is the `LCDM` compressed prior table with the strict full-four CMB vector:

```text
late chi2 penalty = 6.515760594759968
```

against a hard cutoff of:

```text
6
```

So this is not a clean survival. It is also not a collapse.

Boxing-score version:

```text
This was a split-card mess. MTS kept finding counters, but one judge gave a
hard round away on the strict LCDM-prior card.
```

## 3. Machine Artifact

Script:

```text
research-programme\scripts\locked_2over27_joint_late_CMB_calibration_runner.py
```

Dry-run:

```text
research-programme\runs\20260531-163152-locked-2over27-joint-late-CMB-dryrun
```

Broad `r_d` score:

```text
research-programme\runs\20260531-164201-locked-2over27-joint-late-CMB-score
```

Physical-band `r_d` sensitivity:

```text
research-programme\runs\20260531-164711-locked-2over27-joint-late-CMB-score
```

Generated:

```text
source_register.csv
data_schema_report.csv
model_register.csv
parameter_map_register.csv
control_reproduction.csv
fit_summary.csv
sector_chi2_breakdown.csv
prior_edge_table.csv
rd_plausibility_table.csv
baseline_comparisons.csv
joint_gates.csv
decision.csv
status.json
```

## 4. Test Definition

Primary data:

| Sector | Rows | Treatment |
|---|---:|---|
| SN | 1624 | Pantheon+ `mb-corr`, no calibrators, full covariance |
| BAO | 13 | DESI DR2 primary, full covariance |
| CMB | 4 or 2 | Planck compressed distance prior, `wCDM` and `LCDM` tables |

Primary score modes:

```text
strict_full4 = R, l_A, Omega_b_h2, n_s
marginal_R_lA = R, l_A
```

Model set:

```text
LCDM
wCDM
CPL
MTS_locked_2over27
MTS_Bmem_zero
```

The locked branch used:

```text
B_mem = 2/27
DeltaR = 2/9
p = 3
u3 = 1/4
```

## 5. Controls

| Control | Status | Evidence |
|---|---|---|
| `alpha_free_late_control` | reference available | T7 primary chi2_late = 1465.2684058007976 |
| `CMB_only_control` | reference available | checkpoint 116 status exists |
| `late_to_CMB_transfer_control` | reference available | checkpoint 117 transfer fail exists |
| `joint_h_rd_score` | complete | 4 locked broad-r_d rows |
| `r_d_prior_sensitivity` | broad run incomplete alone; physical run completed separately | broad + physical runs now both exist |

Interpretation:

```text
the joint score is interpretable as a first guarded joint calibration run,
but the broad and physical r_d modes are stored as separate runs.
```

## 6. Broad r_d Locked Fits

The broad prior was:

```text
80 <= r_d <= 200 Mpc
```

| Prior table | Score mode | chi2_SN | chi2_BAO | chi2_CMB | Omega_m0 | h | r_d | Edge |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `wCDM` | `strict_full4` | 1458.5511938223663 | 12.272818912319421 | 1.9961220187138609 | 0.32240555317663316 | 0.6716183291190234 | 146.66292561505776 | false |
| `wCDM` | `marginal_R_lA` | 1457.8113735315055 | 9.895935928300046 | 2.5602094431704483 | 0.31582283300396563 | 0.6758935375848381 | 146.42782367312972 | false |
| `LCDM` | `strict_full4` | 1458.7735004752776 | 13.010665920280031 | 2.1727892176246355 | 0.32404493506253196 | 0.6704317723056884 | 146.75083597961384 | false |
| `LCDM` | `marginal_R_lA` | 1457.9023681633585 | 10.177891639649864 | 2.8903756091960786 | 0.31676764445410166 | 0.6751206357427594 | 146.49505046560682 | false |

The joint fit pulls the locked branch to:

```text
Omega_m0 about 0.316-0.324;
h about 0.670-0.676;
r_d about 146.4-146.8 Mpc.
```

That is physically sane and edge-free.

## 7. Broad r_d Joint Gates

| Prior table | Score mode | Gate | Late chi2 penalty vs T7 | CMB chi2 penalty vs CMB-only | Delta BIC vs LCDM |
|---|---|---|---:|---:|---:|
| `wCDM` | `strict_full4` | competitive draw | 5.555606933888157 | 1.9961220167282194 | 1.2254090809894933 |
| `wCDM` | `marginal_R_lA` | competitive draw | 2.4389036590080195 | 2.5602094418485497 | -0.9642713413111323 |
| `LCDM` | `strict_full4` | hard loss sector degradation | 6.515760594759968 | 2.172789216061106 | 1.9491166649465868 |
| `LCDM` | `marginal_R_lA` | competitive draw | 2.8118540022107936 | 2.890375607071273 | -0.5252359584794704 |

The reason the broad run status is hard-loss is:

```text
predeclared late/CMB sector degradation hard cutoff = 6;
LCDM strict_full4 late penalty = 6.515760594759968.
```

That is a real fail by the gate.

It is also very close to the boundary, so the scientific readout is:

```text
not promoted;
not dead;
needs red-team and calibration-map repair.
```

## 8. Physical r_d Sensitivity

The physical sensitivity prior was:

```text
130 <= r_d <= 160 Mpc
```

The locked fit lands at essentially the same values:

| Prior table | Score mode | Omega_m0 | h | r_d | Gate |
|---|---|---:|---:|---:|---|
| `wCDM` | `strict_full4` | 0.3224054742792282 | 0.67161838479137 | 146.66290833071062 | competitive draw |
| `wCDM` | `marginal_R_lA` | 0.31582283300396563 | 0.6758935375848381 | 146.42782367312972 | competitive draw |
| `LCDM` | `strict_full4` | 0.32404493506253196 | 0.6704317723056884 | 146.75083597961384 | hard loss sector degradation |
| `LCDM` | `marginal_R_lA` | 0.3167678284934728 | 0.6751204992093961 | 146.4950548169152 | competitive draw |

So the result does not depend on a weird drag scale.

That is good.

But it does not remove the strict LCDM-prior tension.

## 9. Baseline Readout

Against LCDM, the locked branch is:

```text
competitive draw in all four broad-r_d information-card comparisons.
```

The hard loss is not BIC.

The hard loss is the sector-degradation gate.

Against `wCDM` and `CPL`, the locked branch generally benefits from parsimony, but that does not override the sector gate.

This is exactly why the gate exists:

```text
do not let information criteria hide a bad sector transfer.
```

## 10. Strategic Meaning

The old simple transfer failed badly:

```text
late Omega_m0 = 0.303 could not carry into CMB.
```

The joint fit finds a compromise:

```text
Omega_m0 moves upward to about 0.316-0.324;
h moves to about 0.670-0.676;
r_d remains sane near 146.5 Mpc.
```

That is meaningful.

It says:

```text
the bridge is not obviously impossible.
```

But:

```text
the bridge is not clean enough to claim.
```

The next work should not be another free retune.

The next work should red-team the strict `LCDM` compressed-prior table branch and decide whether the failure is:

```text
real physics tension;
compressed-prior model-dependence;
optimizer/numerical tolerance;
or a missing derived calibration relation.
```

## 11. Claim Lock

Allowed:

```text
The locked 2/27 branch now has a working joint SN+BAO+CMB calibration runner.
```

Allowed:

```text
The first joint run is mixed: mostly competitive draws, but one predeclared
hard-loss sector gate.
```

Forbidden:

```text
MTS passes joint cosmology.
```

Forbidden:

```text
MTS is ruled out.
```

Forbidden:

```text
The parent field theory derives h, r_d, or the CMB calibration map.
```

## 12. Decision

Status:

```text
joint_late_CMB_runner_complete_mixed_result_not_promoted
```

The branch remains:

```text
serious empirical closure candidate with unresolved joint calibration tension.
```

## 13. Next Target

Create:

```text
120-joint-calibration-red-team-and-repair-options.md
```

Purpose:

```text
red-team the one failing gate, check whether it is robust to numerical settings
and compressed-prior model dependence, and identify the minimum derived
calibration relation needed to turn the mixed joint result into a clean
survival.
```

Do not promote the branch unless that red-team pass clears the strict sector gate.
