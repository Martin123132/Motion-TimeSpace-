# Released-slope law and a derived boundary-feedback normal form

Private continuation, 2026-09-10 (Europe/London). No GitHub action.

## 1. What actually advances

The homogeneous clock-gradient boundary feedback now has an EXACT, invertible
change of variables which moves it out of the configuration equation and into
explicit mass-norm-controlled terms in the velocity equation. No physical
equation, slope condition, source, or trajectory is changed. No new field,
adjustable coefficient, or small-gain assumption is introduced.

The key cancellation is T_t+T D_g=S, where S depends on existing second metric
time jets, not on a third time jet or a derivative of the unknown graph state.
The feedback T and S have explicit conditional mesh-independent bounds from
the already derived discrete elliptic derivative estimate. The old endpoint
commutator bound supplies the other term needed by this transformation.

This is a constructive change in the energy argument, not a certificate that
the parent theory, local GR, or the horizon problem is solved. The regular
transport estimate and propagation of its coefficient bounds remain open.

Validation: 1039 passing algebra/bound checks on 18 unchanged saved states and
24 manufactured coefficient controls. These are repeated identities and
numerical-analysis tests, NOT 1039 independent confirmations of MTS physics.

## 2. Same canonical system and notation

Use the positive annulus, actual composite Gauss4 rule, zero endpoint VALUES
and fully released slopes of the preceding derivations. All quantities use
the inherited dimensionless coordinate/time conventions. This checkpoint
remains in b2=b3=m_chi=Lambda=0, in both GR and metric_Gram branches.

The weighted projection Pi, mass M, full stiffness K including Gram, and
their time derivatives are unchanged. Put

    L=M^-1 K, U=L^-1, A=M^-1 M_t,
    C=M^-1 K_t U, D_g=C-A, D_h=C-A-L A U,
    B=Pi ell_map, F_B=B_t-D_h B.

The old graph pair satisfies exactly

    g_t=h+D_g g+b,
    h_t=-L g+D_h h+r.

Here b is the ENTIRE old configuration source, including the previously
derived external endpoint term B beta; r retains the actual free Euler
residual. The original energy is E_H=(g^T K g+h^T M h)/2.

Sources:

- `DERIVATION-20260910-endpoint-commutator-bound-with-parent-clock-jumps.md`
- `DERIVATION-20260910-boundary-memory-correction-without-clock-differentiation.md`
- `scripts/annular_paired_variational_energy_20260910.py`
- `scripts/annular_H1_clock_energy_20260909.py`

## 3. The released slope gives a moment equation, not a pointwise boundary PDE

For arbitrary free graph coefficients g, reconstruct the actual cubic u=U g.
At an endpoint R_e let sigma=+1 on the left and -1 on the right and let
s=sigma(R-R_e)/h on the adjacent scalar cell. The positive slope test

    v_e=h s(1-s)^2

belongs to the free space. Its endpoint radial derivative is sigma and its
other nodal values and slopes vanish. It is a scaled original slope row,
not a newly prescribed condition. Gram acts on nodal values only, so this
test has exactly zero Gram force in the canonical branch.

Because u is cubic on that entire scalar cell, including across its interior
staggered mass face, write

    u_R(R)=u_R(e)+(R-R_e)u_RR(e)+(R-R_e)^2 u_RRR/2.

With the ACTUAL quadrature on that cell, define

    I0=Q[p v_e,R], I1=Q[p v_e,R (R-R_e)],
    I2=Q[p v_e,R (R-R_e)^2]/2, J=Q[m g v_e].

The released slope row gives the exact law

    I0 u_R(e)+I1 u_RR(e)+I2 u_RRR=J.

When I1 is nonzero, this determines

    u_RR(e)=(J-I0 u_R(e)-I2 u_RRR)/I1.

All tested variable-coefficient I1 values are negative. This numerical check
is not a general theorem that I1 can never vanish for arbitrary coefficients.
The undivided row identity is the general statement.

