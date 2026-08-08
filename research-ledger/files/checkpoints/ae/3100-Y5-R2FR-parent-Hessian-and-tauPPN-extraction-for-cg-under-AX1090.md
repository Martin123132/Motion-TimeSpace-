# 3100 - Y5 R2FR parent Hessian and tau_PPN extraction for c_g under AX1090

**Progress:** 3100 performs the extraction attempt selected by 3099. It scans the current AX1090 branch for parent-owned `Z_X`, `M_X^2`, `tau_PPN`, and `S_PPN` source values rather than treating symbolic formulas as claim-grade inputs.

**Current verdict:** no source-backed numeric parent inputs were extracted. The corpus contains the right symbolic socket, but not the parent-signed coefficients or PPN response matrix needed to bind raw `c_g` or claim local GR/PPN success.

**Claim ceiling:** no direct `c_g` component bound, PPN pass, local-GR/Newton reduction, R10 pass, GitHub action, or `formalization-workbench` edit is allowed from 3100.

## Source Register
| source_id | path | exists | parseable | needles_found | missing_needles | role |
| --- | --- | --- | --- | --- | --- | --- |
| SRC3100_00_3099_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3099_NEXT_TARGET.csv | True | True | True |  | 3099 selects parent Hessian and tau_PPN extraction. |
| SRC3100_01_3099_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3099-Y5-R2FR-canonical-X-normalization-and-range-gate-for-cg-under-AX1090.md | True | True | True |  | 3099 derives the invariant PPN-facing coupling and missing-input verdict. |
| SRC3100_02_3099_zx_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3099_ZX_MX2_TAUPPN_INPUT_GATE.csv | True | True | True |  | 3099 explicit normalization/range/tau input gate. |
| SRC3100_03_3099_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3099_CG_NORMALIZED_BOUND_ROW.csv | True | True | True |  | 3099 normalized c_g bound row remains nonclaim. |
| SRC3100_04_3093_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3093-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row-under-AX1090.md | True | True | True |  | 3093 current AX1090 parent owner/Hessian audit. |
| SRC3100_05_3093_hessian | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3093_PARENT_HESSIAN_AUDIT.csv | True | True | True |  | 3093 Hessian input checklist. |
| SRC3100_06_3093_locks | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3093_FIELD_NORMALIZATION_LOCKS.csv | True | True | True |  | 3093 field-normalization lock status. |
| SRC3100_07_3094_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3094-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return-under-AX1090.md | True | True | True |  | 3094 parent metric/eigenvalue route status. |
| SRC3100_08_3094_beta | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3094_BETA_EIGENVALUE_ATTEMPT.csv | True | True | True |  | 3094 beta/range eigenvalue ownership failure. |
| SRC3100_09_1030_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md | True | True | True |  | 1030 tau_PPN and single-public-metric zero-route provenance. |
| SRC3100_10_1030_provenance | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv | True | True | True |  | 1030 machine-readable tau_PPN provenance gate. |
| SRC3100_11_3098_assumptions | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3098_SCALAR_TENSOR_ASSUMPTION_GATE.csv | True | True | True |  | 3098 scalar-tensor assumption gate. |

## Parent Input Extraction Scan
| scan_id | target_input | symbolic_hit_count | accepted_numeric_hit_count | rejected_numeric_hit_count | current_status | needed_for |
| --- | --- | --- | --- | --- | --- | --- |
| EX3100_0_ZX | Z_X | 119 | 0 | 0 | MISSING_PARENT_NUMERIC_INPUT | N_X=1/sqrt(Z_X) and raw c_g bound |
| EX3100_1_MX2 | M_X^2 | 54 | 0 | 2 | MISSING_PARENT_NUMERIC_INPUT | lambda_X=sqrt(Z_X/M_X^2) range classification |
| EX3100_2_tauPPN | tau_PPN | 43 | 0 | 2 | MISSING_PPN_RESPONSE_MATRIX | turning alpha_eff_PPN into a c_g component bound |
| EX3100_3_SPPN | S_PPN(lambda_X,environment) | 24 | 0 | 0 | MISSING_RANGE_SCREENING_TRANSFER | deciding Cassini vs R10/orbital arena |
| EX3100_4_cross_sector_silence | cross-sector silence | 3 | 0 | 0 | MISSING_CROSS_SECTOR_SILENCE | one-parameter c_g PPN claim |
| EX3100_5_single_public_metric_zero | c_g=0 zero theorem | 11 | 0 | 0 | ZERO_ROUTE_TARGET_NOT_DERIVED | silencing the local PPN coupling rather than bounding it |

