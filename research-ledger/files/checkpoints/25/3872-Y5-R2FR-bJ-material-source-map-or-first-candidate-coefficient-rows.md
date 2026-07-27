# 3872 — b_J Material/Source Map or First Candidate Coefficient Rows

Generated: `2026-07-01T06:29:18+00:00`

## Result

3872 stops treating “the coupling” as one foggy missing object. It maps the live source-coupling residual into a finite material/source basis:

`S_A=(s_m0,s_EM,s_nuc,s_e,s_press,s_rad,s_boundary,s_clock,s_geometry)`

The first executable nonclaim envelope is:

`b_J,A <= |Delta_w_A|+|D_X ln J_A_measure|+|c_A_pre|+|delta kappa_A|+|z_readout,A|+|K_arena residual|`

This is not a local-GR, WEP, R10, clock, orbital, or EM pass. It is the first finite coefficient scaffold that lets the next checkpoint try to actually close or fill one coupling family.

## Source Register

Resolved `17/17` source rows.

| source_id | path | needle_found | role |
| --- | --- | --- | --- |
| SRC3872_00_3871_next | source-intake\mts_residuals\P8_Y5_R2FR_3871_NEXT_TARGET.csv | True | 3871 selected material/source map |
| SRC3872_01_3871_theorem | source-intake\mts_residuals\P8_Y5_R2FR_3871_ACTION_MEASURE_OWNER_THEOREM.csv | True | action-measure owner verdict |
| SRC3872_02_3871_bj | source-intake\mts_residuals\P8_Y5_R2FR_3871_BJ_FIRST_SOURCE_ROW_CONTRACT.csv | True | first b_J source-row contract |
| SRC3872_03_3868_inputs | source-intake\mts_residuals\P8_Y5_R2FR_3868_CURRENT_NORMALIZATION_BOUND_INPUT_REQUIREMENTS.csv | True | source/current normalization input requirements |
| SRC3872_04_3868_reduced | source-intake\mts_residuals\P8_Y5_R2FR_3868_REDUCED_ZG_CORE_ROWS.csv | True | reduced source-normalization branch |
| SRC3872_05_3867_schema | source-intake\mts_residuals\P8_Y5_R2FR_3867_SOURCE_BACKED_INPUT_SCHEMA.csv | True | projection consistency schema |
| SRC3872_06_3867_candidates | source-intake\mts_residuals\P8_Y5_R2FR_3867_SOURCE_BACKED_CANDIDATE_ROWS.csv | True | source-backed candidate rows |
| SRC3872_07_3863_charge | source-intake\mts_residuals\P8_Y5_R2FR_3863_CHARGE_CURRENT_SLOT_AUDIT.csv | True | EM binding/source slot audit |
| SRC3872_08_3863_em | source-intake\mts_residuals\P8_Y5_R2FR_3863_EM_SOURCE_SCALE_BOUND.csv | True | EM source-scale envelope |
| SRC3872_09_3819_source | source-intake\mts_residuals\P8_Y5_R2FR_3819_FINITE_SOURCE_NORMALIZATION_RESIDUALS.csv | True | Newton/local-GR source-normalization residual |
| SRC3872_10_3843_queue | source-intake\mts_residuals\P8_Y5_R2FR_3843_SOURCE_FILL_QUEUE.csv | True | source normalization / Hilbert measure lock queue |
| SRC3872_11_3829_coeff | source-intake\mts_residuals\P8_Y5_R2FR_3829_SCALAR_COEFFICIENT_OWNER_MAP.csv | True | local PPN coefficient owner map |
| SRC3872_12_3837_beta | source-intake\mts_residuals\P8_Y5_R2FR_3837_BETA_BOUND_ROWS.csv | True | integrated beta bound row |
| SRC3872_13_1387_fill | source-intake\mts_residuals\P8_Y5_R10_1387_DELTA_W_SOURCE_BETA_FIRST_FILL.csv | True | Delta_w/source-beta first-fill pack |
| SRC3872_14_1052_clock | source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv | True | clock alpha product bound |
| SRC3872_15_1052_wep | source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv | True | WEP alpha/Coulomb projection |
| SRC3872_16_1052_r10 | source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv | True | R10 product-law projection |

