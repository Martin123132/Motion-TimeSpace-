# 1210 Y5/R10 First Local Curvature Scale And Gres Bracket Smoke

**Current verdict:** 1210 still makes **no local-GR/R10 claim**. It gives the first algebraic feasibility map for the clean Fermi projector branch by solving the harsh target for the allowed `C_P*G_res_norm` product.

**Main progress:** using the clean branch `q_projector <= C_P*C_eff*L_D*Riemann_norm*G_res_norm`, the generated grid computes `allowed_CpGres_product = target/(C_eff*L_D*Riemann_norm)`. This tells us where the next pain is: `G_res_norm` and `C_P`, not the curvature scale by itself.

**Guardrail:** every grid row omits `domain_motion_Linf`, `projector_stress_Linf`, and the explicit curvature-gradient row, so every row remains nonclaim.

## Source Register

| source_id | local_path | needle | purpose | path_exists | needle_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1210_0_1209_next | 1209-Y5-R10-local-Fermi-domain-curvature-source-pack-or-domain-motion-lock.md | NEXT1209_0_1210 | handoff to first local curvature and G_res bracket smoke | True | True | False | False |
| SRC1210_1_1209_pressure_clean | source-intake/mts_residuals/P8_Y5_R10_1209_PRESSURE_SMOKE_SCHEMA.csv | PSC1209_0_clean_fermi_projector | clean Fermi projector pressure formula | True | True | False | False |
| SRC1210_2_1209_pressure_full | source-intake/mts_residuals/P8_Y5_R10_1209_PRESSURE_SMOKE_SCHEMA.csv | PSC1209_1_full_projector_budget | full projector pressure formula with blockers | True | True | False | False |
| SRC1210_3_1209_CP | source-intake/mts_residuals/P8_Y5_R10_1209_UNIFIED_SOURCE_PACK.csv | USP1209_6_CP | C_P remains an unsourced operator constant | True | True | False | False |
| SRC1210_4_1209_Gres | source-intake/mts_residuals/P8_Y5_R10_1209_UNIFIED_SOURCE_PACK.csv | USP1209_7_Gres | G_res_norm remains an unsourced local residual norm | True | True | False | False |
| SRC1210_5_1209_domain_motion | source-intake/mts_residuals/P8_Y5_R10_1209_DOMAIN_MOTION_PROJECTOR_STRESS_AUDIT.csv | DMP1209_1_non_geodesic_lab_bound | domain motion must stay explicit | True | True | False | False |
| SRC1210_6_1208_fermi_requirement | source-intake/mts_residuals/P8_Y5_R10_1208_PRESSURE_COMPARISON.csv | CMP1208_2_fermi_curvature_requirement | earlier Fermi curvature requirement | True | True | False | False |
| SRC1210_7_1207_target | source-intake/mts_residuals/P8_Y5_R10_1207_PRESSURE_AND_ABSORPTION_GATE.csv | PGA1207_0_total_formula | harsh projector target | True | True | False | False |

## Bracket Assumptions

| assumption_id | assumption | status | consequence | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| ASM1210_0_clean_branch_only | Bracket grid evaluates only the clean Fermi curvature projector drift term. | NONCLAIM_SANDBOX | domain_motion_Linf and projector_stress_Linf remain separate blockers, not silently zeroed | False | False |
| ASM1210_1_effective_constant | C_eff represents C_Fermi plus any retained second-order curvature-gradient allowance. | BRACKET_PARAMETER_NOT_SOURCED | C_eff grid is a sensitivity scan, not evidence | False | False |
| ASM1210_2_allowed_product | Allowed product is S_allowed = target/(C_eff*L_D*Riemann_norm), where S=C_P*G_res_norm in the normalized pressure schema. | ALGEBRAIC_REARRANGEMENT | large S_allowed means the clean curvature drift is not the limiting piece; small S_allowed means C_P*G_res must be correspondingly tiny | False | False |
| ASM1210_3_units_guard | C_P*G_res_norm may carry norm-dependent units until the operator norm is sourced. | UNITS_NOT_CLAIM_READY | all numeric rows are feasibility bookkeeping only | False | False |

## Fermi Bracket Grid Preview

Full grid is in `P8_Y5_R10_1210_FERMI_BRACKET_GRID.csv`.

