# 4878 Y5 R2FR renormalized-EFT local limit and arena-specific residual bounds

**Status:** The strict renormalized-EFT branch is selected. Finite local `R^2` and `C^2` coefficients do not generate an exterior Yukawa force when treated perturbatively: at first EFT order their `q^2` numerator cancels the massless propagator and leaves contact support. The R10 Yukawa curve is therefore relevant only to a separately labelled resummed quadratic-gravity diagnostic. Universal matter logarithms give a derived `r^-3` tail, and the physical pure-gravity one-loop Newton tail supplies the previously open long-range `H`/ghost Newton coefficient. Both are numerically negligible in the tested arenas. Minimal Maxwell remains exact at this order. Full local-GR promotion is still withheld because source-size contact matching, nonlinear `beta`, and gauge-invariant pure-gravity clock/light kernels remain to be completed.

Marker: `MTS_RENORMALIZED_EFT_LOCAL_ARENA_BOUNDS_4878`.

## 1. The branch distinction that removes the false coefficient problem

Take the renormalized public-metric action in the convention

\[
\Gamma_{\rm loc}=\int d^4x\sqrt{-g}\left[
\frac{\overline M_{\rm Pl}^2}{2}R
+a_R R^2+a_C C_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma}
+\cdots\right].
\]

There are two mathematically different uses of this action.

1. **Strict EFT:** expand perturbatively in `a_R q^2/Mbar_Pl^2` and `a_C q^2/Mbar_Pl^2`. This is the selected low-energy branch.
2. **Resummed quadratic gravity:** invert the full fourth-order denominator and interpret its additional zeros as massive poles. This is useful as a diagnostic but changes the spectrum and cannot be silently identified with the strict EFT.

