# 1408 — Sector-Beta Source Fill Queue And U_a Kernel Contract

**Status:** `Y5_R10_1408_sector_beta_source_fill_queue_and_Ua_kernel_contract_written_nonclaim`

**Current verdict:** this checkpoint does not score WEP. It turns the finite WEP branch into a fill queue: `U_a := K_ab(lambda,lab) alpha_source^b` is first, then `beta_EM`, `beta_nuc`, the full `Delta f_s,AB` material tensor, then `beta_e`, `beta_other`, and only last the products `P_s := beta_s^a U_a`.

**Discipline move:** no `P_s` product, WEP pressure score, or cross-arena transfer is allowed until `U_a`, each required `beta_s`, and the material tensor have source-backed rows with units, sign conventions, source anchors, and arena projections. `tau_WEP=1`, surrogate kernels, and one-pair cancellation remain forbidden.

**Claim ceiling:** `fill_queue_and_Ua_kernel_contract_only_no_WEP_pass_no_clock_transfer_no_R10_transfer_no_PPN_no_Newton_no_local_GR_pass`

## Source Register

| source_id | source_path | anchor | role | path_exists | anchor_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1408_0_1407_doc | 1407-Y5-R10-RAB-NoSourceOnlySpeciesSlot-proof-or-sector-beta-source-schema.md | NEXT1407_0_1408 | prior checkpoint selecting sector beta fill queue and U_a kernel contract | True | True | False | False |
| SRC1408_1_1407_schema | source-intake/mts_residuals/P8_Y5_R10_1407_SECTOR_BETA_SOURCE_SCHEMA.csv | SCHEMA1407_8_verdict | strict coefficient schema with missing nonclaim values | True | True | False | False |
| SRC1408_2_1407_gate | source-intake/mts_residuals/P8_Y5_R10_1407_SCHEMA_ACCEPTANCE_GATE.csv | SG1407_5_verdict | schema acceptance remains blocked until values/sources exist | True | True | False | False |
| SRC1408_3_1406_acquisition | source-intake/mts_residuals/P8_Y5_R10_1406_SECTOR_BETA_SOURCE_ACQUISITION.csv | SBAQ1406_7_verdict | sector beta acquisition pack | True | True | False | False |
| SRC1408_4_1405_vector | source-intake/mts_residuals/P8_Y5_R10_1405_SECTOR_RESPONSE_VECTOR_MAP.csv | SVP1405_6_vector_verdict | sector response vector map requiring P_s values | True | True | False | False |
| SRC1408_5_1225_tau_attempt | source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv | TAU1225_6_verdict | tau_WEP/U_a projection not derived | True | True | False | False |
| SRC1408_6_1225_formula | source-intake/mts_residuals/P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv | FORM1225_0_tau_WEP_functional | symbolic WEP source/readout functional | True | True | False | False |
| SRC1408_7_1225_acquisition | source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv | ACQ1225_0_official_readout_arrays | official readout arrays and product convention acquisition rows | True | True | False | False |
| SRC1408_8_1225_shortcuts | source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_ANTI_SHORTCUT_GATES.csv | SHORT1225_0_no_tau_unity | forbids tau_WEP=1 and surrogate kernel shortcuts | True | True | False | False |
| SRC1408_9_1325_fill | source-intake/mts_residuals/P8_Y5_R10_1325_FIRST_FILL_INPUT_MATRIX.csv | IN1325_6_tau_WEP | first fill matrix showing tau_WEP/readout arrays missing | True | True | False | False |
| SRC1408_10_1325_decomp | source-intake/mts_residuals/P8_Y5_R10_1325_WEP_PRODUCT_DECOMPOSITION.csv | DECOMP1325_3_full_finite_tensor | full finite tensor formula-ready but not scoreable | True | True | False | False |
| SRC1408_11_1395_sector_pack | source-intake/mts_residuals/P8_Y5_R10_1395_BINDING_SECTOR_BETA_SOURCE_PACK.csv | SBP1395_5_pack_verdict | sector beta rows explicit but unfilled | True | True | False | False |
| SRC1408_12_1396_beta_EM | source-intake/mts_residuals/P8_Y5_R10_1396_BETA_EM_SOURCE_BOUND_TEMPLATE.csv | BEM1396_6_template_verdict | beta_EM finite source-bound template ready nonclaim | True | True | False | False |
| SRC1408_13_material_tensor | source-intake/mts_residuals/P8_Y5_R10_1079_MATERIAL_TENSOR_CONTRACT.csv | MTC1079_3_uncertainty | full material tensor basis/uncertainty contract still missing | True | True | False | False |
| SRC1408_14_no_cancel | source-intake/mts_residuals/P8_Y5_R10_1087_ALL_MATERIAL_NO_CANCELLATION_POLICY.csv | AMC1087_0_pair_line_forbidden | one-pair cancellation forbidden | True | True | False | False |
| SRC1408_15_1402_isolation | source-intake/mts_residuals/P8_Y5_R10_1402_ARENA_ISOLATION_LEDGER.csv | ISO1402_1_WEP | arena isolation still blocks transfer | True | True | False | False |
| SRC1408_16_this_script | scripts/Y5_R10_RAB_sector_beta_source_fill_queue_and_Ua_kernel_contract.py | STATUS | generator for this checkpoint | True | True | False | False |

