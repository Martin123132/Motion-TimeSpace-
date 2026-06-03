# 290 - DESI Release no-SH0ES Robustness Readout

Private empirical robustness checkpoint. This is not a public cosmology, CMB, local-GR, or parent-field-theory claim.

## Purpose

Checkpoint 289 showed:

```text
removing SH0ES-style calibration pressure barely changed the generic 250-SN + DESI DR2 pattern.
```

This checkpoint keeps the same no-SH0ES setup and swaps BAO release:

```text
DESI DR2 -> DESI DR1.
```

The test is:

```text
does the fixed no-clock branch survive a DESI release split?
```

## Machine Artifacts

DR2 no-SH0ES score run:

```text
runs/20260601-101537-cosmo-SN-BAO-short-smoke
```

DR1 no-SH0ES dry run:

```text
runs/20260601-102027-cosmo-SN-BAO-closure-dryrun
```

DR1 no-SH0ES score run:

```text
runs/20260601-102042-cosmo-SN-BAO-short-smoke
```

Readout script:

```text
scripts/DESI_release_no_SH0ES_robustness_readout.py
```

Readout run:

```text
runs/20260601-000113-DESI-release-no-SH0ES-robustness-readout
```

Status:

```text
DESI_DR1_DR2_no_SH0ES_fixed_branch_survives_qualitatively_but_LCDM_BIC_gap_worsens
```

Claim ceiling:

```text
DESI_release_short_smoke_robustness_only_no_stable_evidence_or_parent_promotion
```

## Core Result

The fixed branch survives qualitatively under DR1, but the release split is not neutral.

| Release | Baseline | delta chi2 | delta AIC | delta BIC | Interpretation |
|---|---|---:|---:|---:|---|
| DR2 | LCDM | -2.645643735189168 | -0.645643735189168 | 2.926510296988596 | mixed |
| DR2 | wCDM | -1.4283628067233565 | -1.4283628067233565 | -1.4283628067233565 | beats |
| DR2 | CPL | 1.6462134456770627 | -0.35378655432293726 | -3.925940586500701 | IC win, raw chi2 worse |
| DR1 | LCDM | -1.1254897186614699 | 0.8745102813385301 | 4.442854785099627 | not preferred by IC |
| DR1 | wCDM | -1.0934198869737486 | -1.0934198869737486 | -1.0934198869737486 | beats |
| DR1 | CPL | 1.5383962700390157 | -0.4616037299609843 | -4.029948233722081 | IC win, raw chi2 worse |

So:

```text
the fixed branch still beats wCDM and CPL by BIC in DR1,
but its BIC loss to LCDM worsens from about 2.93 to about 4.44.
```

That is a robustness caution, not a promotion.

## Release Shift

Fixed-branch release shifts:

| Baseline | DR2 delta BIC | DR1 delta BIC | DR1 - DR2 |
|---|---:|---:|---:|
| LCDM | 2.926510296988596 | 4.442854785099627 | 1.5163444881110308 |
| wCDM | -1.4283628067233565 | -1.0934198869737486 | 0.3349429197496079 |
| CPL | -3.925940586500701 | -4.029948233722081 | -0.10400764672137974 |

Interpretation:

```text
DR1 weakens the fixed branch against LCDM and wCDM,
but slightly strengthens the IC comparison against CPL.
```

Because CPL hits the `wa` prior edge in both releases, the CPL comparison remains unstable.

## Amplitude Shift

The fitted fixed-shape amplitude moves:

```text
DR2 B_mem = 0.13874106497338232
DR1 B_mem = 0.15250879854297641
relative shift = +9.923329889557543%
```

This matters:

```text
the fitted amplitude is release-sensitive at the ~10% level in this short-smoke branch.
```

That reinforces the theory-side decision:

```text
do not claim B_mem is derived;
do not treat the fitted amplitude as stable evidence.
```

## Ablation Readout

The fitted-shape ablations still do not pay for themselves:

| Release | Ablation | delta chi2 vs fixed | delta AIC vs fixed | delta BIC vs fixed | Status |
|---|---|---:|---:|---:|---|
| DR2 | fitted `p` | -0.016249017003445942 | 1.983750982996554 | 5.555905015174318 | not promoted |
| DR2 | fitted `u3` | -0.24701561747215806 | 1.752984382527842 | 5.325138414705606 | not promoted |
| DR1 | fitted `p` | -0.037075114595126024 | 1.962924885404874 | 5.5312693891659706 | not promoted |
| DR1 | fitted `u3` | -0.13872554756437694 | 1.861274452435623 | 5.42961895619672 | not promoted |

