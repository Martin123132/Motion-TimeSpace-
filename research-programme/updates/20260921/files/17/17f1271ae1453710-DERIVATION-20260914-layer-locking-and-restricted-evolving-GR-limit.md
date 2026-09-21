# Layer locking and a restricted evolving GR-limit argument

2026-09-14. Private work in post-checkpoint-work only.
No GitHub action, subagents, protected-workbench edits, or external physical claim.

## 1. What this adds

The previous checkpoint identified a candidate continuum problem but assumed
sufficiently strong convergence to pass its quadratic stress. This note supplies
a route to that convergence using the ACTUAL reference equations:

- switch to scalar velocity and transmitted force;
- prove synchronization of the regulator's internal layers before taking a limit;
- obtain spatial compactness from the cumulative force equation;
- pass the quadratic energy without inserting a bulk defect tensor;
- retain the thin reservoir and its midpoint clock;
- use uniqueness to identify the entire reference sequence, then transfer the
  limit to the MTS sequence using the preceding relative-energy theorem.

This is a paper-level derivation for the specified stationary-source, spherical,
regular annulus and the existing smooth compact preparation. It inherits the
explicit analytic bounds in the cited predecessors. It is not a formally
machine-verified proof, an unrestricted parent-action theorem, a horizon result,
a cosmological or observational result, or a practical numerical error bar.

In particular, the two notions below must stay separate:

    restricted short-time convergence argument derived: yes, as specified here;
    unrestricted/full GR limit or physical theory pass: no.

The computations check finite-dimensional identities and estimates. They cannot,
by a count of successful tests, certify the compactness/uniqueness proof itself.
Independent mathematical scrutiny of this chain remains appropriate.

## 2. Exact system, hypotheses and inherited constants

Sources:

- `DERIVATION-20260914-live-constrained-mass-relative-energy.md`
- `DERIVATION-20260914-reference-wave-boundary-decoupling.md`
- `DERIVATION-20260914-reference-continuum-and-source-shell.md`
- `scripts/annular_compatible_h_evolution_20260914.py`
- `scripts/annular_horizontal_clock_evolution_20260913.py`

Keep the existing fixed annulus [5,6], spacing h, collar width h/2,
W(z)=6(z+1/2)(1/2-z), and normalized layer measure dmu=W dz.
The right scalar is zero, its reservoir S=0.003 is stationary, and the physical
clock is N/U=1 at the collar midpoint b=6. The left mass seed is 0.8.
All field comparisons below use the common base nodes R_i; actual metric
samples remain R_i+(h/2)z. This O(h) shift is not a change of the equations.

Let

    Fgeom = 1-2m/R, U=sqrt(Fgeom), L=NU,
    a_i=L_i/R_i(z)^2,
    c_i=[R_i(z)^2 L_i + R_(i+1)(z)^2 L_(i+1)]/2,
    u_i=(chi_(i+1)-chi_i)/h,
    q_i=chi_t,i=a_i p_i,
    f_i=c_i u_i.

Here f_i is transmitted scalar force, not the metric Fgeom.
Free nodes are i=0,...,n-2. There are n-1 edges. Set q_(n-1)=0 and f_(-1)=0.
The weights are omega_0=h/2, omega_i=h otherwise on the free set.

Inherited uniform bounds, valid along exact solutions while they exist:

    E0(Y)<=Ebar=2.08222448216064,
    E_V=E0(Y_t), E_A=E0(Y_tt),
    Q >= E_V^2 + mu E_A/2,   mu=0.11925180874784208,
    sup_(t<=T) [E_V(t)+Q(t)] < infinity
        for each fixed T < tstar=0.0008345769328864052.

The time is in PILOT units, not seconds. The last bound follows from the
previous tangent comparison and higher-energy differential inequality, with
the actual smooth initial preparation. It is not assumed for arbitrary data.

Use common bounds r=4.9, Rmax=6.1, Mstar=0.9292469107643997, f=0.5,

    Lmin=0.459221543661712, Lmax=1.0887990925101885,
    amin=Lmin/Rmax^2, amax=Lmax/r^2,
    cmin=r^2 Lmin, cmax=Rmax^2 Lmax.

Neither the mass density's pointwise supremum nor its spatial derivative is
assumed uniform in h.

### 2.1 Closing the fixed-h continuation qualification

This is a statement about the EXACT regulator with continuous layer label,
not about a polynomial time integrator.

