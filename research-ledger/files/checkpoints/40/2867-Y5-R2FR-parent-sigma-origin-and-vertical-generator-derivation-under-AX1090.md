# 2867 - Y5 R2FR Parent sigma_R Origin And Vertical Generator Derivation Under AX1090

Status: `Y5_R2FR_2867_conditional_hessian_law_found_parent_origin_not_derived_Uamp_closure_only`

## Private Verdict

2867 takes the requested derivation shot. The useful result is sharp: there is an exact conditional way for the parent to derive the coupling sign instead of fitting it.

Let the amplitude doublet be `Y_amp=(C_AB, delta_R)^T`. If the parent action supplies a rank-one quadratic block with invariant covector

```text
n = (-sigma_R_source_sign, 1)
U_amp = n dot Y_amp = delta_R - sigma_R_source_sign*C_AB
v_amp = (1, sigma_R_source_sign)
H_amp = n^T L_U n
```

then `n(v_amp)=0`, `H_amp v_amp=0`, and a parent source covector `j_amp=J_U n` gives

```text
J_CAB = -sigma_R_source_sign*J_U
J_R = J_U
J_CAB + sigma_R_source_sign*J_R = 0
```

That is the clean mechanism. It means the sign can be derived from the parent Hessian if the parent supplies the Hessian entries:

```text
sigma_R_source_sign = -H_CR/H_RR = -H_CC/H_CR
H_CC*H_RR - H_CR^2 = 0
```

But the current corpus does not supply `H_CC`, `H_CR`, `H_RR`, the parent `Omega`, the amplitude `DC_amp`, the field-by-field `v_amp`, the boundary charge, or the matter/GM descent. The quotient and DCdagger routes therefore remain conditional/open, not theorem-level.

So the verdict is honest: `U_amp` remains the best closure mechanism, but current evidence demotes it to closure-only. The next move is finite source acquisition for the core rows, not another placeholder score.

## Source Register

| source_id | role | path_exists | anchors_found | missing_anchors | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC2867_0_2866_doc | 2866 selected sigma-origin/vertical-generator derivation | True | True |  | False |
| SRC2867_1_2866_contract | parent action contract clauses | True | True |  | False |
| SRC2867_2_2866_variation | conditional variation algebra | True | True |  | False |
| SRC2867_3_2866_routes | route decision matrix | True | True |  | False |
| SRC2867_4_2866_next | handoff target | True | True |  | False |
| SRC2867_5_2866_validation | 2866 validation | True | True |  | False |
| SRC2867_6_2865_doc | sigma sign/common Green failure | True | True |  | False |
| SRC2867_7_2865_evidence | source sign evidence | True | True |  | False |
| SRC2867_8_2865_green | common Green convention audit | True | True |  | False |
| SRC2867_9_2859_doc | U_amp origin demotion | True | True |  | False |
| SRC2867_10_2858_doc | consistency gate doc | True | True |  | False |
| SRC2867_11_2858_quotient | amplitude quotient compatibility | True | True |  | False |
| SRC2867_12_2857_doc | minimal amplitude generator ansatz | True | True |  | False |
| SRC2867_13_2857_owner | parent ownership gates | True | True |  | False |
| SRC2867_14_2856_obs | variational obstructions | True | True |  | False |
| SRC2867_15_2851_ansatz | common current ansatz | True | True |  | False |
| SRC2867_16_2851_proof | algebraic no-free-lunch proof | True | True |  | False |
| SRC2867_17_2851_req | parent signature requirements | True | True |  | False |
| SRC2867_18_2844_contract | parent amplitude contract | True | True |  | False |
| SRC2867_19_1022_doc | quotient/vertical construction | True | True |  | False |
| SRC2867_20_1022_vqc | vertical quotient construction rows | True | True |  | False |
| SRC2867_21_1038_doc | Omega/DCX closure doc | True | True |  | False |
| SRC2867_22_1038_odc | Omega/DCX closure audit | True | True |  | False |
| SRC2867_23_1038_field | vertical generator field map | True | True |  | False |
| SRC2867_24_590_dvm | DCdagger vertical map | True | True |  | False |
| SRC2867_25_590_field | field-by-field vertical map | True | True |  | False |
| SRC2867_26_590_gate | mapping closure gate | True | True |  | False |
| SRC2867_27_591_cmp | Omega/DCdagger comparison | True | True |  | False |
| SRC2867_28_727_dvm | updated DCdagger vertical map | True | True |  | False |
| SRC2867_29_728_cmp | updated Omega/DCdagger comparison | True | True |  | False |
| SRC2867_30_2821_dqvm | vertical response status | True | True |  | False |
| SRC2867_31_2827_kernel | vertical kernel condition | True | True |  | False |
| SRC2867_32_2836_vt | RAB verticality theorem attempt | True | True |  | False |
| SRC2867_33_2836_guards | verticality guards | True | True |  | False |

