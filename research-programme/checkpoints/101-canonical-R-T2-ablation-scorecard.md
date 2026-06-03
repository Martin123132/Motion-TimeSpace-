# 101 — Canonical R Closure T2 Ablation Scorecard

## Verdict

`T2_fixed_shape_survives_ablation`.

The fitted-`p` and fitted-`u3` ablations both converged and did not hit prior edges. They do improve raw `chi2` slightly, but the improvement is too small to pay for the extra parameter under AIC/BIC. That is exactly the result the fixed canonical branch needed: the extra freedom lands light scoring taps, but it does not rescue or overthrow the fixed shape.

This still remains an empirical closure result, not a field-theory proof.

## Authoritative runs

T2 score run:

`runs/20260531-141635-cosmo-SN-BAO-short-smoke`

T2 ablation ledger:

`runs/20260531-141851-canonical-R-T2-ablation-scorecard`

## Branch configuration

| Setting | Value |
|---|---:|
| SN observable | `mb-corr` |
| SN covariance | `full` |
| SN rows used | 1624 |
| BAO rows used | 13 |
| BAO branch | `DESI_DR2_primary` |
| Calibrators | excluded |
| MTS ablations included | True |
| Claim ceiling | `empirical_closure_scorecard_only` |

The score-run schema records valid SN shape, SN covariance, DESI DR2 BAO mean, and DESI DR2 BAO covariance artifacts.

## Fit table

| Model | chi2 total | AIC | BIC | k | Converged | Edge flag |
|---|---:|---:|---:|---:|---|---|
| LCDM | 1470.527873 | 1476.527873 | 1492.729734 | 3 | True | False |
| wCDM | 1465.437415 | 1473.437415 | 1495.039897 | 4 | True | False |
| CPL | 1465.100678 | 1475.100678 | 1502.103781 | 5 | True | False |
| canonical_R_closure | 1465.268214 | 1473.268214 | 1494.870696 | 4 | True | False |
| MTS_Bmem_zero | 1470.527873 | 1476.527873 | 1492.729734 | 3 | True | False |
| MTS_fitted_p | 1465.227806 | 1475.227806 | 1502.230908 | 5 | True | False |
| MTS_fitted_u3 | 1464.417798 | 1474.417798 | 1501.420901 | 5 | True | False |

## Ablation against fixed canonical branch

| Ablation | Free parameter | Delta chi2 | Delta AIC | Delta BIC | Edge flag | Verdict |
|---|---|---:|---:|---:|---|---|
| MTS_fitted_p | `p` | -0.040408 | +1.959592 | +7.360212 | False | raw chi2 nudge, fixed branch wins IC |
| MTS_fitted_u3 | `u3` | -0.850416 | +1.149584 | +6.550205 | False | raw chi2 nudge, fixed branch wins IC |

Boxing translation: the ablations touch the fixed branch, but they do not rock it. Free `p` barely changes the round. Free `u3` throws the better shot, but the judge takes the extra-parameter tax and still gives the disciplined fixed closure the cleaner card.

## Parameter movement

| Model | Parameter | Best fit | Shift from canonical | Status |
|---|---|---:|---:|---|
| canonical_R_closure | `p` | 3.000000 | 0.000000 | fixed canonical |
| canonical_R_closure | `u3` | 0.250000 | 0.000000 | fixed canonical |
| MTS_fitted_p | `p` | 2.172371 | -0.827629 | ablation only |
| MTS_fitted_u3 | `u3` | 0.327116 | +0.077116 | ablation only |
| canonical_R_closure | `B_mem` | 0.074533 | — | fitted closure amplitude |
| MTS_fitted_p | `B_mem` | 0.074414 | — | fitted closure amplitude |
| MTS_fitted_u3 | `B_mem` | 0.107509 | — | fitted closure amplitude |

The `p` ablation drifting to `2.17` is a theory note, but it buys almost nothing in fit quality. The `u3` ablation drifting from `0.25` to `0.327` buys a modest `chi2` improvement, but not enough to beat the fixed branch after information criteria.

## Baseline reading

The fixed canonical branch remains the cleaner closure branch:

- Against `wCDM`, fixed canonical remains slightly ahead on equal parameter count: Delta `chi2/AIC/BIC = -0.169201`.
- Against `CPL`, fixed canonical loses raw `chi2` by only `+0.167536` but wins AIC by `-1.832464` and BIC by `-7.233085`.
- `MTS_fitted_p` is not useful as a promoted branch: it barely improves raw `chi2` and loses AIC/BIC to fixed canonical.
- `MTS_fitted_u3` is the interesting diagnostic: it beats CPL by `-0.682880` on equal parameter count, but as an ablation it does not displace the fixed branch because fixed canonical is still better on AIC/BIC.

## Gate outcomes

All T2 gates passed:

- scores written with no failures;
- branch confirmed as full-covariance ablation run;
- covariance artifacts recorded and valid;
- all required models converged;
- all fitted parameters edge-free;
- fixed shape not rescued by extra parameter;
- claim ceiling enforced.

## Interpretation

This is a meaningful support result for the current closure discipline. If freeing `p` or `u3` had smashed the fixed branch, we would have had to admit the canonical choices were just constraining the fit badly. That did not happen.

The strongest allowed statement is:

> The fixed canonical-R closure shape survives the first full-covariance ablation test: fitted `p/u3` improve raw `chi2` only mildly and lose AIC/BIC against the fixed branch.

The forbidden statement remains:

> `p=3` and `u3=1/4` are now derived from the parent theory.

## Next target

Run `T3_diagonal_covariance_sensitivity`: same no-SH0ES DESI DR2 branch, but switch SN covariance to diagonal. This does not outrank the full-covariance result; it tests whether the signal is fragile to covariance handling.

Suggested command:

```powershell
& "research-programme\.venv-score\Scripts\python.exe" "research-programme\scripts\cosmo_SN_BAO_closure_runner.py" --phase short-smoke --sn-observable mb-corr --sn-covariance-mode diagonal --sn-max-rows 0 --bao-label DESI_DR2_primary --sn-data "[local-formalization-workbench]\data\cosmology\pantheon_plus\Pantheon+SH0ES.dat" --bao-data "[local-formalization-workbench]\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_mean.txt" --bao-cov "[local-formalization-workbench]\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_cov.txt" --max-iter 120
```

Decision logic for T3:

- If diagonal covariance reverses the qualitative scorecard, mark the signal covariance-sensitive.
- If diagonal covariance preserves the broad pattern, treat the result as a robustness point, but keep full covariance primary.
- If diagonal covariance introduces edge hits, treat it as diagnostic only and do not use it for promotion.
