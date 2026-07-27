# 4988 - Renormalized scalar two-particle cut and exact partial-wave projection

Date: `2026-07-14`

Marker: `MTS_4988_SCALAR_TWO_PARTICLE_CUT_SOFT_SUBTRACTION`.

Status: private derivation checkpoint. This evaluates one of the four
surviving cut classes isolated in checkpoint 4987. It does not assign the
full values of `K_mu` or `K_ang`.

## 1. Result

The rational-free scalar-scalar two-particle cut is no longer an unevaluated
symbol. The complete cut-constructible one-loop four-scalar logarithm has
been put in the same canonical normalization as checkpoint 4985, its
nonintegrable gravitational endpoint pole has been subtracted, and its
`J=0,2` partial waves have been integrated exactly.

The regularized hard partial waves are

```text
h0(L)=18161/34560+13pi^2/288-(203/384)L,
h2(L)=-621877/864000+173pi^2/1440-(203/9600)L,

L=ln(s/mu^2).
```

At `L=0`,

```text
h0=0.97099487458620947469,
h2=0.46595826022346692666.
```

All `zeta(3)` endpoint moments cancel in both totals. Independent
70-digit transformed-endpoint quadrature agrees with the exact expressions
to `3.63e-71` in the generator and to better than `1e-70` on unseen points
in the independent validator.

## 2. Canonical normalization

Dunbar and Norridge display the four-scalar tree in an older external-state
convention. On `s+t+u=0`, its kinematic bracket obeys

```text
(1/2)[(t^2+u^2)/s+(s^2+u^2)/t+(s^2+t^2)/u]
 =-[tu/s+su/t+st/u].
```

The normalization is not inferred from that formula alone. Recomputing the
canonical scalar-graviton vertex contraction in de Donder gauge gives

```text
T12 P T34=-tu,
i M_s=i(kappa^2/4)tu/s,
i M_tree=i(kappa^2/4)[tu/s+su/t+st/u].
```

Thus, with

```text
kappa^2=32pi G=4/M_P^2,
M_P^-2=8pi G,
```

the canonical tree is the one already used and independently checked in
checkpoint 4985. The displayed Dunbar four-scalar logarithmic coefficients
are calibrated by the same four-external-scalar normalization, giving the
canonical one-loop hard prefactor

```text
M_hard^(1)=i[kappa^4/(4pi)^2]s^2 h(x,L),
kappa^4/(4pi)^2=64G^2.
```

This explicit calibration prevents a silent factor-four convention change.

## 3. Physical-channel hard kernel

Use

```text
s=1,
t=-x,
u=-(1-x),
x=(1-z)/2,

l_s=L-i pi,
l_t=L+ln x,
l_u=L+ln(1-x).
```

The real cut-constructible one-loop hard function is assembled from the
three crossed box-log products, three squared-log terms, the triangle
combination, and the `163,43,163` bubble coefficients in the archived
Dunbar-Norridge source. The finite local rational polynomial is set to zero
by the declared 4987 rational-free convention.

Before the two-loop phase-space projection,

```text
lim[x h_raw]_(x->0)=-pi^2/16,
lim[(1-x)h_raw]_(x->1)=-pi^2/16.
```

The crossing-even singular subtraction is therefore

```text
h_soft=pi^2/[16x(1-x)]
      =pi^2/[4(1-z^2)],

h_reg=h_raw+h_soft.
```

It removes both nonintegrable residues exactly. This singular part is
unique among crossing-even simple-pole subtractions. Integrable finite local
terms are still scheme coordinates and are not declared unique.

The regular kernel collapses to

```text
h_reg(x,L)=C0(x)+L C1(x),
C1(x)=-(203/320)(x^2-x+1),
C2(x)=coefficient of L^2=0.
```

Writing `X=ln x` and `Y=ln(1-x)`, the exact constant part is

```text
C0=cXX X^2+cXY XY+cYY Y^2+cX X+cY Y+cPi,

cXX=(x^4+x^3-4x^2+6x-3)/[16(x-1)],
cXY=-(2x^4-4x^3+6x^2-4x+1)/[8x(x-1)],
cYY=-(x^4-5x^3+5x^2-5x+1)/(16x),
cX =-(163x^2-283x+283)/960,
cY =-(163x^2-43x+163)/960,
cPi=-pi^2(3x^2-3x+1)/16.
```

The vanishing `L^2` coefficient and the surviving `203/320` slope are
derived by symbolic cancellation, not fitted.

## 4. Exact angular integration

The partial-wave convention is

```text
h_J(L)=integral_0^1 dx P_J(1-2x) h_reg(x,L).
```

No black-box symbolic antiderivative is used. Polynomial moments follow
from beta-function derivatives, while the only endpoint moments are

```text
integral ln^2(x)/(1-x) dx=2 zeta(3),
integral ln^2(1-x)/x dx=2 zeta(3),
integral ln(x)ln(1-x)/x dx=zeta(3),
integral ln(x)ln(1-x)/(1-x) dx=zeta(3).
```

