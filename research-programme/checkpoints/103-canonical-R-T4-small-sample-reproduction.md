# 103 — Canonical R Closure T4 Small-Sample Reproduction

## Verdict

`T4_reproduces_small_sample_instability_but_fixed_pattern_survives`.

The cleaned runner reproduces the old small-sample warning: with only 250 SN rows, prior-edge flags come back. Crucially, those edge flags are not in the fixed canonical branch. They occur in `CPL` and the fitted-`u3` ablation.

So the small-sample branch is messy and diagnostic only. It does not weaken the full-sample primary result, but it explains why older small smoke fits were dangerous to over-read.

## Authoritative runs

Full-sample ablation reference:

`runs/20260531-141635-cosmo-SN-BAO-short-smoke`

T4 small-sample score run:

`runs/20260531-142622-cosmo-SN-BAO-short-smoke`

T4 small-sample ledger:

`runs/20260531-142827-canonical-R-T4-small-sample-scorecard`

## Branch configuration

| Setting | Value |
|---|---:|
| SN observable | `mb-corr` |
| SN covariance | `full` |
| SN rows used | 250 |
| BAO rows used | 13 |
| BAO branch | `DESI_DR2_primary` |
| Calibrators | excluded |
| MTS ablations included | True |
| Claim ceiling | `diagnostic_only_no_stable_evidence` |

## Small-sample fit table

| Model | chi2 total | AIC | BIC | k | Converged | Edge flag |
|---|---:|---:|---:|---:|---|---|
| LCDM | 247.248472 | 253.248472 | 263.964934 | 3 | True | False |
| wCDM | 245.989136 | 253.989136 | 268.277752 | 4 | True | False |
| CPL | 242.674074 | 252.674074 | 270.534844 | 5 | True | True |
| canonical_R_closure | 244.593480 | 252.593480 | 266.882096 | 4 | True | False |
| MTS_Bmem_zero | 247.248472 | 253.248472 | 263.964934 | 3 | True | False |
| MTS_fitted_p | 244.573739 | 254.573739 | 272.434510 | 5 | True | False |
| MTS_fitted_u3 | 243.919935 | 253.919935 | 271.780705 | 5 | True | True |

## Edge flags

| Model | Parameter | Best fit | Edge |
|---|---|---:|---|
| CPL | `wa` | -2.000000 | lower prior edge |
| MTS_fitted_u3 | `B_mem` | 0.987262 | near upper prior edge |
| MTS_fitted_u3 | `u3` | 0.050000 | lower prior edge |

This is the main T4 message. The small sample is unstable because flexible branches run to edges. That makes it bad evidence. It is still useful as a pipeline warning.

## Fixed-branch pattern

| Reference | Full delta chi2 | Full delta AIC | Full delta BIC | Small delta chi2 | Small delta AIC | Small delta BIC | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| LCDM | -5.259659 | -3.259659 | +2.140962 | -2.654992 | -0.654992 | +2.917162 | small preserves LCDM split round |
| wCDM | -0.169201 | -0.169201 | -0.169201 | -1.395657 | -1.395657 | -1.395657 | small preserves wCDM equal-parameter win |
| CPL | +0.167536 | -1.832464 | -7.233085 | +1.919406 | -0.080594 | -3.652748 | small preserves CPL parsimony round |

The fixed canonical branch broadly keeps the same qualitative pattern as the full-sample branch: split against LCDM, wins equal-parameter wCDM, and wins AIC/BIC against CPL while losing raw chi2.

## Amplitude sensitivity

| Model | Full `B_mem` | Small `B_mem` | Relative shift | Small edge flag |
|---|---:|---:|---:|---|
| canonical_R_closure | 0.074533 | 0.139015 | +0.865136 | False |
| MTS_fitted_p | 0.074414 | 0.147080 | +0.976516 | False |
| MTS_fitted_u3 | 0.107509 | 0.987262 | +8.183069 | True |

The fixed branch amplitude almost doubles in the small sample, even though it remains edge-free. That is another reason not to use this branch for amplitude claims. The fitted-`u3` branch is plainly unstable.

## Gate outcomes

All T4 diagnostic gates passed:

- full-sample reference exists;
- small-sample scores were written;
- small-sample branch is confirmed as 250 SN rows, full covariance, DESI DR2, with ablations;
- edge flags were reproduced;
- the fixed canonical branch itself remained edge-free;
- the broad fixed-branch pattern was preserved;
- stable-evidence language is blocked.

## Interpretation

The fair reading is:

> The old small-sample warning is real: flexible branches can edge-hit when the SN sample is cut to 250 rows. The fixed canonical branch still preserves the main qualitative pattern, but T4 is diagnostic only and cannot promote the theory.

The practical result is good discipline: we do not throw away the full-sample result because a deliberately weak branch is unstable, and we do not pretend the weak branch is evidence.

Boxing translation: this was an undercard with a dodgy canvas. MTS stayed upright, but nobody gets a title belt from it.

## Next target

Run `T5_SH0ES_pressure_branch`: a local-H0/calibrator pressure branch. This must be treated as a stress test, never as standalone support.

Suggested command:

```powershell
& "research-programme\.venv-score\Scripts\python.exe" "research-programme\scripts\cosmo_SN_BAO_closure_runner.py" --phase short-smoke --sn-observable mu-sh0es --sn-covariance-mode diagonal --sn-max-rows 250 --bao-label DESI_DR2_primary --sn-data "[local-formalization-workbench]\data\cosmology\pantheon_plus\Pantheon+SH0ES.dat" --bao-data "[local-formalization-workbench]\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_mean.txt" --bao-cov "[local-formalization-workbench]\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_cov.txt" --include-mts-ablations --max-iter 120
```

Decision logic for T5:

- If SH0ES-pressure improves MTS, label it stress behavior only.
- If SH0ES-pressure produces edge hits, mark it unstable and do not weaken the no-SH0ES primary branch.
- If baselines also edge-hit or behave badly, report that symmetrically.
