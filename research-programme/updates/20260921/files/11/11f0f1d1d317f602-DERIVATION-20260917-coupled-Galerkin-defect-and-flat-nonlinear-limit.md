# Coupled Galerkin defect and nonlinear limit of the flat benchmark

2026-09-17. Private continuation of
`DERIVATION-20260917-full-characteristic-reference-and-actual-regularity.md`.

## 1. Result and exact scope

This note derives the missing BASE Galerkin defect, including the source's
field momentum, and combines it with the previously derived extra-Gram
consistency estimate. It then supplies a uniform shifted-energy coercivity
argument and closes the nonlinear relative-energy bootstrap for the specified
flat spherical benchmark. The result is about the exact semidiscrete ODEs,
not an interval certification of numerical time integration.

For the unchanged profile, b0=6.03, V0=.06, m=.03, outer radii5.2/6.8,
T=.4, dyadic base grids n=2^k+1 (k>=5), and eight source-side subdivisions,
both reference and extra-Gram/MTS branches converge in common source-fitted
energy coordinates to the constructed flat continuum reference. A sufficient,
nonsharp error estimate is O(sqrt(h)), for sufficiently small h. Source
position, speed and passive clock converge; material force converges weakly
in time. This does not establish instantaneous source-force convergence.

This is an internal analytic derivation, not an independently reviewed or
proof-assistant-certified theorem. Its bounds are deliberately loose and no
useful numerical h0 is certified. It is not the full GR limit: the geometry
is prescribed flat, not a dynamical solution of Einstein's equations. This
establishes refinement consistency of this action family, not the complete
MTS parent coupling or a new empirical success. Existing force-gate failures
and all previous evidence remain unchanged.

## 2. The unchanged action in fixed source coordinates

Let xi be the source-fitted reference coordinate, with source fixed at xi=b0.
On each side write

    r=xi+w(xi)(b-b0),  J=r_xi,  j=w_xi,  V=bdot,
    rho=J r^2,  kappa=r^2/J,  sigma=r^2 w,  s=V w/J.

Here 0<=w<=1, j is constant separately on the two halves, and the analytic
source gate gives nondegenerate J. For U(t,xi)=phi(t,r(t,xi)), define

    D=U_t-s U_xi.

The base Lagrangian is

    L0=integral [rho D^2/2-kappa U_xi^2/2] dxi
         -m sqrt(1-V^2).                               (1)

The finite action substitutes its continuous P2 field U_h in (1), with the
essential zero at xi=b0. Its fixed-order quadrature is exact on these
piecewise polynomial integrands. The MTS comparison adds the SAME existing
quadratic lifted-Gram potential; no action or sampling rule is changed.

Useful coefficient derivatives are

    rho_b=j r^2+2J r w,     rho_t=V rho_b,
    kappa_b=2r w/J-r^2 j/J^2,
    s_b=-V w j/J^2,         s_t=a w/J-V^2 w j/J^2,
    sigma_t=2r w^2 V,       a=Vdot.

## 3. Exact field and source residuals

Let the reference U be the completed characteristic solution, and I_h its
fixed-xi P2 nodal interpolation. Use

    U_h^r=I_h U,  W_h^r=I_h U_t,  A_h^r=I_h U_tt,
    b_h^r=b,      V_h^r=V,        Vdot_h^r=a.

The source degree of freedom in the field is removed: U_h^r(b0)=0 and its
time derivatives are zero. At the incompatible INITIAL corner that forced
second derivative need not equal the one-sided bulk trace; the estimates
below treat the source-adjacent elements as exceptional. No starting data
are modified to suppress the corner.

For a field test v_h vanishing at the source, the Euler residual is

    R_U(v_h)=-integral v_h(rho_t D+rho D_t) dxi
              -integral v_h,xi(kappa U_xi+sigma V D) dxi,
    D_t=U_tt-s_t U_xi-s U_txi.                         (2)

The SOURCE residual is

    R_b=integral [rho_b D^2/2-rho s_b D U_xi
                  -kappa_b U_xi^2/2
                  +sigma_t D U_xi+sigma D_t U_xi
                  +sigma D U_txi] dxi -mu a,
    mu=m/(1-V^2)^(3/2).                               (3)

In particular, the source field momentum is -integral sigma D U_xi.
Every one of its time-derivative terms is retained in (3). The discrete
source force is not replaced by a continuum pressure formula.

