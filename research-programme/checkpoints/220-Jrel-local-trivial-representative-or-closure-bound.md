# 220 - Jrel Local Trivial Representative or Closure Bound

Private theory checkpoint. This is not a public local-GR, PPN, galaxy, BAO,
CMB, or field-theory completion claim.

## 1. Trigger

Checkpoint 219 reduced the compact local route to:

```text
q_loc^nu = -P_loc(S_L^nu + d_rel J_rel^nu)
```

provided the missing Noether/source identity exists.

In a compact vacuum collar:

```text
S_L^nu = 0.
```

So the next pressure point is:

```text
Can J_rel be forced to the local trivial representative without declaring a
plateau by hand?
```

## 2. Machine Artifact

Script:

```text
scripts/Jrel_local_trivial_representative_or_closure_bound.py
```

Run:

```text
runs/20260601-000037-Jrel-local-trivial-representative-or-closure-bound
```

Command:

```text
python scripts/Jrel_local_trivial_representative_or_closure_bound.py --timestamp 20260601-000037
```

Status:

```text
Jrel_local_trivial_representative_conditional_exactness_missing_closure_bound_retained
```

Claim ceiling:

```text
Jrel_exactness_attempt_no_local_GR_or_PPN_promotion
```

## 3. Main Result

The cheating route is rejected:

```text
set J_rel = 0 in local shells by definition.
```

That would just be the forbidden plateau axiom wearing a fake moustache.

The best non-cheating route is:

```text
J_rel = d_rel A_rel
```

in the projected memory-exchange sector, with:

```text
A_rel|inner boundary = A_rel|outer boundary = 0
```

or matching pure-gauge boundary data.

Then Stokes gives zero integrated memory exchange through a stationary compact
collar.

But this is only conditional, because the parent action has not yet forced:

```text
J_rel = d_rel A_rel,
the compact-shell boundary primitive,
pointwise P_loc d_rel J_rel^nu = 0.
```

So the local trivial representative is not derived today.

## 4. Important Separation

`J_rel` cannot be ordinary gravitational/Gauss flux.

A solar-system shell has ordinary gravitational flux because it encloses mass.
If `J_rel` tracks that flux, then local triviality fails immediately and the
PPN branch is in trouble.

So the required interpretation is narrower:

```text
J_rel = memory/domain-exchange current,
not the Newtonian/GR mass flux.
```

That is a contract requirement, not yet a parent theorem.

## 5. Conditional Lemma

The conditional route is now sharp:

```text
J_rel = d_rel A_rel
A_rel boundary data vanish or match pure gauge
stationary compact collar
J_rel projects only memory/domain exchange
Noether/source identity holds
```

Then:

```text
P_loc d_rel J_rel^nu = 0
```

and:

```text
q_loc^nu = 0.
```

But the actual result is weaker:

```text
integrated exchange can be killed conditionally;
pointwise local PPN silence is not derived.
```

That distinction matters. Integrated zero is not the same as a local GR limit.

## 6. Closure Bound Retained

Because the representative is not derived, the fallback is a named leakage
bound:

```text
|P_loc d_rel J_rel| < remaining compact q_R-like budget.
```

From checkpoint 219:

| compact case | max allowed `|P_loc d_rel J_rel|` |
|---|---:|
| `solar_1AU_shell` | `1.3314422519346338e-05` |
| `solar_Mercury_shell` | `7.432631961576971e-06` |
| `earth_GPS_shell` | `2.1740257329151147e-05` |

Worst compact bound:

```text
7.432631961576971e-06.
```

That is now the hard cage. Any unmodelled local `J_rel` leakage bigger than
that breaks the current compact-shell q-like gate.

## 7. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| formal `J_rel` object exists | pass |
| zero by declaration avoided | pass |
| exact local representative parent-derived | fail |
| closed non-exact local class excluded | fail |
| ordinary gravity flux separated from `J_rel` | conditional pass |
| integrated exchange killed by Stokes | conditional pass |
| pointwise `P_loc d_rel J_rel^nu = 0` derived | fail |
| closure leakage bounds positive | pass |
| local GR or PPN promoted | fail |

## 8. Decision

Decision:

```text
Jrel_local_trivial_representative_conditional_exactness_missing_closure_bound_retained
```

Meaning:

```text
local J_rel silence can be made mathematically clean if the current is exact in
the local memory sector and the compact-shell boundary primitive is selected by
the parent theory.
```

But:

```text
the exact representative, boundary primitive, pointwise projector annihilation,
and Noether/source identity are not derived.
```

So the local branch improves, but does not promote.

Current status:

```text
local route is live as a theorem target;
local q_loc silence remains closure-bounded;
no local-GR or PPN claim is allowed.
```

## 9. Next Target

Create:

```text
221-Noether-source-identity-or-compact-PPN-closure-map.md
```

Purpose:

```text
either derive the Noether/source identity that converts exact J_rel into
q_loc^nu = 0, or map the compact-shell leakage bound into an explicit PPN
residual closure vector.
```

Pass condition:

```text
nabla_mu Khat^{mu nu}-nabla^nu Gamma_eff = S_L^nu + d_rel J_rel^nu
```

is obtained from a parent variation with all auxiliary/boundary stresses
retained.

Fail condition:

```text
the identity is simply assumed to make the local branch quiet.
```
