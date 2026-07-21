# 4887 - Expansion-driven memory with stationary local silence

Marker: `MTS_EXPANSION_DRIVEN_MEMORY_SOURCE_4887`

Status: private constructive checkpoint; mechanism demonstrated, coefficients
not yet parent-matched or data-fit.

**4888 correction:** the statement below that the scalar principal symbol is
unchanged applies to the bare `phi` block. Once the bath clock is dynamical,
its spatial-gradient mixing changes the coupled two-field characteristic
determinant. Checkpoint 4888 derives the stable roots and leaves the full
nonlocal front-velocity test open.

## 1. Decision

Checkpoint 4887 finds a viable structural replacement for the direct
`bTM^2` cosmology rejected in 4886.

The selected interaction is

\[
S_\theta=-\overline M_{\rm Pl}^2\sigma_\theta
\int d^4x\sqrt{-g}\,u^\mu\nabla_\mu\phi,
\qquad
\phi=M/\overline M_{\rm Pl},
\]

where `u` is the timelike Landau flow of the already-required closed bath.
It has four decisive properties.

1. It is diffeomorphism invariant and first derivative.
2. It becomes a boundary term for a stationary divergence-free flow.
3. For a normalized Killing flow, `theta=nabla_mu u^mu=0` exactly, so it
   creates no stationary scalar charge or PPN residual.
4. On FLRW, `theta=3H`, so the identical term becomes a genuine late-time
   bulk source without a redshift switch or direct matter coupling.

A covariant bath-clock completion gives a positive-gradient condition that
the benchmark passes. Three numerical response branches reach present memory
fractions `10^-4`, `10^-3` and `10^-2`, remain below `1.406%` throughout the
fixed-background smoke, and activate late from zero initial memory.

This promotes the expansion source to a **constructed conditional mechanism**.
It does not yet promote it to the parent theory because `sigma_theta` remains
a bath compression-memory response coefficient requiring microscopic Kubo
matching, and the cosmology still needs backreaction and likelihood tests.

## 2. Candidate audit

The source hunt compared five covariant routes.

| Candidate | Local stationary behavior | FLRW behavior | Decision |
|---|---|---|---|
| `beta phi^2 T` | nonzero in matter | nonzero | rejected by 4886 PPN--cosmology identity |
| `phi R` | matter monopole | nonzero | reject local silence |
| `phi Box R` | total divergence at linear order | nonzero for evolving `R` | higher-derivative and field-redefinition redundant as lead route |
| `phi G_GB` | source remains in Ricci-flat curvature | nonzero | reject exact local-vacuum silence |
| `u.grad phi` | boundary for stationary Landau flow | source proportional to `3H` | selected |

The selected operator is the lowest-derivative candidate and uses state data
already present in the 4873 covariant open parent. It does not introduce a
preferred coordinate `t`.

## 3. Closed effective action and open completion

The reversible effective action is

\[
S_{\phi X}=\int d^4x\sqrt{-g}\,\overline M_{\rm Pl}^2
\left[-\frac12(\nabla\phi)^2
-\frac\kappa4\phi^4
-\sigma_\theta u^\mu\nabla_\mu\phi\right]
+S_X,
\]

where `kappa=a Mbar_Pl^2` and the bath stress defines

\[
\overline T^\mu{}_{\nu,X}u^\nu=-\rho_Xu^\mu,
\qquad
u^2=-1.
\]

Integration by parts gives

\[
-\int\sqrt{-g}\,\sigma_\theta u^\mu\nabla_\mu\phi
=\int\sqrt{-g}\,\sigma_\theta\phi\nabla_\mu u^\mu
-\text{boundary}.
\]

Writing `theta=nabla.u`, variation gives

\[
\Box\phi-\kappa\phi^3+\sigma_\theta\theta=0.
\]

The 4873 Schwinger--Keldysh completion adds the already-derived Ohmic damping
and noise:

\[
\Box\phi-\kappa\phi^3
-\gamma_Mu^\mu\nabla_\mu\phi
+\sigma_\theta\theta=\zeta.
\]