For constant p, exact polynomial integration gives

    I0=0, I1=-p h^2/12, I2=-sigma p h^3/30,
    u_RR(e)+(2 sigma h/5)u_RRR=-12 J/(p h^2).

Therefore g(e)=0 DOES NOT imply u_RR(e)=0. In particular the third-derivative
term cannot be silently deleted. These identities are validated as operator
identities for arbitrary g, not just for the saved physical graph vectors.

## 4. Separate the clock gradient from discrete compatibility

Let c=N sqrt(F), m=R^2/c, p=R^2 c, theta=c_t/c. Define on open partition cells

    r_u=-(p_R/m)u_R-c^2 u_RR,
    zeta_g=-c^2 theta_R u_R,
    kappa_g=theta r_u+zeta_g.

The exact free-row identity is

    Cg=Pi kappa_g+M^-1(K_Gram,t u)_I+quadrature remainder.

The full raw trace of kappa_g is NOT simply the gradient trace. It includes
theta(e) r_u(e), whose endpoint curvature is governed by section 3. Moreover,
for a spatially constant theta with the same Gram rate, K_t=theta K and
C=theta I EXACTLY. Our manufactured constant-clock controls nevertheless
have nonzero raw kappa trace. Its artificial decomposition pieces cancel in
the full projected, Gram and quadrature expression.

Consequently subtracting the whole raw trace is not the cleanest correction:
it changes a constant-clock energy estimate which was already exact. Instead
define the specific clock-gradient trace operator

    T=-diag(c(e)^2 theta_R(e)) E_R U,

where E_R is the two-endpoint derivative evaluation on the actual free cubic
space. Thus T g=zeta_g at the endpoints. It vanishes identically for a
constant clock. The discrete compatibility terms are RETAINED, not assumed
to vanish or to have a uniform estimate that has not been proved.

Set D0=D_g-B T. This definition is exact even before a regularity theorem for
D0 is established. It is not a claim that every possible irregular boundary
effect has now been removed.

## 5. The cancellation that makes the correction usable

Differentiate the actual elliptic inverse at fixed coefficient coordinates:

    U_t=-K^-1 K_t U+K^-1 M_t=-U D_g.

Let d_e=c(e)^2 theta_R(e). Then

    T_t=-diag(d_e,t) E_R U-T D_g,
    S := T_t+T D_g=-diag(d_e,t) E_R U,
    d_e,t=c(e)^2 [2 theta(e)theta_R(e)+theta_tR(e)].

This removes D_g from the differentiated feedback, without using a
pointwise endpoint equation. For sigma_g=Tg the exact time law is

    sigma_g,t=T h+S g+T b.

It needs neither g_RR at the endpoint nor a third metric time jet.

The mixed derivative is explicitly sourced. At an endpoint use one-sided
radial derivatives of the original PL fields, D=R-2mu and D_R=1-2mu_R:

    theta_tR=N_ttR/N-N_tt N_R/N^2
       -2(N_t/N)(N_tR/N-N_t N_R/N^2)
       -mu_ttR/D+mu_tt D_R/D^2
       -4mu_t mu_tR/D^2+4mu_t^2 D_R/D^3.

The saved second metric jet supplies N_tt, mu_tt and their reconstructed
spatial slopes. Independent complex-step differentiation checks both this
formula and T_t on every saved state and manufactured control. Uniform
propagation of these sourced quantities from the parent equations remains a
separate obligation; availability at a snapshot is not such a proof.

## 6. Explicit invertible normal form; no discarded boundary energy

Define an ANALYSIS variable, not a new physical field,

    w=h+B T g.

The inverse is h=w-B T g, with no smallness condition. Direct differentiation
using section 5 gives

    g_t=w+D0 g+b,
    w_t=-L g+(D_h+B T)w+H g+r+B T b,
    H=F_B T+B S-B T B T.

