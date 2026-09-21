# Flux-moment lifts and canonical boundary power

Private, 2026-09-12. This extends the NEW finite scalar-action candidate in
`DERIVATION-20260912-joint-covariant-initial-data-and-boundary-energy-law.md`.
The earlier passing old-action first-jet branch is unchanged. No evolution,
publication, physical fit, full GR limit or completed field theory is claimed.

## 1. Outcome

We constructed continuous mass-coordinate corrections for the ENTIRE
16-dimensional transported-current family, not just the actual current
amplitude. The construction satisfies all 19 gravity-constraint derivative
moments and both endpoint traces at its construction geometry. It retains
all old mass phase columns and adds 16 canonical pairs, 79 to 95.

After recomputing the coupled equations, the current family changes. One
construction and four bounded feedback iterations do not give a stable full
first-jet pass. They are preserved, not adopted or cherry-picked.

Separately, deriving power balance from the actual finite canonical
boundary action exposes a mismatch in the previous boundary condition:
raw continuum flux f was being used in a finite system whose mass velocity
is the projected v. Correcting that distinction, and preparing the actual
imposed mass velocity, reduces the unextended candidate's full C1 residual
to 3.35e-8 GR/3.27e-8 MTS. The original 1e-10 gate remains unmet.

The new preferred SMALL diagnostic is original79 with canonical port
power, not any 95-dimensional trial. This is not a replacement for the
separate old-action working branch.

## 2. A constructive continuous lift theorem

Let Q,P be the old mass configuration/momentum maps, W the positive radial
quadrature, M=P^T W Q, and Pi=Q M^-1 P^T W. Nodal evaluations are carried
separately. Let F contain all 16 normalized current carriers

    F_j(R)=c_P(R) exp(-2g(R)) 1_cell_j(R),

and let L stack the 19 full mass derivatives of C0 and the two physical
endpoint evaluation functionals. Write E=L(F)-L(Pi F).

Seek a CONTINUOUS H from nodal hats and the existing continuous bubbles:

    P^T W H=0,    L(H)=E.                             (1)

After normalization Hn=H T, seek added momentum Z satisfying

    Z^T W Q=0,   Z^T W Hn=I,
    Z^T W F=T^-1,   Z_in=Z_out=0.                    (2)

The first two equations give the extended canonical pairing diag(M,I).
Consequently

    Pi_extended F=Pi F+H,
    L(Pi_extended F)=L(F).                           (3)

This is an algebraic proof, conditional on the two moment systems being
solvable and the normalization retaining rank. The discontinuous carriers
are used only in the already broken momentum space; they are NOT inserted
into the continuous mass-coordinate space. Thus (1)-(3) do not silently
change the mass function space or require a new physical coupling.

In this fixture the continuous moment system is 100 by 145, rank 100;
the momentum system is 113 by 161, rank 113. All 16 correction directions
are retained. The canonical pairing condition is about 1.664, although
the construction moment systems themselves have small singular values
(down to order 1e-8/1e-7). A well-conditioned pairing alone is not a
stability certificate for constructing the basis or evolving it.

At the construction geometry, normalized-family C0 moment errors are
1.39e-12 GR/2.13e-12 MTS, endpoint errors below 1.72e-14. Old phase columns
are retained exactly. The source amplitudes are not fit.

## 3. Recomputing matters: frozen and feedback trials

The new momentum space changes P1, hence g and the transported family.
We therefore reprepare all initial constraints/drives, recompute P1, J,
chi1, p1 and mu1, and test the regenerated family at both quadratures.
There is no transfer of the construction certificate to a different g.

With the previous RAW-flux port law, the one-pass C1 maxima become
8.82e-7 GR/1.03e-7 MTS. The regenerated all-family moment defect is around
7e-5, not the construction error of 1e-12. This is not a full repair.

