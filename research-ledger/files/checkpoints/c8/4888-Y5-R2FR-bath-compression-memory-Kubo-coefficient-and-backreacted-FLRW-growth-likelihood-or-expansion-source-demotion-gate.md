# 4888 - Bath Kubo matching, conserved backreaction and real-data smoke

Marker: `MTS_BATH_KUBO_BACKREACTED_COSMOLOGY_4888`

Status: private constructive and corrective checkpoint; no cosmology,
local-GR, causal-completion or parameter-free prediction claim.

**4889 resolution:** the generic `P(X)` clock remains demoted as the selected
local parent. An explicit fixed-norm irrotational clock keeps the same source
and background while replacing the finite-sound clock wave by a constrained
dust mode. Its characteristic polynomial, growth response and local limits
are derived in checkpoint 4889.

## 1. Decision

This checkpoint does the work left open by 4887 rather than recording
`sigma_theta` as another unspecified coefficient.

1. An explicit closed oscillator bath coupled to both memory and bath
   compression produces the 4887 operator. The exact matching equation is

   \[
   \boxed{
   \overline M_{\rm Pl}^2\sigma_\theta
   =K^R_{\phi\theta}(0,0)
   =\sum_a\frac{c_a d_a}{\Omega_a^2}.
   }
   \]

2. The same integration necessarily produces `phi^2` and `theta^2`
   susceptibilities. They cannot be omitted while retaining only the cross
   term. Their Gram matrix obeys a Cauchy--Schwarz bound.
3. `gamma_M` and `sigma_theta` are different spectral data. The former is
   the low-frequency imaginary slope of the memory auto-kernel; the latter
   is the zero-frequency dispersive memory--compression cross-kernel.
   Therefore the parent formula is derived, but the numerical benchmark is
   not predicted from `gamma_M` alone.
4. Varying the covariant clock action gives the complete interaction stress
   and clock current. On FLRW the interaction has zero density but nonzero
   pressure. Adding bath heating from the Ohmic term closes total stress
   conservation exactly.
5. All three predeclared memory branches pass a self-consistent Friedmann,
   Raychaudhuri and bath-energy evolution. The percent branch requires an
   `1.815%` reduction of the primordial dust normalization to compensate the
   energy later deposited into the bath.
6. A real Pantheon+/DESI DR2 fixed-row smoke was run. The percent branch
   modestly improves chi-square relative to matched and fitted LambdaCDM,
   but does not beat fitted `wCDM/CPL` in chi-square and is not evidence once
   unresolved coefficient ownership is counted.
7. A correction is required: 4887's unchanged-principal-cone statement is
   true only for the bare `phi` block. A dynamical clock and memory have a
   mixed characteristic determinant. The benchmark is gradient-stable, but
   its upper low-energy mode exceeds the public metric cone for every
   positive bath sound speed tested.

The expansion route is **not demoted**: it survives backreaction, controlled
growth and a real background-data smoke. It is also **not promoted**: the
full nonlocal bath kernel must establish the causal front and the same model
must pass dynamical-binary and full perturbation tests.

## 2. Explicit closed bath and exact cross Kubo coefficient

Introduce healthy bath modes `chi_a` with the covariant action

\[
S_\chi=\sum_a\int d^4x\sqrt{-g}\left[
-\frac12(\nabla\chi_a)^2-\frac12\Omega_a^2\chi_a^2
+\chi_a(c_a\phi+d_a\theta)
\right].
\]

The compression coupling is first derivative in an equivalent form,

\[
\int\sqrt{-g}\,d_a\chi_a\nabla_\mu u^\mu
=-\int\sqrt{-g}\,d_a u^\mu\nabla_\mu\chi_a
+\text{boundary}.
\]

For `A,B in {phi,theta}`, the retarded kernel is

\[
K^R_{AB}(\omega,k)=
\sum_a\frac{\lambda_{Aa}\lambda_{Ba}}
{\Omega_a^2+k^2-(\omega+i0)^2}.
\]

Integrating out the modes gives

