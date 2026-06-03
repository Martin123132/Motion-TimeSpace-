# 107 - Two-Ninth Fixed-Amplitude Scout

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 106 said the next belt-round gate is:

```text
derive B_mem / DeltaR,
or keep the cosmology branch explicitly closure-only.
```

The strict full-covariance primary branch had:

```text
B_mem = 0.07453319160061826
DeltaR = 3 B_mem = 0.22359957480185477
```

That is very close to:

```text
DeltaR = 2/9 = 0.2222222222222222
B_mem = DeltaR/3 = 2/27 = 0.07407407407407407
```

This checkpoint tests that exact rational amplitude as a fixed no-fit scout branch. The point is not to claim a derivation. The point is to ask whether there is a precise theorem target worth trying to derive.

## 2. Short Verdict

```text
fixed_amplitude_scout_status =
two_ninth_promising_not_derived
```

```text
promotion_allowed =
false
```

Plain English:

```text
DeltaR = 2/9 is an unexpectedly strong fixed-amplitude scout on the primary full-covariance SN+BAO branch.
```

It gives almost the same chi2 as the fitted-amplitude canonical branch, while using one fewer cosmological parameter. That is genuinely interesting.

But it is also post-fit scouted. It is not yet a prediction.

Boxing-score version:

```text
This is a clean counterpunch. Not a title belt, but it made the judges look up.
```

## 3. Machine Artifact

Script:

```text
research-programme\scripts\canonical_R_fixed_amplitude_scout.py
```

Run:

```text
research-programme\runs\20260531-145515-canonical-R-fixed-amplitude-scout
```

Generated:

```text
rational_candidate_register.csv
fixed_candidate_scores.csv
fixed_candidate_comparisons.csv
decision.csv
status.json
```

Status:

```text
two_ninth_fixed_amplitude_scout_promising_not_derived
```

## 4. Candidate Register

The script tested simple normalized-charge contrasts:

| Candidate | `DeltaR` | `B_mem=DeltaR/3` | Role |
|---|---:|---:|---|
| `two_ninth_boundary_charge` | 2/9 | 2/27 = 0.074074 | closest simple charge split to primary fitted value |
| `quarter_boundary_charge` | 1/4 | 1/12 = 0.083333 | cell-quarter contrast scout |
| `one_third_trace_charge` | 1/3 | 1/9 = 0.111111 | trace-third contrast scout |
| `four_ninth_boundary_charge` | 4/9 | 4/27 = 0.148148 | small-sample high-branch contrast scout |
| `half_boundary_charge` | 1/2 | 1/6 = 0.166667 | half-contrast scout |

The exact `2/9` candidate differs from the fitted primary amplitude by:

```text
Delta B_mem = -0.00045911752654419213
relative Delta B_mem = -0.6159%
```

That closeness is not proof. It is a reason to test.

## 5. Fixed-Amplitude Primary Score

Primary branch:

```text
SN observable = mb-corr
SN covariance = full
SN rows = full Pantheon+ shape branch
BAO = DESI DR2 primary
calibrators = excluded
```

The `2/9` candidate fixes:

```text
p = 3
u3 = 1/4
DeltaR = 2/9
B_mem = 2/27
```

Only `Omega_m` is fitted cosmologically, with the same analytic SN offset and BAO alpha nuisance handling as the existing runner.

Best fit:

```text
Omega_m = 0.3032827426766658
chi2 penalty vs fitted-amplitude MTS = 0.00019179382275069656
```

That penalty is basically zero at this scorecard precision.

## 6. Primary Comparison Card

For `two_ninth_boundary_charge`:

| Reference | Delta chi2 | Delta AIC | Delta BIC | Readout |
|---|---:|---:|---:|---|
| `LCDM` | -5.259467 | -5.259467 | -5.259467 | fixed candidate wins AIC/BIC |
| `wCDM` | -0.169009 | -2.169009 | -7.569630 | fixed candidate wins AIC/BIC |
| `CPL` | +0.167728 | -3.832272 | -14.633514 | fixed candidate wins AIC/BIC by parsimony |
| fitted-amplitude `canonical_R_closure` | +0.000192 | -1.999808 | -7.400429 | fixed amplitude beats fitted branch by IC |
| zero-memory control | -5.259467 | -5.259467 | -5.259467 | nonzero fixed memory wins |

This matters because the fitted `B_mem` branch had a fair objection:

```text
one extra parameter buys the memory improvement.
```

The `2/9` scout removes that objection on the primary branch:

```text
same effective cosmological parameter count as LCDM,
better chi2 than LCDM by about 5.26,
better AIC/BIC by the same amount.
```

## 7. Theory Interpretation

If the parent theory could derive:

```text
eta = 1
a_F = 1
DeltaR = 2/9
```

then the amplitude would become:

```text
B_mem = 2/27
```

and the cosmology branch would no longer be using a fitted memory amplitude on the primary scorecard.

The clean theorem target would be:

```text
normalized boundary charge contrast = 2/9.
```

A possible schematic route would be:

```text
R = Q_boundary / Q_*
DeltaR = (Q_early - Q_today) / Q_* = 2/9
```

But that route is not currently derived. A rational number near a fit is not a theory.

## 8. Gate Results

| Gate | Result | Reason |
|---|---|---|
| `fixed_amplitude_branch_constructed` | pass | `B_mem=2/27` scored without fitting `B_mem` |
| `primary_chi2_penalty_small` | pass | penalty vs fitted-amplitude branch is `0.000192` |
| `LCDM_same_k_comparison_wins` | pass | fixed candidate has `k=3`, same as LCDM, and improves chi2/AIC/BIC |
| `aic_bic_penalty_removed` | pass | fixed branch beats fitted-amplitude MTS by IC due one fewer parameter |
| `two_ninth_theory_derived` | fail | no parent boundary-charge theorem yet |
| `post_fit_scout_warning` | fail as claim | candidate was noticed after seeing the fitted primary amplitude |
| `robustness_matrix_repeated` | open | must test across diagonal, small sample, SH0ES, and DR1/DR2 branches |
| `support_claim_allowed` | fail | this is an amplitude scout, not a prediction |

## 9. Claim Ceiling

Allowed statement:

```text
The exact fixed-amplitude scout DeltaR=2/9, B_mem=2/27 reproduces the primary full-covariance fitted-amplitude score almost exactly and beats LCDM on the primary scorecard with no extra amplitude parameter.
```

Forbidden statement:

```text
MTS predicts DeltaR=2/9.
```

Reason:

```text
the normalized boundary charge, endpoint equation, and trace Ward identity have not derived 2/9.
```

## 10. Decision

Decision:

```text
two_ninth_status =
promising_fixed_amplitude_scout_not_prediction
```

Decision:

```text
new_theory_target =
derive_or_reject_normalized_boundary_charge_contrast_2_over_9
```

Decision:

```text
new_empirical_target =
repeat_fixed_2_over_27_amplitude_across_T1_to_T6_robustness_matrix
```

## 11. Next Target

Create a T7 fixed-amplitude robustness matrix:

```text
108-two-ninth-fixed-amplitude-robustness.md
```

Purpose:

```text
lock B_mem=2/27 before scoring,
rerun the relevant T1-T6 branches,
and decide whether 2/9 is a reproducible theorem target or a primary-branch coincidence.
```

Pass condition:

```text
The locked-amplitude branch remains competitive on the primary full-covariance card
and does not collapse under covariance, SH0ES, or BAO-release stress.
```

Fail condition:

```text
2/9 works only because it was reverse-engineered from the primary fitted amplitude.
```
