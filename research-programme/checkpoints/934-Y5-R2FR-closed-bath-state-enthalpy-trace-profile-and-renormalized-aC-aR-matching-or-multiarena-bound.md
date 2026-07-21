# 4918 - Bath-state profile, curvature matching and local arena gate

Marker: `MTS_BATH_STATE_CURVATURE_MATCHING_LOCAL_GATE_4918`

## Decision

Checkpoint 4917 left the hidden enthalpy profile open. The current corpus
already contains enough information to resolve that statement more sharply.

There are three different objects which must not be merged.

1. **Microscopic parent:** the closed bath fields occur in the path integral.
2. **Active low-energy baseline:** those fields are integrated out once into
   renormalized gravitational coefficients and form factors, and
   `Gamma_MTS,res=0`. There is no independent `T_X`, `rho_X`, `p_X` or `u_X`
   in this action.
3. **Nonvacuum extension:** retaining a thermal, coherent or clock-current
   bath state creates an explicit `Gamma_MTS,res` and must pass the re-entry
   gates. The 4896 full-matrix branch supplies one exact stress profile, but
   that branch is retired from active cosmology.

Consequently the gravity-mediated state-flow contact derived at 4917 is
exactly zero on the declared active IR baseline:

\[
\boxed{
T_X^{\mu\nu}=0,
\quad h_X:=\rho_X+p_X=0,
\quad \tau_X:=-\rho_X+3p_X=0,
\quad p_{\rm mix}=\sigma_{\rm mix}=0.
}
\]

This is not the assertion that an active physical bath somehow has zero
stress. It is the field-content statement that the bath has already been
integrated out and cannot be added again as matter. A nonvacuum bath is a
different extension.

Before integration, any Lorentz-invariant hidden vacuum obeys

\[
\langle T_X^{\mu\nu}\rangle=-\rho_v g^{\mu\nu},
\qquad p_X=-\rho_v,
\qquad h_X=0.
\]

It therefore has no flow spurion and gives `p_mix=0`. Its vacuum density and
determinants are absorbed once into `Lambda_cal`, `a_R`, `a_C` and the
nonlocal form factors. Selecting the invariant vacuum is a state/branch
condition, not a microscopic prediction of the vacuum energy.

For a genuine nonvacuum state the exact 4896 parent gives both enthalpy and
trace. The current selected matter-loop ray is also now explicit:

\[
\boxed{
a_{C,{\rm loop}}=\frac{L}{128\pi^2},
\qquad
a_{R,{\rm loop}}=\frac{L}{384\pi^2},
\qquad
\frac{a_R}{a_C}=\frac13
}
\]

for the minimal `complex psi + M + U(1)` matter component. The complete
renormalized coefficients remain open finite matching sums.

The local observable result is therefore

```text
active IR bath stress                    = absent by Wilsonian field content
active p_mix and sigma_mix               = exactly zero
invariant-vacuum enthalpy                = exactly zero by state symmetry
4896 nonvacuum rho/h/tau profile         = derived but retired diagnostic
selected matter-loop a_C/a_R ray         = derived
total renormalized a_C/a_R               = open finite matching sums
universal contact WEP eta                = exactly zero at test-body order
clock anomaly                            = profile difference, not absolute sigma
independent nonuniversal mixed operators = still open
```

## 1. Two-layer action and the no-double-counting theorem

The microscopic proposal has schematic field space

\[
Z_{\rm parent}=\int
\frac{D\mathcal H\,D\psi_rD\psi_aDXD\Phi_{\rm SM}}
{\operatorname{Vol}(\operatorname{Diff}\times G_{\rm SM})}
e^{iS_{\rm parent}}.
\]

At a Wilsonian scale below the hidden thresholds, define

\[
e^{i\Gamma_X[g;\rho_X]}
=\int_{\rho_X}D\psi_rD\psi_aDX\,
e^{iS_{\rm MTS+bath}[g,\psi,X]}.
\]

For an invariant vacuum state, `Gamma_X` is a covariant functional of the
public metric alone. Its local expansion is already represented by

\[
\int\sqrt{-g}\left[
-M_R^2\Lambda_{\rm cal}
+\frac{M_R^2}{2}R+a_RR^2+a_CC^2+a_EE_4+\cdots
\right]
\]

and its nonlocal form factors. The current active action is