\[
\Delta\mathcal L_{\rm IR}
=\frac12C_{\phi\phi}\phi^2
+C_{\phi\theta}\phi\theta
+\frac12C_{\theta\theta}\theta^2+cdots,
\]

\[
C_{\phi\phi}=\sum_a\frac{c_a^2}{\Omega_a^2},
\quad
C_{\phi\theta}=\sum_a\frac{c_a d_a}{\Omega_a^2},
\quad
C_{\theta\theta}=\sum_a\frac{d_a^2}{\Omega_a^2}.
\]

Consequently

\[
\boxed{C_{\phi\theta}^2\le
C_{\phi\phi}C_{\theta\theta}}.
\]

The cross sign is not fixed by passivity because `c_a d_a` can have either
sign. Passivity fixes the positivity of the full spectral Gram matrix.

With the parent subtraction rule fixed, the dispersive form is

\[
\overline M_{\rm Pl}^2\sigma_\theta
=\frac2\pi\int_0^\infty
\frac{d\omega}{\omega}
\operatorname{Im}K^R_{\phi\theta}(\omega,0),
\]

whereas

\[
\gamma_M=lim_{\omega\to0^+}
\frac{\operatorname{Im}K^R_{\phi\phi}(\omega,0)}
{\overline M_{\rm Pl}^2\omega}.
\]

This proves both the matching formula and the underdetermination theorem:
`gamma_M` does not determine `sigma_theta` without the cross spectral
density.

For the benchmark bath enthalpy,

\[
R_{\rm mix}=\frac{\overline M_{\rm Pl}^2\sigma_\theta^2}
{\rho_X+p_X}
=\frac{0.3^2}{3(0.049)}=0.6122449.
\]

A normalized two-mode construction with coupling directions
`a=(1,0)` and `b=(sqrt(R_mix),sqrt(1-R_mix))` has correlation `0.782461`
and Gram eigenvalues `0.217539` and `1.782461`. Thus a healthy cross spectrum
of the required size exists. This is an existence construction, not a
parameter-free MTS spectrum.

## 3. Covariant stress and clock variation

Let

\[
X=-\frac12(\nabla\Theta)^2,
\qquad
u_\mu=-\frac{\nabla_\mu\Theta}{\sqrt{2X}},
\qquad
Y=u^\mu\nabla_\mu\phi.
\]

Metric variation of
`S_sigma=-Mbar_Pl^2 sigma_theta int sqrt(-g) Y` gives

\[
\boxed{
T^{(\sigma)}_{\mu\nu}
=\overline M_{\rm Pl}^2\sigma_\theta
\left[2u_{(\mu}\nabla_{\nu)}\phi
+Yu_\mu u_\nu-Yg_{\mu\nu}\right].
}
\]

Clock variation gives

\[
\boxed{
J_\Theta^\mu=P_X\sqrt{2X}\,u^\mu
+\frac{\overline M_{\rm Pl}^2\sigma_\theta}{\sqrt{2X}}
h^{\mu\nu}\nabla_\nu\phi,
\qquad \nabla_\mu J_\Theta^\mu=0.
}
\]

On homogeneous FLRW,

\[
\rho_\sigma=0,
\qquad
p_\sigma=-\overline M_{\rm Pl}^2\sigma_\theta\dot\phi.
\]

The scalar and bath balances are

\[
\dot\rho_\phi+3H(\rho_\phi+p_\phi)
=\overline M_{\rm Pl}^2
\left(3\sigma_\theta H\dot\phi-\gamma_M\dot\phi^2\right),
\]

\[
\dot\rho_X+3H(\rho_X+p_X)
=\overline M_{\rm Pl}^2\gamma_M\dot\phi^2.
\]

Including `p_sigma`, the source work and damping transfer cancel exactly in
the total continuity equation. This repairs the scalar-only energy proxy of
4887.

## 4. Coupled characteristic correction

For a clock sound speed `c_X`, the high-frequency quadratic determinant of
the local two-field truncation is

\[
\boxed{
(c_{\rm mode}^2-1)(c_{\rm mode}^2-c_X^2)
-R_{\rm mix}c_X^2=0.
}
\]

The roots are

