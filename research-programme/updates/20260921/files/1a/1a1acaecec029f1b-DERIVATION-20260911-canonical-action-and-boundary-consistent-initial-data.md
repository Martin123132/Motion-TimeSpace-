# Canonical action and boundary-conditioned initial data

Private continuation of the coupled initial-jet work, 11 September 2026.
The construction is numerical and conditional, not a physics or evolution claim.

## 1. What this step achieves, and what it does not

We derive a geometric explanation for the almost invisible lapse mode,
rewrite the parent bulk action in canonical variables, and actually solve
initial Hamiltonian constraints AND their first preservation equations.
The smallest GR and metric-Gram cases have positive-lapse numerical roots
after consistent initialization. This is not the earlier fragile lapse-rate
solve with its troublesome eigenvector suppressed.

There are important limitations. Keeping ALL old initial fields fixed did
not yield a usable general boundary-only repair. The successful construction
changes initial scalar momenta substantially. Finer cold-start solves do
not establish refinement convergence. No old trajectory, error certificate,
energy estimate or physical pass transfers to these new initial states.

The inner mass flux remains a declared diagnostic boundary port, not a
parent-derived physical boundary law. Both branches use the SAME inherited
GR port at each mesh in the final initialization experiment. Earlier failed
per-branch and common-port attempts are retained, not hidden.

## 2. The weak mode is located without fitting its residual

Let q be the C1 cubic Hermite scalar velocity, N a positive continuous P1
lapse, and eta a P1 lapse variation. A scalar acceleration represents
q eta/N poorly or weakly according to the projection Schur matrix. At a
node R_j, its exact derivative jump is

    [partial_R(q eta/N)]_j
       = q_j/N_j^2 * [W]_j,
    W_(j,j+1)=(N_j eta_(j+1)-eta_j N_(j+1))/h_j.

The reconstructed scalar velocity is C1, so the jump comes from eta/N.
When q_j is small, even a significant kink in that ratio becomes almost
invisible. The 64-interval weak mode peaks at R=6.04296875, where the saved
q is about 1.43e-6, rather than the roughly 1e-3 nearest-node values on the
two coarser meshes.

A tent is derived entirely from N, the nodes, and the node k nearest a
scalar-velocity zero. Define

    I_0=0, I_(j+1)-I_j=h_j/(N_j N_(j+1)),
    eta_j=(N_j/N_k) I_j/I_k                    for j<=k,
    eta_j=(N_j/N_k) (I_end-I_j)/(I_end-I_k)    for j>=k.

These increments exactly integrate 1/N^2 on each linear-lapse cell. W is
constant separately to the left and right, eta vanishes at both endpoints,
and the sole product derivative jump is

    -q_k/N_k^3 * (1/I_k+1/(I_end-I_k)).

This predicts the old smallest-eigenvalue vector very closely (alignment
about 0.99958 at 16 intervals and 0.9999999988 at 64). The final control report stores all
six alignments and jumps. It is not an eigenvector fitted to a force.
This explains a near-null mechanism, not a proof of an exact gauge mode or
the full Schur asymptotics: cellwise polynomial/rational representation
errors also matter. Endpoint clock conditions alone do not remove this
endpoint-vanishing direction.

## 3. Derive canonical variables before spatial projection

Use the inherited canonical branch kappa=1/10, Lambda=m_chi=b2=b3=0,
F=1-2 mu/R and a=F^(-1/2). Starting from the weak bulk density, introduce

    P=beta/(kappa N F^(3/2)),
    pi=R^2(q-beta w)/(N sqrt(F)),
    beta=kappa N F^(3/2) P, q=chi_t, w=chi_R.

The EXACT equivalent first-order bulk density is

    L_can = P mu_t + pi chi_t + N mu_R/(kappa sqrt(F))
      -N sqrt(F) [pi^2/(2 R^2)+R^2 chi_R^2/2]
      -kappa N F^(3/2) P pi chi_R
      -(kappa R F^3/2) (a_R N+a N_R) P^2.

Eliminating the auxiliary pi by its equation and replacing beta recovers
the original density, including the shift terms. The physical radial
boundary flux transforms to

    -[kappa R N F^(5/2) P^2/2].

It is retained. The outer clock term remains -C(t) mu_out/kappa. No radial
integration by parts is silently used to alter either boundary term.
The canonical bulk is linear in N and N_R at fixed canonical fields.
Its lapse/lapse Hessian vanishes exactly, as the symbolic checks verify.

This is why there is an alternative to dividing by the earlier tiny
velocity-projection Schur matrix. Discretizing a velocity space and then
Legendre transforming does not generally commute with this construction.
The continuum bulk actions are equivalent; their frozen finite-dimensional
representations are NOT claimed identical. The previous certificates stay
with the previous representation.