## Parent Action Contract Required
| contract_id | required_clause | minimal_formula | current_status | why_it_matters |
| --- | --- | --- | --- | --- |
| PAC3100_0_same_variable_owner | Declare a single parent field or quotient residual Xhat used by the Hessian, matter frame, source current, and local projection. | Xhat = Xhat[Phi] with delta S_parent/dXhat, delta^2 S_parent/dXhat^2, and delta ln A_m/dXhat all referring to the same variable. | NOT_SIGNED | prevents mixing a stability variable with a different coupling variable |
| PAC3100_1_quadratic_hessian | Give the local quadratic parent block with sign, units, and domain. | S_X^(2)=(M_Pl^2/2) int sqrt(-g) [Z_X g^mn partial_m Xhat partial_n Xhat - M_X^2 Xhat^2] plus boundary terms | MISSING_ZX_MX2_VALUES | fixes N_X and lambda_X without post-hoc fitting |
| PAC3100_2_matter_frame_choice | Choose either the zero route or the finite coupling route. | zero: S_matter=Sbar[psi,e_pub(q(Phi))]; finite: g_m=A_g(Xhat)^2 g_E with c_g=d ln A_g/dXhat\|0 | CHOICE_NOT_PARENT_SIGNED | determines whether c_g should vanish or be source-bounded |
| PAC3100_3_source_current | State whether J_X and boundary flux vanish, or provide source-normalized coefficient rows. | delta_X S_matter = int sqrt(-g) J_X delta Xhat and boundary_X=0 or bounded | MISSING_SOURCE_CURRENT_OR_ZERO_THEOREM | needed for no-hair/local-vacuum and fifth-force amplitude rows |
| PAC3100_4_ppn_projection | Define the weak-field response matrix from Xhat to PPN gamma/beta in a gauge and readout frame. | delta gamma = M_gammaX delta Xhat_canonical + sum_i M_gammai delta u_i; tau_PPN := M_gammaX with no-cancellation envelope | MISSING_TAUPPN_RESPONSE_MATRIX | needed to use Cassini as an MTS component bound |
| PAC3100_5_range_transfer | Provide S_PPN(lambda_X,environment) and arena transfer rules. | S_PPN -> 1 for unscreened solar-long branch, Yukawa/finite-source kernel otherwise | MISSING_RANGE_SCREENING_TRANSFER | prevents applying Cassini to a short-range or screened mode |
| PAC3100_6_cross_sector_control | Prove cross-Hessian/disformal/non-Hilbert/support/boundary terms are zero or include them in the PPN residual vector. | alpha_eff_vector = (tau_X c_g/sqrt(Z_X), b_dis, q_nonH, Delta_support, Delta_boundary) with absolute envelope | MISSING_NO_CANCELLATION_VECTOR | prevents hiding a failure or success in untracked components |
| PAC3100_7_verdict | All clauses above must be parent-signed before local-GR/PPN claims. | claim_allowed = all(PAC3100_0..PAC3100_6 signed) | CONTRACT_REQUIRED_NOT_CURRENTLY_SIGNED | sets the exact target for the next derivation attempt |

## tau_PPN Response Contract
| tau_id | required_piece | equation | current_status |
| --- | --- | --- | --- |
| TRC3100_0_background | background and perturbation variables | g_mn=eta_mn+h_mn, Xhat=Xhat_0+delta Xhat, other residuals delta u_i | NOT_ASSEMBLED |
| TRC3100_1_gauge_readout | PPN gauge and measured-frame convention | identify gamma from spatial curvature per unit Newtonian potential in the matter readout frame | NOT_ASSEMBLED |
| TRC3100_2_response_matrix | linearized response matrix | delta gamma = M_gammaX delta Xhat_canonical + M_gammadis b_dis + M_gammanonH q_nonH + ... | MISSING_PPN_RESPONSE_MATRIX |
| TRC3100_3_component_projection | component projection for c_g | tau_PPN := M_gammaX after canonical normalization and range transfer | MISSING_TAUPPN |
| TRC3100_4_no_cancellation | absolute envelope or zero proofs for every other component | \|delta gamma\| <= \|tau_X alpha_X\| + \|tau_dis b_dis\| + \|tau_nonH q_nonH\| + ... | MISSING_NO_CANCELLATION_ENVELOPE |
| TRC3100_5_verdict | tau_PPN usable in a c_g bound | requires TRC3100_0 through TRC3100_4 | FAIL_CURRENT_CLAIM |