## Sigma Origin Route Audit

| route_id | route | derivation_target | status | missing_for_acceptance | sigma_origin_accepted | v_amp_parent_accepted | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SIGROUTE2867_0_hessian | quadratic Hessian / invariant covector | derive sigma from a parent-owned rank-one Hessian H=n^T L_U n with n=(-sigma,1) | CONDITIONAL_FORMULA_DERIVED | parent Hessian entries H_CC,H_CR,H_RR not sourced | False | False | False |
| SIGROUTE2867_1_green | Green/source orientation | derive sigma from parent kinetic sign plus Green orientation | FAIL_CURRENT_EVIDENCE | 2865 found sign/common Green owner missing | False | False | False |
| SIGROUTE2867_2_quotient | quotient kernel | derive v_amp from Dq[v_amp]=0 and U_amp as q-basic retained amplitude | FAIL_CURRENT_EVIDENCE | QCA2858/DQT1505 leave Dq computation open | False | False | False |
| SIGROUTE2867_3_dcdagger | DCdagger/Omega-flat generator | derive v_amp=Omega^{-1}[(DC_amp)^dagger epsilon] | FAIL_CURRENT_EVIDENCE | parent Omega, DC operator and all-field vertical action missing | False | False | False |
| SIGROUTE2867_4_source_doublet | single source current | derive J_CAB=-sigma J_U and J_R=J_U from S_src=<J_U,U_amp> | CONDITIONAL_ALGEBRA_ONLY | J_U, measure and sign origin not parent-sourced | False | False | False |
| SIGROUTE2867_5_boundary_matter | boundary and matter descent | prove V_amp is silent to boundary, matter, GM and full local vector | FAIL_CURRENT_EVIDENCE | boundary charge, matter functor and full vector remain open | False | False | False |

## Hessian Factorisation Test

| hessian_id | object | statement | implication | status | algebraically_valid | missing_for_parent_proof | sigma_derived_from_parent | accepted_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HESS2867_0_amplitude_doublet | Y_amp=(C_AB, delta_R)^T | define n=(-sigma_R_source_sign, 1), U_amp=n dot Y_amp, v_amp=(1, sigma_R_source_sign) | n(v_amp)=0 | DERIVED_ALGEBRA | True | sigma value/sign not parent-owned | False | False | False |
| HESS2867_1_rank_one_H | H_amp = n^T L_U n | matrix form H=[[sigma^2 L_U, -sigma L_U],[-sigma L_U,L_U]] | H v_amp=0 and det(H)=0 | DERIVED_CONDITIONAL | True | parent Hessian matrix not sourced | False | False | False |
| HESS2867_2_extract_sigma | if parent supplies H_CC,H_CR,H_RR with rank one | sigma = -H_CR/H_RR = -H_CC/H_CR and H_CC*H_RR-H_CR^2=0 | sigma is derived from Hessian, not fitted | FORMULA_READY_INPUTS_MISSING | True | H_CC,H_CR,H_RR absent from current parent action | False | False | False |
| HESS2867_3_source_covector | j_amp=J_U*n | j_C=-sigma J_U, j_R=J_U | J_CAB+sigma J_R=0 | DERIVED_CONDITIONAL | True | J_U and worldtube/source measure not sourced | False | False | False |
| HESS2867_4_no_free_ratio | arbitrary source vector j=(j_C,j_R) | cancellation requires j_C/j_R=-sigma and is tuning unless j is parent-parallel to n | rejects post-hoc cancellation | NO_TUNING_GUARD | True | parent parallel-source theorem missing | False | False | False |
| HESS2867_5_verdict | sigma origin from Hessian | conditional formula exists, but current corpus supplies no parent Hessian/operator entries | sigma_R_source_sign not derived | FAIL_CURRENT_CLAIM | False | missing parent quadratic action and signature convention | False | False | False |

