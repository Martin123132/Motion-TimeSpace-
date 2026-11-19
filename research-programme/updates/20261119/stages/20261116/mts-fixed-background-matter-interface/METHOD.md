# Fixed-background matter interface: frozen test contract

16 November 2026. Manual continuation; previous MTS histories and source bank
are read-only. No automatic restart, later epochs, fits, publication or relay.

## What is derived and what is selected

The previous compatibility lemma motivates a small gauge-interface test.
This stage selects q=1 (the unquotiented SM product group) for a numerical
fixture only. It does not choose the physical global group. Lattice spacing
is one in dimensionless test units, with a 2x2x2x2 periodic gauge lattice and
a common antiperiodic temporal sign for all fermions. This is neither an
expanding spacetime nor a claim that spacetime is physically a lattice.

The retained representation table is reused unchanged:
Q=(3,2)_1, uc=(bar3,1)_-4, dc=(bar3,1)_2, L=(1,2)_-3, ec=(1,1)_6,
and the Higgs=(1,2)_3, using integer hypercharge y=6Y.
One generation suffices for this interface check because the gauge map acts
identically on generations; flavor dynamics is not being simulated.

For the source convention T_mu psi(x)=R(U_mu(x))psi(x+mu), our Wilson matrix is

    D_W = sum_mu [gamma_mu (T_mu-T_mu^dagger)/2
                    + I -(T_mu+T_mu^dagger)/2],
    H_W = gamma5 (D_W-I),
    D = I + gamma5 sign(H_W),
    P_hat_minus = (I + sign(H_W))/2,  P_plus=(I+gamma5)/2.

We follow the overlap conventions in [Craig, sections 1–3](https://arxiv.org/html/2610.09093v1).
These operators do not by themselves supply the gauge-dependent integration
measure phase discussed in that paper.

## Covariance and Yukawa derivation

Let G_R be the site-diagonal unitary representation of a gauge change.
The link transformation makes T' = G_R T G_R^dagger. Gamma matrices commute
with G_R, so D_W, H_W, their spectral sign and P_hat transform by conjugation.
Thus P_hat'[G_R eta]=G_R[P_hat eta]. Using arbitrary independent test columns
and rows probes this identity and the kinetic bilinear bar(psi)D psi.
A numerical matrix test is not a proof of uniform locality.

For all-left fields, the three holomorphic Yukawa tensors are

    Y_up   = sum_x Q_(a,c,i) C_ab uc_(b,c) epsilon_ij H_j,
    Y_down = sum_x Q_(a,c,i) C_ab dc_(b,c) H_i^*,
    Y_e    = sum_x L_(a,i) C_ab ec_b H_i^*.

C acts on spin only and satisfies C gamma_mu C^-1 = -gamma_mu^T.
Color contractions cancel fundamental against conjugate, while
g2^T epsilon g2=epsilon and g2^T g2^*=I preserve the weak contractions.
Hypercharge sums are 1-4+3, 1+2-3, and -3+6-3: all zero.
These identities remain valid for overlap-projected columns because their
projectors transform covariantly. We test the complex coefficient tensors
using commuting random probes, not a sampled Grassmann path integral.
A complete Euclidean action also needs the independent barred-field
conjugate terms and its reality/reflection properties. This test does not
claim to implement that entire action or its measure.

The Higgs forward-difference kinetic norm and its invariant quadratic/quartic
potential are included. Numeric coefficients and amplitudes in protocol.json
are synthetic controls, not changes to observed masses, charges or cosmology.

## Baseline and MTS labels

Here baseline means the ordinary-matter interface on a fixed flat geometry;
MTS adds a gauge-neutral real field and two real bath components with the
positive mass matrix from the previous conditional lemma. These are two
synthetic interface configurations, NOT the saved cosmological baseline/MTS
histories. Gauge transformations leave each neutral history unchanged. We
compare each total action under the same gauge transformation and check the
bath contribution separately. Metric-mediated interaction is not removed
from the retained theory; the metric is simply not varied in this test.

## Frozen checks and failure controls

All tolerances, seeds and fixtures are fixed in protocol.json before execution.
The normalized algebra/covariance gate is 1e-10; the negative-control separation
is 1e-6. The existing cosmological tolerances are unchanged and not used here.

- Three independent deterministic nonzero link fixtures, with strong local
  noncommuting gauge transformations and both interface configurations.
- Clifford, charge-conjugation, free Fourier spectrum, Wilson hermiticity,
  Ginsparg–Wilson, projector and chiral-intertwining identities.
- Gauge covariance for all five fermion multiplets; kinetic and three
  projected Yukawa tensors; Higgs/gauge actions; neutral addition.
- Faithful plaquette diagnostic iota=diag(z^-2 g3,z^3 g2,z), and direct
  measurement of the Wilson-kernel gap for every fixture/operator.
- A center-valued single-link defect must evade the SU(5)-image diagnostic
  but be rejected by the faithful q=1 diagnostic.
- Incorrect uc hypercharge, conjugation, and holding an old chiral projector
  fixed during a gauge transformation must produce detectable failures.
- A controlled basis-phase rotation must change the reduced chiral
  determinant phase without changing its magnitude. No compensating current
  is implemented or claimed.
- A deliberately unstable bath must fail the positive-Gaussian test.

The plaquette cutoff 0.1 and gap floor 0.5 are frozen engineering guards.
They are NOT a numeric value for the paper's unspecified theorem threshold
or a certified all-configuration locality domain. Passing finite kernel gaps
is only a check of these particular fixtures. No physical mass gap is inferred.

## Execution and preservation

Use the retained Python 3.13 with -B. One worker, one numerical thread,
below-normal priority, a ten-minute wall guard. No subprocess pool or service.
Save each fixture and its report before the next. A cached replay may read
those fixtures, but must not rewrite earlier outputs or hide failed checks.

The input manifest pins the previous compatibility evidence and numerical
closeout. Check their inherited source hashes before and after, compile
without generating pycache, retain any failure receipts, and verify the exact
worker exit before final reporting. Keep the goal paused and wait for the
next manual instruction after the result.
