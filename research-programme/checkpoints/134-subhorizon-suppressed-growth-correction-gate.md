# 134 - Subhorizon Suppressed Growth Correction Gate

Private numeric gate. This is not a public claim.

## 1. Trigger

Checkpoint 133 found:

```text
exact smooth memory fails for an ordinary separately conserved perfect fluid
when w_mem != -1.
```

But it also found a viable subhorizon route:

```text
delta_mem / delta_m ~ (1+w_mem) (aH/ck)^2
```

if the parent stress derives a high-sound-speed or otherwise non-clustering memory sector.

This checkpoint asks:

```text
Would that residual correction be large enough to move the checkpoint-130
SDSS/eBOSS growth result?
```

## 2. Machine Artifact

Script:

```text
research-programme\scripts\subhorizon_suppressed_growth_correction_gate.py
```

Run:

```text
research-programme\runs\20260531-191200-subhorizon-suppressed-growth-correction-gate
```

Generated:

```text
source_register.csv
correction_bounds.csv
summary_by_k_and_safety.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
subhorizon_memory_growth_correction_negligible_conditionally
```

Claim ceiling:

```text
subhorizon_growth_correction_bound_only
```

## 3. Bound Used

The rough bound is:

```text
delta_mem / delta_m ~ |1+w_mem| (aH/ck)^2
```

and the rough Poisson-source fraction is:

```text
source_fraction ~ (Omega_mem / Omega_m) |1+w_mem| (aH/ck)^2
```

This was applied only to the checkpoint-130 primary DR2 `f_sigma8` rows:

```text
MGS
BOSS DR12 LRG
eBOSS DR16 LRG
eBOSS DR16 QSO
```

with:

```text
k = 0.02, 0.05, 0.10, 0.20 h/Mpc
safety factors = 1, 10, 100
```

The safety factors deliberately over-amplify the correction to see whether the result is fragile.

## 4. Summary

Worst-case summary:

| k `[h/Mpc]` | safety | max source fraction | max fractional shift | diagonal chi2 impact |
|---:|---:|---:|---:|---:|
| `0.02` | `1` | `4.1362859290658554e-05` | `4.1362859290658554e-05` | `4.9787062397912674e-08` |
| `0.02` | `10` | `4.1362859290658554e-05` | `0.00041362859290658557` | `4.978706239791267e-06` |
| `0.02` | `100` | `4.1362859290658554e-05` | `0.0041362859290658555` | `0.0004978706239791267` |
| `0.05` | `100` | `6.618057486505369e-06` | `0.0006618057486505369` | `1.2745487973865648e-05` |
| `0.10` | `100` | `1.6545143716263423e-06` | `0.00016545143716263422` | `7.96592998366603e-07` |
| `0.20` | `100` | `4.1362859290658556e-07` | `4.1362859290658554e-05` | `4.978706239791269e-08` |

Main readout:

```text
even safety factor 100 gives total diagonal chi2 impact < 0.001.
```

So this correction is nowhere near large enough to alter checkpoint 130.

## 5. Largest Individual Rows

Largest individual diagonal impacts:

| Sample | z | k `[h/Mpc]` | safety | fractional data sigma | source fraction | fractional shift | diagonal chi2 impact |
|---|---:|---:|---:|---:|---:|---:|---:|
| `BOSS_DR12_LRG` | `0.38` | `0.02` | `100` | `0.08981904669520101` | `1.6521957812688568e-05` | `0.0016521957812688569` | `0.0003383655463778168` |
| `MGS` | `0.15` | `0.02` | `100` | `0.33453366014266217` | `4.1362859290658554e-05` | `0.0041362859290658555` | `0.00015287675680252912` |
| `BOSS_DR12_LRG` | `0.51` | `0.02` | `100` | `0.0750251609398099` | `1.931523553547559e-06` | `0.0001931523553547559` | `6.628055638524608e-06` |

The largest fractional source occurs at low redshift, but the data errors are much larger than the correction.

## 6. Gates

Gate results:

| Gate | Status | Evidence |
|---|---|---|
| nominal high-sound-speed bound | pass | worst diagonal chi2 impact at safety `1` is `4.97871e-08` |
| safety factor 10 bound | pass | worst diagonal chi2 impact at safety `10` is `4.97871e-06` |
| safety factor 100 bound | pass | worst diagonal chi2 impact at safety `100` is `0.000497871` |
| checkpoint-130 proxy practicality | pass conditional | corrections are far below current diagonal growth errors |
| theory promotion | fail | numeric smallness does not derive `c_s^2` or auxiliary/geometric stress owner |

## 7. Interpretation

This is a strong practical result.

Checkpoint 133 said:

```text
exact smooth perfect-fluid memory is not allowed.
```

Checkpoint 134 says:

```text
but if the parent stress gives high-sound-speed/subhorizon suppression, the
correction is completely negligible for the SDSS/eBOSS growth rows used in
checkpoint 130.
```

Therefore:

```text
checkpoint 130 remains a robust late-time subhorizon approximation target.
```

But:

```text
it is still not a derived growth theory.
```

Boxing-score version:

```text
The perfect-fluid jab landed on us in checkpoint 133.
But when we checked the scorecards, the actual damage on SDSS/eBOSS scales is
basically invisible. MTS keeps the round, conditionally.
```

## 8. Consequence For Theory Building

This narrows the parent-action task.

We no longer need the parent stress to prove:

```text
absolutely zero memory perturbations in every gauge and on every scale
```

for the late-time growth gate.

It is enough for this empirical pillar if the parent stress derives:

```text
c_s^2 ~ 1 or stronger smoothing
```

or:

```text
a non-propagating auxiliary/geometric memory constraint
```

because the residual correction is below current sensitivity.

But for a full theory, especially CMB and very-large-scale ISW/lensing:

```text
the exact perturbation sector is still required.
```

## 9. Decision

Decision:

```text
subhorizon_growth_proxy_status =
practically_robust_late_time_subhorizon
```

Meaning:

```text
the checkpoint-130 growth proxy survives the first correction-bound audit;
the perfect-fluid exact theorem remains rejected;
the viable theory route is high-sound-speed or auxiliary/geometric memory.
```

Do not promote as derived.

Do not demote the growth branch.

Use checkpoint 130 as:

```text
a robust empirical/theorem target for late-time subhorizon growth.
```

## 10. Next Target

Create:

```text
135-high-sound-speed-or-auxiliary-memory-owner.md
```

Purpose:

```text
try to derive the mechanism that makes memory perturbations high-sound-speed,
non-propagating, or geometrically constrained.
```

Pass condition:

```text
derive either c_s^2 ~ 1 / large, or an auxiliary/geometric constraint that
removes the scalar mode, while preserving the locked background.
```

Fail condition:

```text
the parent stress necessarily introduces a low-sound-speed clustering scalar
or anisotropic stress that would need a new fitted growth parameter.
```

If it fails:

```text
derive controlled modified growth terms or demote growth to empirical closure-only.
```
