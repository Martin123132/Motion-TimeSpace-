# 1183 - Y5/R10 STF preferred-frame source pack or scalar leakage coefficient derivation

**Current verdict:** the scalar leakage route now has a clean math result: pure tracefree `S_Q` has zero first-order scalar leakage, and canonical log-det leakage begins at `-1/2 Tr(A^2)`.

**Main progress:** scalar `gamma` can only see tracefree `S_Q` through domain anisotropy, second-order log-det leakage with parent normalization, or `q_loc` trace. Direct `K_S` still belongs to STF/preferred-frame/tidal channels.

**Hard blocker:** the math coefficient is not yet a physical coefficient. We still need parent `C` normalization, arena `S_Q` norm, domain anisotropy envelope, `q_trace`, and preferred-frame/STF sources.

**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.

## Local source register

| source_id | relative_path | needle | role | exists | needle_found |
| --- | --- | --- | --- | --- | --- |
| SRC1183_0_1182_next | source-intake/mts_residuals/P8_Y5_R10_1182_NEXT_TARGET.csv | NEXT1182_0_1183 | handoff to STF/preferred-frame source pack or scalar leakage coefficient derivation. | True | True |
| SRC1183_1_1182_summary | source-intake/mts_residuals/P8_Y5_BRR545_1182_VALIDATION.csv | V1182_SUMMARY | 1182 validation summary. | True | True |
| SRC1183_2_1182_trace_zero | source-intake/mts_residuals/P8_Y5_R10_1182_SYMBOLIC_PPN_PROJECTION_MAP.csv | PPNP1182_1_trace_projection | pure tracefree scalar gamma projection is zero at first order. | True | True |
| SRC1183_3_1182_gamma_leak | source-intake/mts_residuals/P8_Y5_R10_1182_SYMBOLIC_PPN_PROJECTION_MAP.csv | PPNP1182_2_gamma_leakage | gamma leakage row to sharpen. | True | True |
| SRC1183_4_1182_STF | source-intake/mts_residuals/P8_Y5_R10_1182_SYMBOLIC_PPN_PROJECTION_MAP.csv | PPNP1182_5_anisotropic_channel | direct K_S channel is STF/anistropic. | True | True |
| SRC1183_5_1177_logdet | 1177-Y5-R10-metric-channel-routing-for-tracefree-shear-or-first-shear-norm-row.md | log det(I+A)=Tr(A)-1/2 Tr(A^2)+... | log-det second-order tracefree leakage warning. | True | True |
| SRC1183_6_1178_deltaC2 | 1178-Y5-R10-parent-metric-channel-owner-or-first-tracefree-shear-norm-bound-runner.md | abs(Delta_C2) <= C_det2 | second-order amplitude bound skeleton. | True | True |
| SRC1183_7_1176_domain_anisotropy | 1176-Y5-R10-domain-isotropy-owner-or-tracefree-shear-bound-row.md | domain anisotropy envelope | domain anisotropy first-order leakage source row. | True | True |
| SRC1183_8_1180_Qcoh | 1180-Y5-R10-parent-Q-geometric-identity-or-PPN-KS-source-row.md | Qcoh=(1/3)hX | Qcoh scalar channel cannot own tracefree metric transfer. | True | True |

## External STF/preferred-frame source status

| external_id | title | url | source_role | candidate_parameter | numeric_bound | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EXT1183_0_Will_PPN_framework | The Confrontation between General Relativity and Experiment | https://link.springer.com/article/10.12942/lrr-2014-4 | framework for preferred-frame/STF PPN slots, not a promoted numeric primary row | alpha1; alpha2; anisotropic/preferred-frame PPN bookkeeping | not_promoted_here | FRAMEWORK_ONLY | False |
| EXT1183_1_alpha1_candidate | New limits on preferred-frame effects from pulsar-white dwarf binaries | https://pmc.ncbi.nlm.nih.gov/articles/PMC5253913/ | candidate primary/near-primary alpha1 preferred-frame source; row needs detailed extraction before claim | alpha1 | candidate_order_10^-5_not_promoted | CANDIDATE_SOURCE_NOT_EXTRACTED_FOR_CLAIM | False |
| EXT1183_2_alpha2_needed | alpha2 primary bound source still required | MISSING_PRIMARY_ALPHA2_URL | placeholder until a primary alpha2/STF source is selected and extracted | alpha2 or direct STF/tidal bound | MISSING_PRIMARY_NUMERIC_BOUND | MISSING_SOURCE | False |

