# Wave energy flux and the first averaged mass response

2026-09-09 BST. Private continuation of the retained spherical O4 branch.

## Result and scope

The next temporal flux can be derived rather than left as a conservation
condition. For the incident wave data already selected, its order-u epsilon
phase mean vanishes. A permitted additional incoming amplitude h(v) instead
produces the explicit mean-mass law `c1'=4pi G A h`. The zero is therefore
conditional on the specified input, not a claim about every possible wave.

The calculation also derives a generally nonzero averaged radial mass
correction at order u epsilon squared, and matches the oscillatory mass at
that order against both radial and temporal constraints. This is not a
statement that the coupling has no mass effect.

An exact general-lapse identity isolates the differentiated curvature source.
It provides a useful mass bookkeeping variable without removing that source
from the physical mass. No new empirical coefficient is fitted. A complete
parent evolution, a uniform error bound and a regular black-hole centre are
not established here. Actual symbolic verification is recorded in section 9.

## 1. Source owners and conventions

Preserved inputs:

- `DERIVATION-20260908-coupled-wave-harmonics-and-subleading-mass.md`:
  U1, W1, the integrated scalar responses D1,D3 and subleading mass harmonics.
- `DERIVATION-20260908-spherical-wave-constraints-and-O4-mass-response.md`:
  the covariant spherical O4 stress and exact null-coordinate constraints.
- `scripts/coupled_wave_harmonics_20260908.py`: the preceding 28-check owner,
  whose hash is checked against its completed run before this companion runs.

Use the same signature, units, fixed coupling u=u_O4 and calibrated G:

```text
ds^2=-exp(2delta)F dv^2+2exp(delta)dvdr+r^2 dOmega^2,
F=1-2mu(v,r)/r-Lambda r^2/3,
X=(grad chi)^2, W=C_abcd C^abcd,
L_scalar=-X/2-V(chi)+Q(X)-uWX,
V=m_chi^2 chi^2/2, Q=b2X^2+b3X^3,
kappa=4pi G, P=1-2Q'(X), H=P+2uW.
```

All higher-order results are first order in u on a finite smooth annulus
with r,r0>=r_min>0. Phase averaging holds slow v and r fixed. It is not
identified with an exact finite-time detector average.

## 2. Derive the exact general-lapse mass identities

Let U be the spherical Weyl combination from the source owner, and define

```text
J=-(2u/3)r^2 X U,
b_g=2F/r-F_r-2F delta_r,
K=2F J_r+2exp(-delta)J_v+b_g J,
mathfrak_m=mu-kappa K.                               (1)
```

J includes u; later lower-case j coefficients are per unit u. Substitution
of the covariant source into the two mass equations gives the exact retained
identities

```text
partial_v mathfrak_m = kappa{
 r^2 H chi_v[exp(-delta)chi_v+F chi_r]
 -F_v J_r-(partial_v b_g)J },                         (2)

partial_r mathfrak_m = kappa{
 r^2[P F chi_r^2/2+V+Q'X-Q]
 +u r^2 W F chi_r^2
 +delta_r K-2exp(-delta)delta_vr J }.                 (3)
```

The general lapse is essential. The last two terms in (3) cannot be deleted
by applying the older delta=0 primitive to the corrected metric.

For an independent algebraic route, let B_AB be the reduced Euler tensor of
the curvature variation in the source owner. The two identities reduce to

```text
-2[exp(-delta)B_vv+F B_vr]=K_v-F_v J_r-(b_g)_v J,
2exp(-delta)B_vr=K_r+delta_r K-2exp(-delta)delta_vr J.
```

These hold for arbitrary smooth F, delta and J; the companion derives the
connection from the two-dimensional metric and checks them symbolically.

mathfrak_m is not a replacement observable or a way to discard curvature
energy. The physical geometric mass is still `mu=mathfrak_m+kappa K`.
K contains differentiated fields. This reorganization alone does not remove
higher-derivative modes or prove the retained EFT well posed.

## 3. Retain the incident data and expose the free amplitude mode

Use theta=v/epsilon and the preceding verified reference:

```text
F0=1-2mu0/r-Lambda r^2/3, mu0'=2pi G A^2,
F_ref=F0+epsilon[2pi G A^2 sin(2theta)/r]+...,
delta_ref=-2pi G epsilon^2 A^2 cos^2(theta)(r^-2-r0^-2)+...,
W_ref=W0+epsilon W1+...,
W0=48mu0^2/r^6,
W1=-32pi G mu0 A^2 sin(2theta)/r^6.
```

The ordinary scalar reference includes its B1 sin(theta) and B3 sin(3theta)
corrections. Its response now permits an explicit homogeneous incoming mode:

```text
chi=chi_ref+u{-W_ref chi_ref
 +epsilon^2[D1 sin(theta)+D3 sin(3theta)+h(v)cos(theta)/r]}+... . (4)
```

