# The native growth prediction after restoring the gravitating heavy source

The local candidate was linked and run, not just compiled. In the retained illustrative F=0.5 two-field model, restoring the matched heavy density to the source used to estimate late radiation momentum removes most of the old apparent loss of clustering at 8/h Mpc. It does **not** erase the strong, scale-dependent small-scale suppression. This is a correction to a numerical approximation, not a fitted change to the action, matching, background, occupation or data. The original native CAMB library and October results remain unchanged.

## Native test before looking at the growth integrals

The pilot used the five preselected growth-weight knots (0.0345989166087, 0.075, 0.1197085030496, 0.1725, 0.255 Mpc⁻¹), the archived adiabatic preparation and main phase projection, original branches and all 61 saved scales. The native program itself switches at its event clocks. Both branches have WantCls=false, so the photon threshold conditional on requesting angular spectra is inapplicable. The massless-neutrino switch is bracketed by τ=1083.5–1084 Mpc at the lowest knot, but 591.0–591.5 Mpc at the other four. Photons switch at 1478.0–1478.5 Mpc for all five in both branches. The five main heavy handoffs occur at kτ≈3.08–22.73. The chronology is different from the previous high-k test.

At these knots the old streaming approximation gives today's MTS/control linear power ratio 2.85–4.91% below the calculation with radiation truncation disabled. With the heavy-only repair, the maximum relative difference is 1.34e-7 today and 1.91e-7 over the 61 epochs. All output channels in the original and patched binaries agree exactly for the all-cold control with the shortcut on, and in both branches with it off. The old matter-transfer calculation is reproduced within 6e-8 against the archive. The no-truncation reference still uses the native finite hierarchy, neutrino, matching and other approximations; it is not an exact continuum solution.

## Complete original qualified band, not an extrapolated five-point correction

Four matched native grids cover all 399 original knots through k=5 Mpc⁻¹, at 61 scales, one numerical worker at a time. Cold RSA and both no-truncation arms use the original library; heavy RSA uses the private patched copy. The original heavy RSA field is independently available from Stage56. The previous 13 exploratory knots above 5 were not promoted. The same slow scalar, cold control, baryons, light sector, primordial normalization, inherited background and measured covariance were used throughout.

| Fixed calculation | σ8 of total matter today | CDM-velocity / total-matter F8 today | Conditional χ², four SDSS growth measurements |
|---|---:|---:|---:|
| Archived heavy | 0.80403100 | 0.41405921 | 4.76081 |
| Corrected heavy | 0.82312048 | 0.42397751 | 4.02382 |
| Heavy, radiation truncation off | 0.82312113 | 0.42397784 | 4.02380 |
| Same slow field, all cold | 0.82885777 | 0.42693305 | 3.87979 |
| Archived matched ΛCDM control | 0.84220693 | 0.43510992 | 4.08255 |

The physical heavy field lowers σ8 by **0.692%** rather than about **3.00%** against the same slow-field cold control. The corrected heavy/cold matter power is 0.99834 at k=0.075, 0.96436 at 0.255, 0.65355 at 0.5 and 0.07364 at 1 Mpc⁻¹ today. Half power moves from 0.55725 to **0.56845 Mpc⁻¹**, versus 0.56844610 without truncation. These are linear perturbations, not halo counts or a local galaxy occupation.

The difference has an additive physical accounting. For a common top-hat/primordial weight W, let V=∫W D² d ln k, C=∫W D U d ln k, σ=√V, F=C/σ, where D is total-matter transfer and U is CDM velocity transfer. Each band's exact contributions are Δσ_b=ΔV_b/(σ_new+σ_ref) and ΔF_b=(ΔC_b−F_ref Δσ_b)/σ_new. Rows sum without assigning a fitted cutoff. Although the old high-k-only numerical correction was small in σ8, about 53% of the **remaining physical heavy-minus-cold σ8 difference** comes from k>0.2556 today. This is not 53% of the total variance. See scale-budget.csv.

## The sky comparison, and its limit

For the already-exposed SDSS DR12/DR16 growth-only marginals at z=0.38, 0.51, 0.698 and 1.48, the unchanged primary mapping now predicts 0.46973, 0.46993, 0.46149 and 0.38513. No parameters refitted. The primary χ² difference relative to fixed ΛCDM is −0.059, versus +0.678 before the repair; this is **numerical parity on this screen**, not evidence for model selection. The slow-field/all-cold benchmark scores slightly lower still. With the separately retained dσ8/d ln a mapping heavy gives 4.124 versus ΛCDM 4.077: even the ordering depends on what the compressed measurement is assumed to represent. The high-z QSO mean (0.462) remains above the corrected primary prediction. The original growth compression has geometry, bias, tracer and template assumptions. Do not add the separately profiled BAO score.

## Error checks and what to do next

- Corrected/native-live heavy-to-cold power ratios pass 2e-5 at **all 24,339** mode–epoch pairs (worst 1.22e-6). Individual absolute power predictions do not all pass: eight modes per branch exceed the threshold, worst about 4.03e-5 near k=0.06612. Relative CDM velocity has nine nonpassing absolute modes per branch, one today. Shared approximation error cancels in the ratio; it has not vanished in both models separately.
- All 18 integrated tests (six definitions × heavy, cold and their ratio) pass the unchanged threshold at eight output redshifts. Heavy σ8 and primary F8 agree with the no-truncation reference within 8.01e-7 fractional. Five-point finite differences, nested-grid and interpolation sensitivities are separately tabulated; these are not total theory error bars.
- An independent spherical-Bessel top hat with trapezoidal integration reproduces 32 rms and velocity-cross pairs within 8.57e-12 fractional. Independent covariance whitening recovers all 35 conditional scores. Inputs, archived libraries, grid and source hashes are locked. No GitHub changes. One 40.45 MB compiler scratch directory (compile-zeh7eeaw) remains on disk after a Windows cleanup denial; it contains the matching link witness, not a running service or an installed library.

**Next practical discriminator:** use the corrected density and velocity transfers with the survey's tracer and window response, against both controls, rather than treating four compressed growth amplitudes as a full-shape test. For higher-precision individual modes use the radiation-active reference. Keep F=0.5 identified as an illustrative preparation: a survey near-tie cannot determine that fraction or any galactic occupation from the field equations.