## Scalar leakage derivation

| derivation_id | object | formula | result | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SLD1183_0_setup | dimensionless tracefree perturbation | A := epsilon S, Tr(S)=0, \|\|A\|\|<1 | work in the canonical local matrix expansion before physical C-normalization | SETUP | False |
| SLD1183_1_first_order | first-order scalar leakage | delta log det(I+A)\|_1 = Tr(A) = epsilon Tr(S) = 0 | leak_iso_linear = 0 for pure tracefree S_Q in an isotropic scalar projection | DERIVED_ZERO | False |
| SLD1183_2_second_order | canonical second-order scalar leakage | log det(I+A)=Tr(A)-1/2 Tr(A^2)+O(A^3) | Delta_logdet_TF = -1/2 epsilon^2 Tr(S^2)+O(epsilon^3) | CANONICAL_COEFFICIENT_MINUS_HALF | False |
| SLD1183_3_absolute_bound | absolute leakage envelope | \|Delta_logdet_TF\| <= 1/2 \|\|A\|\|_F^2 + R3 | C_det2_math = 1/2 for canonical logdet, but physical C_det2 = \|C_C\|/2 times parent normalization | MATH_BOUND_DERIVED_PHYSICAL_NORMALIZATION_MISSING | False |
| SLD1183_4_domain_anisotropy | non-isotropic scalar projection | leak_domain_linear = <W_TF,S_Q>_D <= \|\|W_TF\|\|_D \|\|S_Q\|\|_D | first-order scalar leakage can return only through domain anisotropy / non-SO3 projection, not canonical isotropic trace | DOMAIN_ANISOTROPY_ROUTE_DERIVED_AS_BOUND | False |
| SLD1183_5_q_trace | q_loc trace leakage | gamma_leak_trace = q_trace + O(q_loc*S_Q) | q_loc trace remains an independent scalar leakage source until Gamma/Khat residual is closed | QLOC_TRACE_RETAINED | False |
| SLD1183_6_verdict | scalar leakage coefficient verdict | gamma_MTS-1 = delta_gamma_scalar + epsilon_D\|\|S_Q\|\| + (\|C_C\|/2)\|\|K_S S_Q\|\|^2 + q_trace + R3 | scalar gamma can test tracefree S_Q only through domain anisotropy, second-order logdet leakage, parent normalization, or q_trace | LEAKAGE_LAW_DERIVED_NONCLAIM | False |

## Updated PPN prediction rows

| ppn_update_id | component | updated_prediction | derived_inputs | still_missing | score_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UPPN1183_0_gamma | gamma_minus_1 | gamma_MTS-1 = delta_gamma_scalar + epsilon_D\|\|S_Q\|\| + (\|C_C\|/2)\|\|K_S S_Q\|\|^2 + q_trace + R3 | linear isotropic tracefree contribution = 0; canonical second-order coefficient = 1/2 | delta_gamma_scalar; epsilon_D; C_C; K_S; \|\|S_Q\|\|_PPN; q_trace; R3 | NOT_SCOREABLE | False | False |
| UPPN1183_1_beta | beta_minus_1 | beta_MTS-1 = delta_beta_scalar + C_beta_TF\|\|K_S S_Q\|\|^2 + C_beta_q\|\|q_loc\|\| + Delta_rec_2 | tracefree enters naturally at second order or through q/domain leakage | C_beta_TF; K_S; \|\|S_Q\|\|; q_loc norm; Delta_rec_2 | NOT_SCOREABLE | False | False |
| UPPN1183_2_STF | H_TF_metric | H_TF = K_S_to_metric S_Q + q_loc_TF + projector_TF | direct K_S channel remains STF/preferred-frame/tidal | primary STF/preferred-frame bound; K_S; S_Q norm; q_loc_TF norm | NOT_SCOREABLE | False | False |

## Claim gates

