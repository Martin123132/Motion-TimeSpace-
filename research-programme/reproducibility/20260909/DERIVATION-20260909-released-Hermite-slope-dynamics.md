# Released Hermite slope dynamics from the same action

2026-09-09. Private local work. No GitHub action. This removes one prescribed
numerical history; it does not establish the full coupled field theory,
local-GR recovery, a black-hole theorem or an empirical prediction.

## 1. Concrete outcome

The interpolation slopes now have an explicit canonical momentum and force
derived from the existing action. Their Euler equation is actually evolved,
not canceled by an added force or replaced by a prescribed acceleration.
The previous lifting residual falls from about 1e-6 on the prescribed-history
tests to numerical roundoff on the released branch, in BOTH GR and MTS.

The enlarged kinetic matrix is positive on the six N16/N32/N64 fixture
patches. Twelve initial constraint solves succeed; the GR roots are preserved,
and the candidate takes one Newton step. Twenty-four short released-slope
trajectories finish. All shift equations remain recorded and nonzero.

At N32 the candidate's maximum mass-rate mismatch over the short run falls
by factors about 4.55 and 3.04 relative to its own previous prescribed-history
run at the SAME 16 time steps. GR improves too. Different residual norms do
not all favor MTS; this is not a physical win against GR.

## 2. Coordinates and what is being released

Use the same lifted Hermite scalar and the same finite metric-link action:

    chi_h = H_chi chi + H_I I,
    q_h   = H_chi q   + H_I I_t,
    w_h   = G_chi chi + G_I I,
    w_node = D chi + I.

I is a scalar interpolation-slope coordinate. It is not a newly postulated
fundamental matter field. The previous algorithm kept it on an externally
supplied local Taylor history. The new algorithm varies and evolves it.
This changes the numerical phase space, so old and new runs are not silently
declared identical discretizations.

For conditioning, define

    s=h I,   v_s=s_dot=h I_t,   p_s=Pi_I/h.

The transformation is canonical: Pi_I dI=p_s ds. The natural unknown velocity
pair is (q,v_s), both in scalar/time units. No physical scale or coupling is
introduced by this change of numerical coordinates.

At the endpoint traces H_I=0, while H_chi selects the endpoint scalar values.
Thus independent slope variations preserve the existing Dirichlet scalar
VALUE conditions. They do not require prescribing additional endpoint slope
values. This finite scalar trace result is not complete gravitational or
characteristic boundary compatibility.

## 3. The slope equation is derived, not chosen

At the zero-shift slice, after variation of the shift-unfixed action, write

    F_h=1-2 mu_h/R-Lambda R^2/3,  L=F_h^(-1/2),
    X=-q_h^2/N_h^2+F_h w_h^2,
    K=-X/2-m_chi^2 chi_h^2/2+b2 X^2+b3 X^3,
    P=1-4 b2 X-6 b3 X^2,  P_X=-4 b2-12 b3 X.

With W the shared positive quadrature weights and rho_node=S^T[(Tchi)^2]/(2h),
differentiate the SAME scalar and Gram terms, L_total=L_bulk-U_Gram:

    p_s = (H_I/h)^T W [R^2 L P q_h/N_h],

    p_s_dot = (H_I/h)^T W [-R^2 N_h L m_chi^2 chi_h]
                +(G_I/h)^T W [-R^2 N_h L P F_h w_h]
                -(rho_node/h) a_w.

The Gram contribution to p_s is zero at this slice because its coefficient
samples q at scalar nodes and H_I vanishes there. Its slope force is NOT
zero in the general nonlinear fixture: a depends on w_node=Dchi+s/h.
This last derivative must be retained.

The code independently differentiates the original ADM quadrature action
with respect to s, checks its full velocity gradient/Hessian, and checks
d_t p_s against the written force using the evolved metric/scalar jets.
The lifting Euler covector in the separately implemented Ward identity
agrees with h(p_s_force-d_t p_s). This avoids declaring success simply
because a new variable was named "slope force".

## 4. Enlarged Legendre map and a sufficient positivity condition

Set B=[H_chi,H_I/h]. The exact velocity Hessian at this slice is

    M0 = B^T W diag[R^2 L/N_h (P-2 P_X q_h^2/N_h^2)] B,

    M = M0 - [[diag(rho_node a_qq), 0], [0, 0]].

There are nonzero q--v_s cross entries in M0. Positivity of the previously
tested q-only submatrix would NOT prove positivity of this enlarged map.

If the displayed quadrature coefficient is positive and B has full column
rank, M0 is positive definite. Here the reconstructed scalar is cubic on
each scalar cell. Four distinct Gauss samples on each half-cell suffice:
if B times a coefficient vector vanishes at all samples, each cubic is
identically zero. Its nodal values and slopes then vanish, so the coefficient
vector is zero. The positive quadrature gives the stated injectivity result.

