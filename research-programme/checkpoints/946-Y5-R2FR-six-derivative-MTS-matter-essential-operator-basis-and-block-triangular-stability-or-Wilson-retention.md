# 4930 - Six-derivative MTS matter quotient and C3 block stability

Marker: `MTS_SIX_DERIVATIVE_MATTER_BLOCK_STABILITY_4930`.

Date: `2026-07-12`.

This checkpoint performs the interacting-operator step left open by 4929. It
does not assume that the free-spectator `C^3` block remains closed. It builds
the source-locked six-derivative quotient, identifies every operator with a
direct quadratic matter Hessian on the relevant background, derives explicit
mixing witnesses, and separates an arena-specific one-coefficient vacuum from
the coefficient count of the full unified action.

The outcome is useful but deliberately nonclaim: generic exact block
triangularity is rejected, while the previously found irrelevant `C^3`
direction survives the direct anomalous-dimension stress test and obeys a
quantitative signed-stability contract whose full MTS mixing matrix is not yet
calculated.

## 1. Locked sources and scope

The primary local sources are:

```text
source-intake/functional_rg/4930/1908.08050v2.pdf
source-intake/functional_rg/4930/1908.08050v2-source.tar
source-intake/functional_rg/4930/src1908/GravityEFTv2_final.tex

source-intake/functional_rg/4930/2110.09566v1.pdf
source-intake/functional_rg/4930/2110.09566v1-source.tar
source-intake/functional_rg/4930/src2110/SSTwAS.tex
```

Their SHA-256 values and extraction provenance are locked in
`source-intake/functional_rg/4930/PROVENANCE.md`. The 1908 source supplies the
complete on-shell/EOM/IBP operator quotients. The 2110 source supplies an
independent interacting scalar-gravity fixed-point comparator. Its Type-I
Einstein-Hilbert plus cosmological-constant projection is not numerically
spliced into the natural 4928 beta functions.

## 2. Complete shift-symmetric scalar quotient

For one shift-symmetric motion scalar and gravity, the complete CP-even
six-derivative quotient contains exactly five operators:

```text
O1=[(nabla phi)^2]^3,

O2=(nabla phi)^2
   (nabla_rho nabla_sigma phi)(nabla^rho nabla^sigma phi),

O3=C_mn^rs C^mnab C_abrs,

O4=(C_abrs C^abrs)(nabla phi)^2,

O5=C_mnrs (nabla^m phi)(nabla^r phi)
   (nabla^n nabla^s phi).
```

This is a Hilbert-series result after integration by parts and equations of
motion, not an ad hoc truncation. Two useful exact quotient identities are

```text
(nabla_alpha R_mnrs)^2 = 3 O3,

R_mnab (nabla^m nabla^a phi)(nabla^n nabla^b phi)
  =-O4/8.
```

On a constant-scalar Ricci-flat background, the quadratic scalar Hessians of
`O1`, `O2` and `O5` vanish by field degree. `O3` is the pure Weyl-cubic
direction. `O4=C^2 X` has a nonzero quadratic scalar Hessian and is therefore
the first unavoidable direct motion-scalar portal into the `C^3` stability
problem.

## 3. Complete dimension-six GR plus Standard Model quotient

The source-locked gravity-SM quotient has ten operators in five parity pairs:

```text
zeta_+ C C C,                 zeta_- C C Ctilde,
c_H Hdag H C C,               ctilde_H Hdag H C Ctilde,
c_B B B C,                    ctilde_B B B Ctilde,
c_G G_A G_A C,                ctilde_G G_A G_A Ctilde,
c_W W_a W_a C,                ctilde_W W_a W_a Ctilde.
```

If the parent and regulator preserve CP, the odd members do not mix into the
even `C^3` block. The even Higgs and gauge portals do have nonzero matter
Hessians at zero background field. CP separation therefore halves this SM
block but does not reduce it to the vacuum coefficient.

## 4. Anomalous-dimension leak through the optimized regulator

For a scalar regulator

```text
R_k(z)=Z_k(k^2-z) theta(k^2-z),
eta_s=-partial_t ln Z_k,
```

the subcutoff trace kernel is

```text
W(z)=(2-eta_s)+eta_s z/k^2,

Q_-1[W]=-W'(0)=-eta_s/k^2.
```

Thus the 4929 zero is exact only at `eta_s=0`. In the inherited scalar
heat-kernel and beta-function convention,

```text
c6=1/[30240(4pi)^2],

Delta beta_h=eta_s c6.
```

This is the direct Laplace-trace leak. It is not the full interacting scalar
beta function, because mixed Hessians and portal vertices add further terms.