## Sector-Beta Source Fill Queue

| queue_id | priority | quantity | why_first | current_status | source_basis | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FQ1408_0_Ua_kernel | P0 | U_a := K_ab(lambda,lab) alpha_source^b | all finite WEP sector coefficients P_s=beta_s^a U_a need the same WEP source/kernel contraction | MISSING_SOURCE_KERNEL_AND_READOUT | TAU1225_6_verdict;FORM1225_0_tau_WEP_functional;ACQ1225_0_official_readout_arrays | derive/source official kernel, source worldtube, orbit average, product normalization, and observed-frame convention | False | False |
| FQ1408_1_beta_EM | P1 | beta_EM^a | EM binding touches WEP, clocks, R10, alpha_EM, and the local EM residual vector | MISSING_BETA_EM_ZERO_OR_BOUND | BEM1396_6_template_verdict;SBP1395_2_beta_EM | derive EM-lock/unique normalization or fill finite beta_EM source-bound template | False | False |
| FQ1408_2_beta_nuc | P1 | beta_nuc^a | nuclear/QCD binding controls WEP material contrast and orbital/source-mass residuals | MISSING_NUCLEAR_SECTOR_BETA_ZERO_OR_BOUND | SBP1395_1_beta_nuc;SBZ1395_1_nuclear_zero | derive QCD/nuclear binding owner or create finite beta_nuc bound row | False | False |
| FQ1408_3_Delta_f_tensor | P1 | Delta f_s,AB | without full material contrast tensor, sector betas cannot be contracted into eta_AB honestly | MISSING_FULL_MATERIAL_TENSOR | MTC1079_3_uncertainty;MAT1068_2_full_tensor;MPM1404_6_full_material_tensor | declare parent basis and source material fractions/uncertainties or keep smoke rows nonclaim | False | False |
| FQ1408_4_beta_e | P2 | beta_e^a | electronic/atomic sector couples to clocks and WEP but is less central than U_a/EM/nuclear blockers | MISSING_ELECTRONIC_SECTOR_BETA_ZERO_OR_BOUND | SBP1395_0_beta_e;SBZ1395_0_electronic_zero | derive electron/readout owner or source finite beta_e bound | False | False |
| FQ1408_5_beta_other | P2 | beta_other^a | guard for omitted material/readout sectors; needed for conservative residual envelope | MISSING_SECTOR_COMPLETENESS_OR_RESIDUAL_ENVELOPE | SBP1395_3_beta_other_guard | prove sector inventory complete or define beta_other envelope | False | False |
| FQ1408_6_Ps_products | P3 | P_s := beta_s^a U_a | derived product rows are only meaningful after U_a and beta_s rows exist | DEPENDENT_ON_FQ1408_0_THROUGH_FQ1408_5 | SVP1405_6_vector_verdict;SCHEMA1407_6_P_s | compute only in a runner after source rows are complete and nonclaim gates pass | False | False |
| FQ1408_7_slot_certificate | PARALLEL_THEOREM_ROUTE | NoSourceOnlySpeciesSlot_certificate | if proved, it can demote source-only weight branch without coefficient fitting | NOT_PROVED_CLOSURE_CONDITION | NSS1407_7_current_verdict | continue proof route separately; do not use it as data-row shortcut | False | False |

## U_a Kernel Contract

