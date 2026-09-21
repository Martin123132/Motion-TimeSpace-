# Nonlinear initial-force refinement bound

2026-09-17. Private continuation of
`DERIVATION-20260917-initial-corner-response-and-frozen-action-prediction.md`.

## 1. Result, rather than another missing-regularity hypothesis

For BOTH unchanged prescribed-flat finite-action branches, on the dyadic
base grids with eight source-side subdivisions, the existing nonlinear
energy argument can be sharpened to the material-force estimate

    |f_h(X_h(t))-F_ref(t)| <= C [h+t+t^2],   0<=t<=T=.4, (1)

for sufficiently small h. Here X_h is the EXACT nonlinear semidiscrete
solution, not the frozen tangent prediction, and C is independent of h.
It may be large. The following proof derives the additional observable
and projection estimates required for(1).

Consequences:

- For every fixed finite tau_*, the INITIAL layer0<=t<=tau_* h has
  uniform force error O(h).
- More generally, every shrinking initial window0<=t<=T_h, T_h->0,
  has vanishing uniform force error, bounded by C(h+T_h+T_h^2).
- This DOES NOT prove force convergence at a fixed positive time, nor
  uniformly on the unchanged interval[0,.4]. For fixed t, the right side
  of(1) does not vanish as h->0.

This is an internal analytic derivation using the previously derived
reference regularity, Galerkin defect and uniform Hamiltonian neighborhood.
It is not independent proof review, a useful numerical h0 certificate,
or a certified time-integration error bound. It is not full GR: the
background remains prescribed flat. Every old peak-force failure stays
unchanged. No corrected force is substituted in the tests.

The route is shorter than constructing an entire infinite-lattice response:
derive the ACTUAL material-force functional and a phase-uniform bound on
its Hamiltonian generator. No leading lifted-Gram term is removed, and
no instantaneous-force regularity of the evolved solution is assumed.
All quantities use the existing benchmark units.

## 2. Inputs already established, with their exact role

Let Y_h(t) be the kinetic Legendre image of the P2-interpolated full
characteristic reference. Let H_h be either original finite Hamiltonian,
and use the fixed reference-geometry energy norm

    ||(delta U,delta b,delta P,delta p_b)||_E^2
       =delta U^T K0 delta U+delta b^2
           +delta P^T M0^-1 delta P+delta p_b^2.       (2)

K0 is the positive bulk stiffness with the essential zero at the source;
M0 is the weighted mass matrix at b0. Moving-geometry versions of this
norm are uniformly equivalent on the established tube.

Sections4-7 of
`DERIVATION-20260917-coupled-Galerkin-defect-and-flat-nonlinear-limit.md`
provide the following inputs, including the actual reference's two
curvature fronts and the source-field momentum:

    X_h(0)=Y_h(0),
    R_h=J DH_h(Y_h)-Ydot_h,  ||R_h||_E<=C_R sqrt(h),
    ||J DH_h(Y_h)||_E<=L,
    ||D^j H_h||<=G_j, j=1,2,3,                      (3)

on a mesh-independent, nondegenerate timelike tube. Bounds for the second
and third derivatives are in the energy norm. The first-derivative bound
also follows directly from the bounded kinetic/potential forms and the
scalar source terms on that tube. The canonical Poisson matrix J is not
asserted to be uniformly bounded in this norm.

Retaining t in the existing relative-energy integration, rather than
replacing it immediately by T, gives

    d_h(t):=||X_h(t)-Y_h(t)||_E
       <=A sqrt(h) (exp(Gamma t)-1)/Gamma
       <=A t exp(Gamma T) sqrt(h).                  (4)

The Gamma=0 interpretation is t. The same first-exit argument gives
existence and validity throughout[0,T] for sufficiently small h. Constants
are independent of h, but this does not identify a practical grid below h0.

The interpolation estimates used below are, uniformly in time on both
source halves,

    ||e_xi||_L2+||e_t||_L2=O(h^(3/2)),
    ||e_xi||_L1+||e_t||_L1=O(h^2),
    ||e_txi||_L1+||e_tt||_L1=O(h),                  (5)

where e=I_h U-U. The source-adjacent cells and the finitely many
front-intersected cells are included as exceptional cells, not assumed
smooth. The reference U_xi and U_t are continuous and piecewise Lipschitz
on each source half, with bounded one-sided derivatives.

## 3. Phase-uniform canonical Poisson bound

