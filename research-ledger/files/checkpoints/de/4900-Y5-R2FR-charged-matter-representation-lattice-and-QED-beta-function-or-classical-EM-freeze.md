# 4900 - Charged-matter representations, QED beta function and correspondence gate

Marker: `MTS_CHARGED_MATTER_AND_QED_CORRESPONDENCE_GATE_4900`

## Decision

The present scalar-soliton particle corpus does not derive charged fermions,
their electric representations, or QED. That statement is now based on a full
field-content scan and an executable reproduction of the strongest lepton-mass
calculation, not on the absence of familiar vocabulary alone.

The framework need not remain classical. The integrated-`H` parent already
admits explicit matter fields `Psi`, and checkpoint 4854 already adopts an
independent principal `U(1)` connection. This checkpoint therefore adds an
honest **standard Dirac-QED correspondence module** on the same public metric:

\[
S_{\rm QED}=\int d^4x\sqrt{-g}\left[
-\frac14F_{c\,\mu\nu}F_c^{\mu\nu}
+\sum_a\bar\chi_a
\left(i\gamma^\mu D_\mu-m_a\right)\chi_a
\right],
\]

\[
D_\mu\chi_a=(\nabla_\mu+i e_Rq_aA_\mu)\chi_a.
\]

This closes the ordinary QED known limit **by explicit field-content adoption**.
It is not called an emergence theorem from the current MTS scalar.

The one-loop beta-function form is derived conditionally, but its coefficient
and thresholds depend on charged representations and masses that MTS has not
derived. The old particle documents are retained as heuristic/numerical assets
and quarantined from current primitive particle claims.

```text
primitive scalar -> charged fermions     = not derived
current soliton particle claims          = quarantined, assets retained
standard Dirac-QED correspondence        = explicitly adopted
QED beta-function form                   = derived conditionally
charged spectrum and thresholds          = imported/open
alpha(0) boundary                        = one 4899 calibration
```

## 1. Full particle-corpus field-content scan

All twelve Markdown files under `quantum-particle-field` were scanned for the
minimum structures needed by a charged spin-one-half quantum field theory.

| required object | occurrences | files containing it |
|---|---:|---:|
| Grassmann measure | 0 | 0 |
| Dirac operator | 0 | 0 |
| Clifford module | 0 | 0 |
| spinor field | 0 | 0 |
| fermion field | 0 | 0 |
| spin-statistics map | 0 | 0 |
| principal `U(1)` connection | 0 | 0 |
| gauge-covariant matter derivative | 0 | 0 |

The files do contain scalar amplitudes, angular winding, curvature-memory
proxies and numerical matrices. Those can be useful model ingredients. They do
not supply the field representation, anticommuting measure, current or gauge
coupling needed for an electron, muon, tau, quark or neutrino field.

Checkpoint 4877 independently reached the same determinant-level conclusion:
the primitive substrate is bosonic as written, so soliton labels cannot be
inserted as Dirac determinants.

## 2. Winding is not yet electric charge or spin

The lepton-family ansatz is

\[
\psi_n(r,\theta)=\psi_{\rm soliton}(r)e^{in\theta}.
\]

This has a legitimate integer spatial winding label. However:

1. it is orbital/topological winding of a scalar, not a spinor
   representation of `Spin(1,3)`;
2. no covariant derivative `D_mu psi=(partial_mu+i q A_mu)psi` or moment map
   identifies `n` with the charge of the selected principal `U(1)`;
3. equality of a scalar energy proxy under `n -> -n` proves an even energy
   functional, not charge conjugation of a quantum matter action;
4. the document's own viability criterion says modes `n<=5` survive, then
   assigns only `n=1,2,3` to observed leptons, so it does not select exactly
   three families.

Ordinary perturbative excitations of the printed scalar carry integer spin.
A bosonic soliton could in principle quantize as a fermion through a nontrivial
configuration-space topology and a Finkelstein-Rubinstein sign constraint, but
no such configuration space, fundamental group, topological term or quantum
constraint occurs in the corpus. That loophole remains a possible future
derivation route rather than a current result.

Compact `U(1)` does not finish the selection. Any vectorlike Dirac field of
integer charge is anomaly-free:

\[
q^3+(-q)^3=0,
\qquad
q+(-q)=0.
\]

Thus Abelian compactness and vectorlike anomaly cancellation permit many charge
lattices; they do not pick the observed one.

## 3. Executable lepton-soliton reshoot

The published lepton script solves

