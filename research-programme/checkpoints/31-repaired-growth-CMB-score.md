# Repaired Growth/CMB Score

## 1. Purpose

This file follows:

```text
30-CMB-distance-prior-implementation-audit.md
```

The question is:

```text
After repairing the CMB sound-horizon integral, does the locked C0/MTS branch
survive the first growth/CMB score?
```

Short answer:

```text
no. The catastrophic artifact is gone, but the locked C0/MTS branch is still
not preferred under the repaired lightweight CMB-distance score.
```

## 2. Machine Run

Implemented:

```text
scripts/repaired_growth_CMB_score.py
```

Successful run:

```text
runs/20260531-002219-repaired-growth-CMB-score/status.json
```

Readout:

```text
C0_not_preferred_repaired_CMB_distance_score
```

## 3. Main Result

Best models:

```text
best chi2: LCDM
best AIC: LCDM
best BIC: LCDM
```

C0/MTS deltas versus the best baseline:

```text
Delta chi2 = 257.510236267431
Delta AIC = 259.510236267431
Delta BIC = 260.4006080253272
```

This is a real tension for this locked branch.

## 4. Dataset Split

Growth remains close:

```text
LCDM chi2_growth_primary = 15.682412358967213
wCDM chi2_growth_primary = 14.463332089064483
CPL chi2_growth_primary = 17.110842020618023
C0 chi2_growth_primary = 14.930776159766813
```

Repaired CMB-distance still disfavors C0/MTS:

```text
LCDM chi2_CMB_repaired = 36.78624047499395
wCDM chi2_CMB_repaired = 129.73831540187126
CPL chi2_CMB_repaired = 231.72153734993066
C0 chi2_CMB_repaired = 295.0481129416254
```

## 5. Interpretation Lock

Allowed language:

```text
the repaired lightweight CMB-distance score disfavors the locked C0/MTS branch;
growth-only behavior remains near-competitive;
this branch needs CMB-calibration/early-limit work before it can be revived.
```

Forbidden language:

```text
MTS is dead;
MTS is supported;
this proves/disproves the parent theory;
this is a public CMB result.
```

## 6. Next Target

Create:

```text
32-repaired-score-readout-and-decision.md
```

Purpose:

```text
decide whether the branch should be demoted now, held as growth-only, or moved
to a CMB-calibrated/official-likelihood upgrade path.
```