For fixed positive h, the radial constraint map is locally Lipschitz on
continuous layer profiles within a uniformly regular chart. Collar evaluation,
finite matrices, and the regular radial ODE define a locally Lipschitz vector
field on C([-1/2,1/2];R^(2n-2)). Constants may depend on h.

The earlier exact identity Y_t=g J DH, with H=m(B_h)/kappa and fixed reservoir,
gives H_t=0 for each branch. Positivity then keeps its full mass, Fgeom, L and
total scalar energy inside the stated uniform chart bounds.

At fixed h, the scalar equations have bounded linear coefficients conditional
on the live metric:

    ||chi_t||_infinity <= amax ||p||_infinity,
    ||p_t||_infinity <= C_h ||chi||_infinity.

For the reference C_h can be bounded by 8 cmax/h^2; the finite positive-Gram
stiffness also has a finite C_h. Its dependence on the state enters only through
the already bounded metric coefficients. Thus Gronwall prevents finite-time
divergence of these profile suprema at fixed h. Source and inner clocks have
bounded rates. The regular radial map stays a positive distance from chart
degeneracy, so the local solution can be continued.

This removes a common-time existence obstruction for these exact fixed-h
stationary regulators. It does NOT give a uniform continuum estimate for all
time: the profile bound may grow like exp(C_h t), and only the preceding
E_V,Q estimates give the uniform short interval used below.
There is no global spacetime or black-hole existence claim.

## 3. The coefficient estimate that avoids a density derivative

The exact radial identities are

    (log L)_R = 2m/(R^2 Fgeom) - kappa sigma/(R U),
    m_t,R + kappa[2e/R+sigma/(R U)] m_t = kappa Fgeom e_t.

The latter, quadratic-density Cauchy–Schwarz, and fixed sigma imply

    ||m_t||_infinity <= 2 kappa sqrt(Ebar E_V).

Define Mtime=2 kappa sqrt(Ebar) and ell=Rmax-r. At the physical midpoint,
L=Fgeom, so (log L)_t=-2m_t/(b Fgeom). Differentiate the first radial identity
and integrate from that cut:

    (log L)_t,R
       = 2m_t/(R^2 Fgeom^2) - kappa sigma m_t/(R^2 U^3).

Consequently, with

    B = Mtime[2/(r f)+2ell/(r^2 f^2)+kappa S/(r^2 f^(3/2))],
    B_R = 2 Mtime/(r^2 f^2),
    K = 2/r+2Mstar/(r^2 f),

we have |(log L)_t| <= B sqrt(E_V) everywhere.
Away from the source, |partial_R(log L)_t| <= B_R sqrt(E_V).
Also |a_R|<=amax K and |partial_R(R^2L)|<=cmax K there.

Every free-node sample and every edge except the final edge lies outside
the source collar. Its two layer positions differ by at most h/2. For any z,w,

    |a(z)-a(w)| <= h Da,                 Da=amax K/2,
    |c(z)-c(w)| <= h Dc                 Dc=cmax K/2, bulk edges,
    |bcoef(z)-bcoef(w)| <= h Db sqrt(E_V),  Db=B_R/2,
    |dcoef(z)-dcoef(w)| <= h Dd sqrt(E_V), Dd=(B_R+2BK)/2, bulk edges,

where bcoef=a_t/a and dcoef=c_t/c. The edge-rate estimate follows by
differentiating its positive weighted average of the two nodal log rates.

At the final edge use the honest bounds

    |delta c|<=2cmax, |delta dcoef|<=2B sqrt(E_V).

Do NOT assume those differences are O(h): the source shell survives.
All log rates themselves are bounded by B sqrt(E_V).

More explicitly, set A(z)=integral_(-1/2)^z W(s) ds. In the thin collar,
U_source(z) tends to Uminus-kappa S A(z)/b. The last edge coefficient therefore
tends to b^2 Nshell[Uminus-kappa S A(z)/(2b)], which still depends on z.
Its contribution is controlled by the shrinking edge measure, not by falsely
asserting that this coefficient becomes independent of the layer.

## 4. Exact first-order layer-pair energy

Write Dq_i=(q_(i+1)-q_i)/h and
Div f_i=(f_i-f_(i-1))/omega_i. The reference equations imply exactly

    q_t = a Div f + bcoef q,
    f_t = c Dq + dcoef f.

