# 4895 - Full positive spectral matrix, clock counterterms, and local-GR decoupling

Marker: `MTS_FULL_SPECTRAL_MATRIX_LOCAL_DECOUPLING_GATE_4895`

## Decision

Checkpoint 4894 proved that the one-sided memory equation was not a positive
reciprocal bath parent. This checkpoint constructs the missing parent rather
than merely listing it as absent.

The super-Drude spectral density has an exact double-pole retarded
susceptibility. Its minimal positive two-channel completion is rank one and
couples the collective variable

\[
s=\phi+q\theta,
\qquad
q=\frac{2\sigma}{\gamma\Lambda}.
\]

There are three possible static subtraction patterns. No subtraction leaves
the unwanted `phi^2` and `theta^2` susceptibilities. Subtracting the complete
Gram matrix also removes the desired `sigma phi theta` source. The unique
subtraction satisfying the three already-selected infrared conditions is the
diagonal one:

\[
K^{\rm ren}_{\phi\phi}(0)=0,
\qquad
K^{\rm ren}_{\theta\theta}(0)=0,
\qquad
K^{\rm ren}_{\phi\theta}(0)=\sigma.
\]

It produces the old cross source, the exact nonlocal auto response, the
compulsory reciprocal clock response, and one positive FDT noise matrix from
the same kernel.

On the stationary equilibrium branch, `theta=phi=s=0`. The influence action,
counterterms and induced bath displacement are quadratic in these variables,
so their first metric variation vanishes. This gives an exact conditional
mean-field decoupling to the already-selected EH/Newton/PPN/Maxwell branch.

The bath-cosmology route is therefore **not retired**. The old local Markov
cosmology remains demoted: the new full-matrix background, bath stress and
finite-`k` constraints have not yet been solved.

## 1. Exact positive retarded matrix

For

\[
J_{\phi\phi}(\omega)
=\frac{\gamma\omega}{[1+(\omega/\Lambda)^2]^2},
\qquad
C_{\phi\phi}=\frac{\gamma\Lambda}{2},
\]

causality and the dispersion relation give

\[
\boxed{
K_R(\omega)=\frac{C_{\phi\phi}}
{(1-i\omega/\Lambda)^2}
}
\]

and

\[
k_R(t)=C_{\phi\phi}\Lambda^2t e^{-\Lambda t}\Theta(t).
\]

The only poles are a double pole at `omega=-i Lambda`; there is no
upper-half-plane pole. Its imaginary part is exactly the input spectrum:

\[
\operatorname{Im}K_R
=\frac{\gamma\omega}{[1+(\omega/\Lambda)^2]^2}.
\]

The minimal common-bath completion is

\[
\boxed{
K^R_{AB}(\omega)=v_Av_BK_R(\omega),
\qquad v=(1,q)
}
\]

with spectral eigenvalues

\[
0,
\qquad
J_{\phi\phi}(1+q^2)\ge0.
\]

At the inherited FDT ceiling,

```text
Lambda/H0       = 0.251716646;
gamma/H0        = 1;
sigma/H0        = 0.3;
C_phi_phi       = 0.125858323;
q               = 2.383632585;
C_theta_theta   = 0.715089776.
```

These numbers use the largest cutoff allowed by checkpoint 4893. They are a
benchmark, not a parent prediction of `Lambda`.

## 2. Counterterm fork

Integrating out a positive continuum of oscillators gives the static Gram
matrix

\[
C_{AB}=C_{\phi\phi}
\begin{pmatrix}1&q\\q&q^2\end{pmatrix}.
\]

The three subtraction choices are:

| scheme | zero `phi^2` | zero `theta^2` | retains `sigma` | verdict |
|---|---:|---:|---:|---|
| none | no | no | yes | incompatible with selected IR parent |
| full Gram | yes | yes | no | erases expansion source |
| diagonal | yes | yes | yes | unique match to all three IR conditions |

The selected local counterterm is

\[
\boxed{
\Delta K_{\rm ct}
=-\operatorname{diag}(C_{\phi\phi},C_{\theta\theta}),
\qquad
\Delta K_{\phi\theta}=0.
}
\]

Therefore

\[
K^{\rm ren}(0)=
\begin{pmatrix}0&\sigma\\\sigma&0\end{pmatrix}.
\]

This real static matrix is indefinite. That is not a negative spectral
weight: real local counterterms do not enter the FDT noise matrix. The cross
operator is derivative-equivalent to `-sigma u.grad(phi)` and must be tested
with the constrained clock, not as a two-coordinate static potential. The
subtraction is uniquely fixed only after imposing the selected infrared
renormalization conditions; positivity alone does not select it.

## 3. Exact shared-auxiliary localization

The whole rank-one matrix needs only two shared causal auxiliaries:

\[
\dot a_1=s-\Lambda a_1,
\qquad
\dot a_2=a_1-\Lambda a_2,
\qquad
Y=C_{\phi\phi}\Lambda^2a_2.
\]

