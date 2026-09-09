# Scalar/current driving, a passivity obstruction, and the C3 raw-Volterra test

Private continuation, 2026-09-09. Previous goal turn: progress, checked against
the completed mass-bulk decomposition77/77 and its unchanged input hashes.
No subagents, no GitHub, no edits to frozen workbench or galaxy work.

This concerns the actual numerical route to a regular coupled local solution.
It is not a new MTS physical coefficient, parent closure, or black-hole proof.

## 1. What the current RHS actually contains

For the saved state e=(chi,w,h,mu,delta), keep

    q=q_y e,    f=f_y e,    j_h=D_h e_mu-g_y e,
    w_t=D_h q-d_w,
    h_t=R^-2 D_h(R^2 f)-V_y e-f_mu j_h-(f_mu,y e)J0-d_h
        +alpha S_q+h_mu S_mu+h_delta S_delta.

The new replay splits this into eleven channels, including separate
-f_mu D_h(e_mu), +f_mu g_y e, the off-shell J0 term, the nonzero parent
defect, raw scalar boundary source, interior scalar projection, and the
mass/lapse source transforms. Each product is formed before taking a parity
diagnostic. All terms and all original/hybrid states are retained.

At N512 the original h RHS has alternating RMS about
8.29e-13,1.02e-12,3.30e-12,3.23e-12 for the four case/time combinations.
The flux-derivative channel is about
9.23e-13,1.05e-12,3.51e-12,3.39e-12;
the added scalar projection is about
4.72e-13,7.04e-13,1.90e-12,7.02e-13.
The parent current defect is about1.6e-16--4.4e-16. Signed alignments are saved:
these RMS values do not add as positive percentages, and the projection can
reinforce or partially cancel the flux channel. The w RHS is D_h q; neither
freezing mass nor re-evaluating a small parent defect removes this channel.

## 2. Acoustic energy and the centered blind mode

Holding metric variations external to the scalar principal block, write
h=alpha q-Bw, s^2=B^2+alpha c=PQ. The existing derived principal matrix is

    (w,h)_t = A (w,h)_R + remaining terms,
    A=(1/alpha) [[B,1],[PQ,B]].

On the sampled c>0,alpha>0 branch,

    E_scalar=1/2 sum_i H_i R_i^2 (alpha_i q_i^2+c_i w_i^2),
    H_ac=(1/alpha)[[PQ,B],[B,1]],
    det(H_ac)=c/alpha>0,       H_ac A=A^T H_ac.

Its characteristic polynomial is lambda^2-2B lambda/alpha-c/alpha, with
speeds (B+-sqrt(PQ))/alpha. This scalar energy is not a full coupled
gravitational energy theorem; metric terms, variable coefficients, constraints
and forcing remain to be controlled. In particular c=0/horizon crossing is
NOT covered by this positive scalar-energy argument.

The centered interior derivative symbol is
i sin(theta)(4-cos(theta))/(3h). At theta=pi the acoustic principal derivative
vanishes too. Boundary closures are not blind, and variable-coefficient
products matter; this is not a claim of a global null eigenvector.

## 3. The scalar-only projection has a genuine passivity obstruction

Let n be the existing normalized left compatibility vector for the anchored
centered mass solve. Let v_i=n_i g_q,i, with both endpoint entries set to zero,
and W_i=H_i R_i^2 alpha_i. Define

    d=v^T W^-1 v>0,
    r=n^T(g_q S_q,raw+g_delta S_delta,raw).

Fixed endpoint scalar sources, fixed lapse source and zero outer mass source
require every admissible interior scalar repair c_q to satisfy

    v^T c_q=-r.

The current implementation uses the minimum-W-norm solution
c_q=-r W^-1 v/d. Minimum source norm does NOT imply negative work on the state:

    Delta E'_scalar=q^T W c_q=-r q^T v/d.

More strongly, choose endpoint q=0 and interior q=-r W^-1 v.
Then for EVERY compatible repair, not only the minimum-norm one,

    q^T W c_q=(-r)v^T c_q=r^2>0.