## c_g Source Row Status
| row_id | quantity | current_value | source_status | claim_status | next_action |
| --- | --- | --- | --- | --- | --- |
| CGS3100_0_alpha_proxy_benchmark | alpha_PPN_proxy | 0.005788015401465051 | SOURCE_BACKED_BENCHMARK_FROM_3098 | BENCHMARK_ONLY_NONCLAIM | retain as comparator once tau/Z/range are sourced |
| CGS3100_1_ZX | Z_X | MISSING_SOURCE_BACKED_VALUE | symbolic formulas only | BLOCKS_CG_BOUND | derive from parent Hessian or declare closure requirement |
| CGS3100_2_MX2 | M_X^2 | MISSING_SOURCE_BACKED_VALUE | symbolic formulas only | BLOCKS_RANGE_CLASSIFICATION | derive from parent Hessian/eigenvalue spectrum or demote finite-range branch |
| CGS3100_3_tauPPN | tau_PPN | MISSING_RESPONSE_MATRIX | 1030 provenance gate rejects tau_PPN | BLOCKS_PPN_COMPONENT_BOUND | derive PPN residual vector or zero theorem |
| CGS3100_4_SPPN | S_PPN(lambda_X,environment) | MISSING_TRANSFER_FUNCTION | branch not range-classified | BLOCKS_ARENA_SELECTION | derive lambda_X first, then screening/finite-source transfer |
| CGS3100_5_verdict | c_g local branch | NO_SOURCE_BACKED_COMPONENT_BOUND | contract written, inputs absent | CLOSURE_ONLY_UNTIL_PARENT_ACTION_SIGNED | choose no-shadow zero theorem route or finite-coupling parent action route |

## Decision Ledger
| decision_id | decision | rationale | status |
| --- | --- | --- | --- |
| DEC3100_0_no_numeric_extraction | no parent-owned numeric/source row was extracted for Z_X, M_X^2, tau_PPN, or S_PPN | scanned current AX1090 gates contain symbolic laws and missing-input statuses only | adopted |
| DEC3100_1_keep_cg_nonclaim | do not promote direct c_g, PPN pass, or local-GR/Newton reduction | normalization, range, response, and cross-sector gates remain unsigned | adopted |
| DEC3100_2_next_route_choice | next attack should choose between c_g=0 no-shadow/public-metric theorem and finite-coupling parent action | this is the fork where local GR either emerges cleanly or the theory must own a fifth-force coupling | selected |

## Next Target
| route_id | next_checkpoint | script | objective | selection_status | success_condition |
| --- | --- | --- | --- | --- | --- |
| NEXT3100_0_primary | 3101-Y5-R2FR-single-public-metric-or-finite-coupling-parent-action-choice-under-AX1090.md | scripts/Y5_R2FR_single_public_metric_or_finite_coupling_parent_action_choice_under_AX1090_3101.py | attempt the low-scrutiny zero route first: prove ordinary matter has only one public metric/coframe and no extra A_g(Xhat) slot; if not, require finite-coupling parent action rows | selected | either c_g=0/tau_PPN=0 is parent-signed, or finite c_g is explicitly demoted to source-row closure until Z_X/M_X^2/tau/S are supplied |
| NEXT3100_1_parallel | 3101b-Y5-R2FR-PPN-residual-vector-no-cancellation-envelope-under-AX1090.md | scripts/Y5_R2FR_PPN_residual_vector_no_cancellation_envelope_under_AX1090_3101b.py | build absolute PPN residual vector over c_g, disformal, non-Hilbert, support, boundary, and readout terms | held | Cassini/PPN can be applied as a vector envelope without cancellation assumptions |

