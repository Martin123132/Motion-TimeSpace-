# 3701 Y5 R2FR Local Test Source Row Acquisition And Residual Matrix

Private checkpoint. No GitHub action. No public claim.

## Status

- `LOCAL_TEST_EXTERNAL_SOURCE_ANCHORS_ACQUIRED_MTS_RESIDUAL_SIDE_STILL_MISSING`
- 3701 converts the local-test gates into a source matrix. Public anchors now exist for R10/Newton, Cassini PPN gamma, MICROSCOPE WEP, NIST fine-structure alpha, and optical-clock redshift. These are deliberately nonclaim rows: they provide external normalizers and anchors, while MTS-side rho_i, z2_bound, Kperp, q_loc, full R10 curve, EM/Poynting residual tensors, and orbital kernels remain missing.

## Main Result

- The external side of the local-test matrix is now partly source-backed.
- R10/Newton has a real Eot-Wash anchor: alpha=1 Yukawa interactions are limited to ranges below `38.6 micrometer` at 95% confidence, but this is anchor-only, not a full curve.
- PPN has a Cassini gamma normalizer: `gamma-1=(2.1 +/- 2.3)e-5`.
- WEP has a MICROSCOPE precision anchor of order `eta ~ 1e-15`.
- EM has the NIST/CODATA fine-structure anchor `alpha=7.2973525643e-3` and standard uncertainty `1.1e-12`.
- Clocks have a lab redshift-gradient uncertainty anchor `~2.6e-19 fractional_frequency_per_cm`.

## Claim Discipline

- None of these source rows prove MTS local recovery.
- They only provide external normalizers. The MTS side still needs `rho_i`, `z2_bound`, `Kperp`, `q_loc`, full R10 curve, EM/Poynting residual tensors, and orbital kernels.

## External Web Sources

- `WEB3701_R10_Lee2020`: short-range Newton/R10 | Newtonian fit down to 52 micrometers; gravitational-strength Yukawa interactions limited to ranges below 38.6 micrometers at 95% confidence. | https://pubmed.ncbi.nlm.nih.gov/32216404/
- `WEB3701_R10_UWash2020`: short-range Newton/R10 | 95% confidence alpha=1 Yukawa range anchor: lambda < 38.6 micrometers. | https://phys.washington.edu/news/2020/04/06/experiment-finds-gravity-still-works-down-50-micrometers
- `WEB3701_PPN_Cassini2003`: PPN gamma | gamma = 1 + (2.1 +/- 2.3) x 10^-5. | https://www.nature.com/articles/nature01997
- `WEB3701_WEP_MICROSCOPE2022`: WEP/species | Weak equivalence principle tested at precision 10^-15 in Eotvos ratio eta. | https://link.aps.org/doi/10.1103/PhysRevLett.129.121102
- `WEB3701_EM_NIST_ALPHA2022`: EM/fine structure | alpha = 7.2973525643 x 10^-3 with standard uncertainty 0.0000000011 x 10^-3. | https://physics.nist.gov/cgi-bin/cuu/Value?alph=
- `WEB3701_CLOCK_Zheng2023`: clock/redshift | Measured fractional frequency gradient -12.4 +/- 0.7(stat) +/- 2.5(sys) x 10^-19 per cm over 1 cm. | https://www.nature.com/articles/s41467-023-40629-8
- `WEB3701_CLOCK_Bothwell2022`: clock/redshift | NIST/JILA Nature result resolving gravitational redshift across millimetre-scale atomic sample. | https://www.nist.gov/publications/resolving-gravitational-redshift-across-millimetre-scale-atomic-sample
- `WEB3701_GR_WillReview`: PPN/orbital review | Review source for PPN and Solar-System tests; includes Cassini gamma result. | https://link.springer.com/article/10.12942/lrr-2006-3

## Local Test Source Rows

- `SRC3701_R10_lambda_alpha1_anchor`: short-range Newton/R10 | lambda_alpha1_excluded_above=38.6 micrometer | `anchor_only_non_curve`
- `SRC3701_R10_min_separation`: short-range Newton/R10 | minimum_detector_attractor_separation=52.0 micrometer | `geometry_anchor`
- `SRC3701_PPN_gamma_sigma`: PPN/local metric | sigma_gamma_minus_one=2.3e-05 dimensionless | `numeric_normalizer_partial`
- `SRC3701_WEP_eta_precision`: WEP/species | eta_precision=1e-15 dimensionless | `numeric_normalizer_partial`
- `SRC3701_EM_alpha_value`: Maxwell/EM/Poynting stress | fine_structure_alpha=0.0072973525643 dimensionless | `numeric_constant_anchor`
- `SRC3701_EM_alpha_std_uncertainty`: Maxwell/EM/Poynting stress | fine_structure_alpha_standard_uncertainty=1.1e-12 dimensionless | `numeric_normalizer_partial`
- `SRC3701_CLOCK_gradient_sys_stat_combined`: precision clocks/time | redshift_gradient_uncertainty=2.6e-19 fractional_frequency_per_cm | `numeric_normalizer_partial`

## Residual Matrix Rows