For the EXACT reference, (2) vanishes. At the fixed outer boundaries w=0
and phi_r=0; at the source v_h=0. Across each travelling curvature front,
first derivatives are continuous, so no distributional delta is omitted.

For the exact reference only, integration by parts and the bulk equation
reduce the wave part of (3) to

    b^2(1-V^2)(phi_r,-^2-phi_r,+^2)/2.

One direct shape-variation check: on the left the moving-boundary field
variation is delta phi=-phi_r delta b. The scalar surface term is
-b^2(phi_r+V phi_t)delta phi plus the moving-domain Lagrangian term.
Using phi_t=-V phi_r gives +b^2(1-V^2)phi_r^2 delta b/2.
The right side has the opposite orientation. The material term is -mu a.
Thus the original characteristic source ODE makes (3) exactly zero.

### Canonical meaning

Along this interpolated reference, configuration rates and passive clock
match exactly. If z_h^r denotes its velocity-coordinate state and K_kin the
coupled velocity Hessian, then

    R_c=F_c(Y_h)-Ydot_h=(0,R_U,R_b),
    (R_U,R_b)=K_kin[F_v(z_h^r)-zdot_h^r]_accelerations. (4)

Here Y_h is the kinetic Legendre image of z_h^r. The mass-dual field norm is

    ||R_c||_*^2=R_U^T M(b)^-1 R_U+R_b^2,              (5)

with equivalent fixed-reference weights used for the time-independent
comparison norm. Source scaling in (5) is fixed in benchmark units, not a
new adjustable physical parameter.

Independent split integration of (2)-(3), the original finite-action flow,
and a complex directional derivative of the canonical momenta all agree.
Thus (4) is checked without differentiating the same acceleration code twice.

## 4. Interpolation errors really give a small strong residual

Set e=I_h U-U, e_t=I_h U_t-U_t, e_tt=I_h U_tt-U_tt. Subtract the exact
zero residual from (2). Its two coefficient errors are

    delta D=e_t-s e_xi,
    delta D_t=e_tt-s_t e_xi-s e_txi,
    delta P_t=rho_t delta D+rho delta D_t,
    delta Q=kappa e_xi+sigma V delta D,
    R_U(v_h)=-integral(v_h delta P_t+v_h,xi delta Q).   (6)

These are identities, not a truncation of a nonlinear force law.

### Why this mesh family has uniform constants

With base spacing h=(8/5)/2^k, the anchor phase cycles through1/5,2/5,3/5,4/5.
Eight fixed subdivisions therefore give minimum ELEMENT width h/40 and
maximum width h. No arbitrarily small cut fraction is assumed away.
The exact reference P2 inverse inequality is

    integral_0^1 |p'|^2 <=60 integral_0^1 |p|^2.

Consequently ||v_h,xi||_L2 <=40 sqrt(60) h^-1 ||v_h||_L2.
Bounded positive rho gives the corresponding weighted inverse estimate.
This statement is restricted to the specified family, not arbitrary moving
unfitted meshes with degenerating source cuts.

### Exceptional cells have small total measure

The actual reference is C1 across its two travelling initial fronts, has
bounded piecewise derivatives through order three, and satisfies the
source-fitted one-sided regularity proved in the preceding note. Third
derivatives can change at envelope transitions without a curvature jump.
All mixed spacetime derivatives through order three have analogous bounds
from the same F/G derivative majorants. Pullback derivatives add only bounded
J,w,j,V,a coefficients.

Away from the two fronts, U is W3,infinity, U_t is W2,infinity and U_tt is
W1,infinity. Across a front U_t is continuous and Lipschitz, while U_tt and
U_txi can jump. Include both source-adjacent cells among the exceptional
cells to cover the initial corner. Their total measure is at most4h.

The P2 basis reproduces quadratics, has a conservative value bound3 and
derivative-sum bound8. Taylor remainders on regular cells and Lipschitz
bounds on exceptional cells therefore give, uniformly in time almost
everywhere,

|Error|Regular-cell pointwise size|Exceptional-cell size|Global L2 size|
|---|---|---|---|
|e_xi|O(h^2)|O(h)|O(h^(3/2))|
|e_t|O(h^2)|O(h)|O(h^(3/2))|
|e_txi|O(h)|O(1)|O(h^(1/2))|
|e_tt|O(h)|O(1)|O(h^(1/2))|

