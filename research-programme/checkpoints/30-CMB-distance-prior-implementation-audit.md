# CMB Distance-Prior Implementation Audit

## 1. Purpose

This file follows:

```text
29-growth-CMB-score-readout-and-robustness-gate.md
```

The question is:

```text
Was the huge CMB-distance penalty in the first isolated score a physical C0/MTS
failure, or an implementation/approximation artifact?
```

Short answer:

```text
the huge penalty is an implementation artifact in the sound-horizon integral.
The current 28/29 score is demoted and must be repaired before interpretation.
```

## 2. Machine Run

Implemented:

```text
scripts/post_checkpoint_CMB_distance_prior_implementation_audit.py
```

Successful run:

```text
runs/20260531-001848-CMB-distance-prior-implementation-audit/status.json
```

Readout:

```text
CMB_distance_prior_implementation_error_found_repair_required
```

## 3. Core Finding

The legacy finite redshift-grid sound-horizon method reproduces the huge CMB
penalty:

```text
legacy best chi2 = 4338.670249203061
```

The repaired scale-factor quadrature removes the huge artifact:

```text
scale-factor best chi2 = 36.78624047499395
```

Converged methods agree:

```text
scale-factor quadrature chi2 = 36.78624047499395
quad-to-infinity chi2 = 36.78624047512179
```

## 4. Model Snapshot

With repaired scale-factor quadrature:

```text
LCDM chi2_CMB = 36.78624047499395
wCDM chi2_CMB = 129.73831540187126
CPL chi2_CMB = 231.72153734993066
C0/MTS chi2_CMB = 295.0481129416254
```

So the repair does not automatically rescue C0/MTS, but it changes the result
from catastrophic/pipeline-dominated to interpretable.

## 5. Gate Verdict

Passes:

```text
source 29 required CMB audit;
legacy method reproduces huge chi2;
scale-factor quadrature removes huge artifact;
current score is demoted.
```

Fails intentionally:

```text
support/death claim allowed.
```

Status:

```text
repair required before any physics interpretation.
```

## 6. Caveat

The current lightweight CMB distance prior is still compressed and model
dependent:

```text
the local table uses the wCDM compressed prior by default for C0/MTS.
```

That is acceptable for an internal stress test, but not for a public CMB claim.

## 7. Next Target

Create:

```text
31-repaired-growth-CMB-score.md
```

Purpose:

```text
rerun the isolated growth/CMB first score with the repaired scale-factor CMB
distance integral, then decide whether C0/MTS is still disfavored under the
corrected lightweight CMB treatment.
```
