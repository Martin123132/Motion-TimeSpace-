# 108 - Two-Ninth Fixed-Amplitude Robustness

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 107 found that the exact locked candidate:

```text
DeltaR = 2/9
B_mem = 2/27
```

almost exactly reproduced the fitted-amplitude primary full-covariance branch.

That result could have been a coincidence or a post-fit rationalization. This checkpoint repeats the locked amplitude across the already-built robustness branches.

## 2. Short Verdict

```text
T7_status =
two_ninth_locked_amplitude_survives_matrix
```

```text
promotion_allowed =
false
```

Plain English:

```text
The fixed no-fit amplitude B_mem=2/27 survives the T1-T6 robustness matrix surprisingly well.
```

It remains competitive against `LCDM`, `wCDM`, and `CPL`, and it stays close to the fitted-amplitude MTS branch while using one fewer cosmological parameter.

This upgrades `DeltaR=2/9` from a cute numerical coincidence to a serious private theorem target.

It still does not make it derived.

## 3. Machine Artifact

Script:

```text
research-programme\scripts\canonical_R_two_ninth_T7_robustness.py
```

Run:

```text
research-programme\runs\20260531-145921-canonical-R-two-ninth-T7-robustness
```

Generated:

```text
source_register.csv
locked_branch_scores.csv
locked_branch_comparisons.csv
branch_gates.csv
decision.csv
status.json
```

Status:

```text
two_ninth_locked_amplitude_survives_matrix
```

## 4. Branches Tested

| Branch | Role | SN covariance | SN observable | BAO |
|---|---|---|---|---|
| `T1_primary_fullcov_DR2` | primary | full | `mb-corr` | DESI DR2 |
| `T3_diagonal_fullsample_DR2` | covariance diagnostic | diagonal | `mb-corr` | DESI DR2 |
| `T4_small_fullcov_DR2` | small-sample diagnostic | full | `mb-corr` | DESI DR2 |
| `T5_SH0ES_pressure` | local-H0 pressure stress | diagonal | `mu-sh0es` | DESI DR2 |
| `T5_matched_control` | matched pressure control | diagonal | `mb-corr` | DESI DR2 |
| `T6_small_fullcov_DR1` | BAO-release diagnostic | full | `mb-corr` | DESI DR1 |

The locked branch used:

```text
p = 3
u3 = 1/4
DeltaR = 2/9
B_mem = 2/27
```

Only `Omega_m` was fitted cosmologically, with the same SN-offset and BAO-alpha nuisance treatment as the previous runner.

## 5. Gate Card

| Branch | Gate result | Delta chi2 vs LCDM | Delta AIC vs LCDM | Delta BIC vs LCDM | Delta chi2 vs fitted MTS |
|---|---|---:|---:|---:|---:|
| `T1_primary_fullcov_DR2` | pass | -5.259467 | -5.259467 | -5.259467 | +0.000192 |
| `T3_diagonal_fullsample_DR2` | pass | -7.956849 | -7.956849 | -7.956849 | +0.488038 |
| `T4_small_fullcov_DR2` | pass | -2.112126 | -2.112126 | -2.112126 | +0.542866 |
| `T5_SH0ES_pressure` | pass | -2.107102 | -2.107102 | -2.107102 | +0.538510 |
| `T5_matched_control` | pass | -2.107119 | -2.107119 | -2.107119 | +0.538525 |
| `T6_small_fullcov_DR1` | pass | -0.852546 | -0.852546 | -0.852546 | +0.284359 |

This is the key read:

```text
every tested locked-amplitude branch beats LCDM on chi2/AIC/BIC;
every tested locked-amplitude branch stays within about 0.55 chi2 of the fitted-amplitude MTS branch;
because B_mem is no longer fitted, the locked branch beats the fitted-amplitude branch on AIC/BIC in all tested branches.
```

That is a real improvement in discipline.

## 6. Comparisons Against Flexible Baselines

The locked `2/27` branch also compares well against the flexible baselines:

| Branch | vs `wCDM` Delta AIC | vs `wCDM` Delta BIC | vs `CPL` Delta AIC | vs `CPL` Delta BIC |
|---|---:|---:|---:|---:|
| `T1_primary_fullcov_DR2` | -2.169009 | -7.569630 | -3.832272 | -14.633514 |
| `T3_diagonal_fullsample_DR2` | -2.820426 | -8.221047 | -4.450709 | -15.251950 |
| `T4_small_fullcov_DR2` | -2.852790 | -6.424944 | -1.537728 | -8.682036 |
| `T5_SH0ES_pressure` | -2.889946 | -6.462100 | -1.815880 | -8.960188 |
| `T5_matched_control` | -2.889838 | -6.461992 | -1.815262 | -8.959570 |
| `T6_small_fullcov_DR1` | -2.807374 | -6.375719 | -1.928116 | -9.064805 |

This is exactly the Mayweather-style scoring logic:

```text
not always lower chi2 than every flexible model,
but cleaner parameter count,
stronger AIC/BIC card,
and no fitted memory-amplitude knob.
```

## 7. What Changed Scientifically

Before T7, the branch was:

```text
canonical_R_closure with fitted B_mem.
```

After T7, there is a sharper private branch:

```text
canonical_R_2over27_locked_amplitude
```

with:

```text
eta = 1
a_F = 1
DeltaR = 2/9
B_mem = 2/27
p = 3
u3 = 1/4
```

This branch is much closer to what a field-theory programme needs, because the amplitude can now be treated as a fixed theorem target rather than an optimized number.

The theory debt becomes very precise:

```text
derive normalized boundary-charge contrast 2/9.
```

## 8. Why This Is Still Not a Claim

The number `2/9` was noticed after seeing the primary fitted amplitude. That means it is not an independent prior prediction yet.

The current status is:

```text
locked amplitude robustness scout,
not parent-action derivation.
```

The branch is allowed to guide theory work, but not to claim field-theory support.

Forbidden reading:

```text
MTS predicts B_mem=2/27.
```

Allowed reading:

```text
The exact locked amplitude B_mem=2/27 is a high-value theorem target because it survives the current SN+BAO robustness matrix without fitting the memory amplitude.
```

## 9. New Theorem Target

The parent action must now try to produce:

```text
R = Q_boundary / Q_*
DeltaR = (Q_early - Q_today) / Q_* = 2/9
```

while preserving:

```text
eta = 1
a_F = 1
p = 3
u3 = 1/4
local GR/PPN silence
covariant conservation
```

This is stronger than the previous amplitude corridor:

```text
DeltaR = 0.223600 to 0.460135.
```

The corridor now has a bullseye:

```text
DeltaR = 2/9.
```

## 10. Gate Results

| Gate | Result | Reason |
|---|---|---|
| `primary_fixed_amplitude_gate` | pass | locked branch beats LCDM AIC/BIC and matches fitted MTS within `0.0002` chi2 |
| `covariance_diagnostic_gate` | pass | diagonal fullsample branch remains strong |
| `small_sample_gate` | pass diagnostic | locked branch still beats LCDM and stays close to fitted MTS |
| `SH0ES_pressure_gate` | pass diagnostic | pressure and matched control behave nearly identically |
| `BAO_release_gate` | pass diagnostic | DR1 branch weakens but remains positive vs LCDM |
| `amplitude_parameter_removed` | pass | `B_mem` is fixed, not optimized |
| `two_ninth_parent_derived` | fail | no boundary-charge theorem yet |
| `public_support_claim_allowed` | fail | post-fit scout status blocks prediction language |

## 11. Decision

Decision:

```text
two_ninth_status =
robust_locked_amplitude_theorem_target_not_prediction
```

Decision:

```text
best_next_theory_problem =
derive_or_reject_boundary_charge_contrast_2_over_9
```

Decision:

```text
best_next_empirical_problem =
freeze_B_mem_2_over_27_as_a_predeclared_branch_for_future_CMB_growth_and_external_release_tests
```

## 12. Next Target

Create:

```text
109-boundary-charge-two-ninth-theorem-attempt.md
```

Purpose:

```text
attempt to derive DeltaR = 2/9 from a normalized boundary charge, observer-cell trace split, or relative cohomology current.
```

Pass condition:

```text
2/9 follows from structure already present in the parent programme,
not from fitting SN+BAO.
```

Fail condition:

```text
2/9 remains a useful locked empirical branch but not a theory-owned amplitude.
```
