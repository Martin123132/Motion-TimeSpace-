# 234 - Boundary Metric Variation and Bianchi Ledger

Private local-derivation checkpoint. This is not a public local-GR, PPN,
clock, WEP, or field-theory completion claim.

## 1. Trigger

Checkpoint 233 introduced the candidate:

```text
boundary Hodge/DeWitt metric
```

that makes:

```text
Pi_M,
Pi_TF,
Pi_matter,
P_mem
```

look like canonical projectors.

But a projector metric can still hide stress.

This checkpoint writes the stress/Bianchi ledger before the route is allowed to
claim anything.

## 2. Machine Artifact

Script:

```text
scripts/boundary_metric_variation_and_Bianchi_ledger.py
```

Run:

```text
runs/20260601-000051-boundary-metric-variation-and-Bianchi-ledger
```

Command:

```text
python scripts/boundary_metric_variation_and_Bianchi_ledger.py --timestamp 20260601-000051
```

Status:

```text
boundary_metric_stress_Bianchi_ledger_written_hidden_stress_not_cleared_no_promotion
```

Claim ceiling:

```text
Bianchi_ledger_for_projector_metric_no_parent_stress_theorem_or_PPN_promotion
```

## 3. Projector Stress Ledger

Each block has to be varied.

| block | stress obligation | safe condition |
|---|---|---|
| `Pi_M` harmonic mass flux | monopole shell/mass stress | conserved `M_eff`, no radial memory profile |
| `Pi_TF` trace-free shear | anisotropic boundary stress | sector vanishes or is carried explicitly |
| `Pi_matter` direct coupling | WEP/clock force channel | absent by universal metric coupling |
| `P_mem` relative memory | relative boundary stress | exact current plus pure-gauge primitive |
| projector metric itself | hidden projector force | metric-dependence varied in action |

The dangerous one is:

```text
delta P_mem / delta g_mu_nu.
```

If the projector depends on the metric and that variation is dropped, the
theory can fake conservation.

So the rule is:

```text
no projector without projector stress.
```

## 4. Bianchi Ledger

The total stress must include:

```text
T_total =
T_matter
+ T_metric
+ T_Meff
+ T_TF
+ T_rel
+ T_projector
+ T_X
+ T_boundary.
```

The desired identity is:

```text
nabla_mu T_total^{mu nu} = 0.
```

But that is only valid on shell if all auxiliary, boundary, and projector
variables are varied.

Forbidden shortcut:

```text
use P_mem in q_loc,
then drop T_projector.
```

That would be the same old hidden hand, just with better notation.

## 5. Consequence For Local Tests

The local residuals are now tied to stress obligations:

| residual | stress obligation |
|---|---|
| `gamma - 1` | `Pi_TF` stress must vanish or be retained |
| `Phi - Psi` | no hidden anisotropic projector stress |
| `G_eff/G - 1` | `M_eff` must be conserved and not radial hair |
| `alpha_clock` | direct clock block absent |
| `epsilon_matter` | direct composition block absent |
| `beta - 1` | total stress conserved plus no-hair plus EH operator |

This makes the local route stricter, not looser.

That is good.

It means the theory is being forced toward real field equations rather than
smooth prose.

## 6. What Still Fails

This checkpoint does not derive:

```text
the parent boundary metric,
delta P_mem / delta g_mu_nu,
the total stress tensor,
the X no-hair algebra,
the local Einstein-Hilbert exterior operator.
```

So it does not promote:

```text
q_loc = 0,
beta = 1,
local GR,
PPN safety.
```

It only prevents us from hiding projector stress.

## 7. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| projector metric stress ledger written | pass |
| Bianchi total-stress terms listed | pass |
| beta gate includes Bianchi/no-hair | pass |
| hidden projector stress cleared | fail |
| Bianchi identity parent-derived | fail |
| local GR or PPN promoted | fail |

The fail rows are not a collapse.

They are the next honest work.

## 8. Decision

Decision:

```text
boundary_metric_stress_Bianchi_ledger_written_hidden_stress_not_cleared_no_promotion
```

Meaning:

```text
the candidate boundary metric is no longer allowed to be treated as harmless.
Each projector block now has an explicit stress/Bianchi obligation.
```

Main gain:

```text
hidden projector stress is now explicitly fenced.
```

Main failure:

```text
full parent variation proving conserved total stress is still missing.
```

## 9. Next Target

Create:

```text
235-projector-stress-variation-or-nohair-constraint-algebra.md
```

Purpose:

```text
either compute/structure delta P_mem / delta g_mu_nu,
or attack the X/no-hair constraint algebra.
```

Pass condition:

```text
T_projector is explicitly derived or shown to vanish under the same conditions
that define P_mem.
```

or:

```text
X/J_rel/V_def are shown to carry no exterior propagating local hair.
```

Fail condition:

```text
the projector route is used in local tests without its stress.
```