The derivative B_t, every Gram term and the entire external source survive.
In particular, the term B T b must not be dropped. The previously derived
external boundary source B beta still appears in the g equation: this
normal form does not replace its boundary-memory/BV argument.

Set E_N=(g^T K g+w^T M w)/2. The principal mixed work still cancels exactly:
g^T K w-w^T K g=0. The remaining exact energy law is

    E_N'=g^T[sym(K D0)+K_t/2]g
         +w^T[sym(M(D_h+B T))+M_t/2]w
         +w^T M H g+g^T K b+w^T M(r+B T b).

This is checked against the full time-dependent block similarity transform
and against the derivative of the pullback energy in the original (g,h)
coordinates. The correction is therefore not a reduction obtained by
throwing away positive energy or a boundary source.

## 7. Conditional mesh-independent feedback estimates already derived

Use the inherited elliptic bound, valid for both branches,

    ||(U g)_R||_infinity <= Dinf ||g||_M.

At the two endpoints set

    t_star=Dinf |d_e|_2, s_star=Dinf |d_e,t|_2,
    rho=length sqrt(m_max/p_min), b_star=sqrt(m_max length/2),
    f_star=the preceding explicit bound for ||F_B||_(R2 to M).

Then the following follow directly, without an inverse mesh factor:

    ||T||_(M to R2)<=t_star, ||S||_(M to R2)<=s_star,
    ||g||_M<=rho ||g||_K,
    ||B T||_(K to M)<=a_star=b_star t_star rho,
    ||H||_(M to M)<=h_star=f_star t_star+b_star s_star+b_star^2 t_star^2.

Both energy norms are comparable:

    sqrt(E_N)<=(1+a_star)sqrt(E_H),
    sqrt(E_H)<=(1+a_star)sqrt(E_N).

This uses the triangular transform and its inverse, not an absorption
requiring a_star<1. If Gamma0 is an established bound for the paired forms
with D0 and D_h, the normal-form homogeneous growth is bounded by

    Gamma_N <= Gamma0+2 b_star t_star+rho h_star.

The force contribution is bounded by

    sqrt(2 E_N) sqrt(||b||_K^2+||r+B T b||_M^2).

The code checks this expression using the measured finite-mesh Gamma0.
It does NOT thereby establish a mesh-uniform Gamma0. Likewise t_star and
s_star are uniform only if their sourced coefficient/jet inputs are uniform;
f_star retains the previous clock-curvature/jump hypothesis. The evaluated
upper bounds are conservative analytic expressions in floating point, not
interval-certified enclosures.

## 8. What the controls and actual states say

The manufactured controls prescribe coefficient jets in the original FE
spaces; they are not extra parent-constrained trajectories. Use mu=1, N=.82,
N_t=N theta, all other first and second packed time jets zero. For a constant
theta=.001, T=S=0 and Gamma_N=Gamma_H=.005 in both branches. The corrected
energy does not introduce a fake endpoint correction into this exact case.

For the spatially linear theta=.001(R-6):

|Intervals|GR old growth|GR normal growth|Gram old growth|Gram normal growth|
|---|---:|---:|---:|---:|
|16|.000903534|.000799615|.000905404|.000801519|
|32|.001042713|.000803108|.001045636|.000803830|
|64|.001251636|.000804703|.001256405|.000804925|
|128|.001568618|.000805468|.001576036|.000805529|

The corrected rates are much less refinement-sensitive on these four meshes.
This supports the proposed energy organization, not a proof of all-mesh
boundedness, physical stability or convergence. Quadratic PL-clock controls
retain their nonzero spatial derivative jumps and also pass the identities.

The actual saved t=.01 states are less tidy, and must also be reported:

