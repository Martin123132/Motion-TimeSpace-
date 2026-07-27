# 4965 - Ricci-flat p8 basis, helicity projector and first motion source

Marker: `MTS_4965_P8_BASIS_HELICITY_PARTIAL_FLOW`.

Formal marker: `PPC4161_P8_BASIS_HELICITY_MOTION_SOURCE_4965`.

Date: `2026-07-13`.

Status: private analytic, source-locked and executable checkpoint. This is a
real extension of the parent calculation rather than another missing-input
ledger. It proves the complete local four-dimensional Ricci-flat parity-even
`p8` pure-gravity basis, constructs an invertible two-helicity projector and
derives the first nonzero parent-related `p8` source vector from the minimal
massive motion-scalar Hessian. The vector is only one-dimensional inside the
two-dimensional target space, and the current parent has not yet supplied the
independent boundary, `O4`, photon or pure-gravity contributions. Exact
all-operator compact GR and full MTS therefore remain false.

## 1. Complete p8 quotient rather than a guessed operator list

After the leading Einstein equations, integration by parts, Bianchi identities
and local field redefinitions are quotiented, the vacuum building blocks in
four dimensions are the chiral Weyl tensors `C_L` and `C_R`. Two independent
primary calculations give the dimension-eight Hilbert coefficient

```text
C_L^4 + C_L^2 C_R^2 + C_R^4.
```

The explicit on-shell amplitude/operator table independently lists `C_L^4`
and `C_L^2 C_R^2`, with the Hermitian conjugate of `C_L^4` supplying `C_R^4`.
No derivative pure-gravity coordinate occurs at dimension eight; the first
derivative quartics occur at dimension ten.

Reality pairs `C_L^4` with `C_R^4`. Parity exchanges `L` and `R`. Hence the
three raw chiral monomials reduce to

```text
parity even:
  O_same  = (C_L^2)^2+(C_R^2)^2,
  O_mixed = C_L^2 C_R^2;

parity odd:
  O_odd   = i[(C_L^2)^2-(C_R^2)^2].
```

The selected reflection/parity-even parent excludes `O_odd`. Therefore

```text
rank(local Ricci-flat pure-gravity p8, real and parity even) = 2.
```

This rank is complete in the declared sector, not a truncation guess.

## 2. Exact real/chiral coordinate map

Define the two real quadratic Weyl scalars

```text
X_C = C_mnrs C^mnrs,
Y_C = C_mnrs Ctilde^mnrs.
```

The source convention gives

```text
C_L^2=(X_C+iY_C)/2,
C_R^2=(X_C-iY_C)/2.
```

Writing `L2=C_L^2` and `R2=C_R^2`, the generator proves

```text
X_C^2 = L2^2+2L2R2+R2^2,
Y_C^2 =-L2^2+2L2R2-R2^2,
X_CY_C=-i(L2^2-R2^2).
```

Thus a convenient real parity-even action basis is

```text
O_CC=(X_C)^2,
O_tt=(Y_C)^2.
```

The discarded `X_CY_C` direction is precisely the parity-odd same-chirality
difference. The symbolic remainders for all three maps are zero.

## 3. Full-rank two-helicity projector

Use the source normalization

```text
S_8=int sqrt(-g) (2/kappa^4)
  [beta_C X_C^2+beta_t Y_C^2].
```

The independent local four-graviton amplitudes are

```text
M(++++)=beta_- K_++++,
M(+--+)=beta_+ K_+--+,

beta_-=beta_C-beta_t,
beta_+=beta_C+beta_t,
```

where

```text
K_++++=(s^2+t^2+u^2)^2/2
       *([12][34]/<12><34>)^2,
K_+--+=(<23>[14])^4.
```

After division by the nonzero kinematic factors, the projector is

```text
[beta_-]   [1 -1][beta_C]
[beta_+] = [1  1][beta_t].
```

Its determinant is `2`, its rank is `2`, and

```text
beta_C=(beta_-+beta_+)/2,
beta_t=(beta_+-beta_-)/2.
```

