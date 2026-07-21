# 4933 - Minimal combined `C3-CFF-F4` natural flow

Marker: `MTS_C3_CFF_F4_COMBINED_NATURAL_FLOW_4933`.

Date: `2026-07-12`.

Status: private source-executed derivation checkpoint; exact `C3` source
reproduction, strong photon-flow reconstruction and a five-coordinate partial
common zero; no complete MTS fixed-point, local-GR, Maxwell-emergence or public
evidence claim.

## 1. Decisive result

The work has moved beyond placing an external photon fixed point beside an
external Weyl-cubic fixed point. Their mechanically extracted functional
traces now run in one shared natural-essential projection.

The source-compatible partial system has the common zero

```text
(g,g_plus,g_minus,g_CFF,h_C3)
  =(0.130560452615,
    0.347004250660,
    3.244436423674,
    0.003729942576,
    4.27303833729e-6),

||beta||_infinity=1.44518e-13.
```

Its beta-matrix spectrum is

```text
lambda={
  -1.89083047073,
   0.290529737449,
   0.242075164606 +/- 0.022804251273 i,
   1.09393574651
}.
```

Therefore this partial five-coordinate system has exactly one relevant
direction and four irrelevant directions. Its signed distance from the
imaginary axis is

```text
delta_partial=0.242075164606.
```

This is not the complete MTS point. Two exact cross-source terms remain open
inside this minimal `C3-CFF-F4` truncation, and the MTS motion and full visible-
matter Hessians are not yet appended.

## 2. Sources and execution boundary

The source packet and hashes are recorded in
`source-intake/functional_rg/4933/PROVENANCE.md`.

The Weyl-cubic calculation is arXiv `2312.03831` plus its official Mendeley
notebook DOI `10.17632/zfn4rzthcg.1`. The direct evaluator mechanically parses
all 13 projection equations and evaluates 2272 Litim threshold terms,
including the half-weight endpoint convention for cutoff delta functions.

At the source vacuum law `rho=1/(8 pi)`, it reproduces

```text
g*=0.364187176586604,
h_C3*=4.49003042408494e-7,
theta={2.22518625933,-3.84962423550}.
```

The photon-gravity calculation is arXiv `2405.08860` plus official supplement
DOI `10.17632/tysd636dn4.1`. Its 18 extracted input cells are evaluated with
the natural Litim regulator and reconstructed minimal-essential left-hand
projections. The resulting root is

```text
(g,g_plus,g_minus,g_CFF)
  =(0.130524901127,
    0.348484192031,
    3.297394364468,
    0.003753214554).
```

This is close to rounded published FP1
`(0.131,0.351,3.327,0.00375)`. Three exponents agree closely; the leading
reconstructed exponent is `1.89314` rather than published `1.845`. The photon
calculation is consequently a strong reconstruction, not an exact convention-
independent reproduction.

## 3. Vacuum-law correction

The two sources cannot be joined at the older C3 choice `rho=1/(8 pi)`. The
Gaussian photon volume trace fixes

```text
rho=1/(4 pi),
lambda=g/(4 pi).
```

This also exposes the common source singular line `g=2 pi`. The C3 source
point is therefore continued to the photon vacuum law before any coupling is
attempted. Copying the old `rho=1/(8 pi)` coordinates into FP1 would be a
scheme splice and is prohibited.

## 4. Shared 20-equation system

The combined unknown vector contains the 13 C3 variables

```text
{beta_g,beta_h,beta_Euler,
 gamma_g,gamma_R,gamma_S,gamma_R2,gamma_C2,
 gamma_SSTL,gamma_RS,gamma_CS,gamma_DeltaR,gamma_DeltaS}
```

and seven photon-specific variables

```text
{beta_F2sq,beta_F4,beta_CFF,
 gamma_Ftrace,gamma_FTL,gamma_a,gamma_DF}.
```

The five shared quantities

```text
beta_g,beta_Euler,gamma_g,gamma_R,gamma_S
```

are single variables, not independently frozen outputs. The 13 vacuum-
curvature rows are supplied by the six-derivative C3 notebook. The seven
photon-background rows `F2`, `FDeltaF`, `RFF`, `SFF`, `F2sq`, `F4` and `CFF`
are supplied by the photon notebook. Thus the previous frozen-photon
diagnostic is replaced by one square `20 x 20` projection system.

The matrix condition number at the root is

```text
kappa_2(A)=1.5738267e5.
```

This is finite but large and is retained as a numerical warning. The common
zero is stable under the current solve tolerances, but future coefficient
work must not round its source matrices aggressively.

## 5. Photon curvature contribution

The photon vacuum trace supplies exact affine additions to the C3 curvature
basis. At the reconstructed photon point, the rows

```text
{1,R,R2,S2,C2}
```

receive

```text
{ 0.00651549265,
 -0.00426815377,
 -0.000182252831,
  0.00227424459,
 -0.000497367265 }.
```

These additions remove the apparent `beta_g=0.6676` incompatibility found by
evaluating pure C3 gravity at the photon value of `g`. The large mismatch was
not evidence against the common flow; it was the omitted photon stress trace.

