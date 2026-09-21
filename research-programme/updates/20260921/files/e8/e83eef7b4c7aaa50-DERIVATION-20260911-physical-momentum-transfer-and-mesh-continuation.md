# Physical momentum transfer and canonical mesh continuation

Private working derivation, 11 September 2026. No GitHub action, new physics
claim, interval certificate, or time evolution. This extends, rather than
replaces, the preceding canonical initial-data checkpoint.

**Bottom line:** recovered N32 finite roots, including an MTS root with the
previous fine equations and boundary data unchanged. No N64 root was
recovered. The main obstacle is now obtaining a stable spatial continuation,
not transferring the momentum correctly. A conditional nonlinear mass-
constraint elimination is derived below as the next concrete solver step.

## 1. Problem and unchanged parent equations

Previous result: only the two N16 canonical initializations converged; all
N32/N64 cold starts failed. Here N16 means **16 intervals, 17 scalar nodes**,
not 16 degrees of freedom. Source:
`DERIVATION-20260911-canonical-action-and-boundary-consistent-initial-data.md`.

The current calculation still solves every finite initial equation:

\[
 C_N=0,\qquad \dot C_N=0,\qquad
 (\dot\mu_{\rm in},\dot\chi_{\rm in},\dot\chi_{\rm out})=v_{\partial}.
\]

The initial geometric momentum is P=0, but its derived time derivative is
retained, including the full initial Gram time-link adjoint. The positive
seed lapse, fine-grid scalar configuration, outer clock value and inner mass
are prescribed free/boundary data. Initial extra mass bubbles remain zero.
Neither an arbitrary mode deletion nor a fitted constraint source is added.

Clock **rates**, scalar endpoint **accelerations**, local persistence and
nonlocal Gram energy certification remain separate requirements. A successful
initial root is not yet an evolution solution or a local-GR limit.

## 2. Derived physical momentum transfer

The frozen canonical momentum basis is weighted. Write

\[
 \pi_c(R)=m_c^0(R)u_c(R),\qquad
 m_c^0(R)=\frac{R^2}{N_c^0(R)\sqrt{1-2\mu_c^0(R)/R}},
\]

where u_c is the complete cubic Hermite auxiliary field, including the
released slope coefficients. The superscript 0 denotes the **original frozen
seed geometry**, not the newly solved mass. Interpolating old q-like
coefficients as if they were physical pi would silently change the field.

On the fine grid choose the transferred coefficient vector c by

\[
 \mathop{\rm minimize}_c\int_{R_-}^{R_+}
  |m_f^0(R)V_f(R)c-\pi_c(R)|^2\,dR,
 \qquad (m_f^0V_fc)(R_\pm)=\pi_c(R_\pm).
\]

This is a field projection, **not a fit to an action residual or observations**.
For fixed endpoint coefficients and free columns A_F=m_f^0 V_F, the
quadrature normal equation is

\[
 A_F^T W A_F c_F=A_F^T W(\pi_c-A_Ec_E).
\]

The implementation uses a column-scaled QR least-squares solve, checks full
rank, endpoint values and stationarity, and compares Gauss orders 8 and 12.
Integration is split at **both grids' scalar nodes and mass faces**. This
respects derivative jumps in the seed weight. No global C1 assertion is made
for the physical pi field. Independent spline reconstruction and a same-space
projection identity check test the interpretation of the saved coefficients.

Mass transfer evaluates the coarse P1 face field at fine faces. These face
meshes are not nested, so this is **not** exact mass-field or mass-gradient
preservation. Both errors are measured on common split quadrature. The fine
chi and lapse are the existing fine source data rather than exact coarse
prolongations; their differences are explicitly recorded as well.

Implementation: `scripts/annular_canonical_mesh_transfer_20260911.py`.

## 3. Two distinct boundary controls

The main refinement chain fixes the entire converged N16 boundary-velocity
triple across meshes and verifies it is identical for GR and metric_Gram.
Its inner mass flux is 0.00033578281226508903 in the existing code units.
This is a declared diagnostic port, **not a parent-selected physical flux**.

At each fine grid the main batch compares:

1. Original fine released slope coefficients with a physically transferred
   nodal starting guess.
2. Transferred released slope coefficients and the same nodal starting guess.

These are different free-data slices. Moreover, the fixed coarse flux differs
slightly from the earlier mesh-dependent fine flux. Therefore success in this
batch alone cannot be attributed solely to a better starting guess.

