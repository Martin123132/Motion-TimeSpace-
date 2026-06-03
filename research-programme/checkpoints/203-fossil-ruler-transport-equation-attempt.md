# 203 - Fossil-Ruler Transport Equation Attempt

Private theory checkpoint. This is not a public BAO claim.

## 1. Trigger

Checkpoint 202 left the BAO branch here:

```text
BAO can be a late common-mode matter-ruler readout only if the post-drag
acoustic ruler is transported as a conserved fossil comoving ruler.
```

The target was therefore:

```text
D_t r_BAO^comoving = 0
```

or, failing exact zero, an explicit amplitude law for how the BAO peak can move.

## 2. Machine Artifact

Script:

```text
scripts/fossil_ruler_transport_equation_attempt.py
```

Run:

```text
runs/20260601-000020-fossil-ruler-transport-equation-attempt
```

Command:

```text
python scripts/fossil_ruler_transport_equation_attempt.py --timestamp 20260601-000020
```

Status:

```text
fossil_ruler_transport_conditionally_derived_parent_matter_action_missing
```

Claim ceiling:

```text
fossil_ruler_transport_internal_only_parent_matter_action_missing
```

## 3. Main Result

This checkpoint gets further than the previous closure statement.

The exact-zero condition is now:

```text
u^mu partial_mu X^A = 0
```

for post-drag matter labels, plus source-free two-point transport:

```text
(D_t1 + D_t2) xi = 0.
```

Under those assumptions:

```text
D_t Delta X^A = 0
```

and the BAO peak in label/comoving space obeys:

```text
D_t r_BAO^comoving = 0.
```

So the fossil-ruler transport law is conditionally derived rather than merely asserted.

## 4. Amplitude Law If Exact Zero Fails

If the post-drag correlation function has a source term:

```text
(D_t1 + D_t2) xi = S_xi,
```

then the peak condition:

```text
partial_r xi(r_peak,t) = 0
```

gives:

```text
D_t r_peak = - partial_r S_xi / partial_r^2 xi | peak.
```

This is useful because it turns the failure into a measurable/boundable object:

```text
derive partial_r S_xi = 0,
or prove |Delta r_BAO/r_BAO| is below BAO leakage tolerance.
```

## 5. BAO Ratio Consequence

With the matter metric:

```text
tilde_g_munu = exp(C) g_munu,
```

late physical lengths scale as:

```text
d tilde_ell = exp(C_obs/2) d ell.
```

If the fossil ruler is transported in comoving matter labels:

```text
tilde_l_BAO = exp(C_obs/2) a r_BAO^comoving.
```

Then the same late matter-unit factor appears in both the distance and the ruler:

```text
tilde_D_X / tilde_r_BAO^late = D_X / r_BAO,
```

up to radial `dot_C/H` leakage and any nonzero peak drift.

This strengthens the BAO late-common-mode route, but does not promote it yet.

## 6. Numerical Bounds Imported

From checkpoint 197, a fully common-mode BAO leakage tolerance gives:

| bound | threshold | value |
|---|---:|---:|
| `max_abs_Delta_r_BAO/r_BAO` | `Delta chi2 < 1` | `0.0027698476423345664` |
| `max_abs_Delta_r_BAO/r_BAO` | `Delta chi2 < 4` | `0.005539695284669133` |
| `max_abs_Delta_r_BAO/r_BAO` | `Delta chi2 < 9` | `0.008309542927003699` |

From checkpoint 198, radial drift gives:

| bound | threshold | value |
|---|---:|---:|
| fixed-alpha `max_abs_dot_C/H` | `Delta chi2 < 1` | `0.011285628250379043` |
| shared-alpha `max_abs_dot_C/H` | `Delta chi2 < 1` | `0.018079450186889945` |

The small H0-bridge residual:

```text
dot_C/H = -0.0004084189185673548
```

is BAO-safe against those radial bounds.

But a full memory-scale late drift:

```text
dot_C/H = 2/27 = 0.07407407407407407
```

is too large. The branch still needs saturation/local silence.

## 7. What Is Derived

| piece | result |
|---|---|
| conserved matter labels imply pair label conservation | conditional pass |
| source-free post-drag correlation transport implies `D_t r_BAO^comoving = 0` | conditional pass |
| nonzero-source amplitude law | pass |
| late common-mode BAO ratio route | strengthened |
| universal parent matter action | fail/open |
| source-free/bounded `S_xi` from parent theory | fail/open |

## 8. What Is Still Missing

The parent theory must still own:

| missing owner | required form |
|---|---|
| universal matter metric | `S_matter[psi_m, tilde_g_munu]` |
| matter Noether identity | `tilde_nabla_mu T_m^{mu nu}=0` |
| number current conservation | `tilde_nabla_mu(n u^mu)=0` |
| convective label variables | `u^mu partial_mu X^A=0` |
| correlation source rule | `partial_r S_xi|peak=0` or bounded |
| domain selector | CMB endpoint versus BAO transported late matter ruler |

Until these are parent-owned, this remains an internal theorem target, not a promoted BAO result.

## 9. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| label transport equation derived | conditional pass |
| exact fossil-ruler zero condition derived | conditional pass |
| amplitude law for nonzero source derived | pass |
| parent matter action owns assumptions | fail |
| BAO support claim allowed | fail |

## 10. Decision

Decision:

```text
fossil_ruler_transport_conditionally_derived_parent_matter_action_missing
```

Meaning:

```text
The BAO fossil-ruler transport route is not just hand waving anymore:
if post-drag matter has conserved labels and the BAO two-point feature is
source-free in label space, the comoving ruler is transported exactly.
```

But:

```text
the exact-zero conditions are still assumptions until the parent matter action
and the correlation-source rule derive them.
```

Current theory status:

```text
BAO late common-mode route improved;
no BAO promotion yet;
next burden is parent action ownership.
```

Next target:

```text
204-matter-metric-action-and-ruler-transport-owner-contract.md
```
