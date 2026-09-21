# Nonlinear mass elimination and boundary-flux compatibility

Private checkpoint, 11 September 2026. No publication, new evolution,
interval evolution certificate, or local-GR/experimental pass.

**Main result:** mass-constraint elimination works and replays the saved
roots, but does not recover an N64 root. More importantly, the prescribed
synthetic inner flux is incompatible with the classical GR-plus-canonical-
scalar boundary trace law for the currently fixed initial traces. The full
Gram correction is derived separately; a GR-only flux law cannot simply be
imposed on MTS. This is a concrete boundary-data problem in this diagnostic,
not a rejection of either fundamental theory.

## 1. Implemented reduction, without altering equations

The original finite initializer has free mass-face values m, scalar-momentum
nodal coefficients a and three boundary reactions lambda. Let z=(a,lambda).
It solves the lapse constraints C(m,z)=0 and the constraint-rate plus
boundary-velocity equations R(m,z)=0. Released momentum corrections, scalar
configuration, seed lapse, clock, inner mass and specified boundary velocities
are held at their archived values.

For nonsingular C_m, the local mass-constraint manifold obeys

\[
 m_z=-C_m^{-1}C_z,\qquad
 D\widehat R=R_z-R_m C_m^{-1}C_z,
 \quad \widehat R(z)=R(m(z),z).
\]

This is differentiation with respect to initializer parameters, not time.
The new solver actually solves C=0 inside **every outer trial step**, using
a positive-metric Newton solve. It then differentiates the original full
residual along the tangent (-C_m^{-1}C_z,I), retaining every equation. No
source is fitted, no mode is deleted, and no regularization enters the action.

For the frozen canonical pi reconstruction, write

\[
 H=\frac{\pi^2}{2R^2}+\frac{R^2\chi_R^2}{2},\qquad
 F=1-\frac{2\mu}{R}.
\]

The analytic mass variation of the bulk constraint density is

\[
 \delta C_{\rm bulk}=
 \frac{\delta\mu_R}{\kappa\sqrt F}
 +\left(\frac{\mu_R}{\kappa R F^{3/2}}
        +\frac{H}{R\sqrt F}\right)\delta\mu
 -\frac{\sqrt F\,\pi}{R^2}\delta\pi.
\]

The Gram nodal contribution adds
R_i d_i delta_mu_i/sqrt(F_i) to the mass variation. The pi basis remains
weighted by the **original frozen seed geometry** throughout; recomputing
that basis during the solve would change the canonical problem.

Implementation: `scripts/annular_canonical_mass_reduction_20260911.py` and
`scripts/derive_annular_canonical_mass_reduction_20260911.py`.

## 2. Controls and numerical outcomes

All **five** saved N32 roots are recovered after small perturbations, within
3.42e-9 in the saved coefficient infinity norm. Analytic mass blocks agree
with independent full complex derivatives to 3.56e-15; the complete chain
rule agrees to 4.81e-14. Additional nonlinear-manifold directional controls
cover failed as well as successful final iterates; their largest normalized
error is 2.31e-9. A negative control detects omitting the mass response.

Acceptance remains both full absolute residual <1e-9 and inherited
row-scaled residual <1e-10, not merely a small reduced residual. The inner
mass tolerance is 2e-14; the outer update cap is 35. All trials preserve the
chosen free corrections and boundary data. Saved **original seed_state**
arrays, not previous failed final iterates, start the new attempts.

| Case | Full residual max | Mass-constraint max | Outcome |
|---|---:|---:|---|
| N32 GR, strict legacy port | 1.994e-5 | 2.023e-15 | update limit |
| N32 Gram, strict legacy port | 2.758e-14 | 1.903e-15 | converged |
| N64 GR, original corrections | 3.197e-7 | 2.756e-15 | line search fails |
| N64 GR, transferred corrections | 1.286e-7 | 2.566e-15 | line search fails |
| N64 Gram, original corrections | 8.014e-6 | 2.261e-15 | update limit |
| N64 Gram, transferred corrections | 2.442e-5 | 2.031e-15 | line search fails |

Thus the mass block is no longer the unsolved constraint. The remaining
constraint-rate/boundary system still fails at N64. Some total residuals
improve because the formerly large mass residual has been removed; that
alone is not evidence that the physical solution is closer.

