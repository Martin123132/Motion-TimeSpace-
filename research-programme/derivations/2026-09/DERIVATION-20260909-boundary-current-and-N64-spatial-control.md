# Boundary current, affine remainder bound and N64 spatial control

2026-09-09. Private local continuation. No GitHub action or edits to the
frozen workbench. All new evolution uses the unchanged released-Hermite
action, data and equations. This is a finite-action derivation and short
numerical consistency study, NOT local-GR recovery or black-hole regularity.
No external Navier-Stokes theorem is imported by this step.

## 1. Outcome in plain terms

The scalar/gravity boundary current has been derived, including the Gram
link current, nonlinear coefficient work and the temporal surface term.
Global energy balance does NOT imply that each endpoint mass/flux balance
vanishes separately: both can retain the same nonzero offset.

The full affine Ward identity now reconstructs that offset without fitting
or subtracting it. A piecewise-smooth positive-chart bound has also been
derived for the affine Gram-link interpolation error, including the lapse
derivative jumps which a globally smooth interpolation estimate would miss.

Twelve N64 short evolution runs finish. At matched sample times, N32-to-N64
maximum candidate mass-rate mismatch improves by about 2.93 and 3.08;
maximum weak shift residual improves by about 12.16 and 8.96. GR improves
too. The candidate still has the larger weak shift residual and larger
boundary offset. There is no numerical victory claim.

## 2. Scope, conventions and unchanged data

Continue the action and phase space in
`DERIVATION-20260909-released-Hermite-slope-dynamics.md`.
The branch label GR means the same Einstein/scalar system WITHOUT the Gram
term. For the nonlinear fixture the scalar is P(X), not canonical matter;
this comparator is not a claim that vacuum GR contains that scalar.

The scalar reconstruction and scaled interpolation coordinate are

    chi_h=H_chi chi+H_I I,  q_h=H_chi q+(H_I/h) v_s,
    s=hI,  v_s=s_dot,  p_s=Pi_I/h,
    F=1-2mu/R-Lambda R^2/3,  L=F^(-1/2),
    X=-q_h^2/N^2+F w_h^2,  P=1-4b2 X-6b3 X^2.

Mass and shift use the face P1 reconstruction; lapse uses nodal P1.
All formulas here are evaluated at V=V_t=0 AFTER variation of the original
shift-unfixed action. They are not equations obtained by deleting V first.

With L0=L_bulk-U_Gram, the released Routh functional is

    R=L0-pi_chi dot q-p_s dot v_s-E_b mu_b/kappa,
    y=(mu_faces,N_nodes,q_nodes,v_s_nodes),  G=R_y, H=R_yy.

Fixed entries are inner mass and the two scalar endpoint velocities.
All lapse entries, other mass entries, interior q and all v_s are free.
Scalar value histories and E_b(t) are retained identically in both branches.
The inner mass speed comes from the original full weak shift solve, but
the remaining shift equations are diagnostic and are NOT all satisfied.

Numerical lengths/times/fluxes below retain the fixture normalization.
They are not converted into metres, seconds, measured energy or bounds on
parent couplings. No new physical parameter or boundary counterterm is fit.

## 3. Actual canonical energy and both endpoint orientations

The full scalar momentum includes its endpoint reactions; it is NOT the
stored pi_chi whose endpoint entries are kept at zero:

    Pi_chi=H_chi^T W[R^2 L P q_h/N]-rho a_q,
    Pi_s=(H_I/h)^T W[R^2 L P q_h/N],
    rho=S^T[(Tchi)^2]/(2h).

Omit the rho a_q term in the GR control. The coefficient a is the existing
scalar radial principal coefficient, not a new coupling. At zero shift,

    a=R^2 N L [P F+2 P_X F^2 w^2],  P_X=-4b2-12b3 X.

Its derivatives are taken from the full shift-dependent expression before
setting V=0; see `scripts/annular_adm_mixed_action_20260909.py`.

Rescaling N,q,v_s together by a positive constant rescales L0 by that
constant. Euler's homogeneous-function identity therefore gives

    q dot Pi_chi+v_s dot Pi_s+N dot G_N=L0,
    E_total=q dot Pi_chi+v_s dot Pi_s-(L0-E_b mu_b/kappa)
           =E_b mu_b/kappa-N dot G_N.

This constrained boundary energy is not by itself a positive, coercive
scalar energy norm. Its exact time-work identity is

    d_t E_total+q dot E_chi+v_s dot E_s
       +mu_dot dot G_mu+N_dot dot G_N-E_b_dot mu_b/kappa=0,

