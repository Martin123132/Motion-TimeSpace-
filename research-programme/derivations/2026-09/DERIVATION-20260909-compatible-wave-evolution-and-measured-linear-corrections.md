# Compatible exterior wave evolution and measured linear corrections

2026-09-09. Private continuation; no public or observational claim.

## Result in plain language

We have moved from checking the residual of an explicit approximate field to
actually evolving a source-driven correction. The scalar and Einstein mass/lapse
equations admit a regular constrained evolution on the retained exterior
annulus. Its implementation avoids a redundant scalar-gradient variable and
solves the initial/boundary compatibility equations rather than simply imposing
inconsistent zero error data.

The final short run passes 50/50 implementation gates. In both fixtures, for
both the ordinary reference and first-order coupling response, the final
discrete mass-constraint error is smaller than before correction. This is
progress in a specific linear exterior problem, not a completed nonlinear MTS
solution, a black-hole regularity proof, or an empirical comparison with GR.

The initial data are deliberately changed by a small, explicitly saved repair.
Coarse-grid differences are still appreciable. Do not interpret tiny final
correction amplitudes as certified error bounds on the physical theory.

## 1. Scope, sources and conventions

All local paths below are relative to this document's post-checkpoint-work
directory. The source equations, coefficients and two field fixtures come from:

- `DERIVATION-20260909-adapted-wave-energy-and-coupled-stability-entry.md`
- `DERIVATION-20260909-coupled-lapse-current-and-fixed-reference-error-control.md`
- `RESULT-20260909-oscillatory-mass-correction-and-angular-equation.md`
- `source-intake/navier-stokes/20260909/annular-constraint-correction-initial/status.json`
- `scripts/annular_source_derivative_residuals_20260909.py`

Use the same spherical metric, coupling normalization and matter block:

```text
ds^2=-E^2 F dv^2+2E dv dr+r^2 dOmega^2,
E=exp(delta), F=1-2mu/r-Lambda r^2/3, kappa=4pi G,
p=E^-1 chi_v, s=chi_r, X=2ps+Fs^2,
P=1-4b2 X-6b3 X^2, Px=-4b2-12b3 X,
rho=E r^2, t=v-sigma(r-4), R=r, sigma=1/20.
```

The u=0 reference is Einstein gravity with the selected scalar matter, not
vacuum GR. The u coefficient retains the previously sourced curvature/kinetic
operator and physical mass restoration K. Neither its numerical physical
coupling nor a new fundamental matter action is derived here.

The exact evolution/constraint statement below first concerns the u=0
two-derivative sector. The numerical response is a fixed-reference linear
defect problem, as distinguished in section 4.

## 2. A regular evolution reduction

Define the scalar principal densities and local source functions:

```text
a=2r^2 Px s^2/E,
b=r^2[P+2Px s(p+Fs)],
c=E r^2[PF+2Px(p+Fs)^2], A_t=a-2sigma b+sigma^2 c,
D0=kappa r P s^2,
C0=kappa r^2 E P p(p+Fs),
R0=kappa r^2[PFs^2/2+m_chi^2 chi^2/2+b2 X^2+2b3 X^3],
j_mu_v=-2r Px s^3,
j_mu_r=-2r E[Px s^2(p+Fs)+P s], j_r=rho P(p+Fs),
F_r_explicit=2mu/r^2-2Lambda r/3,
j_explicit=E[2rP(p+Fs)
  +r^2 F_r_explicit(Px s^2(p+Fs)+P s)].
```

In j_explicit the derivative is at fixed chi,p,s,mu,delta. Substitution of
the temporal mass and radial mass/lapse sources into the scalar current gives

```text
H=rho m_chi^2 chi-j_mu_v C0-j_mu_r R0
  -[(b-sigma c)Ep+j_r]D0-j_explicit,
p_t=[H-E(2b-sigma c)p_R-c s_R]/(E A_t),
s_t=E p_R-sigma E p_t+Ep D0,
mu_t=C0, delta_t=(delta_R-D0)/sigma, chi_t=Ep.       (1)
```

