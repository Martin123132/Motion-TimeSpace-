# 249 - Projector Boundary-Only Condition or Metric-Only Reduction Fail

Private local-derivation checkpoint. This is not a public beta, PPN, local-GR,
or field-theory completion claim.

## 1. Trigger

Checkpoint 248 split `N5_projector_stress` into a hard fork:

```text
T_projector = 0,
T_projector is boundary-only,
bulk T_projector remains,
or T_projector is wrongly dropped.
```

For local GR, only the first two are allowed.

This checkpoint tests the boundary-only route.

## 2. Machine Artifact

Script:

```text
scripts/projector_boundary_only_condition_or_metric_only_reduction_fail.py
```

Run:

```text
runs/20260601-000066-projector-boundary-only-condition-or-metric-only-reduction-fail
```

Command:

```text
python scripts/projector_boundary_only_condition_or_metric_only_reduction_fail.py --timestamp 20260601-000066
```

Status:

```text
projector_boundary_only_condition_not_derived_bulk_projector_stress_blocks_metric_only_EH_no_promotion
```

Claim ceiling:

```text
N5_boundary_only_not_derived_metric_only_EH_blocked_no_beta_or_local_GR_promotion
```

## 3. Boundary-Only Condition

For projector stress to be compatible with metric-only EH, the bulk exterior
variation must vanish:

```text
delta S_projector|bulk = 0.
```

Any remaining variation must be a well-posed boundary term:

```text
delta S_projector = delta S_boundary on partial E.
```

This requires:

```text
P_mem J_rel = d_rel A_rel
```

with pure-gauge/boundary-only support,

```text
delta_g P_mem|bulk = 0,
delta_g B|bulk = 0,
```

and:

```text
delta Pi_M,
delta Pi_TF,
delta Pi_matter
```

either vanish or have owned boundary stress ledgers.

## 4. Verdict

The boundary-only route is:

```text
not derived.
```

Reason:

```text
exact relative memory helps,
but it does not prove the projector metric and projector variation have no
bulk support.
```

The current corpus has:

```text
P_mem J_rel exactness as a conditional topology gate,
but not parent ownership of delta_g P_mem|bulk = 0,
not parent ownership of delta_g B|bulk = 0,
and not parent selection of A_rel as pure boundary gauge.
```

So:

```text
metric-only EH reduction remains blocked by N5.
```

## 5. Metric-Only Fork

| case | result |
|---|---|
| `T_projector = 0` | EH route can continue |
| `T_projector` boundary-only | EH route can continue with boundary term |
| bulk `T_projector` present | modified exterior, not vacuum EH |
| `T_projector` dropped | fake conservation, forbidden |

This is the cleanest status:

```text
bulk projector stress is not a harmless detail.
```

It changes the exterior equation to:

```text
G_mu_nu + Lambda g_mu_nu = 8 pi G T_projector_mu_nu.
```

That is not metric-only vacuum EH.

## 6. What Improved

Before this checkpoint:

```text
N5 said projector stress must be zero or retained.
```

After this checkpoint:

```text
N5 says metric-only EH requires projector stress to be zero or boundary-only.
```

If projector stress is bulk, the local branch becomes:

```text
modified exterior theory,
not local GR.
```

That is not a collapse of MTS as a broad programme.

It is a strict block on the local-GR promotion route.

## 7. What Still Fails

Still not derived:

```text
T_projector|bulk = 0,
A_rel pure-gauge boundary representative,
metric-independent/topological projector variation,
parent boundary symplectic metric.
```

Therefore:

```text
beta = 1 is not promoted,
metric-only EH is not promoted,
local GR is not promoted.
```

## 8. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| boundary-only condition written | pass |
| projector stress boundary-only derived | fail |
| metric-only EH reduction cleared | fail |
| metric-only reduction fail condition recorded | pass |
| local GR or PPN promoted | fail |

## 9. Decision

Decision:

```text
projector_boundary_only_condition_not_derived_bulk_projector_stress_blocks_metric_only_EH_no_promotion
```

Meaning:

```text
exact relative memory is not enough. To keep local GR, projector stress must
have no bulk exterior support. That condition is not parent-derived yet.
```

Main gain:

```text
we now know the exact N5 obstruction to metric-only EH.
```

Main failure:

```text
boundary-only projector stress is not derived.
```

## 10. Next Target

Create:

```text
250-local-GR-gate-scorecard-and-test-readiness.md
```

Purpose:

```text
summarize the local-GR branch after N1-N6 pressure: which gates are conditional,
which are open blockers, and which empirical local-bound tests can be run only
as closure/proxy checks.
```

Pass condition:

```text
no local-GR claim is made,
but the remaining theorem/test queue is explicit and ranked.
```

Fail condition:

```text
the branch is called solved, dead, or empirically passed without parent gates.
```