| gate_id | claim | status | why | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| G1183_0_leak_iso_linear | pure tracefree S_Q leaks into scalar gamma at first order under isotropic projection | FAILED_DERIVED_ZERO | Tr(S_Q)=0 gives delta logdet first order zero | False | False |
| G1183_1_Cdet2_math | canonical logdet second-order coefficient is known | PASS_MATH_ONLY | coefficient is -1/2 before physical C normalization; not a physical claim | False | False |
| G1183_2_gamma_score | gamma leakage is scoreable | BLOCKED_PHYSICAL_NORMALIZATION_AND_NORMS_MISSING | C_C, epsilon_D, K_S, S_Q norm, q_trace, and R3 are missing | False | False |
| G1183_3_STF_preferred_source | direct STF/preferred-frame comparator is source-complete | BLOCKED_ALPHA2_OR_DIRECT_STF_PRIMARY_SOURCE_MISSING | alpha1 candidate exists but alpha2/direct STF source row is incomplete | False | False |
| G1183_4_local_GR_Newton | local GR/Newton limit is derived | BLOCKED_NO_LOCAL_LIMIT_CLAIM | leakage law is nonclaim and physical coefficients/residuals remain missing | False | False |

## Runner dry-run

| run_id | operation | result | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- |
| RUN1183_0_logdet_derivation | derive tracefree logdet leakage through second order | PASS_MATH_NONCLAIM | False | False |
| RUN1183_1_gamma_runner | attempt gamma leakage score | REFUSED_PHYSICAL_INPUTS_MISSING | False | False |
| RUN1183_2_STF_source_pack | stage preferred-frame/STF source rows | PARTIAL_ALPHA1_CANDIDATE_ALPHA2_MISSING | False | False |
| RUN1183_3_local_promotion | local-GR/PPN promotion | REFUSED_NO_LOCAL_CLAIM | False | False |

## Decision ledger

| decision_id | decision | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| D1183_0_derivation_result | scalar_leakage_law_derived_as_nonclaim_math | linear tracefree leak vanishes; canonical second-order logdet coefficient is -1/2 before physical normalization. | source/derive physical C_C, epsilon_D, K_S, S_Q norm, q_trace, and R3. | False |
| D1183_1_STF_status | preferred_frame_source_pack_still_incomplete | alpha1 candidate source is staged but alpha2/direct STF primary source remains missing. | complete alpha1/alpha2 primary extraction or use scalar leakage route first. | False |
| D1183_2_best_next | derive_or_source_physical_leakage_inputs_before_numeric_PPN | without physical normalization and arena norms, PPN numbers cannot score MTS fairly. | 1184 should target C_C/epsilon_D/q_trace/S_Q norm source rows or parent theorem. | False |

## Validation

| check_id | result | detail | claim_allowed |
| --- | --- | --- | --- |
| V1183_0_sources_exist | pass | all cited local source paths exist and needles are found | False |
| V1183_1_linear_leak_zero | pass | linear tracefree scalar leakage is derived zero | False |
| V1183_2_second_order_coeff | pass | canonical logdet second-order coefficient is recorded | False |
| V1183_3_domain_anisotropy_route | pass | domain anisotropy first-order leakage route is bounded | False |
| V1183_4_external_sources_nonclaim | pass | external preferred-frame/STF source rows remain nonclaim | False |
| V1183_5_PPN_updates_nonclaim | pass | updated PPN prediction rows remain nonclaim | False |
| V1183_6_missing_inputs_not_claim_valid | pass | rows with missing inputs remain invalid for claim | False |
| V1183_7_gates_blocked_or_math_only | pass | gates remain blocked or math-only nonclaim | False |
| V1183_8_runner_refuses_claim | pass | dry-runs refuse PPN/local promotion | False |
| V1183_9_no_claim_rows | pass | all generated science rows remain nonclaim | False |
| V1183_10_next_target | pass | 1184 handoff targets physical scalar leakage inputs or STF source completion | False |
| V1183_11_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work | False |
| V1183_12_formalization_untouched | pass | generator writes no outputs under formalization-workbench | False |
| V1183_SUMMARY | pass | 1183 derives zero linear scalar leakage and canonical -1/2 second-order logdet leakage for tracefree S_Q, identifies domain anisotropy/q_trace as first-order scalar leak routes, stages incomplete STF/preferred-frame sources, and keeps PPN nonclaim | False |

## Next target

| next_id | next_target | objective | include | exclude | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT1183_0_1184 | 1184-Y5-R10-physical-scalar-leakage-inputs-or-STF-source-completion.md | derive/source the physical inputs that make the scalar leakage law scoreable: C_C, epsilon_D, K_S, \|\|S_Q\|\|_PPN, q_trace, R3; or complete alpha1/alpha2/direct-STF primary source extraction | parent C normalization; domain anisotropy envelope; S_Q PPN norm; q_loc trace/TF split; preferred-frame sources; no-claim validation | claiming PPN pass; treating math coefficient as physical coefficient; invented norms; GitHub; formalization edits | False | False |