The distinction matters because a Yukawa exclusion curve bounds an extra propagating pole. It does not directly bound a perturbative contact operator. This agrees with the field-redefinition and amplitude theorem of [Accettulli Huber et al.](https://arxiv.org/abs/1911.10108): curvature-squared operators do not correct the long-range Newton potential in the strict EFT with minimally coupled separated heavy sources.

## 2. Exact scalar and spin-2 response transfer

Let the conserved-source scalar and spin-2 denominators be

\[
A_0(q)=1+d_0(q),\qquad A_2(q)=1+d_2(q).
\]

The exact weak static potentials are

\[
\boxed{
\frac{\Phi}{\Phi_N}
=\frac{4}{3A_2}-\frac{1}{3A_0},
\qquad
\frac{\Psi}{\Psi_N}
=\frac{2}{3A_2}+\frac{1}{3A_0}.
}
\]

Consequently,

\[
\boxed{
\gamma(q)=\frac{\Psi}{\Phi}
=\frac{2d_0+d_2+3}{4d_0-d_2+3}.
}
\]

To first order,

\[
\frac{\Phi}{\Phi_N}=1+\frac{d_0}{3}-\frac{4d_2}{3},
\]

\[
\frac{\Psi}{\Psi_N}=1-\frac{d_0}{3}-\frac{2d_2}{3},
\qquad
\gamma-1=\frac{2}{3}(d_2-d_0).
\]

These identities are derived symbolically in `scripts/Y5_R2FR_4878_local_eft_arena_bounds.py`; they are not fitted projection coefficients.

## 3. Strict-EFT contact theorem

For the finite local operators,

\[
d_{0,\rm loc}=12a_R\bar\ell_P^2q^2,
\qquad
d_{2,\rm loc}=-4a_C\bar\ell_P^2q^2,
\]

where

\[
\bar\ell_P^2=8\pi\frac{G\hbar}{c^3}.
\]

The correction to the static Fourier integrand contains the Newton propagator `1/q^2`. Substitution gives

\[
\frac{1}{q^2}\left(\frac{d_0}{3}-\frac{4d_2}{3}\right)
=\frac{4\bar\ell_P^2}{3}(3a_R+4a_C),
\]

\[
\frac{1}{q^2}\left(-\frac{d_0}{3}-\frac{2d_2}{3}\right)
=\frac{4\bar\ell_P^2}{3}(-3a_R+2a_C).
\]

Both are momentum polynomials. Their transforms are `delta^3(r)` and derivative contact distributions. Therefore

\[
\boxed{
\delta\Phi_{R^2,C^2}(r)=\delta\Psi_{R^2,C^2}(r)=0
\quad\text{outside nonoverlapping source supports at first EFT order}.
}
\]

This is not a claim that `a_R=a_C=0`. It is a support theorem: finite local coefficients affect contact/source structure and higher-order matching, not the long-range exterior potential at the retained order.

At the shortest Eot-Wash separation, `r_min=52 micrometres`,

\[
\frac{\bar\ell_P^2}{r_{\min}^2}=2.42802384824\times10^{-60}.
\]

Requiring each derivative correction to be below one percent gives only the EFT-control caps

\[
|a_R|<3.43214640967\times10^{56},
\qquad
|a_C|<1.02964392290\times10^{57}.
\]

These are not empirical bounds. If a coefficient exceeds the control corridor, the calculation must switch branches and resum the pole rather than continue to call itself strict EFT.

## 4. Resummed quadratic-gravity diagnostic

For

\[
A_0=1+\frac{q^2}{m_0^2},
\qquad
A_2=1+\frac{q^2}{m_2^2},
\]

the partial fraction identity

\[
\frac{1}{q^2(1+q^2/m^2)}
=\frac1{q^2}-\frac1{q^2+m^2}
\]

gives

\[
\Phi(r)=-\frac{GM}{r}\left[
1+\frac13e^{-m_0r}-\frac43e^{-m_2r}
\right],
\]

\[
\Psi(r)=-\frac{GM}{r}\left[
1-\frac13e^{-m_0r}-\frac23e^{-m_2r}
\right].
\]

With this checkpoint's normalization,

\[
\lambda_0=\sqrt{12a_R}\,\bar\ell_P,
\qquad
\lambda_2=2\sqrt{|a_C|}\,\bar\ell_P.
\]

The 176-point vector extraction of the Eot-Wash 2020 absolute-`alpha` curve yields the log-log crossings

| channel | `|alpha|` | extracted range | internal coefficient envelope |
|---|---:|---:|---:|
| scalar | `1/3` | `53.6702301 micrometres` | `a_R < 3.65616707e58` |
| published check | `1` | `38.3693961 micrometres` | agrees with stated `38.6 micrometres` to `0.60%` |
| spin-2 absolute envelope | `4/3` | `35.5493808 micrometres` | `|a_C| < 4.81220871e58` |

At these diagnostic limits, `d0(52 micrometres)=1.0653` and `|d2|=0.4674`; they are not in the one-percent perturbative corridor. This confirms that the two branches must not be mixed.

The curve remains private nonclaim evidence because it is a vector extraction from the published figure rather than the official sign-specific supplementary table. In addition, the spin-2 pole is not a healthy fundamental completion: `a_C<0` gives a real pole with negative residue, while `a_C>0` gives a tachyonic/oscillatory denominator.

## 5. Universal matter nonlocal tail

Checkpoint 4877 derived the covariant matter form factors. For `r>0`,

\[
\int\frac{d^3q}{(2\pi)^3}e^{i\mathbf q\cdot\mathbf r}
\log\!\left(\frac{q^2}{\mu^2}\right)
=-\frac{1}{2\pi r^3}.
\]

For the imported Standard Model correspondence anchor `S_h2=4`, `W_C=283`, define

\[
\kappa_0=\frac{S_{h^2}\bar\ell_P^2}{96\pi^2}
=2.77171549\times10^{-71}\ {\rm m}^2,
\]

\[
\kappa_2=\frac{W_C\bar\ell_P^2}{480\pi^2}
=3.92197741\times10^{-70}\ {\rm m}^2.
\]

Without allowing scalar/spin-2 cancellation, the position-space envelopes are

\[
\left|\frac{\delta\Phi}{\Phi_N}\right|
\le\frac{\eta_\Phi}{r^2},
\qquad
\eta_\Phi=\frac{\kappa_0+4\kappa_2}{3}
=5.32169373\times10^{-70}\ {\rm m}^2,
\]

\[
\left|\frac{\delta\Psi}{\Psi_N}\right|
\le\frac{\eta_\Psi}{r^2},
\qquad
\eta_\Psi=\frac{\kappa_0+2\kappa_2}{3}
=2.70704212\times10^{-70}\ {\rm m}^2,
\]

\[
|\gamma-1|\le\frac{\eta_{\rm slip}}{r^2},
\qquad
\eta_{\rm slip}=\frac{2(\kappa_0+\kappa_2)}{3}
=2.79943264\times10^{-70}\ {\rm m}^2.
\]

The acceleration envelope is `3 eta_Phi/r^2`.

## 6. Physical pure-gravity long-range Newton coefficient

The gauge-invariant nonanalytic one-loop result of [Bjerrum-Bohr, Donoghue and Holstein](https://arxiv.org/abs/hep-th/0211072) gives

\[
V(r)=-\frac{Gm_1m_2}{r}\left[
1+\frac{3G(m_1+m_2)}{rc^2}
+\frac{41}{10\pi}\frac{G\hbar}{r^2c^3}
\right].
\]

The classical post-Newtonian term is part of the GR baseline. The universal quantum coefficient is

\[
\eta_{\rm grav}=\frac{41}{10\pi}\ell_P^2
=3.40921005\times10^{-70}\ {\rm m}^2.
\]

This replaces an open generic `H`/ghost coefficient in the physical Newton/scattering channel. It does not license a gauge-dependent off-shell split into `d0` and `d2`, and it is not automatically a clock or light-propagation kernel.

The conservative physical central-potential envelope used below is

\[
\eta_{N,\rm total}=\eta_\Phi+\eta_{\rm grav}
=8.73090378\times10^{-70}\ {\rm m}^2.
\]

## 7. Arena projections and inverted coefficient limits

The comparison uses the same calibrated `G_N` and frozen `Lambda_cal` in every row.

| arena | derived observable envelope | source anchor | margin |
|---|---:|---:|---:|
| R10 at `52 micrometres` | `|delta a/a| = 9.68665e-61` | `1e-2` percent-level context | `1.03e58` |
| Cassini, `b=1.6 R_sun` | matter-loop deflection-equivalent `|gamma-1| = 1.29596e-87` | `2.3e-5` 1-sigma anchor | `1.77e82` |
| Galileo Earth-to-satellite redshift | `|alpha_clock| = 1.65403e-83` | `2.48e-5` 1-sigma anchor | `1.50e78` |
| Mercury extra precession | `4.58225e-82 arcsec/century` | `0.0015 arcsec/century` uncertainty | `3.27e78` |

The corresponding observable-level coefficient caps are

| arena | coefficient combination | predicted coefficient | inverted cap |
|---|---|---:|---:|
| R10 point-separation envelope | `eta_N,total` | `8.73090e-70 m^2` | `9.01333e-12 m^2` |
| Cassini deflection-equivalent | `eta_Phi+eta_Psi` | `8.02874e-70 m^2` | `1.42489e13 m^2` |
| Galileo redshift | `eta_Phi` | `5.32169e-70 m^2` | `7.97917e8 m^2` |
| Mercury precession | `eta_N,total` | `8.73090e-70 m^2` | `2.85806e9 m^2` |

The formulas used are

\[
\left|\frac{\delta a}{a_N}\right|
\le\frac{3\eta_{N,\rm total}}{r^2},
\]

\[
|\gamma-1|_{\rm deflection,eq}
\le\frac{2(\eta_\Phi+\eta_\Psi)}{b^2},
\]

\[
|\alpha_{\rm clock}|\le
\eta_\Phi\left(
\frac1{r_1^2}+\frac1{r_1r_2}+\frac1{r_2^2}
\right),
\]

\[
|\Delta\varpi|\le
\frac{6\pi\eta_{N,\rm total}}
{a^2(1-e^2)^2}
\quad\text{per orbit}.
\]

The empirical anchors are the [Eot-Wash 2020 short-range test](https://arxiv.org/abs/2002.11761), the [Cassini radio-science result](https://pubmed.ncbi.nlm.nih.gov/14508481/), the [Galileo redshift test](https://arxiv.org/abs/1906.06161), and the [MESSENGER Mercury analysis](https://www.osti.gov/biblio/22863119).

These huge margins establish a scale hierarchy, not four public likelihood passes. The R10 `r^-3` tail still requires convolution through the torsion-balance geometry for a likelihood-level result. The pure-gravity Newton coefficient does not yet supply the corresponding clock or light kernel.

## 8. Maxwell projection closes at this order

For the independent public `U(1)` branch,

\[
S_{\rm EM}=-\frac{\lambda_A}{4}\int\sqrt{-g}\,F_{\mu\nu}F^{\mu\nu}
+\int\sqrt{-g}\,A_\mu J^\mu.
\]

Neither `a_R` nor `a_C` appears in the variation with respect to `A_mu`, so

\[
\boxed{\nabla_\mu(\lambda_A F^{\mu\nu})=J^\nu}
\]

remains exact at this order. In four classical dimensions,

\[
T^{\mu}{}_{{\rm EM}\mu}=0.
\]

Therefore free Maxwell stress does not source the scalar `R^2` channel at linear order when no incoming homogeneous scalar is admitted. Its traceless stress does source the spin-2 metric channel. The Poynting vector remains `T^{0i}_{EM}`, not an extra force or a second source.

If `RF^2`, `R_{\mu\nu}F^{\mu\alpha}F^\nu{}_{\alpha}`, or flow-constitutive `u_mu u_nu F^{mu alpha}F^nu{}_alpha` operators are absent, photons remain on the same public-metric null cone. Checkpoint 4854's constitutive branch is separate and cannot be attributed to `a_R` or `a_C`.

## 9. What is now closed and what is not

Closed in the selected branch:

- exact scalar/spin-2 source transfer and linear slip;
- strict-EFT exterior contact theorem for finite local `R^2/C^2`;
- branch-correct R10 treatment and internal resummed coefficient envelopes;
- matter-loop `r^-3` metric tails in position space;
- physical pure-gravity long-range Newton coefficient `41/(10pi)`;
- analytic clock, central-orbit and matter-loop light projections;
- minimal Maxwell equation, classical trace selection and Poynting source bookkeeping.

Not yet closed:

- finite-size/contact matching inside material source supports;
- the nonlinear second-order metric coefficient entering PPN `beta`;
- the gauge-invariant pure-gravity clock and light-bending kernels;
- a full R10 apparatus convolution for the power-law tail;
- primitive MTS derivation of the imported Standard Model loop spectrum.

The local branch is materially closer to GR: finite local Wilson coefficients are no longer treated as arbitrary long-range Yukawa defects, and the pure-gravity Newton tail is no longer an unspecified `H`/ghost placeholder. Full local-GR promotion remains false until the nonlinear and observable-specific items above are derived.

## 10. Claim guards

- Do not apply the R10 Yukawa curve directly to strict-EFT `a_R` or `a_C`.
- Do not call the one-percent derivative caps empirical limits.
- Do not call the extracted absolute-`alpha` curve sign-specific official data.
- Do not admit the resummed spin-2 ghost as a healthy MTS particle.
- Do not use cancellation between scalar, spin-2, matter and graviton tails.
- Do not promote the point-separation R10 envelope to an apparatus likelihood.
- Do not map the `41/(10pi)` Newton potential coefficient to clocks or photons without the corresponding gauge-invariant observable calculation.
- Do not retune `G_N`, `Lambda_cal`, the loop spectrum or any coefficient by arena.

## 11. Decision and next target

Decision:

`STRICT_RENORMALIZED_EFT_SELECTED; LOCAL_R2_C2_EXTERIOR_CONTACT_ONLY; RESUMMED_YUKAWA_DIAGNOSTIC_NONCLAIM; MATTER_AND_PURE_GRAVITY_LONG_RANGE_NEWTON_TAILS_DERIVED_AND_TINY; MINIMAL_MAXWELL_CLOSED_AT_THIS_ORDER; FULL_LOCAL_GR_PROMOTION_WITHHELD`.

Next target:

`4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md`
