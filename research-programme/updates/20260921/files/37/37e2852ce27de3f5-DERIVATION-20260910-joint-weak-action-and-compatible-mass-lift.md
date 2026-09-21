# Joint weak-action prototype: compatible mass lift and Gram cancellation

10 September 2026. Private canonical annular continuation.
**319/319 checks, 18 states**, matched GR-plus-scalar and metric-Gram,
at 16/32/64 radial intervals and saved times 0/0.005/0.01.

This step constructs a solution to a specific obstruction: a continuous
mass-space enrichment now satisfies both the original shift tests and the
new discontinuous compatibility tests. The construction uses the action's
pairing and test functions, not an added force fitted to the residual.
It also proves an exact cancellation of the Gram virtual-work terms.

It is NOT a completed joint parent solution. The enlarged action has extra
mass Euler equations; all 18 old field profiles fail them if both shift
and shift rate are kept zero. Full initial-data/Legendre consistency and
constraint preservation remain to be derived. No evolution was launched.

Predecessor: `DERIVATION-20260910-weak-product-compatibility-and-action-repair-condition.md`.

## 1. The joint virtual displacement

Keep the canonical definitions

    F=1-2mu/R,  q=chi_t,  w=chi_R,  kappa=1/10,
    rho=1/(kappa N F^(3/2)),  s=kappa R^2 F q w.

For an interior lapse hat eta, the products required by the weak identity are

    phi=eta q/N,   h=eta u/N,   zeta=F(N eta_R-eta N_R).

The previous derivation established that zeta generally has jumps and is
not in the old continuous face space. Phi and h are continuous H1 functions
on a fixed positive background. Enrichment functions are frozen before
taking variations: they are numerical basis functions, not extra physical
fields or state-dependent forces. Across a root enclosure this defines a
family of local prototypes; it is not yet one globally adaptive action.

## 2. An exact primitive closes the Gram virtual-work identity

The metric-link generator for a shift test zeta satisfies

    zeta/(N^2 F) = partial_R(eta/N).

Therefore its exact integral from a factor anchor a_f to a node R_i is

    K_exact,fi = eta(R_i)/N(R_i) - eta(a_f)/N(a_f).

This identity holds piecewise and across internal nodes because eta/N is
continuous. No interface jump of eta/N is being suppressed. It is checked
symbolically, and the endpoint kernel is evaluated independently of the
existing link Gauss quadrature.

Let B_fi be the stored Gram difference factor, S_fi its sampling weights,
A_f=sum_i B_fi chi_i, A_dot,f=sum_i B_fi q_i, C_i=R_i^2 N_i sqrt(F_i),
and Cbar_f=sum_i S_fi C_i. The original link current is

    J_fi = C_i S_fi A_f A_dot,f/h_grid
            - q_i B_fi Cbar_f A_f/h_grid.

Its factor sum vanishes identically: sum_i J_fi=0. Thus anchor terms cancel
from j_G[zeta]=-sum_fi J_fi K_exact,fi. With

    d_i=sum_f S_fi A_f^2/(2h_grid),
    d_dot,i=sum_f S_fi A_f A_dot,f/h_grid,

the four action-owned terms satisfy

    G_chi[phi] + (G_N)_t[eta] - G_mu[h] - j_G[zeta] = 0.

Here G_chi is the positive Gram-potential scalar variation, while G_N and
G_mu denote its contributions to the ACTION's lapse and mass covectors.
Explicitly, the mass-rate pieces +R_i d_i u_i/sqrt(F_i) in (G_N)_t
cancel those in G_mu[h]; the remaining -R_i^2 sqrt(F_i) d_dot,i and
scalar-force term cancel the endpoint link current. This is a derived
coupling identity, not independent tuning of four coefficients.

All nine Gram cases enclose this exact cancellation; the largest interval
upper norm is 7.971e-15. GR has no Gram terms at all.
The prototype shift solve retains the ORIGINAL link Gauss integration,
not a silent replacement by the exact primitive. Its separately enclosed
remainder j_G,exact-j_G,Gauss has maximum upper norm 1.014e-14 over these
states. This is a bound for this particular functional on these boxes,
not a general quadrature-error or continuum-convergence theorem.

## 3. A continuous mass lift compatible with the new shift tests

Write V for the original face reconstruction and P=Q[rho V^T V]. For all
interior hats form the columns Z=zeta and their weighted residuals

    T=P^(-1) Q[rho V^T Z],     R_Z=Z-VT,
    Q[rho V^T R_Z]=0.

Simply adding Z to the shift tests with no mass enrichment fails: the old
square shift system uniquely fixes u_old, and its new-test residual is
strictly nonzero in all 18 cases. An old-space mass rate cannot satisfy both.

To add admissible mass functions, split at the union of nodal and face
knots. On each subcell with local coordinate xi in [0,1] use the two bubbles

    b_even=4xi(1-xi),    b_odd=4xi(1-xi)(2xi-1).

