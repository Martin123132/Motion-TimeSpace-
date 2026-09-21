# Time-dependent force adjoint and nonlinear relative energy

2026-09-17. Private continuation of
`DERIVATION-20260917-finite-width-curvature-and-coupled-energy.md`.

## 1. Scope

The original prescribed-flat-background spherical action, both reference and
MTS branches, all Gram rows, source motion and passive clock are retained.
No field equation, force or published file is changed. The aim is an actual
signed response calculation and a nonlinear energy argument, not another
list of missing coefficients. This is not the full GR limit.

All planned backward calculations and their independent forward comparisons
are complete. The current suite has 290 successful implementation checks.
These check the stated identities and numerical protocols, not the full
physical theory. Three independent spectral-reference accuracy comparisons
fail their old control threshold and are retained explicitly in section8.

## 2. A matrix-free adjoint of the unchanged coupled flow

Let z(t) be the same cubic-Hermite GR-driven reference used previously,
A(t)=DF_h(z(t)), r(t)=F_h(z(t))-zdot(t), and eta(0) the original retained
initial projection error. The existing forward correction solves

    eta' = A eta+r.

For a specified terminal force f at T, define g=Df_h(z(T)) and solve

    -q'=A^T q,    q(T)=g^T.

Then, exactly for the continuous finite-dimensional equations,

    f_linear(T)-f_GR(T)
      = [f_h(z(T))-f_GR(T)] + q(0)^T eta(0)
        + integral_0^T q(t)^T r(t) dt.                   (1)

This is an independent backward calculation of the existing forward linear
response, not a new nonlinear trajectory or a fitted correction to a force.

The transpose is derived from the implicit acceleration equation

    H(z) a(z)=R(z),
    Da=H^-1 [DR-(DH)a].

For an acceleration covector l, first solve H k=l using the original banded
field mass and scalar kinetic Schur complement. Apply [DR-(DH)a]^T k by
banded matrix products and the sparse lifted Gram factor. Include the identity
coordinate-to-velocity block and the derivative of sqrt(1-V^2) for clock.
No dense Jacobian, truncated eigenbasis or omitted source row is needed.
Force gradient includes the derivative of the material inertia as well as
the source acceleration derivative.

The implementation is independently checked against the older dense analytic
Jacobian, complex directional derivatives, and the canonical energy map on
both branches. This avoids assuming that forward and backward code share a
correct transpose merely because they use the same equations.

## 3. Canonical conversion does not discard the reference defect

Write T for the derivative of the kinetic Legendre map. In canonical variables
the linear generator is Ac=JQ-B_r, with

    B_r=(DT[r])T^-1.

This term is necessary because the reconstructed reference is not an exact
solution of the finite action. Evolving q in velocity coordinates and defining

    p=T^-T q

retains it automatically: -p'=Ac^T p. The qualifier checks this identity,
including an arbitrary clock covector. The terminal force has no clock
dependence, so its clock covector stays zero in the response calculation.

For the MTS branch, split the same-state reference defect as

    r_MTS = r_reference + (F_MTS(z)-F_reference(z)).

Reference and MTS have the same kinetic Legendre map. With G the full lifted
Gram factor and a=G U, the extra canonical forcing is

    T(F_MTS-F_reference)=(0, -G^T D a, -a^T D_b a/2).

Thus its signed adjoint density is exactly

    rho_Gram = -(G p_PU)^T D a - p_Pb a^T D_b a/2.        (2)

The remaining density is rho_base=q^T r_MTS-rho_Gram. These are integrated
alongside q, separately from their absolute values. Absolute integrals are
numerical diagnostics, not interval-certified upper bounds. The MTS and
reference adjoints are DIFFERENT; subtracting their two Gram integrals is
not in itself a full comparison of evolved branches.

The finite-width curvature identity from the preceding checkpoint can be
inserted into a in (2). This expresses the forcing through interval curvature
while retaining its signs and phases, without replacing the original action.

## 4. A reduced Hamiltonian with uniformly controlled derivatives