## Material / Source Class Map

| material_id | class | basis_component | zero_or_bound_condition | test_arenas | current_status |
| --- | --- | --- | --- | --- | --- |
| MAT3872_0_rest_mass | rest_mass_baryon_lepton | s_m0 | Delta_w_A common mode only; no relative species marker | mass source; WEP; Newton; PPN; orbital | COMMON_MODE_CANDIDATE_NOT_PARENT_SIGNED |
| MAT3872_1_EM_binding_static | electrostatic_magnetic_binding | s_EM | same parent F2 coefficient and same current owner | WEP; clocks; R10; source mass; local GR | FINITE_COMPONENT_ROW_REQUIRED |
| MAT3872_2_nuclear_binding | nuclear_binding_strong_internal | s_nuc | no independent nuclear source marker | WEP; orbital source mass; clocks if transition-sensitive | FINITE_COMPONENT_ROW_REQUIRED |
| MAT3872_3_pressure_kinetic | pressure_kinetic_internal_energy | s_press | pressure/binding terms bounded or shown negligible in chosen limit | Newton; PPN; orbital | BOUND_LIMIT_REQUIRED |
| MAT3872_4_poynting_radiation | radiation_poynting_boundary_flux | s_rad+s_boundary | closed stationary worldtube or explicit flux term | source mass; local GR; orbital; EM | POYNTING_BRIDGE_OPEN_BUT_LOCALIZED |
| MAT3872_5_clock_transition | clock_transition_readout | s_clock | same Xhat/readout normalization as source branch | clock drift; alpha variation | PRODUCT_BOUND_AVAILABLE_MTS_TAU_MISSING |
| MAT3872_6_R10_lab_materials | short_range_source_test_materials | s_geometry+s_EM+s_nuc | lambda profile, beta_source, beta_test, K_R10 all share one convention | R10; fifth-force alpha(lambda) | PROFILE_KERNEL_REQUIRED |
| MAT3872_7_orbital_body | orbital_bulk_source | s_m0+s_press+s_boundary | anti-circularity guard: do not fit away G_ref*M_H | Newtonian limit; orbital; PPN | SOURCE_LEDGER_REQUIRED |
| MAT3872_8_vacuum_exterior | local_vacuum_exterior | s_boundary+s_geometry | compact boundary silence and no extra scalar/local dof | PPN gamma/beta; local GR | BOUNDARY_AND_DOF_GATE_OPEN |

## Coefficient Basis

| basis_id | quantity | formula | promotion_requirement | status |
| --- | --- | --- | --- | --- |
| BAS3872_0_basis | material sensitivity vector | S_A=(s_m0,s_EM,s_nuc,s_e,s_press,s_rad,s_boundary,s_clock,s_geometry) | prevents arbitrary per-test coupling knobs | BASIS_DECLARED_NONCLAIM |
| BAS3872_1_Delta_w | Delta_w_A | Delta_w_A = theta_m0*s_m0^A + theta_EM*s_EM^A + theta_nuc*s_nuc^A + theta_press*s_press^A + theta_rad*s_rad^A + theta_bdy*s_boundary^A + theta_clock*s_clock^A | theta_i must be zero by parent owner or bounded from source-backed material rows | FINITE_LINEAR_BASIS_ROW |
| BAS3872_2_beta_w | beta_w_A | beta_w_A = D_Xhat Delta_w_A = sum_i beta_i*s_i^A + sum_i theta_i*D_Xhat(s_i^A) | composition derivatives vanish only for fixed material branch | FINITE_DERIVATIVE_BASIS_ROW |
| BAS3872_3_measure | D_X ln J_A_measure | D_X ln J_A_measure = sum_i j_i*s_i^A + j_readout,A | zero if parent measure is species-blind and readout-stable | FINITE_MEASURE_ROW |
| BAS3872_4_current | c_A_pre | c_A_pre = sum_i c_i*s_i^A + c_boundary,A | ill-typed under 3870 grammar unless real current/source selector remains | FINITE_CURRENT_SLOT_ROW |
| BAS3872_5_selector | delta kappa_A | delta kappa_A = sum_i kappa_i*s_i^A + kappa_geometry,A | zero only if selected Hilbert/Hamiltonian source is parent-owned | FINITE_SELECTOR_ROW |
| BAS3872_6_envelope | b_J,A | b_J,A <= \|Delta_w_A\|+\|D_X ln J_A_measure\|+\|c_A_pre\|+\|delta kappa_A\|+\|z_readout,A\|+\|K_arena residual\| | all terms share material class and arena projection convention | FIRST_BJ_ENVELOPE_NONCLAIM |

