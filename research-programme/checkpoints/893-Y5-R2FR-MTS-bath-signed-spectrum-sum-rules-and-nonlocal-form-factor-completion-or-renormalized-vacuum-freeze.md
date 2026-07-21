# 4877 - MTS spectrum sum rules, nonlocal completion and renormalized-vacuum freeze

Marker: MTS_SPECTRUM_NO_GO_NONLOCAL_COMPLETION_AND_RENORMALIZED_VACUUM_FREEZE_4877

Decision: PRIMITIVE_BOSONIC_SPECTRUM_CANNOT_CANCEL_VACUUM_IMPORTED_SM_NONZERO_UNIVERSAL_NONLOCAL_LOGS_DERIVED_IR_DECOUPLING_PROVED_C0R_RENORMALIZED_FREEZE_SELECTED_LOCAL_ARENA_SMOKE_TINY_PRIVATE_NONCLAIM

## Result

Checkpoint 4876 left a real fork: derive a signed MTS spectrum that cancels the public-volume source while retaining positive Einstein stiffness, or stop implying that the vacuum is predicted and freeze one renormalized cosmological coefficient. This checkpoint searches the corpus, calculates the full ordinary scalar/Dirac/Maxwell weight algebra, and decides that fork.

The answer is deliberately split into what is derived and what is not:

- the primitive MTS substrate is bosonic as presently written;
- no Grassmann measure, Dirac kinetic operator, Clifford module or spin-statistics map is supplied by the corpus;
- the primitive bosonic spectrum therefore cannot satisfy the one-loop quartic vacuum cancellation condition;
- importing the Standard Model gives positive Einstein weight in the chosen counting convention, but still does not cancel the vacuum weight;
- the earlier four-scalar/one-Dirac example is threshold-rigid and is not an MTS-owned cancellation mechanism;
- the universal matter-induced `C log(-Box) C` and `R log(-Box) R` form factors are now explicit and decouple relative to Einstein gravity in the infrared;
- a single renormalized `C0_R` condition is therefore frozen at one cosmological matching scale, with no arena-by-arena retuning.

This does not solve the cosmological-constant problem and does not open a local-GR claim. It gives the competitive infrared EFT a mathematically honest background condition and removes the false alternative of treating an unsupported particle count as a derivation.

## 1. Actual corpus spectrum

The core action and effective-field-theory documents call the elementary object a scalar motion field and print

\[
\psi:\mathbb R^4\rightarrow\mathbb R.
\]

Later particle documents instead call `psi` complex, introduce a bosonic curvature-memory variable, describe particle families as configurations of one nonlinear motion field, and explicitly say that no gauge fields are used in those constructions. Across the core and particle Markdown corpus, the search found no primitive:

- Grassmann integration variables;
- anticommutation algebra;
- Dirac operator;
- Clifford representation;
- spin-statistics derivation.

The particle solitons therefore cannot be counted as independent Dirac determinants merely because they are labelled leptons or quarks. Schwinger-Keldysh `r/a` doubling also does not double the number of physical species.

The independent Maxwell and generic matter actions enter only in the later public correspondence parent. The separate Yang-Mills document is an extension and has not been wired into the selected integrated-`H` microscopic measure. The current corpus thus supports the following narrow verdict:

\[
\boxed{\text{primitive UV substrate as written: bosonic, with a real/complex normalization conflict.}}
\]

This is a spectrum result, not a statement that fermions can never emerge. To enter a one-loop signed determinant, an emergent fermion branch must still derive its Grassmann measure and kinetic operator.

## 2. Determinant weights

Use one minimally coupled real scalar as the normalization unit. The gauge-fixed one-loop operators are

\[
\Gamma_s=\frac12{\rm Tr}\log\Delta_0,
\]

\[
\Gamma_D=-\frac12{\rm Tr}\log(\slashed D^2),
\]

\[
\Gamma_V=\frac12{\rm Tr}\log\Delta_1-{\rm Tr}\log\Delta_{0,\rm gh}.
\]

Their relative heat-kernel weights are

| field | vacuum `C0` | Einstein `Mstar^2` | Weyl-log `C log C` |
|---|---:|---:|---:|
| real scalar | `+1` | `+1` | `+1` |
| Dirac fermion | `-4` | `+2` | `+6` |
| Maxwell vector plus ghost | `+2` | `-4` | `+12` |