For two layers z,w, write delta q=q(z)-q(w), delta f=f(z)-f(w), with
coefficients without an indicated layer on the z side. Then

    delta q_t = a(z) Div(delta f) + bcoef(z) delta q + r_q,
    delta f_t = c(z) D(delta q) + dcoef(z) delta f + r_f,

    r_q = delta a Div f(w) + delta bcoef q(w),
    r_f = delta c Dq(w) + delta dcoef f(w).

Use the positive pair energy

    Ezw = (1/2) sum_free omega_i delta q_i^2/a_i(z)
         +(1/2) sum_edges h delta f_i^2/c_i(z).

Summation by parts cancels the principal terms, INCLUDING omega_0=h/2 and
q_source=0. Its exact derivative is

    Ezw_t = (1/2) sum omega bcoef(z) delta q^2/a(z)
            +(1/2) sum h dcoef(z) delta f^2/c(z)
            +sum omega delta q r_q/a(z)
            +sum h delta f r_f/c(z).

No changing clock or live metric term has been omitted.
Let Epair=integral integral Ezw dmu(z)dmu(w), and

    Rh^2 = integral integral [
          sum omega r_q^2/a(z) + sum h r_f^2/c(z)] dmu(z)dmu(w).

Then

    |Epair_t| <= B sqrt(E_V) Epair + sqrt(2 Epair) Rh.

This is not the earlier difference of two physical branches. It compares layers
within ONE actual reference solution and supplies the missing layer compactness.

## 5. Source-edge forcing is small in its correct norm

The actual cumulative force and its time derivative are

    f_i = sum_(j<=i) omega_j p_t,j,
    f_t,i = sum_(j<=i) omega_j p_tt,j.

They give

    integral sup_i |f_i|^2 dmu <= 2 Rmax^2 E_V,
    integral sup_i |f_t,i|^2 dmu <= 2 Rmax^2 E_A.

Since Dq=(f_t-dcoef f)/c,

    integral sup_i |Dq_i|^2 dmu
        <= (4Rmax^2/cmin^2) [E_A+B^2 E_V^2].

Also, directly from E_V and q_source=0,

    integral sum h |Dq|^2 dmu <= 2 E_V/r^2,
    integral sup_i |q_i|^2 dmu <= 2 E_V/r^2,
    integral sum omega |Div f|^2 dmu <= 2 Rmax^2 E_V.

Thus the final edge has an O(1) coefficient difference but only O(h) measure,
with bounded velocity-gradient/force energy. The source term is small without
assuming that its coefficient or its force vanishes.

An explicit reproducible bound is

    Rh^2 <= h^2 (K1 E_V + K2 E_V^2) + h(K3 E_A + K4 E_V^2),

    K1=4[Da^2 Rmax^2/amin + Dc^2/(r^2 cmin)],
    K2=4[Db^2/(r^2 amin) + Dd^2 Rmax^2/cmin],
    K3=32 cmax^2 Rmax^2/cmin^3,
    K4=B^2[K3+16Rmax^2/cmin].

These deliberately conservative constants retain the exceptional source edge.
The inherited E_V,Q bound makes Rh=O_T(sqrt(h)).

The smooth compact initial preparation has Epair(0)=O(h^2): the bulk offsets
differ by O(h), and the source-adjacent fields initially vanish.
Square-root Gronwall therefore yields

    sup_(t<=T) Epair(t) = O_T(h).

The positive energy is asymmetric in z,w, but its coefficients have common
upper/lower bounds; double integration and Cauchy–Schwarz need no symmetry
assumption on those coefficients.

## 6. Convert locking into physical-field compactness

It is essential not to stop after proving a q,f estimate.

### 6.1 Layer variance of momentum and scalar gradient

Use p=q/a and u=f/c. Bulk coefficient differences are O(h). On the source
edge retain the bounded coefficient difference and use its h-weight with
the uniform force supremum. This gives

    integral integral [sum omega |p(z)-p(w)|^2
                        +sum h |u(z)-u(w)|^2] dmu(z)dmu(w)
       <= C[Epair+h E_V+h^2 E_V] = O_T(h).

For normalized dmu, pair variance is exactly twice variance around the layer
mean. Hence p and u approach their layer averages strongly, uniformly in time.
No derivative with respect to z was assumed or inferred from a plot.

### 6.2 Uniform spatial compactness of those means

For bulk edges, difference u=f/c between adjacent edges. Since
f_i-f_(i-1)=omega_i p_t,i and c is spatially Lipschitz there,

    integral [sum_bulk h |Du|^2 + sum h |u|^2] dmu <= C E_V.

