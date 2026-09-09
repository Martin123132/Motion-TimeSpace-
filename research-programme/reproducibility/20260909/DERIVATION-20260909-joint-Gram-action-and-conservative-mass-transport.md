# Joint Gram action and a conservative energy-to-mass transport construction

Private continuation, 2026-09-09. Previous turn verified as progress from the
saved matched evolution, failure records, source-floor calculation and hashes.
This extends DERIVATION-20260909-compatible-current-smoke-and-coupled-variation.md.
Paths below are relative to post-checkpoint-work. No published files changed.

## 1. Result and scope

The full field variation of the proposed Gram potential is now independently
checked on the actual canonical/nonlinear annular backgrounds. A specified
discrete action gives scalar momentum, scalar force and metric variations
together. The metric equation absent after premature gauge fixing is recovered
by varying an off-gauge metric component before setting it to zero.

This does NOT itself prove a local discrete Bianchi identity. Instead, a separate
constructive calculation obtains an antisymmetric, finite-range energy current
from the existing Gram factors. In the canonical fixed-flat-metric, leading-
backreaction limit, the complete scalar action then supplies a cell-face mass
update that preserves the cell mass constraint exactly at semidiscrete level.
Its continuum flux agrees under refinement with the GR scalar stress formula.
Both the original and Gram-augmented operators receive the same controls.

The full dynamical metric, nonlinear kinetic sector, physical incoming boundary
conditions, affine parent-response forcing and curvature reconstruction are NOT
yet attached to this face-mass formulation. The failed 157/164 coupled evolution
remains failed. We have not replaced the full objective with this easier limit;
this is a necessary conservative transport component for the same annular route.

## 2. Full coefficient and potential variation

Use t=v-sigma(r-4), q=chi_t, w=chi_R, E=exp(delta),
F=1-2mu/r-Lambda r^2/3, p=q/E, s=w-sigma q. Introduce beta=g_rr in the original
(v,r) metric before gauge restriction:

    ds^2=-E^2 F dv^2+2E dv dr+beta dr^2+r^2 dOmega^2,
    d=1+F beta,
    X=(2ps+Fs^2-beta p^2)/d,
    K=-X/2-V+b2 X^2+b3 X^3,
    P=-2K_X=1-4b2 X-6b3 X^2.

The explicitly chosen extension of the principal coefficient is

    a(Phi)=r^2 E [F P/sqrt(d)+2P_X(p+Fs)^2/d^(3/2)].

At beta=0 it equals the actual r^2 c from the existing constitutive code. It is
the natural scalar principal-density extension for this metric; it is not
claimed to uniquely determine a covariant discretization of the spatial Gram
stencil. Different off-gauge stencil constructions remain a real issue.

Write the already derived positive remainder as

    R_a = T^T diag(S a) T / h,
    U=chi^T R_a chi/2,
    rho=S^T (Tchi)^2/(2h),    U=sum_i a_i rho_i.

T contains the fixed third-difference Gram factors; S is their nonnegative
linear coefficient interpolation. Thus rho>=0, and signed coefficient
variations are legal without changing Gram edge orientations. For independent
primitive field variations e,z,

    DU[e]=e_chi^T R_a chi + 1/2 chi^T R_{Da[e]} chi,
    D2U[e,z]=e_chi^T R_a z_chi
             + e_chi^T R_{Da[z]} chi + z_chi^T R_{Da[e]} chi
             + 1/2 chi^T R_{D2a[e,z]} chi.

This is the full Hessian, not only its frozen scalar block. Canonically,

    a=r^2 E F, a_q=a_w=0,
    a_mu=-2rE, a_delta=a, a_beta=-r^2 E F^2/2,
    D2a[e,z]=-2rE(e_mu z_delta+z_mu e_delta)+a e_delta z_delta

for variations tangent to beta=0. Mixed scalar/mass Hessians do not vanish:
one N128,t=.1 test gives 1.714e-13 canonically and 1.691e-13 nonlinearly,
entirely from a coefficient-variation term omitted by a frozen scalar Hessian.
These are normalized numerical directional values, not calibrated couplings.

### Numerical cancellation found and corrected

The first implementation evaluated bilinears by forming R_a chi and then
contracting. Four tiny symmetry comparisons failed, giving 670/674. That failed
owner and its scripts are retained unchanged. The identical bilinears are now
evaluated as (Tu)^T diag(Sa)(Tv)/h, which avoids subtracting large intermediate
nodal quantities. The same tolerances, plus a failure-preservation check, pass
675/675. Independent complex-step first variations and two-step mixed finite
differences remain separate from the analytic Hessian formula.

## 3. One proposed action, including the lost metric variation

Let H denote the diagonal quadrature weights and D the existing SBP derivative.
The following is a specified action germ through first order in beta, after
continuum integration by parts. It suffices to define its first variations at
beta=0; it is not a complete ungauged finite-grid Einstein theory:

    L_h = sum_i H_i {
      E/ kappa (Dmu-sigma mu_t)
      + beta/(2kappa) [ -mu_t + EF(Dmu-sigma mu_t)
                        -rF^2(DE-sigma E delta_t) ]
      + r^2 E sqrt(d) K(X,chi) } - U.