The previous basic-energy bound on D2F loses a derivative at high frequency.
The nonlinear route here instead keeps the principal Hamiltonian in a relative
energy. This requires a bound on D3H, NOT a uniform bound on D2(J grad H) as a
map from the basic energy space to itself.

In canonical coordinates X=(U,b,P,p_b), set

    c=A(b)U,
    d=U^T B U-c^T M^-1 c >= 0,
    ell=p_b-c^T M^-1 P,
    phi(ell,d)=sup_{|V|<1} [ell V-d V^2/2+m sqrt(1-V^2)].

The maximizer is unique because

    ell=d V+m V/sqrt(1-V^2),
    s=d+m/(1-V^2)^(3/2) >= m>0.

The exact Hamiltonian is

    H(X)=P^T M^-1 P/2+U^T K U/2+phi(ell,d).              (3)

Equivalently phi=d V^2/2+m/sqrt(1-V^2) at the maximizer.
No coupling is added in writing (3); it is the Legendre transform of the same
action. The numerical inverse solves only this monotone scalar equation.

For a direction (delta ell,delta d), put a=delta ell-V delta d. Then

    Dphi=V delta ell-V^2 delta d/2,
    D2phi=a^2/s,
    D3phi=-3 delta d a^2/s^2-mu_V a^3/s^3,
    mu_V=3m V/(1-V^2)^(5/2).                            (4)

Mixed third derivatives follow by polarization. These derivatives are bounded
on a bounded energy neighborhood away from |V|=1, with constants independent
of mesh size because s>=m. The qualifier symbolically checks the last identity.

Choose a fixed canonical energy norm ||.||_* consisting of a reference H1
field norm, mass-dual L2 momentum norm, and the two scalar source components.
On uniformly nondegenerate source maps, the matrix forms and their b
derivatives through third order have mesh-independent bounds in these norms.
The lifted Gram form is H1-bounded by the previous endpoint/mesh estimates.
M^-1 and its b derivatives have corresponding mass-dual bounds. Consequently
d and ell in (3) are bounded smooth quadratic/bilinear forms on bounded
energy neighborhoods. Equations (3)-(4) give a uniform C3 bound for H there.

This statement is about the Hamiltonian functional on the energy space.
It does not say its vector field is uniformly C2 in that space: J sends
energy-dual gradients to the evolution space with an unbounded spatial
principal operator. That distinction is exactly what the previous
high-frequency mixed-derivative test exposed in both branches.

## 5. Exact nonlinear relative-energy identity

Let X(t) be an exact canonical solution and Y(t) the canonical image of an
arbitrary reference path. Write

    F_c=J grad H,   R_c=F_c(Y)-Ydot,   Delta=X-Y,
    Q(Y)=Hessian H(Y),   W_beta(Y)=Q(Y)+beta e_b e_b^T.

For one constant beta define

    E(X|Y)=H(X)-H(Y)-grad H(Y)^T Delta+beta(Delta b)^2/2. (5)

The beta term is only a comparison-energy shift, NOT an additional force.
Direct differentiation and antisymmetry of J give the exact identity

    E'=[grad H(X)-grad H(Y)-Q(Y)Delta]^T F_c(Y)
        + beta Delta b [V(X)-V(Y)]
        + Delta^T W_beta(Y) R_c.                        (6)

The high-frequency principal evolution of the perturbed solution cancels;
it is not estimated by ||D2F||. The first term is exactly

    integral_0^1 (1-s) D3H(Y+sDelta)[Delta,Delta,F_c(Y)] ds.

The energy itself is exactly

    E=integral_0^1 (1-s) Delta^T W_beta(Y+sDelta)Delta ds. (7)

Thus no nonlinear Taylor remainder has been discarded. The tests compare
(5), (6), (7), independently differentiated time evolution, and two orders
of segment quadrature after the scalar inverse Legendre solve.

### Conditional nonlinear estimate

Suppose the relevant canonical segments lie in a bounded nondegenerate
timelike neighborhood with one beta satisfying

    m0 ||z||_*^2 <= z^T W_beta(X_s) z <= M0 ||z||_*^2,
    ||D3H(X_s)|| <= C3,   ||F_c(Y)||_* <= L_F,
    ||DV(X_s)|| <= L_V,                                 (8)

