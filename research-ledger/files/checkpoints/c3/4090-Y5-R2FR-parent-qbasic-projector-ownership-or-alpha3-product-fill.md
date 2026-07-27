# 4090 - Parent Q-Basic Projector Ownership Or Alpha3 Product Fill

- Timestamp: `2026-07-02T04:24:04+00:00`
- Status: `private_nonclaim_checkpoint`
- Decision: `QBASIC_PROJECTOR_PRIVATE_BRANCH_ALPHA3_ZERO_CONSOLIDATED_PUBLIC_PROMOTION_STILL_PARENT_ADOPTION_BLOCKED`
- Public local-GR/projector-sector claim: `false`
- GitHub action: `false`

## Result

4090 consolidates the clean route:

```text
P_D readout-only or q-basic/topological
delta_g P_D = 0
D_D P_D = 0
Phi_D = tau_wall_TF = 0
same Hilbert denominator
```

Therefore, in the selected private local branch:

```text
epsilon_domain_flux = 0
alpha3_domain = W_domain_alpha3 * epsilon_domain_flux = 0
```

This beats the brutal `alpha3 <= 4e-20` bound by theorem-zero, not by tuning.

## Why It Is Not Public Yet

The proof is strong inside the selected branch, but the corpus still needs one more parent-adoption move:

```text
the parent action must make q-basic/topological projector ownership mandatory
not optional branch choice
not closure-only
not post-readout fitting
```

So 4090 is a serious internal advance, not a public local-GR claim.

## Fallback If Rejected

If q-basic/topological ownership is rejected:

```text
alpha3_domain = W_domain_alpha3 * epsilon_domain_flux
|alpha3_domain| <= 4.0e-20
```

Required source fields:

```text
W_domain_alpha3
epsilon_domain_flux
units
frame/coframe
source denominator
source path
no-cancellation policy
```

For unit coefficient:

```text
|epsilon_domain_flux| <= 4.0e-20
```

That is why zero is the better route.

## Decision

```text
private selected branch alpha3 projector = exact zero
public projector-sector claim = still false
fallback alpha3 product contract = ready
next = parent adoption promotion or vector preferred-frame branch
```

## Next

```text
4091-Y5-R2FR-projector-adoption-promotion-or-vector-preferred-frame-bound.md
```