A nonzero endpoint w can supply r while endpoint q remains zero, so the
usual negative scalar SAT boundary work is zero in this construction. It
cannot absorb that positive interior work. This proves a source/scalar-energy
passivity obstruction on the unrestricted discrete current state space.

Important limits of this result:
- r=0 gives no such obstruction; d=0 is a separate feasibility case.
- It does not prove full coupled instability or rule out a different norm,
  a higher-regularity estimate, or a constraint-restricted energy argument.
- The numerical directions enforce w=D_h chi, but do NOT enforce homogeneous
  mass constraint. Their nonzero constraint is explicitly saved.
- This is not a counterexample to MTS, GR, or any physical continuum solution.
- The current-variable mass source does not evade the scalar-work calculation:
  q_y S_current=S_q, because its induced h_mu S_mu/h_delta S_delta terms cancel
  when converting back to the coordinate velocity source. This is replayed.

Twelve normalized directions on the actual two backgrounds and three meshes
give positive scalar source work. Canonical early work/E is
9.1185,12.9484,18.3491 at N128,256,512; nonlinear early is
8.9021,12.6410,17.9133. The late values also grow by roughly sqrt(2) per doubling.
Those finite samples alone are NOT an asymptotic unboundedness theorem.

On the two-dimensional span of a unit kinetic direction and the normalized
boundary-gradient bump, write r=r0*b and q=a W^-1 v/sqrt(d).
The source work is -k*a*b, k=r0/sqrt(d), while E=(a^2+b^2)/2.
Thus |work|<=|k|E, sharply. A source estimate exists at each fixed mesh, but
these data do not establish a mesh-independent coefficient.

## 4. Why this suggests a specific replacement, not another projection tweak

With N+1 nodal mass values and the outer value fixed, there are N free mass
values. Requiring N+1 centered derivative equations imposes at least one left
compatibility condition on arbitrary source samples. The implemented n makes
that extra discrete condition explicit. Its use is legitimate as a chosen
discretization, but the condition is not an additional continuum law.

The continuum terminal-value equation

    u_R=g_mu u+g_q S_q+g_delta S_delta,       u(R_outer)=0

has a unique Volterra solution for arbitrary bounded forcing on a finite
annulus. It does not demand that the scalar source be globally projected.
The cell-integral method has N cell equations plus the one outer value.
Therefore retaining the centered solver's compatibility projection after
switching to Volterra is unnecessary.

This does NOT permit ignoring conservation or nodal accuracy. For the
unprojected cell method:
- keep the raw physical scalar/lapse boundary sources unchanged;
- retain and bound every collocated source residual row using the already
  derived Volterra bound, with the actual unprojected forcing;
- keep all field, boundary, mass-constraint, curvature and strong-norm gates;
- distinguish exact cell integration of the declared piecewise coefficients
  from a continuum error certificate;
- derive and validate the actual raw-source time derivatives before curvature.

Removing the unnecessary projection eliminates its extra scalar work.
The raw characteristic boundary work has its previous derived sign, but that
alone still is NOT a full coupled energy estimate.

## 5. Matched experiment and provenance

The earlier raw-source Volterra run used OLD initial data and failed141/145.
It is preserved; it does not decide the SAME C3-data experiment.

The new run uses the unchanged existing runner:
scripts/run_annular_coupled_current_correction_20260909.py
with source-completion=volterra, initial-kind=third_corner, max-grid=512,
tag=annular-coupled-current-third-corner-raw-volterra.
No physical coefficient or acceptance tolerance changes.

The actual raw-source Taylor engine bypasses the scalar projection entirely.
It differentiates the same thirteen-term small-moment integrator as the
ordinary source implementation. Preflight on twelve matched saved states
passes175/175 at09:11:39 UTC, including independent finite-time differences.
This is not yet a field result.

Owners under source-intake/navier-stokes/20260909/:
- annular-current-driving-and-passivity-obstruction/status.json (205/205).
- annular-current-driving-and-passivity-qualified/status.json (232/232).
- annular-raw-volterra-C3-time-jets-preflight/status.json (175/175).
- annular-coupled-current-third-corner-raw-volterra/status.json (evolution).