| contract_id | component | required_object | current_status | source | claim_effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UAK1408_0_definition | U_a | U_a := K_ab(lambda,lab) alpha_source^b | SYMBOLIC_ONLY | FORM1225_0_tau_WEP_functional | cannot compute P_s without U_a | False | False |
| UAK1408_1_source_worldtube | alpha_source^b | Earth/source stress-current worldtube in observed local frame | MISSING_SOURCE_PROFILE_WEIGHTING | TAU1225_0_source_worldtube;ACQ1225_2_source_worldtube | source side of U_a unavailable | False | False |
| UAK1408_2_readout_kernel | K_ab(lambda,lab) | official or exactly equivalent WEP readout/kernel arrays | OFFICIAL_ARRAYS_NOT_IMPORTED | TAU1225_4_force_readout;ACQ1225_0_official_readout_arrays | no surrogate kernel can promote a claim | False | False |
| UAK1408_3_orbit_average | lab/orbit average | time/session/orbit average matched to the reported eta_AB channel | MISSING_ORBIT_AVERAGE_ARRAYS | TAU1225_1_orbit_average;ACQ1225_3_orbit_average | kernel cannot be normalized to the experiment | False | False |
| UAK1408_4_product_normalization | N_eta/product convention | map from source response x material response x readout kernel to reported Eotvos eta | NORMALIZATION_NOT_FILLED | TAU1225_5_normalization;ACQ1225_1_product_convention | U_a cannot be compared to eta_AB bound | False | False |
| UAK1408_5_observed_frame | e_obs/source frame | same observed frame for force law, source variation, clocks, and readout | CONDITIONAL_FROM_PRIOR_SPINE | TAU1225_2_observed_coframe | frame consistency remains conditional | False | False |
| UAK1408_6_material_tensor_domain | Delta f_s,AB/R_material | material tensor in the same basis as U_a and beta_s | MISSING_FULL_MATERIAL_TENSOR | MTC1079_0_basis;MTC1079_2_response_map | U_a cannot be safely contracted with material rows | False | False |
| UAK1408_7_anti_shortcuts | shortcut guards | no tau_WEP=1, no surrogate kernel claim, no sign/material cancellation | ENFORCED | SHORT1225_0_no_tau_unity;SHORT1225_1_no_surrogate_claim;SHORT1225_3_no_cancellation | prevents fake WEP pass | False | False |
| UAK1408_8_verdict | U_a contract status | all UAK1408_1 through UAK1408_6 complete without MISSING markers | UA_KERNEL_CONTRACT_READY_VALUES_MISSING | 1408 checkpoint | U_a remains nonclaim and blocks P_s products | False | False |

## Source-Ready Template Rows