uniformly in h and time. The coercivity route is the previous kinetic and
coordinate Schur complements. In particular beta must exceed their source
threshold throughout this neighborhood, not merely at three sampled times.
Uniform C3 follows as above; F_c(Y)'s energy norm requires strong enough
regularity of the REFERENCE path, including its field acceleration in L2.

Equations (6)-(8) imply

    E' <= [(C3 L_F+2 beta L_V)/m0] E
           + M0 sqrt(2E/m0) ||R_c||_*,

and, for r_E=sqrt(2E),

    r_E' <= [(C3 L_F+2 beta L_V)/(2m0)] r_E
             + (M0/sqrt(m0)) ||R_c||_*.                 (9)

This provides a conditional NONLINEAR stability estimate without the invalid
uniform basic-energy Hessian bound on F. If the initial energy error and the
integrated canonical residual vanish uniformly and the neighborhood bootstrap
holds, (9) yields energy convergence on the chosen finite interval.

It does not prove continuum existence, the common regularity bounds,
vanishing total GR-reference residual, or the neighborhood bootstrap for MTS.
Nor does energy convergence alone prove instantaneous source-force convergence:
the force trace still has the sensitivity identified previously. Source
position/speed and the passive clock are lower-order observables; their
continuity follows inside the coercive timelike neighborhood. No claim that
these hypotheses are already established for the complete parent theory is made.

## 6. Numerical protocol

### Initial-corner obstruction and a weaker spatial-consistency route

The original benchmark data are not C2-compatible at the initial moving
source corner. This is an identifiable issue in the shared reference data,
not an MTS-only test failure. The initialization in
`scripts/run_annular_dense_GR_references_20260916.py` uses the unchanged
profile from `scripts/run_annular_source_fitted_crossing_20260915.py`:
near b0=6.03, U=.01(r-b0), phi_t=-.06 phi_r, with V0=.06.
The equal two-sided gradients give zero initial source acceleration.

Hence at that corner, phi_rr=phi_tr=a_b=0 and phi_r=.01. The radial wave
equation and twice differentiated moving Dirichlet condition would require

    0=phi_tt+2V phi_tr+V^2 phi_rr+a_b phi_r
     =2 phi_r/b0=2/603=0.0033167495854063,

which is impossible for a C2 solution extending to the corner with all
those initial traces. Position and first derivative compatibility are not
the problem. This does NOT prove nonexistence of a weaker or piecewise-smooth
solution, nor does it invalidate every saved finite calculation. It does mean
that global classical C2 regularity up to t=0 cannot simply be assumed.

There is a constructive extension of the spatial estimate. Suppose U-j1 x_+
is C1 with uniformly bounded piecewise curvature, and has at most J curvature
fronts in addition to the source; between fronts use a common modulus omega.
Away from front-crossing stencils, |D3 U|<=h^2 omega(h). On each exceptional
stencil the double-integral identity gives |D3(U-j1 x_+)|<=2 M2 h^2.
At most4(J+1) stencils are exceptional, even when fronts align with vertices.
Without continuity of curvature within the small source elements, the exact
trace kernel still gives |J_h U-j1|<=M2(ell_-+ell_+)/3. Therefore

    ||Gtilde U|| <= C[h^(3/2) omega(h)+h^2 M2 sqrt(J+1)]. (10)

The full extra canonical forcing, not only its material-force component,
has energy norm bounded by

    C[h^(-3/2)||Gtilde U||+h^(-1)||Gtilde U||^2].          (11)

Here the momentum block uses M^-1/2, the bounded Euclidean lifted factor and
D=O(1/h); the source block is quadratic. Equations (10)-(11) imply vanishing
extra forcing for fixed J and a common modulus, including fronts that move
through the source cells. This avoids demanding an impossible smooth initial
corner while preserving the action. It is still conditional on an actual
reference solution having bounded curvature and finitely many such fronts.

