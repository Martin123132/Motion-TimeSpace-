# 267 - Projected Matter Metric and `Cperp` Decoupling Attempt

Private derivation checkpoint. This is not a public local-GR, CMB, BAO, or unified-field claim.

## Purpose

Checkpoint 266 found the live obstruction:

```text
(1-P_D)[T_tilde]
```

still sources:

```text
Cperp
```

if matter couples to the ordinary local conformal field:

```text
tilde_g_munu = exp(C_D + Cperp) g_munu.
```

This checkpoint tests a cleaner branch:

```text
matter couples to the projected coherent mode P_D C = C_D,
not to the residual local contrast Cperp.
```

## Machine Artifact

Script:

```text
scripts/projected_matter_metric_Cperp_decoupling_attempt.py
```

Run:

```text
runs/20260601-000085-projected-matter-metric-Cperp-decoupling-attempt
```

Status:

```text
projected_matter_metric_exact_Cperp_matter_decoupling_conditional_parent_projector_coupling_missing
```

Claim ceiling:

```text
projected_matter_metric_internal_only_no_local_GR_CMB_or_BAO_promotion
```

## Main Result

The ordinary local matter metric is now rejected as the lead local-silence route:

```text
tilde_g_munu = exp(C_D + Cperp) g_munu
```

because:

```text
delta S_m / delta Cperp
= 1/2 (1-P_D)[sqrt(-tilde_g) T_tilde].
```

That directly sources the residual mode.

The cleaner branch is:

```text
tilde_g_munu = exp(P_D C) g_munu = exp(C_D) g_munu.
```

Then:

```text
delta C_m / delta Cperp = P_D[delta Cperp] = 0
```

and therefore:

```text
delta S_matter / delta Cperp = 0.
```

This is the strongest local-silence move so far:

```text
Cperp is not matter-sourced if matter couples only to the projected coherent metric.
```

## What This Buys

| Issue | Result |
|---|---|
| local trace contrast sourcing `Cperp` | removed conditionally |
| coherent `C_D` local spatial force | absent if `partial_i C_D = 0` |
| compact local source contribution to `C_D` | volume-suppressed |
| BAO same-domain ruler cancellation | preserved |
| CMB endpoint contrast | preserved if endpoint selector is derived |

The BAO cancellation still works:

```text
tilde_D_X / tilde_r_BAO
= exp(C_D/2) D_X / [exp(C_D/2) r_BAO]
= D_X / r_BAO.
```

And the CMB endpoint contrast still has:

```text
exp((C_D,obs - C_D,emit)/2).
```

So this route does not destroy the useful bridge structure.

## Residual Coupling Bound

If matter couples to:

```text
exp(C_D + epsilon Cperp) g_munu,
```

then the residual coupling must satisfy:

| Gate | Max `epsilon` |
|---|---:|
| local `Delta C` gate | `0.000621` |
| local `q_R`-like gate | `0.0003105` |
| BAO `Delta C` gate | `0.07478588634303329` |
| BAO `dot_C/H` gate | `0.15235598138011708` |

So the branch really wants:

```text
epsilon = 0
```

or a parent-derived suppression at least at the `10^-4` level locally.

## What Is Still Not Derived

This checkpoint moves the burden, but it does not erase it.

The required parent contract is:

```text
S_matter[psi, exp(P_D C) g_munu],
not
S_matter[psi, exp(C) g_munu].
```

That must be derived from the parent theory.

Otherwise it is just a nonlocal coupling chosen because it helps.

The remaining contracts are:

| Contract | Status |
|---|---|
| projector before matter coupling | new conditional contract |
| projector is variational | previous conditional pass |
| universal projected matter metric | contract, not derived |
| all domain/projector stresses retained | previous conditional pass |
| endpoint/same-domain selector | open |
| late drift saturation | open |
| `B_mem = 2/27`, `Hstar = H0` | not derived |

## Why This Is Better Than A Plateau Axiom

A plateau axiom would say:

```text
Cperp = 0 locally.
```

This branch says something sharper:

```text
local matter never couples to Cperp in the first place;
matter couples only to the coherent projected metric.
```

That is a possible action-level rule, not just a local patch.

But it is still not a theorem until the parent action explains why the matter metric uses:

```text
P_D C
```

instead of:

```text
C.
```

## Gate Results

| Gate | Result |
|---|---|
| ordinary `exp(C)` matter metric | fail as lead |
| projected `exp(P_D C)` matter metric | conditional pass |
| `delta S_m/delta Cperp = 0` | conditional pass |
| local force from `C_D` | conditional pass |
| universal late matter rulers | conditional pass |
| parent origin of projected coupling | open |
| late drift saturation | open |
| local-GR/CMB/BAO support claim | forbidden |

## Decision

Decision:

```text
projected_matter_metric_exact_Cperp_matter_decoupling_conditional_parent_projector_coupling_missing
```

Meaning:

```text
If matter couples to exp(P_D C)g rather than exp(C)g, the dangerous residual
mode Cperp is not matter-sourced: delta S_m/delta Cperp = 0.
```

This is cleaner than:

```text
huge local mass,
hand plateau,
or pretending the projector alone kills the trace source.
```

But:

```text
the projected matter metric, domain selector, Bianchi stresses, and drift law
are not yet parent-derived.
```

## Where This Leaves Us

This is a meaningful improvement to the local branch.

Before:

```text
Cperp was directly trace-sourced.
```

Now the best branch is:

```text
Cperp is not in the matter metric.
```

The next target is therefore:

```text
derive_projected_matter_metric_from_parent_action_or_reject_as_nonlocal_closure
```

If this can be derived, local silence becomes a serious conditional theorem. If not, this becomes an explicit closure rule.

## Validation

- Script compiles in `.venv-score`.
- Run completed and wrote `DONE.txt`.
- CSV outputs parse cleanly.
- Cited source paths exist.
- No changes were made to `formalization-workbench`.
- Claim ceiling remains internal only; no local-GR, CMB, or BAO promotion is allowed.