At the source comparator value `eta_s=1.27`, the direct source is

```text
Delta beta_h=2.65951354219926e-7,
```

and the inherited two-coordinate fixed point moves from
`h_*=-3.2567460923e-7` to `h_*=-3.5960565799e-7`, a `10.42%` coordinate
shift. The `C^3` critical exponent remains negative in the inherited
convention.

The executed grid

```text
W1 in [-20,20] on 81 points,
eta_s in [-3,3] on 121 points
```

contains `9,801` rows. All `9,801/9,801` retain

```text
g_*>0 below the gravitational pole,
theta_g>0,
theta_C3<0.
```

The scan establishes robustness of this direct leak inside the inherited
two-coordinate projection. It does not substitute for portal beta functions.

## 5. Interacting scalar comparator

The independent 2110 scalar-gravity calculation has the lower interacting
basis

```text
X^2,
R_mn X^mn,
R X.
```

Its primary full branch including `eta_s=1.27` has nonzero fixed-point
coordinates and three tracked matter directions with negative critical
exponents:

```text
theta_matter=-4.54+-2.69i, -3.00.
```

The no-eta full branch also has all three tracked matter directions
irrelevant. A secondary eta branch has one relevant matter direction. This is
external existence and branch-sensitivity evidence, not a numerical result
for the MTS parent.

## 6. Explicit gauge-portal mixing witness

For any parity-even gauge portal

```text
u_X C_mnrs F_X^mn F_X^rs,
```

the two-form principal symbol can be written, in the checkpoint normalization,

```text
K=I-4u_X C.
```

Its algebraic one-loop determinant has the exact expansion

```text
(1/2)Tr log K
 =-2u_X Tr C
  -4u_X^2 Tr C^2
  -(32/3)u_X^3 Tr C^3+... .
```

Weyl tracelessness gives `Tr C=0`, but it does not remove the cubic term. With
adjoint multiplicities `d_X=(1,3,8)` for `U(1)_Y`, `SU(2)` and `SU(3)`, the
explicit `C^3` witnesses are

```text
-(32/3)d_X u_X^3 Tr C^3,

partial/partial u_X -> -32 d_X u_X^2 Tr C^3.
```

This is not a complete FRG coefficient: threshold functions, gauge fixing,
gravity mixing and the regulator still have to be included. It is sufficient
to reject the claim that a nonzero even gauge portal is generically exactly
block triangular with the `C^3` direction.

The exact-zero submanifold would require at least

```text
eta_s*=0,
u_O4*=u_H*=u_B*=u_W*=u_G*=0,
```

or separate parent-derived cancellations of every corresponding Jacobian
entry. No such parent theorem is currently present.

## 7. Signed stability contract

Write the enlarged beta-function stability matrix in its displayed modal
basis as

```text
B=B0+E.
```

The signed comparator includes the inherited relevant gravity beta mode,
the irrelevant `C^3` beta mode, the source scalar-matter modes, and three
near-canonical gauge-portal modes:

```text
lambda_g=-2.78260869565,
lambda_C3=+7.75000535538,
lambda_scalar=+1.88+-1.28i, +9.69,
lambda_gauge=+2,+2,+2.
```

The nearest real part to the imaginary axis is `delta=1.88`. Bauer-Fike in
this modal basis gives the sufficient signed-index condition

```text
||E_modal||_2 < 1.88.
```

If this holds, no eigenvalue crosses the imaginary axis and the comparator's
one-relevant-mode count is preserved. This is an exact sufficient condition,
not a claim that the MTS matrix satisfies it. The required full `E_modal` has
not yet been calculated.

For a real pair consisting of `lambda_C3` and one matter mode `lambda_m`, the
exact two-by-two condition is

```text
M_hm M_mh < lambda_C3 lambda_m.
```

The resulting product thresholds are tabulated for the real scalar and
canonical portal modes. A seeded random-matrix run is retained only as a
smoke check of the theorem and the failure mode; it is not evidence for the
unknown MTS entries.

## 8. Maxwell and Poynting-vector interface

After electroweak symmetry breaking, the photon combination is

```text
c_gamma=c_B cos^2(theta_W)+c_W sin^2(theta_W).
```

For

```text
L_EM=-F_mn F^mn/4+c_gamma C_mnrs F^mn F^rs,
```

variation with respect to the electromagnetic potential gives

```text
H^mn=F^mn-4c_gamma C^mnrs F_rs,

nabla_m H^mn=J^n,
nabla_[m F_rs]=0.
```

Define the covariant constitutive control parameter

```text
epsilon_CF=4|c_gamma| ||C||_op.
```

