# 4880 Y5 R2FR selected-metric local-GR domain and strong-field entry gate

**Status:** A substantive strong-field advance is derived. Every four-dimensional Einstein metric is an exact common solution of Einstein-Hilbert gravity plus finite local `R^2` and `C^2` terms. Therefore strong compactness does not by itself destroy the selected metric-only MTS-to-GR branch: weak systems use the checkpoint-4879 1PN certificate, while Ricci-flat strong-field vacuum systems hand off to the full Schwarzschild/Kerr/Einstein solution. Compact matter interiors, charged electrovac, perturbation spectra, independent flow operators and the first nonredundant curvature-cubed operator remain separate gates.

Marker: `MTS_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880`.

## 1. What is proved here

Checkpoint 4879 established the weak-field correspondence but deliberately stopped at strong fields. The next question is not whether a post-Newtonian series works at a neutron-star surface or black-hole horizon; it does not. The correct question is whether the full selected field equations still contain the corresponding GR spacetime.

For the retained local metric action

\[
S=\int d^4x\sqrt{-g}\left[
\frac{\overline M_{\rm Pl}^2}{2}(R-2\Lambda_{\rm cal})
+a_RR^2+a_CC_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma}
\right]+S_m,
\]

the answer is exactly yes for every four-dimensional Einstein vacuum background. This is stronger than extending a weak-field expansion.

## 2. Exact Einstein/Bach-flat theorem

The `R^2` Euler tensor is

\[
H^{(R^2)}_{\mu\nu}
=2RR_{\mu\nu}-\frac12g_{\mu\nu}R^2
+2(g_{\mu\nu}\Box-\nabla_\mu\nabla_\nu)R.
\]

On a four-dimensional Einstein metric,

\[
R_{\mu\nu}=\Lambda_Eg_{\mu\nu},
\qquad
R=4\Lambda_E,
\qquad
\nabla_\mu R=0.
\]

Therefore

\[
H^{(R^2)}_{\mu\nu}
=\left[2(4\Lambda_E)\Lambda_E
-\frac12(4\Lambda_E)^2\right]g_{\mu\nu}=0.
\]

The local variation of `C^2` is proportional to the Bach tensor

\[
B_{\mu\nu}
=\left(\nabla^\rho\nabla^\sigma
+\frac12R^{\rho\sigma}\right)
C_{\mu\rho\nu\sigma}.
\]

For an Einstein metric, the contracted Bianchi identity gives

\[
\nabla^\sigma C_{\mu\rho\nu\sigma}=0,
\]

and tracelessness gives

\[
R^{\rho\sigma}C_{\mu\rho\nu\sigma}
=\Lambda_Eg^{\rho\sigma}C_{\mu\rho\nu\sigma}=0.
\]

Hence

\[
\boxed{B_{\mu\nu}=0.}
\]

The four-dimensional Euler density in the decomposition of `C^2` is topological and has no local bulk Euler tensor. Finally,

\[
G_{\mu\nu}+\Lambda_{\rm cal}g_{\mu\nu}=0
\]

on the matched Einstein branch `Lambda_E=Lambda_cal`. Thus

\[
\boxed{
R_{\mu\nu}=\Lambda_{\rm cal}g_{\mu\nu}
\Longrightarrow
E_{\mu\nu}^{\rm EH+R^2+C^2}=0
}
\]

for arbitrary finite `a_R` and `a_C`.

