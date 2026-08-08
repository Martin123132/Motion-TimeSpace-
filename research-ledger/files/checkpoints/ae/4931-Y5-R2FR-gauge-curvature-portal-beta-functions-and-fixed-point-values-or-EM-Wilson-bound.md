# 4931 - Gauge-curvature portal running, threshold matching and EM Wilson bound

Marker: `MTS_GAUGE_CURVATURE_PORTAL_MATCHING_EM_BOUND_4931`.

Date: `2026-07-12`.

Status: private derivation and source-backed bound checkpoint; no public MTS,
local-GR or Maxwell-emergence claim.

## 1. Question and result

Checkpoint 4930 proved that the parity-even gauge-curvature portals are real
essential directions and that a nonzero portal generically mixes into the
Weyl-cubic sector. It left two alternatives:

```text
calculate the portal beta block and fixed point,
or derive a sourced low-energy electromagnetic Wilson bound.
```

Checkpoint 4931 closes a substantial part of both routes.

The source-locked perturbative result is

```text
minimal massless Einstein-Maxwell/Yang-Mills:
    one-loop additive CFF divergence at u_X=0 = 0;

massive charged Dirac matter:
    finite CFF threshold != 0.
```

Thus the portal is neither generically forced to zero nor an arbitrary
unstructured coefficient. Between thresholds, `u_X=0` is a perturbative
one-loop additive-zero manifold. At each charged mass threshold, a finite,
calculable Wilson coefficient is generated. The remaining ultraviolet
unknown is a parent matching coefficient and the full nonperturbative
anomalous/mixing block.

For the electron, in the declared MTS convention,

```text
c_gamma,e = -9.621568578321357e-31 m^2,
sqrt(|c_gamma,e|) = 9.808959464857297e-16 m.
```

The free `e+mu+tau` subtotal is

```text
c_gamma,leptons = -9.621794423569482e-31 m^2.
```

The known QED baseline is more than `6.23e36` below the legacy pulsar
positive-side bound scale. It is therefore negligible for the tabulated
astrophysical tests. This does not bound an independent MTS parent
coefficient without the stated observational assumptions.

## 2. Operator and convention lock

The retained photon action is

```text
L_EM = -F_mn F^mn/4
       + c_gamma C_mnrs F^mn F^rs.
```

The dimensionful coefficient `c_gamma` has units of length squared. The
source GRSMEFT normalization is

```text
L_6 contains (c_3/Lambda^2) B^mn B^rs C_mnrs.
```

All signs in this checkpoint use the curvature convention of the locked
GRSMEFT source. Independent QED calculations are used to verify the magnitude
because their Riemann conventions can reverse the displayed sign.

On a Ricci-flat background,

```text
R_mn=0  =>  R=0,
Riemann_mnrs=C_mnrs,
L_doubledual_mnrs F^mn F^rs=Riemann_mnrs F^mn F^rs.
```

Only in this arena may the legacy `lambda Riemann F F` and Horndeski `alpha`
rows be identified directly with `c_gamma`. The identification is not made in
matter-filled or cosmological backgrounds where Ricci operators are active.

Source files and hashes are locked in
`source-intake/functional_rg/4931/PROVENANCE.md`.

## 3. Perturbative beta boundary

Define the dimensionless portal coordinate

```text
u_X(k)=k^2 c_X(k).
```

The general local beta function has the form

```text
beta_uX=(2+gamma_X)u_X
        +b_X(g_N,gauge,matter,...)
        +O(u_X^2).
```

Here `2u_X` is canonical scaling, `gamma_X` is the multiplicative anomalous
dimension of the inserted operator, and `b_X` is the inhomogeneous source
which can generate the portal even when `u_X=0`.

The locked GRSMEFT source states that the leading Einstein-Maxwell action has
no one-loop divergence for the on-shell `X X C` operator. It relates the U(1)
zero to vector-field duality. The corresponding Einstein-Yang-Mills zero is
related to its supersymmetry embedding. Therefore,