The last two errors have global L1 size O(h). All constants depend on the
explicit reference bounds, not on h. At a front exactly coincident with a
vertex, either bounded one-sided second derivative may be assigned; the
affected elements are still in the exceptional set. The reference path is
absolutely continuous in canonical variables, which suffices for the
almost-everywhere energy estimate; no false C2-in-time condition is imposed.

Using (6), the inverse estimate and these error sizes yields

    ||R_U||_M^-1 <= C[||e_t||+||e_xi||+||e_tt||+||e_txi||
                       +h^-1(||e_xi||+||e_t||)]
                  <=C sqrt(h).                        (7)

For (3), interpolated D,U_xi,D_t,U_txi and the corresponding exact quantities
are uniformly bounded. Differences of its quadratic products are controlled
by the L1 errors just listed. The identical material inertia term cancels.
Hence

    |R_b,base|<=C h,    ||R_c,base||_*<=C sqrt(h).      (8)

This is a STRONG mass-dual residual estimate, not merely an H^-1 estimate
silently inserted into an L2-energy proof.

The preceding actual-reference curvature/lift estimate gives

    ||R_c,Gram||_*<=C sqrt(h).

The kinetic Legendre map is common to the two branches, so their residuals
add exactly. Thus the TOTAL canonical reference defect satisfies

    ess sup_[0,T] ||R_c,h||_*<=C_R sqrt(h)             (9)

for both unchanged actions. The statement is asymptotic and nonsharp; it
does not assert monotone sampled residuals or a small force error at a
particular existing grid.

## 5. The reference-flow regularity hypothesis also closes

The energy norm on canonical variations consists of one-sided reference H1
field coordinates, mass-dual L2 momenta and the two scalar source components.
Poincare's inequality uses the fixed essential value at the source, so the
bulk stiffness is positive without an artificial outer Dirichlet condition.

For Ydot_h, the configuration component I_h U_t has uniformly bounded H1
norm. The field momentum derivative is the finite-element moment of
rho_t D_h+rho D_h,t; both densities have a uniform L2 bound. Its mass-dual
norm is therefore bounded. The source momentum derivative contains products
of bounded L2 functions and fixed bounded scalar coefficients; it too is
uniformly bounded. These bounds use the actual characteristic derivatives,
not a supposition that an evolved MTS solution is already smooth.

Consequently

    ||Ydot_h||_*<=C_Y,
    ||F_c,h(Y_h)||_*<=C_Y+C_R sqrt(h)<=L_F             (10)

uniformly for h<=1. This supplies the strong reference-flow input required
by the previous relative-Hamiltonian identity.

## 6. A uniform nonlinear energy neighborhood

Use the same reduced Hamiltonian and kinetic Legendre transform as in
`DERIVATION-20260917-time-dependent-force-adjoint-and-relative-energy.md`.
Write A for the transport matrix, B for the source-wave kinetic square, and
K=K_bulk+K_Gram for the potential stiffness. The kinetic Hessian is

    K_kin=[[M, A U],[(A U)^T, mu+U^T B U]].

Its quadratic form is the integral of a squared physical field-rate
variation plus mu(delta V)^2. Cauchy-Schwarz and mu>=m>0 give uniform
coercivity and upper bounds in mass-L2 field rate plus scalar speed norm
on a bounded field-energy neighborhood. The constants depend on its radius
and the positive geometry margins, not on the number of nodes.

### Fixed-b canonical square completion

Hold delta b=0, but retain BOTH field and source momentum variations. With
L_vU the velocity/field-coordinate mixed derivative, the exact identity is

    delta^2 H_h
      =delta U^T(K-V^2 B)delta U
        +(delta p-L_vU delta U)^T K_kin^-1
                     (delta p-L_vU delta U).          (11)

Since 0<=w<=1, B<=K_bulk as quadratic forms. The Gram coefficient weights
are nonnegative convex samples of positive r^2/J. Thus

    K-V^2 B >=(1-V^2)K_bulk+K_Gram.                   (12)

Uniform kinetic bounds and bounded L_vU convert (11)-(12) into a strictly
positive lower bound c_Z for the entire fixed-b canonical block in the
energy norm. This includes source momentum: it is not a field-only test
that discards the coupled source degree of freedom.

### Uniform bounds on the remaining blocks

