# 210 - GK AlphaK Parent Invariant or Fixed Closure

Private theory checkpoint. This is not a public BAO, local-GR, galaxy, or CMB
claim.

## 1. Trigger

Checkpoint 209 left the useful scale rule:

```text
L_cg^-2 = L_H^-2 + alpha_K G_K^2.
```

That is a clean inverse-coherence law, but it still had two loose pieces:

```text
G_K
alpha_K
```

This checkpoint asks whether they can be parent-owned, or whether they must be
frozen as explicit closure.

## 2. Machine Artifact

Script:

```text
scripts/GK_alphaK_parent_invariant_or_fixed_closure.py
```

Run:

```text
runs/20260601-000027-GK-alphaK-parent-invariant-or-fixed-closure
```

Command:

```text
python scripts/GK_alphaK_parent_invariant_or_fixed_closure.py --timestamp 20260601-000027
```

Status:

```text
GK_composite_invariant_candidate_alphaK_fixed_closure_parent_metric_missing
```

Claim ceiling:

```text
GK_alphaK_internal_candidate_no_domain_scale_or_local_GR_promotion
```

## 3. Best Current Construction

The strongest non-cheating route is:

```text
G_K^2[D] = ||Xi_D||_M^2.
```

where `Xi_D` is a coherence-breaking vector with inverse-length components:

```text
Xi_D =
(
c^-1 delta theta,
c^-1 sigma,
c^-1 omega,
W_D,
L_D^-1 [J_rel],
L_D^-1 delta Q/||Q||_*
).
```

The Weyl component is:

```text
W_D = (C_abcd C^abcd)^1/4.
```

So:

```text
W_D^2 = (C_abcd C^abcd)^1/2.
```

which has units `L^-2` when inserted into `G_K^2`.

This gives:

```text
G_K^2 >= 0.
```

and:

```text
G_K = 0
```

for exact FLRW, because expansion dispersion, shear, vorticity, Weyl curvature,
relative boundary obstruction, and load anisotropy vanish in the ideal coherent
branch.

## 4. AlphaK Result

The honest way to stop `alpha_K` becoming a hidden fit knob is to absorb it into
the definition of `G_K`:

```text
L_cg^-2 = L_H^-2 + G_K^2.
```

So:

```text
alpha_K = 1
```

by canonical norm convention.

This is better than a free parameter, but it is not yet a parent theorem because
the parent theory has not derived the field-space metric:

```text
M_AB.
```

If `M_AB` is later derived, this route becomes serious. If `M_AB` remains chosen
by hand, this remains closure.

## 5. Why This Helps

This construction gives a cleaner local route without smuggling in a plateau
axiom:

```text
local curvature / flow / boundary obstruction high
-> G_K high
-> L_cg ~= 1/G_K
-> local memory response suppressed.
```

It also keeps the FLRW branch alive:

```text
exact FLRW -> G_K=0 -> L_cg=L_H=c/H.
```

So it narrows the rule rather than widening it.

## 6. Numeric Sanity Readouts

The script generated illustrative readouts only; these are not promotions.

Key machine outputs:

| case | result |
|---|---|
| exact FLRW | `G_K=0`, `L_cg=c/H` |
| smooth BAO late domain | near-Hubble common-mode branch |
| inverse-Gpc transition | starts to pressure BAO shape |
| inverse-BAO transition | not safe as smooth BAO common-mode |
| solar-system Weyl branch | possible local suppressor, needs PPN derivation |
| galaxy Weyl estimate | warning that naive curvature suppression could affect galaxy branch |

The BAO guardrail remains important:

```text
G_K near inverse BAO scale fails the checkpoint-205 C-gradient safety scan.
```

So the BAO branch needs smooth, Hubble-like coherence, not a BAO-sized tuned
domain.

## 7. What Still Fails

The construction still lacks:

```text
M_AB
```

as a parent-derived metric/norm.

It also lacks the full stress accounting:

```text
delta Xi_D,
delta M_AB,
and their Bianchi contribution.
```

That means the current result is:

```text
candidate invariant + fixed closure,
not parent theorem.
```

The hidden-knob risk has been reduced, not eliminated:

```text
alpha_K
```

has been frozen, but the component weights inside `M_AB` are not yet derived.

## 8. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| `G_K` candidate invariant constructed | pass |
| independent `alpha_K` knob removed | conditional pass |
| FLRW limit recovered | conditional pass |
| local suppressor route available | conditional pass |
| BAO smooth-domain danger identified | pass |
| parent metric `M_AB` derived | fail |
| Bianchi/stress accounting derived | fail/open |

## 9. Decision

Decision:

```text
GK_composite_invariant_candidate_alphaK_fixed_closure_parent_metric_missing
```

Meaning:

```text
G_K can now be treated as a concrete candidate invariant norm, and alpha_K can
be fixed to one as closure rather than fitted.
```

But:

```text
the parent metric M_AB and stress/Bianchi variation are missing.
```

So:

```text
no local-GR, BAO, galaxy, or field-theory promotion is allowed from this alone.
```

## 10. Next Target

Next target:

```text
211-GK-parent-metric-Ward-identity-attempt.md
```

The exact next question is:

```text
Can M_AB be derived from a Ward/current norm, or must the composite G_K norm be
frozen permanently as a closure object?
```
