# Spherical curvature, parent stress, and a residual-controlled delta K route

2026-09-09. Private derivation. Scope: the existing spherical ordinary-reference
sector and first variation of its curvature-dependent mass improvement.
This is a consequence of the chosen reference action and spherical geometry,
not a new proof that the complete MTS programme reduces to GR.

## 1. Why this moves the physics calculation forward

The curvature source previously required feeding corrected metric derivatives
back into a higher-derivative expression. We now have an exact decomposition:
an algebraic mass/stress term plus explicitly retained equation residuals.
The residual term is further derived from the existing mass, lapse and scalar
equations; no independent unexplained angular/trace input has to be invented.

That provides a concrete route from the computed reference corrections to the
Weyl-squared source and the mass-restoration coefficient K1. It does not permit
us to set the residuals to zero, and it does not derive the physical coupling u.

Parent source, unchanged:
scripts/annular_evolution_operator_20260909.py, equations().
The geometry, scalar Lagrangian and normalization below match that source.

## 2. Exact curvature-stress identity

Use the advanced spherical metric with
F=1-2mu/r-Lambda*r^2/3, E=exp(delta), kappa=4pi G.
The ordinary scalar sector is

X=2p s+F s^2,  p=exp(-delta) chi_v,  s=chi_r,
L=-X/2+b2 X^2+b3 X^3-V(chi),
P=1-4b2 X-6b3 X^2,
T_ab=P chi_a chi_b+g_ab L.

Let Z be the signed curvature amplitude used by the parent:
Weyl_abcd Weyl^abcd=Z^2/3.
If R2 is the scalar curvature of the two-dimensional orbit metric and
B_r=F_r+F delta_r, then

Z=R2+2 B_r/r+2(1-F)/r^2,
R4=R2-4 B_r/r+2(1-F)/r^2.

Define the Einstein residual, with no assumption it vanishes,

E_ab=G_ab+Lambda*g_ab-2kappa*T_ab,
E_Omega=E_theta_theta/r^2,
E_trace=g^ab E_ab.

The exact identity is

Z=Z_alg-6 E_Omega+2 E_trace,
Z_alg=12mu/r^3+4kappa(PX+L)
     =12mu/r^3+4kappa[X/2-3b2 X^2-5b3 X^3-V].

It follows by substituting
E_Omega=B_r/r-R2/2+Lambda-2kappa L
and E_trace=-R4+4Lambda-2kappa(PX+4L).
The Lambda terms cancel explicitly, rather than being dropped.

Checks:
- vacuum: Z_alg=12mu/r^3 and Weyl^2=48mu^2/r^6;
- homogeneous isotropic, on-shell stress: mu/r^3=-kappa(PX+L)/3 gives Z=0.

These are consistency limits of the identity, not new observational tests.

## 3. Derive the angular/trace error from the parent residuals

Use physical (v,r) derivatives here, and distinguish radius r from the residual:

R_m=mu_r-R0,
D_l=delta_r-D0,
F_chi=exp(-delta)/r^2 [
  partial_v(r^2 P chi_r)
  +partial_r(r^2 P chi_v+exp(delta) r^2 P F chi_r)]
  -V_chi.

F_chi is the scalar equation residual, NOT the scalar-density residual.
The ordinary sources are the existing parent expressions

R0=kappa*r^2[PFs^2/2+V+b2 X^2+2b3 X^3],
D0=kappa*r*P*s^2.

Direct symbolic differentiation of these sources gives

E_Omega=exp(-delta) partial_v D_l
        -(partial_r R_m)/r+F partial_r D_l
        +(3F_r/2+F delta_r+F/r)D_l
        +kappa*r*s*F_chi.

The orbit-space trace is
E_orbit=-4R_m/r^2+2F D_l/r.
Since E_trace=E_orbit+2E_Omega, the curvature error is exactly

Delta_Z=Z-Z_alg
 =-8R_m/r^2+2(partial_r R_m)/r
  -2exp(-delta) partial_v D_l-2F partial_r D_l
  +(2F/r-3F_r-2F delta_r)D_l
  -2kappa*r*s*F_chi.

The checker verifies both identities for symbolic b2,b3 and V=m_chi^2 chi^2/2,
using independent local field derivatives, rather than imposing the scalar or
Einstein equations. The scalar residual term is essential off shell.

A direct sup-norm bound on an annulus is therefore

||Delta_Z|| <= 8/r_min^2 ||R_m||+2/r_min ||partial_r R_m||
 +2||exp(-delta)|| ||partial_v D_l||
 +2||F|| ||partial_r D_l||
 +||2F/r-3F_r-2F delta_r|| ||D_l||
 +2|kappa| r_max ||s|| ||F_chi||.

All norms must cover the domain of the claim. Small sampled residual amplitudes
alone do not establish this bound: their derivatives must also be controlled.

Coordinate warning for implementation:
t=v-sigma(r-4), R=r, so partial_v=partial_t and
partial_r at fixed v = partial_R-sigma*partial_t.
In saved variables,