The P2 element mass/stiffness generalized eigenvalues on[0,1] are exactly
0,12,60. Thus ||v'||_L2<=sqrt(60)/ell ||v||_L2 on an element of length ell.
The anchor fraction on h=(8/5)/2^k, k>=5, lies in
{1/5,2/5,3/5,4/5}, because2^k is nonzero modulo5. Eight subdivisions
give minimum element width h/40. This covers every phase in this family,
not just two numerically convenient meshes.

Since r lies in[26/5,34/5] at the reference geometry,

    K0 <= [40 sqrt(60) (17/13)/h]^2 M0.              (6)

For covectors, the canonical J swaps position and momentum blocks. Direct
use of(2) shows

    ||J||_(E* -> E)
       =max(1,sqrt(lambda_max(M0^-1 K0)))
       <=C_J/h,  C_J=40 sqrt(60)(17/13)~405.173642.  (7)

The source block has unit norm. This is an analytic bound, not an eigenvalue
fit, and does not erase the mesh-frequency amplification.

## 4. Exact material force and source projection

Write c=A U and

    p_b=p_m+W^T A U+V U^T B U,
    p_m=mV/sqrt(1-V^2),   mu=dp_m/dV,
    v_h=M^-1 c,
    S=mu+U^T B U-c^T M^-1 c >=mu>0.                (8)

The inequality is the original coupled kinetic square/Cauchy-Schwarz
identity. No source-field term has been dropped.

In canonical coordinates V=partial H_h/partial p_b. Define p(X)=p_m(V(X)).
On the established |V|<=v_*<1 tube,

    ||Dp||<=P1:=mu_max G2,
    ||D2p||<=P2:=mu_max G3+|mu'|_max G2^2,          (9)

where mu_max=m/(1-v_*^2)^(3/2) and
|mu'|_max=3m v_* /(1-v_*^2)^(5/2). These constants are uniform because
the canonical p_b unit vector has E-norm1. The exact force observable is

    f_h(X)=Dp(X) J DH_h(X).                         (10)

The reference configuration rates agree with its interpolant, so R_h has
only momentum components (R_U,R_b). Since p(Y_h)=p_m(V_ref),

    f_h(Y_h)-F_ref
       =Dp(Y_h)R_h
       =(mu/S)[R_b-c^T M^-1 R_U].                  (11)

This is the material-source Schur projection of the full Galerkin defect.
It is not a substitution of the continuum pressure formula for the
discrete source equation. Equation(11) is independently checked against
the original finite force and the transformed canonical momentum covector.

### Why the projected consistency error improves to O(h)

We need a bounded test v_h=M^-1 c. In weak form it is the weighted L2
projection of g_h=-(w/Jmap)(I_h U)_xi, with mass density rho=Jmap r^2.
The reference interpolation has a uniform one-sided slope bound, so
||g_h||_infinity<=C.

Here is a direct max-norm projection bound, avoiding an assumed discrete
maximum principle. For the standard P2 basis, the endpoint/midpoint
absolute integrals are1/4 and2/3; the Lebesgue constant is5/4. The unweighted
mass diagonal-dominance margins are1/30 and2/5. If rho_max/rho_min<=51/50
on each element, weighted margins are at least

    rho_min ell [1/30-(1/50)(5/16)]=rho_min ell(13/480),
    rho_min ell [2/5-(1/50)(5/6)]=rho_min ell(23/60). (12)

This follows by bounding each off-diagonal perturbation by
eta integral |N_i| sum_j |N_j|; the nonnegative diagonal perturbation
can be discarded. Assembly preserves the lower bounds, and deleting the
essential-source column can only improve them.

At a maximal nodal component of the mass solve, diagonal dominance and
the load bound give ||v_nodes||_infinity<=10||g_h||_infinity. Hence

    ||v_h||_infinity<=12.5||g_h||_infinity<=C,
    ||v_h,xi||_infinity<=C/h.                       (13)

The density condition holds for all sufficiently small h: on each half
Jmap is constant per element, r varies by at most Jmax h, and r>=26/5.
It suffices that(1+Jmax h/(26/5))^2<=51/50. This is only a projection
mesh condition, not the complete nonlinear h0.

The exact weak-form base residual from the earlier note is

    R_U,base(v)=-integral(v delta P_t+v_xi delta Q),
    ||delta P_t||_L1=O(h), ||delta Q||_L1=O(h^2),
    |R_b,base|=O(h).                                (14)

Combining(13)-(14) proves |R_U,base(v_h)|<=C h.

The retained Gram part has R_U,G(v_h)=-(L_h v_h)^T D_h L_h I_h U.
The actual bounded-row local third-difference factor and its hinge lift
give

    ||L_h I_h U||_ell1<=C h^2,
    ||L_h v_h||_ell-infinity<=C,  ||D_h||<=C/h.      (15)