There is no division by a or Px, so the canonical case Px=0 is included.
The needed nondegeneracy is A_t<0 and b^2-ac>0 on the chosen spacelike
domain, together with positive E and the existing energy assumptions.
The wave p/s rows have no mu_R or delta_R coupling. Their principal block is

```text
B=[[-(2b-sigma c)/A_t, -c/(E A_t)],
   [ E(1+sigma(2b-sigma c)/A_t), sigma c/A_t]],
tr B=-2(b-sigma c)/A_t, det B=c/A_t,
(tr B)^2/4-det B=(b^2-ac)/A_t^2.                   (2)
```

The lapse is an advection variable with RHS speed 1/sigma. This removes
the suspected wave/metric derivative coupling in this variable choice;
it is not a general strong-hyperbolicity theorem for the full higher-order
finite-u field theory.

## 3. Why the radial Einstein equation is not discarded

Let C=mu_v-C0, R_err=mu_r-R0, D=delta_r-D0 and let F_chi be the scalar
density residual. Write A_ang for the angular Einstein residual. For the
reference sector the off-shell Einstein/Noether identities are

```text
C_r-(R_err)_v+delta_r C-mu_v D+kappa p F_chi=0,     (3)
A_ang=E^-1 D_v+F D_r
 +(F/r+3F_r/2+F delta_r)D-(R_err)_r/r
 +kappa r chi_r F_chi/rho.                         (4)
```

The checker explicitly constructs the metric connection and both divergence
projections. Its residual tensor uses
E_rr=2D/r, E_vr=-2E R_err/r^2, and
E_vv=2E C/r^2+2E^2 F R_err/r^2.

Crucially, off the radial constraint, evolution (1) gives
F_chi=j_mu_r R_err, not automatically F_chi=0. Equations (1) and (3) imply

```text
(R_err)_t=kappa p j_mu_r R_err.                    (5)
```

Thus zero radial constraint propagates for a smooth solution satisfying
compatible initial and boundary data; then the scalar and angular equations
also hold. It would be incorrect to assert (R_err)_t=0 for arbitrary errors.
The kinematic constraint chi_R-s-sigma Ep has exactly zero time derivative.
This is a conditional equivalence statement, not an existence proof.

Linearization of these identities about an exact reference preserves their
compatibility structure. About an approximate reference there are additional
terms involving its residuals; our two separately evolved correction channels
do not silently remove those terms or update that reference.

## 4. Actual parent residuals drive the correction

For an arbitrary explicit field, the reduction gives the defect map

```text
d_p=[F_chi-j_mu_v C-j_mu_r R_err
     -((b-sigma c)Ep+j_r)D]/(E A_t),
d_s=-sigma E d_p+EpD,
d_mu=C, d_delta=-D/sigma, d_chi=0.                 (6)
```

The parent residuals in the evaluator are copied from the retained, unexpanded
equations, including the order-u source and exact K restoration. Products in
(6) use exact first-order-u dual arithmetic, including normalization times
background-residual terms. The ordinary defect is independently compared
against U_app,t-F0[U_app]. No forcing is manufactured by declaring the desired
answer to be an exact solution.

For evolution we eliminate the redundant gradient and use
U=(chi,q=chi_v,mu,delta), with s=chi_R-sigma q and p=q/E. Then

```text
p_R=(q_R-delta_R q)/E, s_R=chi_RR-sigma q_R,
q_t=E p_t+q delta_t, d_q=E d_p+q d_delta.
e_t=DF0[U_app,0]e-d_app,j,  j=0 or 1.             (7)
```

j=0 is one linear Newton correction, not a completed nonlinear solve.
j=1 is a coupling-response correction on the same prescribed approximate
reference. The j=0 correction is NOT yet fed back into the curvature source,
K or the j=1 coefficients. The two solutions must not simply be added and
called a verified finite-u solution.

