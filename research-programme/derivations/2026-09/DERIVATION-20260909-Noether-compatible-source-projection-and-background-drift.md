# Noether-compatible numerical sources and retained background drift

Date: 2026-09-09. Private continuation; no publication action.
Scope: the existing fixed-reference, finite-annulus correction problem.
This is a derived numerical compatibility mechanism, **not** a newly derived
physical MTS coupling, a black-hole solution, or an accepted continuum evolution.

## Outcome in plain language

We implemented the conservation-based correction instead of merely listing it
as missing. An outer-boundary compatibility condition was exposed, derived,
and enforced. The final version preserves the lapse numerical source and
outer physical mass-flux equation, while cancelling the added mass-constraint
drift at **all** grid points. It does not cancel the original/background error.

The refined evolution remains **FAILED 134/137**. All eight full mass-constraint
and boundary-accuracy comparisons pass. Two short-time spatial refinement gates
remain open. A separate derivative-control study explains the third failure as
an insufficient finite-difference diagnostic: higher-order controls satisfy the
original tolerance without changing the evolution. The original failed state
is retained, not retrospectively promoted.

Independent evidence: **59/59**. Derivative/localization controls: **18/18**.
These are checks of the stated construction and artifacts, not a percentage of
the full theory proved.

## 1. Owners, conventions, and unchanged physics

All paths below are relative to this post-checkpoint-work directory.
Parent field/constraint owner:
- source-intake/navier-stokes/20260909/annular-constraint-correction-initial/status.json
- source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json
- source-intake/navier-stokes/20260909/annular-constraint-correction-initial/nonlinear_modulated.json

Initial-data owner:
- source-intake/navier-stokes/20260909/annular-continuum-data-initial/status.json

Previous derivation:
- DERIVATION-20260909-grid-independent-data-and-boundary-energy-control.md

The two dimensionless fixtures, epsilon=0.1, sigma=0.05, R in [4,8], and the
degree64 continuum initial-data lift are unchanged. The final comparison uses
N=128/256/512 intervals and outputs T=0.1,0.3. No physical parameter was fitted.
The ordinary and first-u correction channels still use the frozen ordinary
reference Jacobian; this is not a solved finite-u or fully nonlinear problem.

Write U=(chi,q,mu,delta), q=chi_t, w=chi_R, E=exp(delta),
p=q/E, s=w-sigma*q, F=1-2mu/R-Lambda*R^2/3, X=2ps+Fs^2.
The existing parent defines P=1-4b2 X-6b3 X^2 and P_X=-4b2-12b3 X.

Its scalar density coefficients are
a=2R^2 P_X s^2/E,
b=R^2[P+2P_X s(p+Fs)],
c=ER^2[PF+2P_X(p+Fs)^2],
A_t=a-2sigma*b+sigma^2*c.
The tested domain has A_t<0; this domain assumption is essential.

Let D0=kappa R P s^2,
C0=kappa R^2 E P p(p+Fs),
R0=kappa R^2[PFs^2/2+m_chi^2 chi^2/2+b2 X^2+2b3 X^3].
The spatial mass constraint is H(U)=mu_R-G, G=R0+sigma*C0.

## 2. Exact local constraint derivatives

Differentiating the parent G, rather than choosing a convenient projection,
gives the following five coefficients:

G_chi = kappa R^2 m_chi^2 chi,
G_q = -kappa p A_t,
G_mu = -beta,
G_delta = kappa p q(a-sigma*b),
G_w = kappa R^2[PFs-2P_X p s(p+Fs)]
      +sigma*kappa*R^2 E p[PF+2P_X(p+Fs)^2],

where beta=D0+kappa*p(j_mu_v-sigma*j_mu_R),
j_mu_v=-2R P_X s^3,
j_mu_R=-2RE[P_X s^2(p+Fs)+Ps].

The identity script verifies all five symbolically and independently compares
the closed coefficients against complex-step differentiation of the original G.
Owner: source-intake/navier-stokes/20260909/annular-noether-completion-identities-initial/status.json
Result: 16/16, completed 03:00:15 UTC.

For an added numerical source S with S_chi=0, its linearized constraint drift is

M_h S = (D_h-G_mu)S_mu-G_q S_q-G_delta S_delta.

D_h is the already derived SBP D4-2 derivative. These are exact finite-matrix
identities at a fixed reference state, applied separately to both correction
channels. They do not replace or prove the nonlinear field equations.

## 3. Continuum completion and the missing discrete boundary condition

The previously derived Noether source identity requires a mass source C obeying

C_R+beta*C = G_q*S_q+G_delta*S_delta = -f_S,   C(8)=0.

Thus
C(R)=integral_R^8 exp(integral_R^s beta(x) dx) f_S(s) ds.

For bounded beta on this annulus,
||C||_infinity <= 4 exp(4||beta||_infinity)||f_S||_infinity.
This is a continuum source bound, not a mesh-uniform inverse bound.

