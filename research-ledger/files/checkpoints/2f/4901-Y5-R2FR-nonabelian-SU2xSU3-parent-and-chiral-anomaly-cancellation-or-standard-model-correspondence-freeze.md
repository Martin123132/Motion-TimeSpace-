# 4901 - Non-Abelian chiral parent, anomaly cancellation and Standard-Model correspondence

Marker: `MTS_NONABELIAN_CHIRAL_SM_CORRESPONDENCE_GATE_4901`

## Decision

The current MTS parent does not derive the Standard Model gauge group or its
chiral matter representations. The only non-Abelian source in the original
core/particle corpus is a legacy generic Yang-Mills mass-gap document. Its
standard `A,F` kinematics are useful, but its proposed curvature-resistance
equation is not gauge covariant and its positivity and spectral-gap steps do
not follow.

The competitive framework therefore takes the same disciplined route used for
GR, Maxwell and QED: write an explicit anomaly-free Standard-Model
correspondence module on the one public metric, and keep the deeper primitive
origin question open.

This checkpoint also obtains a real conditional derivation rather than merely
copying a charge table. Once the five one-generation chiral multiplets, one
Higgs doublet, the three Yukawa operators, and anomaly cancellation are
adopted, a rank-five linear system fixes all six hypercharges up to one overall
normalization. Setting `Y_H=1/2` gives exactly

```text
(Y_Q,Y_uc,Y_dc,Y_L,Y_ec,Y_H)
    = (1/6,-2/3,1/3,-1/2,1,1/2).
```

That theorem does not derive why MTS selects those multiplets, one Higgs, three
families or the Yukawa operators. It sharply separates a representation-level
consistency result from a primitive unification claim.

```text
primitive SU3c x SU2L parent          = not derived
legacy MTS Yang-Mills mass-gap claim  = quarantined
CP2 internal geometry                 = retained as a U2 clue
Standard-Model known limit            = explicitly adopted
local and global anomaly cancellation = exactly verified
hypercharge ratios                    = conditionally derived
overall couplings and mass parameters = imported/calibrated
```

## 1. Corpus audit

The executable audit scans all 26 Markdown files in `core-mts-framework` and
`quantum-particle-field`.

| object | corpus result |
|---|---:|
| files containing an `SU(2)` label | 1 |
| files containing an `SU(3)` label | 1 |
| files containing hypercharge | 0 |
| files containing a chiral representation | 0 |
| files containing a left-Weyl field | 0 |
| files containing a principal non-Abelian connection | 0 |

Both group labels occur in the same legacy Yang-Mills document. The current
integrated-metric parent permits generic matter/gauge placeholders and the 4854
baseline explicitly owns a principal `U(1)`; neither supplies principal
`SU(3)_c` or `SU(2)_L` bundles, transition data, chiral representations or a
group selector.

## 2. Legacy curvature-resistance Yang-Mills audit

The old document begins with valid standard kinematics,

\[
A_\mu\in\mathfrak g,
\qquad
F_{\mu\nu}=\partial_\mu A_\nu-\partial_\nu A_\mu+[A_\mu,A_\nu],
\qquad
\mathcal L_{\rm YM}=-\frac14\operatorname{Tr}F_{\mu\nu}F^{\mu\nu}.
\]

Those equations are retained. The claimed MTS extension is not.

### 2.1 The proposed scalar is not globally regular

The document sets

\[
C(F)=\sqrt{\operatorname{Tr}(F_{\mu\nu}F^{\mu\nu})}.
\]

In Lorentz signature, `Tr(F^2)` is not positive: electric-dominated and
magnetic-dominated configurations have opposite signs. The square root is also
nonanalytic at `F=0`. Thus `C` is not a globally real smooth local scalar on
the claimed configuration space.

### 2.2 The displayed equation is not gauge covariant

The document writes

\[
D^\mu F_{\mu\nu}=\alpha\partial_\nu C.
\]

The left-hand side transforms in the adjoint representation. The right-hand
side is a gauge singlet. They cannot be equated without an additional
adjoint-valued field or current and its covariant conservation law.

Moreover, varying the displayed interaction

\[
\partial^\mu\phi\,\partial_\mu C(F)
\]

with respect to `A` produces derivative constitutive terms through
`delta C/delta F`; it does not produce the printed singlet source directly.

