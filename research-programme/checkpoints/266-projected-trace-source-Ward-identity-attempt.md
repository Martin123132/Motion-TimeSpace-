# 266 - Projected Trace-Source Ward Identity Attempt

Private derivation checkpoint. This is not a public local-GR, CMB, BAO, or unified-field claim.

## Purpose

Checkpoint 265 narrowed the local-silence problem to:

```text
derive delta C_D / delta T_local = 0
```

or at least:

```text
delta C_D / delta T_local ~ (L_local/L_D)^3.
```

This checkpoint asks whether the projected trace-source equation gives exact local silence, volume suppression, or a no-go.

## Machine Artifact

Script:

```text
scripts/projected_trace_source_Ward_identity_attempt.py
```

Run:

```text
runs/20260601-000084-projected-trace-source-Ward-identity-attempt
```

Status:

```text
projected_trace_source_Ward_identity_volume_suppression_derived_exact_silence_not_derived
```

Claim ceiling:

```text
trace_projection_internal_only_no_local_GR_CMB_or_BAO_promotion
```

## Main Derivation

Start with the matter metric:

```text
tilde_g_munu = exp(C) g_munu.
```

Metric matter coupling gives the trace variation:

```text
delta S_m / delta C = 1/2 sqrt(-tilde_g) T_tilde.
```

Now split:

```text
C(x) = C_D + C_perp(x),
P_D[C_perp] = 0.
```

Variation gives two equations:

```text
P_D[E_C] + 1/2 P_D[sqrt(-tilde_g) T_tilde] = 0
```

and:

```text
(1-P_D)[E_C] + 1/2 (1-P_D)[sqrt(-tilde_g) T_tilde] = 0.
```

This is the key result:

```text
the projector alone does not annihilate the trace source.
```

It separates the source into:

```text
domain-average trace source -> C_D
local trace contrast -> C_perp.
```

So a projector is useful, but not magic.

## What Is Derived

### Volume Suppression

For a compact source with support scale `L` inside a coherent domain `L_D`, the coherent response is bounded like:

```text
delta C_D ~ B_mem (L/L_D)^3.
```

Using:

```text
L_D = c/H0 = 4440.711864908902 Mpc
B_mem = 2/27
```

the volume-suppressed response is:

| Probe | `B_mem (L/L_D)^3` | Local-safe? |
|---:|---:|---|
| Earth radius | `7.445255845809257e-60` | yes |
| Solar radius | `9.69444209842441e-54` | yes |
| `1 AU` | `9.639023679180706e-47` | yes |
| `1 pc` | `8.458793963504762e-31` | yes |
| `8 kpc` | `4.3309025093144393e-19` | yes |
| `150 Mpc` | `2.8548429626828576e-06` | yes |
| `300 Mpc` | `2.283874370146286e-05` | yes |
| `1000 Mpc` | `0.0008458793963504763` | no for local gate |

The local `Delta C` gate gives:

```text
L < 378.8638151894848 Mpc.
```

The stricter `q_R`-like proxy gives:

```text
L < 300.70440939223687 Mpc.
```

So volume suppression is genuinely strong for local systems and BAO-sized subdomains.

### Gradient Safety of `C_D`

Because:

```text
C_D = C_D(t)
```

the coherent response has:

```text
grad_i C_D = 0.
```

That means the zero-mode response does not create a local spatial fifth force by itself.

This is good.

## What Is Not Derived

The residual equation still contains:

```text
(1-P_D)[T_tilde].
```

So local trace contrast sources:

```text
C_perp
```

unless one of the following is derived:

```text
C_perp is constrained,
C_perp is very heavy/stiff,
Cperp response is volume-suppressed,
or the trace source is Ward-cancelled.
```

Therefore:

```text
exact local silence is not derived.
```

## Ward Identity Target

The clean exact route would be:

```text
sqrt(-tilde_g) T_tilde = nabla_mu J_W^mu + A_top[D].
```

Then compact stationary local sources could satisfy:

```text
integral_D nabla_mu J_W^mu = boundary flux = 0,
```

while coherent FLRW expansion could retain:

```text
A_top[D] != 0.
```

That would be a real projected trace-source Ward identity:

```text
local compact trace -> no coherent memory charge
FLRW boundary/topological class -> coherent memory charge
```

But this identity is not derived here.

It is now the precise theorem target.

## No-Go Clarification

This checkpoint rejects one tempting shortcut:

```text
Pi_D exists, therefore local matter does not source C.
```

False.

The correct statement is:

```text
Pi_D turns local trace into a tiny coherent average plus a residual contrast.
```

The coherent average is probably safe.

The residual contrast is the live danger.

## Drift Still Not Solved

Volume suppression does not solve late time drift.

The full rolling memory value:

```text
dot_C/H ~= B_mem = 0.07407407407407407
```

exceeds the imported BAO drift bound by:

```text
6.563575587525328.
```

So the branch still needs:

```text
late saturation / residual drift law.
```

## Gate Results

| Gate | Result |
|---|---|
| plain trace source annihilated by projector | fail |
| zero-mode volume suppression | conditional pass |
| spatial fifth force from `C_D` | conditional pass / absent |
| residual `C_perp` trace response | open |
| exact Ward identity | not derived |
| late drift safety | fail unless saturated |
| local-GR/CMB/BAO support claim | forbidden |

## Decision

Decision:

```text
projected_trace_source_Ward_identity_volume_suppression_derived_exact_silence_not_derived
```

Meaning:

```text
Variation of a projected C field proves the projector alone does not annihilate
local trace sources.
```

But:

```text
it does derive a useful volume-suppressed coherent zero-mode response, and
C_D has no spatial gradient.
```

The remaining local-GR burden is:

```text
derive C_perp suppression
or derive a Weyl/topological trace-current identity.
```

## Where This Leaves Us

This is not a kill shot against the local branch.

It is a cleaner map:

```text
C_D zero-mode:
  conditionally safe by volume suppression and no spatial gradient.

C_perp residual:
  not safe until parent-suppressed or Ward-cancelled.
```

So the next target is:

```text
derive_Cperp_response_operator_or_Weyl_topological_trace_current
```

If `Cperp` gets an owned suppression operator, local silence becomes a serious conditional theorem. If not, local silence stays closure-only.

## Validation

- Script compiles in `.venv-score`.
- Run completed and wrote `DONE.txt`.
- CSV outputs parse cleanly.
- Cited source paths exist.
- No changes were made to `formalization-workbench`.
- Claim ceiling remains internal only; no local-GR, CMB, or BAO promotion is allowed.