On bounded canonical energy sets with nondegenerate b and |V|<v_*<1,
the reduced Hamiltonian is uniformly C3 in the energy norm. To make the
mesh-independent point explicit: the raw third-difference factor is bounded
by sqrt(h) times the H1 norm; its hinge vector is O(h), while its P2 jump
trace is bounded by C h^-1/2 times that norm. The Gram quadratic form has
weight O(1/h), so those factors cancel. The same estimates hold for its
first three b derivatives because only bounded smooth coefficient weights
change. Bulk, kinetic and inverse-mass derivatives obey the corresponding
uniform form bounds. The scalar Legendre inverse has denominator
d+m/(1-V^2)^(3/2)>=m. No uniform bound on D2F is invoked.

Let C_b bound the energy-dual b/canonical mixed block and C_bb bound |H_bb|
on such a neighborhood. ONE constant comparison shift

    beta=1+C_bb+2 C_b^2/c_Z

gives

    D2H_h+beta e_b e_b^T >=min(c_Z/2,1) I_energy.      (13)

This follows by Young's inequality on the mixed block. Its upper bound is
uniform as well. The shift is only part of the comparison energy, never
an added source force or a replacement physical action.

Choose a fixed small canonical-energy tube around the uniformly bounded
reference family. Smooth inverse Legendre dependence gives a mesh-independent
speed margin (for example choose a tube inside |V|<7/8) and the already
nondegenerate source geometry. The same uniform bounds apply on straight
segments inside a sufficiently small tube. Thus (13) holds throughout the
tube, not only at the numerical sample points.

The sample-specific Schur shifts recorded by the checker are illustrations
of (11)-(13), NOT the global beta or a certificate of this entire tube.

## 7. Close the nonlinear bootstrap

Let X_h be the exact finite canonical solution and Y_h the reference just
constructed. Define the unchanged Hamiltonian's shifted relative energy

    E_h=H_h(X_h)-H_h(Y_h)-DH_h(Y_h)(X_h-Y_h)
         +beta(delta b)^2/2.

Its exact identity from the preceding note cancels the perturbed principal
Hamiltonian evolution. With (9)-(13), it gives for r_h=sqrt(2E_h)

    r_h'<=C_s r_h+C_f C_R sqrt(h)                     (14)

almost everywhere, with constants independent of h while the solution
remains in the chosen tube. Explicitly C_s=(C3 L_F+2 beta L_V)/(2m0)
and C_f=M0/sqrt(m0) in the earlier notation.

The original discrete initialization is EXACTLY I_h U(0), I_h U_t(0),
b0,V0 and the same passive clock; hence X_h(0)=Y_h(0) in exact arithmetic.
There is no hidden initial-data projection fitted to the outcome. Therefore

    ||X_h(t)-Y_h(t)||_* <=A_T sqrt(h),    0<=t<=T,     (15)

where A_T=(C_f C_R/sqrt(m0))(exp(C_s T)-1)/C_s, using T when C_s=0.
For a tube radius epsilon choose h0 so A_T sqrt(h0)<epsilon/2.
A first-exit argument then prevents leaving the tube for h<h0. Smooth
finite-dimensional Hamiltonian continuation on its nondegenerate timelike
domain extends the solution through T. This closes, rather than assumes,
the nonlinear neighborhood bootstrap for the stated exact flat benchmark.

Interpolation errors vanish too. Thus the exact semidiscrete fields converge
in common source-fitted energy coordinates; source b,V and passive clock
converge uniformly. Transforming to a common PHYSICAL radius across two
slightly different source positions may lose a rate because the reference
field gradient jumps at the source. Equation (15) must not be relabelled
as the same rate for every fixed-radius waveform norm.

This is a sufficient asymptotic result. The majorants are too loose to say
that a currently computed grid is below h0, and time-discretization error
requires separate controls. No current force gate is promoted by (15).

### A force consequence that really follows

The physical material momentum is p_m=mV/sqrt(1-V^2), and the unchanged
finite force observable is F_m=dp_m/dt. Uniform speed convergence on the
timelike tube gives uniform material-momentum convergence. For any fixed
smooth time test eta with compact support in (0,T),

    |integral eta(t)[F_m,h-F_m](t) dt|
       =|integral eta'(t)[p_m,h-p_m](t) dt|
       <=C sqrt(h) ||eta'||_L1.                       (16)