In particular DE is the discrete derivative of E, NOT E Ddelta. Their equality
cannot be assumed on a finite grid. In the scalar variation w=Dchi+I, where
the probe's I is fixed rather than silently set to zero. The initial probes
retain the actual nonzero integrability and parent-defect values.

The beta gravitational coefficient was independently checked by computing the
four-dimensional Christoffels, Ricci tensor and Einstein tensor:

    G^{rr}+Lambda g^{rr}
      =2mu_v/(E r^2)-2F mu_r/r^2+2F^2 delta_r/r.

Consequently variation with respect to g_rr contributes
-E r^2(G^{rr}+Lambda g^{rr})/(4kappa), giving the displayed beta coefficient.
The continuum bulk match is exact. Original gravitational boundary total
derivatives and the actual problem's boundary data are not thereby resolved.

Denote U_z=rho a_z for z=q,w,mu,delta,beta; U_chi=R_a chi. At beta=0 the scalar
momentum and force from this action are

    Pi_chi=H r^2 h_current-U_q,
    L_chi=-H r^2 E V_chi-D^T(H r^2 f)-U_chi-D^T U_w,
    (Pi_chi)_t=L_chi + external scalar boundary covector.

The gravitational momentum is Pi_mu=-sigma H E/kappa. The modified scalar
Legendre derivative at fixed chi,w,mu,delta is diagonal:

    M_eff=H r^2 alpha-rho a_qq.

All 18 actual background probes retain positive M_eff; the largest relative
change is 5.15e-12 in these samples. This is neither a neighborhood nor a
uniform hyperbolicity theorem. Nonlinear coefficient dependence also changes
the q/w/metric cross derivatives of Pi_chi, which must be retained in evolution.

All-row action gradients are tested against direct variation, including the
endpoint rows of D^T. The interior metric equations, or equations with the
corresponding endpoint covectors explicitly supplied, reduce to

    Dmu-sigma mu_t = R_parent + kappa U_delta/(H E),
    DE/E-sigma delta_t = kappa r P s^2-kappa U_mu/(H E),
    mu_t = C_parent + kappa[ F U_delta+rF^2 U_mu-2U_beta ]/H,
    R_parent=-kappa r^2(K+Pps),
    C_parent=kappa r^2 q f/E.

The last equation follows by eliminating the first two from the beta equation;
it is not imposed as a separate empirical closure. The weak endpoint covector
from the mu variation includes B_boundary E/kappa and has NOT been dropped in
the validator. It still needs matching to the physical boundary prescription.

Canonically, the added mass-time source cancels exactly, while

    Delta R= kappa r^2 F rho/H,
    Delta(lapse radial source)=2kappa r rho/H.

That cancellation is not evidence that no energy travels through the Gram
coupling. Its discrete energy flux is generally nonzero, as derived next.
This is why varying a chosen action is not by itself a proof that its metric
equations implement the required local lattice conservation law.

## 4. Time Noether identity and an explicit local energy current

For the proposed time-independent finite-dimensional action, with fixed I,

    d/dt(sum_A Pi_A A_t-L_h)=sum_A[(Pi_A)_t-L_A] A_t.

All-row direct complex-step tests verify this identity on arbitrary paths
through each of the 18 actual backgrounds. These are virtual-work tests, not
solutions. The Gram sector is tested separately so its tiny contribution is
not hidden underneath a much larger gravitational term. Its energy addition
is U-q.U_q, not necessarily just U when a depends on q.

There is also an exact transport identity for the restoring-force part. Choose
the positive nodal potential energy e_U,i=a_i rho_i and define

    J^Gram_ij = sum_l (Tchi)_l/h
       [ T_li q_i S_lj a_j - T_lj q_j S_li a_i ].

It is antisymmetric and has finite range (at most five node separations in
these closures). Direct summation gives

    sum_j J^Gram_ij = q_i(R_a chi)_i-a_i rho_t,i,
    -q_i(R_a chi)_i + (e_U,i)_t
       = -sum_j J^Gram_ij + rho_i a_t,i.

The last term is retained coefficient/metric work, not deleted as damping.
For a cut after node k, define F^Gram_{k+1/2}=sum_{i<=k,j>k} J^Gram_ij.
Then the difference of adjacent cut fluxes is exactly the nodal divergence.
All nodes, cuts and coefficient-work terms are verified; software 130/130.
This derived graph current is NOT yet a Hilbert stress tensor.

## 5. Constructive canonical energy-to-mass correspondence

To determine whether the graph current can do useful gravitational work, use
the canonical fixed-flat-metric leading-stress limit E=F=1, sigma=.05,
kappa=.1. The scalar can source a mass response at leading order without
including its metric backreaction in the leading wave equation. This is not
an exact self-gravitating solution or a new assumption about the full parent.