R_m=mu_R-sigma*mu_t-R0,
D_l=delta_R-sigma*delta_t-D0.

The existing saved spatial mass constraint J=R_m+sigma*C_m, where
C_m=mu_t-C0. J must not be mistaken for R_m when evaluating this identity.
Numerical sources and approximate-background residuals remain included.

## 4. First variation into the curvature source

For the ordinary correction e=(e_chi,e_q,e_mu,e_delta),

delta p=exp(-delta)e_q-p e_delta,
delta s=partial_R e_chi-sigma e_q,
delta F=-2e_mu/r,
delta X=2s delta p+2(p+Fs)delta s+s^2 delta F.

For V=m_chi^2 chi^2/2,

delta Z_alg=12e_mu/r^3
 +4kappa[(1/2-6b2 X-15b3 X^2)delta X-m_chi^2 chi e_chi],
delta(Weyl^2)_alg=2 Z_alg delta Z_alg/3.

The actual change must also retain delta(Delta_Z). In particular,

delta(Weyl^2)-delta(Weyl^2)_alg
 =2[Z_alg delta(Delta_Z)+Delta_Z delta Z_alg
      +Delta_Z delta(Delta_Z)]/3.

Similarly,
Weyl^2-Weyl_alg^2=(2Z_alg Delta_Z+Delta_Z^2)/3.
These formulas quantify the price of an on-shell reduction; they do not hide it.

Implementation:
scripts/annular_curvature_stress_bridge_20260909.py

The saved, unmasked N512 evolution is explicitly still FAILED 136/137.
Applying the algebraic variation map to its ordinary-reference corrections gives:

| Fixture/time | Maximum absolute delta Z_alg | Maximum absolute delta Weyl_alg^2 |
| --- | ---: | ---: |
| canonical, 0.1 | 3.21466e-12 | 3.53726e-13 |
| canonical, 0.3 | 5.14560e-12 | 6.32121e-13 |
| nonlinear, 0.1 | 3.42267e-11 | 3.87569e-12 |
| nonlinear, 0.3 | 1.63455e-11 | 1.97582e-12 |

These are dimensionless conditional proxy variations, not established physical
curvature shifts. The corrected residual derivative bounds have not yet been
evaluated. Every projection row remains valid_for_physics_claim=false.
The data source is recorded separately from the newer boundary-fixed evolution;
do not silently relabel it as a measurement from that newer run.

## 5. Exact variation of the mass-restoration coefficient

At first order in the parent's curvature coupling u, write the multiplier as

M1=-2r^2 X Z/3,
B0=2F/r-F_r-2F delta_r,
K1=kappa[2F partial_r M1+2exp(-delta) partial_v M1+B0 M1].

K1 here is the mass-improvement/restoration coefficient from the parent's
boundary term, not the unrelated general memory-stress tensor K_hat.
The parent's improved mass is mu-u*K1+O(u^2).

Its variation is

delta M1=-2r^2[X delta Z+Z delta X]/3,
delta B0=2delta F/r-partial_r(delta F)
         -2delta F delta_r-2F partial_r(e_delta),

delta K1=kappa[
 2delta F partial_r M1+2F partial_r(delta M1)
 +2exp(-delta) partial_v(delta M1)
 -2exp(-delta)e_delta partial_v M1
 +delta B0 M1+B0 delta M1].

This chain rule is verified symbolically. Substitution of Z_alg alone is only
conditional: the omitted multiplier is
Delta M1=-2r^2 X Delta_Z/3, and the omitted K1 is the same displayed differential
operator applied to Delta M1. Bounding it requires derivatives of Delta_Z,
not just its amplitude. First variation requires the corresponding varied
residual terms too.

## 6. Evidence and next actual calculation

Checker:
scripts/derive_annular_curvature_stress_bridge_20260909.py

Owners:
source-intake/navier-stokes/20260909/annular-curvature-stress-bridge-initial/status.json
(25/25, 03:57:12 UTC; first version, execution snapshot retained).
source-intake/navier-stokes/20260909/annular-curvature-residual-bridge-derived/status.json
(27/27, 04:00:41 UTC; adds the explicit angular and curvature-residual identities).

Latest checker SHA256:
6f37327cd3fcd8460774e540344ce5740329701333828ffbff0aebaeb74a90c1.

The next calculation is now specific: reconstruct the corrected reference
R_m, D_l and F_chi together with their physical derivative jets; evaluate the
derived Delta_Z bound and propagate it through delta M1 and delta K1.
Do not reset the angular/trace residual to zero or differentiate in the wrong
time slicing. A second-order Newton remainder must be retained when turning
the linear correction into a nonlinear residual estimate.

The numerical companion still has a finite-grid boundary-accuracy failure and
no full coupled energy theorem. Keep those gates visible, but do not substitute
another large mesh sweep for this derived physics transfer. There is no full
GR/Newton/Maxwell limit or calibrated source-coupling claim from this checkpoint.