Seven meshes33..2049 and five manufactured front placements per mesh satisfy
the explicit bound, including fronts coincident with the source. The count
and regularity of fronts in the ACTUAL reference solution remain to be proved.
No old initial data have been changed to make a test pass.

### Adjoint and nonlinear qualification

The transpose qualification uses grids33/129, both branches, and GR degree768
at times0,.21,.4. A NEW small33/8 forward/backward duality test uses T=.05;
it is not falsely described as a previously existing prediction.

Only after that qualification, the513/8 full interval[0,.4] is integrated
backward, with terminal force at T=.4. A tighter run reduces tolerances by100
and the maximum step by2. Reference interpolation and terminal observable
are identical. Neither runner may open the old forward predictions or finite
future trajectories. The validator freezes and hashes both adjoints before
opening the already completed forward linear response.

The comparison is for ONE terminal force at T=.4, not every time sample or
the maximum force error. Gates:duality2e-9, signed-term/total control2e-10.
Original physical force gate2e-7 is not upgraded by a duality pass.

The nonlinear test uses both branches, grids33/65/129/257, T=.21 reference
states, high-frequency unit-energy field perturbations and source motion,
at amplitudes1e-4 and5e-5. A positive sampled segment is NOT proof of positive
coercivity over a whole nonlinear neighborhood.
Additional derivative-only manufactured probes make the reference position
and velocity defects explicitly nonzero; they test the residual term in (6)
without changing any physical trajectory or input file.

## 7. Results

### Adjoint comparison

The full513/8 backward integrations cover[0,.4], with force observed atT=.4.
Both branches complete at standard and tighter settings. All four prediction
packs were frozen and hash-verified before the validator opened the saved
forward linear responses; the forward and finite nonlinear trajectories were
not re-evolved. This is independent computation of a KNOWN benchmark, not a
blind empirical prediction.

|Branch|Tighter backward linear force difference from GR reference|Saved forward linear difference|Absolute duality error|
|---|---:|---:|---:|
|Reference|+2.25918252837e-7|+2.25918247093e-7|5.74373296e-15|
|MTS|-2.30033007567e-6|-2.30033285586e-6|2.78018924e-12|

The largest absolute duality error across both settings and both branches is
2.78018924e-12, below the declared2e-9 numerical gate. Tightening tolerances
by100 and halving the maximum step changes the total result by4.14720044e-15
for reference and1.74253691e-13 for MTS. The largest signed-term change is
1.75959742e-13, below the separate2e-10 control gate. The small33/8 forward-
backward tests also pass at both settings; no small test is substituted for
the full-time513/8 comparison.

For MTS the tighter signed decomposition is

    instantaneous terminal defect    +4.130199905683714e-5
    propagated initial mismatch     -4.051607473096240e-9
    base-reference residual         -3.986903805042241e-7
    extra Gram residual             -4.319958714453455e-5
    total                           -2.300330075674728e-6.

This exhibits cancellation inside the unchanged coupled linear response.
It does NOT subtract an error from the original nonlinear force or make its
physical gate pass. The MTS absolute Gram integral is about.13637236, far
larger than its signed value; its standard-to-tight change is3.68884806e-5.
Accordingly absolute-integral diagnostics are not reported as tightly
converged or interval-certified stability bounds. Signed-term controls and
absolute-integral accuracy are distinct questions.

The result qualifies one terminal linear observable, not the entire force
curve, the nonlinear remainder, uniform mesh stability or the full GR limit.
The old spectral-reference discrepancy identified in section8 is an
additional, separate reference-accuracy issue: the duality comparison here
deliberately retains the SAME old Hermite reference on both sides.

### Nonlinear relative energy

All16 nonlinear relative-energy cases complete: two branches, four grids,
two perturbation amplitudes. The explicit inverse Legendre transform, reduced
Hamiltonian value, nonlinear time-rate identity, nonzero reference-position
defect, third-Hamiltonian contraction and independent4/8-point segment
quadratures pass their separate implementation gates. Tested frequencies
range approximately3.07e3..7.86e4 without the previous mixed-D2F blowup in
the corresponding homogeneous energy-rate probes.

