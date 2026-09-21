# Joint covariant initial data and the boundary energy law

Private numerical/derivation checkpoint, 2026-09-12. No publication or
evolution. This continues the NEW finite scalar action from
`DERIVATION-20260912-covariant-full-scalar-action-and-initial-constraint.md`.
The old working branch, `annular-acceleration-trace-completion-attempt02`,
remains unchanged. Certificates from that different finite action do not
transfer here. All numbers below are in the existing annular fixture's
normalization, not SI experimental bounds.

## 1. What was actually solved

The previous checkpoint prepared 19 gravity constraints alone. This one
jointly solves those 19 rows, the inner physical mass-flux condition, and
the outer scalar-velocity condition. At each trial, the outer clock is
normalized exactly and two cubic lapse amplitudes solve the two projected
metric-momentum endpoint conditions. Thus all 23 conditions are addressed,
not a C0 root combined with an unrelated old time jet.

The fixture is unchanged: N16, R in [5.875,6.125], kappa=.1, the existing
common scalar/free profile and K_seed, inner mass, outer clock and signed
velocity drives. GR means the matched GR-plus-scalar comparator, not vacuum
GR. MTS adds the same Gram factors without a coupling/amplitude refit.

There are 19 dependent mass directions X_j=int_Rin^R eta_j dr and the
same two previously sourced auxiliary boundary lifts. With z the normalized
radial coordinate, their nodal shapes are K_seed*(1-3z^2+2z^3) and
K_seed*(3z^2-2z^3). They modify the auxiliary momentum across the annulus:
these are NOT endpoint-only changes and NOT unchanged total momentum.
The free profile modulo those two declared directions is retained. The
maximum new p change is .202006 GR/.204105 MTS. This nontrivial dependent
change must not be described as a tiny correction of the old full data.

We keep the old 79-dimensional mass phase frozen for this test. All new
scalar nodes are independent. No old scalar evolution equation is used.

## 2. Triangular first jet from the new action

At P=0, let U=sqrt(F), F=1-2mu/R, a=c_P=kappa*U/N,

    C_i=R_i^2 N_i U_i,
    d_i=sum_f S_fi A_f^2/(2h),
    e_i=omega_i p_i^2/(2R_i^2)+R_i^2 d_i,
    s_i=N_i e_i/(R_i U_i).

The complete gravity-only plus nodal scalar force is

    f_bulk=-N_R/(kappa U)+N mu/(kappa R^2 U^3),
    M^T P1_coeff=Q_mass^T W f_bulk+Q_nodes^T s
                    +Q_out*(N_out/U_out-C_out)/kappa.

Here M=P_mass^T W Q_mass. The inner metric reaction equals
N_in/(kappa U_in), cancelling the existing inner gravity radial-action
term, not the scalar nodal source. The outer clock makes the displayed
outer load zero. Endpoint nodal scalar energy is retained in s, including
both endpoints; no use is made of the old interior-Gram-only cancellation.
This selects the previous classical P=0/clock boundary branch, not every
possible matter/boundary history.

P1 determines g_R=a P1 and J_fi=exp(g(R_i)-g(anchor_f)). Then

    q_i=chi_i,t=C_i p_i/R_i^4,
    D_f=sum_i S_fi J_fi C_i,
    A1_f=sum_i B_fi J_fi q_i,
    Gchi_i=-sum_f B_fi A_f D_f/(h J_fi),
    d1_i=sum_f S_fi A_f A1_f/(h J_fi),
    omega_i p1_i=Gchi_i+rho_i,
    f_raw=mu1_raw=-a K,
    M mu1_coeff=P_mass^T W f_raw.

All factor sums include the transported BASE scalar action and, for MTS,
the unchanged Gram correction. K is reconstructed from oriented currents.
The anchor sums cancel, so K=e^(-2g)*k_cell on each parent radial cell.
Both parent-cell sides of each anchor are checked; K's physical endpoints
are one-sided, and right traces at interior nodes are used consistently
when diagnosing the raw discontinuous current profile.

## 3. Joint solve results: starting compatibility, not propagation

Newton uses three updates, with a 21-variable Jacobian condition about
258.3. The two eliminated lapse equations have condition about 1.01.

| Quantity | GR | MTS |
|---|---:|---:|
| 19 C0 rows, primary maximum | 1.18e-13 | 1.17e-13 |
| 19 C0 rows, higher quadrature | 1.57e-13 | 1.63e-13 |
| Raw inner mass-drive error | <1e-18 | <1e-18 |
| Outer scalar-drive error | <6e-18 | <6e-18 |
| Outer clock error | 0 | 0 |
| Projected P1 endpoint error, primary | 2.26e-17 | 2.95e-17 |
| Projected P1 endpoint error, higher | 5.34e-10 | 9.29e-11 |
| Projected inner mass-drive error, primary | 3.37e-9 | 2.24e-9 |
| Both-endpoint mass projection error, primary | 3.56e-9 | 4.37e-9 |

Minimum sampled F remains .659572 and minimum N exceeds .812070. Time
Jacobian ranges are [.99996375,1.00003396] GR and [.99985829,1.00006885]
MTS. These are numerical chart checks, not interval certificates.

The projected mass flux does NOT equal the raw action current at the
required 1e-10 tolerance. GR also misses the higher-quadrature P1 endpoint
gate. No full first-jet pass is claimed.

## 4. Boundary energy balance derived, not row-fitted

The exact full scalar boundary current is

    K_b=n_b*(C_b d1_b+Gchi_b q_b), n_in=-1, n_out=+1.

It includes C*d1 at the endpoints, because the base coefficient samples
them. The old Gram-only endpoint identity cannot be substituted.

