# 268 - Projected Matter Metric Parent Action or Closure

Private derivation checkpoint. This is not a public local-GR, CMB, BAO, or unified-field claim.

## Purpose

Checkpoint 267 found the cleanest local-silence branch so far:

```text
S_matter[psi, exp(P_D C) g_munu]
```

instead of:

```text
S_matter[psi, exp(C) g_munu].
```

This checkpoint asks the hard question:

```text
Can that projected matter metric be parent-owned,
or is it just a nonlocal closure chosen because it helps?
```

## Machine Artifact

Script:

```text
scripts/projected_matter_metric_parent_action_or_closure.py
```

Run:

```text
runs/20260601-000086-projected-matter-metric-parent-action-or-closure
```

Status:

```text
projected_matter_metric_parent_action_skeleton_conditional_nonlocal_selector_not_derived
```

Claim ceiling:

```text
projected_matter_metric_parent_skeleton_internal_only_no_local_GR_or_unification_promotion
```

## Parent-Action Skeleton

The projected metric can be written as an action skeleton using auxiliary variables:

```text
C = C_D + Cperp
P_D[Cperp] = 0
C_m = C_D
bar_g_munu = exp(C_m) g_munu
S_matter = S_matter[psi, bar_g_munu].
```

Schematic constraint terms:

```text
lambda_Pi (C - C_D - Cperp)
Lambda_D integral_D sqrt(h) W_D Cperp
lambda_m (C_m - C_D)
Lambda_bar^{munu} (bar_g_munu - exp(C_m) g_munu)
```

Then matter couples to:

```text
bar_g_munu = exp(C_D) g_munu
```

not:

```text
exp(C_D + Cperp) g_munu.
```

## Main Result

In this skeleton:

```text
delta S_matter / delta Cperp = 0.
```

So the dangerous local trace-source term:

```text
(1-P_D)[sqrt(-tilde_g) T]
```

is removed from the matter coupling.

This is stronger than:

```text
Cperp is heavy,
Cperp is tiny,
Cperp is locally plateaued.
```

It says:

```text
Cperp is not in the matter metric.
```

That is a clean action-level skeleton.

## What Is Actually Gained

| Item | Result |
|---|---|
| projected matter metric can be action-written | conditional pass |
| direct `Cperp` matter source | removed in skeleton |
| universal matter ruler metric | contract |
| local composition force from `Cperp` | absent if universal `bar_g` holds |
| Bianchi accounting | conditional if all selector/projector/domain stresses are retained |

The important variation audit is:

```text
ordinary exp(C)g:
  delta_Cperp S_matter = 1/2 (1-P_D)[sqrt(-tilde_g)T]

projected exp(P_D C)g:
  delta_Cperp S_matter = 0
```

So the algebra is good.

## What Is Not Yet Derived

The skeleton still chooses:

```text
C_m = P_D C
```

as the matter metric scalar.

That is the unresolved physics.

The missing parent principle must explain why matter sees:

```text
the domain-zero representative
```

instead of:

```text
the raw local conformal field.
```

Until that is derived, this branch is:

```text
action-writeable,
conditionally coherent,
but not parent-derived.
```

## Closure Risks

| Risk | Why it matters |
|---|---|
| nonlocal matter coupling | `S_matter` depends on a domain projection |
| equivalence-principle composition | all species must see one universal `bar_g` |
| hidden conservation failure | selector/projector/domain stresses cannot be dropped |
| domain-scale tuning | `L_D` must not be picked from BAO/local success |
| local microcausality | `C_D` must be a constraint/boundary zero mode, not instant signalling |
| late drift | projected metric does not suppress `dot_C_D/H` |
| amplitude scale-lock | `B_mem=2/27`, `Hstar=H0` remain closure/theorem targets |

## Decision

Decision:

```text
projected_matter_metric_parent_action_skeleton_conditional_nonlocal_selector_not_derived
```

Meaning:

```text
A parent-action skeleton can encode the projected matter metric using auxiliary
fields C_m and bar_g, and in that skeleton delta S_matter/delta Cperp is
exactly zero.
```

But:

```text
the principle selecting exp(P_D C)g as the universal matter metric is still
missing.
```

Therefore this is not yet a theorem.

## Current Theory Status

This is a real improvement:

```text
local trace-source problem:
  no longer algebraically fatal.
```

But the burden has moved:

```text
derive metric selector principle,
or demote projected matter metric to explicit closure.
```

The local branch is now in better shape than before because we have a precise action contract rather than a vague screening wish.

It still cannot be promoted to derived local GR.

## Next Target

The next derivation should try one of:

```text
1. quotient/gauge-representative route:
   Cperp is unphysical for matter; only P_D C is matter-gauge-invariant.

2. cohomology/relative-class route:
   compact local Cperp is exact, while domain C_D is the observable class.

3. boundary-clock route:
   matter clocks couple to boundary-normalized domain time, not local residual memory.
```

If none of those works, write the closure explicitly:

```text
projected matter metric is an imposed effective coupling.
```

## Claim Gates

| Gate | Result |
|---|---|
| action can encode projected metric | conditional pass |
| `delta S_matter / delta Cperp = 0` | conditional pass |
| projected metric parent principle | not derived |
| Bianchi accounting | conditional pass if all stresses retained |
| local equivalence principle | conditional pass |
| domain selector and scale | open |
| late drift and amplitude | open |
| local-GR/unification promotion | forbidden |

## Validation

- Script compiles in `.venv-score`.
- Run completed and wrote `DONE.txt`.
- CSV outputs parse cleanly.
- Cited source paths exist.
- No changes were made to `formalization-workbench`.
- Claim ceiling remains internal only; no local-GR or unification promotion is allowed.
