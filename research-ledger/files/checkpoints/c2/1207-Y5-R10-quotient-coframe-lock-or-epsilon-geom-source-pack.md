# 1207 Y5/R10 Quotient Coframe Lock Or Epsilon Geom Source Pack

**Current verdict:** 1207 does **not** prove `epsilon_geom=0`. It proves the important narrower point: quotient/coframe chain-rule descent can kill vertical coframe/shadow-frame leakage if parent-signed, but it does not by itself kill the spatial `nabla_P_loc` term, domain motion, or projector stress.

**Main progress:** primitive `eps_P` stays eliminated. The live object is now the source-pack formula `epsilon_geom=C_P(nabla_P_loc_Linf+coframe_lock_Linf+domain_motion_Linf+projector_stress_Linf)`, with the harsh target `epsilon_geom*G_res_norm <= 1.17233215026e-05` and absorption condition `C_CK*epsilon_geom < 1`.

## Source Register

| source_id | local_path | needle | purpose | path_exists | needle_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1207_0_1206_next | 1206-Y5-R10-KT-boundary-trace-law-or-Ploc-leakage-smallness-derivation.md | NEXT1206_0_1207 | handoff to quotient/coframe lock or epsilon_geom source pack | True | True | False | False |
| SRC1207_1_1206_projector_lowering | source-intake/mts_residuals/P8_Y5_R10_1206_LOWERED_COMPONENT_DERIVATIONS.csv | DRV1206_1_projector_leakage_lowering | epsilon_geom lowered formula from 1206 | True | True | False | False |
| SRC1207_2_1206_pressure | source-intake/mts_residuals/P8_Y5_R10_1206_PRESSURE_COMPARISON.csv | CMP1206_1_projector_lowered_target | projector pressure target epsilon_geom*G_res_norm | True | True | False | False |
| SRC1207_3_943_coframe_contract | source-intake/mts_residuals/P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv | CFC943_7_contract_verdict | coframe coupling parent contract and verdict | True | True | False | False |
| SRC1207_4_863_chain_rule | source-intake/mts_residuals/P8_Y5_R10_863_COFRAME_ZERO_THEOREM.csv | CZT863_5_zero_verdict | conditional coframe chain-rule zero theorem | True | True | False | False |
| SRC1207_5_637_qmap | source-intake/mts_residuals/P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv | QM637_2_vertical_kernel | quotient map vertical-kernel condition | True | True | False | False |
| SRC1207_6_581_quotient_chain | source-intake/mts_residuals/P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv | QVT581_2_matter_factorization | quotient/matter factorization chain | True | True | False | False |
| SRC1207_7_1003_frame_audit | 1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md | CFA1003_6_theorem_verdict | covariant frame/coframe theorem remains unsigned | True | True | False | False |
| SRC1207_8_1029_shadow_frame | 1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md | NST1029_1_chain_rule_zero | no-shadow-frame chain-rule zero conditional theorem | True | True | False | False |
| SRC1207_9_1019_projector | 1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md | PO1019_5_verdict | projector orthogonality remains unsigned | True | True | False | False |

## Epsilon Geom Zero Audit

| audit_id | epsilon_component | zero_route | what_it_really_kills | what_it_does_not_kill | current_status | source_anchor | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZEA1207_0_chain_rule_coframe | coframe_lock_Linf | If e_obs(Phi)=Obs_e(q(Phi)) and Dq[v]=0, then Lie_v e_obs=0 by chain rule. | vertical/readout coframe variation and shadow-frame drift | spatial derivative nabla P_loc or domain-boundary motion | CONDITIONAL_ZERO_NOT_PARENT_SIGNED | P8_Y5_R10_863_COFRAME_ZERO_THEOREM.csv::CZT863_5_zero_verdict | False | False |
| ZEA1207_1_shadow_frame | projector_stress_Linf/frame_channel | If ordinary matter has no independent conformal/disformal/source-frame argument, frame response factors through q and vertical derivative is zero. | hidden matter-frame coupling components such as c_g when no-shadow-frame parent clause is signed | projector stress from changing the projector/domain itself | CONDITIONAL_ZERO_NOT_PARENT_SIGNED | 1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md::NST1029_1_chain_rule_zero | False | False |
| ZEA1207_2_parallel_projector | nabla_P_loc_Linf | Require covariant parallelism or fixed block projector in the selected local domain: nabla P_loc=0. | the derivative projector term in D_T^dagger | coframe/domain/projector-stress variation unless those are separately signed | NOT_DERIVED_BY_QUOTIENT_CHAIN_RULE | 1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md::DTA1195_1_formal_adjoint | False | False |
| ZEA1207_3_domain_motion | domain_motion_Linf | Require the local test domain, boundary, tau-normal, and support map to be fixed by the same parent quotient/readout lock. | moving-domain/coframe support terms in the projector leakage budget | spatial nabla P_loc if the projector varies within the fixed domain | MISSING_PARENT_DOMAIN_LOCK | 1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md::CFA1003_6_theorem_verdict | False | False |
| ZEA1207_4_total_epsilon_zero | epsilon_geom | epsilon_geom=0 only if coframe_lock_Linf=nabla_P_loc_Linf=domain_motion_Linf=projector_stress_Linf=0 in one parent-owned domain. | q_projector as a positive local residual component | q_boundary, q_coker, q_regularizer, official W_R10, or G_res_norm | TOTAL_ZERO_BLOCKED | 1206-Y5-R10-KT-boundary-trace-law-or-Ploc-leakage-smallness-derivation.md::DRV1206_1_projector_leakage_lowering | False | False |