\[
c_\pm^2=\frac{1+c_X^2\pm
\sqrt{(1-c_X^2)^2+4R_{\rm mix}c_X^2}}{2}.
\]

`R_mix<1` is exactly the positive-gradient condition. However, for nonzero
mixing and `c_X^2>0`,

\[
\boxed{c_+^2>\max(1,c_X^2)}.
\]

| `c_X^2` | `c_+^2` | `c_-^2` |
|---:|---:|---:|
| `1/3` | `1.228087` | `0.105246` |
| `0.1` | `1.063541` | `0.036459` |
| `0.001` | `1.000612` | `0.000388` |

There is no gradient instability at the benchmark, but the local derivative
truncation does not preserve a single public characteristic cone. This does
not by itself prove acausality: the UV front is determined by the full
retarded nonlocal kernel, not by a low-frequency truncation. It does prevent
a local-GR or causal-completion promotion until that kernel is tested.

The exact stationary result `theta=0` is unchanged. This correction affects
dynamical clock/memory perturbations, not the stationary PPN theorem.

## 5. Fully backreacted FLRW system

Write `x_X=rho_X/(3 Mbar_Pl^2 H0^2)`, `v=phi_N`, `E=H/H0`. The closed
background equations are

\[
E^2=\frac{x_r+x_o+x_X+x_\Lambda+
\bar\kappa\phi^4/12}{1-v^2/6},
\]

\[
\frac{H_N}{H}=-\frac{2x_r}{E^2}
-\frac{3[x_o+(1+w_X)x_X]}{2E^2}
-\frac{v^2}{2}+\frac{\bar\sigma v}{2E},
\]

\[
v_N+\left(3+\frac{H_N}{H}+\frac{\bar\gamma}{E}\right)v
+\frac{\bar\kappa}{E^2}\phi^3=\frac{3\bar\sigma}{E},
\]

\[
x_{X,N}=-3(1+w_X)x_X+\frac{\bar\gamma E v^2}{3}.
\]

The shooting conditions fix the requested present memory fraction,
`Omega_X,0=0.049`, and `E(0)=1` simultaneously.

| `Omega_phi,0` | `kappa/H0^2` | initial bath/dust ratio | max `Omega_phi` | half activation `z` |
|---:|---:|---:|---:|---:|
| `1e-4` | `3.35621846e8` | `0.999983433` | `1.130976e-4` | `4.606` |
| `1e-3` | `4.71872692e5` | `0.999294529` | `1.147714e-3` | `4.069` |
| `1e-2` | `9.85392051e2` | `0.981849096` | `1.397680e-2` | `0.996` |

The maximum Friedmann/Raychaudhuri derivative mismatch is `8.88e-16`; the
maximum relative total-continuity residual is `2.13e-16`. All branches keep
`E^2>0` and `v^2<6`. Backreaction therefore does not destroy the 4887
existence branches.

## 6. Controlled growth limit

In the pressure-supported-memory, dust-bath limit, there is no direct matter
fifth force and the clustering equation is

\[
D_{NN}+\left(2+\frac{H_N}{H}\right)D_N
-\frac32\Omega_{\rm cluster}(N)D=0.
\]

For the percent branch the largest normalized growth-factor shift on
`z=0,0.5,1,2` is `0.186%`; the largest growth-rate shift is `0.384%` at
`z=0.5`. The smaller branches are correspondingly negligible.

This is not the full clock--memory perturbation likelihood. It is the
controlled `c_X^2 -> 0` limit selected because the finite-`c_X` local cone
requires the nonlocal-kernel resolution above.

## 7. Real Pantheon+/DESI DR2 smoke

The existing local Pantheon+ covariance and DESI DR2 BAO covariance were
loaded directly. A single SN offset was profiled. BAO identifies the product
`q=H0 r_d`. Baselines were refitted with radiation retained and no prior-edge
hits.

