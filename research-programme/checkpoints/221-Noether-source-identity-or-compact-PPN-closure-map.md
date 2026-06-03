# 221 - Noether Source Identity or Compact PPN Closure Map

Private theory checkpoint. This is not a public local-GR, PPN, galaxy, BAO,
CMB, or field-theory completion claim.

## 1. Trigger

Checkpoint 220 left the local branch here:

```text
J_rel exactness can kill integrated memory exchange conditionally,
but q_loc^nu = 0 still needs the source identity.
```

The target identity is:

```text
nabla_mu Khat^{mu nu} - nabla^nu Gamma_eff
= S_L^nu + d_rel J_rel^nu.
```

If this is derived, then in a compact vacuum collar with exact local `J_rel`:

```text
q_loc^nu = -P_loc(S_L^nu + d_rel J_rel^nu) = 0.
```

This checkpoint asks whether that identity can come from a parent variation
rather than being assumed to silence the local branch.

## 2. Machine Artifact

Script:

```text
scripts/Noether_source_identity_or_compact_PPN_closure_map.py
```

Run:

```text
runs/20260601-000038-Noether-source-identity-or-compact-PPN-closure-map
```

Command:

```text
python scripts/Noether_source_identity_or_compact_PPN_closure_map.py --timestamp 20260601-000038
```

Status:

```text
source_identity_parent_displacement_route_written_not_derived_PPN_closure_map_retained
```

Claim ceiling:

```text
conditional_source_identity_contract_no_local_GR_or_PPN_promotion
```

## 3. Main Result

There is a clean parent-variation route.

Introduce a genuine parent response/embedding field:

```text
X^nu.
```

Demand that the `X^nu` variation has the bulk form:

```text
delta S_X =
int sqrt(-g) [
  Khat^{mu nu} nabla_mu delta X_nu
  - Gamma_eff nabla_nu delta X^nu
  + (S_L^nu + d_rel J_rel^nu) delta X_nu
]
+ boundary.
```

Integrating by parts gives:

```text
delta S_X =
int sqrt(-g) [
  -nabla_mu Khat^{mu nu}
  + nabla^nu Gamma_eff
  + S_L^nu
  + d_rel J_rel^nu
] delta X_nu
+ boundary.
```

Then the `X^nu` Euler equation gives:

```text
nabla_mu Khat^{mu nu} - nabla^nu Gamma_eff
= S_L^nu + d_rel J_rel^nu.
```

So the identity is not mathematically mysterious. It can be derived if `Khat`
and `Gamma_eff` are conjugates of the same parent response field.

## 4. Why This Is Not Promotion

The current theory does not yet own:

```text
X^nu,
the constitutive parent L_X,
the compact-shell boundary primitive,
the no-extra-local-hair degree count,
the PPN response coefficients.
```

So this is an exact action-class template, not a completed MTS parent theorem.

The hard danger is:

```text
the field introduced to derive local silence could itself create local PPN
hair.
```

Therefore `X^nu` must be:

```text
constrained,
gauge,
auxiliary,
high-mass,
topological,
or otherwise locally nonpropagating.
```

That is the next thing to prove.

## 5. Boundary and Bianchi Conditions

The variation produces a boundary term:

```text
n_mu (Khat^{mu nu} - Gamma_eff g^{mu nu}) delta X_nu.
```

This must be:

```text
fixed,
cancelled,
or carried by the explicit relative boundary primitive.
```

It cannot be dropped.

For Bianchi safety, the metric variation must retain:

```text
T_X
T_source
T_rel
T_projector
T_boundary.
```

Otherwise the source identity can look conserved only because an auxiliary
stress was thrown away. That would be fake conservation.

## 6. Compact PPN Closure Vector

Because the parent `X^nu` sector is not yet derived, the local result remains a
closure map.

The compact leakage variable is:

```text
epsilon_J = |P_loc d_rel J_rel|.
```

From checkpoint 220, the hard bound is:

```text
epsilon_J < 7.432631961576971e-06
```

at the worst compact case, `solar_Mercury_shell`.

The closure residual vector is:

| residual | closure form | status |
|---|---|---|
| `q_loc_source` | `q_proxy + epsilon_J` | bounded closure |
| `gamma - 1` | `c_gamma epsilon_J` | coefficient not derived |
| `beta - 1` | `c_beta epsilon_J` | coefficient not derived |
| `Phi - Psi` | `c_slip epsilon_J` | coefficient not derived |
| `G_eff/G - 1` | `c_G epsilon_J` | coefficient not derived |
| `alpha_clock` | `c_clock epsilon_J` | coefficient not derived |
| `epsilon_matter` | `c_matter epsilon_J` | coefficient not derived |

For the worst compact case, a unit response gives:

```text
epsilon_J / q_gate = 0.3231579113729118.
```

That is not a PPN proof. It only says the current closure budget has positive
room if the unowned response coefficients are order-unity or smaller.

## 7. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| source identity derivation route written | conditional pass |
| source identity derived in current parent theory | fail |
| boundary leakage removed | fail |
| Bianchi-safe stress accounting stated | conditional pass |
| new local vector/scalar hair excluded | fail |
| compact q-like closure map positive | pass |
| PPN residual coefficients derived | fail |
| local GR or PPN promoted | fail |

## 8. Decision

Decision:

```text
source_identity_parent_displacement_route_written_not_derived_PPN_closure_map_retained
```

Meaning:

```text
the source identity has a real derivation template:
make Khat and Gamma_eff conjugates of a common parent response field X^nu.
```

But:

```text
the actual parent X-sector, boundary primitive, local degree count, and PPN
response coefficients are not derived.
```

So the local branch has improved again:

```text
the missing identity is now localized to a precise action sector.
```

But it still does not promote:

```text
local GR remains a closure-bounded theorem target.
```

## 9. Next Target

Create:

```text
222-parent-X-sector-degree-count-and-boundary-action.md
```

Purpose:

```text
try to make X^nu a nonpropagating/gauge/auxiliary parent field and attach the
boundary primitive without creating a new local PPN degree of freedom.
```

Pass condition:

```text
X^nu derives the source identity,
its boundary term is owned,
and its local propagating degree count is zero or screened.
```

Fail condition:

```text
X^nu becomes a new vector/scalar hair that fixes q_loc algebra while breaking
PPN physics.
```