The converged N32 Gram run has sampled bulk-density L2 4.455e-4 versus
6.399e-4 on its coarse input, and pi total variation 5.028 versus 4.333.
Its pi L2 difference from that coarse state is still 0.2058. These are
code-normalized finite diagnostics, not a convergent mesh sequence. The
bulk density excludes Gram point/nonlocal covectors. Failed N64 states are
not evolved or promoted to physical initial data.

Main batch: 88 checks, five replays, six fresh attempts.
`source-intake/navier-stokes/20260911/annular-canonical-mass-reduction-attempt01/status.json`.
Independent controls: 42 checks.
`source-intake/navier-stokes/20260911/annular-canonical-mass-reduction-control-attempt01/status.json`.

## 3. Derived GR boundary compatibility lemma

Here the label GR means the **GR plus canonical scalar control**, not empty
vacuum GR. This statement concerns the sourced kappa=1/10, Lambda=m_chi=b2=b3=0,
initial P=0 branch in the existing annular coordinates.

The canonical bulk action contains

\[
 L=P\dot\mu+\pi q+\frac{N\mu_R}{\kappa\sqrt F}
   -N\sqrt F\left(\frac{\pi^2}{2R^2}
                      +\frac{R^2w^2}{2}\right)
   -\kappa N F^{3/2}P\pi w-\mathcal Q P^2,
 \quad q=\chi_t,\ w=\chi_R.
\]

At P=0 its independent P and pi equations give

\[
 \dot\mu=\kappa N F^{3/2}\pi w,\qquad
 q=\frac{N\sqrt F}{R^2}\pi.
\]

Consequently, for a classical one-sided boundary trace with no additional
P-linear boundary source,

\[
 \boxed{\dot\mu_b=\kappa R_b^2 F_b q_b w_b.}
\]

The retained quadratic P-boundary flux also has zero first P variation at
P=0, so it does not supply a missing linear term here. The implication is
conditional on the stated smooth trace/branch assumptions; it is not a
statement about all weak solutions, nonzero-P initial data or other actions.

**Compatibility lemma:** if mu_b, q_b, w_b and the mass rate v_b are all
specified at that slice, a classical extension satisfying this parent
equation requires v_b-kappa R_b^2 F_b q_b w_b=0. A nonzero difference rules
out that particular collection of boundary traces under these assumptions.
It does not rule out GR, or a different compatible boundary preparation.

The elimination is checked symbolically from the canonical density. The
stored boundary numbers and Hermite coefficients are also evaluated as exact
rationals of their binary values, so the following nonzero discrepancies
are not just subtractive floating-point noise:

| Prescribed synthetic port | Parent bulk flux from fixed traces | Prescribed minus parent | Relative mismatch |
|---|---:|---:|---:|
| N32 legacy: 0.000336590206429 | 0.000336490800877 | +9.94056e-8 | +0.02954% |
| Fixed N16 port at N64: 0.000335782812265 | 0.000336490800877 | -7.07989e-7 | -0.21040% |

These exact-rational checks concern the specified digital data, not an
experimental uncertainty enclosure. They do not by themselves prove that
the discrepancies explain every Newton stall. They do identify an actual
obstruction to retaining those traces in a smooth GR-control limit. In
particular, carrying the fixed coarse projected flux into a refinement
study was **not** guaranteed to preserve a compatible continuum boundary
problem merely because the same number was used for both branches.

## 4. Full Gram endpoint correction, not a GR substitution

Retain the existing full time-link action. For each factor/link (f,i), write

\[
 A_f=\sum_i B_{fi}\chi_i,\quad
 C_i=R_i^2N_i\sqrt{F_i},\quad
 D_f=\sum_i S_{fi}J_{fi}C_i,\quad
 \dot A_f=\sum_i B_{fi}q_iJ_{fi},
\]
\[
 I_{fi}=\frac{A_f}{h}
     (S_{fi}C_i\dot A_f-B_{fi}q_iD_f).
\]

The initial full momentum force functional has the oriented kernel

\[
 G_P[\delta P]=\sum_{fi} I_{fi}J_{fi}
 \int_{a_f}^{R_i}
    \frac{\kappa\sqrt F}{N J_f(R)^2}\,\delta P(R)\,dR.
\]

All current factor anchors lie strictly inside the annulus. Immediately
inside its inner edge, only links ending at node 0 contribute, with negative
orientation. Since J_f(R) tends to J_f0 at that endpoint,

