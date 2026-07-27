# 4889 - Constrained bath clock, local cone closure and growth/binary gate

Marker: `MTS_CONSTRAINED_CLOCK_LOCAL_GROWTH_BINARY_4889`

Status: private parent-selection and empirical checkpoint; no full local-GR,
cosmology, bath-identity or fundamental-theory claim.

## 1. Decision

Checkpoint 4888 found that the generic dynamical `P(X)` bath clock is
gradient-stable but has a low-energy clock--memory root above the public
metric cone. This checkpoint does not hide that result with an asserted
nonlocal cure. It compares the existing constrained-flow precedent in
checkpoints 4850--4851 with the expansion source and selects an explicit
fixed-norm irrotational clock parent.

The selected parent:

1. produces exactly the same `sigma_theta theta` memory source;
2. has a unit timelike flow by an Euler--Lagrange constraint;
3. turns the clock into a zero-sound dust constraint rather than an
   additional finite-speed wave;
4. gives the symbolic characteristic polynomial
   `omega^2(omega^2-k^2)`;
5. preserves the three fully backreacted 4888 background rays with positive
   clock multiplier and positive effective inertia;
6. derives a nontrivial subhorizon two-component growth kernel;
7. modestly improves both primary and robustness SDSS/eBOSS scores relative
   to matched LambdaCDM with the same two profiled nuisance parameters;
8. reduces exactly to EH plus universal matter and Maxwell stress on the
   stationary background-subtracted local branch;
9. suppresses finite-frequency orbital/binary leakage below `2.86e-23` in
   the most conservative sampled metric-amplitude envelope.

The generic `P(X)` realization is demoted as the selected local parent. It
could return only with a separately demonstrated nonlocal UV completion.
The constrained route closes the immediate cone obstruction, but it remains
conditional because the clock bath's microscopic identity, zero-density
strong-coupling/caustic behavior, full Einstein--Boltzmann equations and SK
noise perturbations are not yet closed.

## 2. Fixed-norm parent action

Let `U` be an irrotational clock potential and `varrho` a multiplier. Select

\[
\boxed{
S_{U\phi}=\int d^4x\sqrt{-g}\left[
-\frac{\varrho}{2}
(\nabla_\mu U\nabla^\mu U+1)
+\overline M_{\rm Pl}^2\sigma_\theta
\nabla_\mu\phi\nabla^\mu U
\right].
}
\]

Define

\[
u_\mu=-\nabla_\mu U.
\]

Variation of `varrho` gives

\[
\boxed{u_\mu u^\mu=-1}.
\]

The memory equation is

\[
\Box\phi-\kappa\phi^3-\sigma_\theta\Box U=0.
\]

Since

\[
\theta=\nabla_\mu u^\mu=-\Box U,
\]

this is exactly

\[
\boxed{\Box\phi-\kappa\phi^3+\sigma_\theta\theta=0}.
\]

The clock current is

\[
\boxed{
J_U^\mu=\varrho u^\mu
+\overline M_{\rm Pl}^2\sigma_\theta\nabla^\mu\phi,
\qquad
\nabla_\mu J_U^\mu=0
}
\]

before the already-selected SK bath transfers damping energy.

This is an action, not a plateau or projection closure. It is not unique;
it is selected because it is the shortest explicit parent that retains the
4888 source while resolving the generic clock-wave problem.

## 3. Stress and background equivalence

Metric variation gives

\[
\boxed{
T^{(U\phi)}_{\mu\nu}
=\varrho u_\mu u_\nu
+\overline M_{\rm Pl}^2\sigma_\theta
\left[2u_{(\mu}\nabla_{\nu)}\phi-Yg_{\mu\nu}\right],
\qquad Y=u^\mu\nabla_\mu\phi.
}
\]

On homogeneous FLRW define the physical clock-plus-cross energy

\[
D=\varrho-overline M_{\rm Pl}^2\sigma_\theta\dot\phi.
\]

The pressure remains

\[
p_\sigma=-\overline M_{\rm Pl}^2\sigma_\theta\dot\phi.
\]

After the same SK damping-energy transfer used in 4888, `D` obeys the 4888
`x_X` equation. Therefore the previously validated Friedmann solutions are
not retuned or replaced.

The multiplier itself and the clock's effective subhorizon inertia are

\[
\frac{\varrho}{3\overline M_{\rm Pl}^2H_0^2}
=x_X+\frac{\bar\sigma E\phi_N}{3},
\]

\[
\boxed{
B=\frac{\varrho-overline M_{\rm Pl}^2\sigma_\theta^2}{D}
=1+\frac{\bar\sigma E\phi_N-\bar\sigma^2}{3x_X}.
}
\]

| `Omega_phi,0` | minimum `varrho/rho_crit,0` | minimum `B` |
|---:|---:|---:|
| `1e-4` | `0.0488590` | `0.384878` |
| `1e-3` | `0.0478408` | `0.364097` |
| `1e-2` | `0.0406882` | `0.218126` |

Every ray keeps both quantities positive. The percent ray is closest to the
constraint boundary, but it retains a `21.8%` inertia margin.

