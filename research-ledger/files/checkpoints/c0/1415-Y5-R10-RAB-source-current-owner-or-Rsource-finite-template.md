# 1415 - Source-Current Owner Or R_source Finite Template

**Status:** `Y5_R10_1415_source_current_owner_not_derived_Rsource_template_written_nonclaim`

**Current verdict:** a single source-current owner is not derived. `beta_source_alpha` is therefore merged into the broader `R_source` residual as its EM/alpha WEP projection, not treated as an independent escape knob. The same missing object controls source/test current normalization, source-only species weights, Newton-GM normalization, WEP source charge, and R10/R11 source-side rows.

**Discipline move:** no WEP, Newton, R10, PPN, or local-GR claim is made. `R_source` is now an explicit finite nonclaim template with hard anti-shortcuts: no measured-G absorption of relative source weights, no `tau_WEP=1`, no point-source-by-taste, and no transfer of the `beta_source_alpha` target to other arenas.

**Claim ceiling:** `source_current_owner_attempt_and_Rsource_template_only_no_WEP_pass_no_beta_source_pass_no_R10_no_Newton_no_PPN_no_local_GR_pass`

## Source Register

| source_id | source_path | anchor | role | path_exists | anchor_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1415_0_1414_doc | 1414-Y5-R10-RAB-beta-source-alpha-owner-or-finite-bound-row.md | NEXT1414_0_1415 | prior checkpoint selecting source-current owner/R_source merge | True | True | False | False |
| SRC1415_1_1414_owner | source-intake/mts_residuals/P8_Y5_R10_1414_BETA_SOURCE_ALPHA_OWNER_ATTEMPT.csv | BSA1414_5_verdict | beta_source_alpha owner not derived and redirected to source-current owner | True | True | False | False |
| SRC1415_2_1414_bound | source-intake/mts_residuals/P8_Y5_R10_1414_BETA_SOURCE_ALPHA_FINITE_BOUND_ROW.csv | BSB1414_4_score_ready_gate | beta_source_alpha target rows not score-ready | True | True | False | False |
| SRC1415_3_1412_Rsource | source-intake/mts_residuals/P8_Y5_R10_1412_FINITE_RESIDUAL_VECTOR_BRANCH.csv | RV1412_3_R_source | R_source residual component definition | True | True | False | False |
| SRC1415_4_1412_morphism | source-intake/mts_residuals/P8_Y5_R10_1412_VISIBLE_COEFFICIENT_MORPHISM_COUNTEREXAMPLES.csv | MOR1412_3_species_source | species/source coefficient morphism remains live | True | True | False | False |
| SRC1415_5_1077_theorem | source-intake/mts_residuals/P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv | WCO1077_5_verdict | parent WEP coupling owner theorem not closed | True | True | False | False |
| SRC1415_6_1077_clauses | source-intake/mts_residuals/P8_Y5_R10_1077_CLAUSE_SIGNATURE_MATRIX.csv | CLAUSE1077_2_current_owner | current/source normalization owner is missing | True | True | False | False |
| SRC1415_7_1077_counterexamples | source-intake/mts_residuals/P8_Y5_R10_1077_ZERO_THEOREM_COUNTEREXAMPLE_AUDIT.csv | CE1077_1_current_rescaling | current rescaling/source marker counterexample | True | True | False | False |
| SRC1415_8_1076_parent_map | source-intake/mts_residuals/P8_Y5_R10_1076_PARENT_MAP_DERIVATION_ATTEMPT.csv | DER1076_5_verdict | parent material/source map not derived | True | True | False | False |
| SRC1415_9_1076_owner_gates | source-intake/mts_residuals/P8_Y5_R10_1076_COUPLING_OWNER_GATES.csv | OWN1076_4_source_worldtube | current owner and source worldtube missing | True | True | False | False |
| SRC1415_10_1068_worldtube | source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv | SWT1068_5_verdict | source worldtube pack not acquired | True | True | False | False |
| SRC1415_11_1068_force_map | source-intake/mts_residuals/P8_Y5_R10_1068_OBSERVED_FRAME_FORCE_MAP.csv | FRM1068_5_verdict | observed-frame force/readout map not derived | True | True | False | False |
| SRC1415_12_1068_fallback | source-intake/mts_residuals/P8_Y5_R10_1068_DIRECT_PRODUCT_FALLBACK.csv | DPF1068_3_refusal_rule | direct product fallback and refusal rules | True | True | False | False |
| SRC1415_13_1405_response | source-intake/mts_residuals/P8_Y5_R10_1405_PARENT_WEP_RESPONSE_CURRENT_DERIVATION.csv | WRC1405_5_sector_prior_compression | WEP source contraction and P_s form | True | True | False | False |
| SRC1415_14_1409_Ua | source-intake/mts_residuals/P8_Y5_R10_1409_OFFICIAL_READOUT_BLOCKER_LEDGER.csv | ORB1409_7_verdict | U_a official readout/source blocker | True | True | False | False |
| SRC1415_15_this_script | scripts/Y5_R10_RAB_source_current_owner_or_Rsource_finite_template.py | STATUS | generator for this checkpoint | True | True | False | False |

