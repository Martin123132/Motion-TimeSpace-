# Constrained initial-slice solve and mass-flux tangent

Date: 2026-09-09. Private local continuation. No public or local-GR claim.

## 1. What changes in this step

The saved affine geometry defects have now been used in an actual square
Newton correction, not merely listed again. Both canonical and nonlinear
P(X) references, with and without the covariant Gram candidate, solve all
free initial radial/Legendre equations on N=16,32,64 local patches. Twelve
systems converge in one Newton step from the reference data. Independent
perturbed starts on N16 return to the same roots. No pseudoinverse,
least-squares fit, diagonal regularizer or projected bad row is used.

The follow-on time-compatibility test is NOT closed. It gives a nonzero
mass-rate disagreement in both GR/P(X) and Gram branches. The Gram error
is larger but decreases by about four per halving of grid spacing here.
The distinction between an initial constraint root and a constrained
evolution is therefore now measured, not assumed.

Prior derivation: `DERIVATION-20260909-shift-unfixed-GR-and-local-quadratic-clock-action.md`.

## 2. A stated local boundary problem, not an invented global completion

Use the same owned orthogonal patch R in [5.875,6.125], at old anchor time
0.15. The old advanced-time domain [0,0.5] is respected. V=V_t=0 specifies
the orthogonal radial constraint branch, after the shift-unfixed action
and its variations have been derived. It does not discard the shift test.

Let F=1-2 mu/R-Lambda R^2/3, L=F^(-1/2), E=NL, q=chi_t, and
X=-q^2/N^2+F w^2. K=-X/2-m_chi^2 chi^2/2+b2 X^2+b3 X^3, P=-2 K_X.
The local Routh functional is

    Routh = integral [NL mu_R/kappa + R^2 NL K] dR
            - U_Gram (candidate only)
            - pi_interior^T q_interior - E_b mu_outer/kappa.

The single common pi_interior is the GR/P(X) canonical momentum evaluated
at the reference data, independently checked against the full ADM matter
action. Comparing the two branches at equal canonical phase data is more
precise than silently keeping q fixed when the momentum law changes.

Fix the inner mass and both scalar endpoint velocities to the reference
data. Keep ALL lapse variables free. Prescribe the reference outer clock
E_b=N_b/sqrt(F_b). The written boundary Legendre term, rather than deleting
an outer mass equation, supplies its natural variational boundary condition.
The inner mass and scalar endpoint reactions are retained, not scored as
free bulk equations. With n scalar/lapse nodes and n+1 mass faces, the
number of free equations and unknowns is 3n-2.

In the continuum, variation gives the baseline equations

    mu_R = kappa R^2 [P q^2/N^2 - K],
    E_R/E = kappa R P [w^2 + q^2/(E^2 F^2)],
    p_muR = E/kappa,
    pi = R^2 L P q/N.

The E-chart identities are symbolically checked; the finite system is
assembled directly in its actual face-mass/nodal-lapse basis, not obtained
by pretending nonlinear changes of coordinates commute with interpolation.
The weak outer natural row includes volume terms. Its nodal E trace need
not equal E_b exactly at finite resolution: the measured discrepancy drops
from about 1.58e-7 to 1.01e-8 between N16 and N64. No lapse row is dropped.

This is a chosen, explicit local patch boundary-value problem. A globally
admissible physical interface/horizon boundary completion and the full
hyperbolic characteristic count have NOT been established by this choice.

## 3. The initial constraint roots are real numerical progress

The nonlinear Newton Hessian is the analytic second derivative of the same
Routh functional. Its gradient is checked by independent complex-step
action variations; Hessian-vector products by two central-difference steps.
Shared row/unknown scaling is computed once from the GR seed Hessian, then
used unchanged for both branches. Positive metric/principal branches and
the positive free-scalar Legendre block are enforced throughout.

All twelve systems take one accepted full step. Maximum raw free residual
is at most 4.77e-13 in the fixture normalization; at N64 it is below
4.18e-15. Scaled Jacobian condition numbers range from about 20 to 77.
These are floating-point checks, not interval-certified existence bounds.

Candidate-minus-GR maximum mass corrections:

| fixture | N16 | N32 | N64 |
|---|---:|---:|---:|
| canonical | 1.717e-8 | 1.062e-9 | 6.583e-11 |
| nonlinear | 1.944e-8 | 1.205e-9 | 7.468e-11 |

The mass, lapse and velocity corrections and full residual vectors are
saved, not only these maxima. Roughly fourth-order decay of this difference
on the three smooth profiles is NOT a universal GR-limit theorem. The
small Gram term here is not a fitted physical MTS coupling measurement.

Removing the outer boundary action produces an order-ten free residual.
That negative control confirms why the earlier large endpoint covectors
were boundary work, not a gravitational instability to be erased.

## 4. Lapse rate and the remaining evolution condition

Write y=(mu_faces,N_nodes,q_nodes) and G=partial_y Routh. Differentiating
the free constraints at a solved root gives

    H_ff ydot_free = -G_data_dot_free - H_fc ydot_fixed.

Here chi_dot=q and pi_dot=partial_chi L are used, with the full scalar
Gram force and the actual nonzero lifting. I=w-D chi and I_t remain
the supplied reference lifting data. Their declared time-jet continuation
has I_tt=-D chi_tt_reference. Scalar endpoint accelerations and E_b_dot
are those of the explicitly declared reference path. This is not an
arbitrarily extrapolated parent solution.

The shift equation independently gives

    B mu_dot_flux + J_matter - J_Gram = 0,
    B=Q_face^T diag(weights/(kappa N F^(3/2))) Q_face > 0.