|Intervals/branch|Old growth|Normal growth|Derived norm-comparison factor upper|
|---|---:|---:|---:|
|16 GR|.000170943|.000165270|1.00246610|
|16 Gram|.000203418|.000261683|1.00356608|
|32 GR|.000205529|.000218391|1.00057817|
|32 Gram|.000207261|.000292720|1.00060442|
|64 GR|.000236055|.000235703|1.00051186|
|64 Gram|.000240158|.000338923|1.00129726|

Some normal-form rates are HIGHER, particularly Gram. The mixed clock jet
and its cross work have not been erased to manufacture an improvement.
These are instantaneous rates of different, explicitly comparable energies,
not new physical trajectories or changed empirical predictions.

At N64 the actual shear norms are about 6.06e-7 GR and 1.19e-6 Gram. The
conservative derived bounds are about .000512 and .001297. The conditional
additional growth upper bounds over Gamma0 are much looser, about .209 and
1.90 respectively. Do not substitute measured small rates for those bounds.
The external source norm remains about 5; it was not solved by this shear.

## 9. Precise next derivation, now downstream of an actual construction

The next target is a mesh-uniform H1 estimate for D0, not another search for
an unspecified endpoint correction. There is an exact decomposition:

    D0 g=-2A g+Pi(zeta_g-ell_map T g)+E g,
    E=C+A-Pi zeta_map.

The first term already has the inherited zero-trace multiplication/projection
bound. The second has zero endpoint trace but may have INTERNAL VALUE jumps:

    [zeta_g]=-c^2 (U g)_R [theta_R].

Retain those jumps; zero endpoint trace does not alone justify applying an
H1 theorem for continuous functions. Their weighted radius is directly
connected to the already sourced clock-gradient jump radius.

The last term is the exact weak compatibility/Gram/quadrature remainder,
saved as a matrix in every new artifact. It is not set to zero. A useful
starting identity for a free test v is, with z=Pi(theta v),

    (v,E g)_M=Q[p (U g)_R (theta v-z)_R]
               +a_Gram,t(U g,v)-a_Gram(U g,z).

Indeed z belongs to the actual free space, its weak equation is available,
and weighted projection orthogonality kills Q[m g(theta v-z)]. This identity
points to a discrete multiplication/elliptic commutator estimate rather than
the invalid pointwise substitution r_u=g at the endpoint.

Once Gamma0 is derived, the present explicit normal form already shows how
to add its genuine feedback without a new unknown state derivative. Parent
clock/second-jet propagation, external beta variation, regular source bounds,
energy propagation and box persistence then remain. There is no new physical
long run, local-GR pass, nonlinear/DAE closure or horizon claim here.

## 10. Reproducibility and preservation

- `scripts/annular_homogeneous_trace_feedback_20260910.py`
- `scripts/derive_annular_homogeneous_trace_feedback_20260910.py`
- `scripts/explore_annular_trace_feedback_20260910.py`
- `source-intake/navier-stokes/20260910/annular-homogeneous-trace-feedback-derived/status.json`
- `source-intake/navier-stokes/20260910/annular-homogeneous-trace-feedback-final-integrity.json`

The formal derive runner completed at 2026-09-10T01:14:39Z. Its derive phase
requires a fresh destination; use a new attempt identifier for any rerun,
never overwrite completed evidence. Seal only after the note and resume are
ready. The final seal owns a resume snapshot and all inherited input/output
hashes. The exploratory script has no authority to certify evidence.

Validation includes actual released-slope matrix rows, exact symbolic slope
moments, independent complex-step derivatives, operator reconstruction,
conditional feedback bounds, invertible block transformation, source
retention, pullback energy differentiation and GR/MTS control comparisons.

All inherited trajectories remain hash-identical. Compilation uses no
bytecode cache. One single-core BelowNormal Python worker at a time with
BLAS/OMP threads set to one; no subagents, shared-process shutdowns, Git action
or edits to the frozen workbench. Protected verification is an mtime scan
since 2026-09-10T00:59:00Z, not a full pre-turn hash baseline.
