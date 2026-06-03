# 146 - Source-Locked Growth Covariance Holdout

Private empirical checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 145 showed that source-locked cosmic-chronometer H(z) does not disfavor the frozen branch.

The next useful empirical pressure is growth/RSD with covariances, while applying the same jackknife punches to the baselines.

Question:

```text
Does frozen B_mem = 2/27 survive source-locked SDSS/eBOSS DR16 growth covariance tests?
```

Short answer:

```text
yes, under the current conditional GR-proxy growth gate.
```

But:

```text
this still does not derive MTS perturbation theory.
```

## 2. Machine Artifact

Script:

```text
research-programme\scripts\source_locked_growth_covariance_holdout.py
```

Run:

```text
research-programme\runs\20260531-224500-source-locked-growth-covariance-holdout
```

Fetched source intake:

```text
research-programme\source-intake\sdss_eboss_dr16\20260531-224500
```

Generated:

```text
source_register.csv
fetch_hash_lock.csv
data_schema.csv
branch_manifest.csv
fit_summary.csv
baseline_comparisons.csv
control_reproduction.csv
jackknife_scorecard.csv
residuals.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
growth_covariance_source_locked_primary_preferred_or_draw
```

Claim ceiling:

```text
source_locked_growth_covariance_holdout_no_perturbation_promotion
```

## 3. Source Lock

The runner re-fetched the SDSS/eBOSS DR16 likelihood files listed in the local source manifest from:

```text
https://svn.sdss.org/public/data/eboss/DR16cosmo/tags/v1_0_1/likelihoods/
```

Hash lock:

```text
fetched_files = 19
failures = 0
```

This covers:

```text
BAO-plus vectors and covariances
Full-shape-only vectors and covariances
README metadata files
```

The ELG grid likelihood is still not used because it needs a grid-likelihood parser, not a Gaussian covariance shortcut.

## 4. Fairness Contract

All scored branches use the same conditional rule:

```text
fixed late-time background from BAO+H(z)
frozen B_mem = 2/27
shared fitted sigma8_0 only
same branches for LCDM, wCDM, CPL, MTS locked, and MTS Bmem-zero
```

The growth equation remains the GR background-growth proxy:

```text
D'' + [2 + d ln H / d ln a]D' - 3 Omega_m(a)D/2 = 0
```

So the result is a covariance stress test, not a derived perturbation theorem.

## 5. Branches

Primary production branch:

```text
MGS
BOSS_DR12_LRG
eBOSS_DR16_LRG
eBOSS_DR16_QSO
```

Jackknife branches:

```text
drop MGS
drop BOSS_DR12_LRG
drop eBOSS_DR16_LRG
drop eBOSS_DR16_QSO
```

Alternative full-shape-only branch:

```text
BOSS_DR12_LRG
eBOSS_DR16_LRG
eBOSS_DR16_QSO
```

Important:

```text
BAO-plus and full-shape-only are scored separately.
They are not combined as independent evidence.
```

## 6. Primary Result

DR2 no-CMB primary, BAO-plus all rows:

| Model | chi2 | sigma8_0 | Edge |
|---|---:|---:|---|
| LCDM | `16.760271551343262` | `0.8688417011864101` | false |
| wCDM | `13.914502904076793` | `0.8873719885141126` | false |
| CPL | `13.96396112228521` | `0.8777006500420644` | background edge |
| MTS locked 2/27 | `14.45670127098755` | `0.8823631714101979` | false |
| MTS Bmem-zero | `16.760271551343262` | `0.8688417011864101` | false |

MTS locked comparisons:

| Reference | Delta chi2 | Readout |
|---|---:|---|
| LCDM | `-2.3035702803557125` | locked preferred |
| wCDM | `0.5421983669107568` | competitive draw |
| CPL | `0.49274014870233884` | competitive draw, but CPL background edge |
| MTS Bmem-zero | `-2.3035702803557125` | locked preferred |

RSD-only slice:

```text
MTS locked vs LCDM delta chi2 = -0.334685976748
```

Readout:

```text
competitive draw
```

This means the all-row improvement is not pure growth-amplitude proof. It is a joint geometry-plus-growth score.

## 7. Full-Shape Alternative

Full-shape-only is not combined with BAO-plus.

It is scored as an alternative compression:

```text
all rows delta chi2 vs LCDM = -0.217790489076
RSD-only delta chi2 vs LCDM = -0.304121377055
```

Readout:

```text
competitive draw
```

So the source-locked alternative compression does not punch the branch out.

## 8. Jackknife Card

All jackknives are scored against LCDM with the same sigma8-only nuisance rule.

| Background | File Set | Mode | Preferred | Draw | Disfavored | Delta Range |
|---|---|---|---:|---:|---:|---|
| DR2 | BAO-plus | all | 2 | 2 | 0 | `[-2.314391592135225, -0.7317938345793245]` |
| DR2 | BAO-plus | RSD-only | 0 | 4 | 0 | `[-0.3385208414616545, -0.025970252369213576]` |
| DR2 | full-shape-only | all | 0 | 3 | 0 | `[-0.4976645866504379, 1.1735443313469176]` |
| DR2 | full-shape-only | RSD-only | 0 | 3 | 0 | `[-0.3142424793871914, 0.04065562506484377]` |
| DR1 | BAO-plus | all | 2 | 2 | 0 | `[-2.4339237025004827, -0.8469374090062622]` |
| DR1 | BAO-plus | RSD-only | 0 | 4 | 0 | `[-0.32544774669082877, -0.02948297317566606]` |
| DR1 | full-shape-only | all | 0 | 3 | 0 | `[-0.5277583823759997, 1.0016248218830937]` |
| DR1 | full-shape-only | RSD-only | 0 | 3 | 0 | `[-0.30007090942738834, 0.03716914242300162]` |

Jackknife verdict:

```text
8 jackknife groups
0 failing groups
```

This directly answers the fairness concern:

```text
we did not only jackknife MTS.
the baselines took the same leave-one-sample-out tests.
```

## 9. Gates

| Gate | Status | Evidence |
|---|---|---|
| source fetch hash lock | pass | 19 files |
| covariance schema | pass | 7 unique vector/covariance pairs |
| frozen `B_mem` no refit | pass | only `sigma8_0` profiled for every model |
| same-test retest baselines | pass | LCDM, wCDM, CPL, locked MTS, and Bmem-zero all scored |
| primary growth not disfavored | pass | all rows preferred; RSD-only draw |
| jackknife no hard loss | pass | 8 jackknife groups |
| do not combine alternative compressions | pass | BAO-plus and full-shape-only scored separately |
| theory promotion | fail | no perturbation action, local GR, or CMB theorem |

## 10. Judge's Card

This is a good round for the frozen branch.

Boxing version:

```text
MTS lands the cleaner counter on the primary all-row card.
On pure RSD-only, it stays in the pack.
On full-shape-only, it stays in the pack.
On jackknives, it does not get dropped.
```

The honest readout:

```text
growth/RSD covariance does not currently kill the frozen branch.
```

The stronger but still internal readout:

```text
the frozen branch is now a serious late-time empirical closure candidate across SN+BAO, BAO-only, BAO+H(z), H(z), and SDSS/eBOSS growth covariance stress tests.
```

Still forbidden:

```text
MTS derives perturbations.
MTS passes CMB.
MTS derives local GR.
MTS is a completed unified theory.
```

## 11. Next Target

The next empirical title-fight route is:

```text
official_likelihood_reimplementation_or_ELG_grid_parser
```

Two clean options:

1. parse the eBOSS DR16 ELG grid likelihood and add it as a non-Gaussian growth/geometry branch;
2. start an official/full-likelihood BAO+SN+growth reimplementation wrapper.

The branch has earned the harder test.

It has not earned public theory promotion.