```text
b_gamma^(1)|u=0=0,
b_W^(1)|u=0=0,
b_G^(1)|u=0=0
```

for the stated minimal massless one-loop systems and on-shell basis.

This yields the perturbative fixed manifold

```text
u_X*=0,
theta_X=-(2+gamma_X*).
```

If one additionally makes the explicit strict-canonical approximation
`gamma_X=0`, then

```text
beta_uX=2u_X,
u_X*=0,
theta_X=-2.
```

The last line is a comparator, not the full MTS fixed point. The source does
not determine the multiplicative insertion anomalous dimension, two-loop
inhomogeneous terms, regulator dependence, mixed MTS Hessians, or the
nonperturbative fixed point.

## 4. Finite charged-matter matching

The same source gives a finite unit-hypercharge Dirac threshold,

```text
c_3=-(1/90)(g'/(4pi))^2.
```

In canonical QED this becomes

```text
Delta c_gamma
 =-Q^2 e^2/[90(4pi)^2 m^2]
 =-Q^2 alpha_EM/(360pi) (hbar/(m c))^2.
```

The independent QED effective action in `1609.00723` contains

```text
(a,b,c,d)=1/[180(4pi)^2](5,-26,2,24)
```

in the noncanonical photon normalization `-F^2/(4e^2)`. Rescaling the photon
to canonical normalization gives

```text
|Delta c_gamma|=e^2/[90(4pi)^2m^2],
```

which exactly checks the magnitude. The worldline/heat-kernel source
`0812.4849` independently reproduces the Drummond-Hathrell coefficient.

Using the locally installed SciPy physical constants gives

| free Dirac particle | `Delta c_gamma` (`m^2`) | relative to electron |
|---|---:|---:|
| electron | `-9.621568578321357e-31` | `1` |
| muon | `-2.2504949261146214e-35` | `2.3390104303629645e-5` |
| tau | `-7.95755513350286e-38` | `8.270538289808861e-8` |
| sum | `-9.621794423569482e-31` | `1.0000234728096866` |

The sum is not the full Standard-Model threshold. The correct decomposition
is

```text
c_gamma^IR
 =c_gamma^parent(mu_match)
  +c_gamma^free-leptons
  +c_gamma^QCD/hadronic
  +c_gamma^EW-spin1
  +... .
```

Current quarks are not inserted as free `1/m_q^2` thresholds below
confinement. The QCD contribution requires hadronic matching. The charged-W
term requires its own spin-1 coefficient in the identical convention.

## 5. Electroweak projection

With

```text
B=c_W A-s_W Z,
W3=s_W A+c_W Z,
```

the neutral portals project to

```text
c_gamma=c_B cos^2(theta_W)+c_W sin^2(theta_W),

c_Z=c_B sin^2(theta_W)+c_W cos^2(theta_W),

c_AZ=2 sin(theta_W)cos(theta_W)(c_W-c_B).
```

Consequently a photon bound supplies only the strip

```text
|c_B cos^2(theta_W)+c_W sin^2(theta_W)+c_thresholds|
 <=B_gamma.
```

It does not separately determine `c_B` and `c_W`, and it says nothing direct
about `c_G`. This prevents an electromagnetic bound from being overcounted as
three ultraviolet portal predictions.

## 6. Maxwell variation and stress identity

Varying the retained action with respect to `F_mn` gives the excitation

```text
H^mn=F^mn-4c_gamma C^mnrs F_rs.
```

Varying `A_n` gives

```text
nabla_m H^mn=J^n,
nabla_[m F_rs]=0.
```

Antisymmetry of `H` then yields exact current conservation,

```text
nabla_n J^n=0.
```

The complete Hilbert stress is defined by varying Maxwell plus the portal,
not by appending a force term to the Maxwell tensor. Diffeomorphism invariance
and the electromagnetic equation give

```text
nabla_m T_EM,total^(mn)=-F^(n m)J_m.
```

Thus the source-free total electromagnetic stress is covariantly conserved.
The constitutive/Poynting control parameter is

```text
epsilon_CF=4|c_gamma|||C||_op,

||delta H||/||F||<=epsilon_CF.
```