- `RM3701_0_PPN_gamma`: PPN/local metric | `EXTERNAL_NORMALIZER_PARTIAL_MTS_SIDE_MISSING` | missing `MISS3701_0_rho_PPN;MISS3701_5_z2_bound;MISS3701_6_Kperp;MISS3701_7_q_loc`
- `RM3701_1_R10_anchor`: short-range Newton/R10 | `ANCHOR_ONLY_MTS_SIDE_AND_FULL_CURVE_MISSING` | missing `MISS3701_1_rho_Newton;MISS3701_5_z2_bound;MISS3701_8_R10_curve`
- `RM3701_2_clock`: precision clocks/time | `EXTERNAL_NORMALIZER_PARTIAL_MTS_SIDE_MISSING` | missing `MISS3701_3_rho_clock;MISS3701_5_z2_bound`
- `RM3701_3_EM_alpha`: Maxwell/EM/Poynting stress | `CONSTANT_ANCHOR_READY_EM_RESIDUAL_MISSING` | missing `MISS3701_2_rho_EM;MISS3701_5_z2_bound`
- `RM3701_4_WEP`: WEP/species | `EXTERNAL_NORMALIZER_PARTIAL_MTS_SIDE_MISSING` | missing `MISS3701_4_rho_WEP;MISS3701_5_z2_bound`
- `RM3701_5_orbital`: orbital dynamics | `REVIEW_CONTEXT_ONLY_ORBITAL_KERNEL_MISSING` | missing `MISS3701_1_rho_Newton;MISS3701_5_z2_bound;MISS3701_9_orbital_kernel`

## Missing MTS Inputs

- `MISS3701_0_rho_PPN`: PPN/local metric | `rho_PPN` | `MISSING_PARENT_RESIDUAL_TENSOR`
- `MISS3701_1_rho_Newton`: short-range Newton/R10 | `rho_Newton` | `MISSING_PARENT_RESIDUAL_TENSOR`
- `MISS3701_2_rho_EM`: Maxwell/EM/Poynting stress | `rho_EM` | `MISSING_PARENT_RESIDUAL_TENSOR`
- `MISS3701_3_rho_clock`: precision clocks/time | `rho_clock` | `MISSING_PARENT_RESIDUAL_TENSOR`
- `MISS3701_4_rho_WEP`: WEP/species | `rho_species_a_minus_b` | `MISSING_SPECIES_SCORE_MAP`
- `MISS3701_5_z2_bound`: all local arenas | `z2_bound` | `MISSING_PARENT_AMPLITUDE`
- `MISS3701_6_Kperp`: PPN/local metric | `Kperp_norm` | `MISSING_TENSOR_GATE`
- `MISS3701_7_q_loc`: PPN/local metric | `q_loc_norm` | `MISSING_LOCAL_CURRENT_SOLVER`
- `MISS3701_8_R10_curve`: short-range Newton/R10 | `alpha_bound(lambda)` | `MISSING_FULL_BOUND_CURVE`
- `MISS3701_9_orbital_kernel`: orbital dynamics | `K_orbit` | `MISSING_ORBITAL_PROJECTION`

## Score Readiness

- `READY3701_0_R10`: short-range Newton/R10 | external=True mts=False score=False | R10 has a real alpha=1/lambda anchor, but not a full alpha_bound(lambda) curve and no MTS alpha/lambda rows.
- `READY3701_1_PPN`: PPN/local metric | external=True mts=False score=False | Cassini gamma normalizer exists, but PPN vector projection, Kperp, q_loc, and rho_PPN are missing.
- `READY3701_2_clock`: precision clocks/time | external=True mts=False score=False | Clock redshift normalizer exists, but clock residual tensor and convention are missing.
- `READY3701_3_EM`: Maxwell/EM/Poynting stress | external=True mts=False score=False | NIST alpha anchor exists, but EM/Poynting residual tensor and alpha-source silence row are missing.
- `READY3701_4_WEP`: WEP/species | external=True mts=False score=False | MICROSCOPE precision exists, but species residual difference map is missing.
- `READY3701_5_orbital`: orbital dynamics | external=False mts=False score=False | Only review context is attached; orbital kernel/tolerance source row is not ready.

## Decisions

- `DEC3701_0`: `SOURCE_ANCHORS_ADVANCE` | External local-test anchors acquired. | R10, PPN gamma, WEP, alpha, and clock anchors now have source-backed rows.
- `DEC3701_1`: `CLAIM_BLOCKED` | No local arena is score-ready yet. | The external side is partly real, but every arena still lacks MTS residual tensors/amplitudes or full bound curves.
- `DEC3701_2`: `R10_FIRST_RECOMMENDED` | Next step should focus on one arena to completion. | R10 is the cleanest first target because its external anchor/curve directly matches the Yukawa lambda_H branch.

## Claim Gates

- `CG3701_0_external_sources`: `PARTIAL` | external normalizer/source rows attached for all local arenas
- `CG3701_1_mts_residuals`: `BLOCKED` | rho_i residual tensors sourced/bounded
- `CG3701_2_amplitude`: `BLOCKED` | z2_bound sourced from parent mass-gap/amplitude rows
- `CG3701_3_R10_full_curve`: `BLOCKED` | full R10 alpha_bound(lambda) curve or machine-readable table
- `CG3701_4_PPN_tensor`: `BLOCKED` | Kperp and q_loc PPN projection bounded
- `CG3701_5_public_claim`: `BLOCKED` | public local-GR/Maxwell/Newton claim allowed

## Next Target

- `3702-Y5-R2FR-R10-bound-curve-digitizer-and-MTS-alpha-lambda-binder.md`
- Objective: turn the R10 anchor into a real alpha_bound(lambda) curve/table if possible, and bind symbolic MTS alpha_eff(lambda_H) rows to the 3700 residual formula without allowing claims
