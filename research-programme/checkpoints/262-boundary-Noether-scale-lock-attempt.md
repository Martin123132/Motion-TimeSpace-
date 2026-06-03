# 262 - Boundary/Noether Scale-Lock Attempt

Private derivation checkpoint. This is the promised one serious attempt at:

```text
derive H_star = H0
```

from a boundary, Noether, or global scale-lock mechanism.

Result:

```text
H_star = H0 is not parent-derived.
```

It is now closure-locked unless new boundary equations are introduced.

## 1. Trigger

Checkpoint 261 found:

```text
B_mem = q (H_star/H0)^2
```

is a clean geometric identity.

For:

```text
q = 2/27,
```

the fixed branch follows if:

```text
H_star = H0.
```

But 261 did not derive that equality. This checkpoint gives the boundary and
Noether routes one fair attempt.

## 2. Machine Artifact

Script:

```text
scripts/boundary_Noether_scale_lock_attempt.py
```

Run:

```text
runs/20260601-000080-boundary-Noether-scale-lock-attempt
```

Command:

```text
python scripts/boundary_Noether_scale_lock_attempt.py --timestamp 20260601-000080
```

Status:

```text
boundary_Noether_scale_lock_not_derived_Hstar_equals_H0_closure_locked_for_now
```

Claim ceiling:

```text
scale_lock_closure_only_no_Bmem_parent_amplitude_promotion
```

## 3. Boundary/York-Time Route

The natural boundary variable is mean curvature:

```text
K_boundary / 3 = H_boundary.
```

So a boundary action could impose:

```text
H_star = K_D / 3.
```

This is meaningful. It would make `H_star` equal a domain expansion variable.

But to get:

```text
H_star = H0,
```

the parent theory must also derive:

```text
K_D = 3 H0.
```

Right now that is the present-domain boundary value, not a parent-selected
number.

So this route gives:

```text
H_star = H_D(now)
```

as a possible closure, not:

```text
H_D(now) = H0
```

as a theorem.

## 4. Noether Route

A Noether or dilation charge can have the form:

```text
Q_D = a pi_a + memory/projector terms.
```

or some time-translation/domain charge:

```text
Q_T = constant.
```

This can relate:

```text
expansion,
boundary volume,
memory canonical data,
projector charge.
```

But the crucial limitation is:

```text
dQ/dt = 0
```

does not select the numerical value of `Q`.

Noether conservation preserves boundary data. It does not choose:

```text
H0.
```

So the Noether route is not empty, but it is not yet a scale-lock theorem.

## 5. Global Constraint Route

A global/sequestering-style route could impose:

```text
H_star^2 = <H^2>_W.
```

That would be attractive because `H_star` would be a global/domain zero-mode,
which is good for local silence.

But it predicts a weighted historical average, not necessarily:

```text
H0^2.
```

To recover the fixed branch, it still needs a theorem:

```text
<H^2>_W = H0^2.
```

No such theorem exists here.

## 6. No-Go Lemmas

This checkpoint adds five no-go statements:

```text
Noether conservation not selection:
  charges are conserved, not numerically chosen.

York-time boundary data no-go:
  K/3=H0 on the present slice is the observed boundary expansion.

F_zero boundary no-go:
  F(0)=0 removes memory amplitude from the present Friedmann constraint.

Global average not present value:
  <H^2>_W is not generically H0^2.

Local silence blocks local scale field:
  a local trace-coupled scale-lock field would be sourced by matter.
```

These are enough to stop this route becoming circular.

## 7. Sufficient Theorem Contract

For a real theorem, the parent action would need:

```text
S1: boundary/domain canonical pair (V_D, K_D)
    and memory pair (H_star, Q_mem).

S2: variation gives H_star = K_D/3
    with no independent scale or fit coefficient.

S3: parent equations select K_D = 3H0
    rather than accepting it as observational boundary data.

S4: H_star is a global/domain zero-mode
    with no local trace response or fifth force.

S5: boundary, memory, projector, and matter stresses are retained
    so total stress is Bianchi-safe.
```

The hard missing condition is:

```text
S3_parent_selects_present_domain.
```

Without S3, the route is a closure condition.

## 8. Branch Policy

The branch policy is now:

```text
strict lead closure:
  B_mem = (2/27)(H_star/H0)^2 with H_star=H0 imposed.
  Allowed as closure, not parent-derived.

kappa ablation:
  B_mem = kappa_mem(2/27).
  Allowed as diagnostic only.
  258 says it does not pay AIC/BIC tax.

future boundary theorem:
  H_star=K_D/3=H0 from parent equations.
  Not available yet.

global average branch:
  H_star^2=<H^2>_W.
  Future route, but not equivalent to fixed 2/27 unless <H^2>_W=H0^2.
```

## 9. Decision

Decision:

```text
boundary_Noether_scale_lock_not_derived_Hstar_equals_H0_closure_locked_for_now
```

Meaning:

```text
the boundary/Noether route gives a precise theorem target,
but not the theorem.
```

Allowed:

```text
H_star=H0 is a disciplined closure condition.
fixed 2/27 remains the clean lead branch.
```

Forbidden:

```text
H_star=H0 is derived,
kappa_mem=1 is proved,
B_mem=2/27 is parent-owned.
```

## 10. Pivot

We should stop repeating scale-lock unless new boundary equations are supplied.

Next useful targets are:

```text
rank-27/rank-2 cell theorem,
CMB bridge/readiness,
perturbation parent bridge,
local-GR N6/no-hair.
```

My recommendation:

```text
pivot to a CMB bridge/readiness gate or rank-27/rank-2 theorem,
while keeping H_star=H0 explicitly closure-locked.
```

Reason:

```text
the scale-lock route is now sharp enough to preserve,
but not productive enough to keep circling without new ingredients.
```