## 5. Boundary compatibility: a repaired implementation, not a fitted theory

The scalar error conditions are eta_R=(sigma+k)eta_t, with k_plus at r=4
and k_minus at r=8, roots of a+2bk+ck^2=0. The outer lapse error is zero;
the outer mass error evolves by the Einstein mass-flux ODE, rather than
being clamped to a constant during evolution.

Initially, zero eta and eta_t generally contradict the time derivative of
that boundary condition because the bulk equation has nonzero forcing.
An independent check also found outer lapse corner mismatches up to
approximately 2e-12 after repairing only the scalar corners.

The final implementation solves all three first time-compatibility equations
simultaneously. Choose fixed-width-one profiles, zero beyond distance one:

```text
H(d)=d^2(1-d)^4/2, J(d)=-d(1-d)^4, 0<=d<=1.
eta_initial=A_left H(r-4)+A_right H(8-r),
zeta_initial=A_lapse J(8-r).                        (8)
```

H has zero value and first derivative at its boundary, and second derivative
one. J has zero outer value and radial derivative one. The profiles and width
are an explicit numerical initial-data choice, not a parent-derived physical
law. They are C3 at the support join, not infinitely smooth profiles.

The incoming q error is projected from eta_R. Every profile's mass component
is obtained by solving the linearized initial radial constraint; its outer
initial mass correction is anchored at zero. Evaluate the three corner
mismatches (two scalar accelerations and outer lapse time derivative) for
these templates and solve a 3x3 linear system per response channel. Amplitudes
are determined by that system, not adjusted to reduce a final constraint.

The linear initial mass equation is checked on all rows except the outer row
replaced by its mass anchor. The outer constraint is included in the final
maximum-error diagnostic, not silently excluded. Only first time compatibility
is imposed. Higher corner derivatives and continuum-compatible data still
need separate control. The finite-grid amplitudes vary with resolution; this
is one reason current refinement factors are not a certified convergence order.

## 6. What was run, including the unsuccessful controls

All run folders below are under `source-intake/navier-stokes/20260909/`:

| Run | Gates | Interpretation |
| --- | --- | --- |
| annular-evolution-reduction-initial | 17/17 | Seven exact reduction/divergence identities and ten operator checks |
| annular-linear-evolution-initial | 20/20 | Five-variable prototype; redundant gradient boundary error remains |
| annular-compatible-linear-evolution-initial | 34/34 | Coordinate scalar fixes that redundancy, but boundary constraint accuracy is insufficient |
| sbp4-operator-derived | 8/8 | SBP D4-2 stencil derived by exact linear equations, positive norm and SBP identity |
| annular-sbp4-linear-evolution-initial | 37/38, FAILED | Canonical u1 full mass constraint worsens: 2.20e-11 versus 1.53e-11 |
| annular-corner-compatible-evolution-initial | 50/50 | Scalar corners repaired; outer lapse corner was not yet tested |
| annular-full-corner-evolution-final | 50/50 | Simultaneous scalar/lapse first-corner repair; current accepted smoke run |

Earlier passes mean their stated gates passed, not that omitted gates were
satisfied. The failed run and every prototype remain intact. The failed run
has no COMPLETE marker. The earlier two-corner script is preserved verbatim
as its executed-script.py; the live script now contains the full three-corner
repair and has a different, recorded hash.

The derived SBP norm has left weights (17,59,43,49)/48, mirrored on the right.
Its fourth-order interior and second-order boundary stencil is verified from
polynomial exactness and HD+D^T H=boundary, not borrowed without checking.
This operator identity alone does not prove stability of our complete
projected boundary treatment.

