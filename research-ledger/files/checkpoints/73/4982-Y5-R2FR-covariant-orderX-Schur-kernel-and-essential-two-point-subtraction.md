# 4982 - Covariant order-X Schur kernel and essential two-point subtraction

Formal marker: `PPC4161_COVARIANT_ORDERX_ESSENTIAL_SUBTRACTION_4982`.

## Decision

Checkpoint 4982 closes the constant-gradient order-`X` parent calculation
left open by checkpoint 4981. It derives the covariant second variation of
the actual `P(X)` action, independently differentiates the original metric
density, reduces the mixed metric-motion Schur operator, and maps the
source-owned off-shell curvature subtractions into the unique essential
`X^2` source.

The central result is

```text
raw standard-frame source:       beta_c=20 g^2,
redundant curvature sources:      beta_ctilde=-g/(6pi),
                                  beta_d=-g/(3pi),
running Einstein-frame shift:     8pi g(beta_ctilde+beta_d)=-4g^2,
essential source:                 beta_c,ess=16g^2.
```

No finite coefficient is fitted. The `RX` and
`R_mn nabla^m psi nabla^n psi` rows are not promoted as independent physics;
they are removed with the already derived finite disformal-conformal map.

The result is deliberately scoped:

```text
covariant P(X) metric-motion Hessian                    = derived;
independent automatic-differentiation check             = passed;
checkpoint-4956 flat Hessian                            = exactly recovered;
principal mixed Schur operator                          = reduced;
constant-gradient four-derivative source basis          = closed modulo EOM/IBP;
essential two-point subtraction map                     = derived;
essential source beta_c,ess=16g^2                       = derived;
full N=8 principal cone on x<=0.1                       = positive;
P(X) packet at X=0 local branch                         = exactly silent;
nonconstant-gradient (Box psi)^2/O2 projector           = open;
finite parent metric TTT                                = false;
exact all-operator local GR                             = false;
full MTS                                                = false.
```

The runner passes `19/19` gates and the independent validator passes
`79/79`. No web or GitHub action was performed.

## 1. Exact covariant second variation

Use the source convention

```text
X=g^(mu nu)v_mu v_nu,
v_mu=nabla_mu psi_bar,
S_P=integral sqrt(g) P(X),
P(0)=0,
P_X(0)=1/2.
```

For a linear covariant-metric fluctuation `h_mn`,

```text
delta_h X=-v.h.v,
delta_h delta_k X=v.(hk+kh).v,
rho_hk=delta_h delta_k sqrt(g)/sqrt(g)
      =tr(h)tr(k)/4-tr(hk)/2.
```

The complete mixed metric-metric response is therefore

```text
delta_h delta_k[sqrt(g)P]/sqrt(g)
 =P rho_hk
 +(tr(h)/2)P_X delta_k X
 +(tr(k)/2)P_X delta_h X
 +P_X delta_h delta_k X
 +P_XX delta_h X delta_k X.
```

Let `w_mu=nabla_mu chi` and `u_mu=nabla_mu xi` be two scalar-fluctuation
gradients. The remaining blocks are

```text
delta_h delta_chi[sqrt(g)P]/sqrt(g)
 =P_X[tr(h)(v.w)-2v.h.w]
  -2P_XX(v.h.v)(v.w),

delta_chi delta_xi[sqrt(g)P]/sqrt(g)
 =2P_X(w.u)+4P_XX(v.w)(v.u).
```

These expressions contain the measure, inverse-metric, and nonlinear
`P_XX` contacts in one parent-owned variation. No separate contact axiom is
inserted.

## 2. Independent differentiation and old-block recovery

A second-order automatic-differentiation jet engine evaluates

```text
sqrt(det(g)) [X/2+cX^2],
X=v^T g^-1 v,
```

directly for eight random controls in each of the metric-metric,
metric-scalar, and scalar-scalar blocks. The maximum relative and absolute
differences from the analytic formulas are

```text
4.882051039911455e-15,
5.551115123125783e-17.
```