The final edge may violate a derivative bound. Replace its u value by the
penultimate edge value solely to construct an auxiliary interpolant.
The force supremum proves that this changes its L2 norm squared by at most
C h E_V. Extend the first edge value constantly to the left endpoint.
The resulting piecewise-linear interpolant has bounded H1 norm.

This auxiliary replacement is NOT an alteration of the evolved equations,
the source matching, or the stored data; its approximation error is estimated.

For p=q/a, the q gradient bound and the bulk Lipschitz bound for a give a
bounded H1 interpolant as well. At the right endpoint p=q=0; for this estimate
one may extend a to that endpoint by its last free value, since multiplying
the zero q there does not change p. This avoids dividing a source jump by h.

The layer means therefore have uniform H1 approximants, with vanishing L2
errors. Their original time derivatives are also uniformly bounded in L2:

    u_t=Dq,       p_t=Div f.

### 6.3 Strong time-uniform convergence, not merely weak subsequences

For completeness, compactness can be seen constructively. Project the layer
means on the first M fixed spatial cosine modes. The H1 approximants give an
L2 tail bounded by C/M^2 + C h. Each finite collection of coefficients is
uniformly Lipschitz in time because the original time derivatives are bounded
in L2. Finite-dimensional Arzela–Ascoli and a diagonal extraction give strong
convergence in C([0,T];L2([5,6])) for a subsequence of those means.

Combining with the O(h) layer variance gives strong convergence of the actual
p_h,u_h in C([0,T];L2(dR dmu)). Recover chi from its right zero value by integrating
u. Its time derivative passes through q=a p. Endpoint traces follow from the
uniform H1 approximants and the already derived zero left force/right q.

In particular, the averaged quadratic scalar energies converge strongly in L1.
There is no residual bulk energy from unresolved layer oscillations within
these estimates.

## 7. Pass the metric, equations and shell; then remove the subsequence

Every scalar collar has energy <= C h E_V by the same force/q supremum bounds
used for the boundary collar. Pushforward from the common base-node cells
to physical collars changes a smooth test integral by O(h) times the total
energy. The cumulative energy discrepancy also vanishes: strong convergence
of the cell energies plus the O(h) maximum cell mass controls partial cells.

The radial integrating-factor/integration-by-parts stability argument from the
preceding note therefore applies at each time, uniformly on [0,T].
It gives convergence of m and N on the retained bulk and their prescribed
one-sided source data. Raw collar density still need not converge pointwise.

Pass the scalar equations in their discrete weak forms:

    chi_t = L p/R^2,
    p_t = partial_R(R^2 L chi_R),

    e=(R^2 chi_R^2+p^2/R^2)/2,
    m_R=kappa Fgeom e,
    (log N)_R=m/(R^2 Fgeom)+kappa e/R.

Strong quadratic convergence excludes an added bulk defect stress. The fixed
left mass and zero flux give m_t=kappa Fgeom L p chi_R as previously derived.
These are the spherical Einstein–massless-scalar equations in the stated
normalization, in weak/strong finite-energy form. This argument alone does
not claim arbitrary differentiability of the limit.

The source remains

    Uplus=Uminus-kappa S/b,
    mplus-mminus=kappa S Uminus-(kappa S)^2/(2b),
    Nshell=(Uminus+Uplus)/2,

with the supporting surface stress calculated in the preceding note.
There is no deletion of the source, change of clock normalization, or inference
that a freely static pressureless shell is allowed.

### 7.1 Uniqueness on the resulting regular annular class

For two limits with bounded H1 scalar-gradient/momentum norms, the radial
constraint and the smooth shell normalization imply

    ||delta L||_(W1,infinity) <= C ||(delta p,delta chi_R)||_L2.

Indeed, the quadratic density difference has an L1 bound by the phase error
times the bounded energies; the mass/lapse integrating-factor bounds control
delta L, and (log L)_R=2m/(R^2Fgeom) controls its bulk derivative.
The boundary clock is a smooth function of mminus while Fgeom stays positive.

Compare the two first-order equations for p and u=chi_R using the first metric
in the positive wave energy. Principal derivatives cancel by integration by
parts. The remaining terms contain delta L and its first derivative times
the second solution's p,u and first spatial derivatives. The displayed
coefficient estimate and its H1 bound control them by C times the error energy.
Metric-time coefficients are bounded as in section 3. Boundary products vanish
because u(left)=0 and p(right)=0.

Gronwall gives uniqueness for common initial and boundary data in this class.
Every convergent subsequence has that same limit, hence the whole reference
family converges on each fixed T<tstar.

