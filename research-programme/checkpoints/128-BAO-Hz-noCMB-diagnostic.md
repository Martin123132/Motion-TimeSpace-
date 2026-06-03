# 128 - BAO + H(z) No-CMB Diagnostic

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 127 selected the clean no-CMB radial diagnostic:

```text
DESI DR2 BAO shape + cosmic chronometer H(z)
```

with:

```text
BAO alpha profiled
no compressed CMB priors
no BAO-shape correction
no Omega-map fit
```

## 2. Machine Artifact

Script:

```text
research-programme\scripts\BAO_Hz_noCMB_diagnostic.py
```

Run:

```text
research-programme\runs\20260531-180700-BAO-Hz-noCMB-diagnostic
```

Generated:

```text
source_register.csv
data_schema.csv
fit_summary.csv
sector_breakdown.csv
prior_edge_table.csv
residuals.csv
baseline_comparisons.csv
control_reproduction.csv
decision.csv
status.json
```

Status:

```text
BAO_Hz_noCMB_LCDM_draw
```

Claim ceiling:

```text
no_CMB_BAO_Hz_diagnostic_only
```

## 3. Primary Branch

Primary dataset:

```text
BAO_DR2_plus_CC15_suggested
```

Model set:

```text
LCDM
wCDM
CPL
MTS_locked_2over27
MTS_Bmem_zero
```

Parameter count includes:

```text
BAO alpha as one profiled nuisance.
```

## 4. Primary Fit Results

| Model | BAO chi2 | H(z) chi2 | Total chi2 | AIC | BIC | Edge | `Omega_m0` | `H0` | `BAO alpha` |
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|
| `LCDM` | `10.272654066432164` | `6.304103115931127` | `16.57675718236329` | `22.57675718236329` | `26.573370712888902` | false | `0.2978393053380677` | `68.68680551265663` | `29.53330084638998` |
| `wCDM` | `9.04254826049188` | `6.349191211302014` | `15.391739471793894` | `23.391739471793894` | `28.720557512494707` | false | `0.29797986716272895` | `67.46300989521606` | `30.046054467881287` |
| `CPL` | `5.865403582748783` | `7.009156502346921` | `12.874560085095705` | `22.874560085095705` | `29.535582635971725` | true | `0.3650192206963086` | `62.8338810913986` | `32.08038804261726` |
| `MTS_locked_2over27` | `8.163167212786957` | `6.529732032183844` | `14.692899244970802` | `20.692899244970803` | `24.68951277549641` | false | `0.3042725199400447` | `67.50994528839665` | `30.034792746095537` |
| `MTS_Bmem_zero` | `10.272654066432164` | `6.304103115931127` | `16.57675718236329` | `22.57675718236329` | `26.573370712888902` | false | `0.2978393053380677` | `68.68680551265663` | `29.53330084638998` |

## 5. Primary Comparisons

Locked MTS against references:

| Reference | Delta chi2 | Delta AIC | Delta BIC | Readout |
|---|---:|---:|---:|---|
| `LCDM` | `-1.8838579373924897` | `-1.883857937392488` | `-1.8838579373924915` | competitive draw |
| `wCDM` | `-0.6988402268230924` | `-2.6988402268230907` | `-4.031044736998297` | locked preferred by BIC |
| `CPL` | `1.8183391598750962` | `-2.181660840124902` | `-4.846069860475314` | locked preferred by BIC, but CPL edge-hit |
| `MTS_Bmem_zero` | `-1.8838579373924897` | `-1.883857937392488` | `-1.8838579373924915` | competitive draw |

Important:

```text
The LCDM comparison is just shy of the predeclared -2 BIC preference line.
So this is a strong draw / near-point-win, not a declared win.
```

## 6. Sector Balance

Locked MTS primary sector split:

```text
BAO chi2 = 8.163167212786957
H(z) chi2 = 6.529732032183844
```

The combined score is BAO-dominated, but H(z) does not fight the locked branch.

Compared with T7:

```text
T7 Omega_m0 = 0.3032827426766658
no-CMB BAO+H(z) Omega_m0 = 0.3042725199400447
shift = +0.000989777263379
```

So the no-CMB radial diagnostic keeps the locked branch almost exactly on the
late-only BAO/SN value, unlike the compressed CMB bridge.

## 7. Sensitivity Results

Locked MTS vs LCDM across sensitivity branches:

| Dataset | Delta chi2 | Delta BIC | Readout |
|---|---:|---:|---|
| `BAO_DR2_plus_CC15_suggested` | `-1.8838579373924897` | `-1.8838579373924915` | competitive draw |
| `BAO_DR2_plus_CC15_diagonal_total_error_sensitivity` | `-1.8835737097080028` | `-1.8835737097080028` | competitive draw |
| `BAO_DR2_plus_CC15_conservative_sensitivity` | `-1.9014668577456` | `-1.9014668577456` | competitive draw |
| `BAO_DR2_plus_CC15_extra_conservative_sensitivity` | `-1.8928545782006658` | `-1.8928545782006658` | competitive draw |
| `BAO_DR2_plus_CC15_nonstat_systematic_only_diagnostic` | `-1.9999118889934024` | `-1.9999118889934095` | competitive draw by threshold |
| `BAO_DR2_plus_CC32_diagonal_sensitivity` | `-1.819201726139518` | `-1.819201726139518` | competitive draw |

This is strikingly stable:

```text
every branch lands near Delta BIC ~= -1.8 to -2.0 versus LCDM.
```

But the threshold discipline matters:

```text
near win is still a draw unless it crosses the declared line.
```

## 8. Edge Flags and Controls

Primary edge flag:

```text
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

Negative control:

```text
MTS_Bmem_zero reproduces LCDM exactly in every branch.
```

This means the code path is behaving correctly.

## 9. Interpretation

This is the best no-CMB radial result so far:

```text
BAO + H(z), without CMB, puts locked MTS in a very strong draw with LCDM and
preferred by BIC over wCDM/CPL once parameter cost is counted.
```

But:

```text
it is not a decisive win over LCDM,
and it is not a derivation of radial BAO physics.
```

What it does say:

```text
the compressed CMB bridge is the thing creating the damaging Omega_m0 shift.
Without CMB, BAO+H(z) keeps MTS near the late-only locked value and remains
competitive.
```

Boxing-score version:

```text
This is a proper counterpunch. Not a knockout, but it made the no-CMB judge
look very interested.
```

## 10. Decision

Allowed statement:

```text
No-CMB BAO+H(z) gives locked MTS a stable near-win / competitive draw against
LCDM, with Delta BIC about -1.88.
```

Allowed statement:

```text
The no-CMB diagnostic supports treating the compressed CMB bridge as the live
source of the damaging Omega_m0 shift.
```

Forbidden statement:

```text
MTS beats LCDM decisively.
```

Forbidden statement:

```text
MTS has derived the radial BAO correction.
```

Current status:

```text
promising no-CMB radial diagnostic; no promotion.
```

## 11. Next Target

Next checkpoint:

```text
129-noCMB-radial-robustness-or-growth-route.md
```

Recommended move:

```text
Run a no-CMB robustness pass around this BAO+H(z) near-win:
DR1/DR2 BAO split, CC15 covariance variants, full32 diagonal, and maybe an
Omega_m0-fixed transfer check.
```

Only after that should we decide whether to:

```text
attempt a radial theorem,
move to growth,
or return to local-GR/PPN.
```