\[
 G_{P,-}=-\frac{\kappa\sqrt{F_-}}{N_-}
           \sum_{f:i=0}\frac{I_{f0}}{J_{f0}}.
\]

The present sampling has S_f0=0, and the scalar source is
G_chi,0=-sum_f B_f0 A_f D_f/(h J_f0), hence

\[
 \boxed{G_{P,-}=-\frac{\kappa\sqrt{F_-}}{N_-}q_-G_{\chi,0}},
 \qquad
 \boxed{\dot\mu_-=
       \kappa R_-^2F_-q_-w_- -G_{P,-}.}
\]

This is a one-sided parent-kernel trace, not a new fitted flux term. The
endpoint Jacobians and path orientation have not been discarded. The
kernel-current/scalar-force identity is checked on every new Gram saved
iterate, including failed ones.

For the converged N32 Gram finite initializer, G_P,- is approximately
6.32943e-7 in code units. Its finite mass-rate trace differs from the local
canonical EP trace by about 7.32345e-7. Therefore a solved finite boundary
row is **not** a certificate that this classical parent trace condition is
resolved. Nonlocal force values here use the stored finite initial jet and
its quadratures; they are not certified continuum-limit bounds.

We also tested a tempting stronger sign argument. At N16, N32 and N64 the
three contributing endpoint products -B_f0 A_f have **two positive signs and
one negative sign**. Positive Gram quadratic energy therefore does not
establish an unconditional sign for this endpoint force. No such sign or
universal flux inequality is claimed.

Boundary checks and exact stored-factor signs:
`scripts/derive_annular_canonical_boundary_compatibility_20260911.py` and
`source-intake/navier-stokes/20260911/annular-canonical-boundary-compatibility-attempt01/status.json`
(11 checks). Underlying full-source implementation:
`scripts/annular_canonical_boundary_20260911.py`.

## 5. What the nearly singular reduced matrices do and do not show

Saved reduced Jacobians include their smallest left/right singular vectors.
Two-step finite-difference curvature tests give negative discriminants for
the local projected quadratic residual at all five failed final states.
This is consistent with local turning behaviour of these solver branches,
but **is not a fold theorem or a proof of no roots elsewhere**. Some step-
size comparisons are not asymptotically tight. No higher-order remainder or
neighborhood bound has been established.

Condition numbers change substantially under seed-based column scaling.
They are coordinate-dependent numerical diagnostics, not physical stability
measures. No singular vector is removed from the equations. The analytic
second-variation identity, if needed for a certified local study, is

\[
 m''=-C_m^{-1}D^2C[t,t],\qquad
 \widehat R''=D^2R[t,t]-R_m C_m^{-1}D^2C[t,t],
 \quad t=(m_zv,v),
\]

where z varies affinely in direction v. This identity is conditional on
the same local mass invertibility; the numerical curvature samples are not
an exact Hessian enclosure.

## 6. Next constructive target

**Boundary-consistent initial preparation, before more refinement of the old
fixed-port problem.** Derive which inner boundary data are supplied by the
boundary action/clock and scalar drive, and which flux is predicted. Keep
the derived GR law and full Gram endpoint correction visible in the same
contract. Do not independently lock mu_t, q and chi_R to mutually incompatible
numbers or insert a new source to conceal the mismatch.

There are physically different choices to distinguish: retaining a specified
mass history requires deriving a compatible scalar boundary trace; retaining
the scalar preparation requires deriving the mass flux. The choice must be
stated and tied to the parent boundary problem, not selected separately for
GR/MTS according to which fit succeeds. Simply replacing both fluxes by
the GR bulk expression would incorrectly omit the MTS correction.

Then implement the corresponding initial-data solve using the mass-reduced
solver already built, rerun paired GR/Gram controls and demand shrinking
spatial/trace defects. This checkpoint has **not yet implemented that boundary
replacement**. The old tests remain intact. Clock-rate, endpoint-acceleration,
general-time canonical equations and local persistence follow only after
compatible initial preparation and spatial control.

All work remains in post-checkpoint-work. Prior sources, frozen workbench
and galaxy work are unchanged. No GitHub action or new agents. One
BelowNormal single-core Python at a time; no work is left running after the
final seal. The protected-file check is an mtime scan from this turn's
start, not a pre-turn content snapshot.
