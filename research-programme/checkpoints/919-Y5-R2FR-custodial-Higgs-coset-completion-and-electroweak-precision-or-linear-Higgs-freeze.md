# 4903 - Custodial Higgs completion, precision smoke and route freeze

Marker: `MTS_CUSTODIAL_HIGGS_COMPLETION_PRECISION_GATE_4903`

## Decision

The smallest standard custodial completion in Higgs field count is

\[
SO(5)/SO(4)\simeq S^4.
\]

It has four real Goldstone coordinates, transforming as `(2,2)` under
`SU(2)_L x SU(2)_R`, so it retains exactly one complex Higgs doublet without
extra pseudo-Goldstone fields. Unlike raw `CP^2`, it derives `rho=1` at every
vacuum-misalignment angle.

The completion also gives a one-parameter gauge-coupling correlation,

\[
\kappa_V=\sqrt{1-\xi},
\qquad
\kappa_{2V}=1-2\xi,
\qquad
\kappa_{2V}=2\kappa_V^2-1,
\]

where `xi=v^2/f^2`. Translating the 2026 ATLAS+CMS Run-2 Higgs-pair interval
`0.73<kappa_2V<1.3` gives the conditional smoke bound

\[
\xi<0.135,
\qquad
f/v>2.721655.
\]

This is a viable custodial benchmark, not an MTS derivation. No existing MTS
field, current, condensate or constraint selects `SO(5)`, its breaking to
`SO(4)`, the scale `f`, the vacuum angle, fermion embeddings or the explicit
breaking potential. The full experimental likelihood was not reproduced.

The arbitration is therefore decisive:

```text
raw CP2 Higgs route   -> frozen as an internal U2 geometry clue
SO5/SO4 completion    -> retained as an optional precision benchmark
active MTS known limit -> linear Standard-Model Higgs correspondence
primitive Higgs claim -> not allowed
```

The programme now leaves the Higgs sub-branch and returns to the unified-action
spine rather than manufacturing further cosets.

## 1. Minimal field-count custodial construction

The group dimensions are

\[
\dim SO(5)-\dim SO(4)=10-6=4.
\]

Using the local isomorphism

\[
SO(4)\simeq SU(2)_L\times SU(2)_R,
\]

the four broken generators transform as `(2,2)`. Gauging `SU(2)_L` and
`Y=T_R^3` packages the four real fields into one complex doublet with
`Y=1/2` after the checkpoint-4901 normalization.

In unitary orientation, use

\[
\Sigma(h)=
(0,0,0,\sin(h/f),\cos(h/f))^T,
\qquad
\Sigma^T\Sigma=1,
\]

with kinetic action

\[
\mathcal L_\Sigma=\frac{f^2}{2}(D_\mu\Sigma)^T(D^\mu\Sigma).
\]

This construction is minimal in pseudo-Goldstone field count, not a proof that
no other four-dimensional custodial realization exists.

As with `CP^2`, the exact global group acts transitively on the homogeneous
space. An exactly `SO(5)`-invariant scalar potential is constant. Gauge,
fermion or other parent spurions are still required for vacuum misalignment.

## 2. Exact custodial mass theorem

Let the vacuum angle be `theta` and define

\[
v=f\sin\theta.
\]

The gauged sigma kinetic term gives

\[
m_W^2=\frac{g_2^2f^2\sin^2\theta}{4},
\qquad
m_Z^2=\frac{(g_2^2+g_Y^2)f^2\sin^2\theta}{4}.
\]

The orthogonal neutral combination remains massless. Therefore

\[
\boxed{
\rho=\frac{m_W^2}{m_Z^2\cos^2\theta_W}=1
}
\]

for every `theta`. This repairs the checkpoint-4902 result
`rho_CP2=1+t^2` without increasing the scalar field count.

## 3. Correlated Higgs couplings

The gauge-boson mass function in the fluctuating Higgs direction is

\[
m_V^2(h)=C_V\sin^2(\theta+h/f).
\]

Comparing its first and second derivatives with the linear Standard-Model
normalization gives

\[
\boxed{\kappa_V=\cos\theta=\sqrt{1-\xi}},
\]

\[
\boxed{\kappa_{2V}=\cos2\theta=1-2\xi},
\]

