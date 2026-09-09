# Coupled wave harmonics and subleading mass response

2026-09-08 UTC. Private continuation; no GitHub action.

## What this step derives

The curvature-potential response is combined with the wave's own geometry
and the quartic kinetic interaction, rather than treated as an isolated
fixed-background correction. This yields explicit first- and third-harmonic
scalar responses and a second/fourth-harmonic subleading mass response.

An important term was absent from the earlier fixed-Vaidya approximation:
the ordinary order-epsilon-squared redshift contributes at order epsilon to
curvature because curvature differentiates it in time. Its inclusion changes
the first oscillatory Weyl-squared coefficient by a factor of three relative
to keeping the oscillatory mass alone. The earlier fixed-background results
retain their stated scope; they are not the complete coupled expansion.

This is finite-order equation matching on a finite annulus, not a proof of
existence, a uniform EFT error estimate, a regular centre, or completed MTS.
The source/response identities have a runnable symbolic companion; actual
validation outcomes are recorded in section 8.

## 1. Owners, conventions and expansion order

Immediate owners, preserved unchanged:

- `DERIVATION-20260908-spherical-wave-constraints-and-O4-mass-response.md`:
  covariant retained O4 source, exact spherical constraints and linearization.
- `DERIVATION-20260908-Navier-Stokes-to-MTS-wave-stress-and-collapse-bridge.md`:
  incident wave, ordinary first/third harmonics and averaged leading mass law.

Use the same action block, signature (-,+,+,+), c=hbar=1, geometric mass mu,
calibrated G, scalar mass m=m_chi, and fixed coefficients:

```text
L_matter = -X/2-m^2 chi^2/2 + b2 X^2+b3 X^3 -u W X,
X=(grad chi)^2,       W=C_abcd C^abcd,       u=u_O4,
ds^2=-exp(2delta)F dv^2+2exp(delta)dvdr+r^2 dOmega^2,
F=1-2mu(v,r)/r-Lambda r^2/3.
```

Retain first order in u. At this stage the scalar equation is matched through
u epsilon, the radial mass equation through u epsilon, the temporal mass
equation through u epsilon^0, and the leading u epsilon redshift equation.
The differing orders reflect the fast derivative, not an assertion that
every equation is solved to the same absolute remainder order.

Take theta=v/epsilon, r,r0>=r_min>0, and smooth slow amplitudes on a finite
time interval. Partial_v acting on coefficient functions is slow; the full
derivative is D_v=partial_v+epsilon^-1 partial_theta. Coefficients below
exclude their displayed powers of u and epsilon.

## 2. The reference must include its unaveraged geometry

Write

```text
F0=1-2mu0(v)/r-Lambda r^2/3,      mu0'=2pi G A^2,

mu_ref = mu0+epsilon mu1+...,
mu1 = -pi G A^2 sin(2theta),
F_ref = F0+epsilon F1+...,        F1=-2mu1/r,

delta_ref=epsilon^2 d2+...,
d2=-2pi G A^2 cos^2(theta)(r^-2-r0^-2).
```

The leading unaveraged temporal constraint is
`mu0'+partial_theta mu1=4pi G A^2 sin^2(theta)`, not just its phase mean.
The radial redshift equation gives `partial_r d2=4pi G A^2 cos^2(theta)/r^3`.
The chosen r-independent part fixes the reference lapse normalization at r0;
it has no effect on the curvature coefficient below.

For `U=R_h+2 Box_h r/r+2(1-F)/r^2`, use the exact general-gauge formula
from the preceding note before expanding:

```text
U0=12mu0/r^3,
U1=-F1_rr+2F1_r/r-2F1/r^2-2 partial_theta partial_r d2
   =-4pi G A^2 sin(2theta)/r^3,

W_ref=W0+epsilon W1+...,
W0=48mu0^2/r^6,
W1=2U0 U1/3=-32pi G mu0 A^2 sin(2theta)/r^6.          (1)
```

Without d2, U1 would incorrectly be -12pi G A^2 sin(2theta)/r^3 for this
coupled reference. Dropping a term merely because its metric amplitude is
order epsilon squared is not valid inside a differentiated curvature source.

