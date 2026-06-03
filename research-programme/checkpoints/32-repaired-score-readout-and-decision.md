# Repaired Score Readout and Decision

## 1. Purpose

This file follows:

```text
31-repaired-growth-CMB-score.md
```

The question is:

```text
How should the repaired growth/CMB result change the status of the locked
C0/MTS branch?
```

Short answer:

```text
demote the locked C0/MTS growth+CMB branch for this repaired lightweight
CMB-distance holdout, but retain the growth-only behavior as a subdiagnostic.
Do not claim support, death, or public CMB evidence.
```

## 2. Machine Run

Implemented:

```text
scripts/repaired_score_readout_and_decision.py
```

Successful run:

```text
runs/20260531-002511-repaired-score-readout-and-decision/status.json
```

Readout:

```text
locked_C0_demoted_for_repaired_CMB_distance_but_growth_subdiagnostic_retained
```

## 3. Decision Register

Locked C0 growth+CMB:

```text
demote for repaired lightweight CMB-distance holdout.
```

Growth-only projection:

```text
retain as interesting near-competitive subdiagnostic.
```

Full-shape growth robustness:

```text
retain as near-competitive subdiagnostic.
```

CMB-distance projection:

```text
requires calibration or parent early-limit work before revival.
```

## 4. Gate Verdict

Passes:

```text
source 31 complete;
growth-only subdiagnostic retained.
```

Fails intentionally:

```text
locked C0 support allowed;
locked C0 death claim allowed;
public claim allowed.
```

## 5. What This Means

This is the disciplined read:

```text
the strict no-SH0ES locked C0/MTS background branch is not currently a viable
growth+CMB support branch.
```

But it is not theory death:

```text
the failure is branch-specific and CMB-distance-specific; the growth sector is
close enough to preserve as a controlled diagnostic.
```

## 6. Next Target

Create:

```text
33-CMB-calibration-freedom-audit.md
```

Purpose:

```text
test whether equal CMB calibration/background freedom changes the CMB-distance
verdict, without giving MTS extra freedom that baselines do not receive.
```
