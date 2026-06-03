# 105 — Canonical R Closure T6 BAO-Release Sensitivity

## Verdict

`T6_DR1_weaker_release_warning_not_reversal`.

The DESI DR1 BAO release weakens the small-sample MTS scorecard, especially against LCDM, but it does not reverse the whole qualitative pattern. The fixed canonical branch remains edge-free, still beats `wCDM` on equal-parameter score, and still gets the parsimony card against `CPL`.

This is a real robustness warning: do not cherry-pick DR2 as if DR1 did not soften the result. But it is not a knockout against the branch.

## Authoritative runs

DESI DR2 reference:

`runs/20260531-142622-cosmo-SN-BAO-short-smoke`

DESI DR1 sensitivity run:

`runs/20260531-143908-cosmo-SN-BAO-short-smoke`

T6 BAO-release ledger:

`runs/20260531-144136-canonical-R-T6-BAO-release-scorecard`

## Branch configuration

| Setting | DR2 reference | DR1 sensitivity |
|---|---:|---:|
| SN observable | `mb-corr` | `mb-corr` |
| SN covariance | `full` | `full` |
| SN rows used | 250 | 250 |
| BAO rows used | 13 | 12 |
| BAO branch | `DESI_DR2_primary` | `DESI_DR1_primary` |
| MTS ablations included | True | True |
| Claim ceiling | diagnostic only | diagnostic only |

This branch is deliberately small-sample and unstable; it tests BAO-release sensitivity only. It does not outrank the full-sample DR2 primary scorecard.

## DR1 fit table

| Model | chi2 total | AIC | BIC | k | Converged | Edge flag |
|---|---:|---:|---:|---:|---|---|
| LCDM | 249.719883 | 255.719883 | 266.424916 | 3 | True | False |
| wCDM | 249.674712 | 257.674712 | 271.948090 | 4 | True | False |
| CPL | 246.795454 | 256.795454 | 274.637176 | 5 | True | True |
| canonical_R_closure | 248.582979 | 256.582979 | 270.856357 | 4 | True | False |
| MTS_Bmem_zero | 249.719883 | 255.719883 | 266.424916 | 3 | True | False |
| MTS_fitted_p | 248.547546 | 258.547546 | 276.389268 | 5 | True | False |
| MTS_fitted_u3 | 248.020846 | 258.020846 | 275.862569 | 5 | True | True |

## Edge flags

| Release | Model | Parameter | Best fit | Meaning |
|---|---|---|---:|---|
| DR2 | CPL | `wa` | -2.000000 | baseline edge hit |
| DR2 | MTS_fitted_u3 | `B_mem` | 0.987262 | ablation edge hit |
| DR2 | MTS_fitted_u3 | `u3` | 0.050000 | ablation edge hit |
| DR1 | CPL | `wa` | -2.000000 | baseline edge hit |
| DR1 | MTS_fitted_u3 | `B_mem` | 1.000000 | ablation edge hit |
| DR1 | MTS_fitted_u3 | `u3` | 0.050000 | ablation edge hit |

Both BAO-release branches are unstable because the small-sample flexible branches hit edges. The fixed canonical branch remains edge-free in both.

## Fixed-branch release card

| Reference | DR2 delta chi2 | DR2 delta AIC | DR2 delta BIC | DR1 delta chi2 | DR1 delta AIC | DR1 delta BIC | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| LCDM | -2.654992 | -0.654992 | +2.917162 | -1.136904 | +0.863096 | +4.431440 | DR1 weakens LCDM round |
| wCDM | -1.395657 | -1.395657 | -1.395657 | -1.091733 | -1.091733 | -1.091733 | DR1 preserves wCDM win |
| CPL | +1.919406 | -0.080594 | -3.652748 | +1.787525 | -0.212475 | -3.780820 | DR1 preserves CPL parsimony round |

The LCDM round is the warning. Under DR2, the fixed branch beats LCDM on chi2/AIC but loses BIC. Under DR1, it still beats LCDM on chi2, but loses both AIC and BIC. That is a meaningful softening.

## Memory signal by release

| Release | Fixed minus zero chi2 | Fixed minus zero AIC | Fixed minus zero BIC | Fixed edge flag |
|---|---:|---:|---:|---|
| DESI DR2 | -2.654992 | -0.654992 | +2.917162 | False |
| DESI DR1 | -1.136904 | +0.863096 | +4.431440 | False |

The nonzero memory term still improves raw chi2 over the zero-memory branch in DR1, but it no longer pays for its extra parameter on AIC/BIC in that small-sample DR1 branch.

## Amplitude release shift

| Model | DR2 `B_mem` | DR1 `B_mem` | Relative shift | Edge status |
|---|---:|---:|---:|---|
| canonical_R_closure | 0.139015 | 0.153378 | +0.103326 | edge-free |
| MTS_fitted_p | 0.147080 | 0.148652 | +0.010682 | edge-free |
| MTS_fitted_u3 | 0.987262 | 1.000000 | +0.012903 | edge-hit in both |

The fixed-branch amplitude moves only about `10%` from DR2 to DR1, so the amplitude itself is not the main DR1 problem. The issue is the weaker information-criterion score against LCDM.

## Ablations under DR1

| Ablation | Delta chi2 vs fixed | Delta AIC vs fixed | Delta BIC vs fixed | Verdict |
|---|---:|---:|---:|---|
| MTS_fitted_p | -0.035433 | +1.964567 | +5.532912 | fixed branch wins IC |
| MTS_fitted_u3 | -0.562133 | +1.437867 | +5.006212 | fixed branch wins IC |

Even under DR1, the fitted ablations do not displace the fixed canonical branch on AIC/BIC. The fitted-`u3` branch is also edge-hit, so it is diagnostic only.

## Gate outcomes

All T6 diagnostic gates passed:

- DR2 reference scores exist;
- DR1 scores were written;
- the release pair is matched except for BAO release;
- DR1 edge flags were reproduced;
- the fixed canonical branch is edge-free under DR1;
- no full scorecard reversal occurred;
- a BAO-release warning is explicitly recorded;
- fitted ablations do not displace the fixed branch by information criteria;
- DR1 remains diagnostic-only and blocked from stable-evidence language.

## Interpretation

The fair reading is:

> DR1 weakens the small-sample MTS result, especially against LCDM, but does not reverse the wCDM/CPL qualitative pattern. The branch is BAO-release sensitive enough that DR2 cannot be cherry-picked, yet not so sensitive that the whole closure collapses.

The forbidden reading is:

> DR2 is the good one, so ignore DR1.

No. DR1 is a warning label. The full-sample DR2 primary branch remains the best current scorecard, but future robustness must include release dependence and ideally full-sample DR1/DR2 comparisons where data shapes allow it.

Boxing translation: DR1 took some shine off the LCDM round. It did not knock MTS down, but it absolutely tells us not to swagger.

## Next target

Write a compact cosmology robustness summary and next theory gate, consolidating T1–T6 into a single decision document:

- primary full-covariance status;
- ablation status;
- covariance sensitivity;
- small-sample instability;
- SH0ES-pressure neutrality;
- BAO-release warning;
- exact claim ceiling;
- next derivation target needed before any stronger physics claim.