A **strict legacy-port control** separately restores all the previous N32
free data and the original N32 flux, 0.00033659020642862794. Only the starting
guess changes; the larger solver cap is reported and successful iteration
counts must be checked against the old cap before ruling out that effect.
This control is applied to **both** GR and MTS.

Runners: `scripts/derive_annular_canonical_mesh_continuation_20260911.py` and
`scripts/verify_annular_canonical_continuation_20260911.py`.

## 4. A second derived choice of free derivative data

The basis uses coefficients (a,b) with actual auxiliary nodal derivative

\[
 u_R\big|_{\rm nodes}=D a+b/h.
\]

Holding b fixed while solving for a does **not** hold this derivative fixed.
As h shrinks, a change in nodal values can produce large derivative changes.
That observation motivates a separate, explicitly labelled initialization:

\[
 d_* =D a_{\rm transfer}+b_{\rm transfer}/h,\qquad
 b(a)=h(d_*-D a).
\]

The initial guess is identical to the physical projection; during Newton,
the auxiliary Hermite derivative d_* is fixed instead of its correction b.
This changes the specified free initial data, not the parent field equations
or the number of equations. It is not a proof that the physical pi derivative
is fixed: pi_R=(m_f^0)_R u+m_f^0 u_R still changes through u. No slope is
chosen after seeing the desired root or selected to minimize its residual.

Both branches use this same prescription. The complete Jacobian includes
the chain rule b_a=-hD and is checked against an independent directional
finite difference when a root converges. Implementation:
`scripts/derive_annular_canonical_fixed_derivative_20260911.py`.

## 5. Acceptance and interpretation

Root acceptance requires both absolute infinity residual below 1e-9 and
row-scaled residual below 1e-10, all finite saved arrays, positive lapse and
F>0.1. Line-search failure and iteration limits are explicit failed attempts,
not proofs of nonexistence. Failed iterates never seed the next refinement
and never enter time evolution.

Spatial diagnostics are not hidden behind small algebraic residuals:

- Common-grid physical mass, pi, chi, lapse and scalar-velocity differences.
- Sampled pi total variation and field-gradient differences.
- Bulk Hamiltonian density sampled maxima and L2 norms.
- Reintegrated finite constraint using order-12 split quadrature.

The bulk density excludes the Gram point/nonlocal covectors. It is not the
full MTS strong residual, and neither branch's sampled norm is an interval
bound. The reintegrated MTS weak constraint **does** subtract its nodal Gram
term. All quoted raw values are in the inherited code normalization, not
experimental tolerances or SI error bars.

## 6. Evidence and retained failures

### Main continuation results

The corrected main batch finishes with **4/8 finite roots**: both free-slope
prescriptions converge for both branches at N32; neither converges at N64.

| Grid/branch | Original fine corrections: residual max | Transferred corrections: residual max | Result |
|---|---:|---:|---|
| N32 GR | 6.325e-14 | 9.826e-13 | both converge |
| N32 metric_Gram | 2.146e-15 | 2.202e-15 | both converge |
| N64 GR | 3.509e-5 | 1.567e-5 | both fail line search |
| N64 metric_Gram | 1.039e-3 | 8.162e-4 | line-search failure / iteration limit |

There is a substantial distinction between good transfer and good continuum
continuation. For the N16-to-N32 transferred-correction branch:

| Diagnostic | GR | metric_Gram |
|---|---:|---:|
| pi projection L2 error before solving | 2.604e-9 | 6.410e-9 |
| solved pi L2 difference from coarse state | 0.2295 | 0.3587 |
| coarse sampled pi total variation | 2.985 | 4.333 |
| fine sampled pi total variation | 5.559 | 15.316 |
| coarse bulk density L2 | 3.357e-4 | 6.399e-4 |
| fine bulk density L2 | 3.418e-4 | 3.198e-3 |

Thus the transfer preserves the physical momentum very accurately, but the
nonlinear initial solve changes it substantially and adds spatial variation.
The N32 finite equations are solved; **mesh convergence of the physical
initial data is not demonstrated**. Reintegrated N32 weak constraints are
below 1e-12, so merely tightening the bulk-constraint quadrature is not an
explanation for those large field changes. That check does not certify every
time-link or constraint-rate quadrature contribution.

Main evidence:
`source-intake/navier-stokes/20260911/annular-canonical-mesh-continuation-attempt02/status.json`.

### Strict legacy-port outcome

With **all original N32 fine free and boundary data restored**, the MTS
metric_Gram case converges in 9 Newton updates, with absolute residual
3.766e-15 and scaled residual 2.329e-11. That is inside the original
25-iteration budget. The corresponding GR start reaches the 35-update cap
with residual 1.666e-4 and is explicitly not converged.