This is a rigorous excitation bound. The full local Hilbert stress also
contains terms generated by metric variation of the curvature operator,
including derivative terms. Those cannot be assigned the same simple bound
without specifying an electromagnetic profile scale.

## 7. Photon characteristic and birefringence

Use the geometric-optics form

```text
A_m=a_m exp(i theta/epsilon),
k_m=nabla_m theta,
k.a=0.
```

Keeping the two-phase-derivative terms gives

```text
[k^2 delta^nu_sigma
 -8c_gamma k_mu C^(mu nu rho)_sigma k_rho]a^sigma=0.
```

For a unit transverse polarization `f`,

```text
k^2
 =8c_gamma C_mrns k^m k^n f^r f^s.
```

Equivalently, on a transverse screen basis `e_A`, define

```text
K_AB=C_mrns l^m l^n e_A^r e_B^s.
```

The two physical characteristics are the two eigenvalues of this real tidal
matrix. Both sides of the dispersion equation are quadratic in `k`, so the
leading local dimension-six correction is polarization dependent but not
dependent on the magnitude of the photon frequency. Higher-derivative and
nonlocal loop terms may restore frequency dependence and are outside this
truncation.

For Schwarzschild,

```text
p^2=+/-12c_gamma(M_geom/r^3)p_3^2,
M_geom=GM/c^2.
```

For weak coupling and tangential propagation, the magnitude of the split
between the two polarization velocities is

```text
|Delta v_pol|/c
 =12|c_gamma|M_geom/r^3
  +O[(c_gamma M_geom/r^3)^2].
```

The exact two optical angular factors in the Horndeski/Ricci-flat branch are

```text
rho_l=(r^3-8c_gamma M_geom)/(r^3+16c_gamma M_geom),

rho_m=(r^3+16c_gamma M_geom)/(r^3-8c_gamma M_geom)
     =1/rho_l.
```

Requiring both optical metrics to remain nonsingular at and outside the
Schwarzschild horizon gives

```text
-1/2<=c_gamma/M_geom^2<=1.
```

This is a theory-validity interval, not observational evidence.

For the known free-lepton threshold, the leading polarization splits are

| control arena | `|Delta v_pol|/c` |
|---|---:|
| solar limb | `5.063391844905093e-53` |
| `1.4 M_sun`, `12 km` neutron-star benchmark | `1.3813121930235602e-38` |
| `10 M_sun` horizon benchmark | `6.619220923807397e-39` |
| M87* horizon case | `1.5195640320953621e-56` |

These are QED baseline controls, not fitted data rows.

## 8. Source-backed bounds

### 8.1 Legacy source

The original nonminimal-electrodynamics paper uses exactly

```text
L=-F^2/4+lambda Riemann F F.
```

Its detailed pulsar calculation allows a one-microsecond polarization
correction to the PSR B1534+12 Shapiro delay and prints

```text
lambda<0.6e11 cm^2=6.0e6 m^2,
sqrt(lambda)<2.449 km.
```

This is the strongest original numeric scale acquired here, but it is
one-sided and model conditional. In particular, the printed inequality does
not constrain a large negative coefficient.

The same paper contains an internal radar discrepancy:

```text
introduction: lambda<3.9e19 cm^2,
detailed section: lambda<1.1e20 cm^2.
```

Both rows are retained and marked inconsistent. Neither is selected.

### 8.2 Secondary absolute recast

The 2025 black-hole-imaging source summarizes the older pulsar scale as

```text
sqrt(|alpha|)<2.45 km,
```

but explicitly warns that these astrophysical constraints depend on the
absence or control of other Ricci and Euler-Heisenberg operators, magnetic
fields and environmental assumptions. This is a useful two-sided secondary
recast, not a reconstructed modern likelihood.

### 8.3 M87* case study

Under the paper's stated assumptions that the reconstructed thin M87* ring is
the `n=1` photon ring, that the unpolarized PPL/PPM bands overlap, and that the
external mass and distance estimates apply, the source obtains

