# 2747 - Y5 R2/f(R): q_R/delta_beta Two-Parameter PPN Control Runner And Zero-Condition Hunt Under AX1090

Status: `Y5_R2FR_2747_two_parameter_control_runner_ready_parent_zero_theorem_missing`

## Private Verdict

2747 makes the local residual branch properly test-shaped.

The control plane is now:

`gamma-1 = q_R`

`beta-1 = delta_beta`

`Delta Mercury / Delta Mercury_GR = (2 q_R - delta_beta)/3`.

This runner can reject trial leak vectors. It cannot score MTS as a prediction, because the parent action still has not produced `q_R`, `delta_beta`, or the zero theorem `q_R=delta_beta=0`.

So the next target is exactly the leap that matters: derive first-order `R_AB=O(L^2)` and second-order `beta=1` from a parent weak-field structure, or demote local GR to bounded closure.

## Source Register

| source_id | description | source_path | exists | needles_present | missing_needles | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2747_0_2746_doc | 2746 selects q_R/delta_beta two-parameter PPN control runner. | 2746-Y5-R2FR-qR-beta-matter-clock-coefficient-source-map-or-rejection-under-AX1090.md | True | True |  | False |
| SRC2747_1_2746_validation | 2746 validation output. | source-intake/mts_residuals/P8_Y5_BRR545_2746_VALIDATION.csv | True | True |  | False |
| SRC2747_2_2746_ppn | live q_R/delta_beta PPN coefficient translation. | source-intake/mts_residuals/P8_Y5_R2FR_2746_PPN_COEFFICIENT_DERIVATION.csv | True | True |  | False |
| SRC2747_3_2746_readiness | live coefficient readiness matrix. | source-intake/mts_residuals/P8_Y5_R2FR_2746_COEFFICIENT_READINESS_MATRIX.csv | True | True |  | False |
| SRC2747_4_2745_budget | live q_R and beta bound budget rows. | source-intake/mts_residuals/P8_Y5_R2FR_2745_BOUND_BUDGET_NONCLAIM.csv | True | True |  | False |
| SRC2747_5_local_bounds | local Cassini gamma and beta bound source rows. | source-intake/local_bounds/local_bound_claims.csv | True | True |  | False |
| SRC2747_6_1559_doc | prior two-parameter runner and zero-condition hunt. | 1559-Y5-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt.md | True | True |  | False |
| SRC2747_7_14_deviation_doc | deviation sensitivity source text. | 14-closure-deviation-PPN-sensitivity.md | True | True |  | False |
| SRC2747_8_10_observer_contract | observer-map contract and zero-condition warning. | 10-observer-map-symplectic-contract.md | True | True |  | False |
| SRC2747_9_2746_queue | live queue into this checkpoint. | source-intake/rab-sector/acquisition-queue/JR2746_TWO_PARAMETER_PPN_CONTROL_NEXT.csv | True | True |  | False |

## Two-Parameter Model

| model_id | observable_response | leak_parameter | coefficient | units | derivation_note | model_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MODEL2747_0_gamma | gamma_minus_1 | q_R | 1 | dimensionless | linear PPN dictionary | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION | False |
| MODEL2747_1_beta | beta_minus_1 | delta_beta | 1 | dimensionless | definition of nonlinear beta drift | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION | False |
| MODEL2747_2_light | solar_light_bending_residual_arcsec | q_R | 0.8756216406841224 | arcsec | theta_GR q_R/2 | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION | False |
| MODEL2747_3_shapiro | solar_Shapiro_residual_microseconds | q_R | 59.7375179242781 | microseconds | delay_GR q_R/2 | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION | False |
| MODEL2747_4_mercury_qR | Mercury_perihelion_residual_arcsec_per_century | q_R | 28.65467507274745 | arcsec/century | GR_perihelion 2 q_R/3 | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION | False |
| MODEL2747_5_mercury_beta | Mercury_perihelion_residual_arcsec_per_century | delta_beta | -14.327337536373726 | arcsec/century | -GR_perihelion delta_beta/3 | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION | False |
| MODEL2747_6_mercury_combo | Mercury_perihelion_fractional_factor | q_R; delta_beta | (2 q_R - delta_beta)/3 | dimensionless | perihelion degeneracy line | PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION | False |