Four additional feedback constructions were tested per branch, always
rebuilding from the original 79 columns rather than growing the dimension
again. They keep the phase at 95. The generator change decreases at first
but increases again: no contraction is established. The last C1 values
are 1.05e-7 GR/3.23e-7 MTS under raw-flux ports; smaller intermediate values
were not selected as a success. The fixed feedback budget is finished.

## 4. Correct finite boundary power, without fitting C1

The previous raw rule was

    rho_b q_b=-n_b K_b
             =n_b N_b f_b/(kappa U_b),
    f=-c_P K, U=sqrt(F), n_in=-1,n_out=+1.

It is the appropriate expression when the mass velocity equals the raw
current. In the finite canonical system, however,

    v=Q M^-1 P^T W f

is the actual mass velocity. The source action already contains the inner
metric reaction lambda_in=N_in/(kappa U_in) and the outer clock term
-C_out mu_out/kappa, with N_out/U_out=C_out. Their power is determined by
v (or the imposed inner velocity once its constraint is satisfied), not
by a different diagnostic current.

Within the SAME endpoint-by-endpoint balanced-power branch, the finite
version of that condition is therefore

    rho_in q_in=-lambda_in v_in,
    rho_out q_out=(C_out/kappa) v_out,
    rho_b q_b=n_b N_b v_b/(kappa U_b).                (4)

Global energy conservation alone fixes a total power, not two arbitrary
source histories separately. Equation (4) retains the earlier assumption
of endpoint-by-endpoint balancing; it is not a new uniqueness theorem for
external forces. It supplies instantaneous compatible reactions, not
parent-signed full boundary histories. The undivided equations are required
when q_b=0. This fixture has nonzero endpoint q.

We now solve the actual condition v_in=the signed imposed mass velocity,
alongside 19 C0 rows, outer q drive, clock and projected P1 boundary rows.
The raw condition f_in=the drive is still evaluated as a separate gate.
The difference v-f is NOT erased, redefined away or declared physical.

Define the endpoint part of the C0 mass differential by

    B_eta(delta)=[eta delta/(kappa U)]_in^out.

Changing from the raw rule to (4), at the same state, gives EXACTLY

    C1_canonical[eta]=C1_raw[eta]-B_eta(v-f).         (5)

No C1 row appears in the prescription for rho. Equation (5) is independently
checked in all 12 branch/frame/quadrature comparisons, error below 2.3e-17.

## 5. Global power identity and local error

Write L0=L_mu-B, so it retains bulk and nodal mass derivatives but removes
the explicit radial-boundary evaluation. Let

    W_metric[eta]=integral (eta f/N)(f_bulk-P1) dR
                         +sum_i (eta_i f_i/N_i) s_i.

The complete earlier Ward identity now gives

    C1_canonical[eta]=L0[eta](v-f)+W_metric[eta],      (6)

up to the separately measured integration-by-parts quadrature error.
For eta=N, the metric canonical equation and mass projection give

    C1_canonical[N]=<P1,v-f>_W=0.                   (7)

The actual N lies in the 19-dimensional lapse space; its recovered
coefficients and values are checked, not assumed. Equation (7) holds
numerically to about 1e-17 in every tested configuration. Thus the total
power identity is recovered without pretending that all local constraints
are preserved. The full local Ward reconstruction remains below 2.3e-14.

| Reprepared finite canonical ports, primary C1 | GR | MTS |
|---|---:|---:|
| Original 79-dimensional mass phase | 3.34565e-8 | 3.26653e-8 |
| One-pass 95-dimensional lift | 1.41216e-7 | 1.60435e-7 |
| Last bounded-feedback 95-dimensional lift | 1.10934e-7 | 2.29426e-7 |

Higher quadrature reproduces those values. The larger spaces improve the
interior P1 lapse rows to about 2e-9 but leave larger cubic-test metric
Euler work. The original79 candidate is better on the FULL retained set.
Do not select a sub-block or cancellation-prone feedback iteration as a pass.