## Branch Copies
| copy_id | source | target | target_exists | purpose |
| --- | --- | --- | --- | --- |
| COPY3100_0 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_PARENT_INPUT_EXTRACTION_SCAN.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\parent-action\parent_Hessian_tauPPN_extraction_scan_3100_NO_SOURCE_VALUES.csv | True | nonclaim parent-action handoff copy |
| COPY3100_1 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_PARENT_ACTION_CONTRACT_REQUIRED.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\parent-action\parent_action_contract_required_for_cg_3100_NOT_SIGNED.csv | True | nonclaim parent-action handoff copy |
| COPY3100_2 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_TAUPPN_RESPONSE_CONTRACT.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\parent-action\tauPPN_response_contract_3100_NOT_SIGNED.csv | True | nonclaim parent-action handoff copy |
| COPY3100_3 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_CG_SOURCE_ROW_STATUS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\cg_source_row_status_3100_NONCLAIM.csv | True | nonclaim parent-action handoff copy |
| COPY3100_4 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_NEXT_TARGET.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR3100_single_public_metric_or_finite_coupling_choice_NEXT_NONCLAIM.csv | True | nonclaim parent-action handoff copy |

## Validation
| validation_id | check_pass | detail | artifact |
| --- | --- | --- | --- |
| VAL3100_00_sources_csv | True | source register exists | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_SOURCE_REGISTER.csv |
| VAL3100_01_sources_exist | True | every cited source path exists | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_SOURCE_REGISTER.csv |
| VAL3100_02_sources_parse | True | every cited csv source parses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_SOURCE_REGISTER.csv |
| VAL3100_03_sources_needles | True | all source needles found | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_SOURCE_REGISTER.csv |
| VAL3100_04_doc_exists | True | checkpoint doc exists | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3100-Y5-R2FR-parent-Hessian-and-tauPPN-extraction-for-cg-under-AX1090.md |
| VAL3100_05_scan_parses | True | extraction scan parses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_PARENT_INPUT_EXTRACTION_SCAN.csv |
| VAL3100_06_no_accepted_numeric_inputs | True | no accepted source-backed numeric parent inputs found | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_PARENT_INPUT_EXTRACTION_SCAN.csv |
| VAL3100_07_symbolic_hits_present | True | symbolic structure was actually searched and found | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_PARENT_INPUT_EXTRACTION_SCAN.csv |
| VAL3100_08_tau_missing | True | tau_PPN remains missing | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_PARENT_INPUT_EXTRACTION_SCAN.csv |
| VAL3100_09_contract_parses | True | parent action contract parses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_PARENT_ACTION_CONTRACT_REQUIRED.csv |
| VAL3100_10_contract_verdict | True | parent action contract verdict blocks claim | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_PARENT_ACTION_CONTRACT_REQUIRED.csv |
| VAL3100_11_tau_contract_parses | True | tau_PPN contract parses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_TAUPPN_RESPONSE_CONTRACT.csv |
| VAL3100_12_tau_contract_verdict | True | tau contract verdict blocks claim | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_TAUPPN_RESPONSE_CONTRACT.csv |
| VAL3100_13_cg_status_parses | True | c_g source status parses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_CG_SOURCE_ROW_STATUS.csv |
| VAL3100_14_cg_status_nonclaim | True | c_g verdict remains closure-only | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_CG_SOURCE_ROW_STATUS.csv |
| VAL3100_15_all_cg_rows_nonclaim | True | all c_g status rows are nonclaim | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_CG_SOURCE_ROW_STATUS.csv |
| VAL3100_16_decision_selected | True | next route decision selected | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_DECISION_LEDGER.csv |
| VAL3100_17_next_primary | True | primary next target selected | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_NEXT_TARGET.csv |
| VAL3100_18_branch_copies_exist | True | all branch copies exist | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_BRANCH_COPIES.csv |
| VAL3100_19_branch_copies_parse | True | all branch copies parse | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3100_BRANCH_COPIES.csv |
| VAL3100_20_formalization_untouched | True | no formalization-workbench 3100 artifacts modified by this run | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench |
| VAL3100_21_pycache_removed | True | scripts __pycache__ absent after run | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\__pycache__ |
