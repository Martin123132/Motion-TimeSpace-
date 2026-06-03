# 211 - GK Parent Metric Ward Identity Attempt

Private theory checkpoint. This is not a public local-GR, galaxy, BAO, CMB, or
field-theory completion claim.

## 1. Trigger

Checkpoint 210 made the best current move:

```text
G_K^2[D] = ||Xi_D||_M^2.
```

That freezes:

```text
alpha_K = 1
```

if `G_K` is a canonical norm.

But that simply moves the hard question into:

```text
M_AB.
```

This checkpoint asks whether a Ward identity or parent norm can derive `M_AB`.

## 2. Machine Artifact

Script:

```text
scripts/GK_parent_metric_Ward_identity_attempt.py
```

Run:

```text
runs/20260601-000028-GK-parent-metric-Ward-identity-attempt
```

Command:

```text
python scripts/GK_parent_metric_Ward_identity_attempt.py --timestamp 20260601-000028
```

Status:

```text
GK_metric_Ward_identity_partial_flow_block_only_composite_metric_fixed_closure
```

Claim ceiling:

```text
GK_metric_partial_no_parent_norm_promotion
```

## 3. What Was Actually Derived

The flow/kinematic block has partial geometric ownership.

Using the domain congruence, the extrinsic/flow tensor can be decomposed into:

```text
expansion dispersion,
shear,
vorticity.
```

An ADM/DeWitt-style norm gives a natural metric for this block:

```text
||delta K||^2 ~ variance(theta) + sigma^2
```

up to trace convention and sign choices.

Raychaudhuri also supports the physical interpretation:

```text
shear and expansion dispersion break coherent FLRW transport.
```

So the flow part of `G_K` is not arbitrary in the same way a fitted coefficient
would be.

## 4. What Did Not Derive

The full composite metric still does not follow from one parent Ward identity.

The pieces are heterogeneous:

| piece | status |
|---|---|
| flow dispersion/shear/vorticity | partial geometric ownership |
| Weyl curvature | natural scalar norm, coefficient not derived |
| relative current `J_rel` | Hodge norm possible, representative missing |
| load anisotropy `Q` | MTS-native but owner/normalization incomplete |
| cross terms | set to zero only by minimal closure policy |

The missing theorem would need:

```text
M_AB = partial_A partial_B V_defect | FLRW
```

or an equivalent Ward/current norm.

That is not currently in the corpus.

## 5. Fixed Closure That Survives This Pass

The honest fixed branch is:

```text
M_AB = diag(1,1,1,1)
```

after canonical inverse-length normalization of each block.

This means:

```text
L_cg^-2 = L_H^-2 + G_K^2
```

with no free `alpha_K`.

But:

```text
unit diagonal metric is closure, not parent derivation.
```

## 6. Beta Sensitivity Warning

The script checked how dangerous hidden metric weights would be.

Key beta ceilings before named gates are hit:

| branch | `beta_max` before gate | unit beta safe? |
|---|---:|---|
| smooth BAO late domain | `19.78645552864463` | yes |
| Gpc transition domain | `0.19786455528644634` | no |
| BAO-scale transition | `0.0044519524939450415` | no |
| solar-system 1AU Weyl | `5.639032956009601` | yes |
| Earth-surface Weyl | `79.95976807722626` | yes |

This is useful:

```text
unit Weyl/flow closure can be locally safe in the illustrative solar/Earth
readouts, but transition-scale G_K cannot be treated as a smooth BAO branch.
```

That is exactly the kind of guardrail we want.

## 7. Exact Future Parent Contract

A future parent action must satisfy all of this:

| clause | requirement |
|---|---|
| `P1` | derive the domain congruence `u_D^mu` and domain `D` |
| `P2` | derive `Xi_D` as projections of one coherent defect operator |
| `P3` | derive `M_AB` as a Hessian or Ward/current norm |
| `P4` | prove cross terms vanish, or include them before scoring |
| `P5` | vary `Xi_D` and `M_AB` into the stress/Bianchi accounting |
| `P6` | freeze the metric before empirical scoring |

Until that exists, the route remains disciplined closure.

## 8. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| flow block partially derived | partial pass |
| Weyl block parent-normalized | fail |
| `J_rel` representative derived | fail |
| `Q` load metric derived | fail/open |
| single Ward identity for `M_AB` | fail |
| unit diagonal metric safe as predeclared closure | conditional pass |
| Bianchi/stress variation derived | fail |

## 9. Decision

Decision:

```text
GK_metric_Ward_identity_partial_flow_block_only_composite_metric_fixed_closure
```

Meaning:

```text
the flow block has partial geometric ownership, but the full composite G_K
metric is not parent-derived.
```

So:

```text
alpha_K remains frozen as closure,
M_AB remains fixed diagonal closure,
and no promotion is allowed.
```

## 10. Next Target

Next target:

```text
212-composite-GK-local-BAO-galaxy-safety-gate.md
```

The next question is practical and ruthless:

```text
Does the fixed composite G_K closure preserve local suppression, BAO smoothness,
and galaxy viability at the same time?
```