For scalar nonminimal couplings define

\[
S_h=\sum_s(1-6\xi_s),
\qquad
S_{h^2}=\sum_s(1-6\xi_s)^2.
\]

For `N_s` real scalars, `N_D` Dirac fields and `N_V` Maxwell fields,

\[
\boxed{W_0=N_s+2N_V-4N_D,}
\]

\[
\boxed{W_1=S_h+2N_D-4N_V,}
\]

\[
\boxed{W_C=N_s+6N_D+12N_V.}
\]

`N_D` may be half-integral when a Weyl field is counted as half a Dirac field. The massless proper-time coefficients are

\[
C_{0,\rm loop}=\frac{\Lambda_{\rm UV}^4}{64\pi^2}W_0,
\qquad
M_*^2=\frac{\Lambda_{\rm UV}^2}{96\pi^2}W_1,
\]

\[
a_C=\frac{L}{1920\pi^2}W_C,
\qquad
a_R=\frac{L}{1152\pi^2}S_{h^2}.
\]

The simultaneous massless gate is therefore

\[
\boxed{W_0=0,\qquad W_1>0.}
\]

## 3. Spectrum theorem and branch tests

For a healthy bosonic primitive spectrum, `N_D=0`, `N_s>0` and `N_V>=0`. Hence

\[
W_0=N_s+2N_V>0.
\]

This proves the one-loop bosonic vacuum-cancellation no-go in the stated regulator and field class. It is stronger than saying that a coefficient is missing: no choice of positive bosonic multiplicities can satisfy the required quartic supertrace.

The Einstein sign gives a second useful condition. For minimally coupled scalars,

\[
W_1=N_s-4N_V.
\]

One public `U(1)` therefore requires at least five real scalar modes for positive induced Einstein stiffness. The explicit branches are:

| branch | `(N_s,N_D,N_V)` | `W0` | `W1` | `WC` |
|---|---:|---:|---:|---:|
| primitive real `psi` | `(1,0,0)` | `1` | `1` | `1` |
| primitive complex `psi` | `(2,0,0)` | `2` | `2` | `2` |
| real `psi` plus public `U(1)` | `(1,0,1)` | `3` | `-3` | `13` |
| complex `psi`, memory scalar, public `U(1)` | `(3,0,1)` | `5` | `-1` | `15` |
| five minimal scalars plus public `U(1)` | `(5,0,1)` | `7` | `1` | `17` |
| imported SM, no right-handed neutrinos | `(4,22.5,12)` | `-62` | `1` | `283` |
| imported SM plus three right-handed neutrinos | `(4,24,12)` | `-68` | `4` | `292` |

The Standard Model rows are external correspondence benchmarks, not primitive MTS spectrum claims. They show that ordinary observed field content can make `W1` positive in this convention but does not select `W0=0`.

The integrated `H` graviton and diffeomorphism ghosts are not included in these matter weights. Their off-shell power-law `C0` and Einstein terms are gauge- and regulator-dependent matching contributions. They must be absorbed into renormalized `C0_R` and `M_R^2`; they cannot be used as unsourced physical species numbers to manufacture a cancellation. Their universal logarithms require a separate gauge-consistent background-field calculation.

## 4. Threshold-rigidity theorem

Checkpoint 4876 exhibited four real scalars and one Dirac field as an algebraic cancellation example. Let

\[
x_i=m_{s_i}^2,
\qquad
a=m_D^2.
\]

Cancellation of the quadratic and logarithmic mass moments requires

\[
\sum_{i=1}^4x_i=4a,
\qquad
\sum_{i=1}^4x_i^2=4a^2.
\]

Then

\[
\sum_{i=1}^4(x_i-a)^2
=\sum_i x_i^2-2a\sum_i x_i+4a^2
=0.
\]

Every term is nonnegative, so

\[
\boxed{x_1=x_2=x_3=x_4=a.}
\]

The cancellation is therefore threshold-rigid. Any mass splitting destroys it unless additional fields or a protecting symmetry repair all spectral moments. The old example proves compatibility only; it does not provide a natural MTS vacuum selector.

## 5. Covariant nonlocal completion

For the healthy massless matter sector, the universal quadratic-curvature terms are