| template_id | quantity | parent_definition | required_columns | units | dimension_basis | value | uncertainty | sign_convention | source_path | source_anchor | arena_projection | lambda_or_domain | fill_queue_ref | valid_for_claim | claim_allowed | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TEMPLATE1408_0_beta_e | beta_e^a | partial ln E_e / partial X_a | coefficient_id;quantity;parent_definition;units;dimension_basis;value;uncertainty;sign_convention;source_path;source_anchor;arena_projection;lambda_or_domain;fill_status;valid_for_claim;claim_allowed | X_a^-1 or dimensionless per parent coordinate | MISSING_PARENT_COORDINATE_BASIS | MISSING_SOURCE_VALUE | MISSING_UNCERTAINTY | MISSING_SIGN_CONVENTION | MISSING_SOURCE_PATH | MISSING_SOURCE_ANCHOR | clock/fine-structure;WEP;R10 | WEP_LOCAL_DOMAIN_ONLY_UNTIL_TRANSFER | FQ1408_4_beta_e | False | False | SOURCE_READY_TEMPLATE_NONCLAIM |
| TEMPLATE1408_1_beta_nuc | beta_nuc^a | partial ln E_nuc / partial X_a | coefficient_id;quantity;parent_definition;units;dimension_basis;value;uncertainty;sign_convention;source_path;source_anchor;arena_projection;lambda_or_domain;fill_status;valid_for_claim;claim_allowed | X_a^-1 or dimensionless per parent coordinate | MISSING_PARENT_COORDINATE_BASIS | MISSING_SOURCE_VALUE | MISSING_UNCERTAINTY | MISSING_SIGN_CONVENTION | MISSING_SOURCE_PATH | MISSING_SOURCE_ANCHOR | WEP;orbital;R10 | WEP_LOCAL_DOMAIN_ONLY_UNTIL_TRANSFER | FQ1408_2_beta_nuc | False | False | SOURCE_READY_TEMPLATE_NONCLAIM |
| TEMPLATE1408_2_beta_EM | beta_EM^a | partial ln E_EM / partial X_a | coefficient_id;quantity;parent_definition;units;dimension_basis;value;uncertainty;sign_convention;source_path;source_anchor;arena_projection;lambda_or_domain;fill_status;valid_for_claim;claim_allowed | X_a^-1 or dimensionless per parent coordinate | MISSING_PARENT_COORDINATE_BASIS | MISSING_SOURCE_VALUE | MISSING_UNCERTAINTY | MISSING_SIGN_CONVENTION | MISSING_SOURCE_PATH | MISSING_SOURCE_ANCHOR | WEP;clock;R10 | WEP_LOCAL_DOMAIN_ONLY_UNTIL_TRANSFER | FQ1408_1_beta_EM | False | False | SOURCE_READY_TEMPLATE_NONCLAIM |
| TEMPLATE1408_3_beta_other | beta_other^a | partial ln E_other / partial X_a | coefficient_id;quantity;parent_definition;units;dimension_basis;value;uncertainty;sign_convention;source_path;source_anchor;arena_projection;lambda_or_domain;fill_status;valid_for_claim;claim_allowed | X_a^-1 or dimensionless per parent coordinate | MISSING_PARENT_COORDINATE_BASIS | MISSING_SOURCE_VALUE | MISSING_UNCERTAINTY | MISSING_SIGN_CONVENTION | MISSING_SOURCE_PATH | MISSING_SOURCE_ANCHOR | WEP;PPN;readout | WEP_LOCAL_DOMAIN_ONLY_UNTIL_TRANSFER | FQ1408_5_beta_other | False | False | SOURCE_READY_TEMPLATE_NONCLAIM |
| TEMPLATE1408_4_Ua | U_a | K_ab(lambda,lab) alpha_source^b | coefficient_id;quantity;parent_definition;units;dimension_basis;value;uncertainty;sign_convention;source_path;source_anchor;arena_projection;lambda_or_domain;fill_status;valid_for_claim;claim_allowed | inverse response-coordinate or arena-normalized source factor | MISSING_PARENT_COORDINATE_BASIS | MISSING_SOURCE_VALUE | MISSING_UNCERTAINTY | MISSING_SIGN_CONVENTION | MISSING_SOURCE_PATH | MISSING_SOURCE_ANCHOR | WEP only until transfer theorem | WEP_LOCAL_DOMAIN_ONLY_UNTIL_TRANSFER | FQ1408_0_Ua_kernel | False | False | SOURCE_READY_TEMPLATE_NONCLAIM |
| TEMPLATE1408_5_Delta_f | Delta f_s,AB | f_s,A - f_s,B for each material pair and sector | coefficient_id;quantity;parent_definition;units;dimension_basis;value;uncertainty;sign_convention;source_path;source_anchor;arena_projection;lambda_or_domain;fill_status;valid_for_claim;claim_allowed | dimensionless fraction | MISSING_PARENT_COORDINATE_BASIS | MISSING_SOURCE_VALUE | MISSING_UNCERTAINTY | MISSING_SIGN_CONVENTION | MISSING_SOURCE_PATH | MISSING_SOURCE_ANCHOR | WEP material scoring | WEP_LOCAL_DOMAIN_ONLY_UNTIL_TRANSFER | FQ1408_3_Delta_f_tensor | False | False | SOURCE_READY_TEMPLATE_NONCLAIM |
| TEMPLATE1408_6_Ps | P_s | P_s := beta_s^a U_a | coefficient_id;quantity;parent_definition;units;dimension_basis;value;uncertainty;sign_convention;source_path;source_anchor;arena_projection;lambda_or_domain;fill_status;valid_for_claim;claim_allowed | dimensionless Eotvos-response coefficient | MISSING_PARENT_COORDINATE_BASIS | MISSING_SOURCE_VALUE | MISSING_UNCERTAINTY | MISSING_SIGN_CONVENTION | MISSING_SOURCE_PATH | MISSING_SOURCE_ANCHOR | WEP pressure only | WEP_LOCAL_DOMAIN_ONLY_UNTIL_TRANSFER | FQ1408_6_Ps_products | False | False | SOURCE_READY_TEMPLATE_NONCLAIM |
| TEMPLATE1408_7_verdict | source_ready_template_pack | schema rows are ready for later fill; no numeric claim values are present | coefficient_id;quantity;parent_definition;units;dimension_basis;value;uncertainty;sign_convention;source_path;source_anchor;arena_projection;lambda_or_domain;fill_status;valid_for_claim;claim_allowed | declared_per_future_row | declared_per_future_row | TEMPLATE_ONLY | not_applicable | declared_per_future_row | not_applicable | not_applicable | WEP pressure only until transfer gates close | not_applicable | FQ1408_0_through_FQ1408_6 | False | False | TEMPLATE_PACK_READY_NO_VALUES |

## Priority Decision Matrix