They vanish at every subcell endpoint. Their global extensions are
continuous H1 functions, with no mass-value jumps at nodes or interfaces.
The odd bubble is retained rather than relying only on even cell moments.
Let B be the bubble reconstruction. Define

    D=Q[rho B^T B],       M=Q[rho B^T R_Z],
    C=D^(-1) M,           H=B C,
    G=M^T D^(-1) M.

D consists of positive 2-by-2 cell blocks; each determinant is enclosed
strictly positive. H is the weighted Riesz representative of R_Z restricted
to the bubble space. Equivalently each column minimizes the positive
quadratic 1/2 Q[rho h^2]-Q[rho R_Z,j h] over that space.
This is a BASIS CONSTRUCTION, not a term added to the physical action.
It depends on the metric and test spaces, not the scalar forcing or the
observed shift defect. G is a Gram matrix; its inverse is verified on all
18 root boxes, establishing positivity and independence for this finite lift.

Use enlarged mass space span(V,H) and shift space span(V,R_Z), equivalent
to span(V,Z). The mass functions remain continuous; the extra shift tests
can be broken because the weak bulk form below has no shift derivative.

## 4. Solve all original and enlarged shift equations

The original sourced shift load is b_old=Q[rho V^T s]+j_G[V]. The new load is

    b_Z=Q[rho R_Z^T s]+j_G[Z]-T^T j_G[V].

Every load is calculated from the original scalar field and link current.
The two exact solves are

    G d=b_Z,
    P c=b_old-Q[rho V^T H] d,
    u_new=V c+H d.

Weighted orthogonality and the definition of G imply

    Q[rho V^T u_new]=b_old,
    Q[rho Z^T(u_new-s)]-j_G[Z]=0.

This is the solution of the enlarged action-derived shift equations, not
definition of an extra source as minus the measured error. The old rate
is recomputed only as a comparison. Verified inverses of P and G own the
existence statement; zero-containing residual intervals and independent
pairing checks are additional validation, not the sole argument.

All 18 cases pass both sets of equations. The largest midpoint residual
in the new tests is 1.051e-17. The interval residual enclosures can be much
wider because repeated correlated quantities are enclosed independently:
the final N64 Gram new-test interval upper norm is about 1.494e-5. Do NOT
describe that as a tight 1e-17 error certificate or infer convergence from it.

The solution changes the mass RATE, not the saved initial mass/scalar/lapse
fields. Even though the bubbles vanish at endpoints, the solved old-space
coefficients also change: old endpoint rates are not assumed preserved.
No prior trajectory or residence certificate is transplanted to u_new.

## 5. The action and its coupled variations

With a=F^(-1/2) and beta the shift, use the smooth-equivalent weak bulk form

    L_weak = N mu_R/(kappa sqrt(F))
             + beta mu_t/(kappa N F^(3/2))
             - R (aN)_R beta^2/(2kappa N^2)
             + R^2 a(q-beta w)^2/(2N) - R^2 N w^2/(2a).

Retain the spatial boundary action -[R a beta^2/(2kappa N)] and the
existing outer clock term -C mu_outer/kappa. Substitute the enlarged
functions into this action before varying; do not append only new shift
equations to the old mass evolution. At beta=beta_t=0 the relevant rows are

    scalar: Pi=Q[m v_h q],  Pi_t=-Q[p w v_h,R]-G_chi[v_h],
    mass:   Q[ell_mu h_h+ell_muR h_h,R]+G_mu[h_h]-C h_h(out)/kappa,
    lapse:  Q[eta (mu_R/(kappa sqrt(F))-R^2 q^2/(2N^2 sqrt(F))
                   -R^2 sqrt(F) w^2/2)]+G_N[eta],
    shift:  Q[rho beta_test (mu_t-s)]-j_G[beta_test].

For the first row m=R^2/(N sqrt(F)) and p=R^2 N sqrt(F); ell_mu and
ell_muR are the original bulk mass derivatives in the preceding note.
The scalar enrichment span(V_scalar,phi_j) is admissible at this slice;
its additional momenta are fixed by the same Legendre expression. The
Gram virtual-work calculation includes the exact phi tests, not just their
old projection. A full enlarged scalar trajectory has not been solved.

Crucially, the full mass equation away from beta_t=0 also contains the
time derivative of its canonical momentum. The bulk contribution is

    Pi_mass[h_h]=Q[rho beta h_h],
    E_mass[h_h]|_(beta=0)=F_mass[h_h]-Q[rho beta_t h_h]

in the temporally reduced first-order Gram representative. Thus a nonzero
added mass row does not by itself rule out embedding with a derived shift
rate. The complete Legendre/time-link/boundary calculation must decide that,
rather than imposing zero shift rate as an unearned identity.

There is a specific guard against overextending that formula. In the raw
inherited metric-link action, beta=0 at one time does not imply unit time
Jacobian if beta_t is nonzero. The link equations then give, along an
anchor-to-node path on that time slice,

    dT/dR=0,      dJ/dR=beta_t J/(N^2 F),
    J(R_i)=exp(integral_(anchor)^(R_i) beta_t/(N^2 F) dR).

