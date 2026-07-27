# 1184 - Y5/R10 physical scalar leakage inputs or STF source completion

**Current verdict:** the physical PPN leakage runner is closer but still not scoreable. The math series is controlled, yet `C_C`, `epsilon_D`, `K_S`, `||S_Q||_PPN`, and the q_loc response split are still missing.

**Main progress:** all physical input rows are now explicit, the log-det remainder has a bound `|R3| <= rho^3/(1-rho)` for `||A||_2 <= rho < 1`, and alpha1/alpha2 preferred-frame source candidates are recorded.

**Hard blocker:** the remaining obstacle is no longer the log-det algebra; it is the physical response map and normalization of MTS variables into PPN residuals.

**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.

## Local source register

| source_id | relative_path | needle | role | exists | needle_found |
| --- | --- | --- | --- | --- | --- |
| SRC1184_0_1183_next | source-intake/mts_residuals/P8_Y5_R10_1183_NEXT_TARGET.csv | NEXT1183_0_1184 | handoff to physical scalar leakage inputs or STF source completion. | True | True |
| SRC1184_1_1183_summary | source-intake/mts_residuals/P8_Y5_BRR545_1183_VALIDATION.csv | V1183_SUMMARY | 1183 validation summary. | True | True |
| SRC1184_2_1183_Cdet2 | source-intake/mts_residuals/P8_Y5_R10_1183_SCALAR_LEAKAGE_DERIVATION.csv | SLD1183_3_absolute_bound | canonical C_det2 math coefficient and missing physical normalization. | True | True |
| SRC1184_3_1183_domain | source-intake/mts_residuals/P8_Y5_R10_1183_SCALAR_LEAKAGE_DERIVATION.csv | SLD1183_4_domain_anisotropy | domain anisotropy first-order leakage route. | True | True |
| SRC1184_4_1183_qtrace | source-intake/mts_residuals/P8_Y5_R10_1183_SCALAR_LEAKAGE_DERIVATION.csv | SLD1183_5_q_trace | q_loc trace leakage route. | True | True |
| SRC1184_5_1183_gamma | source-intake/mts_residuals/P8_Y5_R10_1183_UPDATED_PPN_PREDICTION_ROWS.csv | UPPN1183_0_gamma | updated gamma leakage formula. | True | True |
| SRC1184_6_1183_gate | source-intake/mts_residuals/P8_Y5_R10_1183_CLAIM_GATES.csv | G1183_2_gamma_score | gamma leakage remains blocked by physical inputs. | True | True |
| SRC1184_7_1179_KS | 1179-Y5-R10-reciprocal-metric-tracefree-transfer-derivation-or-KS-closure.md | K_S_to_metric = sigma_KS * K_norm | K_S closure decomposition. | True | True |
| SRC1184_8_1010_q_loc | 1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md | retained as an explicit nonclaim residual | q_loc remains retained residual. | True | True |

## External preferred-frame source register

| external_id | title | url | source_role | extracted_comparator | confidence | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| EXT1184_0_Will_PPN_framework | The Confrontation between General Relativity and Experiment | https://link.springer.com/article/10.12942/lrr-2014-4 | PPN/preferred-frame framework reference | framework only; no new numeric bound promoted | framework_reference | False |
| EXT1184_1_Shao_Wex_alpha1_alpha2 | New tests of local Lorentz invariance of gravity with small-eccentricity binary pulsars | https://arxiv.org/abs/1209.4503 | candidate alpha1/alpha2 preferred-frame comparator source | \|alpha_2\| < 1.8e-4 (95% CL); alpha_1 = -0.4^{+3.7}_{-3.1}e-5 (95% CL), from abstract | source_backed_from_arxiv_abstract | False |
| EXT1184_2_Shao_Wex_Kramer_binary_pulsars | New Constraints on Preferred Frame Effects from Binary Pulsars | https://arxiv.org/abs/1209.5171 | supporting preferred-frame binary-pulsar source | preferred-frame alpha1/alpha2 binary-pulsar context; no independent numeric claim promoted here | supporting_source_not_claim_row | False |

## Physical scalar-leakage input ledger

