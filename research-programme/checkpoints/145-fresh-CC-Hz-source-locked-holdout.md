# 145 - Fresh CC H(z) Source-Locked Holdout

Private empirical checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 144 said the clean next move was:

```text
one stricter independent late-time non-SN holdout.
```

So this checkpoint re-runs the H(z) round from fetched source tables, not just from remembered local files.

Question:

```text
Does frozen B_mem = 2/27 survive source-locked cosmic-chronometer H(z) data?
```

Short answer:

```text
yes, as a competitive draw.
```

Not a knockout. Not a theory promotion. But it stays on the judge's card.

## 2. Machine Artifact

Script:

```text
research-programme\scripts\fresh_CC_Hz_source_locked_holdout.py
```

Run:

```text
research-programme\runs\20260531-221500-fresh-CC-Hz-source-locked-holdout
```

Fetched source intake:

```text
research-programme\source-intake\cosmic_chronometers\20260531-221500
```

Generated:

```text
source_register.csv
source_url_register.csv
row_lock_comparison.csv
data_schema.csv
fit_summary.csv
prior_edge_table.csv
residuals.csv
baseline_comparisons.csv
control_reproduction.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
fresh_CC_source_locked_Hz_holdout_competitive_draw
```

Claim ceiling:

```text
fresh_CC_Hz_source_locked_holdout_no_theory_promotion
```

## 3. Source Lock

Fetched sources:

| Dataset | URL | Use |
|---|---|---|
| full 32-row CC H(z) table | `https://cluster.difa.unibo.it/astro/CC_data/data_CC.dat` | diagonal sensitivity only |
| 15-row Moresco BC03 branch | `https://gitlab.com/mmoresco/CCcovariance/-/raw/master/data/HzTable_MM_BC03.dat` | primary covariance branch row lock |

The source page warns that the full current CC dataset does not provide a full covariance matrix. So the full 32-row table is not promoted above diagonal sensitivity.

Row-lock check:

| Dataset | Source Rows | Local Rows | Max Numeric Delta | Reference Mismatches | Status |
|---|---:|---:|---:|---:|---|
| CC32 full table | 32 | 32 | `0.0` | 0 | pass |
| CC15 BC03 covariance branch | 15 | 15 | `0.0` | 0 | pass |

This means the local H(z) files used earlier match the freshly fetched source tables exactly for the checked numeric fields and references.

## 4. Scoring Setup

Same data rows and covariance are applied to:

```text
LCDM
wCDM
CPL
MTS_locked_2over27
MTS_Bmem_zero
```

Frozen rule:

```text
B_mem = 2/27 = 0.07407407407407407
```

No H(z) amplitude refit is introduced.

Primary dataset:

```text
source_CC15_BC03_suggested_primary
```

Sensitivity datasets:

```text
source_CC15_BC03_diagonal_total_error_sensitivity
source_CC15_BC03_conservative_sensitivity
source_CC15_BC03_extra_conservative_sensitivity
source_CC15_BC03_nonstat_systematic_only_diagnostic
source_CC32_diagonal_sensitivity
```

All six covariance/data shapes passed positive-definite or diagonal checks.

## 5. Primary Result

Primary source-locked H(z):

| Model | chi2 | BIC | Edge Flag |
|---|---:|---:|---|
| LCDM | `6.1128594336276905` | `11.528959835832111` | false |
| MTS locked 2/27 | `6.445429002731165` | `11.861529404935585` | false |
| wCDM | `5.414503680165549` | `13.538654283472178` | true |
| CPL | `5.384135484770669` | `16.21633628917951` | true |

MTS locked vs LCDM:

```text
Delta chi2 = 0.3325695691034749
Delta AIC  = 0.3325695691034749
Delta BIC  = 0.33256956910347313
```

Readout:

```text
competitive_draw_by_BIC
```

The flexible baselines reduce chi2, but they hit prior edges and pay parameter penalties. This is exactly why this is a scoring-card result, not a handwave.

## 6. Sensitivity Card

MTS locked vs LCDM across all H(z) branches:

| Dataset | Delta BIC | Readout |
|---|---:|---|
| CC15 suggested primary | `0.33256956910347313` | competitive draw |
| CC15 diagonal total error | `0.33423122494789226` | competitive draw |
| CC15 conservative | `0.32269697400774966` | competitive draw |
| CC15 extra conservative | `0.3059726913592833` | competitive draw |
| CC15 nonstat systematic diagnostic | `0.7511366115793585` | competitive draw |
| CC32 diagonal sensitivity | `0.36740925208060915` | competitive draw |

Card total:

```text
preferred = 0
draws = 6
disfavored = 0
```

## 7. Gates

| Gate | Status | Evidence |
|---|---|---|
| source fetch | pass | CC32 rows `32`; CC15 rows `15` |
| row lock against local tables | pass | both source tables match local tables |
| covariance shapes positive | pass | 6 datasets checked |
| frozen `B_mem` no refit | pass | `B_mem=0.07407407407407407` |
| primary H(z) not disfavored vs LCDM | pass | primary `DeltaBIC=0.33256956910347313` |
| all H(z) sensitivities not disfavored vs LCDM | pass | disfavored count `0` |
| theory promotion | fail | H(z) cannot derive action, amplitude, CMB, or local GR |

## 8. Judge's Card

This is a Mayweather round, not a Tyson round:

```text
MTS does not smash LCDM on H(z).
LCDM does not smash MTS either.
MTS survives with the amplitude frozen and no extra H(z) knob.
```

That matters because H(z) is independent of SN and does not rely on the CMB bridge.

But the limit is equally important:

```text
H(z) does not independently demand the MTS radial behaviour.
```

So the honest wording is:

```text
fresh source-locked CC H(z) supports late-time survivability, not promotion.
```

## 9. Next Target

The next empirical target should not be another lightweight H(z) replay.

Best next choices:

```text
official_likelihood_or_growth_covariance_holdout
```

In practical terms:

1. build a stricter growth/RSD covariance holdout, or
2. move toward an official/full-likelihood BAO+SN+growth reimplementation.

The branch has now earned that harder test:

```text
frozen amplitude, source-locked H(z), no disfavored H(z) branch.
```

Still forbidden:

```text
MTS passes CMB.
MTS derives B_mem.
MTS derives perturbations.
MTS derives local GR.
```