\[
\Gamma_{\rm current}
=\Gamma_{\rm grav,R}[g(\mathcal H)]
+S_{\rm SM}[g(\mathcal H),\Phi_{\rm SM}]
+\Gamma_{\rm MTS,res},
\qquad
\boxed{\Gamma_{\rm MTS,res}=0}.
\]

There is no remaining independent functional argument `X` and no separate
IR Hilbert source `T_X`. Re-adding the same determinant as a bath-fluid source
would count the same microscopic sector twice. Thus, in the active baseline,

\[
\boxed{
\rho_X=p_X=h_X=\tau_X=0
}
\]

as independent IR source variables. This is exact for the declared action.
It does not prove that the microscopic theory dynamically selects this state
in every environment.

If a nonvacuum density matrix introduces a Landau vector or coherent current,
then

\[
\Gamma_X[g;\rho_X]
=\Gamma_X^{\rm vac}[g]
+\Gamma_X^{\rm state}[g,u_X,\rho_X,\ldots]
\]

and the second term is precisely a nonzero `Gamma_MTS,res` extension. It may
not inherit the active-baseline pass without being tested.

## 2. Invariant-vacuum theorem

With no vector or tensor state spurion, local Lorentz invariance permits only

\[
\langle T_X^{\mu\nu}\rangle=A g^{\mu\nu}.
\]

Defining the rest-frame density fixes `A=-rho_v`, hence

\[
\langle T_X^{\mu\nu}\rangle
=-\rho_vg^{\mu\nu},
\qquad
p_X=-\rho_v,
\qquad
\tau_X=-4\rho_v.
\]

The enthalpy is exactly

\[
\boxed{h_X=\rho_X+p_X=0.}
\]

Therefore

\[
p_{\rm mix}
=-8a_Ch_X/M_R^4=0
\]

without setting `a_C=0`. A constant conformal contact can be written before
vacuum matching, but after the vacuum determinant and relevant coupling have
been absorbed it is not an additional local matter source. A constant common
rescaling is fixed together with measured masses, rods, clocks and `G_N`.

This theorem distinguishes two claims:

```text
existence of a Lorentz-invariant local-GR state branch = derived;
unique dynamical selection of that state everywhere    = not derived.
```

## 3. Exact nonvacuum bath stress

Checkpoint 4896 derives the stress from the same reciprocal closed continuum
that owns its response. Write

\[
K_\chi=\int d\Omega\,\dot\chi_\Omega^2,
\qquad
I_m=\int d\Omega\,\Omega^2\chi_\Omega^2,
\qquad
Y=\int d\Omega\,g_\Omega\chi_\Omega,
\]

and

\[
J=\int d\Omega\,g_\Omega\dot\chi_\Omega.
\]

The exact homogeneous density and enthalpy are

\[
\boxed{
\frac{\rho_B}{M_R^2}
=D+\frac12K_\chi+\frac12I_m-\phi Y
+\frac12C_{\phi\phi}\phi^2
-\frac12C_{\theta\theta}\theta^2,
}
\]

\[
\boxed{
\frac{h_B}{M_R^2}
=\frac{\rho_B+p_B}{M_R^2}
=D+K_\chi-qJ-\dot b.
}
\]

It follows, without a new closure, that

\[
\boxed{
\begin{aligned}
\frac{\tau_B}{M_R^2}
={}&-D+K_\chi-2I_m-3qJ-3\dot b+4\phi Y\\
&-2C_{\phi\phi}\phi^2
+2C_{\theta\theta}\theta^2.
\end{aligned}
}
\]

The executable symbolic residual in `tau_B=3h_B-4rho_B` is exactly zero.

On the stationary zero-response mean field:

- if `D=0`, then `rho_B=h_B=tau_B=0`;
- if `D` is nonzero, then

  \[
  \rho_B=M_R^2D,
  \quad p_B=0,
  \quad h_B=M_R^2D,
  \quad \tau_B=-M_R^2D.
  \]

Thus checkpoint 4895's response decoupling does not prove that an equilibrium
bath has no stress. A nonzero conserved clock current is ordinary hidden dust
and belongs to an extension, not the metric-only baseline.

## 4. Reconstructed 4896 profile

The archived full-matrix background already contains `E`, `d ln H/dN`, the
memory kinetic variable and bath density fraction. Raychaudhuri gives the
bath enthalpy fraction directly:

\[
\frac{h_B}{3M_R^2H^2}
=-\frac23\left[
\frac{d\ln H}{dN}
+2\Omega_r(z)
+\frac32\Omega_{m,{\rm other}}(z)
+\frac12\phi_N^2
\right].
\]

Then

\[
\frac{\tau_B}{3M_R^2H^2}
=3\frac{h_B}{3M_R^2H^2}
-4\frac{\rho_B}{3M_R^2H^2}.
\]

All eight Raychaudhuri reconstructions close below `4.45e-16`. Selected rows
are

| `z` | `rho_B/(3M_R^2H^2)` | `h_B/(3M_R^2H^2)` | `tau_B/(3M_R^2H^2)` | `w_B` |
|---:|---:|---:|---:|---:|
| `1e6` | `-1.04739` | `-1.39954` | `-0.009056` | `0.33622` |
| `1100` | `0.48800` | `0.46403` | `-0.55992` | `-0.04912` |
| `10` | `0.59833` | `0.59847` | `-0.59791` | `0.000233` |
| `0` | `0.04900` | `0.39896` | `1.00089` | `7.14214` |

This is an actual derived profile, not a placeholder. It also reinforces the
4896 retirement: the state is neither a small late-only fluid nor an
innocuous hidden dust component. These rows are diagnostic and may not be
reintroduced as current MTS cosmology predictions.

## 5. Renormalized `a_C/a_R` matching

Checkpoint 4884 gives the complete decomposition

\[
\boxed{
\begin{aligned}
a_C^R(\mu)={}&a_{C,{\rm fin}}(\mu_0)
+a_{C,{\rm loop}}(\mu)
+a_{C,H/{\rm gh}}(\mu)
+a_{C,{\rm th}}(\mu),\\
a_R^R(\mu)={}&a_{R,{\rm fin}}(\mu_0)
+a_{R,{\rm loop}}(\mu)
+a_{R,H/{\rm gh}}(\mu)
+a_{R,{\rm th}}(\mu).
\end{aligned}
}
\]

Checkpoint 4885 selects the renormalized-Einstein fallback and identifies the
minimal matter weights

\[
N_s=3,
\quad N_V=1,
\quad W_C=15,
\quad S_{h^2}=3,
\quad W_1=-1.
\]

For `L=ln(Lambda_UV/mu)`, the matter-loop component is therefore

\[
\boxed{
a_{C,{\rm loop}}
=\frac{15L}{1920\pi^2}
=\frac{L}{128\pi^2}
=7.91572\times10^{-4}L,
}
\]

\[
\boxed{
a_{R,{\rm loop}}
=\frac{3L}{1152\pi^2}
=\frac{L}{384\pi^2}
=2.63857\times10^{-4}L.
}
\]

Thus

\[
\frac{a_{R,{\rm loop}}}{a_{C,{\rm loop}}}=\frac13,
\qquad
\frac{da_C}{d\ln\mu}=-\frac1{128\pi^2},
\qquad
\frac{da_R}{d\ln\mu}=-\frac1{384\pi^2}
\]

for this matter component. The optional boundary condition
`a_R,fin=a_C,fin=0` is not promoted. The total coefficients remain unknown,
but that no longer blocks the active state-flow channel because its source is
zero independently of their values.

## 6. Loop projection of the retired profile

Using the one global Planck calibration and `H0=67.4 km s^-1 Mpc^-1`,

\[
\frac{3H_0^2}{M_R^2}=1.04558221\times10^{-120}.
\]

On the loop ray,

\[
p_{{\rm mix},{\rm loop}}
=-\frac{Lh_B}{16\pi^2M_R^4},
\]

\[
\sigma_{{\rm mix},{\rm loop}}
=-\frac{L(3h_B+\tau_B)}{384\pi^2M_R^4}.
\]

At `z=0` on the retired profile,

\[
\boxed{
\frac{p_{\rm mix}}L=-2.64164\times10^{-123},
\qquad
\frac{\sigma_{\rm mix}}L=-6.06336\times10^{-124}.
}
\]

These values are tiny diagnostics, not active predictions. Conversely, using
the multimessenger product interval to constrain the unknown total coefficient
on this present profile gives only approximately

\[
-1.80\times10^{105}
\lesssim a_C^R
\lesssim4.20\times10^{104}.
\]

The cone observation does not meaningfully determine `a_C`; the Planck
hierarchy does the suppression. The exact active-baseline zero is therefore
more informative than pretending this enormous interval is a useful
coefficient measurement.

