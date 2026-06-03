# C2 Activation Background Smoke

## 1. Purpose

This file follows:

```text
46-activation-regularity-repair-gate.md
```

The question is:

```text
If we replace the nonanalytic fractional activation with C2-safe no-knob
activation candidates, does the frozen background branch immediately collapse?
```

Short answer:

```text
no. The best C2-safe no-knob repair survives a short SN/BAO/H(z) background
smoke with only a tiny penalty versus the original frozen fractional branch.
```

This is not evidence. It is permission to carry the best repair into the next
fixed-row CMB/growth guardrail.

## 2. Machine Run

Implemented:

```text
scripts/C2_activation_background_smoke.py
```

Successful run:

```text
runs/20260531-014459-C2-activation-background-smoke/status.json
```

Readout:

```text
C2_activation_background_smoke_retains_best_repair_not_evidence
```

Generated:

```text
runs/20260531-014459-C2-activation-background-smoke/results/source_checkpoint_register.csv
runs/20260531-014459-C2-activation-background-smoke/results/C2_activation_background_scores.csv
runs/20260531-014459-C2-activation-background-smoke/results/C2_activation_background_summary.csv
runs/20260531-014459-C2-activation-background-smoke/results/C2_activation_background_gates.csv
runs/20260531-014459-C2-activation-background-smoke/results/decision.csv
```

## 3. Test Setup

Compared:

```text
LCDM_fixed_fit;
wCDM_fixed_fit;
CPL_fixed_fit;
locked_C0_no_SH0ES_fit;
C0_frozen_original_fractional_weibull;
C2_weibull_p3_match_N50;
C2_weibull_p4_match_N50;
C2_hill_p3_match_N50;
C2_hill_p4_match_N50.
```

Data/guardrails:

```text
Pantheon+ no-SH0ES shape branch;
DESI DR1 BAO branch from the existing no-SH0ES config;
row-locked Moresco15_BC03 H(z) suggested covariance branch.
```

Frozen rule:

```text
no h0/Omega_m0/b_mem/alpha/nu/rd refit;
no new activation scale;
no model-selection claim.
```

## 4. Main Result

Best C2-safe no-knob repair:

```text
C2_weibull_p3_match_N50
```

Penalty versus the original frozen fractional branch:

```text
Delta chi2 SN+BAO = +0.050450388109538835
Delta chi2 SN+BAO+H(z) = +0.08339169113128264
```

That is safely inside the predeclared smoke threshold:

```text
Delta chi2 <= 3
```

So the regularity repair does not immediately wreck the late-background branch.

## 5. Score Table

Selected SN+BAO+H(z) totals:

```text
CPL_fixed_fit = 1474.2355285889776
locked_C0_no_SH0ES_fit = 1474.7371896627758
C0_frozen_original_fractional_weibull = 1477.4624163594585
C2_weibull_p3_match_N50 = 1477.5458080505898
C2_weibull_p4_match_N50 = 1477.6425434472242
C2_hill_p3_match_N50 = 1477.6497707768553
C2_hill_p4_match_N50 = 1477.7061136763152
```

Interpretation:

```text
the C2 repairs stay close to the frozen original branch;
they do not beat the standard fitted baselines in this smoke;
they are not model-selection evidence.
```

## 6. Gates

Passed:

```text
source 46 complete;
four no-knob C2 repairs evaluated;
best repair not worse than original by 3;
next fixed-row CMB/growth retest authorized.
```

Failed by design:

```text
model-selection claim.
```

The failed claim is important. These rows are frozen closure candidates, not
new fitted cosmology models.

## 7. Decision

Decision:

```text
C2_activation_late_background_status = retained_for_next_guardrail
```

Meaning:

```text
C2_weibull_p3_match_N50 becomes the current preferred regularity-safe closure
candidate for the next fixed-row retest.
```

Allowed:

```text
the C2-safe repair survived a short no-rescue late-background smoke.
```

Forbidden:

```text
the C2 repair is supported by data;
the C2 repair beats LCDM/wCDM/CPL;
the parent activation law is derived.
```

## 8. Next Target

Create:

```text
48-C2-activation-growth-CMB-retest.md
```

Purpose:

```text
repeat the fixed-row compressed CMB, growth, and H(z) guardrails for
C2_weibull_p3_match_N50. If it survives, the regularized scalar-action route
remains alive as a disciplined closure candidate. If it fails, regularity has
destroyed the cosmology branch and the route is demoted.
```

This is exactly the right kind of progress: a field-theory regularity demand
made a new empirical bet, and the first smoke did not kill it.
