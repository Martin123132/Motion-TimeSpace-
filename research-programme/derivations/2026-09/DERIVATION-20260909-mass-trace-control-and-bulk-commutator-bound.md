# Physical mass-trace control and bulk commutator bounds

2026-09-09. Private continuation of
`DERIVATION-20260909-boundary-current-and-N64-spatial-control.md`.
No boundary-data changes, new evolution, fitted coefficients, filtering,
GitHub action or edits to the frozen workbench.

## 1. What was actually derived

1. The boundary shift contribution is a positive weighted average of the
   mass-rate mismatch, with an explicit coefficient that need not grow
   as the grid is refined. It is not an unnormalized nodal residual norm.
2. The affine bulk reconstruction defect has an exact six-term formula.
   Two apparent time-derivative terms cancel, and a zero cell moment gives
   the gravitational radial-product term an additional power of mesh size.
3. The scalar interpolation defect can be bounded using ONE spatial
   derivative of the scalar velocity, instead of demanding a uniformly
   bounded third derivative. The constants are derived exactly.

All these statements are conditional on the specified action, positive
chart and finite-element spaces. The new work does NOT establish a
mesh-uniform evolution estimate, solve every coupled equation, or prove
local-GR/horizon recovery. It supplies more useful estimates for doing that.

## 2. Setup and meaning of the norm

Use the released-Hermite system unchanged. Mass and shift use face P1
basis Q, lapse uses nodal P1, and scalar/velocity use the lifted cubic
Hermite reconstruction. Let W denote positive action quadrature weights.

    F_h=1-2mu_h/R-Lambda R^2/3,  gamma_h=N_h^2 F_h,
    ell=b-a,  f=(R-a)/ell,  S_f=-gamma_face/ell.

Let mu_dot,c be the differentiated-constraint mass velocity and mu_dot,V
the velocity obtained from the full shift equation. Define

    d=mu_dot,c-mu_dot,V,    E_V=B d.

All face entries, including boundaries, are retained. The norm ||d||_inf
is the sup norm of the reconstructed P1 mass-rate mismatch: a linear
function reaches its interval extrema at endpoints. Here "physical" means
a mass-velocity variable rather than its integrated dual covector. It is
still in fixture units, not an observed mass flow or an empirical bound.

The label GR denotes the same Einstein/scalar action without the Gram
term; the nonlinear GR comparator still contains the declared P(X) scalar.

## 3. Positive mass pairing and an explicit boundary coefficient

Directly from the action,

    B=Q^T W diag[b_h] Q,     b_h=1/(kappa N_h F_h^(3/2)).

For kappa>0,N_h>0,F_h>0 this is positive definite on the face space.
If M0=Q^T W Q and b_min<=b_h<=b_max, then

    b_min M0 <= B <= b_max M0

as quadratic forms. This is coercivity in the physical quadrature L2 norm,
not an assertion that the smallest Euclidean eigenvalue stays independent
of cell size. Positive quadrature and injectivity of P1 sampling justify
the positive definiteness.

Since Q is nonnegative and a partition of unity,

    -S_f dot E_V = w dot d,
    w=Q^T W[b_h (P_face gamma_face)/ell] > 0,
    C_h=sum_i w_i
       =(1/ell) sum W[b_h P_face gamma_face],

    |-S_f dot E_V| <= C_h ||d||_inf.

This identity and bound are independently checked against the original
mass pairing and the full saved shift vector. No cancellation-prone
signed sum is mistaken for a norm.

A sufficient explicit envelope is

    C_h <= N_max^2 F_max/(kappa N_min F_min^(3/2)).

The positive quadrature weights sum to ell. Face interpolation preserves
the maximum of gamma_face, so the number of cells does not appear.
For each face cell [u,v] the implemented sufficient metric bounds are

    F_lower=1-2 max(|mu_u|,|mu_v|)/u-|Lambda|v^2/3,
    F_upper=1+2 max(|mu_u|,|mu_v|)/u+|Lambda|v^2/3.