## Epsilon Geom Component Source Pack

| component_id | epsilon_component | definition | zero_certificate_needed | finite_row_columns | current_value | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EGP1207_0_nabla_P_loc | nabla_P_loc_Linf | sup_D \|\|nabla P_loc\|\| in the observed coframe/connection used by D_T | P_loc is covariantly parallel or a fixed parent block projector on the selected local branch | domain_id;norm_id;P_loc_definition_path;connection_path;nabla_P_loc_Linf;units;source_path;valid_for_claim | MISSING | MOST_DANGEROUS_REMAINING_COMPONENT | False | False |
| EGP1207_1_coframe_lock | coframe_lock_Linf | vertical/readout variation norm of e_obs and induced connection under the selected quotient direction | e_obs factors through q and Dq[v]=0 with matter/readout functor signed by parent action | domain_id;norm_id;q_map_path;vertical_generator_path;coframe_descent_path;coframe_lock_Linf;source_path;valid_for_claim | CONDITIONAL_ZERO_IF_PARENT_SIGNED | CHAIN_RULE_READY_PARENT_SIGNATURE_MISSING | False | False |
| EGP1207_2_domain_motion | domain_motion_Linf | motion of local integration domain, boundary support, tau-normal, and source support under quotient/coframe flow | domain/support/tau-normal are quotient-owned fixed readout data in the same branch | domain_id;boundary_map_path;tau_normal_path;support_lock_path;domain_motion_Linf;units;source_path;valid_for_claim | MISSING | DOMAIN_LOCK_MISSING | False | False |
| EGP1207_3_projector_stress | projector_stress_Linf | stress/Ward residual generated by variation of P_loc/projector/readout map | projector variation either has no stress or its stress is carried in the parent Ward identity and projected out | domain_id;projector_variation_path;Ward_identity_path;projector_stress_Linf;units;source_path;valid_for_claim | MISSING | PROJECTOR_STRESS_NOT_SILENT | False | False |
| EGP1207_4_C_P | C_P | operator constant converting summed lower-level leakage norms into epsilon_geom | not a zero component; must be finite and same-norm | domain_id;norm_id;operator_family;C_P;units;source_path;valid_for_claim | MISSING | MISSING_OPERATOR_CONSTANT | False | False |
| EGP1207_5_C_CK_Gres | C_CK_and_G_res_norm | absorption and scoring constants required after epsilon_geom is formed | not zero components; C_CK finite and G_res_norm sourced or theorem-zero | domain_id;norm_id;C_CK;G_res_norm;C_CK_epsilon_geom;epsilon_geom_G_res_norm;source_path;valid_for_claim | MISSING | MISSING_ABSORPTION_AND_SCORE_INPUTS | False | False |

## Pressure And Absorption Gate

| pressure_id | formula | target | gate | absorption_gate | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PGA1207_0_total_formula | epsilon_geom=C_P*(nabla_P_loc_Linf+coframe_lock_Linf+domain_motion_Linf+projector_stress_Linf) | 1.17233215026e-05 | epsilon_geom*G_res_norm <= target | C_CK*epsilon_geom < 1 | FORMULA_READY_VALUES_MISSING | False | False |
| PGA1207_1_if_chain_rule_only | epsilon_geom=C_P*(nabla_P_loc_Linf+domain_motion_Linf+projector_stress_Linf) if coframe_lock_Linf=0 only | 1.17233215026e-05 | still blocked because chain-rule coframe zero does not kill nabla_P_loc/domain/stress | C_CK*C_P*(remaining components)<1 | PARTIAL_ZERO_NOT_ENOUGH | False | False |
| PGA1207_2_total_zero_condition | epsilon_geom=0 | 1.17233215026e-05 | requires every component source row theorem-zero in one domain | automatic if epsilon_geom=0 | BLOCKED_BY_NABLA_PLOC_DOMAIN_PROJECTOR_STRESS | False | False |

