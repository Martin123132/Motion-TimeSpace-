# 130 - Growth Route Gate

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 129 left the no-CMB radial branch in a useful state:

```text
stable competitive draw vs LCDM across DR1/DR2 BAO + H(z)
no disfavored production branch
no CMB prior
no Omega-map patch
```

The next stress test was:

```text
Does the same locked background survive an independent growth / f_sigma8 route?
```

## 2. Machine Artifact

Script:

```text
research-programme\scripts\growth_route_gate.py
```

Run:

```text
research-programme\runs\20260531-183400-growth-route-gate
```

Generated:

```text
source_register.csv
data_schema.csv
background_params.csv
fit_summary.csv
baseline_comparisons.csv
control_reproduction.csv
residuals.csv
decision.csv
status.json
```

Status:

```text
growth_gate_locked_primary_preferred_or_draw
```

Claim ceiling:

```text
conditional_growth_gate_only_no_MTS_perturbation_claim
```

## 3. Fairness Contract

This gate is conditional, not a derived perturbation theory.

Fixed inputs:

```text
backgrounds from checkpoint 129
BAO alpha from the same no-CMB background fits
locked B_mem = 2/27
p = 3
u3 = 1/4
```

Allowed fitted freedom:

```text
sigma8_0 only
```

The same `sigma8_0` freedom is given to:

```text
LCDM
wCDM
CPL
MTS_locked_2over27
MTS_Bmem_zero
```

No CMB priors are used.

No extra MTS perturbation term is fitted.

The growth equation used here is the GR background-growth proxy:

```text
D'' + [2 + d ln H / d ln a] D' - 3 Omega_m(a) D / 2 = 0
```

That is a stress tool, not a derivation of MTS structure growth.

## 4. Data Used

Primary recommended SDSS/eBOSS BAO+FS files:

```text
MGS
BOSS DR12 LRG
eBOSS DR16 LRG
eBOSS DR16 QSO
```

Primary rows:

```text
14 total rows
5 f_sigma8 rows
9 geometry rows
```

Robustness full-shape-only files:

```text
BOSS DR12 LRG
eBOSS DR16 LRG
eBOSS DR16 QSO
```

Robustness rows:

```text
12 total rows
4 f_sigma8 rows
8 geometry rows
```

The ELG grid likelihood is intentionally excluded because it needs a separate grid-likelihood parser.

All covariance matrices used here passed positive-definite schema checks.

## 5. Primary DR2 Background Result

Primary background:

```text
DR2_noCMB_primary
source = BAO_DR2_plus_CC15_suggested
```

### BAO+FS all rows

| Model | chi2 | n | sigma8_0 | Edge | Omega_m0 | BAO alpha |
|---|---:|---:|---:|---|---:|---:|
| `LCDM` | `16.760271551343266` | `14` | `0.8688417011864101` | false | `0.2978393053380677` | `29.53330084638998` |
| `wCDM` | `13.914502904076787` | `14` | `0.8873719885141129` | false | `0.29797986716272895` | `30.046054467881287` |
| `CPL` | `13.963961122285223` | `14` | `0.8777006500420642` | false | `0.3650192206963086` | `32.08038804261726` |
| `MTS_locked_2over27` | `14.456701270987548` | `14` | `0.882363171410198` | false | `0.3042725199400447` | `30.034792746095537` |
| `MTS_Bmem_zero` | `16.760271551343266` | `14` | `0.8688417011864101` | false | `0.2978393053380677` | `29.53330084638998` |

Locked MTS comparisons:

| Reference | Delta chi2 | Readout |
|---|---:|---|
| `LCDM` | `-2.303570280355718` | locked preferred |
| `wCDM` | `0.5421983669107604` | competitive draw |
| `CPL` | `0.49274014870232463` | competitive draw, but CPL background edge-hit |
| `MTS_Bmem_zero` | `-2.303570280355718` | locked preferred |

This is the strongest clean growth-route result in this pass.

## 6. RSD-Only Check

Same DR2 background, but using only the `f_sigma8` rows:

| Model | chi2 | n | sigma8_0 | Edge |
|---|---:|---:|---:|---|
| `LCDM` | `3.3591667969528` | `5` | `0.8582171843437892` | false |
| `wCDM` | `2.9596519521554683` | `5` | `0.8735403199421852` | false |
| `CPL` | `2.887680249205501` | `5` | `0.8569784212380465` | false |
| `MTS_locked_2over27` | `3.0244808202051328` | `5` | `0.8673161472723515` | false |
| `MTS_Bmem_zero` | `3.3591667969528` | `5` | `0.8582171843437892` | false |

Locked MTS comparisons:

| Reference | Delta chi2 | Readout |
|---|---:|---|
| `LCDM` | `-0.3346859767476671` | competitive draw |
| `wCDM` | `0.06482886804966448` | competitive draw |
| `CPL` | `0.1368005709996316` | competitive draw, but CPL background edge-hit |

Interpretation:

```text
The primary BAO+FS point is not pure growth-amplitude evidence.
The RSD-only slice says MTS stays in the pack.
```

That is still good. It means growth does not immediately punch the locked branch in the mouth.

## 7. Full-Shape Transfer Check

The `sigma8_0` fitted on primary BAO+FS all rows was transferred to the full-shape-only robustness set.

DR2 locked MTS vs LCDM:

```text
all rows Delta chi2 = -0.22215672144448284
RSD-only Delta chi2 = -0.3049232482226305
```

Readout:

```text
competitive draw
```

So the primary preference does not turn into a full-shape-only loss.

## 8. DR1 Background Sensitivity

Using the DR1 no-CMB background instead:

```text
primary BAO+FS all rows, locked MTS vs LCDM:
Delta chi2 = -2.550113706585332
```

RSD-only:

```text
Delta chi2 = -0.32232137858804055
```

Full-shape transfer:

```text
all rows Delta chi2 = -0.332607952586228
RSD-only Delta chi2 = -0.2923046384315202
```

Readout:

```text
primary BAO+FS all rows: locked preferred vs LCDM
RSD-only and full-shape transfer: competitive draws
```

This is useful because DR1 weakened the radial BAO+H(z) near-win in checkpoint 129, but it did not weaken the growth-route gate.

## 9. Controls

Negative control:

```text
MTS_Bmem_zero reproduced LCDM in all 8 growth-stage control rows.
```

Edge flags:

```text
locked MTS sigma8_0: no edge
LCDM sigma8_0: no edge
wCDM sigma8_0: no edge
CPL sigma8_0: no edge
```

Important caveat:

```text
CPL inherited a background edge from the no-CMB BAO+H(z) fit.
```

So CPL can be compared as a stress baseline, but not treated as clean stable evidence.

## 10. Interpretation

This is a positive gate result.

What survived:

```text
The locked 2/27 background is compatible with SDSS/eBOSS BAO+FS growth data
under a one-parameter sigma8_0 stress, and it scores a primary BAO+FS point
against LCDM on both DR2 and DR1 no-CMB backgrounds.
```

What did not get proven:

```text
MTS perturbations are not derived.
The growth equation is still the GR proxy on the MTS background.
The primary advantage is not isolated to f_sigma8-only rows.
```

Boxing-score version:

```text
This was not just staying alive.
On the primary BAO+FS card MTS nicked the round off LCDM.
On pure RSD and full-shape transfer it boxed to a draw.
That is exactly the kind of Mayweather round we wanted.
```

## 11. Decision

Do not demote the locked branch.

Do not claim a derived growth theory yet.

Promote this to a serious theorem target:

```text
A future parent perturbation sector should reproduce, or improve on, the
conditional GR-growth-proxy survival seen here without fitting an extra MTS
growth-amplitude parameter beyond the shared sigma8_0.
```

Recommended next step:

```text
Build 131-growth-perturbation-contract.md.
```

The contract should specify exactly what a derived MTS perturbation equation must provide:

```text
1. background limit equal to the locked 2/27 branch;
2. matter conservation / Bianchi consistency;
3. a growth equation reducing to GR when B_mem -> 0;
4. no new unconstrained scale-dependent growth fudge;
5. a clean prediction for f_sigma8(z), not only distance geometry;
6. a rule for when BAO+FS geometry and RSD-only rows may be jointly interpreted.
```

Reason:

```text
The empirical branch has now survived SN+BAO, BAO-only, BAO+H(z), and a first
growth gate. The bottleneck has moved from scoring to derivation.
```