## Vertical Generator Derivation Gate

| vertical_id | test | meaning | status | missing_for_acceptance | v_amp_parent_accepted | theorem_claimed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VGEN2867_0_candidate | v_amp=partial_C+sigma partial_R | annihilates U_amp algebraically | CONDITIONAL_PASS | sigma and U_amp not parent-owned | False | False | False |
| VGEN2867_1_parent_chart | parent field chart splits amplitude variables into U_amp plus V_amp | would make v_amp an internal representative direction | OPEN | field chart not sourced | False | False | False |
| VGEN2867_2_actual_Dq | Dq[v_amp]=0 on the parent quotient before variation | would make V_amp unobservable in q-basic readouts | OPEN | QCA2858_1_Dq/DQT1505 says Dq computation missing | False | False | False |
| VGEN2867_3_all_field_action | v_amp acts on metric/coframe, memory/projector/domain, matter/readout and boundary fields | needed to stop leakage into local tests | OPEN | 590/1038 field maps incomplete | False | False | False |
| VGEN2867_4_boundary | v_amp has zero/proper/exact boundary charge | needed for integrated charge identity | OPEN | Q_X/B/K_boundary not computed | False | False | False |
| VGEN2867_5_matter | ordinary matter and measured GM see only quotient variables | needed for Newton/GR source-side reduction | OPEN | matter descent not parent-signed | False | False | False |
| VGEN2867_6_verdict | v_amp is the actual parent vertical generator | not proven in current corpus | FAIL_CURRENT_CLAIM | parent chart, Dq, all-field action and boundary/matter descent missing | False | False | False |

## Quotient Dq Gate

| dq_id | statement | status | missing_for_acceptance | dq_kernel_accepted | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DQ2867_0_chain_rule | if q is parent-defined and Dq[v_amp]=0, then q-basic observables have zero vertical derivative | EXACT_CONDITIONAL | actual q/v_amp/readout functor not sourced | False | False |
| DQ2867_1_RAB_warning | current observer-cell map treats R_AB as explicit residual, so cheap R_AB deletion is not verticality | COUNTER_GUARD | must prove observed coframe/matter basicity | False | False |
| DQ2867_2_kernel_condition | Dq[v]=0 requires the tangent to preserve the actual reciprocal/determinant branch | CONDITIONAL_TEST_AVAILABLE | not evaluated for v_amp because q chart is not parent-owned | False | False |
| DQ2867_3_matter_kernel | matter/local generator kernel must be sourced from matter descent and generator decomposition | NOT_PROVED | KER2827_5_matter_kernel remains unsigned | False | False |
| DQ2867_4_verdict | Dq[v_amp]=0 for actual amplitude vertical generator | FAIL_CURRENT_CLAIM | QCA2858_1_Dq, VQC1022 and DQV2821 are conditional/open | False | False |

## DCdagger Omega Gate

