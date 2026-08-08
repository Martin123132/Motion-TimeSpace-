# 4883 — Tabulated microphysical EOS acquisition and multi-EOS mass-radius-tidal contact response

**Status:** Three source-backed neutron-star EOS families now replace the analytic control polytrope. Hash-locked LALSuite tables for BSK24, SLY4 and DD2 reproduce independent CompOSE maximum-mass and `R_1.4` anchors, all support two-solar-mass stars, and all pass the differentiated MTS contact-response calculation. Forty-eight nonlinear comparisons validate the multi-EOS tangent implementation. The result materially strengthens the selected metric branch's strong-matter correspondence, but remains conditional because `a_R,a_C` are inherited control caps rather than parent-derived or measured Wilson coefficients.

Marker: `MTS_MULTI_EOS_TOV_LOVE_CONTACT_RESPONSE_4883`.

## 1. What this checkpoint changes

Checkpoint 4882 established the TOV/Love response operator on a deliberately simple `Gamma=2` polytrope. Its maximum mass was only `1.637 M_sun`, so it could validate algebra and code but not the strong-matter physics.

Checkpoint 4883 now:

1. acquires independently maintained tabulated EOS data;
2. locks every selected table to a LALSuite commit, blob and SHA-256 digest;
3. audits the two LALSuite table formats and converts both to one geometrized unit convention;
4. reconstructs a smooth barotropic `rho(p)` map with a regular low-pressure surface extension;
5. derives the general barotropic MTS contact image without requiring an explicit baryon-density column;
6. solves and differentiates TOV plus the relativistic `l=2` Love equation for three EOS families;
7. checks maximum masses and canonical radii against CompOSE;
8. validates `48` fixed-central-pressure and fixed-mass derivatives against nonlinear solves;
9. compares the MTS contact envelope with actual EOS spread.

No public strong-matter or full-unification claim is made.

## 2. Data acquisition and provenance