The qualified derivation replaces a redundant characteristic-polynomial
check with the explicit formula and its actual-coefficient replay, and adds
the sharp two-direction energy algebra. The initial diagnostic is immutable.
Analytic proof is supplied above; green software checks alone are not proof.

Scripts:
- scripts/derive_annular_current_driving_and_passivity_20260909.py.
- scripts/derive_annular_current_driving_and_passivity_qualified_20260909.py.
- scripts/annular_raw_volterra_time_jets_20260909.py.
- scripts/derive_annular_raw_volterra_C3_time_jets_20260909.py.

Previous context:
DERIVATION-20260909-projected-Volterra-mass-only-experiment.md and
DERIVATION-20260909-compatible-boundary-energy-and-Noether-coupling.md.

## 6. Completed raw-source C3 experiment: not an accepted replacement

The field experiment completed FAILED145/147 at09:19:04 UTC. The two failures
are again the late nonlinear mass constraint at full and half time steps:
3.19837e-12 / 4.86928e-11, about6.57%, above the unchanged5%+1e-16-floor gate.
All field mesh/time refinements pass. The earlier projected-mass-only failure
and the old-data raw-Volterra failure remain unchanged, with no pass promotion.

Actual raw-source trajectory time jets pass187/187; normal reconstruction
software526/526; the matched comparison255/255. The latter explicitly retains
the failed field, curvature and strong-refinement flags. Its additional cell
check verifies the actual SOURCE recurrence, including zero outer source:
it does not assert that the evolved mass field satisfies every cell constraint.
Fine source-cell residuals are zero to roughly2.3e-28 in floating arithmetic.

| Case/time | Raw-source nodal Z stencil difference | K1 difference | Raw/original mass H4 trace floor |
|---|---:|---:|---:|
| canonical .1 | 15.79% | .0463% | .6526 |
| canonical .3 | 22.47% | .1100% | 2.0014 |
| nonlinear .1 | 25.14% | .2323% | .8977 |
| nonlinear .3 | 23.71% | .1389% | 4.7688 |

All four nodal Z gates still fail; all sampled subcell Z/K1 gates pass.
That is not a continuum or full reconstruction pass. Poly7 strong-derivative
coarse/fine difference ratios are .154,.383,.315,.402, so the strong differences
still increase. The mass-source parity is now about1e-33--1e-28, while bulk
mass parity remains1e-14--1e-13. Merely removing projection is insufficient:
the bulk scalar/current discretization still needs grid-scale control.

New owners under source-intake/navier-stokes/20260909/:
- annular-raw-volterra-C3-time-jets-trajectory/status.json (187/187).
- annular-raw-volterra-C3-normal-reconstruction/status.json (526/526).
- annular-raw-volterra-C3-matched-comparison/status.json (255/255).

## 7. A constructive next operator: derived restoring force, not fitted damping

The existing compatible SBP operator provides a positive remainder, not just
a better stencil. Set a=R^2 c>0 and H=H_h. With the existing coefficient-fixed
Gram factor W_a and unscaled third-difference matrix Delta3, define

    R_a=Delta3^T W_a Delta3/h >=0,
    M_a=D_h^T H diag(a)D_h+R_a,
    D2_a=H^-1[-M_a+B_boundary diag(a)S_h].

This is the previously derived operator, with no new free strength parameter.
Its use with the CURRENT source completion is new here. Preserve the actual
integrability remainder I=w-D_h chi; do not silently replace analytic initial
w by D_h chi. In the present kinematically compatible evolution I is fixed.

Replace the c*w flux derivative by D2_a chi+D_h(a I). Simultaneously use
S_h chi+I at the scalar boundary instead of D_h chi+I. The combined bulk and
SAT difference simplifies on EVERY row, including endpoints, to

    Delta S_q = - (H R^2 alpha)^-1 R_a chi.

