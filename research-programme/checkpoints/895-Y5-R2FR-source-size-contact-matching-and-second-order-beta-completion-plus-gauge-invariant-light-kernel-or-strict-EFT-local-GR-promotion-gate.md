# 4879 Y5 R2FR finite-source contact matching, beta completion and physical light-clock kernels

**Status:** The selected metric-only strict-EFT branch now has a private conditional classical local-GR certificate through 1PN for weak, separated, minimally coupled sources. A concrete field redefinition maps finite local `R^2/C^2` operators to stress-tensor contact operators. Their interbody cross term vanishes for positively separated finite source supports, while self terms renormalize measured body parameters. The long-range two-source amplitudes therefore remain Einstein-Hilbert, giving operational `gamma=beta=1`. The classical one- and two-PM photon bending terms equal GR. Physical quantum light and point-clock kernels are inserted without using an incomplete off-shell metric, and remain enormously below Cassini and Galileo sensitivity. This does not promote strong-field GR, primitive MTS ownership of the metric/Diff parent, or the full unified theory.

Marker: `MTS_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879`.

## 1. Why this checkpoint can advance rather than list another coefficient

Checkpoint 4878 proved that finite local curvature-squared terms have contact support in the linear exterior potential. The remaining questions were whether finite material sources reintroduce a force, whether the nonlinear `U^2` coefficient differs from GR, and whether the gravity-loop light and clock projections can be made physical.

The decisive external theorem is stronger than the linear result. [Accettulli Huber et al.](https://arxiv.org/abs/1911.10108) show that, in strict EFT, pure-graviton amplitudes and amplitudes with two minimally coupled heavy scalars and any number of external gravitons are unchanged by curvature-squared interactions. The field redefinition leaves only local interactions with four or more source fields. Long-range classical and quantum two-body potentials receive no `R^2/R_{mu nu}^2` correction.

That theorem is used here together with an explicit stress-tensor matching calculation, not merely cited as an analogy.

## 2. Exact four-dimensional field redefinition

Start from

\[
S=\int d^4x\sqrt{-g}\left[
\frac{\overline M_{\rm Pl}^2}{2}R
+a_RR^2+a_CC_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma}
\right]+S_m[g,\Psi].
\]

In four dimensions,

\[
C^2=E_4+2R_{\mu\nu}R^{\mu\nu}-\frac23R^2,
\]

so, up to the topological Euler density,

\[
a_RR^2+a_CC^2
=aR_b R^2+bR_{\mu\nu}R^{\mu\nu},
\]

with

\[
aR_b=a_R-\frac23a_C,
\qquad
b=2a_C.
\]

Define the local inverse-metric redefinition

\[
\boxed{
\delta g^{\mu\nu}
=\frac{-2bR^{\mu\nu}+(2aR_b+b)g^{\mu\nu}R}
{\overline M_{\rm Pl}^2}
=\frac{-4a_CR^{\mu\nu}+(2a_R+2a_C/3)g^{\mu\nu}R}
{\overline M_{\rm Pl}^2}.
}
\]

Using

\[
G_{\mu\nu}R^{\mu\nu}=R_{\mu\nu}R^{\mu\nu}-\frac12R^2,
\qquad
G^\mu{}_{\mu}=-R,
\]

the Einstein-Hilbert variation is exactly

\[
\delta S_{\rm EH}
=-\int\sqrt{-g}\left[
aR_bR^2+bR_{\mu\nu}R^{\mu\nu}
\right].
\]

Thus the finite local curvature-squared action is removed at first strict-EFT order.

## 3. Matter-contact image and finite-source theorem

With

\[
T_{\mu\nu}=-\frac{2}{\sqrt{-g}}\frac{\delta S_m}{\delta g^{\mu\nu}},
\]

the matter variation is

\[
\delta S_m
=\int\sqrt{-g}\left[
\frac{b}{\overline M_{\rm Pl}^2}T_{\mu\nu}R^{\mu\nu}
-\frac{2aR_b+b}{2\overline M_{\rm Pl}^2}TR
\right].
\]

Using the leading Einstein equation

\[
\overline M_{\rm Pl}^2G_{\mu\nu}=T_{\mu\nu},
\]

gives

\[
R=-\frac{T}{\overline M_{\rm Pl}^2},
\qquad
R_{\mu\nu}=\frac{T_{\mu\nu}-g_{\mu\nu}T/2}
{\overline M_{\rm Pl}^2}.
\]

Therefore

\[
\boxed{
\Delta S_{\rm contact}
=\frac1{\overline M_{\rm Pl}^4}
\int\sqrt{-g}\left[
2a_CT_{\mu\nu}T^{\mu\nu}
+\left(a_R-\frac23a_C\right)T^2
\right].
}
\]

For two finite bodies,