\[
\psi''=-1.2\psi-|\psi|^{0.75}\psi
\]

with the three selected initial amplitudes

```text
psi_e=0.4;
psi_mu=4.33;
psi_tau=13.40;  # source labels this a tau-only fine adjustment
```

and integrates an `r^2`-weighted positive proxy to a hard endpoint. The 4900
runner reproduces the printed `R=40` ratios, then changes only the endpoint:

| `R_max` | `M_mu/M_e` | `M_tau/M_mu` | `|psi_e(R)|` | `|psi_mu(R)|` | `|psi_tau(R)|` |
|---:|---:|---:|---:|---:|---:|
| 10 | 214.636316 | 14.543959 | 0.387472 | 3.206640 | 4.334099 |
| 20 | 202.385407 | 16.793634 | 0.350836 | 0.599704 | 9.947613 |
| 40 | 202.723816 | 16.717441 | 0.217544 | 4.125574 | 2.034501 |
| 80 | 211.025216 | 16.518329 | 0.153395 | 3.541142 | 12.603967 |

None of the profiles approaches a localized zero boundary in this test. From
`R=40` to `R=80`, the three integrated proxies grow with powers

```text
electron-like: 2.945;
muon-like:     3.003;
tau-like:      2.986.
```

That is the expected approximately `R^3` growth of a bounded nondecaying
oscillation under an `r^2` measure. The printed quantities are therefore
cutoff-dependent amplitude integrals, not converged finite-energy soliton
masses. Three amplitude inputs are also used to match two displayed mass
ratios; the amplitudes are labels chosen from the data, not eigenvalues selected
by a boundary-value problem.

The result is not discarded: it is a reproducible nonlinear amplitude-to-proxy
map. Its evidential status changes from particle-mass prediction to heuristic
regression until a regular-center, decaying-boundary eigenproblem selects the
amplitudes before mass data are inspected.

## 4. Other particle-claim audit

| file/sector | decisive result | retained asset |
|---|---|---|
| finite lepton families | `n<=5` does not imply three; no spin/U1 map | winding-cost diagnostic |
| lepton masses | selected amplitudes and nonconvergent radial integral | nonlinear proxy solver |
| quark hierarchy | six flavour amplitudes are assigned and code explicitly minimizes a loss against target ratios | scalar regression experiment |
| proton soliton | `938 MeV` and `0.84 fm` are asserted without an executable, dimensionally closed BVP producing them | candidate nonlinear BVP |
| neutrino mixing | numerical Hermitian matrix entries are supplied without a parent derivation or weak-spinor readout | matrix diagonalization target |
| Yang-Mills gap | `J^mu partial_mu C` is not proved positive/coercive; residual energy in a finite damped grid is not a continuum quantum spectral gap | nonlinear damping experiment |

No current primitive particle claim is promoted from these files. Their ideas,
code and failure information remain available for reconstruction.

## 5. Explicit Dirac-QED correspondence module

To obtain a valid known limit now, declare the following additional parent
data:

1. the public spacetime is spin and carries a tetrad compatible with `g`;
2. `chi_a` are independent Grassmann Dirac fields;
3. `gamma^mu` realizes the Clifford algebra;
4. each field carries a chosen vectorlike `U(1)` representation `q_a`;
5. all kinetic terms use the same public metric and connection;
6. `e_R(0)` is inherited from the single checkpoint-4899 alpha calibration.

The current is

\[
j^\mu=\sum_aq_a\bar\chi_a\gamma^\mu\chi_a,
\qquad
\nabla_\mu j^\mu=0.
\]

Each Dirac pair cancels its pure Abelian and mixed gravitational chiral anomaly
as shown above. The module therefore provides a consistent vectorlike QED
known limit without inventing a scalar-to-fermion map.

This branch adopts the representation list and masses as matter data. It does
not derive the Standard Model's chiral representations, fractional quark
charges, family replication or Yukawa spectrum.

## 6. Conditional one-loop QED running

For Dirac fields of charge `q_f` and multiplicity/color `N_c`, and charged
complex scalars of charge `q_s`, define

\[
B_D=\sum_fN_cq_f^2,
\qquad
B_S=\sum_sq_s^2,
\qquad
B_{\rm eff}=B_D+\frac14B_S.
\]

The one-loop equations are

\[
\boxed{
\beta(e)=\frac{e^3}{12\pi^2}B_D
+\frac{e^3}{48\pi^2}B_S,
}
\]

