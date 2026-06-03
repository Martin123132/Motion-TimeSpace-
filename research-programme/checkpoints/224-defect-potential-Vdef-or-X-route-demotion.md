# 224 - Defect Potential Vdef or X-Route Demotion

Private theory checkpoint. This is not a public local-GR, PPN, galaxy, BAO,
CMB, or field-theory completion claim.

## 1. Trigger

Checkpoint 223 found the cleanest local source-identity route:

```text
X_nu is a pure multiplier,
P^{mu nu}=P^{mu nu}[Y] is composite in parent fields,
C_X^nu=-nabla_mu P[Y]^{mu nu}+J_eff[Y]^nu approx 0.
```

But this only works if:

```text
P^{mu nu}
```

is actually parent-owned.

The exact target was:

```text
P^{mu nu} = partial V_def(Y,Z) / partial Z_{mu nu}.
```

This checkpoint asks:

```text
Can V_def and Z_{mu nu} be built from existing MTS blocks, or must the X route
be demoted to closure support?
```

## 2. Machine Artifact

Script:

```text
scripts/defect_potential_Vdef_or_X_route_demotion.py
```

Run:

```text
runs/20260601-000041-defect-potential-Vdef-or-X-route-demotion
```

Command:

```text
python scripts/defect_potential_Vdef_or_X_route_demotion.py --timestamp 20260601-000041
```

Status:

```text
Vdef_composite_candidate_partial_trace_flow_owned_X_route_demoted_to_closure_support
```

Claim ceiling:

```text
Vdef_contract_only_X_source_identity_support_no_local_GR_promotion
```

## 3. Main Result

A free new `V_def` is rejected.

This route:

```text
declare V_def so that partial V_def / partial Z = P
```

is just the free-`P` problem wearing a nicer suit.

The best honest result is a composite candidate:

```text
V_def =
V_trace
+ V_flow
+ V_GK_sidecar
+ V_rel
```

with no cross terms as a minimal fixed closure.

The useful split is:

| block | status |
|---|---|
| `V_trace` | partial conditional owner |
| `V_flow` | partial geometric owner |
| `V_GK_sidecar` | contract only |
| `V_rel` | open boundary closure |
| cross terms | fixed zero closure |

So `V_def` can be organized. It cannot yet be promoted.

## 4. What Is Partially Owned

The trace block has real support:

```text
N_D = (1/3) ln(V_D0/V_D)
```

and checkpoint 138 showed:

```text
p = -rho + (1/3) d rho/dN_D.
```

Checkpoint 139 then gave the conditional additive-hazard shape:

```text
A = 1 - exp(-I_M).
```

So the trace/volume part can partially own:

```text
Gamma_eff.
```

The flow block also has partial support:

```text
V_flow = 1/2 ||Xi_flow||^2_DeWitt.
```

Checkpoint 211 gave partial ADM/DeWitt/Raychaudhuri ownership for expansion
dispersion, shear, and vorticity.

So the flow part can partially own a trace-free:

```text
Khat.
```

That is useful. It is not the full parent action.

## 5. What Is Not Owned

The missing pieces are still decisive:

```text
Z_{mu nu},
M_AB,
cross terms,
J_rel boundary primitive,
B_mem = 2/27,
constraint algebra,
stress/Bianchi variation.
```

The response deformation ledger is:

| response piece | status |
|---|---|
| `Z_trace` | partial pass |
| `Z_flow_TF` | partial pass |
| `Z_Weyl` | natural norm, not parent-weighted |
| `Z_Q` | open |
| `Z_Jrel` | open |
| cross terms | closure zero |

This means:

```text
P = partial V_def / partial Z
```

is a good contract, but not a theorem.

## 6. Demotion Decision

The `X` route is not killed.

It is demoted.

New status:

```text
X_source_identity_route = closure_support_theorem_target.
```

Allowed use:

```text
organize q_loc source identity and leakage bounds.
```

Forbidden use:

```text
claim derived local GR or PPN silence.
```

The same applies to `V_def`:

```text
V_def = composite_candidate_contract.
```

It can track which blocks could own `Gamma_eff` and `Khat`. It cannot be called
the parent action until `Z_{mu nu}` and `M_AB` are derived.

## 7. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| free `V_def` rejected | pass |
| trace block partially owned | conditional pass |
| flow block partially owned | conditional pass |
| combined `V_def` contract written | conditional pass |
| `V_def` parent-derived | fail |
| `P=partial V_def/partial Z` promoted | fail |
| `X` route promoted | fail |
| local GR or PPN promoted | fail |

## 8. Decision

Decision:

```text
Vdef_composite_candidate_partial_trace_flow_owned_X_route_demoted_to_closure_support
```

Meaning:

```text
V_def can be decomposed into blocks that are partly motivated by existing MTS
mechanics, but the full defect potential is not parent-derived.
```

Main gain:

```text
we did not leave V_def as magic.
```

Main failure:

```text
we still do not have parent Z_{mu nu} or full M_AB.
```

Current status:

```text
local-GR route remains a disciplined theorem target;
X/P/V_def are closure-support machinery;
no local-GR or PPN promotion is allowed.
```

This is a useful “Mayweather round”, not a knockout: we slipped the worst
mistake, landed some structure, and refused to throw a wild overclaim.

## 9. Next Target

Create:

```text
225-local-GR-route-ledger-and-empirical-pivot-gate.md
```

Purpose:

```text
compile the local-GR route after checkpoints 218-224:
what is conditionally derived, what is closure support, what is numerically
bounded, and whether the next move should stay on derivation or pivot to an
empirical/local-bound test.
```

Pass condition:

```text
the local route has no hidden promotion drift and a clean next action.
```

Fail condition:

```text
we keep inventing elegant parent-action placeholders without admitting which
ones are closure support.
```