### 2.3 Positivity and a mass gap do not follow

The Lorentz contraction

\[
\partial^\mu\phi\,\partial_\mu C
\]

has no fixed sign. A damping term in a finite classical grid also does not
construct a self-adjoint continuum gauge Hamiltonian, gauge-invariant Hilbert
space or a volume-uniform lower spectral bound. Residual finite-box energy is
not a Yang-Mills quantum mass gap.

The document is retained as a nonlinear dissipative simulation and operator
design asset. Its mass-gap and QCD claims are quarantined.

## 3. What the `CP^2` route can and cannot provide

Checkpoint 4854 uses

\[
CP^2=SU(3)/S(U(2)\times U(1))
\]

as a minimal target with a nondegenerate Berry two-form. This is a meaningful
clue:

- the tautological line supplies the already-discussed `U(1)` Berry
  connection;
- the rank-two quotient bundle admits a canonical `U(2)` connection and may
  motivate an `SU(2)xU(1)` internal construction;
- `SU(3)` is a global target-space isometry.

But a global `SU(3)` isometry is not an independent local `SU(3)_c` gauge
connection. Gauging it introduces new connection variables and dynamics. The
current construction also lacks an independent color bundle, chiral Weyl
matter and a representation selector. `CP^2` therefore remains a geometric
UV clue, not a Standard-Model derivation.

## 4. Explicit Standard-Model correspondence module

On the public spin spacetime, adopt the local gauge algebra

\[
\mathfrak g_{\rm SM}=\mathfrak{su}(3)_c\oplus
\mathfrak{su}(2)_L\oplus\mathfrak u(1)_Y.
\]

The global discrete quotient is left open because the parent does not select
it. With canonical fields, the correspondence action is

\[
\begin{aligned}
S_{\rm SM}=\int d^4x\sqrt{-g}\,[
&-\tfrac14G^A_{\mu\nu}G_A^{\mu\nu}
-\tfrac14W^I_{\mu\nu}W_I^{\mu\nu}
-\tfrac14B_{\mu\nu}B^{\mu\nu}\\
&+\sum_f i\chi_f^\dagger\bar\sigma^\mu D_\mu\chi_f
+(D_\mu H)^\dagger D^\mu H-V(H)
-\mathcal L_Y].
\end{aligned}
\]

For one generation, all fermions are represented as left-handed Weyl fields:

| field | `SU(3)_c` | `SU(2)_L` | `Y` |
|---|---:|---:|---:|
| `Q_L` | `3` | `2` | `1/6` |
| `u_R^c` | `bar 3` | `1` | `-2/3` |
| `d_R^c` | `bar 3` | `1` | `1/3` |
| `L_L` | `1` | `2` | `-1/2` |
| `e_R^c` | `1` | `1` | `1` |
| `H` | `1` | `2` | `1/2` |

Three copies and the Yukawa matrices are correspondence data. They are not
read from the scalar winding labels quarantined at 4900.

## 5. Exact anomaly ledger

For one adopted generation, the perturbative anomaly sums are

\[
[SU(3)_c]^3:\quad 2-1-1=0,
\]

\[
[SU(3)_c]^2U(1)_Y:\quad
2Y_Q+Y_{u^c}+Y_{d^c}=0,
\]

\[
[SU(2)_L]^2U(1)_Y:\quad 3Y_Q+Y_L=0,
\]

\[
[U(1)_Y]^3:\quad
6Y_Q^3+3Y_{u^c}^3+3Y_{d^c}^3+2Y_L^3+Y_{e^c}^3=0,
\]

\[
[\mathrm{grav}]^2U(1)_Y:\quad
6Y_Q+3Y_{u^c}+3Y_{d^c}+2Y_L+Y_{e^c}=0.
\]

The local cubic `SU(2)` anomaly vanishes because its fundamental is
pseudoreal. The Witten global anomaly also cancels: one generation contains
three colored `Q_L` doublets plus one `L_L` doublet, for an even total of four.

These are exact consistency checks. Anomaly cancellation by itself does not
explain why the adopted representations exist.

## 6. Conditional hypercharge-ratio theorem

Use the variable order

\[
y=(Y_Q,Y_{u^c},Y_{d^c},Y_L,Y_{e^c},Y_H)^T.
\]

