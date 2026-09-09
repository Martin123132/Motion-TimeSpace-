# Coupled current to curvature: source-aware time jets and an explicit error map

Private continuation, 9 September 2026. No public-repository action.
All numbers below use the existing normalized annular fixtures, not calibrated
SI predictions. Ordinary linear correction only; no physical first-u claim.

## Result in plain language

The passing ordinary evolution now has a reproducible transfer to the actual
geometric curvature and response quantities. Its time derivatives replay the
saved evolution, including numerical sources, and independently check out.
The curvature formulas and their nonlinear remainder machinery also check out.
However, all four pre-existing 10% curvature sensitivity gates still fail.

This is not a new failure of the underlying equations, nor a local-GR pass.
It is a failure to resolve the small curvature CORRECTION consistently with
the two tested spatial reconstructions. The largest discrepancy is at a
boundary. An explicit linear error map identifies which derivatives cause it:
mass second radial derivatives dominate Z; scalar second radial derivatives
dominate K1 in all four cases. Third metric derivatives remain mathematically
required, but they are not the largest measured K1 discrepancy here.

Time-step halving, cache-side choice and degree64/80 initial mass reconstruction
changes are much smaller. Spending more time on the same temporal evolution
is therefore not the next useful intervention.

## Executed evidence

Owners below are under `source-intake/navier-stokes/20260909/`.

| Owner | Completion UTC | Software checks | Curvature claim |
|---|---|---|---|
| `annular-coupled-current-time-jets` | 07:40:32 | 168/168 | None |
| `annular-coupled-current-curvature-transfer` | 07:43:39 | 301/301 | All four sensitivity gates fail |
| `annular-coupled-curvature-error-decomposition` | 07:47:32 | 48/48 | None; error-map validation only |

Each has `status.json`, an executed-script snapshot, hashed inputs and hashed
array outputs, and a terminal `COMPLETE` marker. This marker means its declared
software workflow finished, NOT a physics gate passed. The curvature owner
separately records `all_curvature_sensitivity_gates_passed=false`; all owners
record `valid_for_physics_claim=false`.

The source is the unmodified
`annular-coupled-current-analytic-third-corner` evolution, complete129/129.
Its ordinary scalar/current/mass/lapse equations, original projected source,
zero filter, background defects, initial data and accuracy gates are retained.
Use N128/256/512 at T=.1,.3, with dt2 at the finest grid. None of the old
failed scalar/coordinate, second-corner or source-variant runs was overwritten.

## 1. Time differentiation of the actual semidiscrete operator

Current state ordering is e=(chi,w,h,mu,delta). Write

    e_t = L_h(t)e - d_h(t) + S_h(t,e).

This is the saved coupled current operator, not the old scalar-only coordinate
operator. Its h equation retains both terms

    -f_mu (D_h e_mu - G_y e) - (f_mu,y e) J_background.

The background defect d_h comes from the independent exact-jet residual used
by the evolution. It is not obtained by subtracting nearly equal evolved
quantities, and is not set to zero.

For normalized Taylor coefficients e(t+s)=sum e[k] s^k, use

    (k+1)e[k+1] = coefficient_k(L_h e - d_h + S_h), k=0,1,2.

All coefficient products, quotients, the acoustic square root, boundary SAT
terms and the source projection are differentiated in the same Taylor algebra.
The result is the true derivative array (e[0],e[1],2e[2],6e[3]). The stored
source array instead contains normalized coefficients through degree2.

For the anchored source solve A(t)x(t)=b(t), with A=D_h-G_mu and outer row
replaced by the mass anchor, differentiation is implemented by

    A[0] x[k] = b[k] + sum_{j=1}^k diag(G_mu[j]) x[k-j].

The diagonal contribution is zero at the replaced anchor row. The transpose
solve obeys the same recurrence because this time-dependent correction is
diagonal. No inverse differentiation by noisy finite differences is needed.

The projector's optional normalization n/max|n| is omitted in this derivative
implementation, without changing its mathematics: mismatch and covector each
scale by the same nonzero c(t), while the denominator scales by c(t)^2.
Their ratio-product is invariant. Avoiding max removes an artificial
nondifferentiability. Saved normalized and unnormalized sources replay within
the declared tolerances. A singular restricted denominator raises an error;
the code does not manufacture a source solution at that singularity.

The six-point coefficient interpolant uses the EXACT original
`linspace(0,.3,193)` cache abscissae. Substituting nominal nodes/640 previously
changed tiny background residuals through floating evaluation; do not do that.
Interpolate differences from the first sample to suppress constant cancellation.
Left and right cache windows at T=.1 are compared rather than assumed smooth.