Take the global minimum/maximum and the nodal lapse extrema. A nonpositive
sufficient lower bound rejects the estimate; denominators are not clipped.
This can reject a valid chart if the envelope is too conservative.

In the final-time N16/N32/N64 samples, C_h is approximately 9.99985-9.99987
for both branches. The explicit envelopes are approximately 20.75
(canonical) and 21.28 (nonlinear). This near-10 value belongs to the
fixture normalization kappa=0.1 and its geometry. It is NOT a new coupling,
a universal constant, or a derivation of Newton's constant.

These are mesh-independent FORMULAS. Uniform-in-time constants require
uniform metric bounds, which the finite samples do not prove.

## 4. Exact affine reconstruction products

On a face cell [u,v], let m_h=mu_dot,c be linear and f'=1/ell. Then

    e_mu=P_face(f m_h)-f m_h
        =m_h' (R-u)(v-R)/ell,
    e_mu,R=m_h'(u+v-2R)/ell.

The analogous nodal lapse product is

    e_N=P_node(f N_h)-f N_h=N_h'(R-u)(v-R)/ell

on each lapse cell. In the scalar cells q_h is cubic. The product f q_h
is quartic, and matching its endpoint values and derivatives gives

    e_q=H_3(f q_h)-f q_h
       =-q_h''' (R-u)^2(R-v)^2/(6ell),
    e_q,R=-q_h''' (R-u)(R-v)(2R-u-v)/(3ell).

These identities use the ACTUAL released nodal derivative
Dq+v_s/h. Prescribing the old lifting history would change the state.
The identities were also checked symbolically, not only on the fixtures.

The metric product defect is

    e_V=(gamma_h-P_face gamma_face)/ell.

With L the original bulk density and its partial derivatives evaluated
before constraints are imposed, the full affine bulk remainder reduces to

    D_bulk[f]=sum W[
       L_mu e_mu + L_mu_R e_mu,R
       -(d_t L_N) e_N
       +(L_chi-d_t L_q) e_q + L_w e_q,R + L_V e_V ].

The lapse time-product cancellation is

    L_N d_t e_N-d_t(L_N e_N)=-(d_t L_N)e_N;

the scalar velocity-product cancellation is the same identity with L_q.
No assumption that accelerations or coefficient time derivatives vanish
is made. Their remaining appearances are explicit. Independent assembly
of every term agrees with the previously saved full Ward calculation.

## 5. The mass radial term has a useful cell cancellation

Taking absolute values too early would give only a first-order estimate
for L_mu_R e_mu,R. But its unweighted cell integral is zero:

    integral_cell e_mu,R=0.

The composite Gauss rule integrates this linear polynomial exactly, even
where the lapse node splits a face cell. Let c=(u+v)/2 and

    A=L_mu_R=N_h/(kappa sqrt(F_h)).

Then its discrete contribution is exactly

    sum_cell W [A(R)-A(c)] e_mu,R.

N_h and A are continuous across lapse knots. On their smooth subintervals,

    A'=N_h'/(kappa sqrt(F_h))
        -N_h F_h'/(2kappa F_h^(3/2)),
    F_h'=-2mu_h'/R+2mu_h/R^2-2Lambda R/3.

Endpoint and positive-chart bounds give a Lipschitz constant L_A,C,
including every nodal kink. Therefore

    |sum_cell W A e_mu,R|
       <= |mu_dot_h'| L_A,C (v-u)^3/(6ell).

Together with the mass value product this contributes at most

    sum_C |mu_dot_h'| (v-u)^3
          [sup_Q |L_mu|+L_A,C]/(6ell).

The sup_Q denotes the finite positive quadrature samples; a continuum
coefficient bound may replace it. With uniform coefficient/derivative
control, summing these cells is second order in maximum cell width.
The lapse product has the analogous second-order estimate involving
|N_h'| and |d_t L_N|. It does not require a bound on N_dot,h'.

