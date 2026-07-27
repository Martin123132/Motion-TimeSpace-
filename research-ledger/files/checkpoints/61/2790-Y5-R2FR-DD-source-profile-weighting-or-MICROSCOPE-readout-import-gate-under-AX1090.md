# 2790 - DD source-profile weighting or MICROSCOPE readout import gate under AX1090

## Private Verdict

2790 answers the route-choice question by keeping both gates explicit. The source profile algebra is now in the R2FR branch: finite-range spherical source weighting gives a clean radial kernel and a long-range bulk limit. But using the bulk Earth row physically requires a parent-signed long-range condition lambda_WEP >> R_E, while using finite-range rows requires PREM/profile weighting and a lambda owner. MICROSCOPE readout import remains separate; gx/gz/Sxx/Sxz/masks/timing and eta normalization are not replaced by the spherical profile smoke rows.

## Source Register
| row_id | source_key | exists | needle_found | source_role |
| --- | --- | --- | --- | --- |
| SRC2790_00_2789_next | 2789_next | True | True | current handoff into profile/readout gate |
| SRC2790_01_2789_validation | 2789_validation | True | True | 2789 validation baseline |
| SRC2790_02_2789_source_vector | 2789_source_vector | True | True | R2FR first bulk Earth DD source vector |
| SRC2790_03_2789_product | 2789_product | True | True | R2FR DD source-material products |
| SRC2790_04_2789_caveat | 2789_caveat | True | True | R2FR source vector caveat gates |
| SRC2790_05_1084_kernel | 1084_kernel | True | True | R10 finite-range profile kernel precedent |
| SRC2790_06_1084_layers | 1084_layers | True | True | R10 core/mantle composition rows |
| SRC2790_07_1084_profile_grid | 1084_profile_grid | True | True | R10 profile weighting grid precedent |
| SRC2790_08_1084_readout | 1084_readout | True | True | R10 MICROSCOPE readout import gate |
| SRC2790_09_1084_next | 1084_next | True | True | R10 next target after profile/readout gate |
| SRC2790_10_2780_cmsm | 2780_cmsm | True | True | R2FR official CMSM export search |
| SRC2790_11_2781_tau | 2781_tau | True | True | R2FR physical tau missing status |
| SRC2790_12_local_bounds | local_bounds | True | True | MICROSCOPE WEP bound row |

## Profile Kernel Ledger
| kernel_id | claim | status | claim_blocker |
| --- | --- | --- | --- |
| K2790_0_angular_integral | external finite-range spherical source reduces to a radial kernel | DERIVED_AS_KERNEL_CONTRACT | kernel is external DD/Yukawa profile algebra, not yet MTS parent-derived |
| K2790_1_effective_source_charge | profile-weighted source charge can be defined | DERIVED_AS_NONCLAIM_PROFILE_RULE | requires lambda owner and sourced rho(r), q(r) |
| K2790_2_long_range_limit | bulk source vector is recovered in the long-range limit | LONG_RANGE_LIMIT_CONDITIONALLY_DERIVED | MTS has not derived that the WEP carrier range is long compared with Earth radius |
| K2790_3_finite_range_profile_dependency | finite-range branch is surface/profile sensitive | FINITE_RANGE_PROFILE_DEPENDENCY_RETAINED | no PREM/compositional shell vector and no MTS lambda_WEP selection |
| K2790_4_orbit_factor | 710 km orbit is a common first-pass amplitude factor for a spherical source | READOUT_AMPLITUDE_SEPARATED_NONCLAIM | actual MICROSCOPE readout uses time-dependent gx/gz/Sxx/Sxz/masks not imported here |

## Core/Mantle Composition Candidate
| layer_id | layer | element | normalized_layer_mass_fraction | Z | A | extraction_status |
| --- | --- | --- | --- | --- | --- | --- |
| LAYER2790_mantle_Fe | mantle | Fe | 6.295886553354117e-02 | 26 | 55.845 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER2790_mantle_O | mantle | O | 4.425223775520467e-01 | 8 | 15.999 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER2790_mantle_Si | mantle | Si | 2.112038620134768e-01 | 14 | 28.085 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER2790_mantle_Mg | mantle | Mg | 2.293070501860605e-01 | 12 | 24.305 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER2790_mantle_Ni | mantle | Ni | 2.011465352509303e-03 | 28 | 58.693 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER2790_mantle_Ca | mantle | Ca | 2.544503670924268e-02 | 20 | 40.078 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER2790_mantle_Al | mantle | Al | 2.363471789198431e-02 | 13 | 26.982 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER2790_mantle_S | mantle | S | 3.017198028763954e-04 | 16 | 32.06 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER2790_mantle_Cr | mantle | Cr | 2.614904958262094e-03 | 24 | 51.996 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER2790_core_Fe | core | Fe | 8.592964824120602e-01 | 26 | 55.845 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER2790_core_O | core | O | 0.000000000000000e+00 | 8 | 15.999 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER2790_core_Si | core | Si | 6.030150753768844e-02 | 14 | 28.085 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER2790_core_Mg | core | Mg | 0.000000000000000e+00 | 12 | 24.305 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER2790_core_Ni | core | Ni | 5.226130653266332e-02 | 28 | 58.693 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER2790_core_Ca | core | Ca | 0.000000000000000e+00 | 20 | 40.078 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER2790_core_Al | core | Al | 0.000000000000000e+00 | 13 | 26.982 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER2790_core_S | core | S | 1.909547738693467e-02 | 16 | 32.06 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER2790_core_Cr | core | Cr | 9.045226130653266e-03 | 24 | 51.996 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |

## Core/Mantle DD Charge Vectors
| layer_charge_id | layer | mass_fraction_candidate | Q_alpha_Coulomb_layer | Q_surface_binding_layer | status |
| --- | --- | --- | --- | --- | --- |
| LC2790_mantle | mantle | 6.751640585562846e-01 | 1.399469878526843e-03 | -1.311954404402867e-02 | NUMERIC_TWO_LAYER_DD_CHARGE_NONCLAIM |
| LC2790_core | core | 3.248359414437154e-01 | 2.301637295368259e-03 | -1.001356198854927e-02 | NUMERIC_TWO_LAYER_DD_CHARGE_NONCLAIM |

## Source Profile Weighting Grid
| profile_row_id | lambda_label | lambda_over_R_E | Q_alpha_Coulomb_eff | Q_surface_binding_eff | delta_alpha_vs_2789_bulk | delta_surface_vs_2789_bulk | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PROFILE2790_long_range_mass_average | long_range_mass_average | inf | 1.692526280716369e-03 | -1.211060943892973e-02 | 1.265593965497089e-06 | 8.572761027718367e-06 | NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM |
| PROFILE2790_lambda_over_RE_100 | lambda_over_RE_100 | 1.000000000000000e+02 | 1.692524622151824e-03 | -1.211061514903588e-02 | 1.263935400952270e-06 | 8.567050921566566e-06 | NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM |
| PROFILE2790_lambda_over_RE_10 | lambda_over_RE_10 | 1.000000000000000e+01 | 1.692360490018798e-03 | -1.211118022315670e-02 | 1.099803267926198e-06 | 8.001976800746727e-06 | NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM |
| PROFILE2790_lambda_over_RE_1 | lambda_over_RE_1 | 1.000000000000000e+00 | 1.676581966220657e-03 | -1.216550252616180e-02 | -1.467872053021466e-05 | -4.632032620434552e-05 | NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM |
| PROFILE2790_lambda_over_RE_0p3 | lambda_over_RE_0p3 | 3.000000000000000e-01 | 1.566643720996945e-03 | -1.254399792568670e-02 | -1.246169657539275e-04 | -4.248157257292530e-04 | NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM |
| PROFILE2790_lambda_over_RE_0p1 | lambda_over_RE_0p1 | 1.000000000000000e-01 | 1.411202487080551e-03 | -1.307915101835349e-02 | -2.800581996703212e-04 | -9.599688183960439e-04 | NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM |
| PROFILE2790_lambda_over_RE_0p03 | lambda_over_RE_0p03 | 3.000000000000000e-02 | 1.399470198540942e-03 | -1.311954294228410e-02 | -2.917904882099305e-04 | -1.000360742326654e-03 | NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM |

## Profile Closure Gates
| gate_id | claim_component | gate_pass | condition | current_status |
| --- | --- | --- | --- | --- |
| PCG2790_0_long_range_bulk_limit | bulk source vector suffices | conditional | derive lambda_WEP >> R_E or massless/common long-range source carrier from parent action | CONDITION_NOT_PARENT_SIGNED |
| PCG2790_1_finite_range_profile | finite-range source profile vector | false | import PREM density plus shell composition profile and choose lambda_WEP | MISSING_PREM_IMPORT_AND_LAMBDA_OWNER |
| PCG2790_2_source_charge_basis | DD profile vector is an MTS source vector | false | derive parent-to-DD coefficient/source basis map | PARENT_TO_DD_MAP_NOT_DERIVED |
| PCG2790_3_readout_projection | profile vector is projected into MICROSCOPE eta | false | import official/validated MICROSCOPE readout arrays | OFFICIAL_READOUT_NOT_IMPORTED |

## MICROSCOPE Readout Import Gate
| readout_id | needed_object | current_status | claim_blocker |
| --- | --- | --- | --- |
| RIG2790_0_CMSM_arrays | official MICROSCOPE CMSM/export arrays | OFFICIAL_ARRAYS_NOT_IMPORTED | unit or surrogate readout cannot become physical tau_WEP |
| RIG2790_1_product_convention | eta_AB product normalization | NORMALIZATION_NOT_FILLED | numeric profile products are scale probes only |
| RIG2790_2_surrogate_limit | surrogate design matrix relation to official readout | SURROGATE_AVAILABLE_NONCLAIM | cannot replace official readout for a WEP claim |
| RIG2790_3_CMSM_inventory | local CMSM export status | NO_USER_SUPPLIED_CMSM_EXPORT_FOUND | 2780 inventory found no official local export |