```text
-0.3 lesssim alpha/M_M87^2 lesssim 0.3,

sqrt(|alpha|)<5.34e9 km,

|c_gamma|<2.85156e25 m^2.
```

This is a modern two-sided source-backed case-study bound, but it is far
weaker than the legacy compact-star scale and is not a general CFF likelihood.

## 9. Wilson residual projection

For a two-sided total-coefficient bound `|c_gamma^IR|<=B`, the safe outer
envelope on the uncalculated residual is

```text
|c_gamma^parent+c_gamma^QCD+c_gamma^EW+...|
 <=B+|c_gamma^free-leptons|.
```

For the original one-sided pulsar result,

```text
c_gamma^parent+c_gamma^QCD+c_gamma^EW+...
 <B_PSR-c_gamma^free-leptons.
```

The calculated scale ratios are

```text
|c_free-leptons|/B_PSR(original) =1.603632403928247e-37,
B_PSR/|c_free-leptons|           =6.235843061978586e36,

|c_free-leptons|/B_M87          =3.3742212766238415e-56,
B_M87/|c_free-leptons|           =2.9636467736359425e55.
```

Thus known free-lepton matching is harmless by an enormous margin. The
dominant open question is whether the parent MTS coefficient or an uncalculated
threshold is anomalously large. The acquired rows do not justify setting that
residual to zero.

## 10. What is now derived

Closed here:

```text
one-loop additive zero for minimal massless Einstein-Maxwell/Yang-Mills;
general beta/fixed-manifold boundary and strict-canonical theta=-2 comparator;
finite charged-Dirac threshold formula and three-lepton numerical subtotal;
independent matching-magnitude reproduction;
electroweak c_B/c_W to photon/Z/AZ projection;
complete retained Maxwell excitation and source equations;
current conservation and full-stress Ward identity;
geometric-optics polarization characteristic;
frequency-independent local birefringence at dimension six;
Schwarzschild weak split and exact optical metric factors;
legacy pulsar, radar and modern M87* source rows;
one-sided versus two-sided Wilson residual formulas;
QED baseline magnitude in four curvature controls.
```

Still open:

```text
full nonperturbative MTS b_X and gamma_X;
u_B*, u_W*, u_G* and their stability-matrix entries;
separation of c_B and c_W from photon data;
charged-W and confined-QCD threshold matching;
a modern robust two-sided polarization likelihood;
joint treatment of CFF, Ricci-F2 and Euler-Heisenberg operators;
full profile-dependent Hilbert-stress/Poynting correction;
parent prediction or empirical determination of c_gamma^parent;
compact and full MTS-to-GR promotion.
```

## 11. Final gate

```text
massless one-loop additive portal source      -> zero derived;
canonical Gaussian portal coordinate          -> u*=0, theta=-2 comparator;
full MTS portal fixed point                    -> not calculated;
charged-Dirac threshold                        -> finite and calculated;
electron c_gamma                               -> -9.6215686e-31 m^2;
free-lepton subtotal                           -> -9.6217944e-31 m^2;
photon birefringence characteristic            -> derived;
leading local energy dispersion                -> absent;
Maxwell current/stress conservation            -> derived;
legacy PSR positive-side scale                 -> 6.0e6 m^2, conditional;
modern M87 absolute case scale                 -> 2.85156e25 m^2, conditional;
known QED baseline                             -> overwhelmingly safe;
general parent c_gamma                         -> not predicted;
weak uncharged GR/Newton                       -> retained;
compact and full MTS-to-GR                     -> not promoted.
```

Direct next target:

`4932-Y5-R2FR-MTS-gauge-portal-functional-trace-projection-or-two-sided-polarization-likelihood.md`

First attempt the actual MTS `u_B,u_W,u_G` projection in the already selected
functional-flow scheme. If that projection cannot be closed, construct a
joint two-polarization likelihood that fits the total `c_gamma` together with
the competing Ricci and nonlinear electromagnetic operators rather than
reusing a one-sided legacy inequality as a theory prediction.

No GitHub action is authorized.