The ordinary scalar reference is

```text
chi_ref=epsilon A cos(theta)/r
        +epsilon^2[B1 sin(theta)+B3 sin(3theta)],

B1=A/(2r)[(m^2-2Lambda/3)(r-r0)+mu0(r0^-2-r^-2)]
   +b2 A^3/(3r)(r0^-3-r^-3),
B3=5b2 A^3/(9r)(r^-3-r0^-3).                         (2)
```

These obey the ordinary scalar equation through order epsilon. Further
ordinary mass/flux corrections are still required at subsequent orders.

## 3. Combine curvature normalization, metric response and nonlinear matter

Use the already derived leading geometric responses per unit u:

```text
M0=-128pi G mu0 A^2 cos(2theta)/r^4,
f0=-2M0/r=256pi G mu0 A^2 cos(2theta)/r^5,
d1=128pi G mu0 A^2 sin(2theta)/r^6,

F=F_ref+u f0+...,
delta=delta_ref+u epsilon d1+....
```

The physical scalar candidate is

```text
chi=chi_ref+u{-W_ref chi_ref
             +epsilon^2[D1 sin(theta)+D3 sin(3theta)]}+... . (3)
```

The product in braces is retained through epsilon squared. In particular it
contains both -epsilon W1 times the leading scalar and -W0 times its ordinary
harmonic correction. Omitting either changes the next-order forcing.
The normalization is perturbative: K=1+2uW must remain positive on the
chosen branch, and omitted u-squared terms are not presumed uniformly small
as epsilon tends to zero at fixed u.

Define the slow curvature-potential coefficient

```text
V4=-960mu0 mu0'/r^7+1440mu0^2/r^8-3456mu0^3/r^9
   -(288Lambda+96m^2)mu0^2/r^6.                      (4)
```

Direct substitution into the retained scalar equation gives, at order
u epsilon before solving D1,D3,

```text
E_scalar/(u epsilon) =
 [R1+2 partial_r(rD1)/r]cos(theta)
 +[R3+6 partial_r(rD3)/r]cos(3theta),

R1=-A V4/r+320pi G mu0 A^3/r^8+116b2 W0 A^3/r^5,
R3=         320pi G mu0 A^3/r^8-244b2 W0 A^3/r^5.     (5)
```

All lower displayed scalar residual coefficients cancel. Equation (5)
retains the unaveraged metric and matter terms; it is not obtained by setting
mean X or the quartic coefficient to zero. The b3 terms are included in the
companion operator and first contribute at a later epsilon order.

The geometric contribution in (5) has two parts. The ordinary oscillatory
curvature yields `Box(epsilon W1)|epsilon^0=640pi G mu0 A^2 cos(2theta)/r^7`.
The induced f0 contributes `1280pi G mu0 A^3 cos(theta)cos(2theta)/r^8` to
the scalar residual divided by u epsilon. Their difference produces the
320 coefficients after decomposing cos(theta)cos(2theta). The u epsilon
redshift d1 itself enters the scalar equation later for this one-ray seed;
this does not license dropping the ordinary d2 from (1).

For clarity, kinetic normalization also changes the nonlinear interaction.
With chi=(1-uW)psi, the leading X variation is -8uW0 X rather than just
-2uW0 X, because W0 has a radial derivative. Expansion of the transformed
quartic scalar equation yields
`b2 W0 A^3[116cos(theta)-244cos(3theta)]/r^5` at order u epsilon.
These coefficients are checked against direct substitution into the original
scalar operator, rather than accepted from a normalization analogy alone.

## 4. Solve the two coupled transport equations

Equation (5) requires

```text
partial_r(rD1)=A V4/2-160pi G mu0 A^3/r^7-58b2 W0 A^3/r^4,
partial_r(rD3)=-(160/3)pi G mu0 A^3/r^7+(122/3)b2 W0 A^3/r^4.
```

Set

```text
H_V(r)=80mu0 mu0'/r^6-720mu0^2/(7r^7)+216mu0^3/r^8
       +(144Lambda+48m^2)mu0^2/(5r^5).
```