D1,D3 are the already derived functions, not adjusted for this test. h=0
is the previously chosen input. Nonzero h changes the incoming amplitude at
this relative order. It is legitimate boundary data, not a new fundamental
coupling. Keeping h symbolic tests whether a mean-extraction procedure would
incorrectly report zero even when extra incident energy is supplied.

The leading O4 mass and lapse corrections remain

```text
f0=256pi G mu0 A^2 cos(2theta)/r^5,
delta_O4=128pi G u epsilon mu0 A^2 sin(2theta)/r^6+... .
```

## 4. Evaluate the first subleading temporal flux

Define slow coefficients

```text
L2=A r(-D1+3D3)+A^2[partial_v W0+F0 partial_r W0/2]
   +(16mu0 mu0' A^2-64pi G mu0 A^4)/r^6
   +20b2 W0 A^4/r^3,

L4=-3A rD3+48pi G mu0 A^4/r^6-10b2 W0 A^4/r^3.       (5)
```

The order-u epsilon coefficient of (2), relative to the ordinary reference,
is

```text
partial_v Delta mathfrak_m |_(u epsilon)
 = kappa u epsilon [L2 sin(2theta)+L4 sin(4theta)
                     +2A h sin^2(theta)].           (6)
```

The explicit kinetic-weight flux, induced ordinary flux, quartic variation,
mass/redshift response and the geometric terms of (2) are all retained.
The ordinary B1,B3 contributions cancel from this final expression after
kinetic normalization; they were not set to zero before substitution.
b3 is included in the operator and contributes only at subsequent orders.

The leading order-u epsilon^0 weighted matter flux cancels, as in the
previous calculation. Equation (6) evaluates the next term, rather than
extrapolating that leading cancellation to all orders.

## 5. Derive the mean law and integrate the fast mass

Expand the response, after matching the leading homogeneous mass constant,
as

```text
Delta mathfrak_m=u[epsilon c1(v)+epsilon^2 N2(v,r,theta)+...].
```

Periodicity and (6) require

```text
c1'(v)=kappa A(v)h(v),
c1(v)-c1(v0)=kappa integral_(v0)^v A(s)h(s) ds.       (7)
```

Thus h=0 forces no accumulated mean mass at order u epsilon. A constant c1
still belongs to initial mass data; matching the earlier branch sets its
initial value to zero. For nonzero h, the mean is generally not zero and
obeys (7). This rules out presenting the result as universal absence of
energy transfer or as a universal screening mechanism.

The zero-mean fast particular solution is

```text
N2_osc=-kappa[L2 cos(2theta)/2+L4 cos(4theta)/4
             +A h sin(2theta)/2].                   (8)
```

Its phase derivative, together with c1', reproduces (6). Higher ordinary
curvature coefficients appear in the physical boundary term K, but their
pure phase derivatives cannot supply the mean at this order. The analytic
reason is the integral of a derivative of a periodic function; the companion
also checks this using arbitrary Laurent modes -8 through 8.

## 6. The next averaged radial correction is generally nonzero

Direct expansion of (3) gives, per kappa u epsilon squared,

```text
G2=-C_rad sin^2(2theta)-D_rad cos^2(theta),
C_rad=16b2 W0 A^4/r^4+64pi G mu0 A^4/r^7,
D_rad=6F0 W0 A^2/r^2+m_chi^2 W0 A^2,
<G2>=-(C_rad+D_rad)/2.                              (9)
```

One nontrivial cancellation is worth keeping explicit: the metric-response
part of the ordinary radial matter source cancels the delta_r K term at
this order. The remaining delta_vr J term does not vanish and is included
in the coefficient 64pi G in C_rad. Omitting the lapse terms would change
the averaged source.

Define the derived radial primitive

```text
P2(r)=(128/3)b2 mu0^2 A^4/r^9+(16/3)pi G mu0 A^4/r^6
      +(144/7)mu0^2 A^2/r^7-36mu0^3 A^2/r^8
      +(24m_chi^2-48Lambda)mu0^2 A^2/(5r^5).
```

Then `partial_r P2=<G2>`, and the full particular response at this order is

```text
N2=c2(v)+N2_osc+kappa[P2(r)-P2(r0)].                 (10)
```

This is not merely a radial solution pasted onto a time solution. The
previous scalar transport equations, together with mu0'=2pi G A^2, imply

```text
partial_r L2=D_rad,
partial_r L4=-2C_rad.                               (11)
```

Consequently (8) reproduces the oscillatory radial source in (9), while P2
reproduces its mean. Both constraints agree at their stated orders. c2(v)
is the remaining boundary mean at the next order; its evolution is not
fixed by the already evaluated order-u epsilon flux.

## 7. Restore the physical mass, including the averaged boundary term

Write `J/u=epsilon j1+epsilon^2 j2+...`. The source owner gives
`j1=-8mu0 A^2 sin(2theta)/r^4`. The required mean of j2 simplifies to

