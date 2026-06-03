# 104 — Canonical R Closure T5 SH0ES-Pressure Branch

## Verdict

`T5_SH0ES_pressure_neutral_stress_only`.

The SH0ES-pressure branch is not a special MTS boost. When compared against a matched no-SH0ES control with the same 250 SN rows, diagonal covariance, DESI DR2 BAO data, and MTS ablations, the relative scorecard is essentially unchanged.

This is useful because it prevents overclaiming: the pressure branch changes the lighting, not the fight. It remains a stress test only.

## Authoritative runs

SH0ES-pressure run:

`runs/20260531-143143-cosmo-SN-BAO-short-smoke`

Matched no-SH0ES diagonal control:

`runs/20260531-143247-cosmo-SN-BAO-short-smoke`

T5 pressure ledger:

`runs/20260531-143518-canonical-R-T5-SH0ES-pressure-scorecard`

## Why a matched control was added

The planned T5 command changed both the SN observable and covariance/sample treatment relative to the primary full-covariance branch. To avoid fooling ourselves, a matched no-SH0ES control was run with:

- the same `250` SN rows;
- the same diagonal SN covariance treatment;
- the same DESI DR2 BAO data;
- the same ablation set;
- `mb-corr` instead of `mu-sh0es`.

That isolates whether `mu-sh0es` pressure changes the relative behavior.

## Branch configuration

| Setting | SH0ES pressure | Matched control |
|---|---:|---:|
| SN observable | `mu-sh0es` | `mb-corr` |
| SN covariance | `diagonal` | `diagonal` |
| SN rows used | 250 | 250 |
| BAO rows used | 13 | 13 |
| BAO branch | `DESI_DR2_primary` | `DESI_DR2_primary` |
| MTS ablations included | True | True |
| Claim ceiling | stress only | stress only |

## Pressure fit table

| Model | chi2 total | AIC | BIC | k | Converged | Edge flag |
|---|---:|---:|---:|---:|---|---|
| LCDM | 130.308367 | 136.308367 | 147.024829 | 3 | True | False |
| wCDM | 129.091212 | 137.091212 | 151.379828 | 4 | True | False |
| CPL | 126.017145 | 136.017145 | 153.877915 | 5 | True | True |
| canonical_R_closure | 127.662755 | 135.662755 | 149.951372 | 4 | True | False |
| MTS_Bmem_zero | 130.308367 | 136.308367 | 147.024829 | 3 | True | False |
| MTS_fitted_p | 127.646523 | 137.646523 | 155.507293 | 5 | True | False |
| MTS_fitted_u3 | 127.415906 | 137.415906 | 155.276677 | 5 | True | False |

## Edge flags

| Branch | Model | Parameter | Best fit | Meaning |
|---|---|---|---:|---|
| matched no-SH0ES control | CPL | `wa` | -2.000000 | baseline edge hit |
| SH0ES pressure | CPL | `wa` | -2.000000 | baseline edge hit |

The instability is symmetric and baseline-side. The fixed MTS branch and its fitted-`p/u3` ablations are edge-free in the pressure branch.

## Fixed-branch pressure comparison

| Reference | Control delta chi2 | Control delta AIC | Control delta BIC | Pressure delta chi2 | Pressure delta AIC | Pressure delta BIC | Max shift |
|---|---:|---:|---:|---:|---:|---:|---:|
| LCDM | -2.645644 | -0.645644 | +2.926510 | -2.645612 | -0.645612 | +2.926542 | 0.000032 |
| wCDM | -1.428363 | -1.428363 | -1.428363 | -1.428456 | -1.428456 | -1.428456 | 0.000093 |
| CPL | +1.646213 | -0.353787 | -3.925941 | +1.645610 | -0.354390 | -3.926544 | 0.000603 |

The relative scorecard is effectively unchanged. So the SH0ES-pressure branch does not create an MTS-specific advantage.

## Ablations under pressure

| Ablation | Delta chi2 vs fixed | Delta AIC vs fixed | Delta BIC vs fixed | Verdict |
|---|---:|---:|---:|---|
| MTS_fitted_p | -0.016233 | +1.983767 | +5.555921 | fixed branch wins IC |
| MTS_fitted_u3 | -0.246849 | +1.753151 | +5.325305 | fixed branch wins IC |

Even under pressure, fitted `p/u3` do not displace the fixed canonical branch. They buy small raw-chi2 movement and lose information criteria.

## Amplitude pressure shift

| Model | Control `B_mem` | Pressure `B_mem` | Relative shift | Edge flag |
|---|---:|---:|---:|---|
| canonical_R_closure | 0.138741 | 0.138740 | -0.000006 | False |
| MTS_fitted_p | 0.145822 | 0.145816 | -0.000047 | False |
| MTS_fitted_u3 | 0.316843 | 0.316316 | -0.001664 | False |

The amplitude barely changes between the matched control and SH0ES-pressure branch. This is another sign that T5 is not revealing a new MTS-specific pressure response.

## Gate outcomes

All T5 gates passed:

- matched no-SH0ES control scores were written;
- SH0ES-pressure scores were written;
- the branch pair is matched except for SN observable;
- pressure edge flags are baseline-only (`CPL:wa`);
- relative MTS scorecard is nearly unchanged by `mu-sh0es`;
- fitted ablations still lose AIC/BIC against fixed canonical branch;
- stress branch remains blocked from evidence language.

## Interpretation

The fair reading is:

> SH0ES-pressure does not add special support for MTS. The fixed branch stays edge-free and competitive, but the only edge flag is a symmetric CPL baseline edge. The branch is stress-only.

The forbidden reading is:

> MTS improves under SH0ES pressure, therefore this supports the theory.

It does not. This round is useful because it stops us mistaking local-H0 pressure behavior for genuine theory evidence.

Boxing translation: SH0ES changed the arena lights, not the scorecards. MTS did not get hurt, but it also did not win a special belt.

## Next target

Run `T6_BAO_release_sensitivity`: repeat the cleaned branch with the DR1 BAO release to see whether the result is sensitive to BAO release choice.

Suggested command:

```powershell
& "research-programme\.venv-score\Scripts\python.exe" "research-programme\scripts\cosmo_SN_BAO_closure_runner.py" --phase short-smoke --sn-observable mb-corr --sn-covariance-mode full --sn-max-rows 250 --bao-label DESI_DR1_primary --sn-data "[local-formalization-workbench]\data\cosmology\pantheon_plus\Pantheon+SH0ES.dat" --sn-cov "[local-formalization-workbench]\data\cosmology\pantheon_plus\Pantheon+SH0ES_STAT+SYS.cov" --bao-data "[local-formalization-workbench]\data\cosmology\desi_dr1_bao\desi_2024_gaussian_bao_ALL_GCcomb_mean.txt" --bao-cov "[local-formalization-workbench]\data\cosmology\desi_dr1_bao\desi_2024_gaussian_bao_ALL_GCcomb_cov.txt" --include-mts-ablations --max-iter 120
```

Decision logic for T6:

- If DR1 reverses the scorecard, mark BAO-release sensitivity and do not cherry-pick DR2.
- If DR1 is weaker but directionally similar, mark it as a robustness warning.
- If DR1 also preserves the pattern, record a BAO-release robustness point.
