# 126 - H(z) Radial-Expansion Smoke

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 124 localized the joint BAO penalty mainly to:

```text
D_H(z) / r_s
```

Checkpoint 125 found local cosmic-chronometer H(z) data and a usable 15-row
covariance branch.

This checkpoint runs the promised independent radial-expansion smoke test:

```text
H(z) = 100 h E(z).
```

No BAO-shape correction, no CMB claim, no fitted Omega map.

## 2. Machine Artifact

Script:

```text
research-programme\scripts\Hz_radial_expansion_smoke.py
```

Run:

```text
research-programme\runs\20260531-175500-Hz-radial-expansion-smoke
```

Generated:

```text
source_register.csv
data_schema.csv
fit_summary.csv
prior_edge_table.csv
residuals.csv
baseline_comparisons.csv
control_reproduction.csv
decision.csv
status.json
```

Status:

```text
Hz_radial_smoke_LCDM_draw_flexible_edges
```

Claim ceiling:

```text
radial_expansion_stress_only
```

## 3. Primary Data Branch

Primary dataset:

```text
CC15_suggested_primary
```

Data:

```text
[local-formalization-workbench]\data\cosmology\cosmic_chronometers\covariance_branch\Hz_CC_Moresco15_BC03.csv
```

Covariance:

```text
[local-formalization-workbench]\data\cosmology\cosmic_chronometers\covariance_branch\covariance_suggested.csv
```

Rows:

```text
15
```

Model list:

```text
LCDM
wCDM
CPL
MTS_locked_2over27
MTS_Bmem_zero
```

## 4. Primary Fit Results

| Model | chi2 | AIC | BIC | Edge | `Omega_m0` | `H0` |
|---|---:|---:|---:|---|---:|---:|
| `LCDM` | `6.1128594336276905` | `10.11285943362769` | `11.528959835832111` | false | `0.33758094517058357` | `66.98574848423509` |
| `wCDM` | `5.414503680165549` | `11.414503680165549` | `13.538654283472178` | true | `0.32274291793022386` | `76.653239742944` |
| `CPL` | `5.384135484770669` | `13.384135484770669` | `16.21633628917951` | true | `0.3354009408411303` | `76.36310409367195` |
| `MTS_locked_2over27` | `6.445429002731165` | `10.445429002731165` | `11.861529404935585` | false | `0.33150416243811487` | `66.37840121541481` |
| `MTS_Bmem_zero` | `6.1128594336276905` | `10.11285943362769` | `11.528959835832111` | false | `0.33758094517058357` | `66.98574848423509` |

Primary comparison for locked MTS:

| Reference | Delta chi2 | Delta AIC | Delta BIC | Readout |
|---|---:|---:|---:|---|
| `LCDM` | `0.3325695691034749` | `0.3325695691034749` | `0.33256956910347313` | competitive draw |
| `wCDM` | `1.0309253225656168` | `-0.9690746774343832` | `-1.6771248785365938` | competitive draw, but `wCDM` edge-hit |
| `CPL` | `1.0612935179604968` | `-2.9387064820395032` | `-4.354806884243924` | locked preferred by BIC, but `CPL` edge-hit |
| `MTS_Bmem_zero` | `0.3325695691034749` | `0.3325695691034749` | `0.33256956910347313` | competitive draw |

Readout:

```text
Locked MTS draws LCDM on independent H(z). It does not win by chi2, but the
gap is tiny and stable.
```

## 5. Edge Flags

Primary edge flags:

```text
wCDM: w = -2.0
CPL: wa = -2.0
```

Locked MTS:

```text
no edge flag.
```

LCDM:

```text
no edge flag.
```

Therefore:

```text
Do not use the flexible-baseline comparison as stable evidence.
```

The fair primary read is:

```text
MTS_locked_2over27 vs LCDM = competitive draw.
```

## 6. Sensitivity Results

Locked MTS versus LCDM:

| Dataset branch | Delta chi2 | Delta BIC | Readout |
|---|---:|---:|---|
| `CC15_suggested_primary` | `0.3325695691034749` | `0.33256956910347313` | competitive draw |
| `CC15_diagonal_total_error_sensitivity` | `0.33423122494789137` | `0.33423122494789226` | competitive draw |
| `CC15_conservative_sensitivity` | `0.32269697400774877` | `0.32269697400774966` | competitive draw |
| `CC15_extra_conservative_sensitivity` | `0.3059726913592842` | `0.3059726913592833` | competitive draw |
| `CC15_nonstat_systematic_only_diagnostic` | `0.7511366115793585` | `0.7511366115793585` | competitive draw |
| `CC32_diagonal_sensitivity` | `0.36740925208060915` | `0.36740925208060915` | competitive draw |

The result is robust in a boring but useful way:

```text
MTS locked is consistently a near-LCDM draw in H(z).
```

It does not show the independent H(z) data demanding the MTS radial behaviour,
but it also does not punish it.

## 7. Negative Control

`MTS_Bmem_zero` reproduces LCDM exactly in every branch:

```text
delta_chi2 = 0
delta_Omega_m0 = 0
delta_h = 0
```

This is a good sanity check:

```text
the MTS background code reduces to LCDM when B_mem = 0.
```

## 8. Interpretation Against BAO Radial Pressure

Checkpoint 124 said the BAO joint penalty is radial-expansion dominated.

This H(z) test says:

```text
independent cosmic chronometer data do not strongly confirm that radial pressure,
but they tolerate the locked MTS radial history at LCDM-draw level.
```

That matters.

If H(z) had strongly rejected the locked branch, the BAO radial route would look
grim. It did not.

If H(z) had strongly preferred the locked branch, the radial theorem route would
look much stronger. It did not.

So the honest position is:

```text
neutral-to-survival.
```

Boxing-score version:

```text
This round is not a knockout. It is a clean defensive round: MTS stayed in the
pocket, took no serious damage, and made the flashy flexible baselines overreach
onto the ropes.
```

## 9. Decision

Allowed statement:

```text
Locked MTS is H(z)-competitive with LCDM on the 15-row covariance branch and on
the full32 diagonal sensitivity.
```

Allowed statement:

```text
The H(z) data do not independently prove the BAO radial-pressure interpretation.
```

Forbidden statement:

```text
MTS wins H(z) decisively.
```

Forbidden statement:

```text
MTS has derived a BAO radial correction.
```

Current status:

```text
radial stress survived as a draw; no promotion.
```

## 10. Next Target

Next checkpoint:

```text
127-radial-pressure-decision-gate.md
```

Task:

```text
Decide whether to:
1. attempt a radial H(z)/D_H theorem target,
2. build a joint BAO+H(z) diagnostic without CMB,
3. move to growth/fsigma8 as the next non-CMB stress test,
4. or return to local-GR/PPN derivation.
```

Recommendation:

```text
Build a BAO+H(z) no-CMB diagnostic next, because H(z) survived but did not
explain the BAO radial pressure by itself.
```