where E_chi=L_chi-d_t Pi_chi and E_s=L_s-d_t Pi_s. Explicit clock work must
not be dropped before deriving the endpoint balance.

Let the outward orientations be n_a=-1,n_b=+1. Report energy flux in the
positive coordinate-R direction at BOTH endpoints:

    F_a=-q_a E_chi,a,   F_b=+q_b E_chi,b,
    E_a,var=-kappa G_mu,a,
    r_a=E_a,var mu_dot_a/kappa+F_a,
    r_b=E_b mu_dot_b/kappa+F_b.

Direct differentiation of the homogeneous identity yields

    r_b-r_a =
      -q_int dot E_chi,int-v_s dot E_s
      -sum_(mu indices except a) mu_dot G_mu
      +N dot d_t G_N.

Thus solved free equations imply r_b=r_a, NOT r_b=r_a=0. This is an
off-shell identity with the displayed remainder retained; the validation
also deliberately perturbs mass speeds off shell and checks that remainder.

For continuum normalization only, the GR/scalar control has

    F_scalar=q L_matter,w=-R^2 N sqrt(F) P q w,
    mu_t=kappa R^2 F P q w=-kappa F_scalar/(NL).

With the natural continuum clock E_b=NL this gives
E_b mu_t/kappa+F_scalar=0. The finite variational clocks and physical NL
traces need not coincide exactly. The code saves both and imposes neither
an additional zero-offset equation nor a compensating flux.

## 4. Oriented Gram-link current and endpoint corrections

Write z=Tchi, z_t=Tq, a_bar=Sa, rho_dot=S^T(z z_t)/h. The Gram scalar
Euler contribution follows directly from varying -U_Gram:

    g_T=T^T(a_bar z)/h,
    g_w=D^T(rho a_w),
    E_chi,Gram=-g_T-g_w+d_t(rho a_q).

The last derivative includes the actual mu_dot,N_dot,q_dot and
w_dot=Dq+v_s/h. None of these coefficient histories is frozen.

For factor l and sampled scalar node i, define the pair current

    j_li=a_i S_li z_l z_t,l/h-q_i T_li a_bar_l z_l/h.

Its sum over i is zero for every factor. Let sigma_li(R) be sign(target
minus anchor) on the interval crossed by that pair, and zero elsewhere.
The oriented current through a radial cut is

    J(R)=sum_li j_li sigma_li(R).

If Q_j are face P1 functions and the metric is reconstructed BEFORE its
inverse clock is formed, the actual action's transport matrix is

    H_li,j=integral_anchor^target Q_j/(N_h^2 F_h) dR,
    -H^T j=-Q^T W[J/(N_h^2 F_h)].

Independent endpoint-integral and global-cut assemblies agree. This is an
action-derived current, not a fitted spatial filter.

The complete endpoint reaction flux is

    F_Gram=J_boundary
      +n[-a rho_dot+q(-D^T(rho a_w)+d_t(rho a_q))]_endpoint,
    J_boundary=n sum_l j_l,endpoint.

For the ACTUAL sampling matrix S, endpoint columns vanish. Hence rho,
rho_dot and d_t(rho a_q) vanish there and the formula reduces to

    F_Gram=J_boundary-n q[D^T(rho a_w)]_endpoint.

Canonical a_w=0, so the cut current alone suffices in that fixture.
It does not suffice generically. These simplifications depend on the
existing sampling matrix, not on a universal boundary theorem.

## 5. The temporal surface term is retained

For the linear metric-link displacement Y=H deltaV, define

    B1=sum_l z_l^2/(2h) sum_i S_li a_i Y_li.

The raw and time-integrated-by-parts potential variations obey

    delta U_raw=delta U_reduced+d_t B1.

The Lagrangian contains -U, so its surface contribution has the opposite
sign. The derivation runner compares this formula with an independent
nonlinear time-link action variation at two perturbation sizes. The actual
released I_tt is used, rather than the previous prescribed history.

## 6. An affine Ward identity explains the common offset

Set f(R)=(R-a)/(b-a), ell=b-a. Its exact Hermite coefficient vector is the
nodal values of f followed by h/ell at every slope entry. Its shift
generator is S_f=-gamma_face/ell, gamma_face=N_face^2 F_face.

In the conventions of the independently implemented Ward identity,

    r_b=f dot(D_bulk-D_Gram-W_lift-W_lapse)
          -S_f dot E_V-epsilon_free,
    epsilon_free=sum_int f q E_chi
                  +sum_(mass except a) f mu_dot G_mu.