Consequently the p8 target is not intrinsically unprojectable. Exactly two
on-shell helicity channels are sufficient.

## 4. Normalization into the MTS compact action

Write the selected Lorentzian coordinates as

```text
S=(16pi G)^-1 int sqrt(-g)
  [R+a_+ I1+b_C X_C^2+b_t Y_C^2+...],

A_C3=a_+/(16pi l_P^4),
B_C=b_C/l_P^6,
B_t=b_t/l_P^6,
mu_psi=m_psi l_P.
```

Matching the Einstein-Hilbert magnitude with `kappa^2=32pi G` gives the
coefficient map, after fixing the displayed Riemann convention,

```text
beta_R3=(3/2)kappa a_+,
beta_C=kappa^2 b_C,
beta_t=kappa^2 b_t.
```

Only absolute values are used when a source convention has the opposite
Einstein-Hilbert sign. No physical sign claim is transferred without a common
continuation and subtraction convention.

## 5. First calculated p8 motion source

Checkpoint 4935 already derived the renormalized minimal motion entry

```text
Gamma_psi^(2)=Z_psi[-Box_g+m_psi^2]+... .
```

For a canonically normalized minimally coupled real massive scalar, the
source-locked large-mass four-graviton calculation gives

```text
beta_R3^psi
 =1/(4pi)^2 (kappa/2)^3 /(5040 m_psi^2),

beta_-^psi
 =1/(4pi)^2 (kappa/2)^4 /(7560 m_psi^4),

beta_+^psi
 =1/(4pi)^2 (kappa/2)^4 /(6300 m_psi^4).
```

The action map then gives the exact dimensionless source vector

```text
A_C3^psi =1/(483840 pi^2 mu_psi^2),

B_-^psi  =1/(60480 pi mu_psi^4),
B_+^psi  =1/(50400 pi mu_psi^4),

B_C^psi  =11/(604800 pi mu_psi^4),
B_t^psi  = 1/(604800 pi mu_psi^4).
```

Therefore

```text
B_+^psi/B_-^psi=6/5,
B_C^psi/B_t^psi=11.
```

This is a nonzero rank-one ray in the rank-two p8 target space. It is a
calculated source, not a placeholder. Eliminating the same scalar mass gives
the internal consistency curve

```text
B_-^psi =3870720 pi^3 (A_C3^psi)^2,
B_+^psi =4644864 pi^3 (A_C3^psi)^2,
B_C^psi =4257792 pi^3 (A_C3^psi)^2,
B_t^psi = 387072 pi^3 (A_C3^psi)^2.
```

The stripped cubic prefactor is exactly

```text
mu_psi^2 A_C3^psi=1/(483840 pi^2),
```

which independently matches the `4935` minimal scalar heat-kernel coefficient.
That equality is a normalization cross-check; it does not equate the full
finite threshold with the complete running trajectory.

The isolated scalar threshold has the opposite displayed sign to the selected
local `A_C3^S` interval. Since `A_C3^S` by itself is scheme dependent, this
rejects a direct identification of those two displayed local numbers but does
not prove that no scalar-containing physical completion can generate the final
local-plus-nonlocal amplitude.

## 6. What the present parent flow does and does not identify

The gravity-EFT derivative identity

```text
D=2+2L+sum_i V_i(d_i-2)
```

enumerates the local `D=8` source partitions. Before quotienting they include
tree `p8`, tree `p6+p4`, tree `3*p4`, one-loop `p6`, one-loop `2*p4`, two-loop
`p4`, and three-loop Einstein-Hilbert sources. Checkpoint 4964 proves that the
pure-vacuum `p4` rank is zero in the selected strict-EFT basis, so the
`p4`-dependent partitions are relocated into higher-order matching rather than
independent vacuum inputs. The independent source classes are therefore

```text
one p8 boundary/UV matching coordinate pair,
one-loop p6 insertions including C3 and O4,
three-loop pure-Einstein contributions,
massive-threshold determinants including the motion scalar.
```

The current `4935` trajectory has only

```text
{g,g_plus,g_minus,g_CFF,h_C3}.
```