On FLRW this is

\[
\ddot\phi+(3H+\gamma_M)\dot\phi+\kappa\phi^3
=3\sigma_\theta H+\zeta.
\]

No term modifies the second-derivative principal symbol. Scalar disturbances
therefore retain the public-metric characteristic cone.

For a homogeneous field, the canonical momentum is

\[
\Pi_\phi=a^3\overline M_{\rm Pl}^2
(\dot\phi-\sigma_\theta).
\]

The term linear in `dot phi` cancels from the homogeneous Hamiltonian:

\[
\rho_\phi=\overline M_{\rm Pl}^2
\left(\frac12\dot\phi^2+\frac\kappa4\phi^4\right).
\]

Thus the source does not create a wrong-sign scalar kinetic term.

## 4. Covariant bath clock and gradient stability

An explicit covariant flow owner can be written with a bath clock `Theta`:

\[
X=-\frac12(\nabla\Theta)^2,
\qquad
u_\mu=-\frac{\nabla_\mu\Theta}{\sqrt{2X}},
\qquad
S_X=\int\sqrt{-g}\,P(X).
\]

The ordinary clock requirements are

\[
P_X+2XP_{XX}>0,
\qquad
P_X>0.
\]

Around a homogeneous clock background `Theta=q t+pi`, the expansion coupling
produces spatial-gradient mixing between `pi` and the memory fluctuation
`chi`. Positivity of the two-field gradient matrix gives

\[
\boxed{
\sigma_\theta^2<\frac{\rho_X+p_X}{\overline M_{\rm Pl}^2}
}.
\]

For `sigma_theta/H0=0.3`, this requires

\[
\Omega_X(1+w_X)>0.03.
\]

The observed baryon-enthalpy benchmark `Omega_b=0.049`, `w=0` has mixing
ratio

\[
\frac{\sigma_\theta^2}
{3\Omega_b(1+w)H_0^2}=0.61224<1,
\]

leaving a positive determinant margin `0.38776`. A one-percent bath would
fail. The mechanism therefore needs a genuine bath state with sufficient
enthalpy, but not a hidden dominant component.

This is a stability benchmark, not an assertion that visible baryons are the
microscopic `X_Omega` bath.

## 5. Exact stationary silence

Let `K` be a stationary timelike Killing field and

\[
u^\mu=\frac{K^\mu}{\sqrt{-K^2}}.
\]

Killing's equation gives

\[
\nabla_\mu K^\mu=0,
\qquad
K^\mu\nabla_\mu K^2=0.
\]

Therefore

\[
\boxed{\nabla_\mu u^\mu=0}.
\]

For the constant local solution `phi=0`, both the interaction and its stress
vanish. Hence, on the stationary branch,

\[
\alpha_{\rm matter}=0,
\qquad
\gamma_{\rm PPN}=1,
\qquad
\beta_{\rm PPN}=1.
\]

This covers Minkowski space, a static spherical star and its Ricci-flat
exterior when the bath state is Killing-aligned. It does not yet cover a
time-dependent binary.

The residual effect of the slowly evolving cosmic state at a local scale `L`
is derivative suppressed by `(H0 L/c)^2`. The benchmark values are

\[
\epsilon_{\rm AU}=1.1880\times10^{-30},
\qquad
\epsilon_{R_\odot}=2.5693\times10^{-35}.
\]

Unlike the direct trace branch, this mechanism has no long-range static
matter scalar charge to compare with Cassini.

## 6. FLRW response calculation

With `N=ln a`, `E=H/H0`,

\[
\phi_{,NN}
+\left(3+\frac{d\ln H}{dN}+\frac{\bar\gamma}{E}\right)\phi_{,N}
+\frac{\bar\kappa}{E^2}\phi^3
=\frac{3\bar\sigma}{E},
\]

where

\[
\bar\sigma=\sigma_\theta/H_0,
\qquad
\bar\gamma=\gamma_M/H_0,
\qquad
\bar\kappa=\kappa/H_0^2.
\]