| Branch | Model | chi2 | identifiable parameters |
|---|---|---:|---:|
| no-SH0ES | fitted LambdaCDM | `1470.0997` | 2 |
| no-SH0ES | fitted wCDM | `1464.6923` | 3 |
| no-SH0ES | fitted CPL | `1464.2807` | 4 |
| no-SH0ES | MTS `1e-2` fixed row | `1469.4730` | conditional 2; conservative 4 |
| SH0ES-column | fitted LambdaCDM | `1773.6853` | 2 |
| SH0ES-column | fitted wCDM | `1759.4967` | 3 |
| SH0ES-column | fitted CPL | `1755.6490` | 4 |
| SH0ES-column | MTS `1e-2` fixed row | `1770.4215` | conditional 2; conservative 4 |

Relative to the matched fixed-`Omega_m=0.315` LambdaCDM row, the percent
branch gives

```text
no-SH0ES: Delta chi2 = -2.3145;
SH0ES-column: Delta chi2 = -3.5923.
```

Relative to fitted LambdaCDM,

```text
no-SH0ES: Delta chi2 = -0.6267;
SH0ES-column: Delta chi2 = -3.2638.
```

Under the conditional count, where `sigma_bar=0.3` and `gamma_bar=1` are
predeclared rather than charged as fitted freedoms, the percent branch is
competitive with fitted LambdaCDM. Under the conservative count it has
`Delta AIC=+3.373`, `Delta BIC=+14.175` for no-SH0ES and
`Delta AIC=+0.736`, `Delta BIC=+11.629` for the SH0ES column. It is worse in
chi-square than fitted `wCDM/CPL` on both branches.

No likelihood preference is claimed. The rows were not fitted in MTS theory
space, `sigma_theta` is not numerically parent-predicted, `Omega_m` was fixed,
and the full coupled perturbation kernel is not yet in the likelihood.

## 8. Arbitration

| Gate | Result |
|---|---|
| Closed-bath source for `sigma_theta` | Constructed |
| Exact Kubo matching formula | Derived |
| `sigma_theta` predicted from `gamma_M` | No; independent cross spectrum |
| Mandatory diagonal susceptibilities | Derived and retained |
| Covariant interaction stress/clock current | Derived |
| Total FLRW conservation | Closed numerically and analytically |
| Three backreacted branches | Pass |
| Controlled smooth-memory growth | Sub-percent shifts |
| Real SN+BAO background smoke | Executed; MTS remains competitive with LambdaCDM |
| Coupled local characteristic cone | Stable but exceeds public cone |
| Full nonlocal causal front | Open |
| Full perturbation likelihood | Open |
| Dynamical binary leakage | Open |

The project has moved beyond a coefficient placeholder: the coefficient now
has an exact parent matching equation, the stress is owned, backreaction is
closed, and real data have been touched. What remains is sharper than before:
derive the full causal retarded kernel and use it in perturbations and
binaries. If that full kernel cannot restore an acceptable front and control
dynamical leakage, this expansion source must be demoted despite its good
background behavior.

## 9. Next target

`4889-Y5-R2FR-nonlocal-bath-retarded-kernel-causal-front-growth-and-binary-leakage-or-expansion-source-demotion-gate.md`

The next gate must:

1. choose a positive spectral density that produces the same
   `gamma_M`, `sigma_theta`, and required diagonal moments;
2. retain its frequency dependence and calculate poles, branch cuts and the
   high-frequency front velocity;
3. derive the full clock--memory--metric scalar perturbation system rather
   than the dust/smooth limit;
4. rerun growth/CMB data only if the kernel is stable and causal;
5. calculate time-dependent binary sourcing and radiation leakage before
   extending stationary local-GR silence.

## Sources

- `post-checkpoint-work/4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md`.
- `post-checkpoint-work/4885-Y5-R2FR-Gamma-memory-determinant-and-nonminimal-weight-from-closed-bath-or-three-boson-branch-demotion-gate.md`.
- `post-checkpoint-work/4887-Y5-R2FR-conserved-derivative-memory-source-with-local-PPN-silence-and-FLRW-activation-or-active-M-cosmology-demotion-gate.md`.
- `formalization-workbench/data/cosmology/pantheon_plus/`.
- `formalization-workbench/data/cosmology/desi_dr2_bao/`.
