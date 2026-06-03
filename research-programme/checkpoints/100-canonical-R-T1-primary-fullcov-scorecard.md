# 100 — Canonical R Closure T1 Primary Full-Covariance Scorecard

## Verdict

`T1_clean_points_survival_not_promotion`.

The canonical closure branch survived the primary no-SH0ES, full-sample, full-covariance DESI DR2 scorecard cleanly. It converged, did not hit prior edges, beat or drew the flexible baselines on information criteria in the places that matter, and showed a nonzero memory-amplitude improvement over the zero-memory control.

This is not a knockout and not a field-theory promotion. It is a clean empirical closure result: competitive, non-edge, and worth the next robustness round.

## Authoritative runs

Strict score run:

`runs/20260531-141154-cosmo-SN-BAO-short-smoke`

Scorecard ledger:

`runs/20260531-141359-canonical-R-T1-scorecard`

The earlier run at `runs/20260531-141013-cosmo-SN-BAO-short-smoke` produced the same numerical fit, but the runner was then tightened so the score-run schema explicitly records covariance artifacts. The authoritative run is therefore `20260531-141154`.

## Branch configuration

| Setting | Value |
|---|---:|
| SN observable | `mb-corr` |
| SN covariance | `full` |
| SN rows used | 1624 |
| BAO rows used | 13 |
| BAO branch | `DESI_DR2_primary` |
| Calibrators | excluded |
| MTS branch | `MTS_fixed_p3_u3quarter` as `canonical_R_closure` |
| Claim ceiling | `empirical_closure_scorecard_only` |

The score-run data schema records valid SN shape, SN covariance, DESI DR2 BAO mean, and DESI DR2 BAO covariance artifacts.

## Fit table

| Model | χ² total | AIC | BIC | k | Converged | Edge flag |
|---|---:|---:|---:|---:|---|---|
| LCDM | 1470.527873 | 1476.527873 | 1492.729734 | 3 | True | False |
| wCDM | 1465.437415 | 1473.437415 | 1495.039897 | 4 | True | False |
| CPL | 1465.100678 | 1475.100678 | 1502.103781 | 5 | True | False |
| canonical_R_closure | 1465.268214 | 1473.268214 | 1494.870696 | 4 | True | False |
| MTS_Bmem_zero | 1470.527873 | 1476.527873 | 1492.729734 | 3 | True | False |

## Judge card

| Reference | Δχ² | ΔAIC | ΔBIC | Round |
|---|---:|---:|---:|---|
| LCDM | -5.259659 | -3.259659 | +2.140962 | split points win, not BIC promotion |
| wCDM | -0.169201 | -0.169201 | -0.169201 | razor-thin points win |
| CPL | +0.167536 | -1.832464 | -7.233085 | parsimony points win |
| MTS_Bmem_zero | -5.259659 | -3.259659 | +2.140962 | nonzero memory signal, not BIC decisive |

Boxing translation: this is a Mayweather-style round, not a Tyson round. MTS does not smash the baselines, but it slips the flexible CPL haymaker by losing raw χ² by only `0.168` while winning AIC/BIC, edges wCDM on equal parameter count, and improves over LCDM/zero-memory in χ²/AIC. LCDM still gets a weak BIC card because it is simpler.

## Amplitude readout

| Quantity | Value | Status |
|---|---:|---|
| `B_mem` | 0.0745331916 | fitted closure amplitude |
| conditional `DeltaR = 3 B_mem` | 0.2235995748 | translation only under `eta=1`, `a_F=1` |
| χ² gain vs zero memory | -5.2596586716 | empirical fit gain |

This is useful because the memory term is doing work: `B_mem=0` collapses to the LCDM score, while the fitted canonical closure gains about `5.26` in χ². But the amplitude is still fitted, so the parent-action debt remains.

## Gate outcomes

All T1 gates passed:

- scores written with no failures;
- primary full-covariance branch confirmed;
- covariance artifacts recorded in the score-run schema;
- LCDM, wCDM, CPL, canonical closure, and zero-memory control converged;
- no prior-edge flags;
- zero-memory control present;
- claim ceiling enforced.

## Interpretation

The result keeps the branch alive in the exact way we wanted: not by pretending it has already beaten cosmology, but by showing that the canonical closure can stand in the ring with fitted dark-energy baselines on the clean no-SH0ES branch.

The strongest statement allowed is:

> The current canonical-R closure is an edge-free empirical closure contender on the primary SN+BAO background scorecard.

The forbidden statement remains:

> The parent field theory predicts the observed cosmological amplitude.

## Next target

Run `T2_clean_primary_with_ablations`: same no-SH0ES, full-sample, full-covariance DESI DR2 branch, but include `MTS_fitted_p` and `MTS_fitted_u3`.

Suggested command:

```powershell
& "research-programme\.venv-score\Scripts\python.exe" "research-programme\scripts\cosmo_SN_BAO_closure_runner.py" --phase short-smoke --sn-observable mb-corr --sn-covariance-mode full --sn-max-rows 0 --bao-label DESI_DR2_primary --sn-data "[local-formalization-workbench]\data\cosmology\pantheon_plus\Pantheon+SH0ES.dat" --sn-cov "[local-formalization-workbench]\data\cosmology\pantheon_plus\Pantheon+SH0ES_STAT+SYS.cov" --bao-data "[local-formalization-workbench]\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_mean.txt" --bao-cov "[local-formalization-workbench]\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_cov.txt" --include-mts-ablations --max-iter 120
```

Decision logic for T2:

- If fitted `p` or fitted `u3` hits a prior edge, that branch is diagnostic only.
- If fitted `p/u3` hugely improves the score, the fixed canonical shape is probably under-derived or too rigid.
- If fitted `p/u3` does not materially improve the score, the fixed canonical branch gains credibility as a disciplined closure.
- If the zero-memory control remains equivalent to LCDM and worse in χ²/AIC, the memory term continues to carry empirical signal.