## Parameter Bound Box

| bound_id | parameter_or_combo | local_bound_rows | measured_or_central | one_sigma | control_bound | interpretation | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BOX2747_0_qR | q_R | R3_gamma | 2.1e-05 | 2.3e-05 | 2.3e-05 | q_R = gamma-1 in the PPN translation map | False |
| BOX2747_1_delta_beta | delta_beta | R4_beta | -4.1e-05 | 7.8e-05 | 7.8e-05 | delta_beta = beta-1 by PPN parameter definition; beta row carries its original gamma-prior caveat | False |
| BOX2747_2_perihelion_combo | 2 q_R - delta_beta | R3_gamma; R4_beta | not_independently_fit_here | not_independently_fit_here | derived_combination_only | perihelion constrains the combination through (2 q_R-delta_beta)/3, but no independent Mercury covariance is reconstructed here | False |

## Control Runner

| case_id | label | q_R_input | delta_beta_input | gamma_minus_1 | beta_minus_1 | mercury_residual_arcsec_per_century | control_status | purpose | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CASE2747_0_GR_origin | GR/null closure origin | 0 | 0 | 0 | 0 | 0 | PASS_CONTROL_BOX | baseline origin of q_R/delta_beta plane | False |
| CASE2747_1_Cassini_q_edge | positive q_R bound edge | 2.3e-05 | 0 | 2.3e-05 | 0 | 0.000659057526673 | PASS_CONTROL_BOX | Cassini gamma-edge control point | False |
| CASE2747_2_beta_edge | positive delta_beta bound edge | 0 | 7.8e-05 | 0 | 7.8e-05 | -0.00111753232784 | PASS_CONTROL_BOX | beta edge control point | False |
| CASE2747_3_perihelion_degeneracy | perihelion degeneracy line | 2e-05 | 4e-05 | 2e-05 | 4e-05 | 0 | PASS_CONTROL_BOX | 2 q_R - delta_beta = 0 while gamma/beta bounds still matter | False |
| CASE2747_4_q_fail | q_R too large | 5e-05 | 0 | 5e-05 | 0 | 0.00143273375364 | FAIL_CONTROL_BOX | shows Cassini/gamma clamp | False |
| CASE2747_5_beta_fail | delta_beta too large | 0 | 0.00012 | 0 | 0.00012 | -0.00171928050436 | FAIL_CONTROL_BOX | shows beta clamp | False |

## Parent Zero-Condition Hunt

| zero_id | target_zero | required_statement | mathematical_content | status | next_derivation_step | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ZERO2747_0_qR_linear | q_R=0 | parent equations must force R_AB=O(L^2), not R_AB=q_R L | linear reciprocal strain coefficient vanishes | MISSING_PARENT_FIELD_EQUATION | derive first-order observer-sector equation whose regular/local-vacuum solution has T^2 S=1+O(L^2) | False |
| ZERO2747_1_qR_charge | q_R=0 | no reciprocal boundary/current charge may source R_AB at O(L) | Q_R local charge is zero or pure gauge with proper boundary term | MISSING_ZERO_CHARGE_THEOREM | supply first-class constraint/no-boundary-charge proof rather than closure axiom | False |
| ZERO2747_2_qR_matter | q_R observed by matter | matter and photons must read the same T,S coframe, otherwise gamma translation is not universal | universal coframe descent | MISSING_MATTER_DESCENT | derive matter action descent through the same observer map | False |
| ZERO2747_3_beta_second_order | delta_beta=0 | second-order weak-field completion must match beta=1 in a valid PPN gauge | nonlinear source self-coupling equals GR control lane | MISSING_SECOND_ORDER_PARENT_COMPLETION | derive O(U^2) metric/coframe field equation and coordinate/gauge map | False |
| ZERO2747_4_beta_conservation | delta_beta=0 | Bianchi/conservation identity must fix the nonlinear potential terms consistently | local conservation closes source normalization and beta completion | MISSING_BIANCHI_SOURCE_IDENTITY | derive the parent identity linking field equations to matter conservation | False |
| ZERO2747_5_no_extra_modes | q_R=0 and delta_beta=0 | extra finite-range/scalar/tracefree modes must decouple or be suppressed locally | no surviving local hair in the PPN residual vector | MISSING_MODE_DECOUPLING_THEOREM | derive decoupling/suppression or keep local branch as bounded closure | False |