For completeness: ordinary stencils of a piecewise C3 reference contribute
O(h^3) each over O(1/h) rows. Only O(1) rows intersect a curvature front
or the source, contributing O(h^2) each after removing the true source
gradient jump. The P2 jump estimate differs from that true jump by O(h)
even when a front lies in a source-adjacent cell; multiplying by the
O(h), finitely supported hinge vector gives O(h^2). The unchanged
boundary factor combinations have bounded coefficients and bounded
stencil width, so the same sum bound holds.

For v_h, bounded nodal values bound the raw factor. Its P2 jump is at
most C/h times those values; the hinge is O(h). This proves the second
bound in(15) without assuming v_h has a bounded derivative.

Thus the projected Gram term is O(h), NOT set to zero. Also
|R_b,G|<=C h^-1 ||L_h I_h U||_ell2^2<=C h^3; the b derivative changes
only the bounded weight, since L_h is fixed in source coordinates.
With mu/S<=1, equation(11) now yields

    |f_h(Y_h(t))-F_ref(t)|<=C_cons h.                (16)

This is a same-state interpolant consistency result, not yet the force
error on the evolved finite solution.

## 5. Bound the material-momentum Hamiltonian generator

The crucial improvement over a generic O(1/h) force Lipschitz estimate
comes from the reference vector J Dp(Y_h).

First,

    ||v_h||_H1<=C h^-1/2,   v_h=M^-1 A I_h U.       (17)

To see this, let g=-(w/Jmap)U_xi, which is uniformly one-sided H1 and
Lipschitz. It need not vanish at the source. Interpolate g but set its
source nodal value to zero. This approximant z_h has H1 norm O(h^-1/2)
and L2 error O(sqrt(h)); the forced source value changes only two cells.
The P2 inverse bound and L2 stability of the weighted orthogonal
projection then give the same H1 bound for its projection. Replacing
g by g_h changes its L2 norm by O(h^(3/2)), by(5), and its projected
H1 norm by at most O(sqrt(h)). This proves(17), rather than assuming
uniform trace smoothness at the initial corner.

The exact canonical momentum derivatives are

    (Dp)_P=-(mu/S)v_h,      (Dp)_pb=mu/S,
    (Dp)_U=-(mu/S)[A^T W+2V B U-V A^T v_h].         (18)

The b component is uniformly bounded by(9).
For the interpolated reference,

    ||A^T W||_M^-1+||B U||_M^-1<=C,
    ||A^T v_h||_M^-1<=C(1+||v_h||_H1)<=C h^-1/2.  (19)

For the first bound, integrate the exact reference terms by parts: U_t
and U_xi have bounded one-sided derivatives, the field test vanishes at
the source, and w=0 at the outer ends. Continuous first derivatives at
the travelling fronts prevent internal delta terms. The interpolation
remainders have L2 size O(h^(3/2)); the inverse test-derivative bound
costs only1/h, leaving O(sqrt(h)). For the second bound, the same
integration by parts applies to v_h and(17).

Equations(17)-(19), including BOTH source scalar components, give

    ||J Dp(Y_h)||_E<=C_p h^-1/2.                    (20)

The kinetic map is common to both branches, so this reference generator
is the same for both. The Gram term remains in H_h, its derivatives,
and the evolution/defect; common kinetics does not make the dynamics equal.

## 6. Derive the nonlinear force estimate

For a point Z on the straight segment between Y_h and X_h, let
d=||X_h-Y_h||_E. From(7), the uniform Hamiltonian Hessian bound, and(3),

    ||F_c(Z)||_E<=L+C_J G2 d/h,
    ||J Dp(Z)||_E<=C_p h^-1/2+C_J P2 d/h.           (21)

These follow from ordinary differences around Y_h. They do not assume
that the evolved solution already has smooth traces or bounded force rates.

Differentiating the exact observable(10), for any energy-unit variation e,

    Df_h(Z)e=D2p(Z)[e,F_c(Z)]+Dp(Z) J D2H_h(Z)e.

Use antisymmetry of the canonical J to bound the second term by
G2||J Dp(Z)||_E. Equations(9),(20)-(21) imply

    ||Df_h(Z)||_E* <=C_0+C_1 h^-1/2+C_2 d/h.        (22)

Integrating along the segment gives

    |f_h(X_h)-f_h(Y_h)|
       <=(C_0+C_1 h^-1/2)d+C_2 d^2/h.              (23)

