# 164 - Fixed Pair Ruler Branch Smoke

Private empirical smoke checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 163 constructed an effective pair-ruler owner:

```text
K_c = K_raw - K_x - K_y + K_bar.
```

That made the zero one-point marginal more than a wish. The next question was:

```text
does the fixed pair-ruler branch survive an actual SN+BAO/H(z) smoke run?
```

Short answer:

```text
yes, it survives;
it beats LCDM by BIC in SN+BAO and draws H(z);
but it does not beat the no-clock MTS control.
```

That is a useful survival result, not a promotion.

## 2. Machine Artifact

Script:

```text
scripts/fixed_pair_ruler_branch_smoke.py
```

Run:

```text
runs/20260531-235959-fixed-pair-ruler-branch-smoke
```

Generated:

```text
source_register.csv
branch_contract.csv
sn_bao_fit_summary.csv
sn_bao_prior_edges.csv
sn_bao_baseline_comparison.csv
pair_projection_factors.csv
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

Status:

```text
fixed_pair_ruler_branch_survives_smoke_competitive_not_promoted
```

Claim ceiling:

```text
fixed_pair_ruler_branch_smoke_no_bridge_promotion
```

## 3. Branch Contract

The tested pair-ruler branch used:

```text
B_mem = 2/27
u_3 = 1/4
T_D = (B_mem/4)F_D(1-2e^-N)
S_D = (B_mem/6)(1-e^-2N)
```

BAO projection:

```text
Pi_perp     = T_D - S_D/3
Pi_parallel = T_D + 2S_D/3
```

Policy:

```text
SN uses no-clock one-point MTS.
H(z) uses no-clock one-point MTS.
BAO uses the fixed pair-ruler projection.
```

Fitted SN+BAO parameters:

```text
Omega_m + SN_offset + BAO_alpha.
```

No fitted projection amplitudes were added.

## 4. SN+BAO Result

| branch | chi2 SN | chi2 BAO | chi2 total | BIC |
|---|---:|---:|---:|---:|
| LCDM | 1459.575682526303 | 10.938130398054092 | 1470.513812924357 | 1492.7156746564704 |
| wCDM | 1456.3847069257295 | 9.042920548851583 | 1465.427627474581 | 1495.0301097840654 |
| CPL | 1456.4623855608309 | 8.62945011149004 | 1465.091835672321 | 1502.0949385591766 |
| no-clock MTS `u3fit` | 1457.205443679329 | 8.206877473910414 | 1465.4123211532394 | 1487.6141828853529 |
| no-clock MTS `u3=1/4` | 1457.0898807169324 | 8.169991154306091 | 1465.2598718712384 | 1487.4617336033518 |
| fixed pair-ruler MTS | 1458.0970756467407 | 8.664808133531212 | 1466.761883780272 | 1488.9637455123855 |

Against baselines:

| comparison | delta chi2 | delta AIC | delta BIC | readout |
|---|---:|---:|---:|---|
| pair-ruler vs LCDM | -3.7519291440848974 | -3.7519291440848974 | -3.7519291440848974 | preferred |
| pair-ruler vs wCDM | +1.3342563056910421 | -0.6657436943089579 | -6.066364271679959 | preferred by BIC |
| pair-ruler vs CPL | +1.670048107951061 | -2.329951892048939 | -13.131193046791168 | preferred by BIC |
| pair-ruler vs no-clock `u3fit` | +1.349562627032583 | +1.349562627032583 | +1.349562627032583 | competitive draw |
| pair-ruler vs no-clock `u3=1/4` | +1.5020119090336266 | +1.5020119090336266 | +1.5020119090336266 | competitive draw |

This is the correct boxing-card read:

```text
the fixed pair branch beats LCDM;
it survives against wCDM/CPL after information penalty;
it does not beat the no-clock MTS control.
```

## 5. Null-Response Check

SN is not globally clock-shifted in this branch.

Against the no-clock `u3=1/4` control:

```text
delta chi2_SN = +1.0071949298082927
delta chi2_BAO = +0.4948169792251207
delta chi2_total = +1.5020119090336266
```

The SN change is a warning from the common `Omega_m` refit, not a direct SN projection. It is small enough for a draw but not zero.

H(z) is exactly null under the branch policy:

```text
primary CC15 pair vs no-clock delta chi2 = 0.0.
```

Against LCDM in H(z):

```text
primary CC15 delta_BIC = +0.332569569103466.
```

So H(z) is a draw, not a failure driver.

## 6. Projection Factors

The fixed projection is percent-level:

| z | observable | `Pi_perp` | `Pi_parallel` |
|---:|---|---:|---:|
| 0.295 | `DV_over_rs` | -0.008405897113570258 | -0.0034218728245266647 |
| 0.510 | `DM/DH` | -0.008251554189058485 | -0.0013204091937934967 |
| 0.706 | `DM/DH` | -0.005892436513812257 | +0.002211376670751715 |
| 0.934 | `DM/DH` | -0.003646969148921755 | +0.005398040351659354 |
| 1.321 | `DM/DH` | -0.0007901575486637495 | +0.009263784866105322 |
| 1.484 | `DM/DH` | +0.00015999763015481965 | +0.01050483923602244 |
| 2.330 | `DH/DM` | +0.003652171060319951 | +0.014884513401548958 |

The shape is the expected trace/quadrupole pattern:

```text
low-z transverse suppression,
high-z radial enhancement,
smooth sign transition.
```

But the row residuals show where the branch still needs inspection:

```text
worst pair row: z=0.51 DM_over_rs, diagonal pull = +1.959186703622481.
next pressure: z=0.706 DH_over_rs, diagonal pull = -1.3057826227116573.
```

## 7. Gates

| gate | status | readout |
|---|---|---|
| same data / same nuisance | pass | same Pantheon+, DESI, H(z) data and same nuisance freedom |
| no extra projection knobs | pass | fixed `T_D`, `S_D`; no fitted projection amplitudes |
| convergence | pass | all branches converged |
| pair vs LCDM | pass preferred/draw | delta BIC `-3.7519291440848974` |
| pair vs no-clock control | pass competitive | delta BIC `+1.5020119090336266` |
| SN null policy | warning | refit shifts SN chi2 by `+1.0071949298082927` |
| H(z) null policy | pass | pair vs no-clock delta chi2 `0.0` |
| prior edge safety | pass | MTS branches not edge-flagged |
| promotion | fail | no bridge/CMB/local-GR claim |

## 8. Decision

Current fair status:

```text
fixed_pair_ruler_branch_survives_smoke_competitive_not_promoted
```

Meaning:

```text
the fixed pair-ruler branch is not dead;
it scores a BIC win over LCDM and remains a draw against no-clock MTS;
but it is not the empirical lead branch because no-clock MTS still scores better.
```

This is actually a healthy result. The derived-looking pair-ruler structure did not collapse under the first smoke run, but it also did not magically outperform the simpler no-clock branch.

Boxing-card readout:

```text
Pair-ruler MTS wins the LCDM round.
Against no-clock MTS it is basically a close judges' round, not a knockout.
The route stays live, but it has to explain why adding the fixed pair transport
does not yet improve the no-clock control.
```

## 9. Next Target

Create:

```text
165-pair-ruler-residual-and-two-point-safety-audit.md
```

Task:

```text
inspect BAO row residuals and define the next growth/lensing/two-point safety
test for the effective pair operator.
```

Pass condition:

```text
the pair-ruler residual pattern has a clear source-law repair or a justified
two-point observable prediction that can be tested.
```

Fail condition:

```text
the pair-ruler branch only remains competitive by moving residuals around
without a stronger parent or two-point safety story.
```