## Claim Gates

| claim_gate_id | claim_gate | status | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| GATE2747_0_control_runner | two-parameter PPN control runner | PASS_NONCLAIM_CONTROL | control-plane arithmetic works and can reject trial leak vectors | False |
| GATE2747_1_parent_prediction | MTS predicts q_R and delta_beta | BLOCKED_NO_CLAIM | no parent equations produce q_R/delta_beta values | False |
| GATE2747_2_GR_origin | MTS derives local GR origin q_R=0, delta_beta=0 | BLOCKED_NO_CLAIM | zero-condition ledger remains unsigned | False |
| GATE2747_3_matter_universal | local bounds apply to all matter/photons | BLOCKED_NO_CLAIM | matter/coframe descent still missing | False |
| GATE2747_4_empirical_score | empirical MTS local-bound score | BLOCKED_NO_CLAIM | runner can score hypothetical vectors, not the theory | False |

## Decision Ledger

| decision_id | decision | result | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2747_0_verdict | two-parameter local control status | CONTROL_RUNNER_READY_ZERO_THEOREM_MISSING | q_R/delta_beta local residuals are now test-shaped, but the parent theory has not derived the GR origin | False |
| DEC2747_1_first_parent_target | first zero target should be q_R linear | Q_R_LINEAR_FIRST | without R_AB=O(L^2), Cassini kills any generic O(L) reciprocal hair | False |
| DEC2747_2_beta_target | second zero target is beta completion | DELTA_BETA_SECOND_ORDER | beta only becomes meaningful after second-order weak-field/source-normalization closure | False |
| DEC2747_3_next | next target | NEXT_2748_PARENT_WEAK_FIELD_ZERO_CONDITION_DERIVATION | attack the parent equations needed for q_R=0 and delta_beta=0, or demote local GR to bounded closure | False |

## Next Target

| next_id | status | target_doc | target_script | mission | acceptance | forbidden | selected | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT2747_0_2748 | selected_primary | 2748-Y5-R2FR-parent-weak-field-zero-condition-derivation-or-demotion-under-AX1090.md | scripts/Y5_R2FR_parent_weak_field_zero_condition_derivation_or_demotion_under_AX1090_2748.py | attempt to derive the first-order q_R=0 condition and second-order delta_beta=0 condition from a parent weak-field field-equation/action structure; if this fails, demote the local GR branch to an explicit bounded-closure control lane | derive parent first-order R_AB=O(L^2) and second-order beta=1 conditions, or write exact missing field-equation/action clauses and demotion language | do not use the PPN control runner as a parent derivation; do not claim local GR/Newton reduction; do not edit formalization-workbench | True | False |

## Branch Copies