It contains no `B_-` or `B_+` coordinate and no four-graviton p8 trace, so its
total p8 projection rank is exactly zero. Checkpoint 4965 raises the known
parent-related source rank from zero to one analytically through the massive
motion determinant. The total remains rank deficient because `O4`, pure
gravity, photons and the independent p8 renormalization boundary have not
been combined.

## 7. Conditional C3-to-p8 dispersive cone

The primary four-graviton analysis derives, under its infrared-finite massive,
unitarity, crossing and Regge/dispersive assumptions,

```text
|beta_R3|^2 <= beta_+/M_gap^2.
```

The MTS normalization maps this to

```text
B_+ >=576 pi^2 (A_C3^phys)^2 mu_gap^2,
mu_gap=M_gap l_P.
```

For a single particle threshold, `M_gap=2m_psi`. Inserting the source-scheme
`4963` interval merely gives the algebraic coefficient range

```text
2.7195190785650133e-6
 <=576 pi^2 (A_C3^S)^2<=
2.764484931858842e-6.
```

That range is quarantined from claim status because `A_C3^S` is not yet the
scheme-independent local-plus-nonlocal three-graviton amplitude coefficient
and `mu_gap` is not fixed. The source also warns against extending the
perturbative infrared-finite result into an unrestricted nonperturbative
four-dimensional quantum-gravity theorem.

## 8. Two-coordinate compact gate

At first p8 order every retained compact observable has the linear response

```text
delta O_i/O_i=R_i^- B_-+R_i^+ B_+,
```

and therefore

```text
|delta O_i/O_i|
 <=rho_i^-|B_-|+rho_i^+|B_+|.
```

The eleven `4964` coefficient budgets are now represented as explicit
two-coordinate domains. Their unit-response diamond has the same tightest
intercept,

```text
|B_-|+|B_+|<3.027551244686395e232
```

at the near-turning SLY4 star. This is still only a benchmark until the two
static response weights `rho_i^-` and `rho_i^+` are calculated. The known
minimal-scalar ray `B_+=(6/5)B_-` can then be intersected without fitting.

## 9. Decision

```text
complete parity-even Ricci-flat local p8 rank        = 2;
independent p8 helicity-projector rank               = 2;
minimal massive motion-scalar p8 source rank         = 1;
minimal-source helicity ratio                        = 6/5;
minimal-source real-invariant ratio                  = 11/1;
current 4935 total p8 projection rank                = 0;
total parent p8 two-vector                           = open;
static compact p8 response weights                   = open;
selected static compact GR through declared p6       = retained;
exact all-operator compact GR                        = false;
full MTS                                              = false.
```

Checkpoint 4966 should calculate the `O4=C^2(nabla psi)^2` contribution to
the same two helicity amplitudes and derive the two static response weights.
It must not replace either with fitted numbers, identify the scalar ray with
the total parent vector, or turn the conditional dispersive cone into a
numeric MTS prediction.

## 10. Executed artifacts

- `post-checkpoint-work/scripts/Y5_R2FR_4965_p8_on_shell_basis_helicity_projector_and_flow_gate.py`
- `post-checkpoint-work/source-intake/functional_rg/4965/p8_on_shell_basis.csv`
- `post-checkpoint-work/source-intake/functional_rg/4965/p8_helicity_projector.csv`
- `post-checkpoint-work/source-intake/functional_rg/4965/p8_minimal_motion_scalar_source.csv`
- `post-checkpoint-work/source-intake/functional_rg/4965/p8_parent_source_power_count.csv`
- `post-checkpoint-work/source-intake/functional_rg/4965/p8_C3_dispersive_cone.csv`
- `post-checkpoint-work/source-intake/functional_rg/4965/p8_two_coordinate_compact_domain.csv`
- `post-checkpoint-work/source-intake/functional_rg/4965/p8_flow_decision.csv`
- `post-checkpoint-work/source-intake/functional_rg/4965/p8_basis_projector_and_partial_flow_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4965/PROVENANCE.md`

No GitHub action was taken.