For this P=0/clock branch, cancellation of the explicit radial and scalar
source power requires

    rho_b q_b=-n_b K_b,
    rho_b=-n_b K_b/q_b=-Gchi_b-C_b d1_b/q_b.          (1)

The fixture has nonzero endpoint q, so division is legitimate. At q_b=0
the undivided equation must be used: it requires K_b=0 and does not in
general determine rho_b. Equation (1) is an instantaneous energy-compatible
port condition, NOT a proof of a parent-signed source history, nor proof
that the prescribed velocity histories satisfy the next derivative.

Derived rho values are (.56760920,.44447849) GR and
(.56337090,.44171091) MTS. Both signs/orientations and canonical scalar
equations are checked independently at both quadratures.

An initial diagnostic instead solved two C1 endpoint rows for rho, giving
slightly different values (differences up to 5.61e-6). That absorbs part of
the projection error into boundary forces. It is recorded but NOT adopted.
Equation (1), not the row-fitted forces, owns the final candidate's p1.
Copying the old sampled force values gives C1 about .0192 in both branches;
those samples are not the boundary law for this new finite action.

## 5. Exact decomposition of the remaining error

Let f=mu1_raw, v=Q_mass*mu1_coeff, and L_mu denote the new C0 derivative
with respect to mass, including every nodal and radial-boundary term.
With all 19 eta tests, the first-constraint identity is

    C1[eta] = L_mu[eta](v-f)
       + integral (eta*f/N)*(f_bulk-P1) dR
       + sum_i (eta_i*f_i/N_i)*s_i
       - sum_b eta_b*n_b*K_b/N_b
       - sum_i eta_i*rho_i*q_i/N_i.                 (2)

The continuous integrals in (2) arise from cellwise integration by parts,
including all interior jumps. Their finite quadratures leave a measured
reconstruction error, not an asserted exact floating-point zero. The
metric boundary reaction and outer load used in section 2 are part of
this identity's assumptions; other boundary actions require their terms.

The first diagnostic omitted the fourth term (radial endpoint power) and
therefore showed a spurious .0715/.0713 Ward discrepancy. The preserved
control run corrects it explicitly; there is no silent rewriting of that
executed diagnostic. The full corrected reconstruction error is at most
2.25e-14 across both branches and quadratures.

Under (1), the last two terms cancel. What remains is measured mass-flux
projection error plus metric Euler work on tests not exactly represented
by the frozen phase. This is not unexplained scalar off-space work.

| Final C1 with DERIVED port power | GR | MTS |
|---|---:|---:|
| All 19 rows, primary | 5.49677e-7 | 4.75919e-7 |
| All 19 rows, higher quadrature | 5.49548e-7 | 4.75544e-7 |
| 15 interior P1 lapse rows | 2.92704e-8 | 2.91780e-8 |
| Metric Euler-work maximum, primary | 1.58622e-7 | 1.54087e-7 |
| Mass-projection-work maximum, primary | 7.08298e-7 | 6.30006e-7 |

Component maxima are not additive: the vectors partially cancel. The
1e-10 gate remains unchanged and both branches fail it. The shared scale
and explicit decomposition implicate this finite metric approximation;
they do not prove convergence, physical equivalence, or rule out a future
model-specific obstruction. Do not compare these C1 numbers with the old
action's C2 numbers as if they measured the same residual.

## 6. Independent controls

- Ten gravity-plus-full-scalar metric action variations per branch and
  quadrature match the new force, worst error 9.61e-14. Scalar energy is
  included once; there is no old local scalar force added to transport.
- All 79 weak connection loads agree between direct parent-cell integrals
  and independently integrated oriented anchor-to-node links.
- A complex-step, first-order-consistent history constraint curve checks
  the differentiated constraint independently, worst error 1.81e-16. It
  uses exact linear-c transport at the germ and retains the inverse J in
  each nodal amplitude. This is a first-derivative check, not an exact
  nonlinear trajectory or new causal history contract.
- Omitting scalar time transport changes the residual by about 9.2e-6 to
  9.5e-6; omitting the connection load changes it by about 2.35e-6. The
  checks are sensitive to those missing terms.
- Both quadratures recompute the metric momentum and transport from the
  SAME prepared initial fields, not from the previous action's jets.

## 7. Next constructive target

Build an action-compatible metric approximation that controls BOTH terms
in (2): the full parent-current family under the C0 mass differential and
the metric Euler work on eta*f/N. Include the physical endpoint traces.
First determine whether the existing continuous-mass/broken-momentum
spaces admit those identities, before another enrichment loop; K has
interior jumps, so inserting it as a continuous mass basis is not valid.

Any proposed completion must retain the entire declared source family,
reprepare the joint initial state and recompute P1/J/p1/mu1, then pass the
same independent GR/MTS checks. Do not fix the problem by altering rho to
fit C1, by imposing constraint projection as an extra equation without an
action, or by relaxing the tolerance. C2 and evolution wait. Full source
histories and a causal history/IVP contract remain separate tasks.

## 8. Reproducible evidence

- `scripts/annular_covariant_joint_preparation_20260912.py`
- `scripts/derive_annular_covariant_joint_preparation_20260912.py`
- `scripts/verify_annular_covariant_joint_preparation_20260912.py`
- `source-intake/navier-stokes/20260912/annular-covariant-joint-preparation-attempt01/status.json`
- `source-intake/navier-stokes/20260912/annular-covariant-joint-control-attempt01/status.json`

The first run contains initial data, metric first jets and ROW-FITTED port
diagnostics. The second run owns the FINAL DERIVED energy-balanced rho/p1,
C1 and corrected Ward arrays. Neither is adopted as a full passing branch.
No old evidence, protected workbench, galaxy work or GitHub files were
changed. One BelowNormal single-core worker ran at a time; both jobs ended.