\[
\boxed{
\Gamma_{\rm nl}=-\int d^4x\sqrt{-g}\left[
\frac{W_C}{3840\pi^2}
C_{\mu\nu\rho\sigma}\log\!\left(\frac{-\Box}{\Lambda_{\rm UV}^2}\right)
C^{\mu\nu\rho\sigma}
+\frac{S_{h^2}}{2304\pi^2}
R\log\!\left(\frac{-\Box}{\Lambda_{\rm UV}^2}\right)R
\right].
}
\]

At a local matching scale `mu`, `log(mu^2/LambdaUV^2)=-2L`, reproducing exactly

\[
a_C=\frac{LW_C}{1920\pi^2},
\qquad
a_R=\frac{LS_{h^2}}{1152\pi^2}.
\]

This is why a large infrared logarithm must not be frozen into a global polynomial and interpreted as a literal extra particle. With

\[
x=q/\Lambda_{\rm UV},
\]

the relative magnitudes are

\[
\epsilon_0=\frac{S_{h^2}}{W_1}x^2\ln(1/x),
\qquad
\epsilon_2=\frac{W_C}{5W_1}x^2\ln(1/x).
\]

The kernel obeys

\[
\lim_{x\to0^+}x^2\ln(1/x)=0,
\qquad
\max_{0<x<1}x^2\ln(1/x)=\frac1{2e}.
\]

Thus the universal matter logarithms decouple relative to Einstein gravity in the infrared. A sign-independent pole gate follows from

\[
|1+s_i\epsilon_i|\ge1-|\epsilon_i|.
\]

Whenever `epsilon_i<1`, no real root can occur in that tested domain, irrespective of the continuation sign `s_i`. A theorem over the whole subcutoff interval would require the corresponding weight ratio below `2e`. For the imported-SM anchor, `S_h2/W1=4<2e` closes that scalar interval, while `WC/(5W1)=283/5>2e` does not exclude a spin-2 root near the cutoff. The infrared calculation does not decide near-cutoff roots.

Finite renormalized local `R^2/C^2` coefficients and the omitted `H`/ghost form factors remain independent denominator inputs. The no-root statement here applies only where the complete correction magnitude is actually bounded.

## 6. Newton-matched local hierarchy

After the single Newton calibration

\[
M_R^2=\overline M_{\rm Pl}^2,
\qquad
W_1\Lambda_{\rm UV}^2=96\pi^2\overline M_{\rm Pl}^2,
\]

the universal matter residuals become

\[
\boxed{
\epsilon_0=\frac{S_{h^2}Lq^2}{96\pi^2\overline M_{\rm Pl}^2},
\qquad
\epsilon_2=\frac{W_CLq^2}{480\pi^2\overline M_{\rm Pl}^2}.
}
\]

For the imported-SM anchor `WC=283`, `S_h2=4`, `Mbar_Pl=2.435e27 eV`, and `LambdaUV=Mbar_Pl`, the scale smoke is:

| arena scale | `epsilon0` | `epsilon2` |
|---|---:|---:|
| R10, `50 micrometre` | `7.61e-61` | `1.08e-59` |
| atomic/clock, `1 Angstrom` | `1.54e-49` | `2.18e-48` |
| nuclear, `1 fm` | `1.22e-39` | `1.72e-38` |
| solar PPN, `R_sun` | `5.66e-87` | `8.01e-86` |
| orbital, `1 AU` | `1.29e-91` | `1.83e-90` |
| galaxy, `10 kpc` | `3.66e-110` | `5.18e-109` |

As a deliberately severe hierarchy stress, setting each effective logarithmic weight independently to `10^6` still gives a maximum local residual `3.05e-34`. The smallest weight that would reach `10^-30` in this grid is `3.28e9`. This is not a derived bound on omitted gravity loops; it shows how much coefficient room the Planck-suppressed local hierarchy has.

These numbers test only universal one-loop logarithms. They are not R10, PPN, clock or orbital observable predictions yet because finite local coefficients, source projections and experimental likelihoods have not been inserted.

## 7. Renormalized-vacuum freeze

Because neither the primitive MTS spectrum nor imported observed matter satisfies `W0=0`, the competitive EFT now uses an explicit renormalization condition rather than a fictitious cancellation.

Using the Planck 2018 base-LambdaCDM values `H0=67.4 km s^-1 Mpc^-1` and `Omega_m=0.315` as a declared smoke baseline,