## 6. Derived six-derivative photon terms

The primary arXiv `1611.02705` coefficient table gives

```text
c1_vector =1/[10080(4 pi)^2],
c1_scalar =1/[30240(4 pi)^2].
```

Subtracting the Stueckelberg scalar gives the massless Maxwell coefficient

```text
c6_Maxwell=1/[15120(4 pi)^2]
           =4.188210302676e-7.
```

The exact optimized photon kernel produces

```text
4 gamma_a+3 gamma_DF=0.149158694025,

Delta RHS_C3,Maxwell
  =-[4 gamma_a+3 gamma_DF]/[15120(4 pi)^2]
  =-6.24707979048e-8.
```

The constant-Weyl two-form principal symbol

```text
K=I-4 g_CFF C
```

is calibrated against the notebook's exact quadratic `CFF^2` coefficient.
It yields

```text
Delta RHS_C3,principal=g_CFF^3/(5 pi^2)
                      =1.07137232905e-9.
```

The latter is exact within the constant-Weyl principal symbol. It is not the
complete nonminimal `a6` coefficient.

## 7. Movement from the triangular seed

Relative to the reconstructed photon root plus the conditional C3 nullcline,
the shared solve moves the coordinates by

```text
Delta g/g             =+0.02724 percent,
Delta g_plus/g_plus   =-0.42468 percent,
Delta g_minus/g_minus =-1.60605 percent,
Delta g_CFF/g_CFF     =-0.62005 percent,
Delta h_C3/h_C3       =-0.13886 percent.
```

The coupling does not destroy or radically displace FP1 in the terms actually
derived. The largest present movement is the `g_minus` photon self-interaction
coordinate at about `1.61%`.

## 8. Stability and existence response

For the partial stability matrix, the modal sufficient condition is

```text
||V^-1 DeltaJ V||_2 < 0.242075164606.
```

Because `kappa_2(V)=150.5064`, the more conservative coordinate-basis
Bauer-Fike condition is

```text
||DeltaJ||_2 < delta_partial/kappa_2(V)
             =0.00160840422841.
```

The inverse stability response is

```text
||J_partial^-1||_2=224.158805524,

||delta x||_2
  <=224.158805524 ||r_open||_2+O(||r_open||_2^2).
```

This is a first-order response contract, not a nonlinear fixed-point theorem.
The exact inverse matrix and every source-row response are stored in
`combined_c3_photon_stability_results.json`.

## 9. Open terms are now quantified

For a single omitted source projection at a time, the largest linear source
magnitude keeping every fixed-point coordinate shift below one percent is

| omitted source row | one-percent linear threshold |
|---|---:|
| portal-dependent C3 `a6` row | `4.67445977895e-8` |
| direct C3 Hessian in `F2` | `7.19762e-4` |
| direct C3 Hessian in `FDeltaF` | `4.56294e-5` |
| direct C3 Hessian in `RFF` | `1.01204e-2` |
| direct C3 Hessian in `SFF` | `5.93110e-4` |
| direct C3 Hessian in `F2sq` | `1.75831e-3` |
| direct C3 Hessian in `F4` | `1.79217e-3` |
| direct C3 Hessian in `CFF` | `1.13938e-5` |

These are diagnostic linear thresholds, not empirical bounds and not proof
that the unknown coefficients satisfy them. The portal-dependent `a6` row is
the tightest immediate amplitude target. The direct `C3` Hessian also has to
be differentiated with respect to the five couplings before the full index
gate can close.

## 10. What is closed and what is not

```text
official C3 notebook extraction             = closed;
exact C3 source fixed-point reproduction     = closed;
official photon notebook extraction          = closed;
photon fixed-point reconstruction            = closed with convention firewall;
common vacuum law                            = derived;
shared 20-equation partial flow              = assembled;
five-coordinate partial common zero          = solved;
partial signed index                         = one relevant direction;
minimal Maxwell a6 term                      = derived;
principal CFF3-to-C3 chain                   = derived;
open-source linear response matrix           = derived;
portal-dependent linear/quadratic CFF a6     = open;
direct C3 Hessian in photon-background rows  = open;
complete minimal C3-CFF-F4 fixed point       = not claimed;
motion/full-SM enlarged MTS fixed point       = not calculated;
GR-connected enlarged trajectory             = not integrated;
local-GR/Newton/Maxwell promotion             = false.
```

This checkpoint is evidence that the minimal gravity-photon fixed point has
survived the first real six-derivative coupling calculation. It is not yet
evidence that the complete MTS theory has a UV completion.

## 11. Next derivation

The next target is

`4934-Y5-R2FR-portal-a6-completion-and-direct-C3-photon-Hessian-gate.md`.

The order is:

1. derive the linear and quadratic `CFF`-curvature `a6` terms;
2. derive the direct C3 Hessian on the seven photon-background projections;
3. rerun the exact five-coordinate common zero and signed index;
4. only then append the MTS motion and selected visible-matter Hessians.

No closure coefficient is to be inserted merely to keep the current point.