where

\[
\xi=\frac{v^2}{f^2}=\sin^2\theta.
\]

Eliminating `xi` produces the overconstraining curve

\[
\boxed{\kappa_{2V}=2\kappa_V^2-1}.
\]

This correlation is the genuine predictive content of the optional gauge
sector. Fermion coupling modifiers are not unique until the chiral fields are
embedded into representations of the larger group.

## 4. Primary-data precision smoke

The February 2026 ATLAS+CMS Run-2 Higgs-pair combination reports the observed
individual 95% interval

\[
0.73<\kappa_{2V}<1.3.
\]

On the minimal custodial branch, `0<=xi<=1` and `kappa_2V=1-2xi<=1`.
The lower endpoint therefore implies

\[
1-2\xi>0.73
\quad\Longrightarrow\quad
\boxed{\xi<0.135=27/200}.
\]

Consequently

\[
\boxed{f/v>1/\sqrt{0.135}=2.721655},
\]

and the same branch implies `kappa_V>0.930054`.

This is an interval translation, not a reproduction of the ATLAS+CMS
likelihood. It assumes the minimal relation, no additional operators, and the
published individual one-dimensional interval. It is tagged private nonclaim.

## 5. Route comparator

| route | real scalar count | tree `rho` | new scale | MTS-selected? | status |
|---|---:|---:|---:|---:|---|
| linear Standard-Model Higgs | 4 | `1` | none beyond `v` | no | active known limit |
| `CP^2=SU(3)/U(2)` | 4 | `1+t^2` | `f_CP2` | no | frozen as geometry clue |
| `SO(5)/SO(4)` | 4 | `1` | `f` and `theta` | no | optional precision benchmark |

The custodial completion repairs the precision identity and supplies a
correlated gauge test. It does not improve primitive ownership because it adds
an unselected group/breaking pattern and leaves the potential, flavor
embeddings and resonance spectrum open.

## 6. Parent-ownership gate

The current corpus does not supply:

1. an `SO(5)` global current or parent action;
2. a condensate or constraint deriving `SO(5)->SO(4)`;
3. the scale `f`;
4. the vacuum angle `theta`;
5. explicit-breaking potential coefficients;
6. fermion embeddings fixing `kappa_f`;
7. vector/fermion resonances needed for oblique and high-energy predictions.

The constructed branch does close:

- one-doublet field count;
- positive nonlinear kinetic geometry;
- tree custodial `rho=1`;
- the `kappa_V,kappa_2V` correlation;
- a source-backed conditional precision bound.

This is enough to retain it as a benchmark, not enough to promote it into the
MTS parent.

## 7. Arbitration and programme redirect

The particle known-limit layer is now disciplined:

```text
Dirac-QED                     = explicit correspondence
chiral Standard Model         = explicit anomaly-free correspondence
relative hypercharge ratios   = conditional exact theorem
linear Higgs                  = active correspondence
CP2 Higgs                     = frozen
SO5/SO4 composite Higgs       = optional bounded benchmark
Yukawa and neutrino matrices  = imported/open
```

The next work is not another particle ansatz. It is to assemble the actual
current action, Ward identities, limits and free-parameter/prediction ledger in
one executable unified spine.

No GitHub action or public composite-Higgs, precision or unification claim
follows from this checkpoint.

## Sources

- `post-checkpoint-work/4902-Y5-R2FR-electroweak-breaking-Higgs-Yukawa-owner-and-mass-generation-or-SM-parameter-freeze.md`.
- `post-checkpoint-work/4901-Y5-R2FR-nonabelian-SU2xSU3-parent-and-chiral-anomaly-cancellation-or-standard-model-correspondence-freeze.md`.
- [Kaplan and Georgi, vacuum misalignment](https://doi.org/10.1016/0370-2693(84)91177-8).
- [Kaplan, Georgi and Dimopoulos, composite Higgs](https://doi.org/10.1016/0370-2693(84)91178-X).
- [Georgi and Kaplan, custodial composite Higgs](https://doi.org/10.1016/0370-2693(84)90341-1).
- [ATLAS+CMS Run-2 Higgs-pair combination](https://arxiv.org/abs/2602.23991).

## Next target

`4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md`