## Product Stub And Bound
| prediction_id | product_symbol | product_value | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| PRED2790_0_DD_profile_or_readout_not_MTS_product | P_WEP_relative_source_weight | MISSING_LAMBDA_WEP_OR_PREM_PROFILE_AND_OFFICIAL_READOUT_AND_PARENT_TO_DD_MAP | PROFILE_GRID_NUMERIC_BUT_PHYSICAL_PRODUCT_MISSING | False |

| bound_id | observable | upper_bound | units | valid_bound_row |
| --- | --- | --- | --- | --- |
| BOUND2790_0_MICROSCOPE_WEP_source_charge | eta_WEP_source_charge | 2.8e-15 | dimensionless | True |

| runner_id | valid_prediction_rows | valid_bound_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- |
| APR2790_0_DD_profile_readout_product_stub | 0 | 1 | False | reject DD profile/readout rows as MTS product |

## Claim Gates
| gate_id | claim_component | gate_pass | claim_allowed | reason |
| --- | --- | --- | --- | --- |
| CG2790_0_profile_rule | source-profile rule | conditional | False | radial kernel rule derived as external DD/Yukawa algebra, but physical source needs lambda/profile |
| CG2790_1_long_range_bulk | bulk source vector suffices | conditional | False | requires parent-signed lambda_WEP >> R_E or massless common carrier |
| CG2790_2_parent_to_DD | MTS parent-to-DD map | false | False | still not derived |
| CG2790_3_readout | MICROSCOPE official readout | false | False | CMSM/export arrays and eta normalization not imported |
| CG2790_4_product_runner | WEP product runner | false | False | valid_prediction_rows=0 |

## Decision Ledger
| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DECISION2790_0 | source-profile algebra is explicit in R2FR | finite-range spherical source weighting reduces to a hyperbolic radial kernel and has a clean long-range bulk limit | derive lambda_WEP from parent action before using either bulk or finite-range profile rows as physical |
| DECISION2790_1 | MICROSCOPE readout import remains a separate hard gate | 710 km orbit and spherical source profile do not substitute for gx/gz/Sxx/Sxz/masks/timing/product normalization | either acquire official arrays or continue parent-side derivation of the coefficient/range owner |
| DECISION2790_2 | next derivation target is range owner | profile grid shows bulk-vs-finite-range dependence; deciding bulk source legitimacy requires lambda_WEP >> R_E or a common long-range carrier theorem | 2791 should derive WEP range owner or retain lambda-dependent profile rows and route to PREM/readout import |

## Validation
| validation_id | passed | detail |
| --- | --- | --- |
| VAL2790_0_sources | True | every cited source path exists and source needle was found |
| VAL2790_1_kernel_rule | True | effective profile source charge rule is staged |
| VAL2790_2_layer_rows | True | core/mantle composition rows are numeric |
| VAL2790_3_layer_charges | True | core/mantle DD charge vectors are numeric |
| VAL2790_4_profile_grid | True | profile weighting grid is numeric |
| VAL2790_5_profile_gates_block | True | profile closure gates block claims |
| VAL2790_6_readout_gate_blocks | True | official MICROSCOPE readout arrays are not imported |
| VAL2790_7_prediction_nonclaim_missing | True | prediction row remains missing lambda/profile/readout/map inputs |
| VAL2790_8_bound_numeric | True | bound import is positive numeric |
| VAL2790_9_runner_refuses | True | generic product runner refuses DD profile/readout rows as MTS product |
| VAL2790_10_claim_gates_safe | True | all claim gates deny WEP/local-GR claim |
| VAL2790_11_next_target | True | 2791 handoff written |
| VAL2790_12_branch_outputs | True | branch copies exist and contain rows |
| VAL2790_13_csv_parse | True | all generated CSV outputs parse cleanly |
| VAL2790_14_no_claim_flags | True | no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true |
| VAL2790_15_generated_under_post_checkpoint | True | all generated outputs are under post-checkpoint-work |
| VAL2790_16_formalization_untouched | True | formalization-workbench modified-file count remains zero during this run |
| VAL2790_17_pycache_absent | True | scripts __pycache__ absent at validation write |
| VAL2790_OVERALL | True | 2790 stages the finite-range DD source-profile kernel, a two-layer core/mantle profile grid, and the MICROSCOPE readout import gate. Numeric profile rows remain nonclaim because lambda_WEP/range owner, PREM/profile closure, parent-to-DD map, and official readout are still missing. |

## Next Target
| next_id | next_target | objective | include | exclude |
| --- | --- | --- | --- | --- |
| NEXT2790_0_2791 | 2791-Y5-R2FR-WEP-range-owner-or-long-range-limit-theorem-under-AX1090.md | derive whether the local WEP carrier/source response is long range enough for the bulk Earth vector, or retain lambda-dependent profile rows and route to PREM/readout import; do not claim WEP/local-GR | parent mass/range operator; lambda_WEP >> R_E condition; relation to local/R10 lambda; parent-to-DD coefficient pressure point; readout import fallback | measured-G absorption; unit source proxy; DD profile smoke as MTS claim; GitHub; formalization edits |
