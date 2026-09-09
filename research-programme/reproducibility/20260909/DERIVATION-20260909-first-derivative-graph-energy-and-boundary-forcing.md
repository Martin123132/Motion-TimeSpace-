# First-derivative graph energy with the boundary driving retained

2026-09-09. Private continuation of
`DERIVATION-20260909-mass-trace-control-and-bulk-commutator-bound.md`.
No action, trajectory, boundary-data or physical boundary-offset changes.
No GitHub action. This is a conditional scalar energy derivation, not a
proof of the complete coupled MTS system or local-GR recovery.

## 1. Outcome

An explicit positive higher energy now controls the scalar velocity's
first spatial derivative. Its exact evolution identity includes metric
coefficient work, boundary driving, nonlinear forcing and scalar-equation
residuals. The canonical Gram term is included in the energy itself.

The first bound had a problem in BOTH GR and MTS: the norm used for
boundary forcing grew roughly by sqrt(2) per grid doubling. Rather than
discard the cases or tune the boundary data, a boundary-adapted energy was
derived. Its source norm remains near 0.07 on the tested grids instead of
growing from about 13 to 26.

The final-time upper energy-rate bound is about 0.042 for both branches
across N16/N32/N64. This is numerical support for the revised estimate,
not a uniform-in-mesh/time theorem. The metric/source bounds and nonlinear
closure conditions still need derivation.

## 2. The canonical matrices really come from the action

Use c=(chi,s), v=(q,v_s), and the same released Hermite reconstruction:

    B=[H_chi,H_I/h],  D=[G_chi,G_I/h],
    F=1-2mu/R-Lambda R^2/3.

For the canonical scalar sector on the evolving zero-shift chart,

    M=B^T W diag[R^2/(N sqrt(F))] B,
    K=D^T W diag[R^2 N sqrt(F)] D
        +B^T W diag[R^2 N m_chi^2/sqrt(F)] B
        +K_Gram.

K_Gram acts in the nodal chi block and is

    K_Gram,chi=T^T diag[S a0] T/h,
    a0=R_node^2 N_node sqrt(F_node).

Omit this term in the GR comparator. With N,F positive, m_chi^2>=0,
positive quadrature and the existing nonnegative S, M is positive and
K is nonnegative. After homogeneous scalar-value Dirichlet restriction,
K is positive: its radial quadratic form has no nonzero constant in
that restricted space. No slope-value boundary conditions are added.

For the canonical fixture these are the ACTUAL scalar kinetic/stiffness
matrices, not a fit to the trajectory. Matrix time derivatives include
the Gram coefficient rate. For the bulk weights,

    d_t log M_weight=-N_dot/N+mu_dot/(RF),
    d_t log K_radial_weight=N_dot/N-mu_dot/(RF),
    d_t log K_potential_weight=N_dot/N+mu_dot/(RF).

Their analytic derivatives are checked against independent complex
metric paths. The canonical kinetic matrix also agrees with the existing
released-action implementation.

For the nonlinear P(X) fixture, use this canonical quadratic part as a
reference and retain the remaining Euler force explicitly. This is NOT
a proof that the nonlinear Hessian equals M or that the nonlinear force
is an independently prescribed bounded source.

## 3. Remove only the prescribed scalar trace from the coordinates

Let l(t) be the affine-in-R scalar extension of the existing endpoint
values. Its Hermite slope coordinates are chosen to reconstruct precisely
that affine function. Its first and second time derivatives use the SAME
endpoint velocity and acceleration histories as the saved runs.

Write c=P u+l, where P inserts the free coordinates and has zero entries
at the two scalar-value endpoints. All interpolation-slope coordinates
remain free. Then w=u_dot.

In the following formulas M,K and their derivatives denote the restricted
matrices P^T M_full P, P^T K_full P. The free equation is

    M w_dot+M_dot w+K u=f_b+g,

    f_b=-P^T(M_full l_tt+M_full_dot l_t+K_full l),
    g=P^T(E_nonlinear-E_total).

Here E_total=L_c-d_t Pi is the independently evaluated full scalar Euler
covector. The nonlinear Euler force is derived by varying the difference
between the full P(X)/Gram action and the canonical quadratic part.
It vanishes identically on the canonical fixture. Nonlinear momentum
derivatives include the actual scalar acceleration and coefficient jets.

The lift is a change of variables, not new dynamics or a new boundary
condition. The boundary source depends on both prescribed traces and the
evolving metric; it is not an arbitrary function available for fitting.
Off-shell checks perturb accelerations and verify that the residual
force cannot be dropped.

## 4. First graph energy and the exact identity

Set a=M^-1 K u and

    E1=(w^T K w+a^T M a)/2.

This is a higher regularity energy, not an additional physical conserved
quantity or a replacement for the earlier constrained boundary energy.
Differentiation and use of the forced equation give

    d_t E1 =
      (M^-1(f_b+g)-M^-1 M_dot w)^T K w
      +a^T K_dot u
      -a^T M_dot a/2+w^T K_dot w/2.