The smoke uses

```text
sigma_theta/H0 = 0.3;
gamma_M/H0 = 1;
phi(N=-7) = phi_N(N=-7) = 0.
```

For each requested present memory fraction, the high-`kappa` controlled ray
is selected once. No local parameter is retuned.

| `Omega_M,0` target | `kappa/H0^2` | `phi_0` | `phi_N,0` | `Omega_V,0` | `Omega_K,0` | maximum `Omega_M` | half-activation `z` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| `1e-4` | `3.35579e8` | `0.0013740` | `-0.0014097` | `9.9669e-5` | `3.3120e-7` | `1.1314e-4` | 4.60 |
| `1e-3` | `4.71381e5` | `0.0125600` | `-0.0115966` | `9.7759e-4` | `2.2413e-5` | `1.1482e-3` | 4.05 |
| `1e-2` | `9.79643e2` | `0.1020380` | `-0.0830728` | `8.8498e-3` | `1.1502e-3` | `1.40596e-2` | 0.99 |

All integrations are finite. The largest memory fraction is `0.01406`, so
the fixed-LambdaCDM response approximation remains a controlled existence
smoke at the percent level.

The activation is automatic: `3 sigma_bar/E` is tiny at early large `E` and
grows toward the present. There is no inserted redshift threshold.

The displayed `w_phi` values are scalar-energy proxies only. The next
backreacted calculation must include bath work, noise and the full combined
stress before interpreting an effective equation of state.

## 7. Coefficient ownership

The mechanism uses three coefficients with distinct owners:

| Coefficient | Role | Current ownership |
|---|---|---|
| `gamma_M` | Ohmic damping | existing 4873/4885 bath response |
| `kappa=a Mbar_Pl^2` | quartic restoring force | existing canonical memory action |
| `sigma_theta` | bath-compression to memory-force response | new matching coefficient of the same bath |

`sigma_theta` must be extracted from the zero-momentum compression-memory
response of the closed `X_Omega` influence functional. The benchmark
`sigma_theta/H0=0.3` proves existence and stability; it is not a microscopic
prediction.

The theory rule is one matching at the parent/bath state. Local, galaxy and
cosmological arenas may not receive separate values.

## 8. Arbitration

| Gate | Result |
|---|---|
| Variationally closed covariant source | Constructed |
| Preferred coordinate inserted | No |
| State rest frame | Spontaneous bath Landau frame |
| Scalar principal cone changed | No |
| Stationary local PPN source | Exactly zero |
| Clock-gradient stability | Passes selected benchmark |
| FLRW source | `3 sigma_theta H` |
| Percent-level regular existence branch | Passes fixed-background smoke |
| Microscopic `sigma_theta` prediction | Open |
| Backreacted cosmology/data preference | Open |

The direct trace branch remains rejected. The expansion-driven branch is
retained conditionally rather than demoted.

## 9. Next target

`4888-Y5-R2FR-bath-compression-memory-Kubo-coefficient-and-backreacted-FLRW-growth-likelihood-or-expansion-source-demotion-gate.md`

The next gate must:

1. derive `sigma_theta` from an explicit closed bath spectral response or
   demote it to a Wilson coefficient;
2. evolve the bath, memory and Friedmann equations with total stress
   conservation;
3. derive linear scalar perturbations and the growth response;
4. compare the same parameter rows with the existing Pantheon+/BAO/CMB/growth
   machinery;
5. test time-dependent binary and preferred-frame leakage before any local-GR
   promotion beyond stationary systems.

## Sources

- Covariant open bath and Landau vector: `post-checkpoint-work/4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md`.
- Composite-flow construction: `post-checkpoint-work/4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md`.
- Direct-trace rejection: `post-checkpoint-work/4886-Y5-R2FR-canonical-memory-scalar-local-screening-scalarization-and-same-parent-cosmology-compatibility-gate.md`.
- [Crossley, Glorioso and Liu, dissipative EFT](https://arxiv.org/abs/1511.03646).