The explicit particular solutions with D1(r0)=D3(r0)=0 are

```text
D1={A[H_V(r)-H_V(r0)]
    +(80/3)pi G mu0 A^3(r^-6-r0^-6)
    +(928/3)b2 mu0^2 A^3(r^-9-r0^-9)}/r,

D3={(80/9)pi G mu0 A^3(r^-6-r0^-6)
    -(1952/9)b2 mu0^2 A^3(r^-9-r0^-9)}/r.             (6)
```

There are no new fitted coefficients in (6). Independent incident harmonic
data could add homogeneous functions divided by r; they have not been
invented to cancel a test. The zero values here specify the extra normalized
harmonic data at the reference boundary. Even at b2=0 the self-gravitating
geometry produces a third harmonic, unless its amplitude also vanishes.

In canonical four-dimensional dimensions, [u]=[b2]=L^4, [G]=L^2,
[A]=L^-1, [mu0]=L, and [D1]=[D3]=L^-7. Thus u epsilon^2 Dj has the required
scalar dimension L^-1. The formulas have no division by F0 and remain
coordinate-regular at a simple F0=0 sphere with r>0. Their inverse powers of
r do not establish a regular centre.

## 5. Integrate the subleading mass without violating the time constraint

Write `X_ref=epsilon X1+epsilon^2 X2+...`. Let

```text
X1=A^2 sin(2theta)/r^3,
X2=X20+X22 cos(2theta)+X24 cos(4theta),

X20=-A B1_r/r-A(A'/r+B1)/r^2+F0 A^2/(2r^4),
X22= A B1_r/r-A B3_r/r-A(A'/r+B1)/r^2
     -3A B3/r^2+F0 A^2/(2r^4),
X24= A B3_r/r-3A B3/r^2.
```

All quantities on the right are fixed by (2). For the curvature multiplier
per unit u, write `J/u=epsilon j1+epsilon^2 j2+...`. Equation (1) gives

```text
j1=-8mu0 A^2 sin(2theta)/r^4,
j2=j20+j22 cos(2theta)+j24 cos(4theta),
j20=-8mu0 X20/r+(4/3)pi G A^4/r^4,
j22=-8mu0 X22/r,
j24=-8mu0 X24/r-(4/3)pi G A^4/r^4.                   (7)
```

The previously derived source primitive now supplies

```text
Delta mu_O4=u[M0+epsilon M1]+...,
M1=C2 sin(2theta)+C4 sin(4theta),

C2=4pi G[48F0 mu0 A^2/r^5+8F0_r mu0 A^2/r^4
          -16(mu0' A^2+2mu0 A A')/r^4-4j22],
C4=-32pi G j24.                                     (8)
```

This is the radial primitive evaluated, not an unknown local amplitude.
It follows from

```text
M0=8pi G partial_theta j1,
M1=4pi G[2F0 j1_r+2 partial_v j1+2 partial_theta j2
         +(2F0/r-F0_r)j1].
```

The direct bulk term in the O4 mass primitive and the induced ordinary
radial matter variation start at u epsilon squared here. The induced
ordinary time flux does not: its leading term cancels the explicit O4
kinetic time flux, and is included when verifying the temporal constraint.

With that term retained, (8) satisfies both radial orders u epsilon^0 and
u epsilon^1 and both temporal orders u epsilon^-1 and u epsilon^0. The
same calculation checks the leading redshift response. It does not yet
match the time constraint at u epsilon^1.

The displayed periodic particular mass has zero phase mean. That is not a
claim that the full physical mean mass shift vanishes. Homogeneous boundary
mass data and subsequent orders remain; they cannot be assigned arbitrarily
while prescribing an incompatible boundary flux.

## 6. Explicit finite-annulus bounds for the calculated terms

At fixed slow time, let `Delta_p=|r^-p-r0^-p|` and

```text
H_bound=80|mu0 mu0'| Delta_6+(720/7)mu0^2 Delta_7
        +216|mu0|^3 Delta_8
        +|144Lambda+48m^2|mu0^2 Delta_5/5.
```