\[
\Lambda_{\rm cal}
=\frac{3(1-\Omega_m)H_0^2}{c^2}
=1.09091\times10^{-52}\ {\rm m}^{-2}.
\]

At one cosmological matching scale `mu0`, freeze

\[
\boxed{C_{0,R}(\mu_0)=-M_R^2\Lambda_{\rm cal}.}
\]

Then

\[
\Lambda_{\rm bg}=\Lambda_{\rm cal}.
\]

This parameter is fixed once. It may not be retuned for R10, PPN, clocks, orbits, galaxies or separate cosmology samples. Threshold and higher-loop sensitivity remain the usual radiative-stability problem; MTS has not solved it.

The background-curvature expansion parameter is

\[
\epsilon_\Lambda=|\Lambda_{\rm cal}|L_{\rm domain}^2.
\]

It equals `2.73e-61` at `50 micrometre`, `4.43e-39` at Earth radius, `2.44e-30` at `1 AU`, `1.04e-9` at `100 kpc`, and `0.104` at `1 Gpc`. The calibrated cosmological curvature is negligible throughout the local and galactic arenas but cannot be dropped in cosmology.

## 8. Arbitration

The spectrum route is not left as another vague target. It has a definite result:

1. **Primitive cancellation:** rejected for the present bosonic corpus at one loop.
2. **Four-scalar/Dirac example:** retained only as a threshold-rigid existence proof.
3. **Imported Standard Model:** useful positive-Einstein benchmark, but nonzero vacuum weight.
4. **Universal nonlocal terms:** derived, retained, and proven infrared-decoupling.
5. **Local arena hierarchy:** extremely small for the universal matter logarithms, but still nonclaim pending complete coefficients and observable projections.
6. **Vacuum:** frozen as one explicit renormalized relevant coupling; not predicted and not called solved.
7. **Local GR branch:** remains viable as an infrared EFT because the positive massless spin-2 pole, universal source coupling, Newton normalization and tiny universal-log hierarchy coexist on the selected integrated-`H` parent.

This is progress toward local GR rather than a retreat: the background is now mathematically legal, the false scalar-only flat saddle is gone, and the local corrections have a covariant momentum-dependent completion. The remaining local question is no longer whether a frozen polynomial pole looks unhealthy; it is whether every finite counterterm and source projection stays below the real arena bounds.

No R10, PPN, clock, orbital, Maxwell, cosmological-constant or full local-GR claim is opened by checkpoint 4877.

## 9. Next target

`4878-Y5-R2FR-renormalized-EFT-local-limit-and-arena-specific-nonlocal-residual-bounds-to-R10-PPN-clocks-orbit-and-Maxwell.md`

The next checkpoint must propagate the single `GN/Lambda_cal` calibration into each local arena, introduce the finite renormalized `R^2/C^2` coefficients as bounded—not silently zero—inputs, derive the actual source-to-observable projections, and compare those residuals with R10, PPN, clock, orbital and Maxwell limits. The imported-SM logarithms are the fixed floor; unknown tree-level MTS operators are the quantities to constrain.

## Sources

- [Vassilevich, Heat kernel expansion: user's manual](https://arxiv.org/abs/hep-th/0306138)
- [Chaichian, Oksanen and Tureanu, Sakharov's induced gravity and the Poincare gauge theory](https://arxiv.org/abs/1805.03148)
- [Ohta and Rachwal, Effective Action from the Functional Renormalization Group](https://arxiv.org/abs/2002.10839)
- [Donoghue and El-Menoufi, Covariant non-local action for massless QED and the curvature expansion](https://arxiv.org/abs/1507.06321)
- [Planck 2018 results VI, cosmological parameters](https://arxiv.org/abs/1807.06209)
- `core-mts-framework/action-principle/the-fundamental-action-of-motion-timespace-field-theory.md`
- `core-mts-framework/field-theory/the-effective-field-theory-of-motion-timespace.md`
- `quantum-particle-field/leptons-neutrinos/finite-lepton-families-from-curvature-memory-geometry.md`
- `quantum-particle-field/leptons-neutrinos/why-neutrinos-are-light-and-mix.md`
- `post-checkpoint-work/4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md`
- `post-checkpoint-work/scripts/Y5_R2FR_4877_spectrum_nonlocal_vacuum.py`