On a flat constant-gradient background, the same formulas reduce exactly to

```text
H_hh=P M0+X P_X M1+X^2 P_XX M2,

H_hpsi=sqrt(X)[P_X B1+X P_XX B2],

H_psipsi=2P_X p^2+4X P_XX(e.p)^2.
```

After the checkpoint-4956 normalization and regulator insertion, these are
precisely its three functional Hessian blocks. The maximum direct block
residual is `2.7755575615628914e-17`.

Thus checkpoint 4982 is a covariant derivation of the old flat block, not a
new ansatz selected to reproduce it.

## 3. Mixed Schur operator

At first order in the background gradient, the exact mixed vertex is

```text
B_mn=(1/2)g_mn(v.D)-v_(m D_n).
```

With the inverse DeWitt tensor used by the source,

```text
K_AB=delta_AB-(1/2)t_A t_B,
```

four-dimensional contraction gives

```text
B^dagger K B=(1/2)X(-Box).
```

Checkpoint 4982 independently rederives this identity over 128 random
momentum/gradient pairs at maximum relative residual
`5.614831464227381e-16`. Rotating the momentum relative to the background
gradient changes the result by at most `1.3051103788141558e-15`.

On the flat unregulated principal branch,

```text
B^dagger K(-Box)^-1 B=X/2.
```

The leading mixed Schur insertion is therefore local and creates no new
pole. Curvature, endomorphism, and regulator expansions of the inverse
operator generate the local curvature-motion packet rather than an
independent long-range degree of freedom.

## 4. Complete constant-gradient four-derivative packet

The acquired primary scalar-gravity source contains

```text
c X^2
+ctilde R_mn nabla^m psi nabla^n psi
+d R X.
```

It also states that the off-shell bilinear `(Box psi)^2` was not included.
That omission must be handled explicitly. Integration by parts and the
covariant-derivative commutator give

```text
integral[(Box psi)^2-(nabla_mn psi)^2]
 =integral R_mn nabla^m psi nabla^n psi+boundary.
```

The `(Box psi)^2` row is removable by the leading scalar equation of motion;
its Hessian-squared partner differs by `RicciX` and a boundary. Therefore

```text
{X^2, RicciX, RX}
```

is complete for the constant-gradient on-shell/EOM quotient. It is not a
complete off-shell nonconstant-gradient calculation. Derivatives of `X`,
`Box psi`, and the independent `O2` projector remain the explicit next
sector.

The source-locked harmonic gauge ghost operator has no background-scalar
argument, so its direct order-`X` insertion is zero. This does not make
individual off-shell curvature coefficients gauge invariant; the essential
quotient below is the safe physical object.

## 5. Exact essential subtraction

In the standard frame, the acquired one-loop origin sources are

```text
beta_c|0       =20g^2,
beta_ctilde|0  =-g/(6pi),
beta_d|0       =-g/(3pi).
```

The leading Einstein-scalar equations give

```text
R_mn=8pi G X_mn,
R=8pi G X,
X_mn X^mn=X^2.
```

Consequently the field-redefinition invariant coordinate is

```text
c_ess=c+8pi g(ctilde+d).
```

The finite parent map derived at checkpoint 4958 is

```text
g_old,mn=C(X)g_E,mn+A(X)nabla_m psi nabla_n psi,
r=sqrt[(C+AX)/C],
r^3-r+kappa X[d(r^2-1)+ctilde r]=0,
C=(r+kappa dX)/r^2,
A=-kappa ctilde/r,
kappa=16pi g.
```

Maintaining the minimal-essential conditions

```text
ctilde=d=0
```

at every scale shifts the raw scalar source by

```text
Delta beta_c
 =8pi g(beta_ctilde+beta_d)
 =8pi g[-g/(2pi)]
 =-4g^2.
```

Therefore

```text
beta_c,ess|0=20g^2-4g^2=16g^2.
```

This is independently present in the checkpoint-4941 source quotient and is
reproduced without fitting. It proves that the physical `X^2` interaction is
generated, while preventing two redundant curvature coefficients from being
miscounted as extra predictions or extra free local forces.