The selected files are taken from the [LVK Algorithm Library Suite](https://git.ligo.org/lscsoft/lalsuite) at commit

```text
a43ed75d9785b825d33b63072e1812f83efae36a
```

| EOS | LALSuite table | blob | SHA-256 | independent anchor |
|---|---|---|---|---|
| BSK24 | `LALSimNeutronStarEOS_PCP_BSK24_BSK24.dat` | `9a96fe386fdb3781f587a172fa86ca4ae2405849` | `78e6047b0a7724b350692b816f0d6181c49341847351e2a9a5e26b940f62aa1d` | [CompOSE BSK24 data sheet](https://compose.obspm.fr/download/1D/NS/Skyrme/BSK24/eos.pdf) |
| SLY4 | `LALSimNeutronStarEOS_SLY4.dat` | `d76a28d52af8c67b8f008cbd455b58e6328a19da` | `475b77304c6da7253699c3cf48ad5a06bb637178f9615267cc0c6e6b41cc0b75` | [CompOSE SLY4 entry](https://compose.obspm.fr/eos/134) |
| DD2 | `LALSimNeutronStarEOS_GPPVA_DD2_BSK24.dat` | `3d07e5426625a050b13a281a99728b62e1d674e1` | `7c9b5b5b3b50219d35e8a302d596b2b08df193cb62c17386cdd969174390d1fe` | [CompOSE DD2 entry](https://compose.obspm.fr/eos/217) |

The local files live under `source-intake/microphysical_eos/4883/lalsuite`. The corresponding LALSuite parser source is also hash-locked locally.

The first direct CompOSE archive acquisition was not silently trusted. Its published archive checksums match for BSK24 but not for the downloaded APR and SLY4 ZIP payloads. Those archives are retained as a provenance audit and explicitly quarantined from the solver. The selected LALSuite files independently pass their repository content hashes.

## 3. Unit and table-format audit

The LALSuite parser has two paths:

- legacy two-column tables supply pressure and energy directly to the geometrized internal arrays;
- modern nine-column tables convert mass density and pressure from CGS using `G/c^2` and `G/c^4`.

All values are converted to

```text
[rho]=[p]=L_sun^-2,
L_sun=GM_sun/c^2=1476.669691 m.
```

The legacy source comment labels the two columns as SI, while the numerical magnitudes and direct internal assignment are geometrized. Rather than choosing by assertion, this checkpoint uses recovery of the independent CompOSE `Mmax` and `R_1.4` values as a unit regression. The sub-percent agreement below resolves the operational convention.

The table interpolation is cubic in `ln rho(ln p)`. All sampled derivatives are positive on the used domain. Any first acausal point is located, and the stable sequence is restricted below it. The low-pressure extension follows the LALSuite nonrelativistic surface law

\[
\rho\propto p^{3/5}.
\]

The regular surface coordinate

\[
q=p^{2/5}
\]

makes the low-density TOV endpoint finite. The baseline surface is `q_s=10^-7 q_min`; comparison with `10^-9 q_min` changes radius by at most `1.22e-12` fractionally and tidal deformability by at most `1.40e-13`.

## 4. General barotropic contact derivation

For a cold zero-temperature barotrope, the first law gives

\[
n\frac{d\rho}{dn}=\rho+p.
\]

Therefore the pressure image of any contact basis `f_A(rho,p(rho))` can be written without explicitly reconstructing `n`:

\[
D_A=n\frac{df_A}{dn}-f_A
=(\rho+p)\frac{df_A}{d\rho}-f_A.
\]

In the regular coordinate `q`, this is

\[
\boxed{D_A=(\rho+p)\frac{f_{A,q}}{\rho_{,q}}-f_A.}
\]

The two inherited directions are

\[
f_R=(\rho-3p)^2,
\qquad
f_C=4\rho(\rho/3+p).
\]

The effective EOS is

\[
\rho_{\rm eff}=\rho-\lambda_Rf_R-\lambda_Cf_C,
\]

\[
p_{\rm eff}=p-\lambda_RD_R-\lambda_CD_C.
\]

The evolved table coordinate obeys

\[
q'=\frac{p_{\rm eff}'}{p_{{\rm eff},q}},
\qquad
c_{s,{\rm eff}}^2=\frac{p_{{\rm eff},q}}{\rho_{{\rm eff},q}}.
\]

This is the exact first-order barotropic completion of the checkpoint-4881 conserved-current contact map.

## 5. Tangents, moving surface and fixed mass

For `Y=(m,q,y)`, each contact tangent still satisfies

\[
Z_A'=J_YZ_A+s_A.
\]

At the finite numerical surface event,

\[
R_A=-\frac{(Z_A)_q}{q'_s},
\]

\[
M_A=(Z_A)_m+m'_sR_A,
\qquad
(y_R)_A=(Z_A)_y+y'_sR_A.
\]

The `m'_sR_A` term is retained even though the converged surface density is negligible. At fixed observed mass,

\[
O_A|_M=O_A-O_q\frac{M_A}{M_q}.
\]

The pressure-parameterized turning condition is

\[
\kappa_{\rm turn,p}=\left|\frac{d\ln M}{d\ln p_c}\right|^{-1}.
\]

## 6. Independent mass-radius regression

| EOS | calculated `Mmax/M_sun` | source value | calculated `R(Mmax)` km | calculated `R_1.4` km | source `R_1.4` km |
|---|---:|---:|---:|---:|---:|
| BSK24 | 2.27952 | 2.28 | 11.0787 | 12.5770 | 12.57 |
| SLY4 | 2.04899 | 2.06 | 9.9932 | 11.7246 | 11.70 |
| DD2 | 2.41808 | 2.42 | 11.8829 | 13.1973 | 13.19 |

The largest maximum-mass discrepancy is `0.535%`; the largest canonical-radius discrepancy is `0.210%`. All three EOS families support `2 M_sun`.

## 7. Canonical and high-mass response results

At `1.4 M_sun`:

| EOS | radius km | `Lambda_T` | `kappa_turn,p` | cap `|delta R|/R` at fixed mass | cap `|delta Lambda_T|/Lambda_T` |
|---|---:|---:|---:|---:|---:|
| BSK24 | 12.5770 | 516.832 | 2.268 | 6.72e-19 | 3.05e-18 |
| SLY4 | 11.7246 | 297.193 | 2.768 | 8.77e-19 | 4.62e-18 |
| DD2 | 13.1973 | 686.697 | 2.065 | 6.06e-19 | 2.56e-18 |

At `0.99 Mmax`, `kappa_turn,p` rises to `18.21–20.33`. The largest fixed-mass tidal cap across all nine rows is

\[
\boxed{3.039\times10^{-17}}.
\]

The turning-point amplification is present and has not been hidden, but the inherited contact envelope remains tiny throughout the accepted stable rows.

## 8. Nonlinear validation

For every EOS, both contact directions are compared against nonlinear centered solves at:

- fixed central pressure: mass, radius, `k2`, `Lambda_T`;
- fixed observed mass: central coordinate, radius, `k2`, `Lambda_T`.

This gives `3 x 2 x 8 = 48` checks. Every row passes, with maximum relative discrepancy

\[
\boxed{6.007\times10^{-3}}.
\]

The amplified validation step is `0.4 L_sun^2`; its largest `lambda rho_c` is `6.39e-4`, so it resolves the derivative while remaining in the linear regime. It is not interpreted as a physical curvature coefficient.

## 9. EOS spread versus MTS contact envelope

Across the three `1.4 M_sun` models:

\[
R_{1.4}=11.7246\text{--}13.1973\ {\rm km},
\]

\[
\Lambda_{1.4}=297.19\text{--}686.70.
\]

The fractional EOS spreads are `0.1178` in radius and `0.7786` in tidal deformability. They exceed the maximum canonical MTS contact caps by factors

\[
1.34\times10^{17}
\quad\text{and}\quad
1.68\times10^{17},
\]

respectively.

This is not a failure signal. On the selected metric-only strict-EFT branch, the derived contact sector is supposed to reduce to GR plus an extremely small EOS renormalization under the inherited caps. The result says the implementation survives realistic strong matter and that ordinary EOS uncertainty dominates it overwhelmingly.

## 10. Decision and next target

Checkpoint 4883 closes the specific defect left by 4882: the result is no longer tied to an under-massive analytic polytrope. The selected metric branch now has a realistic, multi-EOS, mass-radius-tidal strong-matter correspondence calculation.

The remaining theory question is no longer whether the response can be computed. It is whether `a_R,a_C` are:

1. derived from the MTS parent spectrum/action;
2. constrained directly as Wilson coefficients by compact-star observations; or
3. retained only as conservative EFT-control caps.

Claim guards:

- Do not call the validation step a physical coupling.
- Do not treat EOS spread as an MTS residual.
- Do not cross the maximum-mass turning point.
- Do not use the quarantined checksum-mismatched archives in a claim.
- Do not call control caps measured or parent-derived coefficients.
- Do not promote the selected metric branch result to every MTS branch or to full unification.

Decision:

`THREE_HASH_LOCKED_MICROPHYSICAL_EOS_FAMILIES_PASS_2MSUN_AND_SOURCE_MASS_RADIUS_REGRESSION; MULTI_EOS_TOV_LOVE_CONTACT_TANGENTS_PASS_48_NONLINEAR_CHECKS; EOS_SPREAD_DOMINATES_INHERITED_CONTACT_CAPS_BY_1E17; SELECTED_METRIC_STRONG_MATTER_GR_CORRESPONDENCE_SUPPORTED_CONDITIONALLY; PARENT_CONTACT_COEFFICIENT_OWNERSHIP_STILL_OPEN`.

Next target:

`4884-Y5-R2FR-strong-matter-contact-coefficient-parent-ownership-or-observational-bound-projection-gate.md`