Checks include all12 saved RHS/source/defect replays; unchanged endpoint scalar,
lapse and outer mass sources; integrability recurrence; Noether source identity
at Taylor degrees0,1,2; and independent one-sided finite-time differentiation
at steps .00025 and .000125. These are local semidiscrete checks, not a bound
on the derivatives of an unknown continuum solution over the whole time strip.

## 2. Mixed jets and physical-coordinate conversion

For the time-independent initial lift e0(R), reconstruct spatial derivatives as

    partial_R^b e(t,R) = partial_R^b e0(R)
                         + D_poly^b(e(t,R)-e0(R)).

For positive time order, differentiate the full time derivative instead. Use
the actual current components chi,mu,delta, not a manufactured q third jet.
Initial mass derivatives here are those of the declared degree64 global
Chebyshev lift; they are NOT replaced by an exact-zero mass constraint.
Degree80 sensitivity is reported separately.

With t=v-sigma(r-4), R=r, sigma=.05,

    partial_v = partial_t,
    partial_r|v = partial_R - sigma partial_t.

Thus a physical normalized coefficient is

    [partial_v^a partial_r^b e]/(a!b!)
      = sum_{j=0}^b binomial(b,j)(-sigma)^j
        partial_t^(a+j) partial_R^(b-j)e / (a!b!).

All ten mixed orders through total degree3 are independently checked against
a symbolic polynomial transformation. Both poly7 and poly9 reconstructions
retain every endpoint. The existing geometry engine is source-hash checked;
its prior independent algebra controls remain applicable. Off-shell identities,
complex-step first variations, positive quadratic majorants, residual triangle
bounds and finest-grid four/eight-node Hessian integrals are rechecked here.
Quadratic majorants are conditional on the supplied jets, not interval-certified
enclosures of an unknown solution. Small quadratic remainders do not rescue an
unresolved linear spatial derivative.

## 3. Curvature sensitivity: unchanged gates

The gate is |delta Q_poly9-delta Q_poly7|_infinity <= .1 times the larger
correction norm +1e-25, for BOTH Q=Z,K1. It is not relative to total/background
curvature. All endpoints are included.

| Fixture | T | Z relative difference | K1 relative difference | Result |
|---|---:|---:|---:|---|
| canonical | .1 | 85.710% | 13.905% | fail |
| canonical | .3 | 70.616% | 75.764% | fail |
| nonlinear_modulated | .1 | 75.369% | 79.065% | fail |
| nonlinear_modulated | .3 | 73.103% | 64.416% | fail |

Z differences are 1.237e-10,3.852e-10,1.260e-10,2.411e-9 respectively, all
peaking at R=4. K1 differences are 1.810e-11,3.790e-10,2.757e-9,1.596e-9;
the second peaks at R=8, the others at R=4. The interior looks substantially
better but has NOT been used to hide the endpoints or turn a fail into a pass.

For context, background |Z| is approximately .1875 and background |K1| is
6.5e-5 to1.28e-4. Large percentages of the small correction are not a
demonstration that the total geometry blows up. Conversely, a small absolute
fixture difference is not an experimentally calibrated acceptance bound.
The relative correction gate remains failed; no changed denominator or relaxed
threshold is introduced.

## 4. Derived explicit linear curvature map

All quantities in this section use physical (v,r) derivatives. Hold r,Lambda,
kappa fixed. Let the errors be (eta,m,l) in (chi,mu,delta), and put

    E=exp(delta), F=1-2mu/r-Lambda r^2/3, f=delta F=-2m/r,
    X=2E^-1 chi_v chi_r + F chi_r^2,
    B=2F/r-F_r-2F delta_r, M=-2r^2 XZ/3.

Direct differentiation of the geometric expression gives

    delta Z = -f_rr + (2/r-3delta_r)f_r
        + [-2(delta_rr+delta_r^2)+2delta_r/r-2/r^2]f
        + (-3F_r-4F delta_r+2F/r)l_r
        -2F l_rr -2E^-1 l_vr +2E^-1 delta_vr l.

There is no scalar dependence in this geometric variation. The scalar enters
the response through

    delta X = 2E^-1(chi_r eta_v+chi_v eta_r-chi_v chi_r l)
              + f chi_r^2 + 2F chi_r eta_r,
    delta M = -2r^2(X delta Z+Z delta X)/3,
    delta B = 2f/r-f_r-2f delta_r-2F l_r,
    delta K1 = kappa[2F(delta M)_r+2E^-1(delta M)_v+B delta M
                     +2f M_r-2E^-1 l M_v+(delta B)M].

These independently implemented first-variation formulas reproduce the Taylor
geometry engine for Z,X,M1,K1. They establish explicitly that Z needs second
metric jets only, and K1 needs third metric but at most second scalar jets.
The derivative order is a structural statement, not a numerical convergence
claim.