No second metric time derivative is needed for this identity. For frozen
positive M,K and homogeneous zero forcing it gives exact conservation.
That special case is checked for both canonical branches; it is not
silently substituted for their evolving metrics or driven boundaries.

## 5. Explicit growth constants

Let ||x||_M^2=x^T M x, and sym(A)=(A+A^T)/2. Define generalized
quadratic-form operator norms

    alpha_M=||M^(-1/2) M_dot M^(-1/2)||,
    alpha_K=||K^(-1/2) K_dot K^(-1/2)||,
    alpha_A=||K^(-1/2) sym(K M^-1 M_dot) K^(-1/2)||,
    alpha_L=||M^(-1/2) sym(K_dot K^-1 M) M^(-1/2)||.

Using u=K^-1 M a in the stiffness-rate term gives

    C=max(2alpha_A+alpha_K, 2alpha_L+alpha_M),
    d_t E1 <= C E1+sqrt(2E1) ||M^-1(f_b+g)||_K.

These finite-matrix bounds are derived, not regression coefficients.
The implementation uses symmetric generalized eigenvalue problems rather
than forming principal matrix square roots. A proportional-matrix control
recovers the exact rates on all three grids.

Their finite-state values alone do not prove uniform bounds as h tends
to zero. In particular kinetic positivity by itself does not control
alpha_A or alpha_L in the required stronger norms.

## 6. The first forcing estimate is unnecessarily costly

At final time, the old total forcing graph norm is:

| fixture / branch | N16 | N32 | N64 |
|---|---:|---:|---:|
| canonical GR | 12.756 | 18.135 | 25.714 |
| canonical candidate | 12.844 | 18.258 | 25.887 |
| nonlinear GR | 13.151 | 18.695 | 26.508 |
| nonlinear candidate | 13.241 | 18.822 | 26.687 |

The original E1 itself stays finite and comparable across the grids.
The observed forcing-norm growth is consistent with forcing a boundary
trace through the homogeneous-Dirichlet graph norm; it is not evidence
that the physical solution has developed an instability. GR shows the
same issue, so declaring an MTS failure here would be unjustified.

The exact identity remains correct. Its Cauchy-Schwarz estimate asks for
more boundary regularity than necessary. The next section removes that
particular norm from the boundary term by changing the ENERGY, not the
action, state or prescribed boundary data.

## 7. Derived boundary-adapted energy

Define

    b=M^-1(Ku-f_b),
    Ehat1=(w^T K w+b^T M b)/2.

Both quadratic terms are nonnegative. The subtraction here is of the
DETERMINED driving covector inside the definition of a higher energy.
It is not subtraction of the physical r_a/r_b offsets, a mass-flux
counterterm, or modification of any equation.

The free equation now reads w_dot=-b-M^-1 M_dot w+M^-1 g.
Direct differentiation gives the exact identity

    d_t Ehat1 =
      (M^-1g-M^-1 M_dot w)^T K w
      +b^T(K_dot u-f_b_dot)
      -b^T M_dot b/2+w^T K_dot w/2.

Since u=K^-1(Mb+f_b), define

    h_b=K_dot K^-1 f_b-f_b_dot.

The same growth constant C from section 5 then gives

    d_t Ehat1 <= C Ehat1
       +sqrt(2Ehat1)[ ||h_b||_(M^-1)+||M^-1g||_K ].

Only the remaining nonlinear/residual force uses the K graph norm.
Boundary driving now enters in the weaker M-dual L2 norm. Its rate work
is explicitly retained; treating it as zero fails the derived identity.

If c_* is a positive lower bound for R^2 N sqrt(F), the radial term in K
also gives

    ||q_h,R||_W <= sqrt(2 Ehat1/c_*)+||(l_t)_R||_W.

The positive Gram addition preserves this estimate. This supplies the
energy-to-first-derivative link requested by the previous commutator bound.
Uniform control still requires a uniform positive chart and bounds on
C, h_b and the remaining forcing.

## 8. How the boundary rate is obtained, and its limitations

The saved boundary scalar histories are quadratic in time, so l_ttt=0.
Differentiating the determined boundary source gives

    f_b_dot=-P^T[
       2M_full_dot l_tt+M_full_ddot l_t
       +K_full_dot l+K_full l_t ].

For m=R^2/(N sqrt(F)), write

    r=-N_dot/N+mu_dot/(RF),
    r_dot=-N_tt/N+(N_dot/N)^2+mu_tt/(RF)
                           +2(mu_dot/(RF))^2,
    m_tt=m(r^2+r_dot).

Thus M_ddot has an explicit analytic formula once the metric second jet
is specified. That formula agrees with a separately differentiated M_dot.

The actual local second jets are calculated as directional derivatives of
the EXISTING differentiated-constraint ODE, using centered increments
2e-5, 1e-5 and 5e-6. They are not guessed accelerations or new parent
coefficients. No trajectory is reprojected or reintegrated.