Gauge invariance of the up, down and charged-lepton Yukawa operators gives

\[
Y_Q+Y_{u^c}+Y_H=0,
\quad
Y_Q+Y_{d^c}-Y_H=0,
\quad
Y_L+Y_{e^c}-Y_H=0.
\]

Append the mixed `SU(3)^2U(1)`, `SU(2)^2U(1)` and gravitational equations.
The resulting integer matrix is

\[
M=\begin{pmatrix}
1&1&0&0&0&1\\
1&0&1&0&0&-1\\
0&0&0&1&1&-1\\
2&1&1&0&0&0\\
3&0&0&1&0&0\\
6&3&3&2&1&0
\end{pmatrix}.
\]

Exact symbolic elimination gives

\[
\operatorname{rank}M=5,
\qquad
\dim\ker M=1,
\]

with basis vector

\[
\ker M=\operatorname{span}
\left\{(1/3,-4/3,2/3,-1,2,1)^T\right\}.
\]

Normalizing `Y_H=1/2` yields the Standard-Model hypercharges displayed above,
and the cubic `U(1)` anomaly then vanishes exactly. Electric charge follows
conditionally from the adopted electroweak breaking generator,

\[
Q=T_3+Y,
\]

giving `(2/3,-1/3)` for the quark doublet and `(0,-1)` for the lepton doublet.

This is not a numerical fit. It is an exact rank theorem. Its assumptions are
also explicit: the representation dimensions, one Higgs doublet, all three
Yukawa operators and no baseline right-handed neutrino.

If a right-handed-neutrino conjugate and a Dirac-neutrino Yukawa are added, the
linear system has nullity two because a second anomaly-free direction survives.
A gauge-invariant Majorana condition `Y_{nu^c}=0` restores nullity one. The
particle parent must therefore decide the neutrino branch before calling charge
quantization primitive.

## 7. Electromagnetic correspondence after symmetry breaking

The adopted known-limit relations are

\[
A_\mu=\sin\theta_W W^3_\mu+\cos\theta_W B_\mu,
\qquad
Z_\mu=\cos\theta_W W^3_\mu-\sin\theta_W B_\mu,
\]

\[
e=g_2\sin\theta_W=g_Y\cos\theta_W.
\]

This embeds the checkpoint-4899 calibrated electromagnetic coupling into the
electroweak module. It does not predict `g_2`, `g_Y`, the weak angle, the Higgs
vacuum value or Yukawa matrices. Those are the next ownership problem.

## 8. Promotion gate and arbitration

A primitive non-Abelian MTS derivation still requires parent-owned:

1. principal `SU(3)_c` and `SU(2)_L` bundles;
2. Yang-Mills kinetic normalization and gauge couplings;
3. chiral Weyl fields and their representations;
4. exactly three families;
5. a hypercharge and global-quotient selector;
6. a Higgs or alternative symmetry-breaking owner;
7. Yukawa/flavor matrices or an alternative mass theorem;
8. a valid QCD confinement/mass-gap route.

The adopted spectrum passes all local and global anomaly tests, so the
Standard-Model correspondence branch is internally consistent. The primitive
promotion gate remains closed.

No GitHub action or public unification, particle, QCD or mass-gap claim follows
from this checkpoint.

## Sources

- `post-checkpoint-work/4854-Y5-R2FR-parent-U1-connection-adoption-or-CP2-Berry-constructor-and-time-flow-constitutive-gate.md`.
- `post-checkpoint-work/4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md`.
- `post-checkpoint-work/4900-Y5-R2FR-charged-matter-representation-lattice-and-QED-beta-function-or-classical-EM-freeze.md`.
- `quantum-particle-field/yang-mills/yang-mills-mass-gap-via-the-motion-theory.md`.
- [Yang and Mills, local gauge invariance](https://doi.org/10.1103/PhysRev.96.191).
- [Weinberg, electroweak model](https://doi.org/10.1103/PhysRevLett.19.1264).
- [Adler, chiral anomaly](https://doi.org/10.1103/PhysRev.177.2426).
- [Witten, global `SU(2)` anomaly](https://doi.org/10.1016/0370-2693(82)90728-6).

## Next target

`4902-Y5-R2FR-electroweak-breaking-Higgs-Yukawa-owner-and-mass-generation-or-SM-parameter-freeze.md`