Insert the TIME-RESOLVED estimate(4). Uniformly for0<=t<=T,

    |f_h(X_h)-f_h(Y_h)|<=C[t sqrt(h)+t+t^2].

Finally add the projected consistency result(16), and use h<=1, to
obtain(1). The argument concerns the original nonlinear semidiscrete
flow; the frozen approximation from the preceding step is not used
as a replacement trajectory anywhere in this proof.

The residual/reference derivatives are defined almost everywhere at
front/node coincidences. The force observable and Y_h are continuous,
so the resulting force bound extends to those isolated times and the
initial endpoint. No initial-time plateau or compatible-data replacement
is inserted.

## 7. Limits that must remain visible

Equation(1) is a genuine initial-layer refinement result, not a global
instantaneous-force theorem. It cannot be tiled across[0,T] by resetting
the error to zero at later times: the actual accumulated state error
at such a restart is not zero. At a fixed positive time, the present
energy error O(sqrt(h)) and sensitivity O(h^-1/2) still permit O(1)
force differences. That remaining loss is precisely visible in(23).

The constants in(1) are NOT determined by fitting the diagnostics below.
They depend on the earlier explicit/reference majorants, energy tube,
mass and geometry margins. A practically useful majorant and h0 remain
uncertified, so no existing2e-7 force threshold is declared passed.
This does not derive live geometry, black-hole regularity, a parent
coupling constant or an empirical success.

## 8. Independent qualifications and retained failures

`scripts/qualify_annular_shrinking_window_force_v2_20260917.py` completes
332 implementation checks across7 grids33..2049, both branches, and5
initially scaled times. It checks the exact P2 inverse spectrum, source
phases, canonical Poisson probes, the force-defect Schur identity and
the independent canonical momentum projection. Maximum force-projection
identity discrepancy is6.506e-19 in benchmark arithmetic.

The first version
`scripts/qualify_annular_shrinking_window_force_20260917.py` is retained
as a failed checker attempt. It compared two SymPy Poly objects whose
identical polynomials had different coefficient domains (QQ versus ZZ).
Version2 compares their exact polynomial expressions. The spectrum
remains0,12,60; no physical equation, action or acceptance gate changed.
There are now29 retained failed attempts:28 inherited plus this one.

`scripts/qualify_annular_material_generator_bound_20260917.py` completes
565 implementation checks. It checks the exact weighted mass/projection
constants, canonical generator and projected Gram identities, with both
scaled early times and fixed times through.4. These are not uniform
certificates inferred from numerical samples.

Selected measured maxima:

|Base nodes|max sqrt(h) times reference material-generator norm|max MTS Gram-factor ell1 norm / h^2|
|---|---:|---:|
|33|1.12318|.445197|
|65|1.25823|.438301|
|129|1.06475|.415244|
|257|1.39111|.396770|
|513|1.09808|.384517|
|1025|1.24724|.378457|
|2049|1.05825|.376529|

The first column of measurements is identical for both branches because
it depends on the common kinetic map evaluated at the same reference.
The phase oscillations are retained; no monotone fit is asserted.

Important distinction: the MTS interpolant's force-consistency error can
exceed the actual evolved force error. For example, the sampled1025
interpolant consistency maximum is1.91023e-5, whereas the OLD evolved
full-horizon sampled force error is9.13531e-7. They are different
quantities. The proof compares them through the dynamics; neither is
silently substituted for the other in a physical test.

Evidence:

- `source-intake/navier-stokes/20260914/annular-shrinking-window-force-attempt01/status.json` — retained symbolic-checker failure.
- `source-intake/navier-stokes/20260914/annular-shrinking-window-force-attempt02/status.json` —332 successful checks.
- `source-intake/navier-stokes/20260914/annular-material-generator-bound-attempt01/status.json` —565 successful checks.

Total897 successful current implementation checks, not897 physics passes.
No nonlinear finite trajectory was rerun, no GitHub action or subagent was
used, and the protected workbench is not edited.

## 9. Next target after closing this initial-window bound

Do not repeat the initial-layer proof or launch another coarse/fine pair
to rediscover it. The next substantive step is the fixed-positive-time
force loss in(23): derive an observable-weighted or localized defect
estimate that improves the accumulated state error in the force-sensitive
direction, including the later envelope transition. The full energy norm
bound alone is not enough.

The already qualified signed adjoint and exact source Schur projection
provide a concrete route: exploit localization/cancellation in the
projected residual while controlling the nonlinear remainder. Preserve
the actual source-field momentum and Gram terms. A frozen or linear
adjoint match is a diagnostic unless its nonlinear remainder is bounded.