## Arena Projection Contract

| arena_id | arena | projection_formula | required_domain_lock | runner_status |
| --- | --- | --- | --- | --- |
| APC3872_0_WEP | MICROSCOPE_WEP | eta_ST <= \|K_WEP\|*\|beta_source(S)\|*\|beta_test(A)-beta_test(B)\| + b_J,A+B terms | source body class plus two test-material sensitivity vectors | DO_NOT_SCORE_YET |
| APC3872_1_R10 | R10_short_range | alpha_MTS(lambda)=K_R10(lambda;rho_s,rho_t,profile)*beta_source(lambda)*beta_test(lambda)+epsilon_tail(lambda) | source/test density profile and lambda convention | DO_NOT_SCORE_YET |
| APC3872_2_clock | atomic_clock | d ln(nu_1/nu_2)/dX = (S_clock,1-S_clock,2).beta + z_readout_clock | transition readout vector, not bulk source mass | PRODUCT_BOUND_ONLY |
| APC3872_3_Newton_PPN | Newton_PPN_local_GR | delta C_t and beta/gamma residuals <= R_source_normalization_total + b_J + EM/Poynting/source terms | active source density/worldtube selector plus exterior readout | LOCAL_GR_NOT_CLAIMED |
| APC3872_4_orbital | orbital_systems | delta ln mu = delta ln G_ref + delta ln M_H_source + selector/worldtube/boundary residual | bulk source mass and observed GM anti-circularity | ANTI_CIRCULARITY_GUARD |
| APC3872_5_EM | EM_source_and_Poynting | Delta T_EM_source <= Hodge/F2/current normalization + boundary Poynting flux + EM binding source scale | Maxwell stress, charge current and boundary flux under one parent source owner | SOURCE_BRIDGE_OPEN |

## First Candidate Coefficient Rows

| candidate_id | quantity | candidate_formula | missing_for_claim | status |
| --- | --- | --- | --- | --- |
| CAND3872_0_Delta_w_A | Delta_w_A | Delta_w_A = theta · S_A | missing parent theta_i zero proof or numeric upper bounds | READY_FOR_COMPONENT_FILL_NONCLAIM |
| CAND3872_1_beta_w_source | beta_w_source | beta_w_source(S)=beta · S_source + theta · D_X S_source | missing beta_i and fixed-composition proof | READY_FOR_SOURCE_BETA_FILL_NONCLAIM |
| CAND3872_2_beta_w_test | beta_w_test | beta_w_test(T)=beta · S_test + theta · D_X S_test | missing beta_i and readout-domain lock | READY_FOR_TEST_BETA_FILL_NONCLAIM |
| CAND3872_3_J_measure | J_A_measure | D_X ln J_A_measure = j · S_A + j_readout,A | missing species-blind measure descent | READY_FOR_MEASURE_FILL_NONCLAIM |
| CAND3872_4_c_A_pre | c_A_pre | c_A_pre = c · S_A + c_boundary,A | missing zero theorem or finite current-slot coefficient | READY_FOR_CURRENT_SLOT_FILL_NONCLAIM |
| CAND3872_5_kappa_A | kappa_A | delta kappa_A = kappa · S_A + kappa_geometry,A | missing selected-source owner or finite selector row | READY_FOR_SELECTOR_FILL_NONCLAIM |
| CAND3872_6_K_WEP | K_WEP | K_WEP maps source beta and test material differential into eta_ST | missing shared source/test domain lock | KERNEL_ROW_REQUIRED_NONCLAIM |
| CAND3872_7_K_R10 | K_R10(lambda) | K_R10(lambda)=profile convolution of source/test densities and finite-range propagator | missing promoted bound curve and parent beta/kernel coefficients | KERNEL_ROW_REQUIRED_NONCLAIM |
| CAND3872_8_Poynting_boundary | Phi_EM_boundary | epsilon_Poynting = \|int_dt int_boundary S_EM·n dA\|/(M_ref c^2) | missing worldtube closure/flux bound | POYNTING_SOURCE_ROW_REQUIRED_NONCLAIM |
| CAND3872_9_total_bJ | b_J,A | b_J,A <= \|Delta_w_A\|+\|D_X ln J_A_measure\|+\|c_A_pre\|+\|delta kappa_A\|+\|z_readout,A\|+\|K_arena residual\| | missing coefficients and kernels; no scoring | EXECUTABLE_ENVELOPE_NONCLAIM |