## Source-Current Owner Attempt

| attempt_id | owner_piece | required_statement | current_result | missing_for_claim | if_signed | if_unsigned | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SCO1415_0_target | single source-current owner | source/test current normalization, species weights, beta_source_alpha, and R_source descend from one parent current/measure owner or are explicit residual fields | TARGET_DEFINED | parent object-language, action-measure owner, current owner, source worldtube, and readout/product convention | beta_source_alpha and R_source collapse to common-mode/theorem-owned objects | R_source finite template is mandatory | False | False |
| SCO1415_1_object_language | no source-only species argument | Arg(S_parent) has no w_A(X), kappa_A(X), inert species multiplier, or source-only material slot | CONDITIONAL_UNSIGNED | NoSourceOnlySpeciesSlot / typed object-language theorem from MTS primitives | species/source morphism MOR1412_3 is killed | qbar_source_weight remains live | False | False |
| SCO1415_2_action_measure | species-blind action measure / hbar owner | ordinary matter shares one parent action measure and no species-dependent measure/action multiplier | CONDITIONAL_NOT_PARENT_DERIVED | single measure/action-scale owner signed by parent action | w_A S_A and measure-weight counterexamples are removed | species action weights remain legal counterexamples | False | False |
| SCO1415_3_current_owner | current/source normalization | matter currents and source normalization descend from one current functor, not species/source-specific weights | MISSING | current_id, Noether_owner, charge_unit_owner, source normalization owner, parent basis | beta_source_alpha becomes owned/common-mode | current rescaling/source marker counterexample survives | False | False |
| SCO1415_4_source_worldtube | Earth/source response | source stress-current worldtube/profile is sourced or theorem-reduced to universal common mode | MISSING_SOURCE_WORLDTUBE | T_source^Earth(x), source composition/convention, finite-size correction, frame units | source leg can be projected into WEP/R10/Newton gates | R_source cannot be numeric or score-ready | False | False |
| SCO1415_5_readout_product | source/readout product convention | source-current residual maps to eta_AB/Newton/R10 observables with declared units and official/equivalent readout kernel | BLOCKED_BY_1409_AND_1068 | U_a official arrays/equivalent reconstruction, product convention, observed-frame force map | finite R_source rows could be scored | all R_source rows remain template-only | False | False |
| SCO1415_6_verdict | source-current owner status | SCO1415_1 through SCO1415_5 all close from the parent action and source/readout data | SOURCE_CURRENT_OWNER_NOT_DERIVED_RSOURCE_TEMPLATE_REQUIRED | object-language, measure/current owner, source worldtube, U_a/product convention | R_source and beta_source_alpha can be theorem-owned/common-mode | write R_source finite nonclaim template | False | False |

## R_source Finite Template

