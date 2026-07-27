# 1852: PPN Common-Frame c_g Translation Gate

**Current verdict:** Cassini gives a real source-backed PPN anchor and a clean scalar-tensor proxy `|alpha_PPN| <= 0.00578802` from the conservative `|gamma-1| <= 6.7e-05` envelope. But this is not yet a direct MTS `c_g` bound: the parent branch still lacks `N_X`, `tau_PPN`, solar-system range/screening, and proof that disformal/non-Hilbert/support terms are silent.

## Source Register
| source_id | source_type | source_path | source_url | needle | use | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1852_0_1851_handoff | local_checkpoint | 1851-Y5-R2FR-first-real-local-coupling-bound-source-table.md |  | NEXT1851_0_primary | selected PPN/common-frame c_g translation target | FOUND | False |
| SRC1852_1_1851_observable_table | local_csv | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1851_OBSERVABLE_BOUND_SOURCE_TABLE.csv |  | OBS1851_2_PPN_CASSINI_2003 | Cassini PPN observable bound row | FOUND | False |
| SRC1852_2_1851_translation_gate | local_csv | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1851_MTS_TRANSLATION_GATES.csv |  | TRG1851_0_cg_to_PPN | missing c_g to PPN translation handoff | FOUND | False |
| SRC1852_3_cassini_2003 | primary_paper |  | https://pubmed.ncbi.nlm.nih.gov/14508481/ | gamma = 1 + (2.1 +/- 2.3) x 10^-5 | PPN gamma-minus-one source for conservative bound | WEB_SOURCE_RECORDED | False |

## PPN Observable Bound
| row_id | observable | central_value | one_sigma | conservative_bound_value | bound_rule | units | source_url | source_backed_observable | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PPN1852_0_cassini_gamma | gamma_minus_1 | 2.1e-05 | 2.3e-05 | 6.7e-05 | |central| + 2*sigma | dimensionless | https://pubmed.ncbi.nlm.nih.gov/14508481/ | True | False |
| PPN1852_1_scalar_tensor_alpha0_proxy | alpha0_abs_proxy |  |  | 0.005788015401465051 | from |gamma-1|=2 alpha0^2/(1+alpha0^2), alpha0^2 <= delta_gamma/(2-delta_gamma) | dimensionless | https://pubmed.ncbi.nlm.nih.gov/14508481/ | True | False |

## Common-Frame Derivation
| step_id | statement | equation | status | missing_for_MTS | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DER1852_0_common_frame_ansatz | Assume ordinary matter sees a universal conformal frame g_matter=A_g(Xhat)^2 g_E. | A_g(Xhat)=exp(c_g Xhat + O(Xhat^2)) | CONDITIONAL_ANSATZ | parent action has not signed universal common frame as the only local matter coupling | False |
| DER1852_1_canonical_scalar | Introduce canonical scalar varphi with alpha_PPN=d ln A_g/d(varphi/M_Pl). | alpha_PPN = N_X c_g, where N_X=dXhat/d(varphi/M_Pl) | NORMALIZATION_GATE | N_X from Z_X and parent Hessian/range is not owned | False |
| DER1852_2_ppn_gamma_law | For an unscreened massless single scalar-tensor limit, gamma-1=-2 alpha_PPN^2/(1+alpha_PPN^2). | |alpha_PPN| <= sqrt(delta_gamma/(2-delta_gamma)) | STANDARD_CONDITIONAL_RELATION | MTS has not proven it reduces to this scalar-tensor PPN limit | False |
| DER1852_3_cassini_proxy_bound | Using the conservative Cassini envelope gives a scalar-tensor proxy bound. | delta_gamma=6.7e-05; |alpha_PPN|<=0.0057880154 | NUMERIC_PROXY_DERIVED | proxy is not a direct c_g bound until N_X, range and contamination gates pass | False |
| DER1852_4_cg_translation | If N_X and tau_PPN are signed, c_g inherits the proxy through |N_X tau_PPN c_g| <= alpha0_abs_bound. | |c_g| <= 0.0057880154/|N_X tau_PPN| | CONDITIONAL_BOUND_FORMULA_READY | N_X and tau_PPN are MISSING, so c_g remains unbounded as an MTS component | False |