The existing piecewise-smooth gamma interpolation bound supplies e_V.
The Gram coefficient contribution is bounded by

    sum_nodes |rho|[
      |a_mu| |e_mu at node| + |a_V| B_gamma,cell/ell ],

where B_gamma,cell is the previously derived interpolation bound.
The Gram link contribution retains sum_pairs |j| bound(e_link).
All these quantities, including their signed sums, are saved separately.
Uniform control of their coefficient/current norms is not asserted.

## 6. Removing an unnecessarily strong third-derivative assumption

The maximum q_h''' grows under refinement in BOTH branches. It would be
unjustified to assume it remains uniformly bounded. It is also unnecessary
for controlling this affine scalar commutator.

On a scalar cell of width d, q_h' is quadratic. Its degree-two Legendre
component implies the exact polynomial inverse inequality

    |q_h'''|^2 <= 720 d^(-5) ||q_h'||_L2(cell)^2.

For example, mapping the cell to [-1,1] gives q_h'''=12 a_2/d^2 and
||q_h'||^2 >= d a_2^2/5. The lower Legendre modes can only increase
the norm. This is a finite polynomial-space identity, not an assumed
physical smoothness property.

The exact error integrals are

    ||e_q||_L2(cell)^2
      =|q_h'''|^2 d^9/(22680 ell^2),
    ||e_q,R||_L2(cell)^2
      =|q_h'''|^2 d^7/(1890 ell^2).

Thus, with h_s the largest scalar cell width,

    ||e_q||_W <= sqrt(2/63) (h_s^2/ell) ||q_h'||_W,
    ||e_q,R||_W <= sqrt(8/21) (h_s/ell) ||q_h'||_W.

The derivative and q_h' squared integrands are integrated exactly by the
existing Gauss rule. e_q squared has degree eight; its leading coefficient
is nonnegative, so four-point Gauss underestimates its exact integral.
Consequently the same upper bound applies to the implemented W norm.
The exact polynomial constants and numerical quadrature statements are
checked separately.

Cauchy-Schwarz now bounds the entire scalar commutator by

    [sqrt(2/63) h_s^2 ||L_chi-d_t L_q||_W
      +sqrt(8/21) h_s ||L_w||_W] ||q_h'||_W / ell.

This removes the requirement of a uniform third derivative. With uniform
displayed norms it tends to zero at least linearly. We still need to
derive a uniform-in-time velocity H1 estimate, rather than assume one.
The other coefficient norms and metric chart must also remain controlled.

## 7. Why positive kinetic energy alone is not that estimate

A manufactured counterexample uses alternating nodal q values and chooses
the slope velocities so q_h' vanishes at nodes. It is a continuous cubic
Hermite velocity, normalized to kinetic norm squared exactly one on a
canonical positive chart. Its maximum third derivative increases by
approximately eight on each grid doubling:

| grid | kinetic norm squared | maximum third derivative |
|---|---:|---:|
| N16 | 1 | 3.009e6 |
| N32 | 1 | 2.407e7 |
| N64 | 1 | 1.926e8 |

The same canonical kinetic form applies to both GR and the candidate.
These manufactured configurations are NOT constraint solutions or evolved
counterexamples to MTS. They only refute the inference that a positive
basic kinetic matrix, or a bounded velocity L2 energy, automatically
bounds higher spatial derivatives. They do not refute the weaker
commutator estimates just derived.

## 8. Results on the unmodified saved trajectories

All initial, midpoint and final states are checked: two fixtures, three
grids, GR and candidate, 36 samples. No new long evolution was run.

Final-time sharper, state-specific bounds from the exact polynomial
remainders (not the looser H1-only envelope):

| fixture / branch | grid | actual endpoint offset magnitude | derived outer bound |
|---|---:|---:|---:|
| canonical GR | N32 | 1.342e-6 | 4.352e-6 |
| canonical candidate | N32 | 2.925e-6 | 9.960e-6 |
| canonical GR | N64 | 8.444e-9 | 5.546e-7 |
| canonical candidate | N64 | 1.268e-6 | 2.669e-6 |
| nonlinear GR | N32 | 6.607e-8 | 6.929e-6 |
| nonlinear candidate | N32 | 1.921e-6 | 1.316e-5 |
| nonlinear GR | N64 | 3.544e-7 | 7.665e-7 |
| nonlinear candidate | N64 | 7.188e-7 | 2.534e-6 |

The derived outer bound is C_h ||d||_inf plus the absolute bulk/Gram
remainder bounds and free-equation work. The inner endpoint requires
adding the retained global balance remainder, numerically roundoff here.
These are floating-point evaluations of analytic inequalities, not
interval certificates or continuous-time suprema.

Candidate bulk remainder bounds alone fall from 8.284e-7 to 1.506e-7
(canonical) and 8.565e-7 to 1.572e-7 (nonlinear), from N32 to N64.
Their SIGNED affine bulk remainders are much smaller, around 1e-12.
A small signed cancellation is not substituted for an absolute bound.

The weaker norm needed by section 6 behaves much better than q_h''':