| dcdagger_id | statement | status | missing_for_acceptance | omega_dcdagger_closed | v_amp_parent_accepted | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| DCO2867_0_precise_map | (DC_amp)^dagger epsilon = Omega_parent^flat(v_amp[epsilon]) | FORMAL_ROUTE_VALID | needs parent Omega and DC_amp | False | False | False |
| DCO2867_1_raise_index | v_amp=Omega_parent^{-1}[(DC_amp)^dagger epsilon] on reduced nondegenerate phase space | FORMAL_ROUTE_VALID | Omega inverse/reduced nondegeneracy not supplied | False | False | False |
| DCO2867_2_zero_mode_guard | (DC)^dagger=0 only kills a proper vertical stabilizer after reduced Omega and degeneracies are known | GUARD_ACTIVE | degree count and no proper stabilizer proof missing | False | False | False |
| DCO2867_3_parent_Omega | Omega_parent=delta Theta_parent on full parent variables | MISSING_PARENT_OMEGA | Theta/Omega not extracted for this amplitude sector | False | False | False |
| DCO2867_4_DCamp | DC_amp is the linearized parent amplitude constraint/operator | MISSING_DCAMP_OPERATOR | parent amplitude constraint not written | False | False | False |
| DCO2867_5_field_map | v_amp field action specified on all parent/boundary/matter fields | FIELD_MAP_INCOMPLETE | only candidate maps exist | False | False | False |
| DCO2867_6_verdict | DCdagger/Omega route derives v_amp | FAIL_CURRENT_CLAIM | parent Omega, DC_amp, all-field v_amp, boundary and degree-count missing | False | False | False |

## U_amp Closure Demotion Ledger

| demotion_id | object | status | reason | closure_only_current_status | reentry_allowed_if_parent_signed | runner_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DEM2867_0_Uamp_route | U_amp parent-action route | DEMOTE_CURRENT_CLAIM_TO_CLOSURE_ONLY | sigma origin and vertical generator are not parent-derived | True | False | False | False |
| DEM2867_1_reopen_condition | reopen theorem route | OPEN_REENTRY | source-backed parent Hessian/Omega/Dq/boundary/matter certificate may reopen later | False | True | False | False |
| DEM2867_2_finite_route | finite source acquisition | SELECT_NEXT | fallback must source Q_CAB, q_R_eff, sigma_R_source_sign, boundary/tail, GM and full vector | False | False | False | False |
| DEM2867_3_runner | A_total runner | LOCKED | no scoring until finite rows or parent theorem exist | False | False | False | False |

## Claim Guards

| guard_id | guard | reason | guard_active | claim_prevented | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| GUARD2867_0_no_sigma_claim | do not claim sigma_R_source_sign derived | parent Hessian/sign/Omega route not closed | True | True | False |
| GUARD2867_1_no_vamp_claim | do not claim v_amp is parent vertical | Dq/Omega/all-field action missing | True | True | False |
| GUARD2867_2_no_Uamp_theorem | do not claim U_amp theorem-zero | route is closure-only current status | True | True | False |
| GUARD2867_3_no_A_total_score | do not score A_total | Q_CAB/q_R_eff/sigma still source-incomplete | True | True | False |
| GUARD2867_4_no_local_GR | do not claim local-GR/Newton reduction | matter/GM/full vector not derived | True | True | False |

## Decision Ledger

| decision_id | decision | result | because | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2867_0_hessian_formula | A real derivation route was found in formula form. | CONDITIONAL_SUCCESS | rank-one Hessian/source covector would derive sigma and current locking if parent supplied H and n | False |
| DEC2867_1_current_evidence | Current corpus does not supply that parent Hessian or equivalent Omega/Dq owner. | FAIL_CURRENT_CLAIM | all available quotient/DCdagger evidence is conditional/open | False |
| DEC2867_2_demote | Demote U_amp parent-action route to closure-only current status. | DEMOTED_CURRENT_ROUTE | the candidate remains useful but not theorem-level | False |
| DEC2867_3_next | Move to finite core source acquisition. | SELECTED_2868 | we should now source the rows needed to test instead of circling the same missing parent owner | False |

## Next Target

| next_id | status | target_doc | target_script | mission | selected | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2867_0_2868 | selected_primary | 2868-Y5-R2FR-finite-core-source-acquisition-after-Uamp-closure-demotion-under-AX1090.md | scripts/Y5_R2FR_finite_core_source_acquisition_after_Uamp_closure_demotion_under_AX1090_2868.py | after demoting the U_amp parent-action route to closure-only current status, build a finite nonclaim acquisition pack for Q_CAB, q_R_eff, sigma_R_source_sign, shared Green convention, boundary/tail, measured GM and full local residual vector; no A_total scoring until rows are source-backed | True | False |

## Branch Copies