```text
j20=-4mu0 A^2/r^5+16mu0^2 A^2/r^6
    +4mu0 A^2(m_chi^2-Lambda/3)/r^3
    +8b2 mu0 A^4/r^7+8mu0 A A'/r^4+(4/3)pi G A^4/r^4.
```

Expanding (1), including the ordinary redshift normalization at r0, yields

```text
<K/u>_(epsilon^2)=K20,
K20=2F0 partial_r j20+2 partial_v j20+(2F0/r-F0_r)j20
    +pi G mu0 A^4[24/r^6+16/(r^4 r0^2)].             (12)
```

The unspecified next periodic j3 drops out of this mean by phase
differentiation; j22,j24 also drop out of (12). The full unaveraged K at this
order is not claimed known solely from its mean.

For the physical mass coefficient M2, (10)-(12) imply

```text
<M2(r)>-<M2(r0)>
 =kappa[K20(r)-K20(r0)+P2(r)-P2(r0)].                (13)
```

The phase means of the preceding K coefficients vanish, so the order-u
epsilon physical mean follows (7). At order-u epsilon squared, (13) is
generally nonzero. Subtracting K as bookkeeping has not hidden its physical
contribution. Boundary mean evolution at this next order remains to be
calculated, not set to zero.

## 8. Bounds, interpretation and the next finite target

At fixed slow time on a finite annulus,

```text
|N2_osc| <= |kappa|(|L2|/2+|L4|/4+|A h|/2),
|c1(v)-c1(v0)| <= |kappa| integral_(v0)^v |A(s)h(s)| ds,
|<M2(r)>-<M2(r0)>|
 <= |kappa|[|K20(r)-K20(r0)|+|P2(r)-P2(r0)|].
```

These are bounds on explicitly derived coefficients, not estimates of the
error between this finite-order candidate and a full solution. Inverse
powers of r still prevent extrapolation to a regular centre. The wave
normalization must remain on K_scalar=1+2uW>0, and the derivative/EFT cutoff
conditions are not replaced by the mean cancellations.

The specific question is answered: the previously selected incident data
do not force order-u epsilon mass accumulation, while a change of incident
amplitude has the definite rate (7), and the next averaged radial mass
response is (13). This is not a theorem for arbitrary multi-ray states or
all boundary preparations.

Next finite target: evaluate the phase-averaged temporal constraint at
u epsilon squared to obtain c2'(v), treating the incoming data explicitly.
Use the exact identities (2)-(3) to avoid rebuilding the differentiated
curvature source. Complete the necessary next scalar/reference coefficients
rather than dropping them. After matching that order, seek a controlled
annular remainder estimate for the selected retained system. No local-GR,
empirical, regular-black-hole or unification gate is promoted here.

## 9. Reproducible verification

Companion: `scripts/wave_energy_flux_and_mean_mass_20260909.py`.
Completed run directory:
`source-intake/navier-stokes/20260909/wave-energy-flux-staged-series/`.
The script preserves its executed source, input hashes, incremental status
and a COMPLETE marker only after every check passes. It uses one logical CPU
at BelowNormal priority with numerical-library threads limited to one.

Checks cover both exact general-lapse identities, direct flux extraction,
the h-dependent mean law and nonzero-input control, the integrated fast
response, full radial extraction and radial/time compatibility, mean radial
integration, and restoration of the physical mean boundary contribution.

Actual result: **23/23 symbolic checks passed**, each with zero remainder,
completed `2026-09-08T23:37:41.274135+00:00`. The completed script and executed
snapshot have matching SHA-256:
`b85bb748ddc4b7d40bd43f337d5ebd638a1aab6e5df77420d9fb92d53b295274`.
All three input hashes match their current source files. COMPLETE matches
the status timestamp, and `valid_for_mts_completion_claim` remains false.
An independent in-memory compile passes; no scripts/__pycache__ exists and
no energy-flux worker remains running after completion.

The earlier directory
`source-intake/navier-stokes/20260909/wave-energy-flux-initial/`
is deliberately preserved. That single-core attempt passed its first ten
checks but spent excessive time expanding polynomial orders that would be
discarded. Its verified owned worker was interrupted at 23:36:35 UTC;
`INTERRUPTED.json` records the lifecycle and supersedes its last incremental
"running" status. It has no COMPLETE marker and is not counted as a finished
run. The revised calculation truncates nonnegative series products after
each factor, adds a direct-expansion regression control, and finishes in
approximately 18 seconds. The two attempts ran serially. This optimization
does not alter the retained orders or erase the interrupted evidence.

These checks verify the stated algebraic identities and coefficient
equations, not convergence of the asymptotic series, independent empirical
confirmation, or a solution of the full parent field equations. For shell
rechecks, preserve JSON timestamps as strings (`ConvertFrom-Json -DateKind
String`) rather than comparing PowerShell's auto-converted local DateTime
display against the literal UTC COMPLETE marker.

All work is private and remains under post-checkpoint-work. Earlier source
snapshots, the D4/stellar evidence, RH jobs and Desktop Commander are not
modified by this calculation.