Thus the earlier MTS cold-start failure did not establish absence of a
finite solution. Better initialization is sufficient for that case. The
paired GR failure also shows why Newton success/failure alone is not a
physical ranking between theories. The main batch's GR success at a slightly
different prescribed flux cannot be relabelled as success of this strict
control, nor does the strict failure prove the old-flux GR problem insoluble.

The control batch passes 27 checks, including independent physical-pi
reconstruction to 4.441e-16, same-space transfer identity to 4.113e-17,
piecewise derivative controls, saved-root replay and reduced-Jacobian
identities. Evidence:
`source-intake/navier-stokes/20260911/annular-canonical-continuation-control-attempt01/status.json`.

### Fixed auxiliary derivative outcome

This alternative free-data slice gives **1/3 roots**: GR N32 converges, GR
N64 fails, and MTS N32 fails. MTS N64 is therefore **not run**, rather than
being seeded with a failed N32 iterate.

The successful GR N32 root has residual 1.646e-15, bulk density L2 2.622e-4
versus coarse 3.357e-4, pi L2 change 0.1178, and pi total variation 3.587
versus coarse 2.985. This improves some GR diagnostics relative to fixed
correction data, but is not a mesh sequence or a general repair. Failed GR
N64 and MTS N32 residuals are 4.188e-5 and 3.648e-4 respectively.

These results do not justify selecting the free-data prescription that
favours one branch and calling that a fair comparison. All variants are
retained. The batch passes 16 checks; the final seal additionally replays
the new parameterization and checks its derivative at **failed as well as
successful** saved iterates. Evidence:
`source-intake/navier-stokes/20260911/annular-canonical-fixed-derivative-attempt01/status.json`.

### Derived next solver step: eliminate the mass constraint nonlinearly

Let m be the free mass-face coefficients, z the free scalar-momentum nodal
values together with boundary reactions, C(m,z) the finite lapse constraints,
and R(m,z) the constraint-rate and boundary-velocity equations. If C_m is
invertible in the relevant positive-chart neighborhood, the exact local
constraint manifold satisfies

\[
 \frac{\partial m}{\partial z}=-C_m^{-1}C_z,\qquad
 \frac{d}{dz}R(m(z),z)=R_z-R_m C_m^{-1}C_z.
\]

These are derivatives with respect to initializer parameters, **not physical
time derivatives**. A subsequent solver can solve C=0 inside every outer
trial step and apply Newton to this reduced R. That retains every equation
and every chosen free datum, unlike adding damping terms to the action or
choosing new physical sources. It can avoid searching far away from the mass
constraint manifold, but does not guarantee a root or mesh convergence.

The control runner computes the mass-block conditioning at each converged
N32 root and verifies the tangent/Schur identity against the complete
Jacobian. These are floating-point local controls, not interval proofs of
invertibility on a neighborhood. The nonlinear reduced solver itself is
**not executed in this checkpoint**.

Numerically, the four main N32 mass blocks have condition numbers near
23.876 and smallest singular values near 0.5753. Their tangent identities
agree to at most 1.111e-16. Reduced, row-scaled Jacobian conditions range
from about 5.47e3 to 1.58e5: mass elimination removes a well-conditioned
subproblem but does not make the remaining compatibility system trivial.

**Next implementation:** nonlinear mass-constraint elimination, first
replaying the saved N32 paired controls, then attempting N64 without
changing the selected free data or flux to force a pass. Retain all spatial
diagnostics and ordinary full residual checks. If that still cannot produce
a stable refinement sequence, use the explicit reduced compatibility
operator to identify the unresolved discretization/branch mechanism; do
not return to an unrelated source hunt or evolve failed data.

### Preservation

An initial runner attempt confused interval labels with node counts and
failed before any solve. Its exact executed source and failure are preserved
under source-intake/navier-stokes/20260911/annular-canonical-mesh-continuation-attempt01.
The corrected attempt uses each archive's actual node count. Earlier
completed documents, scripts, sources and failed physical/numerical attempts
remain unchanged.

All computations use one BelowNormal single-core Python at a time, with
single-thread numerical libraries. The final seal verifies inherited hashes,
new archives, source snapshots and a protected-workbench mtime scan; that
scan is explicitly not a pre-turn content snapshot.

Seal runner: `scripts/seal_annular_canonical_mesh_continuation_20260911.py`.
