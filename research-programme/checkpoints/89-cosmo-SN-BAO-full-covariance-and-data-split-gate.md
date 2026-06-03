# 89 - Cosmology SN+BAO Full-Covariance and Data-Split Gate

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 88 found:

```text
CPL boundary-running persists in the 250-row diagonal/SH0ES-shaped smoke;
MTS_fixed_p3_u3quarter is numerically stable and non-edge;
stable_evidence_allowed = false.
```

This checkpoint upgrades the test discipline before interpreting the signal.

## 2. Short Verdict

```text
covariance_split_gate_status =
implemented_and_first_runs_complete
```

```text
stable_evidence_allowed =
false
```

Plain English:

```text
The no-SH0ES/full-covariance branch is now runnable. The fixed-MTS branch remains sane, but preference language is still blocked because the result changes with covariance/sample choices and the ablation branch can edge-hit.
```

## 3. Runner Changes

Extended:

```text
research-programme\scripts\cosmo_SN_BAO_closure_runner.py
```

with:

- `--sn-covariance-mode diagonal|full`;
- `--sn-cov` for Pantheon+ covariance files;
- `--sn-observable mu-sh0es|mb-corr`;
- `--include-calibrators` off by default;
- `--bao-label` for DR1/DR2 residual labeling;
- `--sn-max-rows 0` meaning the full selected SN sample;
- full covariance analytic-offset chi2 using the sliced Pantheon+ covariance matrix.

The no-SH0ES branch uses:

```text
--sn-observable mb-corr
```

with a free analytic offset, so the absolute calibration is not treated as local-H0 evidence.

## 4. Data Used

SN table:

```text
[local-formalization-workbench]\data\cosmology\pantheon_plus\Pantheon+SH0ES.dat
```

SN full covariance:

```text
[local-formalization-workbench]\data\cosmology\pantheon_plus\Pantheon+SH0ES_STAT+SYS.cov
```

DR2 BAO:

```text
[local-formalization-workbench]\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_mean.txt
```

DR1 BAO:

```text
[local-formalization-workbench]\data\cosmology\desi_dr1_bao\desi_2024_gaussian_bao_ALL_GCcomb_mean.txt
```

## 5. Runs

| Run | SN branch | BAO split | SN rows | Models | Status |
|---|---|---|---:|---|---|
| `20260531-125701-cosmo-SN-BAO-short-smoke` | `mb-corr`, full cov | DR2 | 250 | baselines + MTS ablations | unstable edge flags |
| `20260531-125724-cosmo-SN-BAO-short-smoke` | `mb-corr`, full cov | DR1 | 250 | baselines + MTS ablations | unstable edge flags |
| `20260531-125813-cosmo-SN-BAO-short-smoke` | `mb-corr`, diagonal | DR2 | 1624 | required models | no edge flags |
| `20260531-125832-cosmo-SN-BAO-short-smoke` | `mb-corr`, full cov | DR2 | 1624 | required models | no edge flags |

The 1624-row count is the non-calibrator selected Pantheon+ sample.

## 6. Full-Covariance 250-Row DR2 Readout

| Model | chi2 | AIC | BIC | Edge flag |
|---|---:|---:|---:|---:|
| `LCDM` | 247.248472 | 253.248472 | 263.964934 | no |
| `wCDM` | 245.989136 | 253.989136 | 268.277752 | no |
| `CPL` | 242.674074 | 252.674074 | 270.534844 | yes |
| `MTS_fixed_p3_u3quarter` | 244.593480 | 252.593480 | 266.882096 | no |
| `MTS_fitted_p` | 244.573739 | 254.573739 | 272.434510 | no |
| `MTS_fitted_u3` | 243.919935 | 253.919935 | 271.780705 | yes |

Edge flags:

```text
CPL: wa = -2.0
MTS_fitted_u3: B_mem near upper edge and u3 = 0.05
```

The fixed branch stays non-edge; the fitted-u3 ablation is not stable.

## 7. DR1 Split Readout

With the same 250-row full-covariance/no-SH0ES SN branch:

| Model | chi2 | AIC | BIC | Edge flag |
|---|---:|---:|---:|---:|
| `LCDM` | 249.719883 | 255.719883 | 266.424916 | no |
| `wCDM` | 249.674712 | 257.674712 | 271.948090 | no |
| `CPL` | 246.795454 | 256.795454 | 274.637176 | yes |
| `MTS_fixed_p3_u3quarter` | 248.582979 | 256.582979 | 270.856357 | no |
| `MTS_fitted_p` | 248.547546 | 258.547546 | 276.389268 | no |
| `MTS_fitted_u3` | 248.020846 | 258.020846 | 275.862569 | yes |

DR1 weakens the fixed-MTS comparison against `LCDM` by AIC/BIC. This is exactly why split tests matter.

## 8. Full-Sample Readout

Diagonal full-sample/no-SH0ES DR2:

| Model | chi2 | AIC | BIC | Edge flag |
|---|---:|---:|---:|---:|
| `LCDM` | 739.860627 | 745.860627 | 762.062489 | no |
| `wCDM` | 732.724204 | 740.724204 | 762.326686 | no |
| `CPL` | 732.354487 | 742.354487 | 769.357590 | no |
| `MTS_fixed_p3_u3quarter` | 731.415740 | 739.415740 | 761.018223 | no |

Full-covariance full-sample/no-SH0ES DR2:

| Model | chi2 | AIC | BIC | Edge flag |
|---|---:|---:|---:|---:|
| `LCDM` | 1470.527873 | 1476.527873 | 1492.729734 | no |
| `wCDM` | 1465.437415 | 1473.437415 | 1495.039897 | no |
| `CPL` | 1465.100678 | 1475.100678 | 1502.103781 | no |
| `MTS_fixed_p3_u3quarter` | 1465.268214 | 1473.268214 | 1494.870696 | no |

This is the first cleaner full-sample branch. It still does not prove preference: MTS is slightly worse than CPL in chi2, slightly better than CPL in AIC/BIC due to one fewer fitted parameter, and not decisively separated from `wCDM`.

## 9. Interpretation Gate

Allowed statement:

```text
The fixed-MTS background closure survives no-SH0ES/full-covariance execution and remains non-edge in the tested full-sample branch.
```

Forbidden statement:

```text
MTS is cosmologically preferred.
```

Reason:

```text
The 250-row ablation branch can edge-hit, DR1/DR2 shifts the comparison, and the full-sample full-covariance branch is close to wCDM/CPL rather than decisive.
```

## 10. What Improved

The previous cosmology smoke was too easy to dismiss because it used diagonal SN uncertainty and SH0ES-shaped distance moduli.

Now the pipeline can test:

```text
Pantheon+ shape-only/no-SH0ES observable;
Pantheon+ full covariance;
DESI DR1 vs DR2 split;
full selected SN sample;
fixed and ablated MTS branches.
```

That is a real step toward serious empirical discipline.

## 11. Next Target

Create:

```text
90-cosmo-model-selection-stability-ledger.md
```

with a compact stability ledger across all cosmology branches:

1. rank models by chi2, AIC, and BIC for each run;
2. flag whether the best-ranked model is edge-free;
3. identify whether MTS advantage is covariance-dependent, split-dependent, or sample-size-dependent;
4. decide whether the next physics work should be amplitude derivation, perturbation/CMB consistency, or wider cosmology robustness.

Acceptance:

```text
No branch is promoted unless it is edge-free, beats LCDM/wCDM/CPL under the same data/covariance/split rules, and has a derivation route for any fitted closure amplitude.
```