After diagonal subtraction, the reciprocal forces are

\[
\boxed{
F_\phi=Y-C_{\phi\phi}\phi,
\qquad
F_\theta=qY-C_{\theta\theta}\theta.
}
\]

For constant fields, `Y=C_phi_phi(phi+q theta)`, hence

\[
F_\phi=\sigma\theta,
\qquad
F_\theta=\sigma\phi.
\]

For `theta=0`,

\[
K_R-C_{\phi\phi}=i\omega\widetilde\Gamma(\omega),
\]

so the 4894 generalized Langevin kernel is exactly the diagonal-subtracted
auto susceptibility rather than a separate phenomenological insertion.

The same positive spectrum fixes the noise:

\[
\boxed{
\mathcal N_{AB}(\omega)
=\coth\!\left(\frac{\omega}{2T}\right)
J_{\phi\phi}(\omega)v_Av_B.
}
\]

Its eigenvalues are zero and
`coth(omega/2T) J_phi_phi (1+q^2)`, so response and noise now have one owner.

## 4. Exact stationary local decoupling

Let the bath state be stationary and let

\[
u^\mu=K^\mu/\sqrt{-K^2}
\]

for a timelike Killing field. Then

\[
\theta=\nabla_\mu u^\mu=0.
\]

Choose the background-subtracted memory solution `phi=0` and an equilibrium
retarded history with no coherent incoming bath displacement. It follows that

\[
s=a_1=a_2=Y=F_\phi=F_\theta=0.
\]

Every influence and counterterm contribution is at least quadratic in
`phi`, `theta`, or the induced bath displacement. Thus

\[
\left.\frac{\delta S_{\rm influence+ct}}
{\delta g^{\mu\nu}}\right|_{\phi=\theta=0}=0.
\]

The equilibrium bath state stress remains included once as `T_X`; only its
induced extra response vanishes. Since ordinary matter and Maxwell fields
carry no direct `phi` or clock charge, the stationary equations are

\[
G_{\mu\nu}+\Lambda g_{\mu\nu}
=\overline M_{\rm Pl}^{-2}
(T^{\rm matter}_{\mu\nu}+T^{\rm EM}_{\mu\nu}+T^X_{\mu\nu}).
\]

Consequently, within the existing weak-field certificate domain,

\[
G_N=(8\pi\overline M_{\rm Pl}^2)^{-1},
\qquad
\gamma_{\rm PPN}=\beta_{\rm PPN}=1,
\]

and Maxwell/Poynting energy enters through the ordinary Hilbert stress.

This is a stationary classical mean-field theorem. It does not cover a
coherently excited bath, stochastic metric variance, strong fields, or the
time-dependent clock sector.

## 5. Frequency separation

The cross response is no longer a constant:

\[
\boxed{
\frac{|K_{\phi\theta}(\omega)|}{\sigma}
=\frac1{1+(\omega/\Lambda)^2}.
}
\]

At `omega=H0`, only `0.0595858` of the static cross susceptibility remains,
while the dissipative auto fraction is `0.00355047`. Thus the old local
cosmological source cannot be reused.

At the Earth orbital frequency the cross ratio is `7.62616e-24`; it is even
smaller for Mercury, binary pulsars and 100-Hz waves. Applying this filter to
the cross channel alone reduces the old 4889 Earth two-insertion envelope
from `1.08324e-23` to `6.29994e-70`. This is not a total waveform bound: the
clock stress and counterterm response still require a covariant dynamical
calculation.

## 6. Arbitration

Derived here:

- the exact positive full `2x2` retarded matrix;
- the reciprocal `theta-theta` response;
- the only counterterm pattern matching all three selected IR conditions;
- an exact two-auxiliary localization;
- one positive FDT response/noise owner;
- exact stationary mean-field decoupling to the selected local-GR branch;
- strong finite-frequency filtering of the bath cross channel.

Still open:

- the full covariant bath stress evaluated on nonstationary FLRW;
- the full-matrix background reshoot;
- the clock and Einstein constraints with the reciprocal kernel;
- finite-`k` stochastic response and the physical cutoff selection;
- a complete binary waveform or stochastic local-gravity bound.

Decision:

```text
OLD LOCAL MARKOV BATH COSMOLOGY
    -> REMAINS DEMOTED

FULL POSITIVE RECIPROCAL BATH PARENT
    -> CONSTRUCTED AT HOMOGENEOUS RESPONSE/FDT LEVEL

STATIONARY LOCAL GR/NEWTON/PPN/MAXWELL
    -> EXACTLY DECOUPLED ON THE SELECTED EQUILIBRIUM BRANCH

BATH-COSMOLOGY RETIREMENT
    -> NOT TRIGGERED; ADVANCE TO FULL-MATRIX FLRW STRESS GATE
```

No cosmology likelihood or new public claim is authorized from this
checkpoint.

## Next target

`4896-Y5-R2FR-full-matrix-nonlocal-FLRW-reshoot-covariant-bath-stress-and-constraint-gate.md`