## 4. Exact characteristic reduction

On a local inertial background write

\[
U=t+\pi.
\]

At fixed metric, linearizing the norm constraint gives

\[
\boxed{\partial_t\pi=0}.
\]

For Fourier variables `(delta phi, pi, delta D)`, the principal matrix can be
ordered as

\[
\begin{pmatrix}
\omega^2-k^2 & \sigma_\theta k^2 & 0\\
0 & \omega & 0\\
-Ck^2 & \varrho k^2 & \omega
\end{pmatrix}.
\]

Its determinant is

\[
\boxed{\omega^2(\omega^2-k^2)}.
\]

Thus:

- the memory mode has `c_phi^2=1`;
- the clock is a constrained dust/zero mode with `c_U^2=0`;
- there is no `c_+^2>1` clock--memory wave;
- tensor and Maxwell characteristics remain the public metric cone.

This is an executable symbolic determinant in the checkpoint script. It
closes the specific 4888 local derivative-cone obstruction. It does not
remove the separate dust caustic or zero-density strong-coupling questions.

## 5. Linear cosmological constraints and high-k growth

In Newtonian gauge,

\[
ds^2=-(1+2\Psi)dt^2+a^2(1-2\Phi)d\mathbf x^2,
\qquad U=t+\pi,
\]

the norm constraint gives

\[
\boxed{\dot\pi=\Psi}.
\]

The clock expansion perturbation is

\[
\delta\theta=-3(\dot\Phi+H\Psi)+\frac{k^2}{a^2}\pi.
\]

The exact fields to be carried into a Boltzmann implementation are

\[
\delta\Box\phi-V_{,\phi\phi}\delta\phi
+\sigma_\theta\delta\theta=0,
\]

\[
\delta[\nabla_\mu J_U^\mu]=\delta Q_{\rm SK},
\]

together with the Einstein constraints and the stress in section 3.

In the RSD subhorizon limit, the `delta Q_SK` and metric-time-derivative
terms are suppressed by `H^2a^2/k^2`. Eliminating the constrained memory
response gives the two-component kernel

\[
\delta_{o,NN}+(2+h)\delta_{o,N}=\frac32S,
\]

\[
\boxed{
\delta_{X,NN}+left(2+h-\frac{B_N}{B}\right)\delta_{X,N}
=\frac32BS,
}
\]

\[
S=\frac{x_o\delta_o+x_X\delta_X}{E^2}.
\]

Unlike the smooth-memory proxy in 4888, this parent predicts an appreciable
late growth effect. Across the sampled redshifts:

```text
maximum normalized D shift = 2.080%;
maximum f shift            = 11.081%;
```

At `z=0`, the growth-rate suppressions are `8.37%`, `8.69%`, and `11.08%`
for the three rays. This is a real discriminant, not a negligible correction.

## 6. Real SDSS/eBOSS growth score

The existing hash-locked BAO-plus vectors were used as the primary branch;
the full-shape-only vectors were used separately as robustness data. They
were not combined. For each fixed background, only `q=H0 r_d` and
`sigma8_today` were profiled, exactly the same two freedoms for MTS and
matched LambdaCDM.

| Data branch | Model | chi2 | profiled `sigma8_today` | Delta chi2 vs LambdaCDM |
|---|---|---:|---:|---:|
| BAO-plus primary | fixed LambdaCDM | `14.2751` | `0.87798` | `0` |
| BAO-plus primary | MTS `1e-4` | `13.5716` | `0.88230` | `-0.7035` |
| BAO-plus primary | MTS `1e-3` | `13.2952` | `0.88321` | `-0.9799` |
| BAO-plus primary | MTS `1e-2` | `13.5128` | `0.87953` | `-0.7623` |
| full-shape robustness | fixed LambdaCDM | `12.9728` | `0.85540` | `0` |
| full-shape robustness | MTS `1e-4` | `12.2354` | `0.85875` | `-0.7375` |
| full-shape robustness | MTS `1e-3` | `11.9324` | `0.85989` | `-1.0405` |
| full-shape robustness | MTS `1e-2` | `12.2757` | `0.85500` | `-0.6971` |

All fits converge without profile-edge flags. The `1e-3` row is the best of
the predeclared rays on both independent compressions. The improvement is
small and is not evidence: `sigma8` is freely profiled, no CMB amplitude is
enforced, the MTS coefficients remain benchmark data, and the full
radiation/neutrino perturbation system has not been run.

The useful conclusion is narrower and stronger: the constrained parent does
not collapse when its newly derived growth effect is confronted with real
RSD covariance.

## 7. Local GR, Newton and Maxwell reduction

On the stationary background-subtracted local branch,

\[
\theta=0,
\qquad
\phi=\text{constant},
\qquad
Y=0,
\qquad
\delta D=0.
\]

Therefore

\[
\delta T^{(U\phi)}_{\mu\nu}=0.
\]

The selected metric-only EH branch gives

\[
G_{\mu\nu}+\Lambda g_{\mu\nu}
=\overline M_{\rm Pl}^{-2}
(T^{\rm matter}_{\mu\nu}+T^{\rm EM}_{\mu\nu})
+O(H_0^2L^2).
\]