| row_id | quantity | definition | formula_or_target | required_inputs | current_value | units | source_anchor | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RSF1415_0_R_source | R_source | qbar_source_weight from w_A(X), kappa_A(X), source-only material multipliers, or source-current normalization residuals | R_source projects into WEP source charge, Newton-GM normalization, R10/R11 source-side rows, and beta_source_alpha EM subchannel | source-current owner theorem or finite source-weight value; units; sign; source path; material/source labels; projection kernel | MISSING | dimensionless or declared parent source-current units | RV1412_3_R_source;SCO1415_6_verdict | FINITE_RSOURCE_TEMPLATE_NONCLAIM | False | False |
| RSF1415_1_qbar_source_weight | qbar_source_weight | species/source-only gravitational prefactor or kappa_A sensitivity | qbar_source_weight = partial_X ln kappa_A or equivalent source-only weight derivative | NoSourceOnlySpeciesSlot theorem or source-weight coefficient; material/source tags; source paths | MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT | dimensionless | MOR1412_3_species_source;CE1077_0_species_action_weight | SOURCE_WEIGHT_ROW_TEMPLATE_NONCLAIM | False | False |
| RSF1415_2_current_rescaling | current_rescaling_residual | J_A -> c_A J_A or beta_source,A source marker residual | finite source/test current normalization component in parent basis | Noether current owner or finite c_A/beta_source,A coefficient rows | MISSING_CURRENT_OWNER_OR_COEFFICIENT | dimensionless or parent current-normalization units | CE1077_1_current_rescaling;SCO1415_3_current_owner | CURRENT_RESCALING_ROW_TEMPLATE_NONCLAIM | False | False |
| RSF1415_3_source_worldtube | source_worldtube_projection | Earth/source stress-current profile and source composition/convention in observed frame | Integral_Earth K_source(x) delta T_source(x)/delta X_I with common-mode GM removed only after universality proof | T_source^Earth(x), source composition/convention, GM calibration, finite-size correction, frame units | MISSING_SOURCE_WORLDTUBE | declared by source-current convention | SWT1068_5_verdict;DER1076_1_source_leg_definition | SOURCE_WORLDTUBE_TEMPLATE_NONCLAIM | False | False |
| RSF1415_4_direct_product | direct_source_product | direct parent variation product from source residual to eta_AB/Newton/R10 observable | derive delta a_AB or eta_AB directly from parent action instead of arbitrary Delta_w*tau split | parent variation with units/source path or both split factors numeric/sourced | MISSING_DIRECT_PARENT_PRODUCT | observable-specific | DPF1068_0_preferred_route;FRM1068_5_verdict | DIRECT_PRODUCT_TEMPLATE_NONCLAIM | False | False |
| RSF1415_5_beta_source_alpha_projection | beta_source_alpha projection | EM/alpha channel projection of R_source into eta_alpha = DeltaQ_alpha beta_source_alpha b_alpha tau_WEP | beta_source_alpha is a subprojection of the same missing source-current normalization owner | R_source owner/value, EM channel map, b_alpha, tau_WEP/U_a, material tensor | TARGET_ONLY_FROM_1414 | dimensionless target ratio if parent-normalized | BSB1414_0_definition;BSB1414_4_score_ready_gate | MERGED_WITH_RSOURCE_NONCLAIM | False | False |
| RSF1415_6_verdict | R_source finite template pack | source-current owner is not derived, so R_source stays as explicit finite residual branch | score_ready iff all RSF1415_0 through RSF1415_5 are theorem-zero or source-backed with U_a/product convention | source-current owner or finite rows, source worldtube, U_a, product convention, arena projection | TEMPLATE_ONLY | not_applicable | SCO1415_6_verdict | RSOURCE_TEMPLATE_READY_VALUES_MISSING | False | False |

## beta_source_alpha / R_source Merge Map