| input_id | quantity | definition | derived_relation | current_status | source_needed | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PLI1184_0_C_C | C_C | parent normalization multiplying the scalar C/log-det memory response | C_det2_phys = \|C_C\|/2 if C_local contains C_C logdet(I+K_S S_Q) | MISSING_PARENT_C_NORMALIZATION | parent C action term and units | False | False |
| PLI1184_1_epsilon_D | epsilon_D | domain anisotropy envelope \|\|W_TF\|\|_D for scalar projection of tracefree shear | leak_domain_linear <= epsilon_D \|K_S\| \|\|S_Q\|\|_D | MISSING_DOMAIN_ANISOTROPY_ENVELOPE | arena domain geometry or parent SO3/isotropy theorem | False | False |
| PLI1184_2_K_S | K_S_to_metric | tracefree transfer coefficient from S_Q to metric/STF residual | K_S_to_metric = sigma_KS K_norm | MISSING_PARENT_ORIENTATION_AND_NORMALIZATION | Q identity or PPN closure source row | False | False |
| PLI1184_3_norm_SQ_PPN | \|\|S_Q\|\|_PPN | PPN-arena tracefree shear norm | if STF bound H_TF exists and K_S != 0, \|\|S_Q\|\|_PPN <= (\|\|H_TF\|\|+\|\|q_TF\|\|+\|\|projector_TF\|\|)/\|K_S\| | MISSING_STF_BOUND_AND_KS | STF/preferred-frame comparator and K_S source | False | False |
| PLI1184_4_q_trace | q_trace | scalar projection of q_loc-induced metric/scalar response, not a literal trace of a vector without a response map | gamma_leak_trace = q_trace + O(q_loc*S_Q) | MISSING_QLOC_RESPONSE_SPLIT | Gamma/Khat/q_loc action or residual response map | False | False |
| PLI1184_5_R3_math | R3_math | third-and-higher log-det remainder after canonical tracefree second-order term | for 3D \|\|A\|\|_2 <= rho < 1, \|R3_math\| <= rho^3/(1-rho) | MATH_BOUND_DERIVED_PHYSICAL_AMPLITUDE_MISSING | rho=\|\|K_S S_Q\|\|_2 arena bound and parent C normalization | False | False |

## R3 remainder bound

| remainder_id | assumption | formula | result | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| R3B1184_0_series | spectral_radius(A)<1 | log det(I+A)=sum_{n>=1} (-1)^{n+1} Tr(A^n)/n | valid local expansion domain identified | MATH_ONLY | False |
| R3B1184_1_tracefree_terms | Tr(A)=0 and A=K_S S_Q | log det(I+A) = -1/2 Tr(A^2) + R3 | linear term vanishes and second-order term is canonical | MATH_ONLY | False |
| R3B1184_2_bound | 3D and \|\|A\|\|_2 <= rho < 1 | \|R3\| <= sum_{n>=3} 3 rho^n/n <= rho^3/(1-rho) | scoreable once rho=\|\|K_S S_Q\|\|_2 is sourced | BOUND_DERIVED_INPUT_MISSING | False |

## Score formula dry-run

| score_id | component | nonclaim_formula | inputs_closed | inputs_missing | score_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SFR1184_0_gamma_bound | gamma_minus_1 | \|gamma_MTS-1\| <= \|delta_gamma_scalar\| + epsilon_D \|K_S\| \|\|S_Q\|\|_PPN + (\|C_C\|/2)\|K_S\|^2\|\|S_Q\|\|_PPN^2 + \|C_C\|R3_math + \|q_trace\| | R3_math formula only | delta_gamma_scalar; epsilon_D; K_S; \|\|S_Q\|\|_PPN; C_C; q_trace; rho | NOT_SCOREABLE | False | False |
| SFR1184_1_STF_bound | H_TF_metric | \|\|H_TF\|\| <= \|K_S\| \|\|S_Q\|\|_PPN + \|\|q_TF\|\| + \|\|projector_TF\|\| | alpha1/alpha2 candidate source rows staged | direct mapping from H_TF to alpha1/alpha2; K_S; S_Q norm; q_TF; projector_TF | NOT_SCOREABLE | False | False |
| SFR1184_2_local_promotion | local_GR_Newton | local promotion requires gamma/beta/STF/q_loc residual vector below sourced tolerances plus parent covariance/conservation gates | none enough for promotion | parent current chain; q_loc split; K_S; physical leakage inputs; residual vector values | REFUSED_NO_LOCAL_CLAIM | False | False |