The first discrete implementation replaced the last mass-equation row by C(8)=0.
It solved the interior completion, but that alone does not imply the omitted
outer constraint row. We saved this attempt as FAILED 118/121. Its exposed outer
drift was not excluded from later tests.

Let M=D_h-G_mu and impose C_B=0. The rectangular matrix acting on the remaining
mass values has one left compatibility condition when its rank is full.
For the tested matrices its null covector ell satisfies

ell^T M C=0 for every C with C_B=0.

It is computed by one transposed band solve, not by a dense solve per time step.
If A is M with last row replaced by e_B^T, solve A^T y=M_B^T and take
ell=(y_0,...,y_(B-1),-1). Indeed ell^T M=-y_B e_B^T.
Invertibility of A is required; it is not asserted for arbitrary parent data.

The necessary and sufficient source condition on this finite grid is therefore

ell^T(G_q*S_q+G_delta*S_delta)=0.

The first all-row implementation projected both scalar and lapse numerical
sources onto this hyperplane. It enforced the constraint but degraded six
boundary-accuracy checks, including lapse errors. That attempt is preserved as
FAILED 131/137, not selected as the final method.

## 4. Scalar-only projection: derivation and regularity

Keep the original lapse SAT/filter source S_delta fixed.
Set alpha_vec=ell*G_q componentwise, W=h H_SBP (-A_t)>0, and

d=alpha_vec^T W^-1 alpha_vec,
r=ell^T(G_q*S_q+G_delta*S_delta),
S_q_star=S_q-W^-1 alpha_vec*r/d.

Here H_SBP denotes the diagonal SBP norm weights, not the mass constraint H(U).
This is the unique minimum of
||S_q_star-S_q||_W^2 subject to the compatibility condition, if d>0.
Use S_q_star and unchanged S_delta in the anchored band solve for C.
The full source is (0,S_q_star,C,S_delta); C_B is identically zero.

There is no division by the velocity at an individual grid point. In fact,

L=G_delta/G_q=-q(a-sigma*b)/A_t

has a continuous extension through p=0 in the hyperbolic domain. Consequently
r=alpha_vec^T(S_q+L*S_delta). If d=0, alpha_vec=0 and r=0;
leave S_q unchanged. The script raises an error for an inconsistent degenerate
input rather than silently filling it. Zero-velocity fixture controls pass.

Writing P_W for the W-orthogonal projection onto ker(alpha_vec^T),

S_q_star=P_W S_q-W^-1 alpha_vec*(alpha_vec^T L S_delta)/d.

The two terms are W-orthogonal, giving the useful affine bound

||S_q_star||_W^2 <= ||S_q||_W^2+||L*S_delta||_W^2.

This bounds the projected scalar source. It does **not** establish a
mesh-independent bound for C, convergence of the boundary scheme, or a total
energy estimate. Nor does absence of pointwise velocity division prove smooth
dependence of the whole projector through every rank-changing background.

The raw mass filter is REPLACED by C, not added to it. These sources are
numerical SAT/filter terms, not new parent coefficients. Zero numerical forcing
produces zero completion. Consistency in a continuum limit still requires
control of the numerical forcing and inverse as the mesh changes.

## 5. Background drift is retained, not artificially cleaned

The saved linearized full constraint is

J=H(U_app)+D_h e_mu-G_U e-G_w D_R e_chi,

where the fixed initial lift is differentiated analytically and the evolved
remainder is differentiated with D_h. Its time derivative includes both
the prescribed constraint derivative and the time-varying coefficients:

J_t=H(U_app)_t-(G_U)_t e-(G_w)_t D_R e_chi+M_h e_t.

H(U_app)_t is obtained from the original field equations using fifth-order jets,
not assumed zero. The evolution saves separately:
- parent_constraint_drift: drift before the added numerical sources;
- numerical_constraint_drift: M_h S;
- reference_background_bias and reference_product_defect;
- actual_constraint_time.

For the ordinary reference system, the parent identity is DH(U)F0(U)=k(U)H(U),
where k=kappa*p*j_mu_R. Let U_app,t=F0(U_app)+d0 and let the Newton correction
satisfy e_t=DF0(U_app)e-d0. Differentiating the identity gives the exact
continuum linearized bias

J_t-kJ = Dk[e]H(U_app)+D^2H[d0,e].

Because d0_chi=0 in this formulation, its second term is obtained by varying
the G coefficients along d0, with no added chi-gradient direction.
The implementation retains both terms. The difference between the discrete
parent drift and this ordinary reference bias is saved as the spatial
differentiation/product-rule defect. It includes differentiated forcing and
lift discretization, not only a simple Leibniz-rule error.

No ordinary-reference formula is silently substituted for the first-u
background bias. That channel's full unsplit parent drift remains recorded.

At the finest saved outputs, added source drift is at most about 3.06e-25 over
all nodes. Remaining parent drift reaches about 4.48e-12. Ordinary background
bias reaches about 1.30e-15. This distinction matters: removing numerical
source drift has not made the original residual vanish.

## 6. Actual runs and matched controls

All owners are under source-intake/navier-stokes/20260909/.