These are prescribed directions, NOT the maximum growth rate over all
perturbations. In particular the chosen source displacement and speed
perturbations have opposite signs, so negative homogeneous rates must not be
described as a damping theorem. Raw energy rates can be positive and much
larger because the actual reference forcing remains present. No uniform
neighborhood, total-residual or instantaneous-force certificate is inferred
from these sampled checks.

## 8. Constructive continuum-reference reduction

For the flat spherical reference, put chi=r phi. Direct differentiation gives

    chi_tt-chi_rr=r(phi_tt-phi_rr-2 phi_r/r)=0.

Thus chi=F(t-r)+G(t+r). At the moving Dirichlet source,
(1-V)F'+(1+V)G'=0. On the left F is incoming; on the right G is incoming.
Until an incoming source characteristic reaches an outer boundary, its initial
feet are r_-=b-t and r_+=b+t. With the ORIGINAL phi_0 and
phi_t,0=-V0 phi'_0, V0=.06, the exact source gradients are

    H_-=[phi_0(r_-)+(1+V0) r_- phi'_0(r_-)]/[b(1+V)],
    H_+=[phi_0(r_+)+(1-V0) r_+ phi'_0(r_+)]/[b(1-V)].    (12)

Consequently the original continuum-reference source equations reduce to

    b'=V,
    V'=b^2(1-V^2)^(5/2)(H_-^2-H_+^2)/(2m),
    clock'=sqrt(1-V^2).                                 (13)

No spectral field grid, fitted coefficient, MTS force replacement or
altered initial data enters (12)-(13). This reduction is exact for this flat
spherical reference before incoming outer-boundary returns; its numerical
solution is NOT a closed-form trajectory or a solution of full GR/MTS.

### The domain restriction can be justified, not merely sampled

The reference scalar-plus-source continuum energy is

    E=m/sqrt(1-V^2)+integral r^2(phi_t^2+phi_r^2)/2 dr.

Outer Neumann flux is zero. The two source-side field-energy fluxes sum to
-V F_source, while material energy changes by+V F_source. Curvature jumps
with continuous first derivatives add no shock-energy term. Thus the
energy-conserving continuum branch has conserved positive E.

Exact polynomial integration of the unchanged piecewise-quintic initial
profile gives

    E_field,0=944767173293/441000000000000
             =0.00214232919114059,
    E_source,0=3 sqrt(2491)/4982,
    E_total,0=0.0321964754299229 < 41/1000.

The rational inequalities E_field,0<.01, E_source,0<.031 and
(41/1000)^2 < m^2/(1-(3/4)^2) certify |V|<3/4 on this continuum branch.
Therefore through T=2/5,

    b0-(1+3/4)T <= b-t <= b+t <= b0+(1+3/4)T,
    5.33 <= r_- <= r_+ <= 6.73,

strictly inside [5.2,6.8]. Incoming source characteristics have no outer
reflection in this horizon. This analytic energy gate is stronger than the
sampled ODE speed/domain check; it is not an interval certification of the
numerical trajectory, nor of the finite spectral references.

Equation (13) has a locally C1 right-hand side on this compact timelike
domain, because phi_0 is C2. The energy/domain bootstrap excludes a source
ODE escape before T=.4 on the energy-conserving branch. The corresponding
characteristic reflection construction supplies the continuum local field.
An implementation of the COMPLETE field reconstruction, with independently
qualified bulk derivatives and residuals, is still outstanding.

### Actual initial-front amplitudes

At the initial source, F''=.01(1+V0/2), G''=.01(1-V0/2).
The second boundary identity is

    (1-V)^2 F''+(1+V)^2 G''+a_b(-F'+G')=0.

With a_b(0)=0, the outgoing corrections required to close the initial corner
are exactly

    Delta G''_left=-.02/(1+.06)^2=-50/2809,
    Delta F''_right=-.02/(1-.06)^2=-50/2209.              (14)

They propagate on r=6.03-t and r=6.03+t, respectively. Since chi and chi_r
are continuous, the corresponding phi_rr jumps are (14) divided by the front
radius. These are derived jump amplitudes for the original reference, not
free front parameters. The two source-emitted fronts stay inside the outer
boundaries over this interval. Away from them, incoming C2 data and the
timelike reflection map give bounded continuous curvature locally; the
profile transitions can affect higher derivatives without introducing an
additional initial curvature discontinuity. Full uniform reconstruction
bounds should be made explicit before substituting this reference into the
nonlinear convergence estimate.

### Independent source comparison

Both three-variable integrations complete throughT=.4, with tolerances
2e-12 and2e-13 and maximum step.001. Their mutual state/force controls pass.
The old spectral reference is only opened AFTER the characteristic prediction
is saved. Maximum force differences over81 times are:

|Old GR reference degree|Difference from characteristic source|
|---|---:|
|384|8.21990402e-8|
|512|3.68917356e-8|
|768|2.43550942e-8|

All three exceed the previous2e-8 reference-control threshold, including768
by a small margin. They are recorded as comparison failures, not hidden among
successful implementation checks. AtT=.4, degree768 minus the characteristic
force is+6.63028992e-9. This does not explain away the much larger original MTS
force discrepancy, and no old physical gate is upgraded here.

The force discrepancy decreases with reference degree, but position errors
are not monotone. A tight time-step control on one spatial reference was not
sufficient to establish its force accuracy against this independent route.
The new comparison justifies reconstructing the full characteristic reference
and reusing saved finite trajectories against it, rather than launching another
large grid or treating the spectral reference as infallible.

## 9. Explicit starting formula for full-field reconstruction

The next stage need not rediscover the incoming primitives. Put
I(r)=integral_{b0}^r phi_0(s) ds and choose F_0(-b0)=G_0(b0)=0. Then

    F_0(-r)=[(1+V0)r phi_0(r)-V0 I(r)]/2,
    G_0(r)=[(1-V0)r phi_0(r)+V0 I(r)]/2.                (15)

Both are explicit piecewise polynomials for the original profile. On the left,
the source-reflected branch satisfies G(v)=-F_0(tau-b(tau)), where
v=tau+b(tau). On the right, F(u)=-G_0(tau+b(tau)), where u=tau-b(tau).
These retarded maps are strictly increasing, with derivatives1+V and1-V
bounded below by1/4 on the energy-gated domain. Distinguish the initial and
reflected pieces at the two initial-source fronts; do not smooth over them.

The COMPLETE spatial domain can already contain outer-reflected radiation
even though none reaches the source byT=.4. Therefore do not use initial
incoming functions outside their initial domains. At the fixed left outer
radius a=5.2, Neumann phi_r=0 becomes the Robin relation chi_r=chi/a:

    F'(u)+F(u)/a=G'(u+2a)-G(u+2a)/a.

At the right outer radius c=6.8 it gives

    G'(v)-G(v)/c=F'(v-2c)+F(v-2c)/c.                   (16)

These are scalar boundary equations, not naive odd/even reflection of chi.
The original data vanish near both outer boundaries, fixing compatible
initial constants. Implementing and qualifying (15)-(16), the retarded source
branches, bulk derivatives, boundary conditions and source force is the NEXT
task. These full-field formulas have not yet been numerically qualified in
this checkpoint. Once qualified, recompare the already saved finite
trajectories and then prove the base Galerkin residual estimate under the
derived piecewise-curvature structure. Do not rerun large forward trajectories.

Implementation:

- `scripts/annular_matrix_free_adjoint_20260917.py`
- `scripts/qualify_annular_matrix_free_adjoint_20260917.py`
- `scripts/prepare_annular_small_adjoint_20260917.py`
- `scripts/run_annular_force_adjoint_20260917.py`
- `scripts/validate_annular_force_adjoint_20260917.py`
- `scripts/annular_relative_hamiltonian_20260917.py`
- `scripts/qualify_annular_relative_energy_20260917.py`
- `scripts/qualify_annular_curvature_fronts_20260917.py`
- `scripts/derive_annular_characteristic_source_20260917.py`
- `scripts/derive_annular_characteristic_energy_gate_20260917.py`
