# C2 Regularized Closure Ledger

## 1. Purpose

This file follows:

```text
48-C2-activation-growth-CMB-retest.md
```

The question is:

```text
What is the honest status of the C2-regularized activation route after it fixed
the scalar regularity snag and survived internal guardrails?
```

Short answer:

```text
C2_weibull_p3_match_N50 is retained as the cleaner regularized closure
candidate. It is not evidence, not parent-derived, and not public-claim ready.
```

This ledger is here to keep the route alive without letting it cosplay as a
finished theory. Tiny lab coat, no fake doctorate.

## 2. Machine Run

Implemented:

```text
scripts/C2_regularized_closure_ledger.py
```

Successful run:

```text
runs/20260531-015400-C2-regularized-closure-ledger/status.json
```

Readout:

```text
C2_regularized_closure_candidate_retained_not_evidence_parent_derivation_next
```

Generated:

```text
runs/20260531-015400-C2-regularized-closure-ledger/results/source_checkpoint_register.csv
runs/20260531-015400-C2-regularized-closure-ledger/results/regularity_fix_survival_ledger.csv
runs/20260531-015400-C2-regularized-closure-ledger/results/surviving_metric_ledger.csv
runs/20260531-015400-C2-regularized-closure-ledger/results/still_borrowed_missing_gates.csv
runs/20260531-015400-C2-regularized-closure-ledger/results/claim_language_ledger.csv
runs/20260531-015400-C2-regularized-closure-ledger/results/promotion_ladder.csv
runs/20260531-015400-C2-regularized-closure-ledger/results/decision.csv
```

## 3. What It Fixes

The old fractional branch had:

```text
nu_act = 1.7500073382761008
```

That failed:

```text
C2 endpoint regularity;
canonical C1 scalar-potential regularity;
real signed-time-domain status without an extra load invariant.
```

The retained repair is:

```text
C2_weibull_p3_match_N50
F(N) = 1 - exp[-(N/u_3)^3]
```

where:

```text
u_3 is fixed by the original branch's N50;
no new continuous shape knob is added;
endpoint power p = 3 passes the C2/C1 scalar-action regularity threshold.
```

So it fixes the regularity failure that made the fractional scalar proxy
action-unsafe.

## 4. What It Survived

The C2 repair survived:

```text
late SN/BAO/H(z) background smoke;
primary growth guardrail;
full-shape growth guardrail;
compressed CMB distance guardrail;
row-locked H(z) suggested-covariance guardrail.
```

Key deltas versus the original frozen fractional branch:

```text
Delta chi2 late SN+BAO+H(z) = +0.08339169113128264
Delta chi2 primary growth = +0.048037970885054904
Delta chi2 full-shape growth = +0.19868700723528576
Delta chi2 compressed CMB = +0.02092111634944677
Delta chi2 H(z) = +0.03294130302172693
Delta chi2 growth+CMB+H(z) total = +0.10190039025622966
```

Interpretation:

```text
the regularity repair does not materially damage the internal closure behaviour.
```

That is a strong internal result.

## 5. Why It Is Still Not Evidence

Still missing:

```text
parent activation derivation;
b_mem amplitude origin;
transition-scale origin;
perturbation and lensing closure;
official CMB spectra/lensing likelihood;
fresh independent holdout;
local GR/PPN connection.
```

These are not paperwork gaps. They are the difference between:

```text
regularized closure candidate
```

and:

```text
field-theory mechanism.
```

## 6. Allowed and Forbidden Language

Allowed:

```text
the C2-safe activation repair survived fixed-row internal guardrails.
```

Forbidden:

```text
the C2 repair is supported by CMB;
the C2 repair beats LCDM;
the activation law is derived;
official CMB is solved;
the cosmology branch is promoted to field theory.
```

Best wording:

```text
C2_weibull_p3_match_N50 is the current cleaner closure candidate because it
fixes the scalar regularity snag while preserving the internal guardrail
behaviour.
```

## 7. Promotion Ladder

Current stage:

```text
stage 0: regularized_closure_candidate
status: retained
claim level: internal closure candidate
```

Next required stages:

```text
stage 1: parent activation law;
stage 2: perturbation/lensing closure;
stage 3: fresh or official holdout;
stage 4: unified field-theory promotion.
```

The branch cannot skip from stage 0 to stage 4 because the numbers look neat.
Physics does not work by parkour. Sadly.

## 8. Decision

Decision:

```text
C2_regularized_route_status = retained_regularized_closure_candidate_not_evidence
```

Meaning:

```text
the route is alive;
the route is cleaner than the fractional onset;
the route now needs derivation more than another nearby score.
```

So the next move should not be another small internal likelihood tweak. The
next move is to try to derive or reject the parent origin of:

```text
F(N) = 1 - exp[-(N/u_3)^3]
```

and the amplitude/scale attached to it.

## 9. Next Target

Create:

```text
50-parent-activation-law-attempt.md
```

Purpose:

```text
attempt to derive the p=3 activation law from parent memory/load variables.
If p=3 can be connected to a cubic extremality, smooth source onset, or
coarse-grained memory-current theorem, the C2 route moves closer to the field
theory spine. If not, it remains a disciplined closure benchmark.
```

This is the right bottleneck now: the data did not kill the regularized repair,
so the theory has to earn it.