The static weak limit is

\[
\boxed{
\nabla^2U_N=4\pi G_N\rho_{\rm total}+O(H_0^2U_N),
\qquad
G_N=(8\pi\overline M_{\rm Pl}^2)^{-1}.
}
\]

The stationary values remain

\[
\gamma_{\rm PPN}=\beta_{\rm PPN}=1.
\]

Maxwell is minimally coupled to the same public metric,

\[
S_{\rm EM}=-\frac14\int\sqrt{-g}\,F_{\mu\nu}F^{\mu\nu}
+\int\sqrt{-g}\,A_\mu J^\mu,
\]

\[
\boxed{
T^{\rm EM}_{\mu\nu}=F_{\mu\alpha}F_\nu{}^\alpha
-\frac14g_{\mu\nu}F_{\alpha\beta}F^{\alpha\beta}.
}
\]

The Poynting vector is the local observer readout

\[
S^i=-T^i{}_0.
\]

There is no direct Maxwell charge under `phi` or `U`; electromagnetic energy
and momentum gravitate through the ordinary Hilbert stress. Cosmic clock
background corrections are `1.188e-30` at one AU and `2.569e-35` at one
solar radius.

This is a conditional local correspondence theorem for the selected parent,
not yet a derivation of the bath clock from primitive MTS microphysics.

## 8. Dynamical orbital and binary leakage

Ordinary matter and EM have no direct memory charge. A finite-frequency
metric correction from the expansion source requires one `sigma_theta`
insertion to source `phi` and a second insertion when its stress returns to
the metric. Away from the constrained zero mode,

\[
\epsilon_{\rm memory}\lesssim
\left(\frac{\sigma_\theta}{\omega}\right)^2.
\]

The cosmological clock density supplies the separate conservative envelope

\[
\epsilon_{\rm clock}\lesssim
3\Omega_X\left(\frac{H_0}{\omega}\right)^2.
\]

| System | combined metric-amplitude envelope |
|---|---:|
| Earth orbit | `2.853e-23` |
| Mercury orbit | `1.655e-24` |
| Hulse--Taylor period | `2.230e-29` |
| Double Pulsar period | `2.235e-30` |
| `100 Hz` wave | `2.864e-42` |

The stationary `omega=0` case is not obtained by taking this expression to
zero frequency; it is governed by the separate exact theorem `theta=0`.
The envelopes do not replace a waveform calculation, but they show that the
new parent does not introduce an unsuppressed finite-frequency local mode.

## 9. Arbitration

| Gate | Result |
|---|---|
| Explicit fixed-norm parent action | Constructed |
| Same FLRW source as 4888 | Exact |
| Generic finite-sound clock selected | No; demoted |
| Clock multiplier positive | Pass on all rays |
| Effective constrained inertia positive | Pass; minimum `0.218` |
| Coupled finite-frequency cone | `c_phi=1`, `c_U=0`; no upper superluminal root |
| Subhorizon growth equations | Derived |
| Real primary/robustness RSD score | All MTS rays modestly improve matched LambdaCDM chi2 |
| Stationary Newton/PPN reduction | GR values plus `H0^2L^2` background |
| Maxwell/Poynting stress | Standard public-metric Hilbert stress |
| Finite-frequency local leakage | Below `2.86e-23` on sampled systems |
| Clock microscopic identity | Open |
| Zero-density/caustic completion | Open |
| Full CMB/radiation/SK perturbations | Open |

The constrained clock is selected as the current active-memory parent. This
is a genuine forward derivation: it removes the 4888 extra-cone obstruction,
changes the growth prediction, survives two real growth-data compressions,
and provides a direct local Newton/Maxwell reduction.

## 10. Next target

`4890-Y5-R2FR-constrained-clock-full-linear-Einstein-Boltzmann-kernel-and-bath-identity-or-expansion-source-demotion-gate.md`

The next gate must:

1. derive the complete Newtonian-gauge Einstein, clock, memory, ordinary
   matter and radiation equations including `delta Q_SK` and noise;
2. identify whether `U,varrho` are a composite of existing matter/bath fields
   or an additional dust component;
3. test the zero-density local patch for strong coupling and caustics;
4. impose CMB amplitude/distance information instead of profiling
   `sigma8_today` freely;
5. retain the same local Newton, Maxwell and binary limits without retuning.

## Sources

- `post-checkpoint-work/4850-Y5-R2FR-H-load-scalar-kinetic-mode-or-parent-tau-regularization-before-CMB-growth.md`.
- `post-checkpoint-work/4851-Y5-R2FR-H-load-cuscuton-matter-perturbation-constraint-and-growth-kernel.md`.
- `post-checkpoint-work/4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md`.
- `post-checkpoint-work/4888-Y5-R2FR-bath-compression-memory-Kubo-coefficient-and-backreacted-FLRW-growth-likelihood-or-expansion-source-demotion-gate.md`.
- `formalization-workbench/data/cosmology/growth_CMB/sdss_eboss_dr16/`.