The Gram current includes BOTH its direct coefficient variation and the
finite time-link current after the explicit time-boundary subtraction.
The inner mass rate is taken from this flux solve, not imposed from the
old off-shell reference history. The differentiated free constraints then
determine the other mass rates, N_dot and q_dot. All remaining shift rows
are evaluated and saved, without forcing them to zero.

The precise compatibility obstruction is

    R_shift = B (mu_dot_constraint - mu_dot_flux).

This equality is checked from separate saved arrays. Nonlinear root-family
probes at +/-0.001 and +/-0.0005 independently reproduce the constraint
tangent; maximum errors at the smaller step are below 4.22e-10. These are
neighboring parameterized initial roots, not claimed time-evolved solutions.
Full ADM shift variations and finite nonlinear Gram link variations also
verify the flux covectors. Freezing N_dot fails a negative control.

Maximum mass-rate disagreement, in the fixture normalization:

| fixture/branch | N16 | N32 | N64 |
|---|---:|---:|---:|
| canonical GR | 9.139e-7 | 6.493e-7 | 2.237e-7 |
| canonical Gram | 1.640e-5 | 3.836e-6 | 9.129e-7 |
| nonlinear GR | 1.156e-6 | 8.576e-7 | 2.807e-7 |
| nonlinear Gram | 1.637e-5 | 3.837e-6 | 9.259e-7 |

At N64 the Gram disagreement is about 0.09% of the maximum mass flux,
versus about 0.02-0.03% for GR/P(X). These ratios are numerical diagnostics,
not observational tolerances. Gram adjacent measured orders are 2.05-2.10.
The GR control also improves, but has not reached a uniform clean order.
No branch passes exact shift closure, and no stability/causality verdict
or continuum error bound follows from these three profiles alone.

## 5. The boundary and lifting terms cannot simply be removed

The forcing and tangent are split additively at each fixed root into:
internal canonical evolution with flux-derived inner mass rate; lifting
rates; outer clock rate; and scalar endpoint accelerations. The full vector
sum is verified, including cancellations; component maxima are not added
as if they were aligned physical errors.

At canonical N64 the separate internal and scalar-boundary mass-rate
contributions have norms about 1.04e-5 and 1.11e-5 for Gram. They substantially
cancel. Omitting both prescribed boundary rates increases the final error
from 9.13e-7 to 1.04e-5. Omitting the lifting contribution also worsens it,
to 9.53e-7. The nonlinear and GR comparisons support the same caution.
These omissions are diagnostic vector subtractions only: no accepted root,
source field or boundary condition was changed to obtain them.

Thus the remaining error is not explained by merely forgetting to set
the lapse rate, or repaired by deleting a difficult boundary/lifting term.
The split is an operational forcing decomposition, not a proof assigning
a unique physical cause to the residual.

## 6. Next derivation, with its exact starting point

Derive the local time-reparametrization identity of this SAME mixed action,
including the lifted scalar basis and its boundary work, and express the
saved R_shift as explicit reconstruction/product-rule remainders. Do not
launch another coefficient hunt or add an empirical mass-flux counterterm.

For a time-independent local generator f(R), the nodal relation w=D chi+I
already implies the required infinitesimal lifting transformation

    delta I = f (D q + I_t) + q (D f) - D(f q)
            = f I_t - [D(f q)-f Dq-q Df].

This is a chain-rule requirement for the chosen nodal generator, not a
new evolution law for I. The metric generator, its face/node reconstructions,
the full action and endpoint variations must be treated together. A fixed
prescribed lifting is not automatically a freely varying covariant field.
The next step should derive that identity and either bound the observed
remainder or derive the necessary slope/interface dynamics from the action.
It must NOT tune I_t or a boundary datum to cancel the saved residual.

Successful initial constraints are now behind us on these fixtures. The
next missing result is time-compatible constrained evolution, not another
initial-data root. Full parent calibration, global boundaries, local GR,
black-hole regularity and empirical MTS predictions remain separate gates.

## 7. Evidence and reproducibility

All paths here are relative to this post-checkpoint-work directory.

- `scripts/annular_constraint_routhian_20260909.py`: nonlinear action derivatives, positive-branch Newton solve, scalar force, shift flux and constraint tangent.
- `scripts/derive_annular_constraint_routhian_20260909.py`: completed 196/196 checks and twelve saved roots, Hessians, residuals and tangents.
- `scripts/verify_annular_constraint_tangent_20260909.py`: completed 134/134 independent tangent/flux checks.
- `scripts/derive_annular_constraint_work_split_20260909.py`: completed 40/40 additive forcing/vector checks.
- `source-intake/navier-stokes/20260909/annular-constraint-routhian-derived/status.json`.
- `source-intake/navier-stokes/20260909/annular-constraint-tangent-verified-full-fixture/status.json`.
- `source-intake/navier-stokes/20260909/annular-constraint-work-split-derived/status.json`.
- `source-intake/navier-stokes/20260909/annular-constraint-routhian-final-integrity.json`.

One checker attempt is preserved as failed 120/132 in
`source-intake/navier-stokes/20260909/annular-constraint-tangent-verified/status.json`.
Its sole failure was comparing the complete fixture parameter dictionary
(which also contains G and r0) to a four-key subset. All calculations used
the complete fixture in both attempts. The rerun fixes that metadata check,
retains its executed-source snapshot, and changes no mathematical tolerance.

370 final checks validate implementations and the stated conditional results;
they are not 370 independent confirmations of a fundamental theory.
All computations finished, single-core BelowNormal. No subagents, GitHub
actions, shared-process stops, frozen-workbench or galaxy edits.