| merge_id | object_a | object_b | relationship | if_owner_signed | if_owner_unsigned | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MER1415_0_common_owner | beta_source_alpha | R_source | beta_source_alpha is the EM/alpha WEP projection of the broader source-current normalization residual | both become common-mode/theorem-owned and no free source suppression is allowed | beta_source_alpha target rows and R_source finite rows remain nonclaim | False | False |
| MER1415_1_not_identical | beta_source_alpha | R_source | beta_source_alpha is not the whole R_source vector; R_source also includes Newton-GM, R10/R11 source-side, and source-only species weight channels | single owner can reduce all source-side channels | do not transfer beta_source_alpha WEP target to other arenas | False | False |
| MER1415_2_score_policy | beta_source_alpha target | R_source score | a target-only beta_source_alpha threshold is not a score-ready R_source bound | score may be unnecessary if source residual is theorem-zero | source-backed values and arena kernels are required | False | False |

## R_source Anti-Shortcut Gate

| shortcut_id | forbidden_shortcut | reason | source_anchor | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| RSS1415_0_no_measured_G_absorption | absorb relative source weights into measured G or GM | common source normalization can be calibrated away only after universality proof; relative source weights cannot | SWT1068_2_GM_calibration;FRM1068_2_common_mode_separation | FORBIDDEN | False | False |
| RSS1415_1_no_tau_unity | set tau_WEP or source kernel to 1 | source worldtube, orbit/readout kernel, and product convention are missing | DPF1068_3_refusal_rule;ORB1409_7_verdict | FORBIDDEN | False | False |
| RSS1415_2_no_point_source_by_taste | replace source worldtube with point-source convention without sourced error bound | finite-size/source support correction and source composition/convention are missing | SWT1068_0_source_stress_profile;SWT1068_3_finite_source_correction | FORBIDDEN | False | False |
| RSS1415_3_no_beta_source_transfer | transfer beta_source_alpha WEP target to Newton, R10, clocks, or PPN | beta_source_alpha is one EM/WEP projection; R_source needs arena-specific kernels and maps | MER1415_1_not_identical | FORBIDDEN | False | False |

## R_source Arena Gate

| arena_id | arena | dependency | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| RSG1415_0_WEP | WEP/source charge | R_source projection, U_a/source worldtube, material tensor, eta product convention | BLOCKED_TEMPLATE_ONLY | R_source has no source-backed value and U_a/product gates remain blocked | False | False |
| RSG1415_1_Newton_GM | Newton/GM normalization | universal source common mode vs relative source residual | BLOCKED_NO_RELATIVE_SOURCE_PROOF | measured-G/GM absorption is forbidden without universality proof | False | False |
| RSG1415_2_R10_R11 | R10/R11 source-side rows | source-current residual, range kernel, bound curve/interface, source composition | BLOCKED_NO_TRANSFER | R_source has no arena-specific projection or source-backed bound rows | False | False |
| RSG1415_3_PPN_local_GR | PPN/local GR | source-current universality plus EH/PPN silence and retained residual vector bounds | BLOCKED_NO_LOCAL_GR_CLAIM | source current owner, U_a, EH/PPN, and residual-vector gates remain open | False | False |

## Decision Ledger

| decision_id | decision | reason | effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1415_0_owner_verdict | do not promote source-current owner | object-language, action-measure, current owner, source worldtube, and product convention remain unsigned or missing | R_source is retained as finite residual template | False | False |
| DEC1415_1_merge | merge beta_source_alpha into R_source as an EM-channel projection | both are symptoms of the same missing source-current normalization owner | no duplicate escape hatches; target-only beta_source rows feed R_source but do not score it | False | False |
| DEC1415_2_next_best | target source-only species slot / current rescaling theorem next | that is the cleanest route to kill R_source without waiting for data | next checkpoint should try to ban Hom(SpeciesLabel,Coeff_active_source) and J_A -> c_A J_A together | False | False |

## Claim Gate

