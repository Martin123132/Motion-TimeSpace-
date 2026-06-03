# C2 Activation Growth CMB Retest

## 1. Purpose

This file follows:

```text
47-C2-activation-background-smoke.md
```

The question is:

```text
Does the best C2-safe activation repair survive the fixed-row growth,
compressed-CMB, and H(z) guardrails without parameter rescue?
```

Short answer:

```text
yes, as a regularized closure candidate. C2_weibull_p3_match_N50 survives the
guardrail stack with only a small penalty versus the original frozen fractional
row.
```

This is not evidence. It is a stronger internal survival result.

## 2. Machine Run

Implemented:

```text
scripts/C2_activation_growth_CMB_retest.py
```

Successful run:

```text
runs/20260531-015005-C2-activation-growth-CMB-retest/status.json
```

Readout:

```text
C2_activation_growth_CMB_retest_retains_regularized_closure_not_evidence
```

Generated:

```text
runs/20260531-015005-C2-activation-growth-CMB-retest/results/source_checkpoint_register.csv
runs/20260531-015005-C2-activation-growth-CMB-retest/results/C2_activation_growth_CMB_scores.csv
runs/20260531-015005-C2-activation-growth-CMB-retest/results/C2_growth_predictions.csv
runs/20260531-015005-C2-activation-growth-CMB-retest/results/C2_CMB_predictions.csv
runs/20260531-015005-C2-activation-growth-CMB-retest/results/C2_activation_growth_CMB_gates.csv
runs/20260531-015005-C2-activation-growth-CMB-retest/results/decision.csv
```

## 3. Fixed Candidate

Best regularity-safe candidate carried forward:

```text
C2_weibull_p3_match_N50
```

Rules:

```text
same checkpoint-38 frozen h0/Omega_m0/b_mem/alpha/nu/rd values;
activation shape changed only by the predeclared C2 repair;
no refit;
no new scale;
no official-CMB support claim.
```

The repair is:

```text
F(N) = 1 - exp[-(N/u_3)^3]
```

with `u_3` fixed by the original branch's `N50`.

## 4. Main Result

Compared to the original frozen fractional branch:

```text
Delta chi2 primary growth = +0.048037970885054904
Delta chi2 full-shape growth = +0.19868700723528576
Delta chi2 compressed CMB = +0.02092111634944677
Delta chi2 H(z) suggested covariance = +0.03294130302172693
Delta chi2 total growth+CMB+H(z) = +0.10190039025622966
```

All predeclared guardrails passed.

Interpretation:

```text
regularizing the activation to the minimal C2 p=3 Weibull form does not destroy
the CMB/growth/H(z) closure behaviour.
```

This is the strongest internal result for the scalar-action route so far.

## 5. Score Snapshot

Selected totals:

```text
LCDM_fixed_no_SH0ES growth+CMB+H(z) = 58.690850526635224
C0_frozen_original_fractional_weibull = 21.548301488830056
C2_weibull_p3_match_N50 = 21.650201879086286
```

Important caveat:

```text
these totals include compressed CMB distance information and frozen closure
rows, so they are not valid model-selection evidence.
```

The useful comparison is only:

```text
C2 repair versus original frozen closure under the same fixed-row guardrail.
```

## 6. CMB Shift

Compressed CMB predictions moved only slightly:

```text
original R = 1.7492999531314468
C2 R = 1.749231764336998

original l_A = 301.4620001908985
C2 l_A = 301.45024901561925
```

The compressed-CMB chi2 increase was:

```text
+0.02092111634944677
```

So the C2 repair keeps the calibrated distance-prior closure almost intact.

## 7. Gates

Passed:

```text
source 47 complete;
primary growth not worse than original by 2;
full-shape growth not worse than original by 2;
compressed CMB not worse than original by 5;
H(z) not worse than original by 1.
```

Failed by design:

```text
support claim.
```

Reason:

```text
C2 activation is regularized closure, not parent-derived;
compressed CMB is not official spectra/lensing;
metric/lensing perturbations remain imported if used.
```

## 8. Decision

Decision:

```text
C2_activation_growth_CMB_status = retained_regularized_closure_candidate
```

Meaning:

```text
the regularized scalar-action route remains alive;
the C2 repair is now the cleaner closure candidate than the fractional onset;
promotion is still forbidden until parent derivation and official/fresh tests.
```

Allowed:

```text
the C2-safe activation repair survived fixed-row late-background, growth,
compressed-CMB, and H(z) guardrails.
```

Forbidden:

```text
the C2 repair is supported by CMB;
the C2 repair beats LCDM;
the activation law is parent-derived;
official CMB is solved.
```

## 9. Next Target

Create:

```text
49-C2-regularized-closure-ledger.md
```

Purpose:

```text
package the regularized closure candidate honestly: what it fixes, what it
survives, what it still borrows, and what exact gates remain before it can
become part of the field-theory spine.
```

This is now worth ledgering because the C2 repair has survived both regularity
and empirical guardrails without rescue.