## Poynting / EM Source Bridge

| bridge_id | condition_or_formula | effect_on_framework | status |
| --- | --- | --- | --- |
| POY3872_0_do_not_ignore | If the source worldtube is stationary and closed, net flux can vanish; otherwise it must enter Phi_EM_boundary. | retained in CAND3872_8 and APC3872_5 | POYNTING_RETAINED |
| POY3872_1_zero_route | requires closed stationary source worldtube, no radiative leakage, and boundary/reference improvement silence | would remove a source-mass and local-GR residual, but not F2/current normalization | EXACT_CONDITIONAL_ZERO_NOT_SIGNED |
| POY3872_2_bound_route | source-backed bound can be inserted per arena/source class if zero route fails | feeds orbital/source mass/local-GR envelopes | FINITE_BOUND_ROUTE_READY |

## Claim Gates

| gate_id | status | detail | claim_allowed |
| --- | --- | --- | --- |
| G3872_0_sources | PASS | 17/17 sources resolved | False |
| G3872_1_material_map | PASS | 9 classes | False |
| G3872_2_basis | PASS | Delta_w_A,J_A_measure,K_R10(lambda),K_WEP,Phi_EM_boundary,b_J,A,beta_w_source,beta_w_test,c_A_pre,kappa_A | False |
| G3872_3_arenas | PASS | EM_source_and_Poynting,MICROSCOPE_WEP,Newton_PPN_local_GR,R10_short_range,atomic_clock,orbital_systems | False |
| G3872_4_poynting | PASS | explicit Poynting bridge rows written | False |
| G3872_5_no_numeric_fabrication | PASS | candidate values are symbolic/nonclaim | False |
| G3872_6_no_claim | PASS | valid_for_claim=false throughout | False |

## Decisions

| decision_id | decision | because |
| --- | --- | --- |
| DEC3872_0 | replace free coupling talk with material sensitivity vectors | Delta_w/beta/c/kappa are now finite class-basis rows instead of open-ended knobs |
| DEC3872_1 | retain Poynting vector as a source/boundary bridge | EM field momentum/flux can affect source normalization unless stationary boundary silence is proved |
| DEC3872_2 | do not score WEP/R10/clocks/PPN yet | real bounds exist in some arenas but parent beta/kernel/current coefficients are not numeric or theorem-zero |
| DEC3872_3 | next route is first coefficient fill attempt | the finite basis is now declared; progress requires theta/beta/c/kappa/K rows or a theorem-zero for one family |

## Next Target

| next_id | target_checkpoint | objective | why_next |
| --- | --- | --- | --- |
| NEXT3872_0 | 3873-Y5-R2FR-first-coefficient-fill-theta-beta-or-poynting-zero.md | try to zero or source-fill one coefficient family in the 3872 material basis, prioritizing Poynting boundary silence, Delta_w theta-vector commonness, or WEP/R10 beta-source rows | 3872 has converted the coupling problem into finite coefficient families; the next leap is to close one family, not add another abstract audit |

## Bottom Line

3872 moves the framework forward by replacing an unconstrained coupling gap with a finite source/material coefficient basis. The most important practical gain is that Poynting/EM binding is now explicitly carried as a source-normalization bridge instead of being silently ignored. The grim bit remains: no coefficient family is parent-zeroed or numerically sourced yet, so no local test is claimable. The next serious leap is to close one family: `theta_i` commonness, `beta_i` source/test rows, `c_A/kappa_A` slot silence, `K_arena`, or Poynting boundary zero.
