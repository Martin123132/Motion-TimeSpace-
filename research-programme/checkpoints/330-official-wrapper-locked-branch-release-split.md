# 330 — Official Wrapper Locked-Branch Release Split

Private empirical checkpoint. This is not a public cosmology, CMB, local-GR, PPN, perturbation-theory, or unified-field claim.

## Purpose

Checkpoint 329 showed the locked late-time branch survives a source-locked growth covariance stress test, but only as a GR-proxy growth diagnostic.

This checkpoint returns to the official-likelihood wrapper lane:

```text
full Pantheon+ shape information,
full Pantheon+ covariance,
no SH0ES calibrator pressure,
DESI DR2/DR1 BAO release split,
same nuisance policy for MTS and baselines.
```

It also fixes a branch-contract bug before taking the score seriously:

```text
MTS_fixed_p3_u3quarter fixed p=3 and u3=1/4,
but it still fitted B_mem.
```

So the runner now scores the actual primary branch:

```text
MTS_fixed_2over27_no_clock:
p = 3,
u3 = 1/4,
B_mem = 2/27,
no global clock.
```

The fitted-amplitude branch remains in the output, but only as a diagnostic.

## Machine Artifacts

Patched runner:

```text
scripts/cosmo_SN_BAO_closure_runner.py
```

Updated wrapper preflight:

```text
runs/20260601-175000-official-likelihood-wrapper-preflight
```

Dry-runs:

```text
runs/20260601-173800-DR2-locked2over27-fullcov-noSH0ES-cosmo-SN-BAO-closure-dryrun
runs/20260601-173900-DR1-locked2over27-fullcov-noSH0ES-cosmo-SN-BAO-closure-dryrun
```

Short-smoke scores:

```text
runs/20260601-174000-DR2-locked2over27-fullcov-noSH0ES-cosmo-SN-BAO-short-smoke
runs/20260601-174500-DR1-locked2over27-fullcov-noSH0ES-cosmo-SN-BAO-short-smoke
```

Statuses:

```text
dry_run_pass_data_candidates_validated
short_smoke_scores_written_no_edge_flags
```

Claim ceiling:

```text
closure_testing_only_no_stable_evidence_or_theory_promotion
```

## Branch Contract

The scored model set is now:

```text
LCDM,
wCDM,
CPL,
MTS_fixed_2over27_no_clock,
MTS_fixed_p3_u3quarter,
MTS_Bmem_zero.
```

Read the two MTS memory branches differently:

| Branch | Meaning | Promotion status |
|---|---|---|
| `MTS_fixed_2over27_no_clock` | true locked closure branch | primary diagnostic |
| `MTS_fixed_p3_u3quarter` | fitted `B_mem` with `p=3`, `u3=1/4` | amplitude proximity diagnostic only |
| `MTS_Bmem_zero` | zero-memory limit | must reproduce LCDM |

The correction matters because a fitted branch can look like support for `2/27` while still spending a parameter. This checkpoint separates:

```text
does the exact locked value work?
```

from:

```text
where would the data fit the amplitude if allowed?
```

## DR2 Full-Cov No-SH0ES Result

Dataset:

```text
Pantheon+ mb-corr, calibrators excluded,
full Pantheon+ covariance,
DESI DR2 full BAO covariance.
```

Fit snapshot:

| Model | chi2 total | AIC | BIC | k | edge |
|---|---:|---:|---:|---:|---:|
| `LCDM` | 1470.5278726785 | 1476.5278726785 | 1492.7297344107 | 3 | false |
| `wCDM` | 1465.4374150731 | 1473.4374150731 | 1495.0398973826 | 4 | false |
| `CPL` | 1465.1006781972 | 1475.1006781972 | 1502.1037810841 | 5 | false |
| `MTS_fixed_2over27_no_clock` | 1465.2684058008 | 1471.2684058008 | 1487.4702675329 | 3 | false |
| `MTS_fixed_p3_u3quarter` | 1465.2682140070 | 1473.2682140070 | 1494.8706963165 | 4 | false |
| `MTS_Bmem_zero` | 1470.5278726785 | 1476.5278726785 | 1492.7297344107 | 3 | false |

Locked branch versus baselines:

| Reference | Delta chi2 | Delta AIC | Delta BIC |
|---|---:|---:|---:|
| `LCDM` | -5.2594668778 | -5.2594668778 | -5.2594668778 |
| `wCDM` | -0.1690092723 | -2.1690092723 | -7.5696298497 |
| `CPL` | +0.1677276036 | -3.8322723964 | -14.6335135512 |

Against `LCDM`, this is a clean same-parameter win inside this short-smoke wrapper:

```text
same k = 3,
no MTS prior edge,
zero-memory control reproduces LCDM exactly.
```

Against `wCDM` and `CPL`, the useful readout is not a chi2 knockout. It is the Mayweather readout:

```text
MTS stays essentially level on chi2,
then wins AIC/BIC by not spending extra equation-of-state freedom.
```

## DR1 Full-Cov No-SH0ES Result

Dataset:

```text
Pantheon+ mb-corr, calibrators excluded,
full Pantheon+ covariance,
DESI DR1 full BAO covariance.
```

Fit snapshot:

| Model | chi2 total | AIC | BIC | k | edge |
|---|---:|---:|---:|---:|---:|
| `LCDM` | 1472.5810840390 | 1478.5810840390 | 1494.7811125905 | 3 | false |
| `wCDM` | 1469.3437493923 | 1477.3437493923 | 1498.9437874609 | 4 | false |
| `CPL` | 1468.5797888306 | 1478.5797888306 | 1505.5798364165 | 5 | false |
| `MTS_fixed_2over27_no_clock` | 1468.9623256906 | 1474.9623256906 | 1491.1623542421 | 3 | false |
| `MTS_fixed_p3_u3quarter` | 1468.9620417738 | 1476.9620417738 | 1498.5620798425 | 4 | false |
| `MTS_Bmem_zero` | 1472.5810840390 | 1478.5810840390 | 1494.7811125905 | 3 | false |

Locked branch versus baselines:

| Reference | Delta chi2 | Delta AIC | Delta BIC |
|---|---:|---:|---:|
| `LCDM` | -3.6187583484 | -3.6187583484 | -3.6187583484 |
| `wCDM` | -0.3814237017 | -2.3814237017 | -7.7814332188 |
| `CPL` | +0.3825368599 | -3.6174631401 | -14.4174821744 |

So the release split does not collapse the locked branch.

The DR1 score is weaker than DR2 versus `LCDM`, but it remains:

```text
edge-clean,
same-k better than LCDM,
AIC/BIC better than wCDM/CPL,
zero-memory control equal to LCDM.
```

## Amplitude Proximity Check

The fitted-amplitude diagnostic lands very close to the locked value:

| Release | locked `2/27` | fitted `B_mem` | absolute shift | relative shift |
|---|---:|---:|---:|---:|
| DR2 | 0.0740740741 | 0.0745331916 | +0.0004591175 | +0.62% |
| DR1 | 0.0740740741 | 0.0734184619 | -0.0006556122 | -0.89% |

This is one of the cleaner internal signals so far:

```text
the data-preferred free amplitude is not wandering somewhere arbitrary;
it hugs the trace/projector value.
```

But it still does not prove the parent derivation of `2/27`.

The honest status is:

```text
2/27 has empirical traction in this background wrapper,
but remains an empirical closure/theorem target until the parent action supplies the normalization.
```

## What This Improves

This checkpoint improves the programme in four ways:

1. It removes the branch-name ambiguity.
2. It gives the locked no-clock branch its proper AIC/BIC treatment.
3. It confirms the zero-memory branch reproduces `LCDM`.
4. It shows the fitted-amplitude diagnostic independently lands within about one percent of `2/27`.

That is not a full theory win.

It is a strong discipline win.

## What It Does Not Decide

This checkpoint does not derive:

```text
B_mem = 2/27,
Hstar = H0,
the CMB bridge,
MTS perturbation equations,
local GR,
PPN suppression,
the parent action.
```

It also does not justify a public claim such as:

```text
MTS beats LCDM,
MTS passes official cosmology,
MTS derives GR,
MTS replaces dark energy.
```

The correct public-facing ceiling remains:

```text
a locked one-parameter-equivalent background closure has survived a fair no-SH0ES SN+BAO release split,
with no prior-edge flags and with the fitted-amplitude diagnostic close to the locked value.
```

Even that sentence should stay private until the wrapper is independently reviewed.

## Next Derivation Target

The data now points back at the maths.

The most valuable next derivation is not another fitted cosmology variant. It is:

```text
derive the normalization contract that makes Tr(P_active)/27 = 2/27 unavoidable,
or prove exactly which parent-action assumption must be added as closure.
```

In practical terms:

```text
start from the radial-memory parent-action contract,
keep the cubic hazard already conditionally derived,
write the minimal amplitude-normalization theorem,
force every free normalization constant to be named,
and reject any route that only renames B_mem.
```

If that fails, `B_mem=2/27` remains a very interesting empirical closure.

If it succeeds, the programme has a real spine: a conditional field-theory route that predicts the late-time background amplitude before seeing the data.