| claim_id | claim | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE1415_0_source_owner | source-current owner is derived | BLOCKED_NO_CLAIM | parent object-language, measure/current owner, source worldtube, and readout/product convention are incomplete | False | False |
| GATE1415_1_Rsource | R_source is zero or bounded | TEMPLATE_ONLY_NO_CLAIM | R_source rows contain no values, signs, units, source paths, or arena projections | False | False |
| GATE1415_2_beta_source_alpha | beta_source_alpha target becomes a pass | BLOCKED_NO_CLAIM | beta_source_alpha is a target-only R_source projection and lacks parent basis/U_a/product convention | False | False |
| GATE1415_3_WEP_Newton_R10 | WEP, Newton-GM, or R10 source-side arenas pass | BLOCKED_NO_CLAIM | source-current owner and arena-specific projections are missing | False | False |
| GATE1415_4_local_GR | local GR/Newton reduction follows | BLOCKED_NO_CLAIM | R_source is only one open residual and EH/PPN/U_a/matter tensor gates remain active | False | False |
| GATE1415_5_verdict | 1415 closes source normalization | NO_PROMOTION | 1415 merges the debt and writes R_source template only | False | False |

## Next Target

| next_id | target_doc | target_script | task | success_condition | do_not_claim | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1415_0_1416 | 1416-Y5-R10-RAB-source-only-species-slot-and-current-rescaling-ban-or-Rsource-bound-row.md | scripts/Y5_R10_RAB_source_only_species_slot_and_current_rescaling_ban_or_Rsource_bound_row.py | try to prove Hom(SpeciesLabel,Coeff_active_source)=empty and forbid J_A -> c_A J_A source-current rescaling; if it fails, make the first finite R_source coefficient row | source-only species/current rescaling morphisms are theorem-banned, or a source-ready R_source coefficient row is written with units/sign/source anchors and nonclaim gates | WEP pass; beta_source_alpha pass; Newton-GM pass; R10/PPN/local GR | False | False |
| NEXT1415_1_data_parallel | future-source-worldtube-and-Ua-import-route.md | future_data_route | if source-worldtube and official/equivalent U_a data become available, fill RSF1415_3 and product convention rows | source profile, composition/convention, finite-size correction, frame units, U_a, and product convention are all source-backed | point-source or tau=1 shortcut | False | False |

## Validation

| check_id | status | detail | timestamp_utc |
| --- | --- | --- | --- |
| VAL1415_0_sources | PASS | all cited local source paths exist and anchors are present | 2026-06-16T03:09:13.697427+00:00 |
| VAL1415_1_owner_attempt | PASS | source-current owner attempt fails and selects R_source template | 2026-06-16T03:09:13.697427+00:00 |
| VAL1415_2_Rsource_template | PASS | R_source finite template exists but contains no promoted values | 2026-06-16T03:09:13.697427+00:00 |
| VAL1415_3_merge_map | PASS | beta_source_alpha is merged as R_source projection without becoming a pass | 2026-06-16T03:09:13.697427+00:00 |
| VAL1415_4_shortcuts | PASS | measured-G, tau=1, point-source, and beta-source transfer shortcuts are forbidden | 2026-06-16T03:09:13.697427+00:00 |
| VAL1415_5_arena_gates | PASS | WEP, Newton-GM, R10/R11, and local-GR gates remain blocked | 2026-06-16T03:09:13.697427+00:00 |
| VAL1415_6_decision | PASS | decision ledger selects source-only species slot/current rescaling ban next | 2026-06-16T03:09:13.697427+00:00 |
| VAL1415_7_claim_refusal | PASS | source owner, R_source, beta_source_alpha, arena, and local-GR claims are refused | 2026-06-16T03:09:13.697427+00:00 |
| VAL1415_8_scope | PASS | outputs are confined to post-checkpoint-work paths | 2026-06-16T03:09:13.697427+00:00 |
| VAL1415_9_overall | PASS | 1415 merges beta_source_alpha into R_source and keeps source-current ownership nonclaim | 2026-06-16T03:09:13.697427+00:00 |