## Claim gates

| gate_id | claim | status | why | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| G1184_0_physical_Cdet2 | physical C_det2 is known | BLOCKED_PARENT_C_NORMALIZATION_MISSING | math coefficient 1/2 must be multiplied by parent C normalization and units | False | False |
| G1184_1_domain_anisotropy | epsilon_D is known or zero | BLOCKED_DOMAIN_GEOMETRY_OR_ISOTROPY_THEOREM_MISSING | no arena domain geometry or parent SO3 theorem sources epsilon_D | False | False |
| G1184_2_KS_norm | K_S and \|\|S_Q\|\|_PPN are known | BLOCKED_KS_AND_STF_BOUND_MISSING | Q identity/normalization and PPN arena shear norm are not sourced | False | False |
| G1184_3_qtrace | q_trace/q_TF split is known | BLOCKED_QLOC_RESPONSE_SPLIT_MISSING | q_loc remains a retained residual without scalar/STF response map | False | False |
| G1184_4_preferred_frame_sources | preferred-frame comparator source pack is usable for nonclaim runner | PASS_SOURCE_PACK_NONCLAIM | Shao-Wex alpha1/alpha2 source is recorded, but MTS prediction map remains missing | False | False |
| G1184_5_PPN_local | PPN/local-GR pass | BLOCKED_NO_LOCAL_CLAIM | physical leakage and q_loc response inputs remain missing | False | False |

## Decision ledger

| decision_id | decision | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| D1184_0_score_status | do_not_score_gamma_or_STF_yet | R3 math and preferred-frame sources improved the runner, but physical MTS inputs remain missing. | derive q_loc scalar/STF response split or parent C normalization. | False |
| D1184_1_real_progress | R3_remainder_and_alpha_sources_now_staged | the leakage law is closer to scoreable: only physical coefficients/norms remain, not the math series. | use explicit input rows rather than re-deriving logdet again. | False |
| D1184_2_best_next | q_loc_trace_TF_split_is_best_next | q_trace enters gamma at first order and q_TF enters the direct STF channel, so this split affects both PPN routes. | 1185 should derive or bound q_loc scalar/STF response before numeric PPN scoring. | False |

## Validation

| check_id | result | detail | claim_allowed |
| --- | --- | --- | --- |
| V1184_0_sources_exist | pass | all cited local source paths exist and needles are found | False |
| V1184_1_external_urls_recorded | pass | external PPN/preferred-frame source URLs are recorded | False |
| V1184_2_physical_inputs_all_rows | pass | all physical scalar leakage inputs have explicit rows | False |
| V1184_3_R3_bound_derived | pass | R3 remainder bound is derived as math-only/input-missing | False |
| V1184_4_score_rows_nonclaim | pass | score formula rows exist and remain nonclaim | False |
| V1184_5_missing_inputs_not_claim_valid | pass | rows with missing inputs remain invalid for claim | False |
| V1184_6_gates_nonclaim | pass | all gates remain nonclaim | False |
| V1184_7_no_claim_rows | pass | all generated science rows remain nonclaim | False |
| V1184_8_next_target | pass | 1185 handoff targets q_loc trace/TF split or parent C normalization | False |
| V1184_9_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work | False |
| V1184_10_formalization_untouched | pass | generator writes no outputs under formalization-workbench | False |
| V1184_SUMMARY | pass | 1184 stages every physical scalar-leakage input, derives an R3 remainder bound, records alpha1/alpha2 preferred-frame source candidates, refuses PPN scoring, and hands off to q_loc trace/TF response splitting | False |

## Next target

| next_id | next_target | objective | include | exclude | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT1184_0_1185 | 1185-Y5-R10-q_loc-trace-TF-response-split-or-parent-C-normalization.md | derive or bound the scalar trace and STF projections of the retained q_loc/Gamma/Khat residual; if that fails, attempt parent C normalization C_C as the next physical leakage input | P_scalar/P_TF response map; q_trace; q_TF; Gamma/Khat Helmholtz gate; C_C fallback; no-claim validation | claiming q_loc zero; claiming PPN pass; using math coefficients as physical inputs; invented norms; GitHub; formalization edits | False | False |