Here W_lapse=-N f dot d_t G_N; f dot on the first line denotes contraction
with the Hermite generator coefficients. E_V is the entire weak shift
covector, with both endpoints retained. The epsilon term is independently
assembled, NOT defined as the difference needed to make this identity true.

This works because f(a)=0,f(b)=1; the scalar/mass endpoint work on the Ward
right-hand side combines into r_b. It is checked on 36 initial/mid/final
samples of both fixtures, all three grids and both branches.

The common boundary offset is therefore computable from the existing
equations and data; it is not a spare constant which can legitimately be
chosen to remove a discrepancy. The identity still does not prove that
E_V vanishes or that any term tends to zero uniformly under refinement.

At the final N64 candidate state:

| signed contribution to r_b | canonical | nonlinear |
|---|---:|---:|
| bulk affine remainder | -1.8223e-12 | -2.1577e-12 |
| negative Gram affine link remainder | -1.2614e-15 | -1.4258e-15 |
| negative shift contraction | -1.2681063e-6 | -7.1875058e-7 |
| full r_b | -1.2681081e-6 | -7.1875274e-7 |

The other terms are retained in the saved arrays. On this smooth affine
probe the offset is dominated by the unsatisfied shift contraction, not
by a missing standalone endpoint current. A different probe gives a
different decomposition; this is not a unique physical attribution.

## 7. Derived piecewise-smooth bound for the affine link error

Let gamma_h=N_h^2 F_h and P_face gamma its linear interpolant on a face
interval C=[u,v]. N_h can have an interior nodal kink in this interval.
Do not assume that gamma_h has a classical second derivative everywhere.