For original79, C0 is below 1.13e-13 across both branches/quadratures.
Actual inner drive errors are below 3.2e-12; raw/projected mass endpoint
differences remain 3.56e-9 GR/4.37e-9 MTS. Higher-quadrature P1 endpoint
error remains 5.34e-10 GR/9.29e-11 MTS. Both full first-jet gates are FALSE.
F>.65957, N>.81207 and J remains close to one in these numerical fixtures.

The improvement from the preceding roughly 5e-7 drift is partly a corrected
finite source-power condition, not solely a better bulk approximation.
No physical accuracy or continuum-convergence factor is inferred from it.

## 6. Why fixed-grid smooth perfection is the wrong strong target

There is a useful conditional function-space lemma. Suppose the new nodal
scalar action is varied against ALL smooth compact lapse tests, rather
than only its 19 retained numerical tests, while mu is C1 and F>0. At P=0
the resulting distributional constraint is

    mu_R/(kappa sqrtF)-sum_i sqrtF_i e_i delta(R-R_i)=0.

If an interior e_i>0, this cannot hold with a locally bounded smooth
gravitational density: choose a smooth bump equal to one at that node,
supported in a shrinking interval containing no other node. The regular
integral tends to zero while the nodal term remains -sqrtF_i e_i.

This is a statement about the fixed nodal surrogate and enlarged test
class, NOT a no-go theorem for MTS, GR, the finite 19-row first jet, or a
joint continuum limit. The positive nodal energies are a consequence of
this numerical scalar action. It would be wrong to endlessly enlarge only
the smooth metric space and call the resulting fixed-node distribution an
exact smooth parent solution.

Two mathematically honest continuations are a derived weak/interface
interpretation, or a controlled matter-and-metric refinement. Before a
refinement test, h's role must be checked against the parent operator:
naively rebuilding Gram stencils while changing h can change the correction
itself. Do NOT freely rescale a physical kernel or sell a vanishing stencil
term as a demonstrated physical GR limit. This lemma does not replace the
remaining finite local constraint test with a weaker acceptance gate.

## 7. Next constructive step

Use original79 with (4) as the small new-action diagnostic and keep the
completed old-action branch intact. Work on the remaining LOCAL metric
compatibility in (6), not more raw-power or frozen-current feedback loops.

The immediate derivation is a simultaneous weak metric/Ward representation:
it must control L0(v-f) AND metric Euler work on eta*f/N while respecting
continuous mass and broken momentum spaces, with the full retained lapse
set and fixed physical source operator. If that cannot be justified at
fixed grid, derive the weak/interface or scale-preserving refinement route
instead of adding constraint projection by hand. Full C1, raw/weak flux,
both boundary jets and higher quadrature remain gates before C2/evolution.

## 8. Reproduction and validation

- `scripts/annular_covariant_flux_moments_20260912.py`
- `scripts/derive_annular_covariant_flux_moments_20260912.py`
- `scripts/derive_annular_covariant_flux_feedback_20260912.py`
- `scripts/annular_covariant_canonical_ports_20260912.py`
- `scripts/verify_annular_covariant_canonical_ports_physical_units_20260912.py`
- `source-intake/navier-stokes/20260912/annular-covariant-flux-moments-attempt01/status.json`
- `source-intake/navier-stokes/20260912/annular-covariant-flux-feedback-attempt01/status.json`
- `source-intake/navier-stokes/20260912/annular-covariant-canonical-ports-attempt02/status.json`

The first canonical-port control run is preserved as failed: its validator
compared the Newton-scaled drive residual (divided by .02) with the physical
1e-10 tolerance. The corrected runner tests physical errors directly at
the SAME 1e-10 tolerance. No physical gate was relaxed. Old scripts and
results were not overwritten; the second run completes both branches and
all three frame choices. No jobs remain at handoff. Work is private and
restricted to post-checkpoint-work, with one single-core BelowNormal worker.