## 7. Correct clock combination

The inverse matter metric is, at first order,

\[
g_m^{\mu\nu}
=g^{\mu\nu}+p_{\rm mix}u^\mu u^\nu
+2\sigma_{\rm mix}g^{\mu\nu}.
\]

Its inverse is

\[
g^m_{\mu\nu}
=g_{\mu\nu}-p_{\rm mix}u_\mu u_\nu
-2\sigma_{\rm mix}g_{\mu\nu}.
\]

For a stationary clock comoving with the state,

\[
\frac{d\tau_m}{d\tau_g}
=1+\frac12p_{\rm mix}-\sigma_{\rm mix}+O(a_i^2).
\]

The actual clock potential is therefore not `sigma_mix` alone but

\[
\boxed{
\kappa_{\rm clock}
:=\frac12p_{\rm mix}-\sigma_{\rm mix}
=\frac{-4a_C\rho_X
+2(a_R-2a_C/3)\tau_X}{M_R^4}.
}
\]

On the selected loop ray,

\[
\boxed{
\kappa_{{\rm clock},{\rm loop}}
=-\frac{L(9h_X-\tau_X)}{384\pi^2M_R^4}.
}
\]

At `z=0` on the retired profile,

\[
\frac{\kappa_{\rm clock}}L
=-7.14483\times10^{-124}.
\]

A constant `kappa_clock` is common to all minimally coupled clocks and
calibrates out of frequency ratios. Only a profile difference is observable.
The Galileo one-sigma result implies

\[
\boxed{
|\Delta\kappa_{\rm clock}|
\le2.48\times10^{-5}|\Delta U/c^2|.
}
\]

For the Earth-to-Galileo radii used at checkpoints 4878--4879,

\[
|\Delta U/c^2|=5.46295\times10^{-10},
\]

so

\[
\boxed{
|\Delta\kappa_{\rm clock}|
\le1.35481\times10^{-14}.
}
\]

This is a real profile-difference bound. A homogeneous cosmological state has
zero Earth-to-satellite difference at this order; an inhomogeneous revived
bath must supply its local profile before being scored.

## 8. WEP and Maxwell projections

The 4917 contact is universal because it multiplies the total visible Hilbert
stress. All minimally coupled test bodies therefore follow geodesics of the
same `g_m`. At monopole/test-body order,

\[
\boxed{\eta_{AB}=0}
\]

for this contact even when `p_mix` and `sigma_mix` vary. This is a genuine
weak-equivalence zero. It is not a strong-equivalence theorem for compact
bodies and does not remove independent species, Higgs or gauge mixed
operators.

For four-dimensional classical Maxwell,

\[
T_{\rm EM}=0.
\]

The conformal `sigma_mix` shift therefore leaves the photon cone unchanged.
The anisotropic `p_mix` shift remains the relative-cone channel already bounded
at 4917. On the active baseline both are exactly zero.

## 9. Local-GR state gate

The state-flow contact can no longer be listed as a generic active-baseline
unknown.

```text
active metric-only IR action:
    T_X=h_X=tau_X=0 as independent sources;
    p_mix=sigma_mix=kappa_clock=0;
    local GR/Newton/Maxwell source branch unchanged.

microscopic invariant vacuum:
    h_X=0 by symmetry;
    no u_X spurion;
    vacuum matching absorbed once;
    state selection remains a branch condition.

nonvacuum extension:
    exact parent stress formulas exist;
    4896 profile is derived but retired;
    cone and clock profile bounds apply;
    re-entry requires a new passing parent.
```

What remains for the local fundamental claim is not this stress-contact state
channel. It is the vacuum 1PI basis that does not require a flow spurion:
`R H_SM^dagger H_SM`, hidden-scalar vacuum expectation values, and correlated
gauge/Higgs/fermion operators.

## 10. Next target

`4919-Y5-R2FR-vacuum-1PI-operator-selection-curvature-Higgs-and-hidden-scalar-vev-matching-or-local-bound.md`

Calculate the surviving mixed operators in the invariant vacuum after the
`u`-dependent basis is removed. Start with the curvature-Higgs term and any
hidden scalar vacuum expectation value, derive which pieces are field-basis
redundant, and map the irreducible remainder into Higgs, clock, WEP and local
gravity bounds.

No GitHub action or public claim is authorized.