## 4. Memory is retained, not replaced by a unit-J potential

Keep the full Gram action, with its existing time transports. In the new
variables its connection and coefficient are

    c=kappa sqrt(F) P/[N(1-kappa^2 F^2 P^2)],
    C_i=R_i^2 N_i sqrt(F_i)(1-kappa^2 F_i^2 P_i^2).

The last checkpoint's physical-time adjoint is pulled through this change
of variables. At P=0,

    g=partial_t c=kappa sqrt(F) P_t/N,
    G_P[z]=sum_fi I_fi J_fi integral_anchor^Ri
                    kappa sqrt(F) z/(N J_fR^2) dR.

The scalar force still contains D_f/J_fi and the weighted current still
satisfies sum_i J_fi I_fi=0. At fixed P, partial_N c=-c/N. Therefore the
Gram contribution to the first lapse-constraint derivative contains
-P_t/N times the P-covector density. In the old beta variables the equivalent
canonical term is -beta_t/N times the beta-covector density, NOT the old
-2 beta_t/N coefficient appropriate to holding beta fixed. The difference
is the chain rule, not a fitted cancellation.

At the zero-P slice, the direct Gram lapse/mass covectors retain the
previous Jacobian cancellation. The canonical bulk constraints remain
linear in the lapse, but we do NOT assert a local ordinary Hamiltonian
description for the entire nonlocal Gram action. Its initial preservation
equations are obtained from the time-link adjoint, with radial numerical
quadrature, rather than assumed to be an ordinary Poisson bracket.

## 5. Finite canonical construction and boundary reactions

Freeze the previously constructed mass map A and shift map S at the seed.
Choose dual momentum reconstructions

    Pmap=rho_seed S,
    pimap=m_seed V_full,
    K_mu=Q[Pmap^T A], K_chi=Q[pimap^T V_full].

Both are invertible on the tested finite spaces. Configuration and momentum
coefficients are independent; multiplying these maps does not impose the
old restricted-velocity ansatz at all later lapse values.

The inner mass and two scalar endpoint positions have reaction multipliers
lambda=(lambda_mu,lambda_left,lambda_right). Their velocities are boundary
inputs for the present conditional initialization. The two scalar velocities
are inherited. The inner mass velocity is explicitly the prior GR trial's
mass-rate port, used identically for GR and Gram; it is not claimed selected
by the fundamental theory.

For GR, first constraint preservation plus these three boundary velocities
forms the canonical Dirac multiplier system for N and lambda. Its matrix is
skew-symmetric to roundoff, independently checking the canonical signs.
For Gram the corresponding equations are nonlinear through J and are
evaluated using section 4, not a unit-J GR matrix.

The clock VALUE enters the mass momentum equation. Its prescribed RATE
and the scalar endpoint ACCELERATIONS belong to the next differentiated
multiplier problem. They have NOT been satisfied merely by solving this
initial state. No higher-order boundary compatibility is claimed.

## 6. Boundary-only attempts were not promoted

With the old canonical initial fields held fixed, the smallest GR multiplier
solve gives a positive lapse approximately [0.41845,0.82084]. However the
32-interval GR solve gives a negative lapse minimum approximately -8.13.
The smallest Gram positive-chart Newton searches fail both with its own
inherited flux and with the common GR flux.

Those are recorded failed numerical attempts, not proofs that no Gram
solution exists. They rule out promoting that particular computation.
An inadmissible GR counterfactual seed was replaced by the original positive
lapse as a SECOND Newton starting guess; that attempt also failed. The
line-search floor 0.02 is a solver safeguard, not a physical lower bound or
proof of nonexistence throughout N>0.

Thus simply changing boundary multipliers while freezing all old initial
fields was not a justified universal repair. This is why the next actual
construction solves the initial constraints themselves as well.

## 7. Solve compatible initial data, not a smaller residual by damping

Hold the positive original lapse, scalar configuration, inner mass value,
clock value, scalar endpoint velocities, and declared inner flux fixed.
Use the SAME protocol for both branches. Unknowns are:

    n free original mass-face values,
    n scalar momentum nodal coefficients,
    3 boundary reaction multipliers,

where n is the number of scalar nodes. Momentum slope coefficients are
held fixed. Initial added mass-bubble coefficients are exactly zero.
There are 2n+3 unknowns and equations:

    n Hamiltonian constraints C_N=0,
    n first preservation equations dot C_N=0,
    3 specified boundary velocities.