| grid_id | L_D_m | Riemann_norm_m2 | C_eff | fermi_projector_drift | target | allowed_CpGres_product | classification | omitted_terms | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FBG1210_000 | 0.001 | 1e-30 | 1 | 1e-33 | 1.17233215026e-05 | 1.17233215026e+28 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| FBG1210_001 | 0.001 | 1e-30 | 10 | 1e-32 | 1.17233215026e-05 | 1.17233215026e+27 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| FBG1210_002 | 0.001 | 1e-30 | 100 | 1e-31 | 1.17233215026e-05 | 1.17233215026e+26 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| FBG1210_003 | 0.001 | 1e-27 | 1 | 1e-30 | 1.17233215026e-05 | 1.17233215026e+25 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| FBG1210_004 | 0.001 | 1e-27 | 10 | 1e-29 | 1.17233215026e-05 | 1.17233215026e+24 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| FBG1210_005 | 0.001 | 1e-27 | 100 | 1e-28 | 1.17233215026e-05 | 1.17233215026e+23 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| FBG1210_006 | 0.001 | 1e-24 | 1 | 1e-27 | 1.17233215026e-05 | 1.17233215026e+22 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| FBG1210_007 | 0.001 | 1e-24 | 10 | 1e-26 | 1.17233215026e-05 | 1.17233215026e+21 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| FBG1210_008 | 0.001 | 1e-24 | 100 | 1e-25 | 1.17233215026e-05 | 1.17233215026e+20 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| FBG1210_009 | 0.001 | 1e-21 | 1 | 1e-24 | 1.17233215026e-05 | 1.17233215026e+19 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| FBG1210_010 | 0.001 | 1e-21 | 10 | 1e-23 | 1.17233215026e-05 | 1.17233215026e+18 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| FBG1210_011 | 0.001 | 1e-21 | 100 | 1e-22 | 1.17233215026e-05 | 1.17233215026e+17 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| FBG1210_012 | 0.01 | 1e-30 | 1 | 1e-32 | 1.17233215026e-05 | 1.17233215026e+27 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| FBG1210_013 | 0.01 | 1e-30 | 10 | 1e-31 | 1.17233215026e-05 | 1.17233215026e+26 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| FBG1210_014 | 0.01 | 1e-30 | 100 | 1e-30 | 1.17233215026e-05 | 1.17233215026e+25 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| FBG1210_015 | 0.01 | 1e-27 | 1 | 1e-29 | 1.17233215026e-05 | 1.17233215026e+24 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| FBG1210_016 | 0.01 | 1e-27 | 10 | 1e-28 | 1.17233215026e-05 | 1.17233215026e+23 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| FBG1210_017 | 0.01 | 1e-27 | 100 | 1e-27 | 1.17233215026e-05 | 1.17233215026e+22 | VERY_LOOSE_FOR_NORMALIZED_PRODUCT | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row | False | False |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | 66 rows omitted; see CSV |

## Required Radius Grid Preview

Full grid is in `P8_Y5_R10_1210_REQUIRED_RADIUS_GRID.csv`.

| radius_id | Riemann_norm_m2 | C_eff | assumed_CpGres_product | max_L_D_m_clean_branch | target | classification | omitted_terms | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RRG1210_000 | 1e-30 | 1 | 1 | 1.17233215026e+25 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| RRG1210_001 | 1e-30 | 1 | 1000 | 1.17233215026e+22 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| RRG1210_002 | 1e-30 | 1 | 1000000 | 1.17233215026e+19 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| RRG1210_003 | 1e-30 | 1 | 1000000000 | 1.17233215026e+16 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| RRG1210_004 | 1e-30 | 1 | 1e+12 | 1.17233215026e+13 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| RRG1210_005 | 1e-30 | 10 | 1 | 1.17233215026e+24 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| RRG1210_006 | 1e-30 | 10 | 1000 | 1.17233215026e+21 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| RRG1210_007 | 1e-30 | 10 | 1000000 | 1.17233215026e+18 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| RRG1210_008 | 1e-30 | 10 | 1000000000 | 1.17233215026e+15 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| RRG1210_009 | 1e-30 | 10 | 1e+12 | 1.17233215026e+12 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| RRG1210_010 | 1e-30 | 100 | 1 | 1.17233215026e+23 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| RRG1210_011 | 1e-30 | 100 | 1000 | 1.17233215026e+20 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| RRG1210_012 | 1e-30 | 100 | 1000000 | 1.17233215026e+17 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| RRG1210_013 | 1e-30 | 100 | 1000000000 | 1.17233215026e+14 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| RRG1210_014 | 1e-30 | 100 | 1e+12 | 117233215026 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| RRG1210_015 | 1e-27 | 1 | 1 | 1.17233215026e+22 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| RRG1210_016 | 1e-27 | 1 | 1000 | 1.17233215026e+19 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| RRG1210_017 | 1e-27 | 1 | 1000000 | 1.17233215026e+16 | 1.17233215026e-05 | CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM | domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf | False | False |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | 42 rows omitted; see CSV |

## Interpretation Ledger