| decision_id | priority | target | reason | decision | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| PRI1408_0_Ua_first | P0 | U_a kernel/source contract | shared multiplier for every finite WEP sector product | derive/source U_a before any product scoring | False | False |
| PRI1408_1_EM_nuclear_next | P1 | beta_EM and beta_nuc | largest cross-arena entanglement and active prior blockers | target EM-lock/beta_EM and nuclear/QCD owner or finite bounds next | False | False |
| PRI1408_2_material_tensor_parallel | P1 | Delta f_s,AB full material tensor | no sector beta can be contracted honestly without material tensor | build material tensor in same basis as beta_s and U_a, not just alpha/surface smoke rows | False | False |
| PRI1408_3_e_other_later | P2 | beta_e and beta_other | important for clocks/readout/completeness but depends less directly on current WEP kernel | queue after U_a/EM/nuclear or handle as parallel theorem-zero attempts | False | False |
| PRI1408_4_products_last | P3 | P_s products and WEP pressure runner | products are invalid until input rows are sourced/nonclaim-clean | no runner/scoring until input gates clear | False | False |

## Claim Gate

| claim_id | claim | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE1408_0_Ua | U_a kernel/source contraction is derived or sourced | BLOCKED_NO_CLAIM | source worldtube, readout arrays, orbit average, product normalization, and material basis remain missing | False | False |
| GATE1408_1_sector_betas | sector beta coefficients are claim-ready | BLOCKED_NO_CLAIM | beta_e, beta_nuc, beta_EM, beta_other templates contain no source values | False | False |
| GATE1408_2_material_tensor | full material contrast tensor is available | BLOCKED_NO_CLAIM | Delta f_s,AB remains template-only and alpha/surface smoke rows are not a complete parent basis | False | False |
| GATE1408_3_WEP_pass | WEP branch passes | BLOCKED_NO_CLAIM | 1408 is fill queue/template only and contains no claim-ready products | False | False |
| GATE1408_4_transfer | WEP coefficients transfer to clocks, R10, PPN, or orbital tests | BLOCKED_NO_CLAIM | 1402 arena isolation remains active | False | False |
| GATE1408_5_local_GR | local GR/Newton reduction can be claimed | BLOCKED_NO_CLAIM | fill queue does not close q_loc, lambda_A, EM residuals, source kernel, or PPN projection | False | False |

## Next Target

| next_id | target_doc | target_script | task | success_condition | do_not_claim | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1408_0_1409 | 1409-Y5-R10-RAB-Ua-kernel-first-fill-or-official-readout-blocker-ledger.md | scripts/Y5_R10_RAB_Ua_kernel_first_fill_or_official_readout_blocker_ledger.py | try to fill or bound the first U_a kernel pieces: official WEP readout arrays, source worldtube/profile, orbit average, product normalization, and observed-frame convention; if unavailable, write blocker ledger and keep all P_s products nonclaim | U_a has either source-backed rows with units/sign/source anchors or a precise blocker ledger showing which official/readout data are missing | WEP pass;clock pass;R10 pass;PPN pass;Newton limit;local GR;lambda_A=0;q_loc=0;GitHub-ready result | False | False |

## Validation

| check_id | status | detail | timestamp_utc |
| --- | --- | --- | --- |
| VAL1408_0_sources | PASS | all cited local source paths exist and anchors are present | 2026-06-16T02:23:13.256166+00:00 |
| VAL1408_1_fill_queue | PASS | fill queue prioritizes U_a, beta_EM/beta_nuc, and material tensor | 2026-06-16T02:23:13.256166+00:00 |
| VAL1408_2_Ua_contract | PASS | U_a kernel contract records missing source/readout/material inputs and anti-shortcuts | 2026-06-16T02:23:13.256166+00:00 |
| VAL1408_3_templates | PASS | source-ready templates exist but values remain nonclaim missing | 2026-06-16T02:23:13.256166+00:00 |
| VAL1408_4_priorities | PASS | priority matrix keeps products last and U_a first | 2026-06-16T02:23:13.256166+00:00 |
| VAL1408_5_claim_refusal | PASS | U_a, sector beta, WEP, transfer, and local-GR claims are refused | 2026-06-16T02:23:13.256166+00:00 |
| VAL1408_6_scope | PASS | outputs are confined to post-checkpoint-work paths | 2026-06-16T02:23:13.256166+00:00 |
| VAL1408_7_overall | PASS | 1408 writes the nonclaim sector beta fill queue and U_a kernel contract without scoring WEP | 2026-06-16T02:23:13.256166+00:00 |
