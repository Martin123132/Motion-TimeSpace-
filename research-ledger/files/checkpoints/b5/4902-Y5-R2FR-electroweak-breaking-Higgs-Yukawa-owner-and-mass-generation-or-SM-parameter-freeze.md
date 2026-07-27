# 4902 - Electroweak breaking, Higgs ownership, Yukawa rank and mass generation

Marker: `MTS_HIGGS_YUKAWA_MASS_OWNERSHIP_GATE_4902`

## Decision

The primitive real MTS scalar is not the Standard-Model Higgs: it is a real
gauge singlet, while electroweak breaking requires a complex `SU(2)_L`
doublet with `Y=1/2` or a demonstrably equivalent nonlinear realization.

The optional `CP^2` geometry does provide a nontrivial partial route. Its
tangent space is one complex `U(2)` doublet and its Fubini-Study metric supplies
a positive nonlinear kinetic term. This is the first internal MTS construction
in the present branch with the correct Higgs representation count.

Two exact obstructions prevent promotion:

1. because `SU(3)` acts transitively on `CP^2=SU(3)/U(2)`, every exactly
   `SU(3)`-invariant scalar potential on `CP^2` is constant; electroweak vacuum
   misalignment therefore needs explicit symmetry-breaking spurions whose
   coefficients are not in the parent;
2. gauging the raw `CP^2` Fubini-Study metric around a nonzero doublet vacuum
   gives `rho=1+t^2`, not the custodial tree result `rho=1`. A custodial
   completion or strict `t->0` limit is compulsory.

The active known limit therefore remains the explicit linear Higgs doublet.
It reproduces `W`, `Z`, photon and Higgs masses and `rho=1`, but an exact
Jacobian calculation shows that its four basic electroweak observables simply
calibrate four independent parameters. Yukawa matrices likewise invert the
charged mass/mixing data rather than predict them.

```text
primitive real psi as Higgs        = rejected
CP2 doublet representation/kinetic = conditionally derived
CP2 potential/vacuum               = not derived
raw CP2 custodial gate             = failed: rho=1+t^2
linear Higgs known limit           = active correspondence
electroweak parameter prediction   = none in four-by-four block
Yukawa/mass spectrum               = imported/open
neutrino mass operator             = imported/open
```

## 1. Field-content ownership audit

The original microscopic action declares

\[
\psi:\mathbb R^4\rightarrow\mathbb R.
\]

No `SU(2)_L` action, hypercharge, complex partner or four-component internal
target is attached to this field. A nonzero expectation value of a gauge
singlet leaves `SU(2)_L x U(1)_Y` unbroken. Relabeling `psi` as `H` would change
the field space and representation rather than derive the Higgs.

Three branches are distinguished:

| candidate | doublet | kinetic owner | potential owner | vacuum owner |
|---|---:|---:|---:|---:|
| primitive real `psi` | no | scalar only | no | no |
| optional `CP^2` target | yes, conditionally | yes | no | no |
| explicit linear `H` | yes | yes | adopted | adopted |

## 2. The `CP^2` Higgs representation theorem

Write

\[
CP^2=SU(3)/U(2).
\]

Its real dimension is

\[
\dim_\mathbb R CP^2=8-4=4,
\]

exactly one complex doublet. At the base point, the isotropy group `U(2)` acts
on the tangent space as its complex fundamental representation:

\[
T_{[z_0]}CP^2\simeq\mathbf 2_\mathbb C.
\]

The `U(1)` generator normalization is still fixed by the checkpoint-4901
hypercharge convention, not by dimension counting.

For an inhomogeneous coordinate `w in C^2`, the Fubini-Study metric is

\[
g_{i\bar j}=f^2
\frac{(1+w^\dagger w)\delta_{i\bar j}-\bar w_iw_j}
{(1+w^\dagger w)^2}.
\]

Writing `r^2=w^dagger w`, its two complex eigenvalues are

\[
\lambda_\perp=\frac{f^2}{1+r^2},
\qquad
\lambda_\parallel=\frac{f^2}{(1+r^2)^2},
\]

and

\[
\det g=\frac{f^4}{(1+r^2)^3}>0.
\]

Thus the conditional nonlinear doublet is ghost-free for `f^2>0`. Near the
origin, `H=f w` gives the canonical linear kinetic term plus operators
suppressed by `f`.

## 3. Exact potential obstruction

`CP^2` is a homogeneous space: `SU(3)` acts transitively. Any scalar function
invariant under the full action has the same value at every point. Therefore

\[
\boxed{V_{SU(3)}([z])=\mathrm{constant}.}
\]

A mass term, quartic, or vacuum-misalignment potential must break the global
`SU(3)` explicitly through electroweak gauging, fermion couplings, a bath
spurion or another parent operator. The current corpus supplies none of their
finite coefficients or signs. Geometry provides the doublet and kinetic
metric, not the electroweak vacuum.

## 4. Raw `CP^2` custodial calculation

Gauge the tangent `U(2)` as `SU(2)_L x U(1)_Y` and choose the dimensionless
vacuum chart

\[
w_0=(0,t)^T.
\]

Evaluating the exact Fubini-Study metric on the gauge orbit gives

\[
m_W^2=\frac{g_2^2f^2t^2}{2(1+t^2)},
\]

\[
m_Z^2=\frac{(g_2^2+g_Y^2)f^2t^2}{2(1+t^2)^2},
\]

with one zero neutral eigenvalue for the photon. Hence

\[
\boxed{
\rho_{CP^2}
=\frac{m_W^2}{m_Z^2\cos^2\theta_W}
=1+t^2.
}
\]