Set M=H r^2 alpha, N=H r^2 B, C=H r^2 c, with
alpha=sigma(2-sigma), B=1-sigma, c=1. The same scalar action gives

    M q_t = A q-(D^T C D+R_a)chi,   A=N D-D^T N=-A^T,
    chi_t=q,
    e_i=(M_i q_i^2+C_i(Dchi)_i^2)/2+a_i rho_i.

Its remaining pair currents are

    J^adv_ij=-A_ij q_i q_j,
    J^grad_ij=D_ji q_i C_j(Dchi)_j-D_ij q_j C_i(Dchi)_i.

With J=J^adv+J^grad+J^Gram, direct substitution proves
e_t,i=-sum_j J_ij, including endpoints. The action's closed-system endpoint
forces are part of this identity; it is not yet the old absorbing-SAT problem.
External forces add their explicit work, rather than being silently erased.

Let F be the cut flux of J. Put the gravitational mass on cell faces and set

    mu_{i+1/2}-mu_{i-1/2}=kappa e_i/E,
    (mu_{i+1/2})_t=-kappa F_{i+1/2}/E + common boundary-anchor rate.

For fixed E the derivative of this cell constraint is identically zero.
This is a constructive discretization-level conservation law, not the earlier
collocated Dmu constraint with its incompatible source. The face positions
use cumulative SBP quadrature weights; the interior positions are ordinary
half-grid locations. The arbitrary integration anchor used in the verifier
is diagnostic, not a derived physical mass boundary value.

The correspondence is not only algebraic bookkeeping. On two smooth packets
with endpoint-zero velocities, compare every face with the existing GR
leading scalar flux, using analytic packet derivatives:

    mu_t,continuum=kappa r^2 q[(1-sigma)q+chi_R].

At N=32,64,128 the maximum all-face errors and coarse/fine ratios are:

| Packet / operator | N32 error | N64 error | N128 error | Ratios |
|---|---:|---:|---:|---|
| symmetric / baseline | 8.784e-6 | 2.066e-6 | 5.055e-7 | 4.252, 4.087 |
| symmetric / Gram | 8.428e-6 | 2.044e-6 | 5.041e-7 | 4.124, 4.055 |
| asymmetric / baseline | 1.360e-5 | 4.057e-6 | 1.056e-6 | 3.351, 3.841 |
| asymmetric / Gram | 1.473e-5 | 4.131e-6 | 1.061e-6 | 3.565, 3.894 |

Both operators pass the predeclared ratio>=2.5 gate; neither gets special
treatment. At N128 the largest cell-constraint time residual is 8.14e-19
across these controls, consistent with floating arithmetic. The exact identity
is proved above; the finite measurements are not interval-certified errors.
The observed flux accuracy is roughly second order, not a claim of fourth-
order face accuracy or a continuum convergence theorem. Software 56/56.

## 6. Next target, without declaring the full branch solved

Use this derived face transport as the starting point for a dynamically
coupled metric discretization, not as an independently fitted source:

1. Derive the placement/interpolation of face mu into nodal F, and the lapse
   and coefficient-work terms, from one specified discrete geometry/action.
2. Determine whether its metric variation actually supplies the graph flux.
   If the current beta extension does not, derive the missing bond/coframe
   variation; do not insert the graph current and call it Hilbert stress.
3. Derive physical incoming boundary ports and the common mass-anchor rate,
   retaining the previous annular boundary data and nonzero parent forcing.
4. Only then derive the forced response linearization/time jets and perform a
   matched evolution. Recover the continuum GR constraints, not just a renamed
   numerical constraint, and repeat the curvature/strong-norm checks.

Nonlinear P(X), evolving geometry, full local-GR/first-u estimates, horizon
regularity, EM and calibrated source coefficients remain separate obligations.
No new galaxy or public-repository work occurred. No previously failed result
was altered, no subagent used, and all continuation jobs have exited.

## 7. Saved evidence

Owners under source-intake/navier-stokes/20260909:
- annular-Gram-joint-action-derived/status.json: FAILED 670/674; four floating
  symmetry failures preserved, no COMPLETE.
- annular-Gram-joint-action-stable/status.json: 675/675, 10:13:23 UTC.
- annular-Gram-energy-transport-derived/status.json: 130/130, 10:16:03 UTC;
  18 hashed transport arrays.
- annular-canonical-face-mass-transport-derived/status.json: 56/56,
  10:20:53 UTC; 12 hashed face-transport controls.

Scripts:
- scripts/annular_gram_joint_action_20260909.py
- scripts/derive_annular_gram_joint_action_20260909.py
- scripts/annular_gram_stable_hessian_20260909.py
- scripts/derive_annular_gram_joint_action_stable_20260909.py
- scripts/derive_annular_gram_energy_transport_20260909.py
- scripts/derive_annular_canonical_face_mass_transport_20260909.py

The dense factor matrices in these helpers are small derivation diagnostics,
not a commitment to dense high-resolution evolution. All work is private and
single-core/BelowNormal; nothing was pushed, and other tasks were not stopped.
