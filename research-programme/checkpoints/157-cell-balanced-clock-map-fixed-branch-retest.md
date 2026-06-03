# 157 - Cell-Balanced Clock-Map Fixed-Branch Retest

Private empirical stress checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 156 found a compact signed clock-map theorem target:

```text
Theta_clock = B_mem * (1/24) * X_D * F_D * (1 - X_D/4).
```

That was promising because it hit the BAO clock target without a redshift polynomial. But the real question was:

```text
does the same fixed map survive outside the handoff target?
```

So this checkpoint runs the fixed branch through:

```text
Pantheon+ / SH0ES-shape SN,
DESI DR2 BAO,
source-locked cosmic chronometer H(z).
```

No extra redshift freedom is allowed.

## 2. Machine Artifact

Script:

```text
scripts/cell_balanced_clock_map_fixed_branch_retest.py
```

Primary run:

```text
runs/20260531-235959-cell-balanced-clock-map-fixed-branch-retest
```

Strict SN sensitivity run:

```text
runs/20260531-235959-trueSN-cell-balanced-clock-map-fixed-branch-retest
```

Generated:

```text
source_register.csv
branch_contract.csv
sn_bao_fit_summary.csv
sn_bao_prior_edges.csv
sn_bao_baseline_comparison.csv
bao_residuals.csv
sn_residual_summary.csv
hz_fit_summary.csv
hz_prior_edges.csv
hz_baseline_comparison.csv
hz_residuals.csv
gate_results.csv
decision.csv
status.json
```

Primary status:

```text
fixed_cell_clock_mixed_retest_quarter_survives_u3fit_rework
```

Strict SN status:

```text
fixed_cell_clock_branch_demote_or_rework_after_retest
```

Claim ceiling:

```text
fixed_cell_clock_retest_no_bridge_promotion
```

## 3. Fixed-Branch Rules

The clock branches were not given new shape freedom.

Fitted for SN+BAO:

```text
Omega_m + SN offset + BAO alpha.
```

Fitted for H(z):

```text
Omega_m + h.
```

Fixed:

```text
B_mem = 2/27,
kappa = 1/24,
p = 3,
u3 = 0.2429466120286312 or 1/4.
```

Clock map:

```text
z_true = z_obs + zeta(z),
zeta = -(1+z_obs) Theta_clock.
```

BAO projection:

```text
D_M_obs = D_M(z_true),
D_H_obs = D_H(z_true) dz_true/dz_obs.
```

Primary SN convention:

```text
D_L_obs = (1+z_obs) D_M(z_true).
```

Strict SN sensitivity:

```text
D_L = (1+z_true) D_M(z_true).
```

The strict version is harsher. It checks whether the route depends on the kinder observed-redshift distance-duality convention.

## 4. SN+BAO Scorecard

Primary observed-redshift SN convention:

| branch | chi2_SN | chi2_BAO | chi2_total | BIC | readout vs LCDM |
|---|---:|---:|---:|---:|---|
| LCDM | 1459.575682526303 | 10.938130398054092 | 1470.513812924357 | 1492.7156746564704 | baseline |
| MTS no-clock u3fit | 1457.205443679329 | 8.206877473910414 | 1465.4123211532394 | 1487.6141828853529 | preferred |
| MTS no-clock u3quarter | 1457.0898807169324 | 8.169991154306091 | 1465.2598718712384 | 1487.4617336033518 | preferred |
| MTS clock u3fit | 1463.4779707087207 | 9.162579938348907 | 1472.6405506470696 | 1494.842412379183 | disfavored by 2.1267377227127326 |
| MTS clock u3quarter | 1462.592987099126 | 9.016536732213638 | 1471.6095238313396 | 1493.811385563453 | draw by 1.095710906982731 |

Readout:

```text
the no-clock 2/27 background branch still scores better;
the clock map improves BAO relative to LCDM;
but it hurts SN enough to weaken the joint score.
```

This is not a bridge win.

## 5. Baseline Comparisons

Primary observed-redshift convention:

| branch | reference | Δχ² | ΔBIC | readout |
|---|---|---:|---:|---|
| MTS clock u3fit | LCDM | 2.1267377227127326 | 2.1267377227127326 | disfavored |
| MTS clock u3fit | wCDM | 7.2129231724863985 | -0.1876974048846023 | draw |
| MTS clock u3fit | CPL | 7.548714974727318 | -7.252526180014911 | preferred by BIC |
| MTS clock u3quarter | LCDM | 1.095710906982731 | 1.095710906982731 | draw |
| MTS clock u3quarter | wCDM | 6.181896356756397 | -1.2187242206146038 | draw |
| MTS clock u3quarter | CPL | 6.517688158997316 | -8.283552995744913 | preferred by BIC |

This is very Mayweather-scorecard, not Tyson-knockout:

```text
against LCDM, fitted-u3 loses the round narrowly;
quarter-u3 keeps the round close enough to call a draw;
against flexible dark-energy baselines, BIC still likes the lower-parameter branch.
```

But because the no-clock MTS branch scores better than the clock branch, the clock map is not currently an improvement.

## 6. Strict SN Sensitivity

When SN uses the harsher:

```text
D_L=(1+z_true)D_M(z_true),
```

the clock branch weakens:

| branch | ΔBIC vs LCDM | ΔBIC vs wCDM | readout |
|---|---:|---:|---|
| MTS clock u3fit | 4.753307461493478 | 2.4388723338961427 | disfavored |
| MTS clock u3quarter | 3.4893320241126276 | 1.1748968965152926 | disfavored vs LCDM, draw vs wCDM |

So the clock route currently depends on the softer observed-redshift distance-duality convention. That is a real warning sign.

## 7. H(z) Scorecard

The H(z) branch does not kill the clock map.

Primary CC15 suggested covariance:

| branch | chi2 | BIC | H0 | ΔBIC vs LCDM |
|---|---:|---:|---:|---:|
| LCDM | 6.1128594336276985 | 11.528959835832119 | 66.98574820130344 | baseline |
| MTS clock u3fit | 6.465343077691636 | 11.881443479896056 | 65.2350348334562 | 0.3524836440639376 |
| MTS clock u3quarter | 6.494928973556215 | 11.911029375760634 | 65.35970749477953 | 0.38206953992851567 |

Readout:

```text
H(z) is a competitive draw.
```

So the failure mode is not chronometer collapse. The pressure is SN+BAO, especially SN cost plus high-z BAO row changes.

## 8. What Actually Happened

Compared with LCDM under the primary convention:

```text
MTS clock u3fit:
SN penalty  = +3.9022881824177
BAO gain    = -1.775550459705185
joint delta = +2.1267377227127326
```

For the quarter branch:

```text
MTS clock u3quarter:
SN penalty  = +3.017304572823
BAO gain    = -1.921593665840454
joint delta = +1.095710906982731
```

So the clock map is doing something physically clear:

```text
it buys BAO improvement,
but it spends too much SN chi2.
```

This is useful because it tells us where to work next. We do not need a vague “cosmology failed” label. We need to isolate whether the SN cost is:

```text
wrong distance-duality convention,
wrong clock sign/amplitude,
using a global redshift map where only BAO ruler projection should move,
or evidence that the clock route should demote.
```

## 9. Gates

Primary gate result:

| gate | status | evidence |
|---|---|---|
| same data / same nuisance | pass | same Pantheon+/DESI/H(z) rows as baselines |
| no extra clock freedom | pass | only standard nuisance and Omega_m fitted |
| convergence | pass | all fitted branches converged |
| SN+BAO u3fit clock | fail_disfavored_vs_LCDM | ΔBIC = 2.1267377227127326 |
| SN+BAO quarter clock | pass_draw_or_better | ΔBIC = 1.095710906982731 |
| H(z) primary clock | pass_draw_or_better | ΔBIC = 0.3524836440639376 |
| prior edge safety | pass | clock branches not edge-flagged |
| promotion | fail | no bridge promotion |

Strict SN gate result:

```text
both clock branches are BIC-disfavored vs LCDM.
```

## 10. Decision

Current fair status:

```text
fixed_cell_clock_mixed_retest_quarter_survives_u3fit_rework
```

Meaning:

```text
the fixed clock map is not a bridge win;
the u3fit clock branch loses to LCDM by the chosen BIC gate;
the u3=1/4 clock branch survives as a draw under the primary SN convention;
both clock branches fail under stricter true-redshift SN convention;
H(z) remains fine;
the no-clock 2/27 background branch still scores better.
```

So the clock route is no longer allowed to be the leading bridge claim. It is now:

```text
a conditional sub-branch requiring failure-mode repair.
```

That is not a collapse of MTS. It is a narrowing:

```text
late-time 2/27 background remains competitive;
the extra clock/projection bridge needs rework before it can carry CMB/BAO calibration.
```

## 11. Next Target

Next checkpoint:

```text
158-cell-clock-BAO-row-and-SN-Hz-failure-mode-audit.md
```

Task:

```text
inspect whether the clock-map loss comes from radial BAO rows,
transverse BAO rows,
SN distance-duality treatment,
or chronometer derivative-map pressure.
```

Acceptance logic:

```text
if the loss is SN-only, derive a ruler-only projection or demote global clock coupling;
if the loss is BAO row-specific, alter/reject the projection tensor;
if the loss survives every convention, demote the clock route to closure-only;
if a derived convention fixes SN without adding freedom, keep it as a theorem target.
```

Boxing-card version:

```text
MTS still has the late-time background round.
The new clock-map punch landed on BAO,
but it left the chin open on SN.
Next round is defense: find the opening or stop throwing that punch.
```