| final candidate quantity | canonical N16 / N32 / N64 | nonlinear N16 / N32 / N64 |
|---|---|---|
| velocity-gradient L2 norm | 0.0848366 / 0.0848025 / 0.0847976 | 0.0889800 / 0.0889476 / 0.0889430 |
| maximum third derivative | 785.6 / 1303.3 / 3032.1 | 785.8 / 1325.1 / 3399.7 |

The GR first-derivative norms are comparably stable. Across all 36 samples
the first-derivative norm ranges about 0.0848-0.0904. This is encouraging
numerical evidence for the weaker target, NOT a uniform stability proof.

The H1-only scalar bound is substantially looser: for the final N64
candidate it is 1.817e-4 or 1.954e-4, versus the much smaller sharp
state-specific bulk bounds above. These are different estimates with
different input requirements; do not conflate their strengths.

## 9. Provenance and validation

New files:

- `scripts/annular_mass_trace_remainder_bound_20260909.py`
- `scripts/derive_annular_mass_trace_bound_20260909.py`
- `scripts/derive_annular_commutator_energy_control_20260909.py`

Completed result owners:

- `source-intake/navier-stokes/20260909/annular-mass-trace-remainder-bound-derived/status.json`: 1024/1024 implementation checks, 36 state samples and three manufactured counterexamples.
- `source-intake/navier-stokes/20260909/annular-affine-commutator-energy-control/status.json`: 224/224 checks of the exact energy-norm constants and the same 36 states.
- `source-intake/navier-stokes/20260909/annular-mass-trace-final-integrity.json`: combined final source/output/citation and protected-path verification.

Executed-script snapshots, source/output hashes and per-state arrays are
recorded. The combined final seal is produced by the energy-control
script's seal phase; it incorporates the preceding mass-trace derivation.
The checks validate implementation, not additional physical discoveries.
Workers were single-core BelowNormal, one at a time, with bytecode disabled.

## 10. Next derivation, not another coefficient search

Construct a first-spatial-derivative energy for the released scalar/metric
system. Its estimate must control ||q_h'||_L2 and the accompanying scalar
and metric derivatives from the equations, retain Gram coefficient/time
work and actual boundary fluxes, and disclose forcing by unsatisfied
shift equations. Start with the canonical GR control, then use the same
estimate for canonical Gram and the nonlinear fixture.

Target an inequality of the form

    d_t E_1 <= C(E_1+known boundary/source work)
                +explicit full-equation residual forcing,

with positive norm equivalence and constants uniform in the mesh under
the stated positive-chart assumptions. This displayed inequality is the
NEXT TARGET, not a proved result of this file. A differentiated action
calculation may show it needs alteration or cannot close.

Do not return to demanding a uniform q_h''' bound, infer stability from
positive kinetic eigenvalues alone, tune away the boundary offset, or
pretend the identity E_V=Bd proves that d vanishes. Full coupled DAE/Dirac
closure, global boundary compatibility, parent calibration and horizon
regularity remain separate open obligations.