\[
\boxed{
\frac{d\alpha}{d\ln\mu}
=\frac{2\alpha^2}{3\pi}B_{\rm eff}.
}
\]

With a fixed massless active set,

\[
\alpha^{-1}(\mu)=\alpha^{-1}(\mu_0)
-\frac{2B_{\rm eff}}{3\pi}\ln(\mu/\mu_0).
\]

Using the same calibrated `alpha(0)` and a deliberately schematic scale ratio
`mu/mu0=1000` gives:

| conditional active spectrum | `B_eff` | resulting `alpha^-1` |
|---|---:|---:|
| one unit-charge Dirac field | 1 | 135.570128 |
| three unit-charge Dirac leptons | 3 | 132.638386 |
| imported free SM below top | 20/3 | 127.263525 |
| imported full SM above top | 8 | 125.309030 |
| one unit-charge complex scalar | 1/4 | 136.669531 |

These are structure smokes, not physical threshold predictions. In particular,
the free-quark row omits nonperturbative hadronic matching. Their spread proves
the key point: the one-loop law follows from the QED action, but its slope does
not follow until the charged spectrum and thresholds are fixed.

The scalar row is also decisive. Even if the primitive complex `psi` were
gauged, its one-loop weight is one quarter of a Dirac field's weight. Calling a
scalar winding mode an electron would therefore insert the wrong spin/statistics
vacuum polarization as well as the wrong representation.

## 7. Primitive-particle promotion gate

A primitive MTS particle derivation requires all first nine clauses:

1. a parent Grassmann measure;
2. a parent Clifford/spin bundle;
3. a spin-statistics theorem;
4. a soliton-to-`U(1)` Noether moment map;
5. a derived exclusion of lepton modes beyond exactly three;
6. quark color, weak chirality and fractional charge representations;
7. anomaly cancellation on the derived chiral spectrum;
8. normalizable mass eigenstates with data-independent boundary conditions;
9. the charged beta weight and all thresholds.

None closes. Clause 10 records that an honest standard-QED correspondence
fallback exists; that fallback is not counted as primitive derivation.

## 8. Arbitration

```text
CURRENT SCALAR-SOLITON PARTICLE CLAIMS
    -> NOT FIELD-THEORETIC FERMION/CHARGE DERIVATIONS
    -> QUARANTINED; HEURISTIC AND NUMERICAL ASSETS RETAINED

STANDARD QED KNOWN LIMIT
    -> EXPLICIT DIRAC-QED MODULE ADOPTED
    -> SAME PUBLIC METRIC AND PRINCIPAL U1
    -> ONE ALPHA(0) CALIBRATION

QED RUNNING
    -> BETA-FUNCTION FORM DERIVED
    -> SPECTRUM, MASSES AND THRESHOLDS IMPORTED/OPEN

CLASSICAL-ONLY FREEZE
    -> AVOIDED WITHOUT CLAIMING SCALAR FERMION EMERGENCE
```

This is a net advance. The unified action can now possess a valid QED known
limit while the much harder primitive origin of charged matter remains a clean,
testable research programme rather than an overclaim.

No GitHub action or public particle claim follows from this checkpoint.

## Sources

- `post-checkpoint-work/4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md`.
- `post-checkpoint-work/4854-Y5-R2FR-parent-U1-connection-adoption-or-CP2-Berry-constructor-and-time-flow-constitutive-gate.md`.
- `post-checkpoint-work/4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md`.
- `post-checkpoint-work/4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md`.
- `quantum-particle-field/leptons-neutrinos/finite-lepton-families-from-curvature-memory-geometry.md`.
- `quantum-particle-field/leptons-neutrinos/the-lepton-mass-hierarchy-from-motion-timespace.md`.
- `quantum-particle-field/quarks-protons/the-quark-mass-hierarchy-from-motion-timespace.md`.
- `quantum-particle-field/quarks-protons/the-proton-as-a-fundamental-mts-soliton.md`.
- `quantum-particle-field/leptons-neutrinos/neutrino-mixing-from-motion-timespace-geometry.md`.
- `quantum-particle-field/yang-mills/yang-mills-mass-gap-via-the-motion-theory.md`.
- [NIST 2022 CODATA alpha](https://physics.nist.gov/cuu/pdf/wall_2022.pdf).
- [Gell-Mann and Low, QED at small distances](https://doi.org/10.1103/PhysRev.95.1300).

## Next target

`4901-Y5-R2FR-nonabelian-SU2xSU3-parent-and-chiral-anomaly-cancellation-or-standard-model-correspondence-freeze.md`