| copy_id | source_table | copy_path | purpose | exists | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BR2747_0_runner | source-intake/mts_residuals/P8_Y5_R2FR_2747_TWO_PARAMETER_CONTROL_RUNNER_NONCLAIM.csv | source-intake/local_bounds/qR_delta_beta_control_runner_2747_NONCLAIM.csv | local-bound two-parameter qR/delta-beta control runner | True | False |
| BR2747_1_zero_hunt | source-intake/mts_residuals/P8_Y5_R2FR_2747_PARENT_ZERO_CONDITION_HUNT.csv | source-intake/source-weight/parent_zero_condition_hunt_2747_NONCLAIM.csv | source-weight parent zero-condition hunt | True | False |
| BR2747_2_next_queue | source-intake/mts_residuals/P8_Y5_R2FR_2747_NEXT_TARGET.csv | source-intake/rab-sector/acquisition-queue/JR2747_PARENT_WEAK_FIELD_ZERO_CONDITION_NEXT.csv | RAB acquisition queue for parent weak-field zero-condition derivation | True | False |

## Validation

| validation_id | passed | detail | timestamp_utc |
| --- | --- | --- | --- |
| VAL2747_0_sources | True | all source paths exist and required anchors/needles are present | 2026-06-23T14:30:37.720087+00:00 |
| VAL2747_1_model_q_beta | True | q_R and delta_beta unit translation rows present | 2026-06-23T14:30:37.720102+00:00 |
| VAL2747_2_bound_box | True | q_R and delta_beta bound box written | 2026-06-23T14:30:37.720105+00:00 |
| VAL2747_3_GR_origin_passes | True | GR origin passes control box | 2026-06-23T14:30:37.720108+00:00 |
| VAL2747_4_q_fail_fails | True | oversized q_R fails Cassini/gamma bound | 2026-06-23T14:30:37.720111+00:00 |
| VAL2747_5_degeneracy_line | True | perihelion degeneracy example has zero Mercury residual | 2026-06-23T14:30:37.720113+00:00 |
| VAL2747_6_zero_conditions | True | parent zero-condition hunt ledger written | 2026-06-23T14:30:37.720116+00:00 |
| VAL2747_7_claim_gates | True | local GR derivation remains blocked and flags false | 2026-06-23T14:30:37.720119+00:00 |
| VAL2747_8_next_target | True | next target is parent weak-field zero-condition derivation or demotion | 2026-06-23T14:30:37.720121+00:00 |
| VAL2747_9_branch_outputs | True | branch copies exist | 2026-06-23T14:30:37.720124+00:00 |
| VAL2747_10_csv_parse | True | P8_Y5_R2FR_2747_SOURCE_REGISTER.csv:10:ok; P8_Y5_R2FR_2747_TWO_PARAMETER_MODEL.csv:7:ok; P8_Y5_R2FR_2747_PARAMETER_BOUND_BOX_NONCLAIM.csv:3:ok; qR_delta_beta_control_runner_2747_NONCLAIM.csv:6:ok; parent_zero_condition_hunt_2747_NONCLAIM.csv:6:ok; P8_Y5_R2FR_2747_CLAIM_GATES.csv:5:ok; P8_Y5_R2FR_2747_DECISION_LEDGER.csv:4:ok; P8_Y5_R2FR_2747_NEXT_TARGET.csv:1:ok; P8_Y5_R2FR_2747_BRANCH_COPIES.csv:3:ok; JR2747_PARENT_WEAK_FIELD_ZERO_CONDITION_NEXT.csv:1:ok | 2026-06-23T14:30:37.720127+00:00 |
| VAL2747_11_pycache_absent | True | scripts __pycache__ absent=True | 2026-06-23T14:30:37.720139+00:00 |
| VAL2747_12_formalization_untouched | True | formalization-workbench recent modified-file count since script start = 0 | 2026-06-23T14:30:37.720142+00:00 |
| VAL2747_OVERALL | True | 2747 builds the q_R/delta_beta two-parameter PPN control runner and selects parent weak-field zero-condition derivation next | 2026-06-23T14:30:37.720150+00:00 |

## Plain-English Read

This is the good kind of constraint. We now have a local control runner that can say exactly how much `q_R` and `delta_beta` are allowed, and it exposes the Mercury degeneracy rather than hiding it. But the theory still has to earn the origin: the parent weak-field equations must kill the linear reciprocal hair and fix the second-order beta term. That is the next serious derivation target.