## Decision Ledger

| decision_id | condition | decision | result | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| DEC1207_0_verdict | quotient/coframe chain-rule zero closes only part of epsilon_geom | do not claim q_projector=0; stage lower-level epsilon_geom source pack and attack nabla_P_loc/local projector parallelism next | coframe/shadow-frame vertical leakage is conditionally zero, but total epsilon_geom remains blocked by nabla_P_loc, domain_motion, and projector_stress | derive or bound nabla_P_loc_Linf as the highest-value missing component | False | False |

## Claim Gates

| gate_id | gate | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE1207_0_total_epsilon_zero | epsilon_geom=0 | BLOCKED | chain-rule coframe/no-shadow-frame zero does not prove nabla_P_loc=0, domain_motion=0, or projector_stress=0 | False | False |
| GATE1207_1_source_pack_numeric | epsilon_geom numeric score | BLOCKED | all lower-level source rows remain missing or conditional | False | False |
| GATE1207_2_partial_zero_guard | partial zero cannot be promoted to total zero | ACTIVE_GUARD | 1207 explicitly separates coframe vertical zero from spatial projector derivative and domain/stress terms | False | False |
| GATE1207_3_R10_local_GR | R10/local-GR branch | BLOCKED | q_projector, q_boundary, official W_R10, and G_res_norm remain nonclaim/missing | False | False |

## Next Target

| next_id | target_file | target_script | task | success_condition | do_not_do | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1207_0_1208 | 1208-Y5-R10-Ploc-parallel-projector-or-nablaPloc-bound.md | scripts/Y5_R10_Ploc_parallel_projector_or_nablaPloc_bound.py | try to derive P_loc as a covariantly parallel/fixed branch projector in the local GR domain; if not, stage the first source-ready nabla_P_loc_Linf bound row | nabla_P_loc_Linf is theorem-zero, reduced to lower geometry constants, or explicitly source-ready with domain/norm requirements | do not infer spatial nabla_P_loc=0 from vertical quotient descent alone, do not claim R10/local-GR pass, do not edit formalization-workbench, do not push GitHub | False | False |

## Validation

| check_id | check | status | details | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| VAL1207_0_sources_exist | all cited local sources exist | PASS | 10/10 sources exist | False | False |
| VAL1207_1_needles_found | all cited source needles found | PASS | 10/10 needles found | False | False |
| VAL1207_2_chain_rule_present | chain-rule coframe zero route is represented | PASS | ZEA1207_0 present | False | False |
| VAL1207_3_nabla_not_claimed | nabla_P_loc is not falsely zeroed by quotient descent | PASS | nabla_P_loc remains not-derived-by-chain-rule | False | False |
| VAL1207_4_total_zero_blocked | total epsilon zero remains blocked | PASS | epsilon_geom total zero blocked | False | False |
| VAL1207_5_source_pack_complete | epsilon_geom component source pack is complete | PASS | nabla_P_loc_Linf,coframe_lock_Linf,domain_motion_Linf,projector_stress_Linf,C_P,C_CK_and_G_res_norm | False | False |
| VAL1207_6_pressure_preserved | 1206 projector pressure target is preserved | PASS | target=1.17233215026e-05 | False | False |
| VAL1207_7_no_total_zero_claim | no total zero claim is made | PASS | all zero rows nonclaim | False | False |
| VAL1207_8_next_nabla_route | next route targets nabla_P_loc | PASS | 1208-Y5-R10-Ploc-parallel-projector-or-nablaPloc-bound.md | False | False |
| VAL1207_9_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout | False | False |
| VAL1207_10_csv_parse | all generated CSVs parse cleanly | PASS | P8_Y5_R10_1207_SOURCE_REGISTER.csv:10; P8_Y5_R10_1207_EPSILON_GEOM_ZERO_AUDIT.csv:5; P8_Y5_R10_1207_EPSILON_GEOM_COMPONENT_SOURCE_PACK.csv:6; P8_Y5_R10_1207_PRESSURE_AND_ABSORPTION_GATE.csv:3; P8_Y5_R10_1207_DECISION_LEDGER.csv:1; P8_Y5_R10_1207_CLAIM_GATES.csv:4; P8_Y5_R10_1207_NEXT_TARGET.csv:1 | False | False |
| VAL1207_11_formalization_untouched | formalization-workbench untouched during run | PASS | formalization_recent_after_run_start_count=0 | False | False |
| VAL1207_12_overall | overall 1207 validation | PASS | 1207 quotient/coframe epsilon_geom audit is reproducible and nonclaim | False | False |
