# Completed conjugate terms and classical matter-current identity

16 November 2026. Authoritative result: dirac-adjoint/result.json.
Authoritative derivation: dirac-adjoint/DERIVATION.md.
Read ADJOINT-COMPLETION.md for the preserved first convention and its
explicit Dirac-adjoint completion. No previous theory or cosmological file
was altered.

## Derived result

For the completed ordered Yukawa pairs, overlap kinetic terms and Higgs block,
the link response and field-equation contact satisfy

    D^- J_act + E_gauge = 0

at every lattice site and gauge generator. The current is built by
differentiating the Wilson/overlap/projector action; the field contact is
computed separately from the same action's field derivatives. It is not
defined by forcing the sum to vanish. When the charged-field equations hold,
E_gauge vanishes and covariant conservation D^-J_act=0 follows.

The saved arbitrary probes are off shell. Their maximum divergence/contact
magnitudes are about77.40,72.03,89.56; the two terms cancel. Demanding either
term vanish separately on those probes would be the wrong test.

Adding the fixed-background neutral bath changes the action but adds zero
gauge current and zero gauge contact. Thus it obeys the same identity, not
a second independently fitted conservation law. Both action totals are
independently included in the link-perturbation checks.

## Verification

| Check | Final result |
|---|---:|
| Saved fixtures reused | 3 |
| Site/generator identities per fixture | 16 x12=192 |
| Worst local balance error, before/after gauge transformation | 2.63484e-14 |
| Unchanged normalized identity gate | 1e-10 |
| Independent finite-difference checks: three links, two fixed steps, both actions | pass |
| Largest finite-difference discrepancy across reported comparisons | 1.60176e-11 |
| Aggregate panel checks | 114 pass |
| Retained files checked unchanged | 49 |
| Closeout checks | 12 pass |
| Cached replay: reports and saved current arrays | identical |

The three links probe color, weak and hypercharge directions on the first
fixture. Finite differences use eighth-order symmetric stencils at0.005 and
0.0025. Both steps pass the original gate; no monotonic-convergence claim is
made from roundoff-sized differences. The same operator bank, grid, input
coefficients and boundary signs were reused.

There are576 local entries before and576 after the gauge transformations.
Matter and matter-plus-bath share the same classical gauge identity because
the added fields are neutral; do not double-count these as independent
physical tests. These are synthetic regulator checks, not galaxy/cosmological
fits or new physical measurements.

## Essential terms and controls

Omitting the projector's gauge-field derivative produces clear Ward failure,
roughly0.031–0.087 normalized residual, against the unchanged1e-10 gate.
Giving barred rows the wrong sign under a gauge transformation also fails.
The current therefore needs the full chain through sign(H_W) and P_hat,
rather than only the explicit nearest-neighbor Wilson links.

The new independent barred Yukawa tensors preserve the retained holomorphic
terms. The coefficient-conjugacy check is separate: gauge invariance alone
does not enforce the conjugate coupling or spinor convention. A deliberately
unconjugated Yukawa coefficient is detected.

A trivial zero-charged-field configuration has zero current even with the
saved nonzero neutral bath. This is labelled a trivial control, not a
nontrivial on-shell matter solution.

## The spinor convention mattered

The first root run and replay passed a bare Euclidean coefficient-pairing
test using B^dagger. That did not yet check the Dirac-adjoint continuation.

Using bar_psi=psi^dagger Gamma4 for the coefficient audit requires

    Bsharp = Gamma4_R B^dagger Gamma4_L^T,

with reversed Grassmann field order. In the retained gamma convention this
equals -B^dagger for our Yukawa spin tensors. The completed code carries that
factor into the barred interactions and their field/Higgs derivatives.
Independent barred integration rows are still independent; they are not set
equal to conjugates of the overlap-projected columns.

The final test explicitly detects the wrong bare-spin conjugation. All
classical link-current arrays remain byte-identical to the first run because
the barred projector is fixed and those barred Yukawa terms have no link
derivative at fixed Higgs/rows. Their contact contributions cancel with the
associated Higgs variation.

The root artifacts are retained and hash-pinned. This was a completion of
the new prototype's conjugation convention, not a change to an old physical
MTS coupling. It does not establish reflection positivity, a global Wick
rotation, or equality of Euclidean barred states to physical adjoint states.

## Quantum measure and the next connection

J_act is the classical action current, not the chiral fermion-measure current.
The quantum variation also contains delta log(dmu), which has not been
constructed or set to zero by this calculation. That question remains
separate, as requested.

The useful next step is to connect this checked matter current to the
retained common-metric stress/exchange equations, reusing the existing
Hilbert-source and action-pullback derivations. First identify the exact
source interface already owned by those documents; do not present a repeated
textbook identity as a new derivation, enlarge the lattice by default, or
restart the framework. The physical33-report evolution through2924 and its
bank/grids/tolerances are unchanged.

All four numerical run/replay workers exited. One worker/thread at a time,
CPU4 below-normal. No continuing calculation, GitHub action, relay,
subagent or change to another chat's processes. Persistent goal stays paused.