\[
T_{\mu\nu}=T^A_{\mu\nu}+T^B_{\mu\nu},
\]

and the cross-contact density is

\[
\boxed{
\overline M_{\rm Pl}^4\mathcal L_{AB}
=4a_CT^A_{\mu\nu}T_B^{\mu\nu}
+2\left(a_R-\frac23a_C\right)T_AT_B.
}
\]

If

\[
\operatorname{supp}(T_A)\cap\operatorname{supp}(T_B)=\varnothing
\]

with a positive gap, both products vanish pointwise. Derivatives and ideal surface distributions remain supported in each body's closure, so their cross products also vanish for positively separated supports.

Hence

\[
\boxed{
\Delta S^{AB}_{\rm contact}=0,
\qquad
F^{AB}_{R^2,C^2}=0
}
\]

at first strict-EFT order.

The `AA` and `BB` pieces are not discarded. They renormalize each body's mass, internal energy, radius-sensitive worldline coefficients and higher multipoles. Once the observed inertial/Kepler mass and multipoles are used, they are not an additional interbody force.

For R10, the detector, attractor and intervening shield have separated material supports. No extended-apparatus convolution can turn this local contact term into a force across the vacuum gap. Only the genuinely nonlocal `r^-3` kernels from checkpoint 4878 require an apparatus convolution, and their point-separation envelope is already below the percent-level scale by roughly `58` orders of magnitude.

## 4. Nonlinear PPN beta completion

In the standard operational PPN expansion,

\[
g_{00}=-1+2U-2\beta U^2+O(v^6),
\qquad
g_{ij}=(1+2\gamma U)\delta_{ij}+O(v^4).
\]

The two-heavy-source/any-graviton amplitude theorem fixes every long-range classical interaction generated by finite local `R^2/C^2` to the Einstein-Hilbert value. The only additional source operators are self/contact terms, whose cross contribution has just been proven zero.

It follows operationally that

\[
\boxed{
\gamma_{\rm classical}=1,
\qquad
\beta_{\rm classical}=1,
\qquad
\delta\gamma_{R^2,C^2}=\delta\beta_{R^2,C^2}=0
}
\]

for the selected strict-EFT branch and stated source class.

The `r^-3` loop tails are proportional to `hbar`; they are scale-dependent post-PPN corrections, not a constant classical shift of `beta`.

