# Growth/CMB Score Readout and Robustness Gate

## 1. Purpose

This file follows:

```text
28-isolated-growth-CMB-first-score-runner.md
```

The question is:

```text
Does the first isolated growth/CMB score kill the locked C0/MTS branch, or is
the result dominated by a narrower pipeline/observable issue?
```

Short answer:

```text
the locked C0/MTS branch is not preferred in the total score, but the verdict is
dominated by the compressed CMB-distance block. Growth is near-competitive.
Audit the CMB-distance implementation before declaring branch death.
```

## 2. Machine Run

Implemented:

```text
scripts/growth_CMB_score_readout_and_robustness_gate.py
```

Successful run:

```text
runs/20260531-001431-growth-CMB-score-readout-and-robustness-gate/status.json
```

Readout:

```text
growth_CMB_score_disfavors_locked_C0_but_CMB_distance_block_dominates
```

## 3. Robustness Verdict

Locked C0/MTS status:

```text
not preferred in first total growth/CMB score.
```

Growth-side status:

```text
near competitive.
```

CMB-distance status:

```text
dominant tension; audit required.
```

Claim status:

```text
support claim allowed = false
death claim allowed = false
public claim allowed = false
```

## 4. Key Decomposition

C0/MTS compared to best baseline:

```text
primary growth delta chi2 ≈ 0.46744407070233006
CMB-distance delta chi2 ≈ 3387.472138271843
total delta chi2 ≈ 3387.9395823425457
```

So the failure is not evenly distributed.

## 5. What This Means

This is bad for the locked branch, but not the whole theory:

```text
if the compressed CMB-distance implementation is correct, this strict C0
background branch likely needs demotion for growth/CMB.
```

But we must not skip the audit:

```text
all models have very large compressed CMB-distance chi2, so the next check is
whether R, l_A, covariance ordering, units, and Planck-table assumptions are
being handled correctly.
```

## 6. Next Target

Create:

```text
30-CMB-distance-prior-implementation-audit.md
```

Purpose:

```text
verify the compressed CMB-distance likelihood before interpreting the C0/MTS
failure as physical rather than pipeline/approximation-driven.
```