The solve uses Newton with line search, not damping or deleting an equation
of motion. Both P_t and pi_t are obtained from the canonical action with
their boundary reactions. The helper also supports a different exploratory
free-data split (mass bubbles plus endpoint momenta); a preliminary GR
calculation required a much larger mass-field change (~0.0582), so it was
not adopted as the preferred initializer. This is a choice of numerical
initial free data, not a new physical coupling or an observational fit.

At 16 intervals the nodal initialization converges for BOTH branches:

| Diagnostic | GR | metric-Gram |
| --- | ---: | ---: |
| max Hamiltonian constraint | 3.89e-15 | 8.32e-13 |
| max first constraint derivative | 9.76e-18 | 1.79e-16 |
| max boundary velocity residual | 1.74e-17 | 2.95e-17 |
| max mass-field change | 8.37e-5 | 4.37e-5 |
| max reconstructed scalar-velocity change | 0.02347 | 0.01913 |
| original scalar-velocity max | 0.01684 | 0.01684 |
| minimum F | 0.65959 | 0.65959 |

The lapse remains the specified approximately [0.81208,0.82063], rather
than being driven to a huge rate by the earlier Schur solve. These results
do NOT yet calculate the new lapse RATE. Scalar momentum/velocity changes
are comparable to or larger than the original pulse; they must not be
described as a tiny correction to unchanged physical initial data.

Sampled bulk strong-constraint defects do not automatically improve:
approximately 0.00252 to 0.00348 (GR) and 0.00392 (Gram). These diagnostics
exclude Gram point/nonlocal covectors and are not full strong residual
bounds. Weak root residuals alone do not prove convergence to the continuum.

The 32- and 64-interval cold-start solves fail in both branches: 2/6 tested
cases converge, both on the coarsest grid. At 64 intervals the GR run reaches
the iteration limit and the Gram run fails line search. Their Hamiltonian
constraint maxima remain approximately 8.76e-4 and 2.11e-3 respectively.
The failed iterates also develop much worse sampled bulk defects; they
are NOT evolution data. No failed
iterate is promoted to a solution; no fine-grid pass or refinement theorem
is claimed. Solver failure is not a proof of mathematical nonexistence.

## 8. Boundary energy and what remains to derive

For the GR canonical action at P=0, fixed lapse, the boundary power identity
is

    C mu_t,out/kappa - sum_b lambda_b v_b - sum_j N_j (C_j)_t = 0.

The explicit C_t mu_out/kappa contribution cancels from the two sides of the
Noether balance. The independent control checks this identity (error about
2.57e-18) and the
time derivative of the full canonical bulk constraint, including its P
and P^2 terms. Physical boundary flux terms are quadratic in P and have
zero first time derivative at this slice; they return at the next order.

This energy balance verifies the reaction bookkeeping. It does NOT supply
a unique physical inner-flux law by itself. The nonlocal Gram energy
requires its own temporal-boundary/transport analysis and is not inferred
from this GR identity.

Next: continue the two CONVERGED coarse initial states to finer grids with
consistent momentum free data, rather than assuming independent cold
starts find the same branch. Track scalar momentum changes and full spatial
residuals, not just solver tolerances. Then differentiate the canonical
multiplier system using the inherited C_t and endpoint accelerations, and
obtain certified local persistence. Do not evolve the failed fine iterates,
reuse the old residence proof, or declare the physical boundary port closed.

## 9. Sources and reproducibility

- `DERIVATION-20260911-coupled-initial-jet-and-exact-time-link-adjoint.md`
- `scripts/annular_canonical_boundary_20260911.py`
- `scripts/derive_annular_canonical_boundary_20260911.py`
- `scripts/annular_canonical_initial_data_20260911.py`
- `scripts/annular_canonical_nodal_data_20260911.py`
- `scripts/derive_annular_canonical_initial_data_20260911.py`
- `scripts/verify_annular_canonical_control_20260911.py`
- `source-intake/navier-stokes/20260911/annular-canonical-boundary-probe01/status.json`
- `source-intake/navier-stokes/20260911/annular-canonical-boundary-probe02/status.json`
- `source-intake/navier-stokes/20260911/annular-canonical-boundary-probe03/status.json`
- `source-intake/navier-stokes/20260911/annular-canonical-boundary-common01/status.json`
- `source-intake/navier-stokes/20260911/annular-canonical-boundary-GRmatrix01/status.json`
- `source-intake/navier-stokes/20260911/annular-canonical-initial-data-nodal01/status.json`
- `source-intake/navier-stokes/20260911/annular-canonical-independent-control-attempt01/status.json`

Failed attempts preserve their executed source snapshots. They may differ
from the current runner because diagnostics/starting-guess handling were
improved after failures; that difference must not be mistaken for an
alteration to a completed successful checkpoint. All original sealed work
is unchanged. All calculations are private, single-core, without GitHub
actions or new agents. The final seal records validation and scope.