The Bach-flat result is recorded explicitly in [Liu, Lu, Pope and Vazquez-Poritz](https://arxiv.org/abs/1303.5781). The separate non-Einstein branches of the resummed fourth-order equations are real rather than ignored; [Podolsky et al.](https://arxiv.org/abs/1907.00046) exhibit Schwarzschild-Bach and other spherical branches.

## 3. Which branch is selected

The action alone does not select the Einstein solution uniquely. The selected strict-EFT branch imposes:

1. boundary data continuously connected to the Einstein-Hilbert solution as higher coefficients are taken to zero;
2. order reduction rather than independent excitation of the extra fourth-order homogeneous modes;
3. momenta and invariant curvatures below the retained EFT cutoff;
4. the metric-only local branch, with no independent flow/aether excitation.

This is the analytic Einstein branch already selected by the field-redefinition and amplitude results of checkpoints 4878-4879. It is not a declaration that non-Einstein quadratic-gravity solutions do not exist.

Immediate exact inclusions are Ricci-flat Schwarzschild, Kerr, arbitrary Ricci-flat vacuum solutions and matched Einstein-(A)dS backgrounds. This theorem does not automatically include Kerr-Newman or a charged material interior, because a generic Einstein-Maxwell metric is not an Einstein metric.

## 4. Quantitative handoff criteria

Use a declared one-percent domain tolerance

\[
\tau_{\rm dom}=10^{-2}.
\]

Define compactness

\[
u=\frac{GM}{Rc^2}.
\]

After retaining 1PN terms, a conservative relative-to-leading omitted-order proxy is

\[
\epsilon_{\rm PN}=u^2.
\]

Therefore

\[
\boxed{u<\sqrt{\tau_{\rm dom}}=0.1}
\]

is the checkpoint's one-percent 1PN gate. Crossing `u=0.1` means change calculation method; it is not by itself a failure of the field theory.

For a Schwarzschild exterior,

\[
K=R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
=48\frac{(GM/c^2)^2}{r^6},
\qquad
q_K=K^{1/4}.
\]

The off-branch derivative-control diagnostics inherited from checkpoint 4878 are

\[
\epsilon_{R^2}=12|a_R|\bar\ell_P^2q_K^2,
\qquad
\epsilon_{C^2}=4|a_C|\bar\ell_P^2q_K^2.
\]

The deliberately maximal control caps are

\[
|a_R|<3.43215\times10^{56},
\qquad
|a_C|<1.02964\times10^{57}.
\]

They reproduce `epsilon_R2=epsilon_C2=0.01` at `52 micrometres` by construction and are not empirical coefficient measurements. On the exact Einstein vacuum background the local `R^2/C^2` correction vanishes even before applying these envelopes.

The first genuine pure-vacuum operator not removable in the same way can be written schematically as

\[
S_6=\frac{\overline M_{\rm Pl}^2}{2}
\int\sqrt{-g}\,
\frac{c_6}{\Lambda_*^4}{\cal R}_3,
\]

where `R3` denotes a cubic Riemann invariant. With `ell_*=Lambda_*^{-1}`,

\[
\epsilon_6=|c_6|\frac{K}{\Lambda_*^4}
=|c_6|(q_K\ell_*)^4.
\]

The one-percent cutoff condition is therefore

\[
\boxed{
\ell_*<\frac{\tau_{\rm dom}^{1/4}}
{q_K|c_6|^{1/4}}.
}
\]

The remaining invariant controls are

\[
\epsilon_{\rm loop}=\eta_{N,{\rm total}}q_K^2,
\qquad
\epsilon_\Lambda=|\Lambda_{\rm cal}|R^2.
\]

Matter adds a separate logical gate: disjoint-source contact silence applies in the exterior, but interior self-contact, EOS, mass, multipoles and tides must be matched rather than declared absent.

## 5. Representative systems

The script evaluates invariant surface/horizon scales with `tau_dom=0.01`. The `ellStar_max` column assumes `|c6|=1`. `epsilon_R2/C2` uses the maximal checkpoint-4878 control caps, not predicted MTS coefficients.

| system | `u` | `u^2` | `q_K` (`m^-1`) | max `epsilon_R2=C2` | `ellStar_max` | route |
|---|---:|---:|---:|---:|---:|---|
| Earth | `6.961e-10` | `4.846e-19` | `1.090e-11` | `3.213e-33` | `2.901e10 m` | weak 1PN certificate |
| Sun | `2.123e-6` | `4.505e-12` | `5.512e-12` | `8.216e-34` | `5.737e10 m` | weak 1PN certificate |
| `1 Msun`, `7000 km` white dwarf | `2.110e-4` | `4.450e-8` | `5.461e-9` | `8.065e-28` | `5.790e7 m` | weak 1PN certificate |
| `1.4 Msun`, `12 km` neutron star | `0.1723` | `2.968e-2` | `9.104e-5` | `2.241e-19` | `3.473 km` | full matter-interior solver |
| `10 Msun` Schwarzschild horizon | `0.5` | `0.25` | `6.302e-5` | `1.074e-19` | `5.018 km` | exact Einstein vacuum branch |

The loop envelopes are at most `7.24e-78`. A reduced-Planck-length `Riemann^3` benchmark is at most `2.97e-153`. Those numbers do not derive `c6`; they demonstrate the scale hierarchy if the cutoff is microscopic.

For the neutron-star benchmark, the mean-density Ricci proxy gives an `R^2` control value `1.94e-19` even at the enormous control cap. That is encouraging but not an interior solution: relativistic pressure, EOS dependence, contact renormalization, multipoles and tidal response remain to be solved.

## 6. Strong-field decision tree

| case | conditions | action |
|---|---|---|
| weak metric-only | `u^2<tau` and every retained EFT control passes | use the private 1PN local-GR certificate |
| strong Einstein vacuum | `u^2>=tau`, `T_mn=0`, Einstein/Bach-flat analytic branch, higher controls pass | use the full exact GR vacuum solution |
| strong matter interior | `u^2>=tau`, matter support nonzero | solve full GR/TOV plus EOS and contact/worldline matching |
| higher-operator entry | `epsilon6>=tau` or another retained control fails | add operators or UV data; no local-GR certificate |
| independent flow extension | nonzero flow/aether dynamics is activated | exit the metric-only certificate and run preferred-frame/compact-body gates |

This prevents two opposite errors: rejecting GR merely because a PN series fails, and pretending that an exact vacuum background proves the compact-matter or perturbation sector.

## 7. What is now promoted

The selected branch has two connected private certificates:

\[
u<0.1
\Longrightarrow
\text{classical local GR through 1PN},
\]

and

\[
T_{\mu\nu}=0,
\quad
R_{\mu\nu}=\Lambda_{\rm cal}g_{\mu\nu}
\Longrightarrow
\text{exact GR background for arbitrary compactness}.
\]

Thus **strong compactness alone is removed as a blocker** for the local classical metric-only vacuum background. This is an actual extension of the framework rather than another missing-input ledger. Nonlocal quantum terms are controlled by `epsilon_loop`; they are bounded rather than declared exactly zero.

## 8. What remains unproved

- compact-matter interiors and EOS/contact matching;
- strong-equivalence, sensitivities, tides and source-owned multipoles;
- charged electrovac such as Kerr-Newman;
- black-hole and neutron-star perturbation spectra once higher operators are retained;
- the value or microscopic origin of `c6/Lambda_*^4`;
- any independent nonminimal flow/aether branch;
- primitive derivation of the integrated metric/Diff parent from only motion, time and space;
- the full unified theory.

## 9. Claim guards

- Do not call `u>=0.1` a theory failure; it is the 1PN approximation boundary.
- Do not say all quadratic-gravity solutions are Einstein; non-Einstein Bach branches exist.
- Do not count the analytic branch selector as derived from the local action alone.
- Do not extend the vacuum theorem through matter support or charged electrovac.
- Do not infer unchanged quasinormal modes merely from an unchanged background.
- Do not call the full nonlocal quantum EFT background exact; exactness here applies to the finite local classical `EH+R^2+C^2` sector.
- Do not call the derivative-control caps measured coefficients.
- Do not treat the mean-density proxy as a neutron-star EOS calculation.
- Do not set the curvature-cubed coefficient to zero because it is not yet derived.

## 10. Decision and next target

Decision:

`FOUR_DIMENSIONAL_EINSTEIN_METRICS_PROVED_EXACT_ON_FINITE_LOCAL_R2_C2_BRANCH; STRONG_COMPACTNESS_RECLASSIFIED_AS_PN_HANDOFF_NOT_THEORY_FAILURE; EARTH_SUN_WHITE_DWARF_INSIDE_1PN_GATE; BLACK_HOLE_VACUUM_HANDS_TO_EXACT_GR; NEUTRON_STAR_INTERIOR_AND_RIEMANN_CUBED_OWNER_REMAIN_OPEN; PRIVATE_CONDITIONAL_ONLY`.

Next target:

`4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-and-Riemann-cubed-coefficient-owner-gate.md`