Some whole-state acceleration differences reach a numerical-noise floor
rather than decreasing monotonically. This is recorded; it is not claimed
as clean high-order convergence. The resulting boundary-rate covector is
stable at the two finer increments within the declared validation tolerance.
These are floating-point local derivatives, not interval-certified jets
or a bound valid at all times.

An independent quadratic field/metric-jet path on N16 also reproduces
the energy derivative. At every saved state a complex first-jet energy
variation agrees with the exact work identity.

## 9. What the matched controls actually show

All initial/mid/final samples of both fixtures, all three grids and both
branches are retained: 36 states. No new long numerical evolution.

Final-time boundary-adapted results:

| fixture / branch | grid | Ehat1 | C | boundary source norm | upper energy-rate bound |
|---|---:|---:|---:|---:|---:|
| canonical GR | N16 | 0.161439 | 0.000681 | 0.073453 | 0.041848 |
| canonical candidate | N16 | 0.161636 | 0.000670 | 0.073452 | 0.041871 |
| canonical GR | N32 | 0.161440 | 0.000666 | 0.073620 | 0.041941 |
| canonical candidate | N32 | 0.161462 | 0.000666 | 0.073617 | 0.041942 |
| canonical GR | N64 | 0.161441 | 0.000661 | 0.073704 | 0.041987 |
| canonical candidate | N64 | 0.161443 | 0.000661 | 0.073705 | 0.041988 |
| nonlinear GR | N64 | 0.175949 | 0.000727 | 0.071281 | 0.042673 |
| nonlinear candidate | N64 | 0.175952 | 0.000728 | 0.071283 | 0.042758 |

The actual final Ehat1 time derivatives are approximately 0.0305-0.0307.
The original E1 derivatives were negative: these are DIFFERENT energy
functionals on IDENTICAL trajectories. The change in derivative sign is
not physical heating, damping or an improvement to the solution.

The growing old boundary-forcing norm has been replaced by a nearly
grid-stable source norm in the revised estimate. This is a useful result
about the estimate and the tested branch, not a proof that every constant
remains bounded on an infinite mesh sequence or long time interval.

In the canonical cases the remaining forcing graph norm is roundoff-sized.
In nonlinear N64 it is about 4.39e-4 for GR and 5.79e-4 for the candidate.
That nonlinear term is still acceleration-dependent, and its norm is not
uniformly bounded by this calculation. The forced canonical identity
must not be promoted into a closed nonlinear energy theorem.

## 10. Unsatisfied equations have not disappeared

Scalar free-row residual forcing is explicitly retained and tested off
shell. The full shift vector and mass-rate mismatch remain saved and
nonzero. No row is erased on the grounds that an energy identity passes.

In the original graph energy, direct mass-mismatch contributions to
M_dot,K_dot and boundary-lift work are separately computed by the linear
split mu_dot=mu_dot,V+d, keeping the actual lapse rate. This is not a
claim to isolate every indirect dependence of the lapse/metric evolution.

The adapted energy uses the FULL actual metric first and second jets.
It does not supply an independent uniform estimate for those jets or for
the mismatch's time derivative. Those dependencies remain in C and h_b.
Accordingly this is conditional scalar control along the current
differentiated-constraint branch, not closure of the full scalar/metric
DAE or proof that d or the physical boundary offset vanishes.

## 11. Evidence and execution

New implementations:

- `scripts/annular_first_derivative_energy_20260909.py`
- `scripts/derive_annular_first_derivative_energy_20260909.py`
- `scripts/annular_boundary_adapted_energy_20260909.py`
- `scripts/derive_annular_boundary_adapted_energy_20260909.py`

Completed owners:

- `source-intake/navier-stokes/20260909/annular-first-derivative-energy-derived/status.json`: 499/499 checks.
- `source-intake/navier-stokes/20260909/annular-boundary-adapted-energy-derived/status.json`: 339/339 checks.
- `source-intake/navier-stokes/20260909/annular-first-derivative-energy-final-integrity.json`: combined source/output/citation and protected-path verification, sealed by the adapted-energy runner.

These counts validate implementation and provenance, not physical claims.
All new computations use one BelowNormal single-core worker at a time,
with bytecode disabled. No shared processes, old evidence or public
repositories are changed.

## 12. Next mathematical target

Do not derive the same energy identity again or repeat the bad boundary
forcing test. The next target is the UNIFORM coefficient/source estimate:

1. Bound alpha_A and alpha_L analytically using the actual mixed/Hermite
   projection, positive metric bounds and spatial coefficient derivatives;
   do not take the three-grid eigenvalue trend as a proof.
2. Use the metric constraint/evolution relations to bound the first and
   second metric jets entering C and h_b, with all shift mismatch forcing
   accounted for. Start with the canonical GR control and then Gram.
3. After canonical closure is established, absorb or symmetrize the
   acceleration-dependent P(X)/Gram correction instead of merely assuming
   its forcing norm is bounded.

The finite frozen-metric canonical energy law is exact. The evolving
canonical energy inequality is derived but conditional. The full
nonlinear, coupled and horizon-level conclusions remain open.