Endpoint terms give the equivalent cumulative-impulse statement. Fixed
time-window averages therefore converge. This is a WEAK force limit, not
pointwise acceleration or an instantaneous maximum-force bound. Narrowing
the averaging window changes the constant; it is not a way to erase the
old peak-force failures.

## 8. Numerical checks and retained failure

Three successful suites complete505 implementation checks:
296 coupled-defect checks (seven grids, six times),110 coercivity/algebra
checks (two branches, three grids, three times), and99 reference-flow checks.
No finite trajectory is re-evolved or fitted. Tests corroborate the algebra
and implementation; the asymptotic argument is (6)-(15), not a regression
through these sampled values.

|Base nodes|Maximum sampled base canonical defect|Extra-Gram defect|Total MTS defect|
|---|---:|---:|---:|
|33|1.51863645e-2|5.71513452e-1|5.72290884e-1|
|65|7.06325224e-3|1.58596099|1.58597784|
|129|1.95394415e-3|2.29577446e-1|2.29600679e-1|
|257|8.75900613e-4|4.15486891e-1|4.15487683e-1|
|513|5.08748167e-4|5.63825895e-2|5.63865270e-2|
|1025|1.87340684e-4|4.82682977e-2|4.82682722e-2|
|2049|2.14506793e-4|6.18284516e-3|6.18428739e-3|

Neither sequence is asserted monotone. The base defect rises on the last
sampled refinement; the Gram defect rises at65 and257. Moving fronts and
the changing anchor phase matter. The O(sqrt(h)) bound allows such
oscillation; these samples neither replace nor numerically certify the
essential time supremum in (9). A canonical residual norm is not the source
force error in the old acceptance table.

The independent continuum weak balance and finite-action comparison have
errors up to about6.1e-9 at the largest mesh, below their declared2e-8 check.
This diagnostic exhibits finite precision/conditioning limits, not an exact
floating-point zero. The source momentum complex-derivative comparison is
below2.76e-16 on the small-grid coercivity set.

Fixed-b generalized Hessian margins exceed.9400 at all18 sample states;
demonstration shifts about1.00022 give shifted margins above.9085. Actual
reference derivative energy norms stay around.715 across the seven meshes;
the sampled canonical flow remains bounded, with a coarse MTS maximum1.7394.
These are useful cross-checks, not proofs of global or uniform positivity.

One implementation qualification FAILED and is preserved:
`source-intake/navier-stokes/20260914/annular-galerkin-coercivity-attempt01/status.json`.
The test incorrectly demanded every stored sparse sampling entry be strictly
positive. The matrix contains29 explicitly stored zeros on the33 grid, no
negative entries, and each row sums to1. The corrected version tests the
actual mathematical requirement: nonnegative partition weights. It does not
alter the action, remove a negative eigenvalue or relax a force threshold.
The original script and failed evidence remain immutable. This brings the
retained failed-attempt total to26, including the25 inherited failures.

## 9. Next target, without reopening completed work

The base residual, strong reference-flow bound and nonlinear energy tube
are no longer merely missing hypotheses for THIS exact flat benchmark.
Next address the FORCE OBSERVABLE: use the derived momentum/weak-force law
to qualify fixed-window impulses on saved data, and determine what additional
trace/time-regularity estimate is genuinely needed for instantaneous force.
Do not quietly upgrade an averaged result to a peak-force result.

The separate route from prescribed flat geometry to live parent gravity is
still open. This theorem does not sign the full parent action, derive Newton's
constant, solve a black hole or establish a full GR/Newton limit.

Implementation and sources:

- `scripts/annular_characteristic_galerkin_defect_20260917.py`
- `scripts/qualify_annular_galerkin_defect_20260917.py`
- `scripts/qualify_annular_galerkin_coercivity_20260917.py`
- `scripts/qualify_annular_galerkin_coercivity_v2_20260917.py`
- `scripts/qualify_annular_reference_energy_flow_20260917.py`
- `source-intake/navier-stokes/20260914/annular-coupled-galerkin-defect-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-galerkin-coercivity-attempt02/status.json`
- `source-intake/navier-stokes/20260914/annular-reference-energy-flow-attempt01/status.json`
- `DERIVATION-20260917-full-characteristic-reference-and-actual-regularity.md`
- `DERIVATION-20260917-time-dependent-force-adjoint-and-relative-energy.md`
