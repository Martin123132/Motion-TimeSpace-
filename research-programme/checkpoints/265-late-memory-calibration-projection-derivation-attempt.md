# 265 — Late-Memory Calibration Projection Derivation Attempt

Private derivation checkpoint. This is not a public CMB, BAO, local-GR, or unified-field claim.

## Purpose

Checkpoint 264 showed that official CMB scoring is blocked until real likelihood assets and an LCDM baseline exist.

So this checkpoint returns to the derivation problem:

```text
Can late coherent memory project into calibration/ruler observables
without becoming a local fifth force?
```

This is the bridge we need if the post-scale-lock branch is to become more than a fitted cosmology closure.

## Machine Artifact

Script:

```text
scripts/late_memory_calibration_projection_derivation_attempt.py
```

Run:

```text
runs/20260601-000083-late-memory-calibration-projection-derivation-attempt
```

Status:

```text
late_memory_calibration_projection_conditionally_derived_half_factor_parent_selector_missing
```

Claim ceiling:

```text
calibration_projection_internal_only_no_CMB_BAO_or_local_GR_promotion
```

## Core Result

The conformal projected-zero-mode route gives a real conditional theorem:

```text
tilde_g_munu = exp(C_D) g_munu
```

implies:

```text
d tilde_l = exp(C_D/2) d l
d tilde_tau = exp(C_D/2) d tau
```

Therefore endpoint or clock/ruler calibration ratios carry:

```text
exp(Delta C_D / 2)
```

This means the `1/2` in the half-memory bridge is not arbitrary once the metric map is accepted.

The hard burden moves from:

```text
why half?
```

to:

```text
why this C_D?
why this endpoint jump?
why no local trace response?
why B_mem = 2/27?
```

That is progress, but not promotion.

## What Is Conditionally Derived

| Piece | Result | Status |
|---|---|---|
| conformal metric map | lengths and clocks scale as `exp(C_D/2)` | conditional pass |
| half-factor | endpoint ratios carry `exp(Delta C_D/2)` | conditional pass |
| BAO same-domain cancellation | `tilde_D_X / tilde_r = D_X / r` | conditional pass |
| CMB endpoint contrast | different endpoints retain `exp((C_obs-C_emit)/2)` | conditional pass |
| Bianchi safety | possible if all projector/domain stresses are retained | conditional pass |

The BAO cancellation is the clean bit:

```text
tilde_D_X / tilde_r_BAO
= exp(C_D/2) D_X / [exp(C_D/2) r_BAO]
= D_X / r_BAO.
```

So BAO can be a late same-domain matter-ruler readout while CMB remains an endpoint-contrast observable.

## What Still Fails

| Missing theorem | Why it matters |
|---|---|
| parent selector for `C_D` | otherwise the zero-mode projector is inserted by hand |
| local trace-source suppression | otherwise matter sources `C` and creates local fifth-force risk |
| transition law | otherwise local/BAO/CMB branch selection can look post-hoc |
| `B_mem = 2/27` amplitude | still closure/theorem target |
| `Hstar = H0` scale-lock | still closure/theorem target |

The local issue is sharp:

```text
grad_i C_D = 0
```

is locally safe only if:

```text
C_perp
```

is genuinely projected out, constrained, or volume-suppressed by the parent action.

If a local trace source can excite `C_perp`, the local branch fails.

## Bound Readout

Using the Hubble-cap domain:

```text
L_D = c/H0 = 4440.711864908902 Mpc
```

and:

```text
B_mem = 2/27
```

the smooth half-leak condition:

```text
0.5 B_mem (L/L_D) < BAO ratio tolerance
```

gives:

```text
L < 332.10257281123654 Mpc
```

for the imported `Delta chi2 < 1` BAO leakage tolerance.

So a smooth Hubble-domain memory field is not automatically BAO-dead:

| Probe | Half-leak | BAO safe? |
|---:|---:|---|
| `50 Mpc` | `0.0004170168901264305` | yes |
| `150 Mpc` | `0.0012510506703792917` | yes |
| `300 Mpc` | `0.0025021013407585833` | yes |
| `1000 Mpc` | `0.008340337802528611` | no |

For zero-mode volume dilution:

```text
B_mem (L/L_D)^3 < local q_R gate
```

the safe scale is:

```text
L < 300.70440939223687 Mpc.
```

This is useful but conditional: it only helps if the parent projector is real.

## Drift Gate

The full rolling memory value:

```text
dot_C/H ~= B_mem = 0.07407407407407407
```

is too large for the imported BAO radial drift bound by:

```text
6.563575587525328
```

But the small H0-bridge residual:

```text
dot_C/H = -0.0004084189185673548
```

is only:

```text
0.0361892939857945
```

of that same bound.

So the viable branch requires:

```text
late saturation / residual drift,
not full unsaturated rolling memory.
```

## Decision

Decision:

```text
late_memory_calibration_projection_conditionally_derived_half_factor_parent_selector_missing
```

Meaning:

```text
The conformal domain-zero-mode route conditionally derives the half-factor,
same-domain BAO cancellation, and endpoint contrast structure.
```

But:

```text
the parent selector, local trace-source suppression, transition law, and
B_mem/Hstar amplitude lock remain open.
```

## Where This Leaves Us

This is not grim.

It is actually a better-shaped problem than before:

```text
old problem: explain several apparently separate calibration choices.
new problem: derive one projected conformal zero-mode and its source law.
```

That is a narrower, more field-theoretic burden.

The next target should be:

```text
projected trace-source Ward identity
```

Either derive:

```text
delta C_D / delta T_local = 0
```

or a volume-suppressed response:

```text
delta C_D / delta T_local ~ (L_local/L_D)^3,
```

while retaining Bianchi safety.

If that works, local silence becomes much less hand-wavy. If it fails, the calibration projection remains closure-only.

## Claim Gates

| Gate | Result |
|---|---|
| half-factor derived from metric map | conditional pass |
| BAO same-domain cancellation | conditional pass |
| CMB endpoint contrast | conditional pass |
| BAO smooth leakage | pass as bound |
| full rolling memory drift | fail unless saturated |
| local trace-source silence | open |
| parent selector and transition law | fail/open |
| CMB/BAO/local-GR support claim | forbidden |

## Validation

- Script compiles in `.venv-score`.
- Run completed and wrote `DONE.txt`.
- CSV outputs parse cleanly.
- Cited source paths exist.
- No changes were made to `formalization-workbench`.
- This checkpoint keeps `B_mem = 2/27` and `Hstar = H0` as closure/theorem targets, not derived results.
