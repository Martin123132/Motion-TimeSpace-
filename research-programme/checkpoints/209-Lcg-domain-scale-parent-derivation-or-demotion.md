# 209 - Lcg Domain-Scale Parent Derivation or Demotion

Private theory checkpoint. This is not a public BAO, local-GR, or CMB claim.

## 1. Trigger

Checkpoint 208 made representative selection conditional on a predeclared
domain scale:

```text
L_D = L_cg.
```

The useful current rule is:

```text
L_cg = [L_H^-2 + alpha_K G_K^2]^-1/2.
```

For FLRW:

```text
G_K = 0 -> L_cg = L_H = c/H.
```

This checkpoint asks whether that scale rule can be derived, or whether it must
be demoted to labelled closure.

## 2. Machine Artifact

Script:

```text
scripts/Lcg_domain_scale_parent_derivation_or_demotion.py
```

Run:

```text
runs/20260601-000026-Lcg-domain-scale-parent-derivation-or-demotion
```

Command:

```text
python scripts/Lcg_domain_scale_parent_derivation_or_demotion.py --timestamp 20260601-000026
```

Status:

```text
Lcg_rule_formal_inverse_coherence_scale_parent_GK_alpha_missing_closure_retained
```

Claim ceiling:

```text
Lcg_rule_conditional_closure_no_parent_scale_promotion
```

## 3. What Is Derived/Formalized

The rule has a clean formal interpretation:

```text
L_cg^-2 = L_H^-2 + alpha_K G_K^2.
```

That is:

```text
independent positive coherence-breaking rates add as inverse lengths squared.
```

This is the same mathematical structure as a positive mass-squared sum:

```text
m_eff^2 = m_H^2 + m_K^2.
```

So `L_cg` is not an arbitrary BAO-selected length.

It is a formal inverse-coherence scale with:

| term | role |
|---|---|
| `L_H = c/H` | causal/background Hubble cap |
| `G_K` | inhomogeneity/coherence-breaking inverse length |
| `alpha_K` | dimensionless normalization of that penalty |

## 4. FLRW Limit

For homogeneous FLRW:

```text
G_K = 0.
```

Therefore:

```text
L_cg = L_H = c/H.
```

Numerically:

```text
L_H = 4440.715463763339 Mpc.
```

and:

```text
eta = H0 L_cg / c = 1.
```

This preserves the checkpoint-93 result:

```text
eta is conditionally fixed in the homogeneous FLRW branch.
```

But:

```text
eta=1 does not predict B_mem.
```

It only removes one free scale factor from the amplitude corridor.

## 5. BAO Safety Check

The Hubble-cap domain remains safe for BAO common-mode use.

If the full memory amplitude:

```text
B_mem = 2/27
```

is spread linearly over `L_H`, the `150 Mpc` BAO patch sees:

```text
Delta C = 0.002502099313000086,
|Delta C|/2 = 0.001251049656500043.
```

The checkpoint-205 `Delta chi2 < 1` bound allows:

```text
Delta C < 0.005539695284669133.
```

So the Hubble-cap route is safe.

But smaller ad-hoc domains are not:

| domain | `Delta C` across `150 Mpc` | safe? |
|---|---:|---|
| `c/H` | `0.002502099313000086` | yes |
| `2c/H` | `0.001251049656500043` | yes |
| `1 Gpc` | `0.011111111111111112` | no |
| `500 Mpc` | `0.022222222222222223` | no |
| `150 Mpc` | `0.07407407407407407` | no |

This is a good guardrail:

```text
the BAO route wants the Hubble-cap domain, not a BAO-sized tuned domain.
```

## 6. What Still Fails

The rule is not parent-derived because the parent theory still lacks:

```text
G_K
```

as a specific invariant, and lacks:

```text
alpha_K
```

as a fixed normalization.

A multiplier action could impose:

```text
S_L = integral sqrt(-g) lambda_L
(L_cg^-2 - L_H^-2 - alpha_K G_K^2).
```

A potential could force an extremum:

```text
V_L ~ (L_cg^-2 - L_H^-2 - alpha_K G_K^2)^2.
```

But both are only formal unless:

```text
G_K,
alpha_K,
and the L_cg Euler/Ward identity
```

come from the parent structure.

## 7. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| inverse-coherence rule formalized | pass |
| FLRW Hubble-cap limit recovered | conditional pass |
| BAO subdomain safety checked | conditional pass |
| `G_K` parent-derived | fail |
| `alpha_K` parent-normalized | fail |
| `L_cg` promoted as theorem | fail |

## 8. Decision

Decision:

```text
Lcg_rule_formal_inverse_coherence_scale_parent_GK_alpha_missing_closure_retained
```

Meaning:

```text
L_cg is now a formal inverse-coherence contract, not an arbitrary BAO-selected
length.
```

But:

```text
it is not parent-derived.
```

Current theory status:

```text
keep L_cg as labelled closure/theorem target;
allow its FLRW Hubble-cap branch as conditional structure;
do not claim domain-scale derivation.
```

Next target:

```text
210-GK-alphaK-parent-invariant-or-fixed-closure.md
```