## Scalar-Tensor Assumption Gate
| assumption_id | assumption | needed_for | current_status | failure_if_missing | gate_pass | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| AST1852_0_universal_conformal | all ordinary matter sees one universal conformal frame A_g(Xhat)^2 g_E | map c_g to PPN gamma | NOT_PARENT_SIGNED | species/frame/readout terms move PPN and WEP independently | False | False |
| AST1852_1_canonical_normalization | Xhat normalization is tied to the canonical scalar varphi/M_Pl | turn alpha_PPN proxy into c_g bound | MISSING_NX_FROM_ZX_HESSIAN | c_g can be rescaled by field normalization | False | False |
| AST1852_2_solar_system_range | the X mode is effectively long-range across the Cassini solar-system impact scale | use Cassini gamma without Yukawa/range suppression | MISSING_MX2_OR_LAMBDA_SOLAR_SYSTEM_GATE | finite range or screening suppresses Cassini and sends c_g to R10/orbital gates | False | False |
| AST1852_3_no_screening | no local screening, environmental plateau or nonlinear suppression changes the scalar charge | apply weak-field scalar-tensor gamma law | NOT_DERIVED | Cassini bound constrains screened effective coupling, not parent c_g | False | False |
| AST1852_4_no_disformal_nonhilbert_contamination | b_dis, q_nonH, support and boundary terms do not contribute at the same PPN order | isolate c_g as the gamma source | MISSING_CONTAMINATION_ZERO_OR_BOUND | PPN residual vector is multi-component, not a one-parameter c_g bound | False | False |
| AST1852_5_verdict | all scalar-tensor translation assumptions pass simultaneously | promote alpha0 proxy to c_g component bound | FAIL_CURRENT_CLAIM | keep PPN result as source-backed conditional proxy only | False | False |

## c_g Conditional Bound Row
| bound_id | quantity | formula | numeric_bound | units | source | status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CGB1852_0_alpha_proxy | alpha_PPN_proxy | sqrt(delta_gamma/(2-delta_gamma)) | 0.005788015401465051 | dimensionless | Cassini gamma_minus_1 conservative 2sigma envelope | SOURCE_BACKED_PROXY | False | False |
| CGB1852_1_cg_conditional | c_g | abs(c_g) <= alpha_PPN_proxy / abs(N_X tau_PPN) | MISSING_NX_TAU_PPN | dimensionless_per_normalized_Xhat | DER1852_4_cg_translation | CONDITIONAL_FORMULA_READY_COMPONENT_BOUND_MISSING | False | False |
| CGB1852_2_long_range_branch | c_g_long_range | if lambda_X >> solar impact scale and N_X=tau_PPN=1, abs(c_g)<=alpha_PPN_proxy | 0.005788015401465051 | dimensionless | conditional scalar-tensor limit only | ILLUSTRATIVE_NOT_MTS_CLAIM | False | False |
| CGB1852_3_finite_range_branch | c_g_finite_range | Cassini response multiplied by range/screening transfer S_PPN(lambda_X, environment) | MISSING_RANGE_TRANSFER | dimensionless | range gate required | BLOCKED_BY_RANGE_SCREENING | False | False |

## PPN Failure Mode Audit
| failure_id | failure_mode | why_it_matters | required_fix | blocks_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PFM1852_0_rescaling | field normalization rescaling | c_g is derivative with respect to Xhat; PPN sees canonical alpha_PPN | derive N_X from Z_X/Hessian parent action | True | False |
| PFM1852_1_range | finite range or heavy local mode | Cassini constrains long-range solar-system fields; short-range modes need R10/lab bounds | derive M_X^2/lambda_X and solar-system transfer function | True | False |
| PFM1852_2_screening | environmental screening or plateau suppression | Cassini would bound screened effective coupling, not parent coupling | derive local screening map without smuggling plateau axiom | True | False |
| PFM1852_3_multi_component_ppn | b_dis/q_nonH/support/boundary terms contribute to gamma | a single c_g bound would be fake if other residuals share the PPN channel | derive PPN residual vector and absolute no-cancellation envelope | True | False |
| PFM1852_4_matter_frame_nonuniversality | source/test matter frames are not universal | PPN and WEP constraints split into species-dependent charges | parent matter functor/no-marker theorem or material sensitivity map | True | False |

## Local Branch Status
| branch_id | branch | result | status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| LBS1852_0_if_all_gates_pass | long-range scalar-tensor common-frame MTS | |N_X tau_PPN c_g| <= 0.0057880154 | CONDITIONAL_COMPETITIVE_GATE | False | False |
| LBS1852_1_current_MTS | current parent/local branch | Cassini source bound exists, but c_g is not directly bounded | FAIL_CURRENT_CLAIM_TRANSLATION_MISSING | False | False |
| LBS1852_2_best_next | normalization/range repair | derive N_X and lambda_X transfer before claiming PPN/local GR | NEXT_TARGET | False | False |