So:

```text
release switching does not expose p=3 or u3=1/4 as obviously bad closures.
```

But:

```text
it also does not promote them to derived constants.
```

## Prior Edges

Prior-edge readout:

```text
DESI DR2: CPL wa = -2.0 edge
DESI DR1: CPL wa = -2.0 edge
MTS branches: no edge flags in either release
```

Therefore:

```text
stable evidence is still blocked by baseline-side CPL edge behaviour.
```

This is exactly why the comparison should be described as:

```text
robustness diagnostic,
not evidence claim.
```

## Gates

| Gate | Result | Meaning |
|---|---|---|
| DR2 schema | pass | comparator valid |
| DR1 schema | pass | DR1 branch valid |
| DR1 convergence | pass | all models converged |
| prior edges | fail | CPL edge in both releases |
| MTS prior edges | pass | no MTS edge flags |
| DR1 fixed branch competitiveness | mixed | beats wCDM/CPL BIC, not LCDM BIC |
| release shift against LCDM | warn | LCDM BIC gap worsens by 1.516 |
| ablation tax | pass | fitted `p/u3` not promoted |
| stable evidence allowed | fail | diagnostic only |

## What This Does and Does Not Mean

Allowed:

```text
The no-SH0ES fixed-shape branch survives the DESI DR1/DR2 split qualitatively.
```

Allowed:

```text
The DR1 split worsens the fixed branch against LCDM by BIC, so the branch remains competitive but not stable evidence.
```

Allowed:

```text
Fitted p/u3 ablations still do not beat the fixed branch by AIC/BIC.
```

Not allowed:

```text
MTS has stable cosmology evidence.
B_mem is derived.
MTS passes CMB.
MTS derives local GR.
MTS is a finished parent field theory.
```

Boxing-score version:

```text
DR1 did not knock the fixed branch down.
But it did take a cleaner round for LCDM than DR2 did.
So we stay in the fight, not on the podium.
```

## Output Files

DR1 scoring results:

```text
runs/20260601-102042-cosmo-SN-BAO-short-smoke/results/data_schema_report.csv
runs/20260601-102042-cosmo-SN-BAO-short-smoke/results/fit_summary.csv
runs/20260601-102042-cosmo-SN-BAO-short-smoke/results/baseline_comparison.csv
runs/20260601-102042-cosmo-SN-BAO-short-smoke/results/prior_edge_table.csv
runs/20260601-102042-cosmo-SN-BAO-short-smoke/results/amplitude_policy.csv
runs/20260601-102042-cosmo-SN-BAO-short-smoke/results/residuals.csv
```

Readout results:

```text
runs/20260601-000113-DESI-release-no-SH0ES-robustness-readout/results/source_register.csv
runs/20260601-000113-DESI-release-no-SH0ES-robustness-readout/results/score_readout.csv
runs/20260601-000113-DESI-release-no-SH0ES-robustness-readout/results/fixed_branch_comparison.csv
runs/20260601-000113-DESI-release-no-SH0ES-robustness-readout/results/release_score_shifts.csv
runs/20260601-000113-DESI-release-no-SH0ES-robustness-readout/results/fixed_branch_release_delta_shifts.csv
runs/20260601-000113-DESI-release-no-SH0ES-robustness-readout/results/amplitude_shift_readout.csv
runs/20260601-000113-DESI-release-no-SH0ES-robustness-readout/results/ablation_readout.csv
runs/20260601-000113-DESI-release-no-SH0ES-robustness-readout/results/prior_edge_readout.csv
runs/20260601-000113-DESI-release-no-SH0ES-robustness-readout/results/residual_summary.csv
runs/20260601-000113-DESI-release-no-SH0ES-robustness-readout/results/gate_results.csv
runs/20260601-000113-DESI-release-no-SH0ES-robustness-readout/results/decision.csv
```

## Next Step

Recommended:

```text
tighten the unstable CPL comparison before stronger cosmology language.
```

Two concrete options:

```text
1. rerun no-SH0ES DR1/DR2 with wider CPL wa prior to see whether the CPL edge is artificial;
2. run a full-sample/full-covariance version when runtime/data setup allows.
```

Near-term best:

```text
wider-CPL-prior short smoke,
because it directly tests whether the baseline edge is distorting the scorecard.
```