## 6. Principal-cone bound

For the full order-eight essential fixed-function germs,

```text
p(x)=x/2+sum_(n=2)^8 a_n x^n,
lambda_T=2p'(x),
lambda_L=2p'(x)+4x p''(x).
```

Scanning `0<=x<=0.1` gives

| scheme | min `lambda_T` | min `lambda_L` | first `lambda_L=0` |
|---|---:|---:|---:|
| dynamic `eta_N` | `0.957920827810` | `0.846546731674` | `0.161451504082` |
| reference `eta_N=0` | `0.969952113619` | `0.892947075887` | `0.179440681416` |

Both full `N=8` germs are strictly elliptic throughout the certified
`x<=0.1` chart. The independently recomputed first zeros agree exactly with
the stored checkpoint-4958 values. This is a Euclidean principal-symbol
result; it is not silently relabelled as a Lorentzian causality or
superluminality claim.

## 7. Ward identity and local GR branch

For the Euclidean-sign stress representative

```text
Theta^mu_nu=2P_X v^mu v_nu-delta^mu_nu P,
```

direct differentiation gives

```text
nabla_mu Theta^mu_nu
 =2nabla_mu(P_X v^mu)v_nu.
```

The right-hand side vanishes on the motion equation. Thus the `P(X)` packet
does not introduce a separately adjustable force current; its source is the
same Hilbert stress entering the metric equation.

On the selected homogeneous zero-gradient branch,

```text
X=0,
P(0)=0,
v_mu=0.
```

It follows exactly that

```text
T_PX,mn=0,
H_hpsi=0,
all order-X Schur terms=0,
X^2=RicciX=RX=0.
```

The complete four-derivative motion-curvature packet therefore leaves the
checkpoint-4960 leading Einstein pole, calibrated Newton residue, and
Maxwell/Poynting metric source unchanged on that branch. This is a real
packet-level local-GR gate. It is not an all-operator proof because the
nonconstant-gradient/O2 sector and other parent sectors remain separate.

## 8. Promotion and next target

Promoted:

```text
covariant order-X P(X) Hessian                       = true;
principal mixed Schur reduction                     = true;
constant-gradient essential subtraction             = true;
essential source beta_c,ess=16g^2                   = true;
full N8 x<=0.1 Euclidean principal regularity        = true;
P(X) packet local-GR silence at X=0                 = true.
```

Not promoted:

```text
nonconstant-gradient/O2 completion                  = false;
Lorentzian causal cone                              = false;
finite parent metric TTT                            = false;
exact all-operator local GR                         = false;
full MTS                                            = false.
```

The next target is checkpoint 4983: derive the missing nonconstant-gradient
`(Box psi)^2/O2` projector, reduce its EOM and boundary pieces, and test the
remaining invariant response on sourced local profiles. This is now the
specific motion-sector obstruction; the constant-gradient Schur packet is no
longer open.

## Outputs

- `post-checkpoint-work/scripts/Y5_R2FR_4982_covariant_orderX_schur_and_essential_subtraction.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4982_covariant_orderX_schur_and_essential_subtraction_validation.py`
- `post-checkpoint-work/source-intake/functional_rg/4982/covariant_PX_second_variation_contract.csv`
- `post-checkpoint-work/source-intake/functional_rg/4982/covariant_PX_autodiff_crosscheck.csv`
- `post-checkpoint-work/source-intake/functional_rg/4982/order_X_schur_operator_reduction.csv`
- `post-checkpoint-work/source-intake/functional_rg/4982/order_X_two_point_essential_subtraction.csv`
- `post-checkpoint-work/source-intake/functional_rg/4982/essential_PX_principal_cone_bound.csv`
- `post-checkpoint-work/source-intake/functional_rg/4982/local_GR_zero_gradient_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4982/covariant_orderX_essential_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4982/VALIDATION_PROVENANCE.md`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4982_VALIDATION.csv`
