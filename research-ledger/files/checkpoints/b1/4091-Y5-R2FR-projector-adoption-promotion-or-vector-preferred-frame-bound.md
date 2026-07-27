# 4091 - Projector Adoption Promotion Or Vector Preferred-Frame Bound

## Purpose

4090 closed the harsh `alpha3` projector/domain flux row inside the private q-basic local branch. 4091 tests whether that same branch also kills the neighbouring preferred-frame/location rows, rather than leaving `alpha1`, `alpha2`, and `xi` as vague missing coefficients.

- Decision: `PRIVATE_PROJECTOR_DOMAIN_PREFERRED_FRAME_ZERO_EXTENDED_PUBLIC_PROMOTION_STILL_PARENT_ADOPTION_BLOCKED`
- Public local-GR/projector-sector claim: `false`
- Private selected-branch result: `alpha1_domain = alpha2_domain = alpha3_domain = xi_domain = 0`

## Derivation

The 4086 preferred-frame projection says surviving local vector, domain, coframe, or projector markers feed

```text
alpha_i_nonEH = Pi_alpha_i[DeltaE_nonEH, V_extra, domain normal, coframe marker]
xi_nonEH      = Pi_xi[anisotropic/domain marker]
```

The 4043/4061/4090 selected branch removes the relevant projector/domain markers:

```text
D_D P_D = 0                                     => epsilon_domain_vector = 0
Phi_D = 0 and tau_wall_TF = 0                   => epsilon_domain_flux = 0
delta_g P_D = 0, chi=lambda=0, tau_wall_TF=0    => epsilon_domain_anisotropy = 0
```

Therefore the whole projector/domain preferred-frame block collapses before fitting:

```text
alpha1_domain = W_domain_alpha1 * epsilon_domain_vector     = 0
alpha2_domain = W_domain_alpha2 * epsilon_domain_vector     = 0
alpha3_domain = W_domain_alpha3 * epsilon_domain_flux       = 0
xi_domain     = W_domain_xi     * epsilon_domain_anisotropy  = 0
```

This is the clean route. It avoids trying to tune products below `4e-5`, `2e-9`, `4e-20`, and `4e-9` respectively.

## What This Actually Advances

Before 4091, only the `alpha3` flux row had been consolidated in the private q-basic branch. After 4091, the same branch clears the sibling preferred-frame/location block:

- `alpha1`: no local domain vector survives.
- `alpha2`: same vector residual is zero.
- `alpha3`: 4090 flux zero is imported.
- `xi`: no local STF anisotropy survives.

That means the projector/domain sector is no longer leaking preferred-frame structure inside the private selected local branch.

## Why It Is Still Not Public

The public claim is still blocked for the same honest reasons as 4090:

- the parent action has not yet forced the q-basic/topological projector globally rather than as a selected private branch;
- global boundary/harmonic source-blindness is not closed;
- all-sector source-current/source-denominator promotion remains separate;
- non-projector R11 families still need zero theorems or bounds.

So this is not a public `MTS reduces to GR` claim. It is a real internal advance: the private q-basic local collar now kills the whole projector/domain preferred-frame block by theorem-zero.

## Fallback If Rejected

If the q-basic/vector-zero route is rejected, 4091 leaves explicit product contracts:

```text
|W_domain_alpha1 * epsilon_domain_vector|     <= 4.0e-5
|W_domain_alpha2 * epsilon_domain_vector|     <= 2.0e-9
|W_domain_alpha3 * epsilon_domain_flux|       <= 4.0e-20
|W_domain_xi     * epsilon_domain_anisotropy| <= 4.0e-9
```

No cancellation between these rows is allowed.

## Outputs

- `P8_Y5_R2FR_4091_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4091_PROJECTOR_ADOPTION_GATE.csv`
- `P8_Y5_R2FR_4091_VECTOR_ZERO_THEOREM.csv`
- `P8_Y5_R2FR_4091_PREFERRED_FRAME_RESIDUAL_VECTOR.csv`
- `P8_Y5_R2FR_4091_FALLBACK_PRODUCT_CONTRACT.csv`
- `P8_Y5_R2FR_4091_DECISION_GATE.csv`
- `P8_Y5_R2FR_4091_CLAIM_GATE.csv`
- `P8_Y5_R2FR_4091_NEXT_TARGET.csv`
- `P8_Y5_BRR545_4091_VALIDATION.csv`

## Next

4092 should stop circling product coefficients and aim at the remaining structural blocker: either derive parent adoption of the q-basic selector without an axiom, or promote the source denominator/source-current gate that keeps the private branch from becoming public local GR.