At nonzero `t`, the raw coset lacks the custodial protection of the linear
single-doublet known limit. Small `t` can suppress the deviation, but neither
`t` nor `f` is selected. This is a derived precision obstruction, not a reason
to discard `CP^2`: a larger custodial coset or extra symmetry might repair it,
and that is the next construction target.

## 5. Linear Higgs correspondence

The active known-limit branch retains

\[
H:(1,2)_{1/2},
\qquad
V(H)=-\mu_H^2H^\dagger H+\lambda_H(H^\dagger H)^2.
\]

For

\[
\langle H\rangle=(0,v/\sqrt2)^T,
\qquad
v^2=\mu_H^2/\lambda_H,
\]

the neutral mass matrix is

\[
M_N^2=\frac{v^2}{4}
\begin{pmatrix}
g_2^2&-g_2g_Y\\
-g_2g_Y&g_Y^2
\end{pmatrix}.
\]

Its determinant vanishes, giving a massless photon, while

\[
m_W^2=\frac{g_2^2v^2}{4},
\quad
m_Z^2=\frac{(g_2^2+g_Y^2)v^2}{4},
\quad
m_h^2=2\lambda_Hv^2,
\quad
\rho=1.
\]

These relations close the known limit. `mu_H`, `lambda_H` and `v` remain
correspondence parameters.

## 6. Electroweak identifiability theorem

Take the parameter vector

\[
p=(g_2,g_Y,v,\lambda_H)
\]

and observable-coordinate vector

\[
o=(e^2,m_W^2,m_Z^2,m_h^2),
\qquad
e^2=\frac{g_2^2g_Y^2}{g_2^2+g_Y^2}.
\]

The exact Jacobian determinant is

\[
\boxed{
\det\frac{\partial o}{\partial p}
=-\frac{g_2^3g_Y^3v^5}{g_2^2+g_Y^2}.
}
\]

It is nonzero at a physical point. The map has rank four: four observables fix
four parameters. There is no independent MTS prediction inside this block.
New predictivity requires a parent relation among the parameters or additional
observables sensitive to higher operators.

## 7. Yukawa and charged-mass rank

After breaking,

\[
M_u=Y_uv/\sqrt2,
\qquad
M_d=Y_dv/\sqrt2,
\qquad
M_e=Y_ev/\sqrt2.
\]

The inverse exists trivially:

\[
Y_f=\sqrt2M_f/v.
\]

For three generations, the two quark Yukawa matrices contain ten physical
flavor parameters after field redefinitions: six masses and four CKM
parameters. The charged-lepton matrix supplies three further masses. Thus the
charged flavor sector has thirteen independent inputs for thirteen mass/mixing
observables. It is a parameterization, not a spectrum prediction.

The archived MTS mass calculations do not currently reduce this rank:

- the lepton solver selects three amplitudes for two ratios and its integrals
  grow approximately as the radial cutoff cubed;
- the quark solver assigns one amplitude per flavor and explicitly minimizes a
  loss against three target ratios;
- the neutrino Hamiltonian inserts `Phi_nu`, three `kappa_i`, three symmetric
  and three antisymmetric off-diagonal entries before diagonalization.

Their nonlinear and matrix assets remain available, but none replaces the
Yukawa matrices at checkpoint 4902.

## 8. Neutrino mass branch

The renormalizable correspondence spectrum used at 4901 has massless
neutrinos. A massive branch requires additional data, for example

\[
\frac{c^{(5)}_{ij}}{\Lambda}(L_iH)(L_jH)
\quad\Longrightarrow\quad
M_\nu=\frac{c^{(5)}v^2}{2\Lambda},
\]

or a right-handed-neutrino seesaw,

\[
M_\nu\simeq-\frac{v^2}{2}Y_\nu M_R^{-1}Y_\nu^T.
\]

Neither `c^(5)/Lambda` nor `(Y_nu,M_R)` is parent-derived. The old numerical
curvature Hamiltonian is retained as a target texture, not used as their
derivation.

## 9. Arbitration

The framework now has a stronger result than a simple parameter freeze:

```text
CP2 -> one complex Higgs doublet + positive nonlinear kinetic geometry
    -> no invariant potential
    -> raw custodial relation fails at nonzero chart vacuum
    -> needs a custodial completion before promotion

linear H -> exact SM known limit
         -> four-by-four electroweak map is full rank
         -> Higgs/Yukawa/neutrino coefficients remain inputs
```

No GitHub action or public Higgs, particle-mass, neutrino or unification claim
follows from this checkpoint.

## Sources

- `post-checkpoint-work/4854-Y5-R2FR-parent-U1-connection-adoption-or-CP2-Berry-constructor-and-time-flow-constitutive-gate.md`.
- `post-checkpoint-work/4900-Y5-R2FR-charged-matter-representation-lattice-and-QED-beta-function-or-classical-EM-freeze.md`.
- `post-checkpoint-work/4901-Y5-R2FR-nonabelian-SU2xSU3-parent-and-chiral-anomaly-cancellation-or-standard-model-correspondence-freeze.md`.
- `core-mts-framework/action-principle/the-fundamental-action-of-motion-timespace-field-theory.md`.
- [Higgs, gauge-boson masses](https://doi.org/10.1103/PhysRevLett.13.508).
- [Weinberg, electroweak model](https://doi.org/10.1103/PhysRevLett.19.1264).
- [Kaplan and Georgi, vacuum misalignment](https://doi.org/10.1016/0370-2693(84)91177-8).
- [Kaplan, Georgi and Dimopoulos, composite Higgs](https://doi.org/10.1016/0370-2693(84)91178-X).
- [Weinberg, dimension-five operator analysis](https://doi.org/10.1103/PhysRevLett.43.1566).

## Next target

`4903-Y5-R2FR-custodial-Higgs-coset-completion-and-electroweak-precision-or-linear-Higgs-freeze.md`