The transported density uses this J. Therefore the GR shift-rate solve
cannot simply be copied into the Gram branch while keeping its old
unit-Jacobian coefficients. Derive the full contribution or a controlled
small-rate expansion, including the temporal boundary representative,
before claiming a Gram initial solution with beta_t nonzero.

The helper implements the nonlinear WEAK BULK directional action, including
the physical boundary flux, and checks its zero-shift embedding and first/
second directional derivatives. Maximum discrepancies are 1.777e-15 for
embedding, 1.172e-14 for first variation and 1.214e-5 for a centered second
Taylor coefficient of size roughly 37-38. These are midpoint controls,
not interval certificates of nonlinear evolution. They use the stored
floating bulk normalization, while the certified pairing uses rational 1/10.

The Gram first variation and coupled cancellation are enclosed separately.
A complete nonlinear broken-shift Gram action, including second-order
transport, trace choices and all temporal boundary terms, is NOT implemented
or certified here. The inherited smooth Gram quadratic construction remains
available in `scripts/annular_metric_link_quadratic_20260909.py`; it cannot
be transferred to new interface functions without checking those details.

The smooth old and weak finite quadrature actions differ by
[J_beta]-Q[partial_R J_beta]. Its first variation at beta=0 vanishes, but
its quadratic contribution must not be discarded. This prototype does not
establish that nonsmooth spacetime metrics are acceptable physical solutions.

## 6. The new mass equations are tested, not hidden

Every mass lift H vanishes at the original nodes and physical endpoints.
Consequently its Gram mass variation and outer boundary term vanish at
the embedded beta=beta_t=0 state. Its new Euler covector is exactly

    E_added=Q[ell_mu H+ell_muR H_R].

All 18 cases enclose a strictly nonzero E_added. This is the precise reason
the successful enlarged SHIFT solve is not yet a full parent solution.
It does not mean the new prototype is impossible; its initial metric/lapse
fields or its action-derived shift momentum/rate must be solved consistently.

Representative outward-rounded infinity-norm bounds at saved time 0.01:

| Intervals | Branch | Change in reconstructed mass rate | Added mass Euler rows at beta=beta_t=0 |
| --- | --- | --- | --- |
| 16 | GR | [1.58680e-6,1.58722e-6] | [8.47130e-5,8.47951e-5] |
| 16 | metric-Gram | [2.60517e-6,2.60634e-6] | [8.50464e-5,8.51286e-5] |
| 32 | GR | [2.61094e-7,2.64625e-7] | [4.39432e-5,4.41137e-5] |
| 32 | metric-Gram | [6.39035e-7,6.48546e-7] | [4.33693e-5,4.35402e-5] |
| 64 | GR | [2.18502e-8,2.48185e-7] | [2.13837e-5,2.17514e-5] |
| 64 | metric-Gram | [1.57760e-7,7.46653e-7] | [2.12116e-5,2.17124e-5] |

These are basis-dependent code quantities, not SI observational residuals.
The new mass tests have a different normalization from earlier lapse tests.
Neither their sizes nor the mesh trend is a GR/MTS physical fit statistic.

## 7. Evidence and next calculation

The 319 checks include map preservation, original/projected/enriched/base
inverse comparisons, positive local bubble blocks, Gram cancellation,
orthogonality and pairing identities, both sets of shift equations, GR
controls, bulk action controls, and exact archive roundtrips. The inherited
IEEE outward-arithmetic assumptions and realized binary maps remain explicit.
No ideal-basis/continuum quadrature construction certificate is substituted.

Sources and outputs:
- `scripts/annular_joint_weak_action_20260910.py`
- `scripts/derive_annular_joint_weak_action_20260910.py`
- `source-intake/navier-stokes/20260910/annular-joint-weak-action-attempt01/status.json`
- `source-intake/navier-stokes/20260910/annular-joint-weak-action-attempt01/canonical_N64_metric_Gram_sample64.npz`
- `source-intake/navier-stokes/20260910/annular-joint-weak-action-final-integrity.json`

All 18 array archives and executed sources are retained, as are probe01,
probe02 and probe03. The final seal binds the inherited evidence, this note
and a resume snapshot. The protected-workbench check is an mtime scan since
this turn began, not a full pre-turn hash baseline.

**Next concrete target:** derive the enlarged initial Legendre/constraint
system, including the shift-rate term just exposed. Start with the smallest
GR case, with the same boundary data, then use the Gram case. Solve the
added mass and lapse equations together; do not force beta_t=0 unless the
equations support it. Account for the nonunit Gram time Jacobian above,
not just the bulk momentum formula. Derive the temporal/interface contributions needed
at that order before promoting the solution. If a consistent initial jet is
obtained, then enclose its local persistence and test refinement.

Do not return to hunting unspecified couplings: the Gram first-variation
cancellation and compatible mass lift are now explicit. Do not evolve only
the new shift solution while ignoring the added mass equations. No full
parent constraint-preservation, local-GR, continuum or horizon claim is made.
Everything stays private; no production files, galaxy work or GitHub state
were changed, and no worker is needed after sealing this checkpoint.
