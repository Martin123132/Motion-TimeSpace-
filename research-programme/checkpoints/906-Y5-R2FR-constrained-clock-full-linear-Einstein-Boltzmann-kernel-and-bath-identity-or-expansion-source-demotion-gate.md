# 4890 - Composite bath clock, finite-k Einstein-fluid kernel and FDT gate

Marker: `MTS_COMPOSITE_CLOCK_FINITE_K_FDT_GATE_4890`

## 0. Decision

The expansion-source route is **not demoted**. This checkpoint makes two
substantive advances rather than recording another missing-input list:

1. it derives the fixed-norm variables `U,varrho` as the controlled WKB
   variables of two degenerate Cartesian modes already available in the
   closed bath;
2. it derives and integrates the finite-k Einstein--memory--clock--matter--
   radiation system, including the deterministic Schwinger--Keldysh energy
   transfer and the retarded response to a stochastic impulse.

The result is not yet a full Einstein--Boltzmann or CMB prediction. Photons
and neutrinos are represented here only by a perfect radiation fluid, and
the bath state that normalizes the FDT noise power is not selected. The
correct decision is therefore

```text
retain the parent and finite-k route;
do not claim or run a CMB likelihood yet.
```

The 4889 stationary local-GR/Newton/Maxwell correspondence is unchanged.

## 1. Clock identity from existing bath fields

Take two degenerate real bath modes and write

\[
 Z=X_1+iX_2=Ae^{i m_c U},
 \qquad
 X_1=A\cos(m_cU),\quad X_2=A\sin(m_cU).
\]

The clock one-form is the exact Cartesian composite

\[
 \boxed{
 \nabla_\mu U=
 \frac{X_1\nabla_\mu X_2-X_2\nabla_\mu X_1}
 {m_c(X_1^2+X_2^2)} .}
\]

Direct symbolic substitution gives

\[
 (\nabla X_1)^2+(\nabla X_2)^2
 =(\nabla A)^2+m_c^2A^2(\nabla U)^2,
\]

\[
 X_1\nabla_\mu X_2-X_2\nabla_\mu X_1
 =m_cA^2\nabla_\mu U.
\]

Hence the canonical pair action becomes exactly

\[
 \mathcal L_{\rm pair}
 =-\frac12(\nabla A)^2
 -\frac12m_c^2A^2[(\nabla U)^2+1].
\]

With

\[
 \boxed{\varrho=m_c^2A^2},
\]

and at leading WKB order, this is the 4889 constrained-clock action. The
already-selected expansion operator has the Cartesian representation

\[
 \mathcal L_{\rm mix}=
 \frac{\overline M_{\rm Pl}^2\sigma_\theta}{m_c}
 \nabla_\mu\phi\,
 \frac{X_1\nabla^\mu X_2-X_2\nabla^\mu X_1}{X_1^2+X_2^2}.
\]

Its coefficient remains the 4888 cross-susceptibility Kubo coefficient; no
new arena fit or primitive field has been introduced.

Varying the amplitude before taking the limit gives the correction to the
unit constraint,

\[
 \boxed{(\nabla U)^2+1=\frac{\Box A}{m_c^2A}},
\]

while the phase equation gives

\[
 \nabla_\mu(A^2\nabla^\mu U)=0
\]

before the mixing and open-bath transfer are included. Thus the fixed-norm
clock is a controlled infrared chart, not an unexplained extra dust field.

### 1.1 Controlled domain

The reduction requires

\[
 \epsilon_A=\frac{|\nabla A|}{m_cA}\ll1,
 \quad
 \epsilon_R=\frac{\sqrt{|R|}}{m_c}\ll1,
 \quad
 \epsilon_k=\frac{k_{\rm phys}}{m_c}\ll1.
\]

Using `c_s^2=k_phys^2/(4m_c^2)<=10^-6` gives the indicative lower floors

| arena | minimum `m_c` |
|---|---:|
| `k=0.2 h/Mpc`, `z=2` | `1.2931e-27 eV` |
| `k=0.1 h/Mpc`, `z=1095` | `2.3620e-25 eV` |
| `k=0.2 h/Mpc`, `z=1095` | `4.7240e-25 eV` |

Demanding `hbar omega/m_c<=10^-2` gives `m_c>=1.4360e-17 eV` for an
eight-hour binary and `m_c>=1.3105e-20 eV` for an annual forcing period.
These are controlled lower bounds, not a predicted carrier mass.

The polar map is undefined at `A=0`. There the Cartesian `X_1,X_2` fields
remain regular, but the dust chart and its caustic description cannot be
used. This is a real remaining nonlinear gate.

To avoid double counting, the bath spectral density is split as

```text
J_bath = J_coherent_pair + J_continuum.
```

