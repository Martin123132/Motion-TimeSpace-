# 4881 Y5 R2FR compact-fluid EOS/TOV map and dimension-six owner gate

**Status:** Two missing derivations are advanced. First, the finite local `R^2/C^2` self-contact is reduced exactly on an off-shell barotropic perfect-fluid action. It renormalizes the EOS and feeds the ordinary GR TOV equations without introducing a new gravitational differential operator. Second, the checkpoint-4876 scalar determinant is extended to the exact Ricci-flat heat-kernel `a6` tensor. Its massive-loop spectral moment and strong-field hierarchy are derived. The total dimension-six coefficient is not claimed because the existing parent declares neither bare six-derivative matching nor the complete massive signed spectrum.

Marker: `MTS_COMPACT_FLUID_TOV_AND_SCALAR_A6_OWNER_4881`.

## 1. Why this is not another missing-input audit

Checkpoint 4880 routed compact matter and the first nonredundant vacuum operator to separate gates. This checkpoint calculates both gates as far as the existing parent permits:

- the compact-fluid contact functional is simplified exactly;
- its effective energy, pressure, sound-speed and TOV map are derived;
- causal-fluid coefficient envelopes are proved analytically;
- the true profile-dependent direct mass bound is written down;
- the scalar `a6` tensor is read from the same proper-time determinant already adopted at checkpoint 4876;
- the massive spectral moment is integrated exactly;
- the massless-local-`c6` route is rejected in favour of the existing nonlocal branch;
- the remaining total-`c6` gap is localized to bare matching and unsummed spin/mass data.

## 2. Exact perfect-fluid contact image

Use signature `(-,+,+,+)` and

\[
T_{\mu\nu}=(\rho+p)u_\mu u_\nu+pg_{\mu\nu},
\qquad
u_\mu u^\mu=-1.
\]

Then

\[
T_{\mu\nu}T^{\mu\nu}=\rho^2+3p^2,
\qquad
T=-\rho+3p.
\]

The checkpoint-4879 contact numerator is

\[
F=2a_C T_{\mu\nu}T^{\mu\nu}
+\left(a_R-\frac23a_C\right)T^2.
\]

Direct expansion gives the useful exact cancellation

\[
\boxed{
F(\rho,p)
=a_R(\rho-3p)^2
+4a_C\rho\left(\frac{\rho}{3}+p\right).
}
\]

The `R^2` piece couples only to the squared trace. The `C^2` contact image has no independent `p^2` term after the four-dimensional basis conversion.

For `p=w rho`,

\[
\frac{F}{\rho^2}
=a_R(1-3w)^2+4a_C\left(w+\frac13\right).
\]

Radiation therefore removes the `a_R` term but retains `8a_C/3`; dust gives `a_R+4a_C/3`.

## 3. Off-shell fluid action and effective EOS