### 7.2 Transfer to the MTS regulator: what the conclusion actually covers

The preceding live relative-energy result supplies

    E0(Y_MTS,h-Y_ref,h)=O_T(h),   EG(Y_MTS,h)=O_T(h),

and vanishing mass/lapse differences for the same preparation.
Combining it with the reference convergence above identifies the same strong
scalar/radial-metric limit for the MTS regulator. Positive extra-Gram energy
vanishes; its weak scalar-action pairing with an admissible smooth test also
vanishes by the corresponding energy Cauchy–Schwarz bound.

There is NO quantitative rate asserted for the total MTS-to-continuum error:
the compactness step is qualitative, even though layer locking and
MTS-to-reference estimates have rates.

This is a restricted, short-time, stationary-source, annular reduction to the
identified spherical GR system. It is not proof for every parent field,
arbitrary matter, moving sources, global geometry, or a black-hole horizon.
A parent variational origin for the required supporting surface stress remains
a separate question.

## 8. Reproducible checks and limits of their interpretation

New code:

- `scripts/annular_reference_layer_locking_20260914.py`
- `scripts/derive_annular_reference_layer_locking_20260914.py`
- `scripts/verify_annular_reference_layer_locking_20260914.py`
- `scripts/check_annular_layer_locking_active_source_20260914.py`

### 8.1 Fresh evolution of the actual compact preparation

One BelowNormal, single-core worker; no delegated jobs. Fresh reference runs
at 33,65,129 nodes use the original initial data and end at t=0.0002,
inside the conservative analytic comparison interval.

| nodes | layer-pair energy at t=0.0002 | physical p,u pair variance |
|---:|---:|---:|
| 33 | 2.7958621501e-4 | 2.8983639530e-5 |
| 65 | 7.3618465425e-5 | 7.6907374573e-6 |
| 129 | 1.9100657389e-5 | 2.0079075421e-6 |

All 70 main checks pass. Maximum pair-balance discrepancy is below 2e-21.
Coefficient translation, time-rate, Cauchy–Schwarz and full source-inclusive
forcing estimates are checked. The broad analytic bound is very loose and
is not a useful finite-resolution error bar.

The source forcing of this very short compact pulse is essentially zero.
That is disclosed rather than presented as a demanding source-interaction test.

### 8.2 Independent and active-source controls

Nine independent checks pass:

- exact rational pair-energy algebra with nonzero changing coefficients;
- deleting the metric-time term gives a nonzero discrepancy;
- fresh degree-12, smaller-time-step evolution agrees with degree 8:
  maximum compared state discrepancy 1.113e-15;
- quadrature and pair-energy/forcing refinement;
- centered state-direction derivative of the measured pair energy;
- a localized-coefficient algebra control retaining the h-weighted source term.

The last control is not a physical trajectory or an optimal-rate theorem.

To avoid relying solely on an inactive source, 18 further checks use separately
labelled, manufactured but actually constrained reference preparations.
Their transmitted force is set to 0.004 sin(pi(Rmid-5)/2), with a compatible
nonzero velocity-gradient target; fields and the live geometry are solved
together by iteration. They retain the same annulus, source reservoir and clock,
but are NOT the original compact initial data and are not new evolutions.

The source force exceeds 0.003, the boundary residual is resolved and nonzero,
the exact pair balance holds, and the analytic forcing bound passes on all
three grids. The source-edge residual norm squared is 4.035e-16,
4.953e-17,6.022e-18 respectively; preparation force errors are <=1.26e-16.

### 8.3 Evidence

- `source-intake/navier-stokes/20260914/annular-reference-layer-locking-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-reference-layer-locking-independent-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-reference-layer-locking-active-source-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-reference-continuum-shell-final-integrity.json`
- `scripts/seal_annular_reference_layer_locking_20260914.py`

Executed code and evidence are immutable. Numerical status files retain their
broad/unqualified physics guards as false. The final seal records the narrower
paper-level derivation status; that is not retroactive numerical certification.

## 9. Next useful step

Implement an INDEPENDENT continuum Einstein–scalar evolution with precisely this
shell/clock/initial data, and compare physical scalar, momentum, mass, lapse,
and energy observables against both refining regulator branches.

This tests the identified limit directly, rather than measuring only agreement
between layers or between two discrete models. Keep derivation of the apparatus
surface stress separate; do not call the prescribed supported source a complete
parent matter action.