The reserved coherent pair supplies `U,varrho`; it is excluded from the
Ohmic continuum that supplies `gamma_M` and noise.

## 2. Early background required by finite-k modes

The 4888 backgrounds began at `N=-7`. A `0.03 h/Mpc` mode is already inside
the horizon there, so assigning it a superhorizon adiabatic state creates a
false transient. The same parent background equations were therefore shot
again from `N=-14`, imposing the same present memory and clock densities.

| `Omega_memory,0` | `kappa/H0^2` | clock scale | max `|Delta E/E|` on `-7<=N<=0` |
|---:|---:|---:|---:|
| `1e-4` | `3.35497885e8` | `0.999983500` | `6.43e-8` |
| `1e-3` | `4.71747598e5` | `0.999294968` | `2.17e-7` |
| `1e-2` | `9.85242320e2` | `0.981850528` | `4.88e-7` |

All shooting residuals are below `3.36e-12`, `E(0)=1`, and
`x_X(0)=0.049`. This repairs the initial-value problem without changing the
late parent or retuning an observational row.

## 3. Full deterministic finite-k system at perfect-fluid level

Use Newtonian gauge

\[
 ds^2=-(1+2\Psi)dt^2+a^2(1-2\Phi)d\mathbf x^2,
\]

and, at this stage only, the perfect-fluid anisotropic-stress closure
`Psi=Phi`. Write `U=t+pi_U`, `P_U=H0 pi_U`, `E=H/H0`,
`K^2=(kc/aH0)^2`, and primes below as `d/dN`.

The exact linear clock constraint and expansion perturbation are