The two fixed, dimensionless fixtures retain kappa=0.1 and initial mean mass
one on r in [4,8]. Canonical: amplitude 0.1, Lambda=m_chi=b2=b3=0.
Nonlinear/modulated: amplitude 0.1(1+v/10), Lambda=0.001, m_chi=0.2,
b2=0.05, b3=0.02. Both use epsilon=0.1, t in [0,0.1], grids of 16/32/64
intervals, RK4 and a separate fine-grid half-time-step run. Coefficient/forcing
time interpolation uses 65 points and is checked at an off-grid time.

Final N64, refined time-step results (dimensionless, u1 is per unit u):

| Fixture/channel | max abs eta | max abs eta_t | max abs nu | Mass constraint before | Mass constraint after |
| --- | ---: | ---: | ---: | ---: | ---: |
| Canonical/reference | 2.47e-10 | 3.57e-9 | 1.15e-11 | 3.33e-11 | 1.94e-12 |
| Canonical/u1 | 4.51e-10 | 4.77e-9 | 5.57e-12 | 1.53e-11 | 2.46e-12 |
| Nonlinear/reference | 6.83e-10 | 9.84e-9 | 1.21e-10 | 3.11e-11 | 5.36e-12 |
| Nonlinear/u1 | 1.24e-10 | 1.56e-9 | 1.37e-11 | 1.79e-11 | 1.39e-12 |

These are maxima at the final time, not suprema over the whole evolution.
Full-domain discrete constraint improvements are about 17.2, 6.22, 5.80 and
12.9, respectively. Initial scalar repairs on the same fine grid have maxima
6.47e-11, 4.09e-10, 4.36e-10 and 3.29e-11, respectively. Thus particularly
the canonical u1 correction includes a substantial initial-data contribution.
Saved NPZ files include those initial corrections and their three amplitudes.

Successive grid differences decrease by factors 2.31 to 2.46. The maximum
32-to-64 state differences range from 2.94e-10 to 3.81e-9; they are NOT
negligible relative to all final amplitudes. Time-refinement differences are
between 9.34e-15 and 1.24e-13. Spatial/initial-data resolution, not RK4 time
resolution, is the present numerical limitation. No continuum error estimate
or higher-order convergence claim follows from these three grids.

## 7. Reproducibility and next substantive step

The current operator files are `scripts/annular_evolution_operator_20260909.py`
and `scripts/annular_coordinate_evolution_operator_20260909.py`; the current
runner is `scripts/annular_corner_compatible_evolution_20260909.py`.
Its final-run source SHA-256 is
`0630cb0175ea5715b6a009ddc2d5e830118950732b3e353bcf44dfed06929a2c`.
The final run completed at 2026-09-09T02:07:55.421611+00:00, after about
17 seconds on one core BelowNormal. Every status records source owners,
executed source and artifact hashes. Claim flags remain false.

Evidence verification is implemented separately in
`scripts/annular_evolution_evidence_20260909.py`; it does not count file
integrity checks as additional physics proofs.
Its authoritative output is
`source-intake/navier-stokes/20260909/annular-evolution-evidence-verified/status.json`.
The first checker attempt, annular-evolution-evidence-final, aborted because
its AST lookup missed a nested function. It is preserved as failed without
COMPLETE; the corrected checker searches the nested syntax tree. This was
an evidence-checker bug, not a failed evolution or a changed parent equation.

Next, derive a continuum-compatible initial repair and sample the same data
on finer grids, rather than changing the data independently at each grid.
Then test N128/N256 and a longer interval, retaining the matched reference
and u1 controls and full boundary constraints. This will distinguish genuine
spatial error from resolution dependence of the compatibility repair.

After that, feed the reference correction back into the curvature source and
the physical restoration difference kappa delta K, controlling the derivative
norms identified in the preceding note. Finite-u nonlinear stability and any
horizon/centre extension remain separate requirements. Nothing here imports
an alleged Navier-Stokes breakthrough as an unverified theorem about MTS.

All work remains local. No extra agents, public updates, frozen-workbench
edits, galaxy changes or interference with RH/Desktop Commander were needed.
