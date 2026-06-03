# 102 — Canonical R Closure T3 Diagonal-Covariance Sensitivity

## Verdict

`T3_diagonal_preserves_or_strengthens_pattern`.

The diagonal SN-covariance diagnostic does not reverse the primary full-covariance scorecard. It actually strengthens the apparent MTS round against LCDM, wCDM, and CPL. This is a useful robustness point, but it does not replace the full-covariance result as the primary evidence card.

Full covariance remains the official scorecard. Diagonal covariance is diagnostic only.

## Authoritative runs

Primary full-covariance reference:

`runs/20260531-141154-cosmo-SN-BAO-short-smoke`

T3 diagonal score run:

`runs/20260531-142133-cosmo-SN-BAO-short-smoke`

T3 covariance ledger:

`runs/20260531-142400-canonical-R-T3-covariance-scorecard`

## Branch configuration

| Setting | Value |
|---|---:|
| SN observable | `mb-corr` |
| SN covariance | `diagonal` |
| SN rows used | 1624 |
| BAO rows used | 13 |
| BAO branch | `DESI_DR2_primary` |
| Calibrators | excluded |
| MTS ablations included | False |
| Claim ceiling | `empirical_closure_scorecard_only` |

The diagonal run uses the same no-SH0ES SN shape branch and DESI DR2 BAO branch as the primary run. Absolute `chi2` values are not directly comparable between full and diagonal covariance because the weighting changed; the meaningful diagnostic is the relative pattern against the same baselines inside each branch.

## Diagonal fit table

| Model | chi2 total | AIC | BIC | k | Converged | Edge flag |
|---|---:|---:|---:|---:|---|---|
| LCDM | 739.860627 | 745.860627 | 762.062489 | 3 | True | False |
| wCDM | 732.724204 | 740.724204 | 762.326686 | 4 | True | False |
| CPL | 732.354487 | 742.354487 | 769.357590 | 5 | True | False |
| canonical_R_closure | 731.415740 | 739.415740 | 761.018223 | 4 | True | False |
| MTS_Bmem_zero | 739.860627 | 745.860627 | 762.062489 | 3 | True | False |

## Full-vs-diagonal judge card

| Reference | Full delta chi2 | Full delta AIC | Full delta BIC | Diagonal delta chi2 | Diagonal delta AIC | Diagonal delta BIC | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| LCDM | -5.259659 | -3.259659 | +2.140962 | -8.444887 | -6.444887 | -1.044266 | diagonal strengthens LCDM round |
| wCDM | -0.169201 | -0.169201 | -0.169201 | -1.308464 | -1.308464 | -1.308464 | diagonal preserves equal-parameter win |
| CPL | +0.167536 | -1.832464 | -7.233085 | -0.938747 | -2.938747 | -8.339368 | diagonal strengthens CPL round |

Boxing translation: this is not the result of a fragile fighter who only wins under one referee. Under diagonal covariance, MTS does better on the cards. But because diagonal covariance is a weaker treatment of the data covariance, it is a sparring-room confidence boost, not the title-fight scorecard.

## Amplitude sensitivity

| Quantity | Full covariance | Diagonal covariance | Shift | Relative shift | Verdict |
|---|---:|---:|---:|---:|---|
| `B_mem` | 0.074533 | 0.098134 | +0.023601 | +0.316653 | same order, moderate movement |
| conditional `DeltaR = 3 B_mem` | 0.223600 | 0.294403 | +0.070803 | +0.316653 | translation only |

The fitted memory amplitude moves by about `31.7%`, so the amplitude is somewhat covariance-sensitive. That does not kill the branch because the scorecard pattern survives, but it reinforces the existing rule: amplitude language must remain closure-only until derived from the parent action.

## Gate outcomes

All T3 gates passed:

- full-covariance reference exists and has scores;
- diagonal scores written with no failures;
- diagonal branch confirmed as no-SH0ES `mb-corr`, DESI DR2, full sample;
- required models converged;
- no diagonal prior-edge flags;
- qualitative scorecard not reversed;
- full covariance remains primary.

## Interpretation

The robust reading is:

> The primary full-covariance MTS result is not an artifact of requiring full covariance. A diagonal diagnostic preserves or strengthens the relative scorecard, while moving the fitted amplitude by a moderate but same-order amount.

The forbidden reading remains:

> Diagonal covariance proves the cosmology branch.

It does not. It is one robustness check, and full covariance remains the serious card.

## Next target

Run `T4_small_sample_reproduction`: reproduce the older small-sample behavior on the current cleaned runner. This is not decisive evidence; it checks whether older smoke-fit behavior was pipeline/sample-size driven.

Suggested command:

```powershell
& "research-programme\.venv-score\Scripts\python.exe" "research-programme\scripts\cosmo_SN_BAO_closure_runner.py" --phase short-smoke --sn-observable mb-corr --sn-covariance-mode full --sn-max-rows 250 --bao-label DESI_DR2_primary --sn-data "[local-formalization-workbench]\data\cosmology\pantheon_plus\Pantheon+SH0ES.dat" --sn-cov "[local-formalization-workbench]\data\cosmology\pantheon_plus\Pantheon+SH0ES_STAT+SYS.cov" --bao-data "[local-formalization-workbench]\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_mean.txt" --bao-cov "[local-formalization-workbench]\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_cov.txt" --include-mts-ablations --max-iter 120
```

Decision logic for T4:

- If small-sample behavior differs sharply from full-sample behavior, treat older small-sample hits/misses as diagnostic only.
- If edge flags return only in the small sample, do not weaken the full-sample result; mark the small branch unstable.
- If the broad pattern survives even in small sample, that is a minor robustness point, not a promotion.
