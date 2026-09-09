# Metric-flux cancellation, differentiated constraint jets, and radial bounds

Date: 2026-09-09. Private, canonical annular branch only. No new trajectory,
action modification, physical residual cancellation, or public upload.

## 1. Progress and scope

Three concrete advances follow the previous scalar coefficient bounds:

1. Derived a clock-rate/energy-flux cancellation from the actual canonical
   radial and scalar equations, with every finite-action defect retained.
2. Derived the finite constraint branch's second time jets by second-order
   chain rules. They no longer require finite differences of complete ODE
   evaluations. The previous estimates agree within 4.02e-8 in the full
   packed acceleration vector at all 18 saved states.
3. Derived scalar H2 control and explicit radial lower bounds for F and N.
   The residual-inclusive chart lower bound is F>=0.63244 on the saved
   fixtures, versus actual minima about 0.65957. This is a conditional radial
   estimate, NOT a proof of a time-global positive chart.

The remaining evolution problem is specific: uniform control of the inverse
differentiated metric constraint map, its boundary trace, and the paired
defects in the clock-rate identity. We have NOT proved full shift/DAE
closure, nonlinear P(X) regularity, black-hole regularity, or a full MTS-to-GR
limit. A conditional annular theorem must not be relabeled any of those.

Only b2=b3=m_chi=Lambda=0 and kappa>0 are covered. The same GR and canonical
Gram branches, released scalar slopes, prescribed scalar-value histories,
and outer clock action are used throughout. kappa=0.1 is the owned fixture
normalization, not a newly measured fundamental coupling.

## 2. Source owners and verification

Previous theorem:
`DERIVATION-20260909-mesh-uniform-coefficient-and-boundary-source-bounds.md`.
Constraint action and natural boundary:
`scripts/annular_constraint_routhian_20260909.py` and
`DERIVATION-20260909-constrained-initial-slice-solve-and-mass-flux-tangent.md`.
Actual released tangent:
`scripts/annular_released_hermite_action_20260909.py`.
Actual metric-link shift current:
`scripts/annular_metric_link_quadratic_20260909.py`.

New jet/profile/weak-reconstruction helper:
`scripts/annular_metric_flux_jets_20260909.py`.
Its derivation runner:
`scripts/derive_annular_metric_flux_jets_20260909.py` (derive phase).
Radial-bound companion and **combined final seal owner**:
`scripts/derive_annular_radial_metric_bootstrap_20260909.py` (derive/seal).
Results:
`source-intake/navier-stokes/20260909/annular-metric-flux-jets-derived/status.json`
and
`source-intake/navier-stokes/20260909/annular-radial-metric-bootstrap-derived-v2/status.json`.
Combined integrity:
`source-intake/navier-stokes/20260909/annular-coupled-metric-bootstrap-final-integrity.json`.