For `J=0`, the six component integrals group as

```text
2 cXX =6635/6912-zeta(3)/4,
cXY   =-395/432+zeta(3)/4+11pi^2/144,
cX+cY =8293/17280,
cPi   =-pi^2/32.
```

For `J=2`, they group as

```text
2 cXX =566743/864000-zeta(3)/4,
cXY   =-160967/108000+zeta(3)/4+91pi^2/720,
cX+cY =24779/216000,
cPi   =-pi^2/160.
```

The exact totals are the `h0,h2` expressions in section 1.

## 5. Scalar-cut projection

For two massless intermediate scalars, the identical-state factor `1/2`
is cancelled by the two loop placements `A^(0)A^(1)+A^(1)A^(0)`. With
the phase-space and partial-wave conventions already used in 4985,

```text
Disc_s=i/(8pi) sum_J (2J+1)a_J^(0)a_J^(1)P_J(z).
```

Using

```text
a0_GR=-11/6,
a2_GR=-1/30,
s/M_P^2=8pi Gs,
kappa^4/(4pi)^2=64G^2,
```

the scalar-cut contribution to the reduced discontinuity is

```text
D_phiphi(z,L)
 =-32/pi sum_J (2J+1)aJ_GR hJ(L)P_J(z)
 =d0_phi(L)+d2_phi(L)P2(z),

d0_phi(L)=143(120pi^2+1397)/(6480pi)-[2233/(72pi)]L,
d2_phi(L)=(-621877+103800pi^2)/(162000pi)-[203/(1800pi)]L.
```

At `L=0`,

```text
d0_phi=18.1325330568554,
d2_phi=0.791035310816687,

A_phi=d0+d2
     =(242911+29600pi^2)/(9000pi)
     =18.9235683676721,

B_phi=-6d2
     =(621877-103800pi^2)/(27000pi)
     =-4.74621186490012.
```

Applying the exact 4987 inverse projector to `D_phiphi` gives the additive
scalar-cut invariant subtotals

```text
Delta K_mu_phi(L)
 =(-135061+1500pi^2)/(450pi)+[1827/(10pi)]L,

Delta K_ang_phi(L)
 =(13357+24075pi^2)/(3375pi)-[9541/(300pi)]L.
```

Their `L=0` values are

```text
Delta K_mu_phi=-85.0641390166317,
Delta K_ang_phi=23.6697802325722.
```

These values are exact additive subtotals. Bern's convention gives
`D_phiphi=-U_phiphi/(2pi s^3)`, while the real master contains
`2D_phiphi`. The `-6(d0-5d2)` inverse map already combines that factor two
with the cyclic-channel factor three. Multiplying the displayed values by
two again would double count the master normalization. They are not the
complete `K_mu` or `K_ang` invariants because the other cut classes remain.

## 6. Master-subtraction boundary

The nonzero `L` slopes are deliberately retained. The two-loop master is

```text
Pi_stu[-C2_ren/pi-D1 ReF1]=-K_mu stu,
```

and the `D1 ReF1` term is applied once to the complete four-class cut sum,
not once per class. Therefore it would be incorrect either to allocate that
global subtraction to this cut or to call the `L=0` subtotal a complete
physical invariant. The factor-two normalization is already encoded in the
inverse projection above, and only the complete master may be required to
have zero scale slope.

Still open:

```text
global D1 ReF1 normalization and subtraction,
opposite-helicity hh two-particle cut,
mixed-helicity hhh three-particle cut,
phiphih three-particle cut,
numeric full K_mu and K_ang,
finite C_w,
exact all-operator local GR,
full MTS.
```

## 7. Validation and next target

The generator closes `12/20` gates; the eight open rows are deliberate
master/nonclaim gates. The independent validator rebuilds the calculation
without importing the generator and passes `443/443` checks, including the
factor-two/no-double-counting check. Its maximum
direct-versus-decomposed kernel residual is `2.20e-79`.

Primary outputs:

- `post-checkpoint-work/source-intake/functional_rg/4988/canonical_tree_normalization_checks.csv`
- `post-checkpoint-work/source-intake/functional_rg/4988/one_loop_hard_kernel_decomposition.csv`
- `post-checkpoint-work/source-intake/functional_rg/4988/two_loop_soft_endpoint_subtraction.csv`
- `post-checkpoint-work/source-intake/functional_rg/4988/scalar_cut_partial_wave_integrals.csv`
- `post-checkpoint-work/source-intake/functional_rg/4988/scalar_cut_channel_projection.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4988_VALIDATION.csv`

Next target: derive the `D1 ReF1` contribution in exactly the same reduced
normalization and turn cancellation of the total `L` dependence into a
hard sum rule for the remaining three cuts. Then evaluate the
opposite-helicity `hh` two-particle class.

No GitHub action.