\[
 P_U'=\frac{\Phi}{E},
 \qquad
 \boxed{\frac{\delta\theta}{H_0}
 =-3E(\Phi'+\Phi)+K^2P_U}.
\]

For `q=delta phi`, the deterministic part of the Langevin equation is

\[
 q''+\left(h+3+\frac{\bar\gamma}{E}\right)q'
 +\frac{K^2+3\bar\kappa\phi^2}{E^2}q
 =2\Phi[\phi''+(h+3)\phi']+4\phi'\Phi'
 +\frac{\bar\sigma}{E^2}\frac{\delta\theta}{H_0}
 +\frac{\bar\gamma}{E}\phi'\Phi+\frac{\bar\xi}{E^2}.
\]

Define `delta x_X=delta D/(3 Mbar_Pl^2 H0^2)` and

\[
 \lambda_X=x_X+\frac{\bar\sigma E\phi'}{3}.
\]

The clock energy equation, including the required `delta Q_SK`, is

\[
 \begin{split}
 \delta x_X'+3\delta x_X-3x_X\Phi'
 &+\frac{K^2}{3E}(3\lambda_XP_U-\bar\sigma q)\\
 &=\frac{\bar\gamma E}{3}(2\phi'q'-\phi'^2\Phi)
 -\frac{\phi'\bar\xi}{3}.
 \end{split}
\]

The noise impulse therefore changes `q'` by `I/E^2` and `delta x_X` by
`-phi'I/3`; their instantaneous total-density changes cancel exactly.

The scalar density perturbation is

\[
 \delta x_\phi=
 \frac{E^2\phi'q'-E^2\phi'^2\Phi+\bar\kappa\phi^3q}{3}.
\]

The Einstein constraints are

\[
 K^2\Phi+3E^2(\Phi'+\Phi)=-\frac32\delta x_{\rm total},
\]

\[
 E(\Phi'+\Phi)=\frac12[3x_oP_o+4x_rP_r+3x_XP_U
 +(E\phi'-\bar\sigma)q].
\]

Pressureless matter obeys

\[
 \delta_o'=3\Phi'-\frac{K^2}{E}P_o,
 \qquad P_o'=\frac{\Phi}{E}.
\]

Perfect radiation obeys

\[
 \delta_r'=4\Phi'-\frac{4K^2}{3E}P_r,
 \qquad
 \boxed{P_r'=P_r+\frac{\Phi+\delta_r/4}{E}}.
\]

The `+P_r` term follows from the conversion between the conformal velocity
divergence and the cosmic-time potential. Omitting it produces a spurious
momentum-constraint drift; the implemented equations retain it.

## 4. Nine-mode constraint test

The three fixed memory branches were each integrated at
`k={0.001,0.01,0.03} h/Mpc` from `N=-14` to zero. The largest initial
`k/(aH)` is `0.007872`, so every tested mode starts outside the horizon.

Across all nine integrations:

```text
all state arrays finite                         yes
maximum relative Hamiltonian residual          2.215e-16
maximum relative momentum residual             1.721e-3
maximum linearity residual                      0
```

For the central `Omega_memory,0=10^-3` branch, the final ordinary/clock
density contrasts are

| `k [h/Mpc]` | `Phi(0)` | `delta_o(0)` | `delta_X(0)` |
|---:|---:|---:|---:|
| `0.001` | `7.031e-6` | `-1.574e-4` | `-1.564e-4` |
| `0.01` | `5.658e-6` | `-1.095e-2` | `-9.882e-3` |
| `0.03` | `3.549e-6` | `-6.185e-2` | `-5.494e-2` |

This is a deterministic finite-k consistency pass, not a CMB transfer code.

## 5. FDT and retarded noise response

Use the Langevin convention

\[
 \ddot\phi+(3H+\gamma_M)\dot\phi-a^{-2}\nabla^2\phi
 +V'-\sigma_\theta\theta=\xi.
\]

The exchanged energy is

\[
 Q_{\rm SK}=\overline M_{\rm Pl}^2(\gamma_MY-\xi)Y.
\]

The 4873 Schwinger--Keldysh/KMS relation gives

\[
 \mathcal N(\omega,k)=
 [-\operatorname{Im}\Sigma_R(\omega,k)]
 \coth\frac{\omega}{2T_{\rm bath}},
\]

and, in its classical Ohmic convention,

\[
 \boxed{\mathcal N=2\gamma_MT_{\rm bath}}.
\]

The code computes the causal metric response to a normalized impulse
`integral dN xi/H0^2=1` at `k=0.01 h/Mpc` on the central branch:

| injection `N` | final `Phi` response | maximum `|Phi|` response |
|---:|---:|---:|
| `-10` | `-4.94e-20` | `1.19e-19` |
| `-7` | `3.13e-16` | `8.15e-15` |
| `-4` | `-1.32e-10` | `3.19e-10` |
| `-1` | `-1.01e-5` | `1.64e-5` |

The impulse Hamiltonian residual is below `2.19e-16`; the global normalized
momentum residual is below `1.56e-3`. Thus the noise transfer function is
computable and constraint compatible.

The numerical noise power is not yet predictive because `T_bath`, or the
equivalent nonthermal bath density matrix, has no parent-selected value.
The actual metric covariance has the form

\[
 P_\Phi^{\rm noise}(k,N)=\int dN'\,
 |G_{\Phi\xi}(k;N,N')|^2\overline{\mathcal N}(k,N'),
\]

with the state measure fixed by that density matrix.

## 6. CMB gate

Closed here:

- the composite clock identity in its nonzero-amplitude WKB domain;
- the early background required for superhorizon initialization;
- deterministic finite-k Einstein constraints and conservation;
- `delta Q_SK` and the retarded noise response;
- the FDT shape relation.

Still required before a CMB likelihood:

- a parent value for the coherent carrier mass/fraction;
- a bath temperature or nonthermal covariance;
- photon--baryon collisions, recombination and opacity;
- massless/massive neutrino multipoles and anisotropic stress;
- a primordial memory--clock cross-covariance.

Therefore `CMB_likelihood_allowed=false`. This is a gate result, not a
failure of the expansion source and not permission to profile away the CMB
amplitude.

## 7. Status

| item | status |
|---|---|
| `U,varrho` identity | Derived as controlled composite bath variables |
| New primitive field | No |
| Exact global dust chart | No; fails at `A=0` |
| Early background | Reshot and overlap checked |
| Finite-k Einstein-fluid system | Derived and numerically constraint-tested |
| SK mean transfer | Derived |
| Noise response | Computed per unit impulse |
| Noise amplitude | Open parent-state input |
| Full Einstein--Boltzmann hierarchy | Open |
| CMB claim | Blocked |
| 4889 local GR/Newton/Maxwell limit | Retained |

## 8. Next target

`4891-Y5-R2FR-composite-clock-neutrino-photon-baryon-hierarchy-and-FDT-state-normalization-or-CMB-source-demotion-gate.md`

The next checkpoint must wire the standard photon--baryon and neutrino
hierarchies to this unchanged parent, derive or bound the bath-state
normalization, and only then decide whether a CMB transfer calculation is
allowed. The zero-amplitude Cartesian patch remains a separate nonlinear
local target.

## Sources

- `post-checkpoint-work/4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md`.
- `post-checkpoint-work/4888-Y5-R2FR-bath-compression-memory-Kubo-coefficient-and-backreacted-FLRW-growth-likelihood-or-expansion-source-demotion-gate.md`.
- `post-checkpoint-work/4889-Y5-R2FR-nonlocal-bath-retarded-kernel-causal-front-growth-and-binary-leakage-or-expansion-source-demotion-gate.md`.
- `post-checkpoint-work/scripts/Y5_R2FR_4890_wkb_bath_identity_finite_k_kernel.py`.