For a continuous function whose first derivative has bounded variation,
subtract its endpoint linear interpolant. The difference has zero endpoint
values. The Dirichlet Green kernel for the second derivative has absolute
value at most (v-u)/4. Applying it to the second-derivative measure gives

    ||gamma_h-P_face gamma||_infinity,C
       <=(v-u)/4 TV_C(gamma_h').

For this actual P1 metric the variation is bounded constructively by
integrals of |gamma_h''| on smooth subintervals plus the derivative jumps.
On each smooth subinterval,

    F'=-2mu'/R+2mu/R^2-2Lambda R/3,
    F''=4mu'/R^2-4mu/R^3-2Lambda/3,
    gamma''=2N'^2 F+4NN'F'+N^2 F''.

At an interior lapse knot, mass slope is unchanged within C and

    [gamma']=2N F [N'].

The implementation bounds every factor by endpoint extrema and positive
radial distances. It uses the conservative positive-chart lower bound

    gamma_min,C >= N_min,C^2
      [1-2|max mu|_C/u-|Lambda|v^2/3] > 0.

Failure of this sufficient condition causes rejection; it is not silently
replaced by a clipped denominator. Let B_C be the resulting interpolation
bound and gamma_lower,C the certified analytic lower expression. Then

    e_li=(H S_f)_li+(target-anchor)/ell
        =(1/ell) integral_anchor^target
                    [1-(P_face gamma)/gamma_h] dR,

    |e_li| <= (1/ell) sum_C |link intersect C| B_C/gamma_lower,C,
    |D_Gram,link[f]|=|sum_li j_li e_li|
       <=sum_li |j_li| bound(e_li).

The same bound applies to the implemented Gauss sum because oriented
weights have one sign along each link and their absolute sum is its
length. The derivation is analytic; the implementation checks use ordinary
floating point with explicit tolerances, NOT interval-certified arithmetic.

The checks cover all 18 candidate initial/mid/final states, pointwise
quadrature errors, independent integral assembly, a manufactured positive
lapse kink and rejection of a zero-lapse chart.

At the final N64 states, actual maximum |e| is 2.965e-9 and 3.230e-9;
the maximum per-link bounds are 1.155e-8 and 1.181e-8. Bounds on the
contracted affine Gram remainder are 1.841e-12 and 2.041e-12.

CONDITIONAL scaling: with a uniform positive chart, bounded stencil reach,
and TV_C(gamma')=O(h), this gives B_C=O(h^2) and individual e_li=O(h^3).
Those assumptions, bounds on the summed currents and a mesh/time-uniform
solution estimate still need proof. This does NOT prove a global O(h^3)
field-equation error. In particular the positive-chart bound does not
cover a horizon where F approaches zero.

## 8. N64 runs: unchanged equations, matched GR controls

Run both fixtures and branches for relative t=0..0.01, with 16/32/64 RK4
steps: twelve trajectories. Every stage retains kinetic/metric chart
checks. No reprojection, damping, endpoint subtraction or source refitting.
Time-refinement endpoint difference ratios are 14.10-18.17.
Fine-run free-constraint drift is at most about 1.95e-14; this checks the
implemented tangent evolution, not all unsolved gravitational equations.

For spatial comparison, use the SAME 33 coordinate times: the old N16/N32
32-step trajectories and every second sample of the N64 64-step trajectory.
The different integration steps and their separate time-refinement checks
are disclosed; this is not an exact continuum-time supremum.

| fixture / branch | max mass mismatch N32 | N64 | max weak shift N32 | N64 |
|---|---:|---:|---:|---:|
| canonical GR | 1.1205e-6 | 3.4179e-7 | 3.0181e-8 | 6.6223e-9 |
| canonical candidate | 9.2048e-7 | 3.1452e-7 | 1.5045e-7 | 1.2369e-8 |
| nonlinear GR | 1.4184e-6 | 4.1999e-7 | 5.3820e-8 | 1.0661e-8 |
| nonlinear candidate | 1.2455e-6 | 4.0374e-7 | 1.2790e-7 | 1.4269e-8 |

N64 candidate/GR weak-residual ratios are about 1.87 and 1.34, versus
about 4.99 and 2.38 at N32. Candidate maximum mass mismatch is slightly
smaller, but this is not true of every norm or of final-time mismatch.
Weak residuals are integrated covectors whose normalization changes with
the mesh; their decrease alone is not convergence of the underlying PDE.

Both endpoint offsets have now been evaluated at all common times, also
on the immutable lower-grid trajectories:

| fixture / branch | max endpoint offset N16 | N32 | N64 |
|---|---:|---:|---:|
| canonical GR | 1.6076e-5 | 1.3421e-6 | 6.2703e-7 |
| canonical candidate | 4.8162e-5 | 6.9103e-6 | 1.2681e-6 |
| nonlinear GR | 1.1978e-5 | 2.3670e-6 | 9.8102e-7 |
| nonlinear candidate | 4.2851e-5 | 5.2140e-6 | 1.1257e-6 |

The candidate offsets shrink by 5.45 and 4.63 from N32 to N64 and remain
larger than the matched GR control. Final-time offsets can change sign
and do not have uniformly monotone endpoint error ratios. Full 65-time
N64 maxima are saved too; e.g. the canonical GR offset maximum is
6.2798e-7 rather than the common-time 6.2703e-7. Neither is an exact
continuous-time bound.

## 9. Evidence and reproducibility

New implementations:

- `scripts/annular_action_boundary_current_20260909.py`
- `scripts/derive_annular_action_boundary_current_20260909.py`
- `scripts/evolve_annular_boundary_N64_20260909.py`
- `scripts/annular_boundary_ramp_bound_20260909.py`
- `scripts/finalize_annular_boundary_flux_20260909.py`

Completed result owners:

- `source-intake/navier-stokes/20260909/annular-action-boundary-current-derived/status.json`: 149/149 checks.
- `source-intake/navier-stokes/20260909/annular-boundary-N64-evolution-smoke/status.json`: 92/92 checks.
- `source-intake/navier-stokes/20260909/annular-boundary-affine-ramp-analysis/status.json`: 796/796 checks, 396 boundary-time samples and 36 affine Ward samples.
- `source-intake/navier-stokes/20260909/annular-boundary-current-final-integrity.json`: final source/output/citation and protected-path verification.

The counts concern implementation and provenance, not independent physical
confirmations. Each result owner records input/output SHA256 hashes and
an executed-script snapshot. The final seal pins a snapshot of the mutable
resume rather than pretending it is an immutable source.

All jobs use one BelowNormal single-core Python process at a time, no
subagents, with numerical-library thread counts set to one and bytecode
disabled. No existing/shared processes were stopped.

## 10. Exact next mathematical target

Do not repeat the boundary-current derivation or hunt for a tunable common
offset. The next useful step is a mesh-uniform residual/trace estimate:

1. Use the actual shift mass-pairing matrix to turn the affine shift
   contraction into a bound in the physical mass-rate mismatch norm, not
   an unnormalized count of small nodal covectors.
2. Derive bounds for the remaining bulk reconstruction products and
   establish which metric/scalar derivative norms must stay bounded.
3. Attempt to control those norms from the released action/evolution,
   with the same argument and numerical controls applied to GR.

A conditional consistency estimate must be labelled conditional until
stability and the complete coupled equations are established. Finite
sampling cannot supply a mesh/time-uniform theorem. Full DAE/Dirac closure,
global boundary compatibility, parent calibration, horizon regularity and
physical local-GR predictions remain open.
