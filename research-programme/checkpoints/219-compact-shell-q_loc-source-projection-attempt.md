# 219 - Compact Shell Qloc Source Projection Attempt

Private theory checkpoint. This is not a public local-GR, PPN, galaxy, BAO, CMB,
or field-theory completion claim.

## 1. Trigger

Checkpoint 218 showed:

```text
compact-shell sidecar + fixed G_K
```

passes a `q_R`-like magnitude proxy.

But the open row remains:

```text
q_loc^nu.
```

This checkpoint asks:

```text
Can compact-vacuum-shell morphology force q_loc^nu -> 0 without inserting a
plateau axiom?
```

## 2. Machine Artifact

Script:

```text
scripts/compact_shell_qloc_source_projection_attempt.py
```

Run:

```text
runs/20260601-000036-compact-shell-q_loc-source-projection-attempt
```

Command:

```text
python scripts/compact_shell_qloc_source_projection_attempt.py --timestamp 20260601-000036
```

Status:

```text
compact_shell_q_loc_projection_conditional_Noether_identity_missing_leakage_budget_set
```

Claim ceiling:

```text
q_loc_projection_attempt_no_local_GR_or_PPN_promotion
```

## 3. The Conditional Theorem

Start from:

```text
q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu Khat^{mu nu}).
```

The desired parent identity is:

```text
nabla_mu Khat^{mu nu} - nabla^nu Gamma_eff
= S_L^nu + d_rel J_rel^nu.
```

Then:

```text
q_loc^nu = -P_loc(S_L^nu + d_rel J_rel^nu).
```

In a compact vacuum collar:

```text
S_L^nu = 0.
```

If the local representative is trivial:

```text
d_rel J_rel^nu = 0.
```

Then:

```text
q_loc^nu = 0.
```

That is the route.

## 4. What Fails

The route is not yet derived because two ingredients are missing:

```text
the Noether/source identity,
the local trivial J_rel representative.
```

Morphology alone is not enough.

It can say:

```text
this is a compact vacuum shell.
```

It cannot by itself prove:

```text
nabla_mu Khat^{mu nu} = nabla^nu Gamma_eff.
```

So no local-GR promotion is allowed.

## 5. Leakage Budget

Because the theorem is missing, the useful fallback is a leakage budget.

From checkpoint 218:

| compact case | q proxy | remaining source-leakage budget |
|---|---:|---:|
| `solar_1AU_shell` | `9.685577480653662e-06` | `1.3314422519346338e-05` |
| `solar_Mercury_shell` | `1.556736803842303e-05` | `7.4326319615769725e-06` |
| `earth_GPS_shell` | `1.2597426708488547e-06` | `2.1740257329151145e-05` |

Worst compact remaining budget:

```text
7.4326319615769725e-06.
```

Meaning:

```text
any unmodelled source-projection leakage larger than this would break the
current q_R-like compact-shell proxy gate.
```

That is a hard internal constraint.

## 6. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| compact shell collar condition | conditional pass |
| Noether source identity derived | fail |
| `J_rel` local trivial representative derived | fail |
| source leakage budget positive | pass |
| `q_loc^nu = 0` promoted | fail |
| PPN local GR promoted | fail |

## 7. Decision

Decision:

```text
compact_shell_q_loc_projection_conditional_Noether_identity_missing_leakage_budget_set
```

Meaning:

```text
we have a clean theorem target and a numerical leakage budget, but not a local
GR derivation.
```

## 8. Next Target

Next target:

```text
220-Jrel-local-trivial-representative-or-closure-bound.md
```

The exact next question:

```text
Can J_rel be forced to the trivial representative in compact local vacuum
shells, or must local q_loc silence stay an explicit closure bound?
```