Then the derived solutions obey

```text
|D1| <= [|A|H_bound+(80/3)pi|G mu0||A|^3 Delta_6
         +(928/3)|b2|mu0^2|A|^3 Delta_9]/r,
|D3| <= [(80/9)pi|G mu0||A|^3 Delta_6
         +(1952/9)|b2|mu0^2|A|^3 Delta_9]/r,

|Delta mu_O4,matched|
 <= |u|[128pi|G mu0|A^2/r^4+epsilon(|C2|+|C4|)].     (9)
```

These are elementary bounds on explicit finite-order terms. They become
uniform coefficient bounds on a compact annulus with bounded A, A', mu0,
mu0' and fixed finite coefficients. They are not bounds on the error between
the candidate and an actual solution of the full parent equations.

For trapping against a reference F0<=-sigma<0, the appropriate condition
remains `2|Delta mu_total|/r<sigma`, not just the contribution (9). The
ordinary corrections, boundary modes, omitted parent operators and coupled
remainder must still enter the total. No uncomputed remainder is set to zero.

## 7. The next calculation and the remaining boundary

The scalar coupling correction through u epsilon is now explicitly filled,
including its self-gravitating and b2 pieces. The subleading mass response
also has matching radial and leading temporal checks. This is a substantive
advance over leaving D_g and D_chi as uncomputed response operators.

Next: calculate the temporal mass flux at u epsilon, derive any forced mean
or homogeneous boundary mass evolution, and match it with the u epsilon^2
radial/scalar corrections. Then seek an energy/remainder estimate for the
selected order-reduced system on the annulus. The first target must be an
actual flux calculation, not another search for numerical coupling rows.

A regular-centre regime, higher-derivative EFT control and omitted same-order
parent operators remain separate necessary work. This note neither declares
those impossible nor assumes them solved. No observable, local-GR, black-hole
completion or unification gate is promoted.

## 8. Reproducible verification

Companion: `scripts/coupled_wave_harmonics_20260908.py`, one logical CPU,
BelowNormal priority, numerical-library threads set to one. Laurent Fourier
polynomials use z=exp(i theta), allowing exact coefficient extraction without
phase quadrature. Fluxes are truncated high enough before differentiation to
retain every requested residual coefficient; the ingoing gauge has no bare
second-v-derivative scalar principal term that would invalidate that count.

Initial run: `source-intake/navier-stokes/20260908/coupled-wave-harmonics-initial/`.
It records 25/27 passed, with two failures caused by extracting epsilon
coefficients from a factored mass polynomial without first expanding it.
Its executed source and failure remainders are preserved; it has no COMPLETE
marker. It is not promoted as a passing run.

Correction: expand the mass polynomial before coefficient extraction and
add a regression check that its extracted coefficients reconstruct it.
The fresh run is
`source-intake/navier-stokes/20260908/coupled-wave-harmonics-expanded/`.
Require its actual status and COMPLETE marker; a written formula is not a
substitute for the run finishing. Both runs retain false completion-claim
flags, and no previous evidence files are overwritten.

### Completed result

The revised run completed at `2026-09-08T23:11:23Z` (00:11 BST September 9):
**28/28 checks passed**, all with zero symbolic remainder, SymPy 1.14.0.
The status, COMPLETE marker and executed-source hash were independently
checked after exit. The live script matches its revised executed snapshot:

```text
initial failed source: 118e8f0961220818f358f956192f1be26112206cc5795cb091f0c7ca76561958
revised passed source: 82e80c55bff64f1b7ba817562379339054e9f8d1b093d960b75dbf2a201bd3c2
```

The original two failure remainders and failed status remain intact. The
previous 31-check and 16-check companion scripts still match their frozen
executed-source hashes. Immediate cited paths exist; no scripts bytecode
directory was created. Both runs were serial, one core BelowNormal, and have
exited. No RH worker, Desktop Commander process, or other agent was modified.

The passing result covers the finite-order identities and cancellations
listed here. It does not certify the omitted mass-flux order, a uniform
remainder bound, the full parent system or a regular black-hole interior.
