# Accumulated pressure-work error in the retained coupled model

Private; reuse completed3041..3044 histories, not a new physical evolution.
Previous goal turn made verified progress through3044. Keep full MTS objective.
This calculation connects the already-derived field residual to a physical
energy-exchange channel. It does not derive the supplied background tables.

Let e=approximate-parent, split at3041 into inherited h and generated f:
e=h+f, h'=A h, f'=A f-r. These are full coupled native perturbations with
all surrounding species and the same homogeneous background in each branch.
The approximation's field residual r is already derived, not fitted here.

For the weighted scalar pressure S_P=B_P y, the retained work accumulator
obeys Wp'=-3 H S_P. Since both trajectories use identical backgrounds,

    Delta Wp'=-3 H B_P e,
    J_h'=-3 H B_P h, J_f'=-3 H B_P f,
    Delta Wp(t)-Delta Wp(t0)=J_h(t)+J_f(t),
    J_h(t0)=J_f(t0)=0, t0=the saved3041 split.

There is no additional explicit r in this work derivative: r acts through
the field evolution, while the pressure readout is algebraic. Other density
and current balance channels have their separately retained defect terms.
The subtraction of Delta Wp(t0) is essential: the physical matching was3040,
not3041. The stored total error and K1/K2 are never reset.

For any error vector z=(z_f,z_g), the actual source convention gives

    P[z]=beta*(V*z_g-mu^2*Phi*z_f), beta=a/density0, mu=a*m_h.

Use saved native units and conformal time in Mpc. Wp has the weighted source
normalization and H has units Mpc^-1. The integral therefore has Wp's units.
No change to scale factor, clocks, mass or normalization is introduced.

## Stable original/change equations

Write P_1=P_0+deltaP and H_1=H_0+deltaH. For z=h,f,e, compute pressure
changes using exact paired multiplication, including every cross term:

    J_z,0'=-3 H_0 P_z,0,
    deltaJ_z'=-3*(H_0*deltaP_z+deltaH*(P_z,0+deltaP_z)).

The original and coherent non-cancelling integral estimates are

    U_b=integral 3*|H_b|*(|P_h,b|+|P_f,b|) dt, b=0,1.

The branch-change estimate is

    U_delta=integral 3*(|H_0|*(|deltaP_h|+|deltaP_f|)
               +|deltaH|*(|P_h,1|+|P_f,1|)) dt.

Thus |J_h,b+J_f,b|<=U_b and |deltaJ_h+deltaJ_f|<=U_delta for exact histories.
Signed and non-cancelling quantities will both be reported. No averaging of
oscillating pressure and no fitted growth exponent are permitted.

## Frozen numerical experiment

Reuse complete saved32/64 histories through3044, including identical joins.
Recompute their actual RHS at saved nodes with one fresh retained native owner
at a time. This is evaluation only: do not integrate or change physical fields.
Extract17 physical jet components:5 homogeneous changes and the old/change
heavy-field components of h,f,e. Preserve exact native units and layout.
Check pressure reconstruction against saved source packets and full final RHS.

Within each original saved interval, use THREE-node Hermite interpolation
(degree5) matching values and actual derivatives. Integration nodes lie inside
the bracketing interval. Compare diagnostic knot strides1,2,4, always retaining
the original epoch boundaries. These are interpolation tests, not changes to
the original physical or frequency grids. Gauss-Legendre orders3,5,7 are fixed
before evaluation; include a separate two-node cubic control at stride1/order7.
Verify both Hermite representations on manufactured polynomials first.

Integrate J_h,J_f,J_e and all three U estimates. Compare against the INDEPENDENT
saved parent/approximation work increments, never use those increments as the
definition of predicted work. Add fine-versus-coarse diagnostic interpolation,
quadrature,32/64 trajectory and primitive-rounding differences. Report both
successive refinement differences and their contraction; do not turn a sampled
refinement estimate into a certified continuum theorem. Absolute-value kinks
can slow convergence of U; its numerical uncertainty must remain visible.

Keep unchanged2e-5 numerical/1e-10 algebraic gates. Separate error-relative
resolution from comparison relative to full physical work/branch response.
An unresolved very small error is not a physical failure or proof of zero.
No physical continuation is automatically authorized by loose full-scale norms.
This stage ends after diagnostics; choose a longer test only from its evidence.

Baseline gets the same cached-work/pressure-zero checks: the owned cold source
has zero pressure by construction, not all cosmological matter. No claim that
baseline tiny velocity response or other prior uncertainty is fixed.

Freeze source hashes before jets/quadrature. One worker/thread below-normal,
no other-chat actions, no GitHub, no native rebuild. Stop safely before13:25UTC.