After the coordinate change, collect the30 ordinary jets
j=(partial_t^a partial_R^b eta,m,l), a+b<=3. At a fixed background,

    delta Q = sum_j L_Qj j, Q=Z,K1.

The saved kernels L_Qj are obtained by the explicit formulas, applying each
unit jet in turn. They reproduce the complete poly9-minus-poly7 difference:

    Delta(delta Q) = sum_j L_Qj Delta j,
    |Delta(delta Q)| <= sum_j |L_Qj Delta j|.

All-row reconstruction and triangle-enclosure checks pass. The same formula
would convert separately justified error bounds |j-j_true|<=rho_j into
|delta Q-delta Q_true|<=sum_j |L_Qj|rho_j, with coefficient/roundoff enclosures
also needed for a rigorous numerical certificate. No such unknown-solution
rho_j is inferred merely from agreement of two stencils.

### Dominant measured channels

| Fixture,T | largest Z channel: m_RR contribution | largest K1 channel: eta_RR contribution |
|---|---:|---:|
| canonical,.1 | 1.313e-10 | 9.222e-11 |
| canonical,.3 | 3.135e-10 | 3.712e-10 |
| nonlinear,.1 | 9.668e-11 | 3.116e-9 |
| nonlinear,.3 | 2.024e-9 | 1.257e-9 |

These are maxima of individual absolute contributions, not necessarily the
net difference; cancellation is substantial in canonical early-time K1.
The saved signed channels and conservative triangle prevent that cancellation
from being misreported as an independent bound on each derivative.

Time-halving changes Z by at most9.82e-15 and K1 by at most1.85e-16 across
these fixtures. Cache-side changes at T=.1 are below1.1e-18. Degree64/80
initial-lift changes are below6.25e-16 in Z and2.28e-17 in K1. None approaches
the observed spatial-stencil discrepancies. This localizes the current
problem; it does not isolate every source of boundary truncation error.

## 5. Next constructive intervention, not another blind long run

Build a C3 reconstruction using the evolved current variables and retained
constraints, instead of differentiating small nodal mass/scalar corrections
twice without their first-order structure. In particular, the exact saved
semidiscrete identities expose

    D_h(e_chi-e_chi_initial) = e_w-e_w_initial,
    D_h e_mu = G_y e + delta J_h.

The initial integrability offset and NONZERO delta J_h must be retained.
They provide derivative data for a candidate Hermite reconstruction; they
do not license setting a continuum residual to zero. A candidate must own
its reconstruction defect, be compatible across cells, and be compared with
an independent reconstruction/higher-boundary-order method on the SAME data.
Use the explicit error kernels to prioritize m_RR and eta_RR, and apply the
same all-row Z/K1 gates. A mass-only repair cannot address the dominant K1
channel. Extra time steps or blind increases of corner order are not selected.

Still required afterwards: full coupled boundary/source energy and continuum
derivative-error control, physical first-u/finite-u extension, source-coupling
calibration, and the actual GR/Newton/observable limits. This continuation
imports no Navier-Stokes regularity theorem into the gravitational system and
does not establish a black-hole interior regularity result.

## Reproduction and scope

New source files under `scripts/`:
- `annular_coupled_current_time_jets_20260909.py`
- `derive_annular_coupled_current_time_jets_20260909.py`
- `annular_coupled_curvature_transfer_20260909.py`
- `derive_annular_coupled_curvature_transfer_20260909.py`
- `annular_curvature_frechet_20260909.py`
- `diagnose_annular_coupled_curvature_error_20260909.py`

Runners refuse to overwrite an existing output owner. Replay into a NEW named
owner only after declaring that name in a new execution snapshot. Existing
complete and failed evidence must remain intact. All source hashes are in the
owner status files; source paths are relative to this post-checkpoint root.

Only local post-checkpoint files were written. No public/private GitHub action,
no edits to formalization-workbench or galaxy work, and no service/process
shutdowns. The three single-core BelowNormal calculations ran sequentially
and exited; no subagents. The user's permission allows up to two modest jobs,
not a pool of extra agents. This is a safe check-in well before four hours.

Final read-only integrity replay:82 unique input paths and40 output artifacts
exist with matching hashes; all six new scripts compile without bytecode;
all claim flags stay false and all four sensitivity failures stay recorded.
The first ad-hoc integrity reader reached the existing resume file and failed
on Windows' default cp1252 decoding. Explicit UTF-8 fixed that reader; the
entire integrity replay then passed. It did not require changing any physics
source, result or tolerance. Read Markdown resume files as UTF-8.