Then

```text
||delta H||/||F|| <= epsilon_CF,

||delta T_EM||/||T_EM||
 <=epsilon_CF+O(epsilon_CF^2).
```

The second line includes the Poynting vector: standard electromagnetic energy
flow is recovered only inside the same small-curvature-response gate. Current
conservation follows from antisymmetry of `H`. Stress conservation requires
varying the full nonminimal action; the portal stress cannot be appended by
hand to the Maxwell tensor.

For `F=0`, all `CFF` portals and their tree stress vanish. This proves
uncharged stationary-vacuum silence at tree level, not electromagnetic silence
in matter, clocks, binding energies or wave propagation. The curvature-scale
table is explicitly an internal one-percent control smoke, not an empirical
bound.

## 9. Wilson coefficients: arena count versus action count

The operator quotient forces a distinction that was previously implicit:

```text
uncharged constant-motion vacuum                1
  {A_+(Q_GW)}

photon on a curved background                   2
  {A_+(Q_GW), c_gamma}

unbroken SM parity-even dimension-six gravity   5
  {zeta_+, c_H, c_B, c_G, c_W}

motion scalar plus gravity at six derivatives   5
  {O1,O2,O3,O4,O5}

parity-even unified union                       9
  {shared O3 plus four motion and four SM portals}

including the five GRSMEFT parity partners     14.
```

Therefore “one Wilson coefficient” remains correct only for the selected
uncharged constant-motion vacuum arena. It is not the coefficient count of a
full field theory. The full action contains nine parity-even coefficients
before a UV fixed point or data are used to predict or bound them.

## 10. GR/Newton/Maxwell status

On the weak, uncharged, constant-motion branch,

```text
nabla phi=0,
H=0,
F_X=0,
```

all mixed six-derivative matter portals vanish at tree level. They therefore
do not alter the already calibrated two-derivative Einstein source equation
or Newtonian limit in that arena. The higher-curvature `O3=C^3` coefficient
remains the single active vacuum correction.

For electromagnetic backgrounds, standard Maxwell requires
`c_gamma=0` or `epsilon_CF` below the arena tolerance. Because the parent has
not fixed `c_gamma`, Maxwell recovery is bounded rather than promoted.

This checkpoint retains weak GR/Newton. It does not promote compact GR or the
full MTS-to-GR limit, because the interacting portal beta functions and full
stability matrix remain open.

## 11. Closure ledger

Closed here:

```text
complete CP-even shift-symmetric scalar six-derivative quotient,
complete dimension-six GRSMEFT quotient,
constant-background Hessian selection,
optimized-regulator anomalous-dimension C3 leak,
9801-row direct-leak survival grid,
generic nonzero gauge-portal C3 mixing witness,
signed modal and pairwise stability inequalities,
Maxwell/Poynting constitutive map,
arena-specific and full-action Wilson counts.
```

Still open:

```text
the MTS fixed-point values of O4, c_H, c_B, c_W and c_G,
their complete beta functions and threshold coefficients,
the full numerical off-diagonal stability matrix E_modal,
fermion operators beginning above this dimension,
parent regulator and zero-cosmological trajectory selection,
motion-mode ultraviolet activation,
transition-scale ownership,
an empirical bound or ultraviolet prediction for c_gamma.
```

## 12. Final gate

```text
scalar six-derivative quotient             -> exactly 5, closed;
dimension-six GRSMEFT quotient             -> exactly 10, closed;
free eta=0 C3 source zero                  -> not stable to eta != 0;
direct eta leak stress                     -> 9801/9801 survive;
generic exact C3 block triangularity       -> rejected;
special all-zero portal submanifold        -> possible, not parent-derived;
signed stability preservation              -> ||E_modal||_2<1.88 sufficient;
full MTS E_modal                            -> uncalculated;
vacuum active parity-even coefficients     -> 1;
full parity-even unified coefficients      -> 9 before prediction;
weak GR/Newton                              -> retained;
Maxwell/Poynting                            -> constitutively bounded;
compact and full MTS-to-GR                  -> not promoted.
```

Direct next target:

`4931-Y5-R2FR-gauge-curvature-portal-beta-functions-and-fixed-point-values-or-EM-Wilson-bound.md`

Calculate the parity-even gauge-curvature portal beta block first because it
has an explicit nonzero `C^3` witness and a direct electromagnetic observable.
If the parent projection cannot determine `c_B*` and `c_W*`, derive a sourced
bound on `c_gamma` from propagation, clocks or electromagnetic binding rather
than silently setting the portal to zero.

No GitHub action or public claim is authorized.