| Owner directory | Result | Completed UTC | Meaning |
| --- | --- | --- | --- |
| annular-noether-completion-identities-initial | 16/16 | 03:00:15 | algebra/source construction |
| annular-noether-evolution-initial | FAILED 118/121 | 03:03:54 | interior-only completion |
| annular-noether-projected-evolution-final | FAILED 131/137 | 03:09:52 | joint scalar/lapse projection |
| annular-noether-scalar-projection-refined | FAILED 134/137 | 03:16:45 | selected scalar-only N512 run |
| annular-noether-projection-evidence-final | 59/59 | 03:17:59 | source replay, ownership, bounds |
| annular-noether-chain-rule-control | 18/18 | 03:20:36 | derivative and localization controls |

At T=0.3, the selected corrected full-constraint maxima are:

| Fixture/channel | Before correction | After correction |
| --- | ---: | ---: |
| canonical/reference | 2.04013e-11 | 6.09757e-14 |
| canonical/first-u | 3.50522e-12 | 3.24033e-13 |
| nonlinear/reference | 4.86928e-11 | 3.64910e-13 |
| nonlinear/first-u | 2.33157e-11 | 3.98246e-14 |

All eight full mass-constraint comparisons and all eight finite-grid boundary
accuracy checks pass. Compared with the previous N512 fixed-data method, the
largest component change is about 0.166% (canonical first-u mass). Scalar/q
changes are below 0.008%. Initial data are matched bitwise. These are finite-grid
method comparisons, not observational constraints or a physical parameter fit.

The selected run fails two T=0.1 max-norm spatial refinement gates:
canonical/reference factor 0.995874; nonlinear/first-u factor 0.929979.
The unchanged gate requires coarse-to-middle error >1.3 times middle-to-fine.
The middle-to-fine q errors are 1.87653e-12 and 1.26181e-12, about 0.0526% and
0.0811% of their q amplitudes. Both maxima occur at R=4.015625, immediately
inside the left boundary; corresponding interior maxima are 6.66470e-13 and
5.03642e-13. The coarse-to-middle maxima are at different interior locations.
This localizes the remaining numerical question; excluding the boundary would
not be an acceptable resolution.

The third failed check was the nonlinear T=0.3 constraint time derivative.
The original three-point backward diagnostic at step=0.00025 has error
1.27411e-14 against unchanged tolerance 1.14616e-14.
A postprocessor reconstructs the direct RHS and analytic chain rule from the
saved state, and separately tests the parent-source and linearized parts.
Five-point backward controls at steps 0.002,0.001,0.0005 have errors
8.42276e-16,8.48237e-16,3.64695e-15, respectively: all pass the original tolerance.
The original second-order control also improves when its step is halved.
At the smaller high-order steps, parent-source evaluation/cancellation error
dominates the very small derivative. These observations support a diagnostic
truncation/roundoff explanation, not evidence of a broken chain rule.
The original run nevertheless remains FAILED 134/137.

The evidence checker records signed numerical-source work, which is positive
at these samples. That is neither an energy-dissipation certificate nor, by
itself, an instability: the boundary flux and variable-coefficient terms have
not been included in that number. Do not describe the projected full scheme as
energy stable on the strength of source-norm contraction.

## 7. Reproducible implementation and safe next step

New implementation:
- scripts/annular_noether_completion_20260909.py
- scripts/derive_annular_noether_completion_20260909.py
- scripts/annular_noether_source_projection_20260909.py
- scripts/annular_noether_scalar_projection_20260909.py
- scripts/annular_noether_completion_evolution_20260909.py
- scripts/annular_noether_projection_evidence_20260909.py
- scripts/annular_noether_chain_rule_control_20260909.py

The execution snapshots and SHA-256 manifests preserve all failed attempts.
The selected evolution script SHA-256 is
b97950c759c96a8efce70ad4109cbae96273e15bd469dffcceacec6be03fb431.
Evidence SHA-256:
079195ca3033e2c617c6ef1f7559393041efc4ab0394ef155d43b3fbf5df11ce.
Derivative-control SHA-256:
8e79183e8614a28c8db176823b075962bb653acd3f13581d18c4c1f384356593.

Next substantive target: derive and test the **left-boundary truncation and
coupled energy estimate for this scalar-only completion**, including the
induced mass source. Use the saved boundary-localization evidence and an
independent manufactured/characteristic boundary control before another
resolution sweep. Do not merely remove the troublesome row or lower the gate.
Then propagate the controlled ordinary reference correction through the
curvature source and delta K, with its quadratic/background residual retained.

This is genuine progress on a constrained exterior evolution tool. It is not
a solution at a horizon or singularity, not a global regularity theorem, not a
derived empirical coupling, and not a transfer of any Navier-Stokes claim into
gravity. The larger MTS derivation programme remains open.

All jobs in this continuation ran serially, on one core at BelowNormal priority.
They have exited. No subagents, GitHub changes, or edits to the frozen
formalization-workbench, galaxy work, or other tasks were made. No processes
belonging to other tasks were stopped.

