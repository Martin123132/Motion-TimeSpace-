# 197 - BAO Common-Mode Ratio Theorem Attempt

Private theory checkpoint. This is not a public BAO claim.

## 1. Trigger

Checkpoint 196 showed that BAO cannot tolerate a naked half-memory rescaling:

```text
D_X/r_d -> exp(-B_mem/2) D_X/r_d
```

gave a DESI DR2 scale-mode penalty:

```text
chi2 = 172.3159081737169.
```

Therefore BAO survival requires a real theorem:

```text
D_X and r_d must carry the same conformal endpoint unit,
so the ratio D_X/r_d is invariant.
```

This checkpoint attempts that theorem and quantifies how exact the cancellation
must be.

## 2. Machine Artifact

Script:

```text
scripts/BAO_common_mode_ratio_theorem_attempt.py
```

Run:

```text
runs/20260601-000014-BAO-common-mode-ratio-theorem-attempt
```

Command:

```text
python scripts/BAO_common_mode_ratio_theorem_attempt.py --timestamp 20260601-000014
```

Status:

```text
BAO_common_mode_ratio_theorem_conditional_radial_drift_and_alpha_owner_open
```

Claim ceiling:

```text
conditional_BAO_ratio_theorem_internal_only_no_parent_alpha_no_support_claim
```

## 3. Theorem Attempt

Start with the matter-observer metric:

```text
tilde_g_munu = exp(C) g_munu.
```

Then local lengths and clocks scale as:

```text
d tilde_ell = exp(C/2) d ell,
d tilde_tau = exp(C/2) d tau.
```

For homogeneous saturated `C` across the late BAO survey patch:

```text
tilde_D_M = exp(C_obs/2) D_M.
```

The radial BAO distance is more delicate:

```text
tilde_D_H = c / tilde_H
          = exp(C_obs/2) D_H / (1 + dot_C/(2H)).
```

So:

```text
tilde_D_H ~= exp(C_obs/2) D_H
```

only if `dot_C/H` is negligible at BAO readout.

For the isotropic distance:

```text
tilde_D_V = [z tilde_D_M^2 tilde_D_H]^(1/3)
          ~= exp(C_obs/2) D_V
```

if the radial drift term is suppressed.

The required BAO ruler condition is:

```text
tilde_r_d^(late unit) = exp(C_obs/2) r_d.
```

Then:

```text
tilde_D_X / tilde_r_d = D_X / r_d,
X in {M, H, V}.
```

This is the conditional theorem:

```text
homogeneous conformal matter units cancel in BAO ratios.
```

## 4. What Was Derived

The common-mode cancellation is algebraically clean for:

```text
D_M/r_d.
```

It is conditional for:

```text
D_H/r_d and D_V/r_d,
```

because those inherit the radial clock-drift term:

```text
1 / (1 + dot_C/(2H)).
```

So the theorem is not yet a full parent result. It needs a radial drift bound or
a parent proof that BAO readout occurs in a saturated frame.

## 5. Leakage Tolerance

Using the actual DESI DR2 BAO covariance, the allowed common-mode leakage is
tight:

| `Delta chi2` threshold | max exponent mismatch in units of `B_mem/2` | max fractional BAO-ratio shift | approx `|dot_C/H|` bound |
|---:|---:|---:|---:|
| `1` | `0.07468250444495217` | `0.0027698476423345664` | `0.005539695284669133` |
| `4` | `0.14915900536592486` | `0.005539695284669133` | `0.011079390569338266` |
| `9` | `0.2234306361138072` | `0.008309542927003699` | `0.016619085854007398` |
| `25` | `0.3713637739597909` | `0.013849238211672832` | `0.027698476423345664` |

Readout:

```text
for Delta chi2 < 1, BAO allows only about a 0.277% global ratio leakage.
```

So common-mode cancellation cannot be vague. It has to be almost exact.

## 6. Failure Modes

| failure mode | consequence | verdict |
|---|---|---|
| denominator-only `r_d` rescaling | DESI DR2 scale-mode penalty huge | rejected |
| radial clock drift | moves `D_H/r_d` relative to `D_M/r_d` | must be bounded or derived |
| inhomogeneous `C` over survey volume | redshift/environment BAO shape distortion | open |
| independent `r_d` microphysics shift | ratio theorem incomplete | partially checked by CAMB smoke |
| free `alpha` treated as proof | empirical nuisance mistaken for theory | forbidden |

## 7. Theorem Contract

To promote the BAO route, the parent framework must provide:

| contract | current status |
|---|---|
| common late unit for `D_M`, `D_H`, `D_V`, and `r_d` | conditional pass |
| `dot_C/H` suppression for radial BAO distances | bounded, not derived |
| early sound-horizon coordinate microphysics | partial numeric support only |
| no anisotropic endpoint leakage | open shape hazard |
| BAO `alpha` owner | missing |

This is a fair position:

```text
BAO is not killing the endpoint-clock route,
but BAO is demanding a very tight common-mode theorem.
```

## 8. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| BAO ratio theorem algebra written | pass |
| naked half-memory leakage rejected | pass |
| common-mode cancellation tolerance quantified | pass |
| radial drift parent-derived | fail |
| BAO alpha parent-owned | fail |
| BAO support claim allowed | fail |

## 9. Decision

Decision:

```text
BAO_common_mode_ratio_theorem_conditional_radial_drift_and_alpha_owner_open
```

Meaning:

```text
The BAO common-mode ratio theorem can be written conditionally: homogeneous
conformal matter units cancel in D_X/r_d. This prevents the naked half-memory
BAO failure. But radial drift, r_d microphysics, and alpha ownership remain
open gates.
```

Current theory status:

```text
BAO route survives only as a conditional theorem target;
do not claim BAO support;
derive or bound radial drift and alpha ownership next.
```

Next target:

```text
198-BAO-radial-drift-and-alpha-owner-gate.md
```