To avoid the known ambiguity between on-shell shorthands such as `L_m=p` and `L_m=-rho`, use a conserved-current perfect-fluid action with a parent EOS `rho(n)`, as in [Brown's relativistic fluid construction](https://arxiv.org/abs/gr-qc/9304026):

\[
S_{\rm fluid}
=-\int\sqrt{-g}\,\rho(n)
+\frac1{\overline M_{\rm Pl}^4}
\int\sqrt{-g}\,F[\rho(n),p(n)].
\]

The thermodynamic identities are

\[
p=n\frac{d\rho}{dn}-\rho,
\qquad
\frac{d\rho}{dn}=\frac{\rho+p}{n},
\qquad
c_s^2=\frac{dp}{d\rho}.
\]

Writing the complete action again as `-int sqrt(-g) rho_eff(n)` gives

\[
\boxed{
\rho_{\rm eff}=\rho-\frac{F}{\overline M_{\rm Pl}^4},
}
\]

\[
\boxed{
p_{\rm eff}=p-\frac{D}{\overline M_{\rm Pl}^4},
\qquad
D=(\rho+p)(F_{,\rho}+c_s^2F_{,p})-F.
}
\]

For constant `w`, where `c_s^2=w`, the pressure numerator obeys the exact identity

\[
\boxed{D=(1+2w)F.}
\]

The effective sound speed is

\[
c_{s,{\rm eff}}^2
=\frac{p_{,n}-nF_{,nn}/\overline M_{\rm Pl}^4}
{\rho_{,n}-F_{,n}/\overline M_{\rm Pl}^4}.
\]

Thus stability and causality can be checked directly once an EOS is specified; they are not assumed from the uncorrected EOS.

## 4. Corrected compact-star equations

In geometrized units `G=c=1`, solve the standard TOV system for the effective EOS:

\[
\boxed{
\frac{dm}{dr}=4\pi r^2\rho_{\rm eff},
}
\]

\[
\boxed{
\frac{dp_{\rm eff}}{dr}
=-\frac{(\rho_{\rm eff}+p_{\rm eff})
(m+4\pi r^3p_{\rm eff})}{r(r-2m)}.
}
\]

Equivalently,

\[
\frac{dn}{dr}
=\left(\frac{dp_{\rm eff}}{dn}\right)^{-1}
\frac{dp_{\rm eff}}{dr}.
\]

The center conditions are `m(0)=0`, `n(0)=n_c` and regularity. The surface satisfies `p_eff(R)=0`. A self-bound density jump requires the corresponding surface action rather than silently integrating by parts across a discontinuity.

At first strict-EFT order this proves an **EOS-redundancy theorem**:

\[
\boxed{
R^2/C^2\ \text{perfect-fluid self-contact}
\Longleftrightarrow
\text{local EOS renormalization plus local metric map}.
}
\]

No new fourth-order stellar differential equation remains after the legitimate field redefinition. In the exterior `R_mn=R=0`, the metric redefinition vanishes, so the public exterior is the same Schwarzschild metric with matched ADM mass and multipoles.

This also explains the empirical limitation: if the EOS is fitted freely, the contact correction is absorbed into it. A gravity test needs independent microphysical EOS information.

## 5. Causal-fluid contact envelopes

The checkpoint-4878 derivative-control caps obey exactly

\[
|a_C|_{\rm cap}=3|a_R|_{\rm cap}.
\]

For

\[
0\le w=\frac p\rho\le1,
\qquad
0\le c_s^2\le1,
\]

the energy numerator satisfies

\[
\frac{|F|}{\rho^2}
\le |a_R|_{\rm cap}
\left[(1-3w)^2+12\left(w+\frac13\right)\right]
\le20|a_R|_{\rm cap}.
\]

For the pressure numerator,

\[
D_R=(3w-1)(6c_s^2w+6c_s^2-5w-1),
\]

\[
D_C=\frac43(3c_s^2w+3c_s^2+3w^2+2w+1).
\]

On the unit square, `|D_R|<=12` and `D_C<=16`, with both extrema attained at `w=c_s^2=1`. Hence

\[
\boxed{
\frac{|D|}{\rho^2}
\le12|a_R|_{\rm cap}+16|a_C|_{\rm cap}
=60|a_R|_{\rm cap}.
}
\]

Define the dimensionless local density scale

\[
x_\rho=\bar\ell_P^2\frac{8\pi G\rho_{\rm mass}}{c^2}.
\]

The resulting **uniform-mean-density benchmarks** are:

| system | mean density (`kg m^-3`) | `|delta rho|/rho` | `|delta p|/rho` |
|---|---:|---:|---:|
| Earth | `5.513e3` | `4.637e-33` | `1.391e-32` |
| Sun | `1.410e3` | `1.186e-33` | `3.558e-33` |
| `1 Msun`, `7000 km` white dwarf | `1.384e9` | `1.164e-27` | `3.492e-27` |
| `1.4 Msun`, `12 km` neutron star | `3.846e17` | `3.235e-19` | `9.705e-19` |

These are not profile bounds. A mean density does not upper-bound `int rho^2/int rho`. The rigorous direct fixed-profile mass formula is

\[
\boxed{
\frac{|\delta M_{\rm direct}|}{M}
\le20|a_R|_{\rm cap}\bar\ell_P^2\frac{8\pi G}{c^2}
\frac{\int\rho_{\rm mass}^2dV}
{\int\rho_{\rm mass}dV}.
}
\]

A real numerical mass bound therefore needs a density profile or `rho_max`. Radius, tidal and sensitivity shifts additionally require the stable-branch TOV response Jacobian and can be enhanced near a maximum-mass turning point.

## 6. Exact scalar `a6` owner

Checkpoint 4876 already adopts the public-metric scalar operator

\[
D=-\Box+\xi R+m^2
\]

and its covariant proper-time determinant. The next heat-kernel coefficient is therefore part of that same parent calculation, not an unrelated ansatz.

The original arXiv source for [Vassilevich's heat-kernel review](https://arxiv.org/abs/hep-th/0306138) was acquired and hash-locked locally. On a Ricci-flat scalar background, `R=R_mn=E=Omega_mn=0`, its no-boundary `a6` tensor reduces before integration by parts to

\[
\boxed{
A_6^{\rm RF}=\frac1{7!}\left[
9(\nabla R_{\mu\nu\rho\sigma})^2
+12R_{\mu\nu\rho\sigma}\Box R^{\mu\nu\rho\sigma}
-\frac{44}{9}I_1-\frac{80}{9}I_2
\right],
}
\]

where

\[
I_1=R_{ij kn}R_{ij lp}R_{kn lp},
\qquad
I_2=R_{ij kn}R_{il kp}R_{jl np}.
\]

The raw absolute operator-norm coefficient is

\[
\boxed{
C_{A_6}=\frac{313}{45360}=0.00690035\ldots.
}
\]

For a massive scalar,

\[
\int_{\Lambda_{\rm UV}^{-2}}^\infty
ds\,e^{-m^2s}
=\frac{e^{-m^2/\Lambda_{\rm UV}^2}}{m^2}.
\]

Therefore the scalar loop has magnitude

\[
\boxed{
\Gamma_6^{(s)}
=\frac{N_s e^{-m^2/\Lambda_{\rm UV}^2}}
{32\pi^2m^2}
\int\sqrt{-g}\,A_6^{\rm RF},
}
\]

up to the common Euclidean/Lorentzian sign convention already fixed in checkpoint 4876.

Using the checkpoint-4876 scalar-anchor Newton match including its finite-mass term,

\[
\overline M_{\rm Pl}^2
=\frac{N_sh\Lambda_{\rm UV}^2}{96\pi^2}
(1-\delta_{\rm EH}),
\qquad
h=1-6\xi,
\qquad
\delta_{\rm EH}=2L\frac{m^2}{\Lambda_{\rm UV}^2},
\]

eliminates `N_s`:

\[
\boxed{
\frac{2\zeta_6}{\overline M_{\rm Pl}^2}
=\frac{6e^{-m^2/\Lambda_{\rm UV}^2}}
{h(1-\delta_{\rm EH})m^2\Lambda_{\rm UV}^2}.
}
\]

## 7. Scalar strong-field hierarchy

With invariant curvature momentum `q_K`, the complete raw Ricci-flat scalar envelope is

\[
\boxed{
\epsilon_6^{(s)}
\le\frac{6C_{A_6}}{h(1-\delta_{\rm EH})}
e^{-m^2/\Lambda_{\rm UV}^2}
\left(\frac{q_K}{m}\right)^2
\left(\frac{q_K}{\Lambda_{\rm UV}}\right)^2.
}
\]

For the declared local hierarchy

\[
h\ge0.1,
\qquad
q_K/m\le0.1,
\qquad
q_K/\Lambda_{\rm UV}\le0.1,
\qquad
0\le\delta_{\rm EH}\le0.01,
\]

one obtains

\[
\boxed{
\epsilon_6^{(s)}<4.18204\times10^{-5}.
}
\]

The corresponding sufficient length conditions are:

| system | `q_K` (`m^-1`) | max scalar Compton length | max UV cutoff length | scalar `epsilon6` envelope |
|---|---:|---:|---:|---:|
| `1.4 Msun`, `12 km` neutron star | `9.104e-5` | `1.098 km` | `1.098 km` | `4.182e-5` |
| `10 Msun` Schwarzschild horizon | `6.302e-5` | `1.587 km` | `1.587 km` | `4.182e-5` |

This is a derived scalar-loop hierarchy, not the total MTS dimension-six coefficient.

## 8. Why a massless scalar is not a local `c6`

As `m->0`, the proper-time moment `1/m^2` diverges in the infrared. The local derivative expansion has failed; it is not evidence for an infinite physical Wilson coefficient. The primitive massless scalar must remain in the nonlocal curvature-form-factor branch already derived at checkpoint 4877.

The total owner equation is instead

\[
\boxed{
b_{6j}^{\rm total}
=b_{6j}^{\rm bare}
+\sum_i\frac{\sigma_i n_i}{32\pi^2m_i^2}
A_{6j}^{(i)}e^{-m_i^2/\Lambda_{\rm UV}^2}.
}
\]

The current parent supplies the scalar `A6` tensor but not:

- bare dimension-six matching coefficients;
- an MTS-owned massive spectrum and mass gap;
- fermion, vector, ghost and graviton `a6` weights;
- a strong-field nonlocal kernel for massless modes.

Thus `c6` is no longer an undefined symbol: its exact bare-plus-spectral owner is known, and one nontrivial component has been calculated. The total is not set to zero.

## 9. Promotion decision

The compact-matter advance is

`EXACT_CONTACT_TO_EFFECTIVE_EOS_AND_STANDARD_TOV_MAP_DERIVED`.

The scalar dimension-six advance is

`MASSIVE_SCALAR_A6_KERNEL_AND_NEWTON_MATCHED_HIERARCHY_BOUND_DERIVED`.

The following remain withheld:

- a parameter-free mass-radius or tidal prediction;
- a strong-matter GR promotion near stability turning points;
- the total parent-owned `c6`;
- charged electrovac, full perturbations, flow and full unification.

## 10. Claim guards and next target

- Do not use the on-shell `L_m=p` shortcut to vary the contact action.
- Do not call an EOS redefinition a new exterior fifth force.
- Do not call the uniform-mean-density table a profile bound.
- Do not infer a radius or tidal bound without the TOV response Jacobian.
- Do not use the local massive `a6` formula for a massless mode.
- Do not discard bare dimension-six matching or unsummed spin sectors.
- Do not identify the scalar-loop hierarchy with the total MTS `c6`.

Decision:

`PERFECT_FLUID_CONTACT_REDUCED_EXACTLY; EFFECTIVE_EOS_AND_TOV_MAP_DERIVED; EXTERIOR_METRIC_MAP_VANISHES; CAUSAL_LOCAL_COEFFICIENT_ENVELOPES_PROVED; PROFILE_MASS_BOUND_FORMULA_DERIVED; MASSIVE_SCALAR_RICCI_FLAT_A6_AND_HIERARCHY_DERIVED; MASSLESS_ROUTE_NONLOCAL; TOTAL_C6_AND_PARAMETER_FREE_COMPACT_STAR_PROMOTION_WITHHELD`.

Next target:

`4882-Y5-R2FR-compact-star-EOS-response-Jacobian-mass-radius-and-tidal-sensitivity-or-strong-matter-promotion-gate.md`