Indeed D2_a-D_h(a D_h)=-H^-1 R_a+H^-1 B_boundary a(S_h-D_h), and the changed
SAT contributes the negative of that boundary term. I cancels from the
numerical difference; it has not been deleted from the state or energy.

Add the POSITIVE potential energy E_R=chi^T R_a chi/2. Then the restoring
source's scalar work is -q^T R_a chi, exactly canceling the q^T R_a chi part
of E_R'. For time-dependent coefficients and chi_t=q-d_chi, retain

    remaining E_R' = chi^T R_a,t chi/2 - d_chi^T R_a chi,
    |chi^T R_a,t chi/2| <= ||a_t/a||infinity E_R.

The last bound follows termwise from the positive, linearly interpolated Gram
decomposition, not from ignoring time variation. Other existing bulk, metric,
boundary and parent-defect terms remain in the coupled energy budget. This is
an augmented scalar-energy identity, NOT a full coupled stability theorem.

For constant coefficients in the interior, set x=sin(theta/2)^2. In units h^-2,

    k_D^2=4x(1-x)(3+2x)^2/9,
    k_compatible^2=4x(1+x/3),
    k_remainder^2=16x^3(2+x)/9,
    k_compatible^2=k_D^2+k_remainder^2.

At Nyquist, k_D^2=0 but k_compatible^2=16/3. The new positive energy therefore
controls a mode missed by the centered current gradient. The smooth interior
correction is fourth-order (x^3/h^2=O(h^4)); boundary consistency uses the
already derived compatible closures, not an interior Fourier argument alone.

The ENTIRE raw numerical source, SAT plus this restoring term, must then be
completed with the unprojected Volterra mass source and transformed back into
h, including h_mu S_mu+h_delta S_delta. Completing only the SAT would break
the source coupling again. Every nonzero nodal residual and its bound remains.

This operator has now been constructed and statically checked on twelve saved
C3 states:84/84 at09:24:14 UTC. Checks include the full bulk-plus-SAT identity,
positive Gram energy, exact restoring-work cancellation, and the all-row
Noether residual bound for the whole changed source. Some static source bounds
are sizeable, so bounded does not imply that the future mass-constraint gate
will pass. No new evolved result is claimed from these static calculations.

Owner: source-intake/navier-stokes/20260909/annular-compatible-current-restoring-source-derived/status.json.
Script: scripts/derive_annular_compatible_current_restoring_source_20260909.py.
Reconstruction/comparison scripts:
scripts/derive_annular_raw_volterra_C3_normal_reconstruction_20260909.py and
scripts/compare_annular_raw_volterra_C3_20260909.py.

## 8. Next execution target and remaining limits

Implement the derived coefficient-fixed restoring term in the actual current
evolution, with projection-free completion of ALL numerical sources. First
derive its true time jets and explicit stability/time-step control, then run
a short matched C3 smoke before any larger run. Keep the original baseline,
both failed Volterra alternatives, physical boundary data and ALL old gates.

Time-jet implementation warning: W_a is LINEAR in a on the positive leading
coefficient branch, but its higher time coefficients may be signed. Differentiate
the positive Gram decomposition using the fixed edge orientations from the
leading coefficient. Do NOT feed signed Taylor coefficients to gram_parts,
whose positivity guard is intentional, or differentiate changing abs/sign
branches as though they were the same operator. Retain I=w-D_h chi and all
weight-time and nonzero-defect terms.

No first-u, physical source calibration, local-GR, horizon, Maxwell/EM or broad
unification promotion follows yet. This step rules out two inadequate repairs
and supplies a derived, energy-controlled candidate for the remaining bulk
problem. All numerical percentages are normalized annular fixture diagnostics,
not observational errors or calibrated physical predictions.

Final integrity check09:28:27 UTC: eight owners,273 unique input hashes and
116 output hashes verified; seven new scripts compile, no bytecode cache.
The failed evolution retains its failed status and no COMPLETE marker.
All calculations from this continuation have exited. No other task, shared
helper or Desktop Commander process was stopped; no GitHub action occurred.
