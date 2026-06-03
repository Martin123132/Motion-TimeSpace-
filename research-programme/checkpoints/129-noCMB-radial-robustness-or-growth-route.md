# 129 - No-CMB Radial Robustness or Growth Route

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 128 found a near-point-win / strong draw:

```text
DESI DR2 BAO + H(z), no CMB:
locked MTS vs LCDM Delta BIC = -1.8838579373924915
```

This was close to the predeclared `-2` preference line but did not cross it.

So the next fair test was:

```text
Does the no-CMB radial result survive BAO-release and H(z)-covariance changes?
```

## 2. Machine Artifact

Script:

```text
research-programme\scripts\BAO_Hz_noCMB_robustness.py
```

Run:

```text
research-programme\runs\20260531-181900-BAO-Hz-noCMB-robustness
```

Generated:

```text
source_register.csv
data_schema.csv
branch_manifest.csv
fit_summary.csv
sector_breakdown.csv
prior_edge_table.csv
residuals.csv
baseline_comparisons.csv
robustness_matrix.csv
stability_summary.csv
control_reproduction.csv
omega_shift_matrix.csv
decision.csv
status.json
```

Status:

```text
noCMB_radial_robustness_stable_draw
```

Claim ceiling:

```text
no_CMB_BAO_Hz_robustness_only
```

## 3. Test Matrix

BAO releases:

```text
DESI DR2 primary
DESI DR1 primary
```

H(z) branches:

```text
CC15 suggested primary
CC15 diagonal-total-error covariance
CC15 conservative covariance
CC15 extra-conservative covariance
CC32 diagonal sensitivity
CC15 nonstat-systematic-only diagnostic
```

Production branches exclude the nonstat-systematic-only diagnostic.

Models:

```text
LCDM
wCDM
CPL
MTS_locked_2over27
MTS_Bmem_zero
```

The nuisance calibration treatment remains symmetric:

```text
BAO alpha is profiled for every model.
```

No CMB prior, no BAO-shape correction, and no Omega-map closure were introduced.

## 4. Stability Summary vs LCDM

Locked MTS compared with fitted LCDM:

| Group | Branches | Preferred | Draw | Disfavored | Min Delta BIC | Max Delta BIC | Mean Delta BIC | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Production all BAO+H(z) branches | `10` | `0` | `10` | `0` | `-1.9014668577456` | `-0.5803932783513801` | `-1.2546992707348434` | stable competitive draw |
| All branches including nonstat diagnostic | `12` | `0` | `12` | `0` | `-1.9999118889934095` | `-0.5803932783513801` | `-1.2770210114066354` | stable competitive draw |
| DESI DR2 production | `5` | `0` | `5` | `0` | `-1.9014668577456` | `-1.819201726139518` | `-1.8761909618372556` | stable competitive draw |
| DESI DR1 production | `5` | `0` | `5` | `0` | `-0.6582039934909574` | `-0.5803932783513801` | `-0.6332075796324311` | stable competitive draw |

Key point:

```text
DR2 keeps the near-point-win shape.
DR1 weakens it to a cleaner draw.
Neither release produces a loss.
```

## 5. Primary DR2 Branch

Primary branch:

```text
BAO_DR2_plus_CC15_suggested
```

| Model | BAO chi2 | H(z) chi2 | Total chi2 | BIC | Edge | Omega_m0 | H0 | BAO alpha |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| `LCDM` | `10.272654066432164` | `6.304103115931127` | `16.57675718236329` | `26.573370712888902` | false | `0.2978393053380677` | `68.68680551265663` | `29.53330084638998` |
| `wCDM` | `9.04254826049188` | `6.349191211302014` | `15.391739471793894` | `28.720557512494707` | false | `0.29797986716272895` | `67.46300989521606` | `30.046054467881287` |
| `CPL` | `5.865403582748783` | `7.009156502346921` | `12.874560085095705` | `29.535582635971725` | true | `0.3650192206963086` | `62.8338810913986` | `32.08038804261726` |
| `MTS_locked_2over27` | `8.163167212786957` | `6.529732032183844` | `14.692899244970802` | `24.68951277549641` | false | `0.3042725199400447` | `67.50994528839665` | `30.034792746095537` |
| `MTS_Bmem_zero` | `10.272654066432164` | `6.304103115931127` | `16.57675718236329` | `26.573370712888902` | false | `0.2978393053380677` | `68.68680551265663` | `29.53330084638998` |

Primary comparisons:

| Reference | Delta chi2 | Delta BIC | Readout |
|---|---:|---:|---|
| `LCDM` | `-1.8838579373924897` | `-1.8838579373924915` | competitive draw |
| `wCDM` | `-0.6988402268230924` | `-4.031044736998297` | locked preferred by BIC |
| `CPL` | `1.8183391598750962` | `-4.846069860475314` | locked preferred by BIC, but CPL edge-hit |

Omega comparison:

```text
T7 late-only Omega_m0 = 0.3032827426766658
DR2 BAO+H(z) locked Omega_m0 = 0.3042725199400447
shift = +0.000989777263379
```

So the no-CMB DR2 result stays essentially on the late-only value.

## 6. DR1 Release Check

DR1 suggested branch:

```text
BAO_DR1_plus_CC15_suggested
```

| Model | BAO chi2 | H(z) chi2 | Total chi2 | BIC | Edge | Omega_m0 | H0 | BAO alpha |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| `LCDM` | `12.746760189154724` | `6.3333977182705015` | `19.080157907425225` | `28.967668505438212` | false | `0.2950601929638249` | `68.8077847539072` | `29.436766705748663` |
| `wCDM` | `12.710193683284112` | `6.3371953056896135` | `19.047388988973726` | `32.23073645299104` | false | `0.29550695599978327` | `68.45587056575319` | `29.583884814832583` |
| `CPL` | `9.98227899275046` | `6.935181010229181` | `16.91746000297964` | `33.39664433300129` | true | `0.35723563566524086` | `63.837507053248785` | `31.56758945118397` |
| `MTS_locked_2over27` | `11.894689314275936` | `6.544827201073845` | `18.43951651534978` | `28.327027113362767` | false | `0.3020203761550072` | `67.60467915954771` | `29.955526758086783` |
| `MTS_Bmem_zero` | `12.746760189154724` | `6.3333977182705015` | `19.080157907425225` | `28.967668505438212` | false | `0.2950601929638249` | `68.8077847539072` | `29.436766705748663` |

DR1 suggested comparisons:

| Reference | Delta BIC | Readout |
|---|---:|---|
| `LCDM` | `-0.6406413920754446` | competitive draw |
| `wCDM` | `-3.9037093396282714` | locked preferred by BIC |
| `CPL` | `-5.069617219638523` | locked preferred by BIC, but CPL edge-hit |

Omega comparison:

```text
T7 late-only Omega_m0 = 0.3032827426766658
DR1 BAO+H(z) locked Omega_m0 = 0.3020203761550072
shift = -0.0012623665216586
```

DR1 does not reproduce the near `-2` LCDM pressure seen in DR2, but it also does not punish the locked branch.

## 7. Controls and Edge Flags

Controls:

```text
MTS_Bmem_zero reproduced LCDM in all 12 branches.
```

Edge flags:

```text
locked MTS: no production edge flags
LCDM: no production edge flags
wCDM: no production edge flags
CPL: edge-hit in production branches
```

This matters because the flexible baseline with the lowest raw chi2 is not automatically stable evidence if it buys that score at a prior edge.

## 8. Interpretation

This is a good robustness result, but not a promotion theorem.

What survived:

```text
The locked 2/27 branch remains competitive with LCDM across DR1/DR2 and H(z)
covariance changes, with no disfavored no-CMB production branch.
```

What did not survive as a claim:

```text
The DR2 near-win is not release-independent enough to call a decisive LCDM beat.
DR1 turns the effect into an ordinary draw.
```

So the fair scorecard is:

```text
vs LCDM: stable points draw
vs wCDM: BIC preference for locked MTS across production branches
vs CPL: BIC preference for locked MTS, but CPL edge-hits must be reported
```

Boxing-score version:

```text
DR2 made the judge lean forward.
DR1 made the judge sit back down.
But nobody scored the round against MTS.
```

## 9. Decision

Do not demote the no-CMB radial branch.

Do not promote it as a derived or decisive cosmological result.

Use it as a stable empirical target:

```text
Any future parent/radial theorem should naturally produce a background branch
that behaves like the locked 2/27 form and remains near the late-only Omega_m0
without requiring a compressed-CMB Omega-map patch.
```

The next best route is one of:

```text
1. Growth route: test whether the same locked background is compatible with
   growth/fsigma8 without giving itself extra freedom.

2. Radial theorem contract: derive the H(z)/D_H memory-shape term that explains
   why DR2 sees stronger radial pressure than DR1.
```

Recommended next step:

```text
Run the growth route gate before attempting another parent-theorem leap.
```

Reason:

```text
The no-CMB radial branch is now stable enough to keep, but not sharp enough to
declare. Growth gives an independent field-theory stress before we spend more
tokens trying to derive the radial operator.
```