For the Gram correction C, a sufficient finite-state condition is

    ||L0^-1 C L0^-T||_2 < 1,   M0=L0 L0^T.

This condition is actually tested, not assumed from a small diagonal entry.
Canonical C=0 identically. Candidate nonlinear relative operator corrections
are 3.884e-8, 2.211e-9 and 1.556e-10 at N16/32/64. The lowest enlarged kinetic
eigenvalues at the seeds are approximately:

| fixture | N16 | N32 | N64 |
|---|---:|---:|---:|
| canonical | 0.00130639 | 0.000652608 | 0.000326158 |
| nonlinear | 0.00132972 | 0.000664247 | 0.000331970 |

These eigenvalues depend on the chosen scaled nodal basis. They are not
particle masses or grid-independent lower bounds. Positivity here does not
prove a complete Dirac analysis or global absence of extra dynamical modes.

## 5. Consistent initial canonical data

The enlarged Routh functional is

    R_release=L_bulk-U_Gram-pi_chi^T q-p_s^T v_s-E_b mu_outer/kappa.

Unknowns are y=(mu_faces,N_nodes,q_nodes,v_s,nodes). All slope momentum rows
are included. Fixed entries remain ONLY inner mass and the two scalar value
endpoint velocities. All lapse rows and all slope velocities are free.

Both branches share the original scalar profile, I, canonical pi_chi,
inner mass, scalar endpoint data and outer-clock history. The additional
shared p_s is computed once from the old GR corrected root and its supplied
I_t, using the momentum formula above. This is disclosed numerical initial
data, not a new parent-derived coupling or a fit to the shift residual.

The GR root then remains unchanged. The candidate solves for the same p_s,
so its corrected q and I_t may differ slightly; it takes one Newton step on
each of the six patches. Fixing both a canonical momentum and its velocity
by hand would instead overconstrain the new Legendre problem.

The initial root family is differentiated with the actual new forces.
Independent neighboring nonlinear solves at two time increments verify the
tangent on N16. Holding the slope history fixed recovers the old restricted
action, gradient and Hessian, up to numerical arithmetic.

The derived I_tt is materially different from the former prescribed I_tt:
the maximum differences are about 2.51-2.62 for GR and 6.64-7.70 for the
candidate in the existing fixture normalization. It is not defensible to
continue using the old acceleration while claiming to solve this equation.

## 6. Actual released-slope evolution

The state is (chi,s,pi_chi,p_s,y). Integrate

    chi_dot=q,  s_dot=v_s,
    pi_chi_dot=(L_chi)_interior,  pi_chi_dot_endpoints=0,
    p_s_dot=the derived full slope force,
    y_dot_free from differentiated free Routh equations,
    mu_dot_inner from the complete existing shift mass-flow solve,
    q_dot_endpoints from the same declared scalar boundary history.

I, I_t and I_tt are no longer external source histories. The two scalar
value histories and E_b(t) remain prescribed, identically for both branches.
No algebraic root reprojection, constraint damping, mass-flux adjustment or
bad-row deletion is used. All face shift residuals are saved.

Run relative t=0..0.01 on N16/N32, both fixtures and both branches, with
8/16/32 RK4 steps: 24 trajectories. This is the fixture's coordinate-time
normalization, not an asserted physical time in seconds. The enlarged
kinetic/metric chart is checked at every RK stage. All runs finish.

Time-refinement endpoint differences improve by factors 15.02-18.07.
The largest fine-step constraint change is about 1.43e-14. Initial root
error is retained separately. The unscaled I Euler residual stays below
1.77e-19 on the fine runs. Since constraint rates and slope equations are
part of the integrated ODE, these small numbers validate the implementation;
they do not independently establish every gravitational equation.

## 7. Compare both norms and both controls

Maximum mass-rate mismatch over the complete short run, 32 time steps:

| fixture | grid | released GR | released candidate |
|---|---:|---:|---:|
| canonical | 16 | 2.496e-6 | 6.200e-6 |
| canonical | 32 | 1.121e-6 | 9.205e-7 |
| nonlinear | 16 | 3.493e-6 | 5.606e-6 |
| nonlinear | 32 | 1.418e-6 | 1.246e-6 |

At N32, comparing new and old candidate runs at the SAME 16 time steps,
the maximum mass-rate mismatch falls from 4.179e-6 to 9.177e-7 (canonical)
and from 3.787e-6 to 1.245e-6 (nonlinear). GR also improves substantially.
The old prescribed-slope branch remains intact as a separate comparator.

Do not cherry-pick this norm. Maximum WEAK shift residuals at 32 time steps:

| fixture | grid | released GR | released candidate |
|---|---:|---:|---:|
| canonical | 16 | 7.183e-7 | 1.916e-6 |
| canonical | 32 | 3.018e-8 | 1.504e-7 |
| nonlinear | 16 | 6.098e-7 | 1.804e-6 |
| nonlinear | 32 | 5.382e-8 | 1.279e-7 |

The candidate's N32 weak residual is still roughly 5.0 or 2.4 times GR's,
despite the smaller maximum mass-rate norm. The two norms weight the
spatial pattern differently through the mass-flow pairing. The candidate
does not outperform GR across these numerical diagnostics.

Only two spatial grids have been evolved on this released branch. All
residuals remain numerical, not observational error bars. The present
calculation is a differentiated-constraint branch, NOT full coupled DAE
closure, a long-time stability theorem or an exact local-GR solution.

## 8. What remains after solving the slope equation

The full Ward identity is checked at initial, midpoint and final times,
with a constructive Hermite right inverse covering EVERY face. Twenty-four
all-face reconstructions agree with the saved shift covectors to <=2.26e-19.
No singular-value truncation or least-squares projection is used.

The former lifting-work term is now roundoff-sized. For the final canonical
N32 candidate state, the right-inverse decomposition gives maximum norms:

    bulk reconstruction remainder             3.379e-8
    Gram link remainder                       2.636e-8
    Gram coefficient remainder                1.730e-16
    lifting work                              6.586e-21
    combined scalar/mass boundary work         3.826e-8
    final weak shift residual                 6.331e-8

The analogous GR values are bulk 1.333e-8, combined boundary 1.756e-8, and
final shift 3.018e-8, with no Gram terms. For nonlinear N32 the candidate
has bulk 3.240e-8, Gram link 2.769e-8, combined boundary 2.604e-8 and final
shift 5.250e-8. The large individual scalar and mass boundary vectors are
combined WITH THEIR SIGNS before measuring their norm.

These are basis-dependent decompositions, not uniquely identifiable
physical sources. Norms cannot be added as if all contributions aligned.
They do show that another search for a missing I_tt coefficient is now the
wrong target: that equation has been constructed and solved.

## 9. Next constructive target: boundary flux plus the remaining link defect

The next derivation should obtain the scalar/gravity boundary work from the
same finite action and test its compatibility with the declared clock and
scalar-value boundary data. Do not tune those data to cancel a measured E_V.

There is a useful continuum GR normalization control already implied by
the shift variation of this action. At V=0, for positive-coordinate-radial
scalar energy flux (not outward normal flux at both ends), define

    F_scalar = q * (partial L_matter / partial w)
             = -R^2 N sqrt(F) P q w.

The GR shift equation gives

    mu_t = kappa R^2 F P q w
         = -kappa F_scalar/(N L).

Consequently, where the natural outer clock trace is E_b=N L,

    E_b mu_t/kappa + F_scalar = 0.

This is a continuum normalization identity under its stated assumptions,
not permission to impose it as an extra finite-grid equation. The candidate
needs its OWN Gram-corrected boundary current and time-boundary work derived
from the metric-link action. The generic nonzero-metric-work energy identity
must be retained; no conserved scalar energy is assumed on a time-dependent
background. The inner endpoint has the opposite outward-normal convention.

After deriving that boundary/current relation, use matched GR/candidate
N64 spatial controls on the same short interval to distinguish convergent
bulk/link reconstruction error from incompatible boundary data. Do not
replace this with another long prescribed-history run. The global Dirac,
parent-source calibration and physical local-GR claims remain separate gates.

## 10. Sources and reproducibility

Paths below are relative to post-checkpoint-work. Old source files, frozen
workbench and galaxy work are unchanged. One BelowNormal single-core Python
job at a time; no subagents or shared-process shutdowns. All jobs finish.

- `scripts/annular_released_hermite_action_20260909.py`.
- `scripts/derive_annular_released_hermite_20260909.py`.
- `scripts/evolve_annular_released_hermite_20260909.py`.
- `scripts/finalize_annular_released_hermite_20260909.py`.
- `source-intake/navier-stokes/20260909/annular-released-Hermite-initial-derived/status.json`.
- `source-intake/navier-stokes/20260909/annular-released-Hermite-evolution-smoke/status.json`.
- `source-intake/navier-stokes/20260909/annular-released-Hermite-all-face-analysis.json`.
- `source-intake/navier-stokes/20260909/annular-released-Hermite-final-integrity.json`.
- `DERIVATION-20260909-metric-link-quadratic-action-and-short-evolution.md`.

Initial derivation/root checks finish 192/192; short evolution checks finish
144/144. These are implementation and finite-equation checks, not 336
independent physical tests. The final record verifies source/output hashes,
compilation without bytecode, cited local paths and a protected-workbench
mtime scan since turn start; the resume is pinned as an immutable snapshot.
