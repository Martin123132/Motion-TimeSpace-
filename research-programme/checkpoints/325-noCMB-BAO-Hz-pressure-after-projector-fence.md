# 325 — No-CMB BAO+H(z) Pressure After Projector Fence

Private checkpoint. This is not a public cosmology, CMB, local-GR, PPN, or unified-field claim.

## Purpose

Checkpoint 324 fenced the local/projector branch:

```text
S3 singlet + screen bundle + S_D support label
```

is now precise conditional algebra, but it still lacks a parent derivation of:

```text
C_D,
[K_boundary,A_D]=0,
lifted J_C,
local GR,
B_mem=2/27.
```

So this checkpoint follows the disciplined route:

```text
do not promote the local theorem;
stress the locked late-time branch against external data.
```

The selected pressure test is no-CMB BAO+H(z), because it removes the SN support and does not rely on the unresolved CMB bridge.

## Machine Artifact

Script:

```text
scripts/BAO_Hz_noCMB_robustness.py
```

Run:

```text
runs/20260601-151500-BAO-Hz-noCMB-robustness
```

Status:

```text
noCMB_radial_robustness_stable_draw
```

Claim ceiling:

```text
no_CMB_BAO_Hz_robustness_only
```

## Models and Branches

Models fitted:

```text
LCDM,
wCDM,
CPL,
MTS_locked_2over27,
MTS_Bmem_zero.
```

Branches:

```text
12 total branches,
10 production branches,
2 diagnostic-only branches.
```

The data split includes:

```text
DESI DR2 BAO,
DESI DR1 BAO,
CC15 H(z),
CC32 H(z),
covariance and diagonal sensitivity variants.
```

No CMB prior, SN prior, BAO-shape correction, or Omega-map closure was inserted.

## Main Readout

Against fitted `LCDM`, the locked branch is a stable competitive draw.

| Group | Branches | Preferred | Draw | Disfavored | Delta BIC range | Verdict |
|---|---:|---:|---:|---:|---|---|
| production all BAO+H(z) vs `LCDM` | 10 | 0 | 10 | 0 | -1.901 to -0.580 | stable competitive draw |
| all branches including diagnostics vs `LCDM` | 12 | 0 | 12 | 0 | -2.000 to -0.580 | stable competitive draw |
| DESI DR2 production vs `LCDM` | 5 | 0 | 5 | 0 | -1.901 to -1.819 | stable competitive draw |
| DESI DR1 production vs `LCDM` | 5 | 0 | 5 | 0 | -0.658 to -0.580 | stable competitive draw |

Primary branch:

```text
BAO_DR2_plus_CC15_suggested
Delta BIC vs LCDM = -1.8838579373924915
Delta chi2 vs LCDM = -1.8838579373924897
readout = competitive_draw_by_BIC
locked edge flag = false
LCDM edge flag = false
```

Best production branch:

```text
BAO_DR2_plus_CC15_conservative_sensitivity
Delta BIC vs LCDM = -1.9014668577456
```

Worst production branch:

```text
BAO_DR1_plus_CC32_diagonal_sensitivity
Delta BIC vs LCDM = -0.5803932783513801
```

## Baseline Parity

On the primary branch:

| Reference | Delta chi2 | Delta AIC | Delta BIC | Readout | Reference edge? |
|---|---:|---:|---:|---|---:|
| `LCDM` | -1.8838579373924897 | -1.883857937392488 | -1.8838579373924915 | competitive draw | false |
| `wCDM` | -0.6988402268230924 | -2.6988402268230907 | -4.031044736998297 | locked preferred | false |
| `CPL` | 1.8183391598750962 | -2.181660840124902 | -4.846069860475314 | locked preferred | true |
| `MTS_Bmem_zero` | -1.8838579373924897 | -1.883857937392488 | -1.8838579373924915 | competitive draw | false |

The CPL comparison is not clean evidence because CPL hits the `wa=-2` prior edge in every production branch.

## Primary Fit Snapshot

For `BAO_DR2_plus_CC15_suggested`:

| Model | chi2 BAO | chi2 H(z) | chi2 total | BIC | dynamic k | edge flag | Omega_m0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `LCDM` | 10.2726540664 | 6.3041031159 | 16.5767571824 | 26.5733707129 | 3 | false | 0.2978393053 |
| `wCDM` | 9.0425482605 | 6.3491912113 | 15.3917394718 | 28.7205575125 | 4 | false | 0.2979798672 |
| `CPL` | 5.8654035827 | 7.0091565023 | 12.8745600851 | 29.5355826360 | 5 | true | 0.3650192207 |
| `MTS_locked_2over27` | 8.1631672128 | 6.5297320322 | 14.6928992450 | 24.6895127755 | 3 | false | 0.3042725199 |
| `MTS_Bmem_zero` | 10.2726540664 | 6.3041031159 | 16.5767571824 | 26.5733707129 | 3 | false | 0.2978393053 |

The locked branch improves BAO and loses a little H(z), giving a net draw-to-small-win readout under this no-CMB diagnostic.

## Omega Consistency

The locked branch stays close to the T7 late-time value:

```text
T7 Omega_m0 reference = 0.303282742677
primary locked Omega_m0 = 0.304272519940
primary shift = +0.000989777263
production mean shift = -0.000051792091
production min shift = -0.001262366522
production max shift = +0.001102614458
```

This is useful, but it is not a derivation of the early-late Omega map.

## What This Decides

This is a good result in the narrow boxing sense:

```text
MTS does not need to smash LCDM here.
It needs to stay competitive without sneaking in extra support.
```

It does that:

```text
all 10 production branches are BIC draws vs LCDM,
none disfavor the locked branch,
locked and LCDM fits are edge-clean,
the primary branch is close to the preferred side of the draw band.
```

But it does not decide:

```text
the parent origin of B_mem=2/27,
the local-GR reduction,
the CMB bridge,
the growth sector,
the full official-likelihood comparison.
```

## Theory Meaning

Allowed language:

```text
The locked 2/27 late-time branch remains externally viable under a no-CMB BAO+H(z) robustness matrix.
```

Stronger but still private/internal language:

```text
The branch scores like a disciplined contender: no knockout, no collapse, clean edge behavior, and repeated competitive draws.
```

Forbidden language:

```text
MTS is cosmologically preferred.
MTS passes CMB.
MTS derives GR.
B_mem=2/27 is parent-derived.
```

## Derivation Pressure

The run increases pressure on the theory side in a constructive way.

The empirical branch is saying:

```text
B_mem=2/27 is worth keeping alive.
```

The derivation branch is still saying:

```text
B_mem=2/27 is not yet parent-owned.
```

So the next derivation target should not be a vague new field insertion. It should be an exact contract:

```text
derive a radial-memory or activity-current term whose FLRW reduction fixes B_mem=2/27,
while its local/projector limit kills the ordinary coherent bath and preserves local GR.
```

The current minimal target is:

```text
J_C -> C_D,
A_D = C_D^\dagger C_D,
[K_boundary,A_D]=0,
C_D B_ord = 0,
C_D B_FLRW != 0,
FLRW trace ratio = 2/27.
```

That is the bridge between the local derivation work and the empirical survival signal.

## Decision

Decision:

```text
keep the locked 2/27 branch alive as an empirical theorem target;
do not promote it beyond closure;
move next to either growth pressure or a radial-memory parent-action contract.
```

Default next move:

```text
attempt the radial-memory parent-action contract first,
then use growth/H(z)-shape as the next external judge.
```

## Output Files

```text
runs/20260601-151500-BAO-Hz-noCMB-robustness/status.json
runs/20260601-151500-BAO-Hz-noCMB-robustness/results/source_register.csv
runs/20260601-151500-BAO-Hz-noCMB-robustness/results/data_schema.csv
runs/20260601-151500-BAO-Hz-noCMB-robustness/results/branch_manifest.csv
runs/20260601-151500-BAO-Hz-noCMB-robustness/results/fit_summary.csv
runs/20260601-151500-BAO-Hz-noCMB-robustness/results/sector_breakdown.csv
runs/20260601-151500-BAO-Hz-noCMB-robustness/results/prior_edge_table.csv
runs/20260601-151500-BAO-Hz-noCMB-robustness/results/residuals.csv
runs/20260601-151500-BAO-Hz-noCMB-robustness/results/baseline_comparisons.csv
runs/20260601-151500-BAO-Hz-noCMB-robustness/results/robustness_matrix.csv
runs/20260601-151500-BAO-Hz-noCMB-robustness/results/stability_summary.csv
runs/20260601-151500-BAO-Hz-noCMB-robustness/results/control_reproduction.csv
runs/20260601-151500-BAO-Hz-noCMB-robustness/results/omega_shift_matrix.csv
runs/20260601-151500-BAO-Hz-noCMB-robustness/results/decision.csv
```
