# Retained MTS matter and Craig's lattice construction

16 November 2026. Private compatibility result; earlier work and the completed
epochs 2917–2924 remain unchanged.

## Decision

**Conditional fit to the adopted ordinary-matter sector, not an identification
of our cosmological evolution with a lattice gauge calculation.** We can exhibit
a gauge-invariant product-measure interface for the selected neutral
motion/bath subfamily at fixed flat Euclidean geometry, conditional on the
external fermion-measure result. This strengthens a quantum definition route
for the matter block we already retained; it neither replaces that block nor
derives its particle choices from motion.

The numerical longer window is independently complete: 33 reports, all 56
final checks, unchanged bank/grids/tolerances. Its pressure correction uses
16.6765% of the recomputed endpoint envelope. This compatibility review is not
another observational test and changes none of that calculation.

## External result being considered

Craig proposes a gauge-invariant overlap-fermion measure on admissible
four-dimensional Euclidean lattices. Theorem 4.1 treats SU(5) with
10 plus conjugate-5; section 10 restricts it to the four Standard Model
global groups, retaining the original gauge variables. For quotients smaller
than Z6, admissibility uses a faithful representation, not the SU(5) image
alone. Common fermion boundary signs and residual component phases matter.
Section 13 leaves reflection positivity and an interacting continuum
definition open. Section 12 reports formal verification; we have not replayed
it or independently audited the full proof.
[Primary source, v1](https://arxiv.org/html/2610.09093v1).
The [announcement](https://openai.com/index/step-toward-defining-the-standard-model/)
provides context, not an additional theorem.

## Which retained action is being compared

The absolute source paths and pre-review SHA256 hashes are in sources.json.

- **4901:** ordinary quark/lepton representations, one linear Higgs doublet,
  three families and Yukawa operators are explicitly adopted. Hypercharge
  ratios follow conditionally from those choices; the choices are not derived.
  Its local anomaly sums and ordinary Witten parity check are available already.
  Its phrase "all local and global anomaly tests" must not be read as a
  construction of the full lattice determinant line.
- **4904:** owns the assembled SM correspondence action. Its then-current
  zero-residual baseline is historical, not a reason to erase later retained
  motion dynamics.
- **4916:** supplies the common metric and scalar/bath action, with no direct
  ordinary-matter flow argument on the selected parent.
- **Stage49 (6 October):** explicitly specializes the real motion/bath fields
  to a positive quadratic subfamily, preserving ordinary matter and the metric.
  Its complex envelopes are phase-space coordinates, not new electrically
  charged fundamental particles. The earlier charged candidate is separate.
- **MTS-CHARGED-THRESHOLD-AND-GR-TRACE.md:** fixes factorization assumptions at
  prescribed metric, while retaining metric-mediated visible/hidden exchange.

The scalar terms use ordinary derivatives, real bilinear mixing and no SM
gauge action on their fields in this selected branch. We use that declared
branch, not the invalid general inference that every real scalar is neutral.

## Exact representation interface

Our all-left-handed one-generation content, in integer hypercharge y=6Y, is

| Field | Color | Weak representation | y |
|---|---|---|---:|
| Q | 3 | 2 | 1 |
| u-conjugate | conjugate-3 | 1 | -4 |
| d-conjugate | conjugate-3 | 1 | 2 |
| L | 1 | 2 | -3 |
| e-conjugate | 1 | 1 | 6 |
| Higgs (bosonic) | 1 | 2 | 3 |

This is exactly the already adopted content, not an added grand-unified
multiplet or extra gauge boson. Gauge-singlet neutral bath fields add no
fermions. No additional charged or neutrino branch is silently selected.

Here is a direct check of the global-group compatibility rather than assuming
that matching a Lie algebra suffices. For color triality t, weak center parity
p, and integer charge y, the center generator acts by
exp[2 pi i (t/3+p/2+y/6)]. Our six multiplets give exponents
1,-1,0,0,1,1 respectively. Each is an integer, so the representations descend
to every subgroup quotient of this Z6. This does not select a global group;
line operators, topology and component phases can still distinguish choices.

The local checker also rechecks the adopted anomaly/Yukawa arithmetic using
exact fractions, without refitting charges. For the SU(5) representation test,
it builds antisymmetric-pair weights and conjugate fundamental weights:
the cubic sum on diag(1,1,-2,0,0) vanishes, and the embedded two-color SU(2)
has four doublets. These are finite representation checks, not a replacement
proof of global integrability. The Higgs is excluded from fermion anomaly sums.

## Conditional spectator-measure lemma: the actual connection

Assume a finite flat Euclidean lattice, one specified admissible gauge domain,
an external gauge-invariant chiral measure dmu_F[U], and an appropriate
gauge-invariant discretization of the adopted Higgs/Yukawa block. Denote the
neutral real fields together by s. Keep the regulator and matter parameters
independent of s as required by the selected fixed-metric branch. Define

    dmu_total = dU_Haar dmu_F[U] dHiggs ds,
    S_total  = S_visible[U,fermions,Higgs] + S_neutral[s].

For a site gauge transformation, Haar measure is invariant; the assumed
fermion measure is invariant; the unitary Higgs representation preserves its
real-component integration volume; and s is unchanged. Both actions are
invariant. Consequently the complete integrand is gauge invariant. For
convergent finite integrals and nonzero normalizing denominator,

    Z_total = Z_visible Z_neutral,
    <O_visible>_total = <O_visible>_visible.

This is a proof of compatibility on the declared product branch. It does not
derive that product branch uniquely. In geometric language the fermion
determinant line over gauge configurations is pulled back to its product
with neutral scalar configurations: there is no new scalar-direction
fermion-measure curvature. This phase is not our carrier/relative phase.

### Finite neutral integral, not merely a formal spectator

For Stage49's finite quadratic bath, write

    M2 = [[m_b^2, -g^T], [-g, diag(Omega_j^2)]],
    K  = (-Delta_a) tensor I + I tensor M2.

The Euclidean kinetic matrix is nonnegative. If every Omega_j^2>0 and

    m_b^2 - sum_j g_j^2/Omega_j^2 > 0,

the Schur complement makes M2 strictly positive; hence K is positive even
for the lattice constant mode. The finite scalar integral is
(2 pi)^(N/2)/sqrt(det K), up to the fixed field normalization. K is independent
of U, so this factor changes neither gauge anomaly arithmetic nor the
visible measure current. This is the condition behind the positive
quadratic specialization, not a new numerical parameter selection.
A zero eigenvalue needs a separate zero-mode prescription; a negative one
makes the bare real Gaussian integral divergent. An infinite bath additionally
needs convergence/renormalization control. None is silently supplied here.

Once the public metric is integrated, K depends on that metric and its
determinant contributes to the gravitational effective action. Fixed-metric
factorization therefore does NOT remove gravitational interactions or justify
dropping the bath's stress. Match those determinants only once.

## Interface decisions and next useful work

| Question | Decision |
|---|---|
| Adopted chiral multiplets/charges | Match; exact arithmetic check, not an MTS origin derivation |
| Neutral real motion/bath fields | Compatible on selected product branch, by lemma above |
| Global SM quotient | Still unselected; no need to pretend a choice follows from charge matching |
| Higgs/Yukawa regulator | Gauge-invariant lattice realization still to be specified/tested |
| Geometry | Restrict to fixed flat Euclidean specialization for this interface |
| Actual FLRW/cosmological histories | Not that specialization; spatial flatness is not zero spacetime curvature |
| Dynamical metric, boundaries, Lorentzian state | Require their own extension; no automatic Wick rotation of our prepared state |
| Auxiliary operator invertibility | Do not identify with the physical interacting Hamiltonian mass gap |
| Current numerical time evolution | Keep unchanged; no lattice measure has been inserted into it |

The next bounded use, if authorized, is to specify one fixed-background
regulator interface for our exact matter content: choose/document the global
group and fermion boundary signs, enforce faithful plaquette admissibility,
and define the Higgs/Yukawa operators before a small gauge-transformation
test. A toy test would check our implementation, not establish the external
global theorem. No need to restart MTS, replace its motion equations, tune
new charges or launch a full lattice simulation.

For the existing numerical route, preserve all 33 reports and the saved
restart-mismatch transport; the preselected horizon ends at 2924. Choose
the next scientific question before adding arbitrary eight-epoch blocks.

## Verification and scope

Run check_interface.py with the retained Python and -B. It uses only the
standard library; reads the frozen source documents/receipts; checks exact
representation identities and the completed batch status; and writes
checks.json. It does not execute historical scripts, launch a fit, inspect
other agents or alter the sealed numerical stage.

These checks verify our mapping and saved status, not Craig's proof,
reflection positivity, interacting continuum existence, a physical mass gap,
or the numerical value of a new coupling. The external result is explicitly
conditional throughout. All work is local; the persistent goal stays paused.