| interpretation_id | statement | evidence | meaning | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| INT1210_0_range | Clean Fermi curvature drift spans the generated grid. | min_drift=1e-33; max_drift=1e-16; rows=84 | the finite-domain curvature part alone can be made tiny for small domains/weak curvature, but this says nothing about G_res or hidden projector/domain terms | False | False |
| INT1210_1_allowed_product | The clean branch converts the pressure target into an allowed C_P*G_res_norm product. | min_allowed=117233215026; max_allowed=1.17233215026e+28 | this is the first useful design map: source C_P and G_res_norm, then see which domain/curvature rows survive | False | False |
| INT1210_2_no_pass | No row is a pass row. | all rows have valid_for_claim=false and claim_allowed=false | this is a feasibility smoke map, not a local-GR/R10 claim | False | False |

## Source Gaps

| gap_id | missing_object | why_it_matters | best_next_source | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| GAP1210_0_CP | C_P | multiplies every projector leakage term before scoring q_projector | derive same-norm operator bound from D_T adjoint and projector leakage estimate | MISSING | False | False |
| GAP1210_1_Gres | G_res_norm | sets whether small geometry drift actually produces a small residual response | derive from parent GR-reduction residual profile or prove theorem-zero in local branch | MISSING | False | False |
| GAP1210_2_real_curvature_profile | Riemann_norm;nabla_Riemann_norm;L_D | turns bracket grid into a source-backed local arena row | choose explicit local arena/domain and compute curvature/domain scale under the same norm | MISSING | False | False |
| GAP1210_3_domain_stress | domain_motion_Linf;projector_stress_Linf | can dominate clean curvature drift if not theorem-zero or bounded | parent-signed domain/readout lock or non-geodesic/stress finite-bound row | MISSING | False | False |

## Claim Gates

| gate_id | gate | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE1210_0_grid_not_claim | bracket grid as evidence | BLOCKED | grid values are sensitivity parameters, not sourced physical rows | False | False |
| GATE1210_1_clean_branch_only | clean Fermi branch pass | BLOCKED | domain_motion, projector_stress, C_P, and G_res_norm are not sourced or theorem-zero | False | False |
| GATE1210_2_local_GR_R10 | local-GR/R10 pass | BLOCKED | 1210 is a feasibility map only | False | False |

## Next Target

| next_id | target_file | target_script | task | success_condition | do_not_do | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1210_0_1211 | 1211-Y5-R10-Gres-norm-source-or-local-residual-zero-theorem.md | scripts/Y5_R10_Gres_norm_source_or_local_residual_zero_theorem.py | derive or source G_res_norm for the local GR-reduction branch, because the 1210 map shows curvature-domain leakage cannot be scored without C_P*G_res_norm | G_res_norm is theorem-zero, reduced to parent GR-limit residual terms, or staged as a same-norm source row that can feed the 1210 bracket | do not call bracket rows evidence; do not hide C_P or domain/stress blockers; do not edit formalization-workbench; do not push GitHub | False | False |

## Validation

| check_id | check | status | details | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| VAL1210_0_sources_exist | all cited local sources exist | PASS | 8/8 sources exist | False | False |
| VAL1210_1_needles_found | all cited source needles found | PASS | 8/8 needles found | False | False |
| VAL1210_2_grid_count | Fermi bracket grid has expected row count | PASS | rows=84 | False | False |
| VAL1210_3_radius_grid_count | radius requirement grid has expected row count | PASS | rows=60 | False | False |
| VAL1210_4_numeric_positive | grid numeric values are positive | PASS | positive drift, allowed product, and max radius values | False | False |
| VAL1210_5_target_preserved | 1209 projector target is preserved | PASS | target=1.17233215026e-05 | False | False |
| VAL1210_6_omitted_terms_visible | domain/stress omitted terms are visible | PASS | domain_motion_Linf and projector_stress_Linf retained in grid rows | False | False |
| VAL1210_7_gres_gap_visible | G_res_norm source gap remains explicit | PASS | GAP1210_1_Gres present | False | False |
| VAL1210_8_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout | False | False |
| VAL1210_9_csv_parse | all generated CSVs parse cleanly | PASS | P8_Y5_R10_1210_SOURCE_REGISTER.csv:8; P8_Y5_R10_1210_BRACKET_ASSUMPTIONS.csv:4; P8_Y5_R10_1210_FERMI_BRACKET_GRID.csv:84; P8_Y5_R10_1210_REQUIRED_RADIUS_GRID.csv:60; P8_Y5_R10_1210_INTERPRETATION_LEDGER.csv:3; P8_Y5_R10_1210_SOURCE_GAPS.csv:4; P8_Y5_R10_1210_CLAIM_GATES.csv:3; P8_Y5_R10_1210_NEXT_TARGET.csv:1 | False | False |
| VAL1210_10_formalization_untouched | formalization-workbench untouched during run | PASS | formalization_recent_after_run_start_count=0 | False | False |
| VAL1210_11_next_target | next target is staged | PASS | 1211-Y5-R10-Gres-norm-source-or-local-residual-zero-theorem.md | False | False |
| VAL1210_12_overall | overall 1210 validation | PASS | 1210 bracket smoke map is reproducible and nonclaim | False | False |