| copy_id | source_table | copy_path | purpose | exists | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| COPY2867_0_hessian | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2867_HESSIAN_FACTORISATION_TEST.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\beta-source\docs\RAB_SIGMA_HESSIAN_FACTORISATION_2867_NONCLAIM.csv | sigma Hessian factorisation nonclaim copy | True | False |
| COPY2867_1_demotion | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2867_UAMP_CLOSURE_DEMOTION_LEDGER.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\RAB_UAMP_CLOSURE_DEMOTION_2867_NONCLAIM.csv | U_amp closure-only demotion nonclaim copy | True | False |
| COPY2867_2_next_queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2867_NEXT_TARGET.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2867_finite_core_source_acquisition_NEXT.csv | RAB queue handoff to finite acquisition | True | False |
| COPY2867_3_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2867_CLAIM_GUARDS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\RAB_SIGMA_VERTICAL_CLAIM_GUARDS_2867_NONCLAIM.csv | sigma/vertical claim guard nonclaim copy | True | False |

## Validation

| validation_id | passed | detail | timestamp_utc |
| --- | --- | --- | --- |
| VAL2867_0_sources_exist | True | all registered source paths exist | 2026-06-24T14:00:44.359802+00:00 |
| VAL2867_1_source_anchors | True | all registered anchors were found | 2026-06-24T14:00:44.359818+00:00 |
| VAL2867_2_routes_cover_three_derivations | True | sigma origin audit covers Hessian, Green, quotient, DCdagger, source and boundary routes | 2026-06-24T14:00:44.359823+00:00 |
| VAL2867_3_hessian_formula_present | True | rank-one Hessian sigma formula is staged | 2026-06-24T14:00:44.359827+00:00 |
| VAL2867_4_no_sigma_parent_derivation | True | sigma is not marked parent-derived | 2026-06-24T14:00:44.359830+00:00 |
| VAL2867_5_vertical_not_accepted | True | v_amp is not accepted as parent vertical generator | 2026-06-24T14:00:44.359834+00:00 |
| VAL2867_6_quotient_gate_blocked | True | Dq[v_amp]=0 remains blocked | 2026-06-24T14:00:44.359837+00:00 |
| VAL2867_7_dcdagger_gate_blocked | True | DCdagger/Omega route remains blocked | 2026-06-24T14:00:44.359841+00:00 |
| VAL2867_8_uamp_demoted | True | U_amp route is demoted to closure-only current status | 2026-06-24T14:00:44.359844+00:00 |
| VAL2867_9_claim_guards_active | True | claim guards are active | 2026-06-24T14:00:44.359848+00:00 |
| VAL2867_10_next_target_2868 | True | finite core source acquisition selected next | 2026-06-24T14:00:44.359851+00:00 |
| VAL2867_11_outputs_exist | True | all generated output paths exist before validation write | 2026-06-24T14:00:44.359854+00:00 |
| VAL2867_12_branch_outputs_exist | True | branch copies were written | 2026-06-24T14:00:44.359858+00:00 |
| VAL2867_13_csv_parse | True | all generated CSV outputs parse | 2026-06-24T14:00:44.359861+00:00 |
| VAL2867_14_cited_paths_exist | True | all cited local file/copy paths in generated rows exist | 2026-06-24T14:00:44.359865+00:00 |
| VAL2867_15_no_claim_flags | True | no claim/score/prediction flags are true | 2026-06-24T14:00:44.359868+00:00 |
| VAL2867_16_generated_under_post_checkpoint | True | all generated artifacts remain under post-checkpoint-work | 2026-06-24T14:00:44.359872+00:00 |
| VAL2867_17_formalization_untouched | True | formalization-workbench was not modified during this run | 2026-06-24T14:00:44.359875+00:00 |
| VAL2867_18_pycache_absent | True | scripts __pycache__ absent during validation | 2026-06-24T14:00:44.359878+00:00 |
| VAL2867_OVERALL | True | 2867 derives the conditional Hessian/source-covector law for sigma and v_amp, rejects parent-derivation under current evidence, demotes the U_amp parent-action route to closure-only current status, and selects finite core source acquisition for 2868. | 2026-06-24T14:00:44.359888+00:00 |