## Claim Gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1852_0_cassini_source | Cassini PPN source bound is recorded | True | gamma_minus_one conservative bound and alpha0 proxy are computed | True | False |
| CG1852_1_alpha_proxy | scalar-tensor alpha0 proxy is computed | True | standard conditional formula yields numeric proxy | True | False |
| CG1852_2_cg_component_bound | MTS c_g is bounded by Cassini | False | N_X, tau_PPN, range/screening and contamination gates fail current claim | False | False |
| CG1852_3_local_GR | local GR branch passes PPN | False | PPN residual vector and component bounds are not derived | False | False |

## Decisions
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC1852_0_derivation_status | The Cassini-to-alpha0 derivation is exact for the scalar-tensor proxy. | gamma law can be inverted cleanly and gives a numeric common-frame proxy. | keep it as a benchmark bound, not a direct MTS claim | False |
| DEC1852_1_current_block | The direct c_g claim remains blocked. | field normalization, range/screening and residual-vector isolation are unsigned. | derive N_X/lambda_X transfer from the parent Hessian and local range branch | False |
| DEC1852_2_best_next | Next target should be canonical X normalization and range gate. | without N_X and lambda_X, every c_g bound can be rescaled or range-suppressed. | 1853-Y5-R2FR-canonical-X-normalization-and-range-gate-for-cg.md | False |

## Next Target
| route_id | next_target | script | objective | selection_status | success_condition |
| --- | --- | --- | --- | --- | --- |
| NEXT1852_0_primary | 1853-Y5-R2FR-canonical-X-normalization-and-range-gate-for-cg.md | scripts/Y5_R2FR_canonical_X_normalization_and_range_gate_for_cg_1853.py | derive N_X from Z_X/Hessian ownership and decide whether lambda_X is solar-system long-range, R10 short-range, screened, or still missing | selected | PPN c_g bound becomes normalized/range-qualified, or c_g remains source-only with explicit N_X/lambda_X blockers |
| NEXT1852_1_parallel | 1853b-Y5-R2FR-PPN-residual-vector-no-cancellation-envelope.md | scripts/Y5_R2FR_PPN_residual_vector_no_cancellation_envelope_1853b.py | derive the PPN residual vector over c_g, b_dis, q_nonH, support and boundary components | held | PPN no-cancellation vector is explicit enough for multi-component bounds |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1852_0_sources_recorded | PASS | all local paths exist and web source URLs are recorded |
| VAL1852_1_local_needles_present | PASS | all local source needles are present |
| VAL1852_2_gamma_bound_numeric | PASS | Cassini gamma bound is numeric |
| VAL1852_3_alpha_proxy_numeric | PASS | scalar-tensor alpha0 proxy is numeric and small |
| VAL1852_4_derivation_conditional | PASS | c_g conditional bound formula is present |
| VAL1852_5_assumption_gate_blocks | PASS | scalar-tensor assumptions block current MTS c_g claim |
| VAL1852_6_cg_bound_nonclaim | PASS | c_g component bound remains nonclaim |
| VAL1852_7_failure_modes_block | PASS | all listed PPN failure modes block direct claim |
| VAL1852_8_local_branch_status | PASS | current local branch remains blocked |
| VAL1852_9_claim_gates_safe | PASS | source/proxy gates pass but MTS component/local claims do not |
| VAL1852_10_next_target_selected | PASS | next target selected |
| VAL1852_11_no_claim_flags | PASS | no valid_for_claim flags are true |
| VAL1852_12_missing_rows_nonclaim | PASS | MISSING_* rows stay nonclaim |
| VAL1852_13_csv_parse | PASS | all generated 1852 CSVs parse |
| VAL1852_14_branch_copies | PASS | branch/quarantine/queue copies exist |
| VAL1852_15_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1852_16_formalization_untouched | PASS | no 1852 outputs found under formalization-workbench |
| VAL1852_OVERALL | PASS | 1852 PPN common-frame c_g translation gate |

## Working Interpretation
This is a useful tightening. If MTS really has a long-range, unscreened, universal common scalar frame, Cassini is a harsh judge. If it is finite-range, screened, or not canonically normalized the same way, Cassini is still useful but it cannot be used honestly until the transfer map is derived.