External context checked: the primary [Choptuik/Lehner/Pretorius course
index](https://laplace.physics.ubc.ca/2010-pi-nr/www/bgsoft.html) lists
Einstein-massless-Klein-Gordon lectures. Its linked PDF timed out; no formula
or theorem here is attributed to unread contents. Equations below are derived
from the locally owned action, rather than transplanted with an unchecked
normalization. This is not a claimed use of the social-media Navier-Stokes result.

## 3. Canonical radial equations and exact residual definitions

On the annulus [a,b] let

    F=1-2mu/R, E=N/sqrt(F), c=N sqrt(F)=E F,
    q=chi_t, w=chi_R, v=q/c, S=v^2+w^2,
    A=R F=R-2mu, theta=c_t/c, eta=E_t/E.

The canonical static action density is

    L=N mu_R/(kappa sqrt(F))
       +R^2 q^2/(2N sqrt(F))-R^2 N sqrt(F)w^2/2.

Varying N and mu gives the continuum GR radial equations

    mu_R=(kappa/2)R^2 F S,
    (log E)_R=kappa R S.

Define, without setting them to zero on a finite grid,

    r_H=mu_R-(kappa/2)R^2 F S,
    r_E=(log E)_R-kappa R S,
    r_v=v_t-R^-2 (R^2 c w)_R,
    r_w=w_t-(c v)_R.

The last is kinematic: the actual reconstructed chi and q make r_w=0 up to
arithmetic. r_v includes the canonical Gram force in the candidate, plus
the finite weak-to-strong discrepancy and boundary reactions. It is not
automatically a numerical error or an unphysical term to remove.

The corresponding strong bulk metric Euler densities are exactly

    L_N=r_H/(kappa sqrt(F)),
    EL_mu=(E/kappa)[-r_E+r_H/(R F)].

This follows by differentiating L_muR=E/kappa; the mu_R terms in the mu
variation cancel. These equations explain which physical variations own
the residuals, instead of inventing new closure coefficients.

## 4. Finite weak equations are not pointwise radial equations

Let Q be the actual quadrature, P the mass-face reconstruction, and V the
lapse-node reconstruction. The exact lapse covector is

    C_N=V^T Q[r_H/(kappa sqrt(F))]+Gram_N.

For mass test functions, the exact mass covector is

    C_mu=P^T Q[(E/kappa)(-r_E+r_H/A)]
          +delta_IBP+boundary_natural+Gram_mu,
    delta_IBP=(P_R^T Q[E]+P^T Q[E_R]-[-E_a,0,...,E_b])/kappa,
    boundary_natural=[-E_a,0,...,E_b-E_prescribed]/kappa.

The inner entry is a retained fixed-mass reaction. The actual outer nodal
E trace is NOT replaced by the prescribed clock before this reconstruction.
For the owned positive Gram energy, rho=S_sampling^T(T chi)^2/(2h),

    Gram_N=-rho R_node^2 sqrt(F_node),
    Gram_mu=P_node^T[rho R_node N_node/sqrt(F_node)].

Both complete covectors, including all boundary entries, are independently
reconstructed against the old action gradient. Hence small free weak
covectors do not license setting r_H or r_E pointwise to zero. On the saved
states their pointwise residuals are much larger than the weak solve error.

## 5. Important distinction: physical mismatch versus bulk-flux defect

Define the continuum canonical bulk flux

    s=kappa R^2 F q w=kappa R^2 F c v w.

The old physical finite mismatch remains

    d=mu_t-s_mu,

where s_mu is the ACTUAL full shift solve including metric-link Gram current.
The cancellation below instead contains the pointwise bulk-flux defect

    D=mu_t-s=P d+(P s_mu-s).

P denotes reconstruction where needed. The second term contains weighted
projection and, in MTS, the Gram current. It is saved separately. Confusing
D with d would erase a real candidate contribution even if d vanished.
The old d arrays and full shift covectors are checked unchanged.

## 6. Clock-rate cancellation, including every defect

Differentiate S using the two scalar equations:

    S_t=2c(vw)_R+4(c_R+c/R)vw+2(v r_v+w r_w).

Since eta_R=kappa R S_t+(r_E)_t, rearrangement using s gives

    eta_R=2/A[s_R+s(log E)_R]+(r_E)_t+2kappa R(v r_v+w r_w).

Also theta=eta-2mu_t/A. Substitute mu_t=s+D and both radial residuals:

    theta_R=2s/A^2-2(D/A)_R+Delta,
    Delta=2s r_E/A-4s r_H/A^2+(r_E)_t+2kappa R(v r_v+w r_w).

This is an exact off-shell identity for the reconstructed fields. The
potentially high spatial derivatives in the ideal canonical GR case cancel:
when D=r_H=r_E=r_v=r_w=0 along the solution,

    theta_R=2s/A^2=2kappa q w/F.

Thus the clock-rate gradient is driven by scalar flux, not an independently
chosen motion/clock law. This is a consequence of the canonical GR equations;
it is not a new observational prediction or a proof of the whole MTS parent.
For MTS and the actual finite system, Delta and D stay in the formula.

Integration yields the corresponding amplitude law

    theta(R)=eta_b-2s_b/A_b-integral_R^b [2s/A^2+Delta] dx-2D(R)/A(R).

The true eta_b equals E_prescribed,t/E_prescribed plus the time derivative
of log(E_trace/E_prescribed). That clock-trace discrepancy is measured,
not discarded. Composite Gauss8 and Gauss12 reconstructions of the inner
theta from the outer boundary agree with its direct value within 3e-18.

For example, if A>=a F_0>0, an explicit coefficient estimate is

    ||theta_R||_infty
      <=2||s||_infty/(a^2 F_0^2)+2||(D/A)_R||_infty+||Delta||_infty.

This does not yet bound the last two terms from the discrete equations.
Large individual terms can cancel; taking absolute values prematurely is
conservative but can hide the compatibility structure needed for closure.

Differentiating the integrated identity exposes the next time-jet terms:

    theta_t(R)=eta_b,t-2s_b,t/A_b-4s_b mu_b,t/A_b^2
       -integral_R^b [2s_t/A^2+8s mu_t/A^3+Delta_t] dx
       -2D_t/A-4D mu_t/A^2.

In particular a small d does not bound d_t, D_t, Delta_t, or the outer flux
derivative. This displayed derivative is an analytic consequence of the
identity; the integral verification in the runner concerns theta itself,
not an independently certified bound for Delta_t.

## 7. Second metric time jets derived from the finite constraints

Write x=(mu_faces,N_nodes,q_nodes,s_dot_nodes), and z for scalar coordinates,
their momenta, and the prescribed outer clock. The same free constraint map
C(x,z) has Jacobian J=C_x. The old tangent differentiates C along its branch;
it preserves any initial roundoff residual, rather than proving C initially
zero. For its second derivative,

    J x_tt + C_xx[x_t,x_t]+2C_xz[x_t,z_t]
             +C_zz[z_t,z_t]+C_z z_tt=0 on free rows.

A second-order jet algebra evaluates this exact chain rule directly from
the explicit canonical metric/Legendre gradients in section 3, including
the nodal Gram variation and outer boundary action. Each jet stores the
value, first derivative and SECOND derivative (not half the derivative).
Product and power rules include the appropriate factor 2 in cross terms.

The phase accelerations are not free inputs: chi_tt and slope_tt come from
the old tangent; momentum second derivatives are complex-step first
derivatives of the old scalar forces along that same tangent. Likewise the
inner fixed mass acceleration is the derivative of the full shift solve.
Both fixed endpoint q accelerations are zero at this order because the
prescribed scalar histories are quadratic. E_prescribed,tt=0 here.

With known curved-phase forcing T and fixed x_tt entries, solve the same
free J block for x_tt. No pseudoinverse, damping, new boundary data, or
constraint projection is introduced. This also derives

    d_t=mu_tt-(s_mu)_t

at each saved state, including the Gram current's derivative.

All 18 free second-chain-rule residuals are <=1.56e-15. Independent
quadratic-path differences check the jet implementation on N16. The old
directional ODE accelerations agree within 4.02e-8. These are analytic
derivatives evaluated in floating point, NOT exact-real or interval
certificates, and not a mesh-uniform bound on J^-1.

## 8. Scalar H2 and bulk-flux control without a third-derivative assumption

Use C2 and C_e from the preceding quadrature/Gram elliptic comparison.
For its auxiliary H2 solution U, cubic Hermite interpolation also obeys

    ||(I_h U)_RR||<=4||U_RR||.

Proof: after subtracting an affine function, the right-endpoint value and
derivative bounds used previously multiply second basis-derivative norms
sqrt(12) and 2. This gives 2+2=4. The error u_h-I_hU has first-derivative
norm <=h C_e||f||. Apply the already-certified inverse16 estimate to its
piecewise quadratic derivative:

    ||u_h,RR|| <= (4C2+16C_e)||f||.

All slopes are free, so this is the same C1 cubic space, not an extra
boundary condition. For the lifted scalar configuration, l_RR=0 and

    ||chi_RR|| <= (m_+/sqrt(m_-))(4C2+16C_e)(sqrt(2Ehat)+F_b).

F_b is the previous unchanged affine boundary-force bound. The continuous
H2 norm exists because the reconstruction is C1; no jump of chi_R is hidden.

Let E0=(q^T M_full q+chi^T K_full chi)/2, the positive CANONICAL SCALAR
energy, not the complete gravitational Hamiltonian. It controls ||q|| and
||w|| through m_- and p_-. Ehat controls ||q_R||. The elementary 1D bound

    ||f||_infty<=ell^-1/2||f||+sqrt(ell)||f_R||

therefore controls both q and w, and hence

    ||s||_infty<=kappa b^2 F_max ||q||_infty ||w||_infty.

At final time ||chi_RR|| is about 0.127 in both branches on all three grids;
the analytic upper bounds are approximately 19.69 (GR) and 27.74 (Gram).
These are deliberately loose conditional bounds, not precision predictions.

## 9. Radial F, clock and lapse bounds derived from the constraints

The mass residual equation makes F satisfy a LINEAR radial equation once
S and r_H are supplied:

    F_R+(1/R+kappa R S)F=(1-2r_H)/R.

Its integrating-factor solution is

    F(R)=(a/R)exp[-integral_a^R kappa x S dx]F(a)
         +(1/R)integral_a^R exp[-integral_s^R kappa x S dx](1-2r_H(s)) ds.

Set S1>=||S||_L1, H1>=||r_H||_L1, R1>=||r_E||_L1. Since S>=0,

    F_lower=(a/b)exp(-kappa b S1)F(a)-2H1/a,
    F_upper=max(F(a),1)+2H1/a,
    E_lower=E_trace(b)exp(-kappa b S1-R1),
    E_upper=E_trace(b)exp(R1).

The E bounds follow by integrating (log E)_R=kappa R S backward from the
actual outer trace. Its difference from E_prescribed remains explicit.
If F_lower>0 then

    E_lower sqrt(F_lower)<=N<=E_upper sqrt(F_upper),
    E_lower F_lower<=c<=E_upper F_upper.

If F_lower<=0 this estimate refuses to certify a positive chart; it is not
clipped to a small positive number. A manufactured large-residual control
checks this failure mode. A negative lower bound is a failed sufficient
condition, not proof of a physical horizon or singularity.

The numerical test uses conservative analytic norm majorants, not a lucky
quadrature cancellation of signed residuals:

    S1=||q||^2/(N_min^2 F_min)+||w||^2,
    H1=TV(mu)+(kappa/2)b^2 F_max S1,
    R1=TV(log N)+one_half TV(log F)+kappa b S1.

The scalar polynomial norms are integrated exactly by the positive rule;
N and F are monotone inside each union cell, so these total variations
come from its endpoint values. The arithmetic remains ordinary floating
point, not outward-rounded interval arithmetic. These majorants use the
actual metric variations: they demonstrate the formula, not a closed
bootstrap eliminating all metric dependence from its right-hand side.

Across the saved states the resulting lower bounds remain F>=0.632442 and
N approximately >=0.778712, with actual minima F about 0.659571 and N about
0.812081. They retain a substantial annular margin, with nearly identical
GR/Gram results. They say nothing about evolution into a horizon.

For a time bootstrap, the inner value must also be controlled:
F(a,t)=F(a,0)-(2/a)integral_0^t mu_t(a,s) ds. The actual inner rate is supplied
by the full shift solve, not held constant during the existing evolution.

## 10. Matched diagnostics: what is and is not improving

All following values are at the old final relative time 0.01, not maxima
over the entire trajectory. No new evolution was required.

| Grid | branch | max abs d | max abs d_R | max abs d_t | max abs theta_R |
|---|---|---:|---:|---:|---:|
| N16 | GR | 2.477e-6 | 8.827e-4 | 1.612e-4 | 1.039e-3 |
| N16 | Gram | 6.200e-6 | 1.120e-3 | 3.871e-4 | 1.031e-3 |
| N32 | GR | 4.049e-7 | 2.678e-4 | 2.050e-4 | 5.805e-4 |
| N32 | Gram | 9.132e-7 | 5.702e-4 | 2.458e-4 | 5.802e-4 |
| N64 | GR | 4.908e-8 | 5.716e-5 | 1.012e-5 | 3.554e-4 |
| N64 | Gram | 2.518e-7 | 1.461e-4 | 1.055e-4 | 3.554e-4 |

The final physical mismatch and its spatial gradient shrink on these grids
in both branches. Its time derivative is larger for Gram, and the GR N16
to N32 change is NOT monotone. Do not infer a universal convergence order.
The nonzero theta_R is not itself a failure: scalar flux already predicts
a nonzero clock-rate gradient in continuum GR.

At N64 the leading flux term is about 1.2944e-4 in both branches. The full
Delta maximum is about 1.9482e-4, and the D-derivative term about 4.2086e-4.
There are cancellations, not grounds to drop either term. The lapse and
Hamiltonian strong residual L1 diagnostics shrink by roughly a factor two
per refinement, whereas their free weak covectors are near solve precision.

300/300 jet/flux/weak-reconstruction/H2 checks and 112/112 radial-bound
checks pass. These are implementation checks, not independent physics tests.
The first radial runner attempt hit NumPy-boolean JSON serialization before
completion; its executed source and failure ledger are retained. The rerun
changes only that serialization and output location, not equations or gates.

The combined seal verifies old source/output hashes, compiles the new
sources through their runners, pins the mutable resume, and checks zero
frozen-workbench writes by mtime since 2026-09-09T17:10:00Z. This is not a
full pre-turn hash comparison. All jobs finished; no background worker remains.

## 11. Next concrete derivation

Use the actual differentiated constraint Hessian, now with derived first
and second forcing rather than guessed metric accelerations. Partition its
free rows into metric variables and free scalar velocities:

    J=[[A_metric,B],[B^T,M_free]],
    S_metric=A_metric-B M_free^-1 B^T.

M_free is the positive canonical scalar Legendre block. Exact elimination
gives the metric rate/acceleration through S_metric^-1 and the corresponding
Schur-complemented forcing. Derive a mesh-uniform inverse estimate in
physical/weighted norms, keeping the outer natural row and inner shift rate.
Start from the same canonical GR system and then retain the Gram perturbation.
Do not mistake a finite raw condition number for this theorem.

Use that map to bound the PAIRED compatibility remainder
Delta-2(D/A)_R, its time counterpart, and the actual outer clock/flux trace.
This is the missing coupled evolution estimate. The new radial and scalar
bounds show how it would close the bootstrap, but they do not supply it
automatically. Do not repeat the already-completed scalar energy or local
second-jet derivations as another missing-input inventory.