The [MESSENGER Mercury result](https://www.osti.gov/biblio/22863119) gives

\[
\beta-1=(-2.7\pm3.9)\times10^{-5}.
\]

The strict-EFT prediction `beta-1=0` lies `0.692 sigma` from its central value. This is a genuine baseline comparison, not a fitted MTS coefficient.

## 5. Physical point-clock monopole kernel

An incomplete off-shell quantum metric is not used. [Kirilin's reparametrization analysis](https://arxiv.org/abs/gr-qc/0601020) shows why a subset of metric diagrams cannot by itself define a physical quantum correction.

Instead use the complete physical heavy-heavy scattering potential from [Bjerrum-Bohr, Donoghue and Holstein](https://arxiv.org/abs/hep-th/0211072). Its universal quantum monopole coefficient is

\[
\eta_{\rm grav}=\frac{41}{10\pi}\ell_P^2
=3.40921005\times10^{-70}\ {\rm m}^2.
\]

For minimally coupled clock levels `E_n=m_n c^2`, the long-range source interaction is proportional to `m_n`. Taking the transition difference therefore gives the same physical monopole potential per unit transition rest energy. Combined without cancellation with the imported-matter temporal-potential coefficient,

\[
\eta_{\rm clock}
=\eta_\Phi+\eta_{\rm grav}
=8.73090378\times10^{-70}\ {\rm m}^2.
\]

The redshift-deviation parameter between radii `r1` and `r2` is

\[
|\alpha_{\rm clock}|
\le\eta_{\rm clock}\left(
\frac1{r_1^2}+\frac1{r_1r_2}+\frac1{r_2^2}
\right).
\]

For `r1=6.371e6 m` and `r2=2.960e7 m`,

\[
\boxed{|\alpha_{\rm clock}|=2.71364\times10^{-83}.}
\]

The [Galileo result](https://arxiv.org/abs/1906.06161) has `1 sigma` uncertainty `2.48e-5`, leaving a margin of `9.14e77`.

This closes the minimal point-clock monopole. Spin, tidal polarizability and apparatus-specific composite operators remain separate finite-size corrections; they are not silently set to zero.

## 6. Physical photon eikonal kernel

The on-shell photon result is taken from [Bending of Light in Quantum Gravity](https://arxiv.org/abs/1410.7590) and its detailed [light-like eikonal treatment](https://arxiv.org/abs/1609.07477), not inferred from a gauge-dependent metric component.

For a photon passing a mass `M` at invariant impact parameter `b`,

\[
\theta_\gamma
=\frac{4GM}{c^2b}
+\frac{15\pi}{4}\left(\frac{GM}{c^2b}\right)^2
+\frac{-26/15-48\ln[b/(2b_0)]}{\pi}
\frac{G^2M\hbar}{c^5b^3}+\cdots.
\]

The first two terms are exactly the GR one- and two-PM predictions. The photon bubble coefficient is

\[
b_u^\gamma=-\frac{161}{120},
\]

while a massless scalar has `b_u^phi=3/40`.

The absolute quantum term depends on the infrared/detector-resolution scale `b0`. This is retained rather than hidden. A deliberately extreme declared envelope

\[
\left|\ln\frac{b}{2b_0}\right|\le100
\]

gives, for `b=1.6 R_sun`,

\[
|\delta\theta_{\rm grav,q}|<4.27489\times10^{-91}\ {m rad}.
\]

The imported-matter metric tail contributes

\[
|\delta\theta_{\rm matter}|=3.43846\times10^{-93}\ {m rad},
\]

so the no-cancellation total is

\[
|\delta\theta_{\rm total}|<4.30928\times10^{-91}\ {m rad}.
\]

Relative to the classical angle `5.30642e-6 rad`, the deflection-equivalent PPN comparator is

\[
\boxed{|\gamma-1|_{\rm eq}<1.62418\times10^{-85},}
\]

more than `80` orders below the Cassini `2.3e-5` uncertainty anchor.

The infrared-independent photon-minus-scalar difference is also explicit:

\[
\theta_\gamma-\theta_\phi
=-\frac{34}{3\pi}\frac{G^2M\hbar}{c^5b^3}
=-1.00899\times10^{-93}\ {m rad}
\]

at the same impact parameter.

## 7. Private conditional local-GR certificate

The selected branch now passes the following weak-field gates:

| gate | result |
|---|---|
| physical positive massless spin-2 pole with Diff Ward identity | inherited PASS from 4875 |
| one measured Newton normalization | PASS |
| finite separated-source `R^2/C^2` cross force | exactly zero at first strict-EFT order |
| Newton/Poisson exterior limit | GR |
| classical `gamma` | `1` |
| classical `beta` | `1` |
| classical photon bending through two PM | GR |
| minimal point-clock monopole | GR plus `2.71e-83` quantum-EFT envelope |
| minimal Maxwell and Hilbert/Poynting source | exact inherited PASS |
| quantum light comparator | below Cassini by `1.42e80` |

Therefore

\[
\boxed{
\text{selected strict-EFT metric-only branch}
\Longrightarrow
\text{classical local GR through 1PN}
}
\]

for four-dimensional weak fields, minimally coupled sources with disjoint supports, and momenta below the EFT cutoff.

This is a **private conditional local-GR certificate**, not a public claim that the whole MTS research programme has derived GR from motion alone.

## 8. Scope guards

The certificate does not include:

- strong-field or all-orders compact-body equivalence;
- primitive derivation of the integrated principal density `H` and Diff symmetry from only motion, time and space;
- primitive ownership of the imported Standard Model loop spectrum;
- the optional nonminimal flow/aether extension;
- curvature-cubed and higher independent operators;
- overlapping-source contact experiments;
- composite-clock spin, polarizability or material-response operators.

No result from those sectors is being smuggled into the local certificate.

## 9. Claim guards

- Do not interpret the field redefinition as `a_R=a_C=0`.
- Do not discard self-contact terms; absorb them only into measured source/worldline coefficients.
- Do not extend the disjoint-support theorem to overlapping matter.
- Do not call quantum `r^-3` tails a constant PPN `beta` shift.
- Do not use the incomplete harmonic-gauge quantum metric as a physical clock prediction.
- Do not remove the photon infrared-resolution scale; declare or marginalize it.
- Do not call a deflection-equivalent `gamma` an exact Cassini radio likelihood.
- Do not extend the certificate to strong fields, nonminimal flow operators or the full fundamental theory.

## 10. Decision and next target

Decision:

`FINITE_SOURCE_CONTACT_IMAGE_DERIVED; DISJOINT_CROSS_FORCE_ZERO; OPERATIONAL_CLASSICAL_GAMMA_BETA_EQUAL_ONE; PHYSICAL_CLOCK_MONOPOLE_AND_PHOTON_EIKONAL_KERNELS_INSERTED; QUANTUM_RESIDUALS_NEGLIGIBLE; SELECTED_METRIC_ONLY_STRICT_EFT_BRANCH_PROMOTED_TO_PRIVATE_CONDITIONAL_CLASSICAL_LOCAL_GR_1PN_CERTIFICATE`.

Next target:

`4880-Y5-R2FR-selected-metric-branch-local-GR-certificate-domain-of-validity-and-strong-field-entry-gate.md`
