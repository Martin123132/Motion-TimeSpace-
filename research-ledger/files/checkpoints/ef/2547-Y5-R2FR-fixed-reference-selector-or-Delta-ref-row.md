# 2547 - fixed reference selector or Delta-ref row

## Result

2547 pins the fixed-reference route to an exact parent-action contract.

The useful theorem is narrow and clean: if the parent action owns a fixed boundary datum
`beta_ref=(S,sigma_AB,tau,C_top,B_ct)=beta_0` and local q/source/readout variations stay inside
`C_D(beta_0)`, then the 2455 leak law gives `D_a B_ref=0` for `a in {q,source}` without using a plateau axiom,
post-fit counterterm, observed-GM surface, or sign cancellation.

The current corpus still does not source the required parent signatures or a positive same-frame `M_H_ref/N_E`, so
`Delta_ref=0`, local GR, Newton, PPN, R10, clock, orbital, and GitHub/public claims remain blocked.

## Source Register

| row_id | source_path | exists | needles_found | source_role |
| --- | --- | --- | --- | --- |
| SRC2547_00_2546_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2546-Y5-R2FR-boundary-term-classification-exact-vs-corner-reference.md | true | true | immediate handoff selecting fixed-reference selector |
| SRC2547_01_2546_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2546_VALIDATION.csv | true | true | 2546 validation anchor |
| SRC2547_02_2457_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2457-Y5-R2FR-parent-Dirichlet-boundary-action-contract-or-Delta-ref-bound-values.md | true | true | strongest existing Dirichlet/fixed-boundary reference contract |
| SRC2547_03_2457_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2457_PARENT_ACTION_CONTRACT.csv | true | true | machine-readable parent action contract |
| SRC2547_04_2457_variational | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2457_VARIATIONAL_DOMAIN_THEOREM.csv | true | true | fixed beta_0 implies B_ref q/source silence as conditional theorem |
| SRC2547_05_2457_signature | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2457_CONTRACT_SIGNATURE_AUDIT.csv | true | true | current missing signature audit |
| SRC2547_06_2457_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2457_DELTA_REF_BOUND_VALUE_INPUTS.csv | true | true | nonclaim Delta_ref bound-value input precedent |
| SRC2547_07_2456_dirichlet | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2456_DIRICHLET_REFERENCE_BRANCH.csv | true | true | Dirichlet reference branch precursor |
| SRC2547_08_2455_leak_law | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2455_BOUNDARY_REFERENCE_EMBEDDING_DERIVATION.csv | true | true | exact B_ref leak law and finite bound fallback |
| SRC2547_09_2453_ift | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2453_IMPLICIT_FUNCTION_DERIVATION.csv | true | true | implicit-function selector proof route |
| SRC2547_10_1771_boundary | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1771-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md | true | true | older warning that reference terms can fake closure |

## Fixed Reference Selector Theorem

| row_id | step | statement | formula | result | current_status |
| --- | --- | --- | --- | --- | --- |
| FRS2547_0_selector_object | fixed reference data object | Define beta_ref=(S,sigma_AB,tau,C_top,B_ct) as the reference-boundary datum controlled before local q/source/readout variations. | beta_ref(Phi)|dM = beta_0 | the reference problem becomes a boundary-data ownership problem | DEFINITION_CONTRACT_NOT_PARENT_SIGNED |
| FRS2547_1_configuration_domain | Dirichlet configuration bundle | If the parent theory declares C_D(beta_0)={Phi: beta_ref(Phi)|dM=beta_0}, allowed q/source variations are tangent to C_D(beta_0). | delta_a Phi in T C_D(beta_0) => D_a beta_ref=0 for a in {q,source} | D_a S=D_a sigma_AB=D_a tau=D_a C_top=D_a B_ct=0 | CONDITIONAL_THEOREM_AS_CONTRACT |
| FRS2547_2_chain_rule_to_Bref | reference silence | Insert the component zeros into the 2455 leak law. | D_a B_ref=<dB/dsigma,D_a sigma>+<dB/dtau,D_a tau>+<dB/dC_top,D_a C_top>+D_a B_ct=0 | partial_q B_ref=partial_source B_ref=0 without cancellation | PASS_AS_CONDITIONAL_CONTRACT |
| FRS2547_3_to_Href_Deltaref | reference Hamiltonian component | If H_ref is fixed by the same beta_0 and the denominator is same-frame parent-owned, the reference part of Delta_ref is q/source silent. | D_a Delta_ref=0 if H_ref=H_ref[beta_0], tau_H=tau_source=tau_readout, and M_H_ref>0 is parent-owned | reference residual can vanish only under parent signature plus same-frame denominator | BLOCKED_ON_SIGNATURE_AND_MHREF |
| FRS2547_4_no_shortcuts | anti-laundering rule | Observed GM, fitted mass, readout radius, residual sign, and post-hoc counterterm choices cannot enter beta_0, B_ref, H_ref, or M_H_ref. | partial_{GM_obs,M_fit,residual,readout} beta_0 = 0 and partial_{same} B_ct = 0 | prevents proving Newton/GR by importing Newton/GR | GUARDRAIL_DERIVED_NONCLAIM |
| FRS2547_5_verdict | current verdict | The exact fixed-reference selector contract is written, but the active corpus has not signed its required parent action clauses. | PAC/SIG signatures missing => Delta_ref=0 not claim-grade | retain Delta_ref bound rows and hunt parent signatures | THEOREM_NOT_PROMOTED_RETAIN_DELTA_REF |

## Dirichlet Action Contract

| row_id | clause | formula | derivation_role | current_signature | status |
| --- | --- | --- | --- | --- | --- |
| DAC2547_0_parent_bundle | Parent configuration bundle declares fixed beta_0. | C_D(beta_0)={Phi: beta_ref(Phi)|dM=beta_0} | owns the reference branch before source/readout | MISSING_PARENT_CONFIGURATION_BUNDLE | BLOCKED_NONCLAIM |
| DAC2547_1_action_variation | Parent action is varied at fixed beta_0. | S_D[Phi;beta_0]=int_M L_MTS+int_dM B_D(Phi;beta_0)+S_matter[q(Phi),Psi;beta_0] | makes reference data a variational boundary condition, not an empirical fit | MISSING_PARENT_ACTION_WITH_FIXED_BETA0 | BLOCKED_NONCLAIM |
| DAC2547_2_variation_domain | Allowed local q/source/readout variations lie in ker(D beta_ref). | D_a beta_ref=0 for a in {q,source} | turns the selector criterion into a theorem when parent-signed | MISSING_VARIATIONAL_DOMAIN_CERTIFICATE | CONDITIONAL_ONLY |
| DAC2547_3_reference_functional | B_ref and H_ref depend only on beta_ref and fixed counterterm/topological class. | B_ref=B_ref[beta_0,B_ct(C_top0)]; H_ref=H_ref[beta_0] | blocks source/GM/counterterm leakage | MISSING_REFERENCE_FUNCTIONAL_OWNERSHIP | BLOCKED_NONCLAIM |
| DAC2547_4_tau_coframe_lock | Same tau/coframe defines source, charge, clocks, boundary and readout. | tau_source=tau_charge=tau_clock=tau_boundary=tau_readout=tau_0 | needed for same-frame M_H_ref and later PPN bridge | MISSING_TAU_COFRAME_LOCK | BLOCKED_NONCLAIM |
| DAC2547_5_no_shortcut_guard | No observed-GM surface, orbital-GM denominator, or cancellation counterterm can fill a missing clause. | claim_allowed=false if beta_0, B_ct or M_H_ref are inferred from target readout | keeps the route derivational rather than post-hoc | GUARDRAIL_INSTALLED | GUARDRAIL_PASS_NONCLAIM |

## Signature Audit

| row_id | required_signature | current_fill | why_required | blocks | status |
| --- | --- | --- | --- | --- | --- |
| SIG2547_0_configuration_bundle | C_D(beta_0) declared by parent theory | MISSING_PARENT_CONFIGURATION_BUNDLE | without this, fixed beta_0 is an imposed closure | DAC2547_0_parent_bundle | BLOCKED_NONCLAIM |
| SIG2547_1_boundary_surface | S/domain fixed before source/readout | MISSING_SOURCE_BLIND_SURFACE_DOMAIN_RULE | prevents observed-GM boundary laundering | DAC2547_2_variation_domain | BLOCKED_NONCLAIM |
| SIG2547_2_boundary_metric | sigma_AB fixed or source-blind by parent boundary condition | MISSING_BOUNDARY_METRIC_ZERO_CERTIFICATE | main B_ref embedding input | FRS2547_2_chain_rule_to_Bref | BLOCKED_NONCLAIM |
| SIG2547_3_tau_coframe | tau/coframe fixed and shared by charge/clocks/readout | MISSING_TAU_COFRAME_LOCK | same-frame reference and PPN bridge | DAC2547_4_tau_coframe_lock | BLOCKED_NONCLAIM |
| SIG2547_4_topology | C_top superselected before local variation | MISSING_CTOP_SUPERSELECTION_CERTIFICATE | prevents source-selected class switching | DAC2547_3_reference_functional | BLOCKED_NONCLAIM |
| SIG2547_5_counterterm | B_ct fixed by boundary variational principle | MISSING_COUNTERTERM_ZERO_CERTIFICATE | prevents cancellation-based proof | DAC2547_3_reference_functional | BLOCKED_NONCLAIM |
| SIG2547_6_embedding | embedding Hessian/operator norm controlled | MISSING_EMBEDDING_HESSIAN_OR_OPERATOR_NORM | prevents hidden non-rigid reference drift | FRS2547_2_chain_rule_to_Bref | BLOCKED_NONCLAIM |
| SIG2547_7_denominator | positive same-frame M_H_ref or N_E exists | MISSING_SAME_FRAME_N_E_OR_MHREF | normalizes residual without circular orbital-GM import | FRS2547_3_to_Href_Deltaref | BLOCKED_NONCLAIM |
| SIG2547_8_source_paths | all signatures have source paths/equation refs | MISSING_SOURCE_PATHS_FOR_PROMOTION | required before any valid_for_claim switch | all rows | BLOCKED_NONCLAIM |

## Delta-ref Bound Rows

| row_id | quantity | bound_formula | required_inputs | current_value | status | score_ready |
| --- | --- | --- | --- | --- | --- | --- |
| DRB2547_0_zero_contract_switch | Delta_ref_q_source_component_over_MH | 0 only if all DAC2547 and SIG2547 clauses are parent-signed | parent action with fixed beta_0; tau/coframe lock; C_top/B_ct rules; embedding control; positive same-frame M_H_ref | NOT_ALLOWED_AS_VALUE | ZERO_SWITCH_BLOCKED_NONCLAIM | false |
| DRB2547_1_metric_leak | C_sigma*max(||D_q sigma||,||D_source sigma||)/M_H_ref | metric boundary-data leak normalized by same-frame denominator | regular_embedding_class; C_sigma; norm_Dq_sigma; norm_Dsource_sigma; M_H_ref; source_path | MISSING_VALUE | MISSING_BOUND_VALUE | false |
| DRB2547_2_tau_leak | C_tau*max(||D_q tau||,||D_source tau||)/M_H_ref | tau/coframe leak normalized by same-frame denominator | tau_frame_id; C_tau; norm_Dq_tau; norm_Dsource_tau; M_H_ref; source_path | MISSING_VALUE | MISSING_BOUND_VALUE | false |
| DRB2547_3_topology_counterterm_leak | max(C_top|D_a C_top|+|D_a B_ct|)/M_H_ref | topological class and counterterm leak with no cancellation | C_top rule; B_ct rule; derivatives; M_H_ref; source_path | MISSING_VALUE | MISSING_BOUND_VALUE | false |
| DRB2547_4_total_absolute | Delta_ref_over_MH | absolute sum of metric, tau, topology/counterterm and branch-drift components over M_H_ref | DRB2547_1 through DRB2547_3; selector branch drift; positive same-frame M_H_ref; no-cancellation guard | NOT_COMPUTED_COMPONENTS_MISSING | PRIMARY_NONCLAIM_BOUND_ROW | false |

## Decision Ledger

| row_id | decision | reason | consequence | status |
| --- | --- | --- | --- | --- |
| DEC2547_0_contract_result | retain fixed-reference zero route as an exact parent-action contract | the 2455 leak law plus fixed beta_0 variational domain gives D_a B_ref=0 without plateau axiom or cancellation | the local branch has a real derivational target, not just a closure wish | CONTRACT_ACCEPTED_NONCLAIM |
| DEC2547_1_no_promotion | do not promote Delta_ref=0 for current MTS | configuration bundle, boundary action, tau/coframe, topology, counterterm, embedding and denominator signatures are still missing | Delta_ref remains live and non-score-ready | THEOREM_NOT_PARENT_SIGNED |
| DEC2547_2_next | search for existing parent-action signatures before inventing new closure | the required contract is explicit enough to audit the corpus for matches | 2548 should run a signature hunt or demote the reference-zero route to closure-only | SELECT_2548_SIGNATURE_HUNT |
| DEC2547_3_no_github | keep private | this is proof scaffolding, not a local-GR result | no GitHub/public claim | PRIVATE_NONCLAIM |

## Claim Gates

| row_id | gate | gate_status | claim_effect |
| --- | --- | --- | --- |
| CG2547_0_fixed_reference_contract | exact sufficient contract for B_ref q/source silence | PASS_AS_CONTRACT_ONLY | mathematical route accepted but not claim-grade |
| CG2547_1_parent_signature | current corpus proves parent action satisfies fixed beta_0 contract | FAIL | all required signatures remain missing |
| CG2547_2_Delta_ref_zero | Delta_ref q/source leak equals zero for current MTS | FAIL_NONCLAIM | zero switch blocked until parent signatures and M_H_ref are present |
| CG2547_3_finite_bound | finite source-backed Delta_ref bound ready | FAIL | bound rows are schema-only with missing values |
| CG2547_4_MHref | positive same-frame M_H_ref/N_E | FAIL | normalization remains blocked |
| CG2547_5_local_GR_Newton | local GR/Newton/PPN recovery | FAIL_NONCLAIM | reference, denominator and source-measure gates remain open |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows |
| --- | --- | --- | --- | --- |
| REF2547_0_assume_beta_fixed | assume beta_ref is fixed without parent configuration bundle | false | that would be a closure axiom, not a derived fixed-reference theorem | SIG2547_0_configuration_bundle;DAC2547_0_parent_bundle |
| REF2547_1_GM_boundary | choose boundary surface or reference by observed GM/fitted mass | false | this imports Newton/source normalization before deriving it | DAC2547_5_no_shortcut_guard;SIG2547_1_boundary_surface |
| REF2547_2_counterterm_cancel | choose B_ct after seeing the residual | false | post-readout counterterms are cancellation knobs | SIG2547_5_counterterm;DRB2547_3_topology_counterterm_leak |
| REF2547_3_score_bound_now | score Delta_ref_over_MH now | false | component values and same-frame denominator are missing | DRB2547_1_metric_leak;DRB2547_4_total_absolute;SIG2547_7_denominator |
| REF2547_4_public_claim | publish this as local GR/Newton evidence | false | fixed-reference contract is progress but not a closed branch | CG2547_1_parent_signature;CG2547_5_local_GR_Newton |

## Next Target

| row_id | priority | next_file | success_condition | fallback_condition |
| --- | --- | --- | --- | --- |
| NEXT2547_0_selected | selected | 2548-Y5-R2FR-parent-action-signature-hunt-or-reference-route-demotion.md | find source-backed parent-action signatures for fixed beta_0, tau/coframe lock, C_top superselection, B_ct rule, embedding control and same-frame M_H_ref | demote fixed-reference zero to explicit closure-only and move to finite Delta_ref bound-value acquisition ledger |
| NEXT2547_1_parallel | parallel | 2548b-Y5-R2FR-same-frame-MHref-sidecar-or-denominator-row.md | derive positive same-frame M_H_ref/N_E compatible with beta_0 and tau/coframe lock | keep all normalized Delta_ref/Brem rows non-score-ready |
| NEXT2547_2_parallel | parallel | 2548c-Y5-R2FR-boundary-data-leak-first-source-values.md | fill at least one finite metric/tau/topology/counterterm leak value with source path, units and no-cancellation guard | retain MISSING_VALUE rows and do not score Delta_ref |

## Validation

| row_id | status | detail |
| --- | --- | --- |
| VAL2547_00_required_sources_exist | PASS | all required source paths exist |
| VAL2547_01_required_needles_found | PASS | all source needles found |
| VAL2547_02_outputs_exist | PASS | all 2547 output files written before validation |
| VAL2547_03_csv_parse | PASS | all generated CSV files parse and contain rows |
| VAL2547_04_selector_contract_present | PASS | fixed-reference contract and chain-rule theorem present |
| VAL2547_05_signature_blockers_present | PASS | signature blockers explicit |
| VAL2547_06_bounds_nonready | PASS | Delta_ref bound rows remain non-score-ready |
| VAL2547_07_no_shortcut_refusals | PASS | GM boundary and counterterm cancellation refused |
| VAL2547_08_global_claims_blocked | PASS | global/local claims remain blocked |
| VAL2547_09_next_selected | PASS | signature hunt/demotion selected next |
| VAL2547_10_branch_copies | PASS | all nonclaim branch copies exist |
| VAL2547_11_no_positive_claim_flags | PASS | all generated claim/readiness flags remain negative |
| VAL2547_12_formalization_untouched | PASS | generator writes only under post-checkpoint-work |
| VAL2547_13_pycache_absent | PASS | scripts __pycache__ absent |
| VAL2547_OVERALL | PASS | 2547 writes the exact fixed-reference selector contract, blocks promotion without parent signatures/MHref, stages Delta_ref bounds, and selects signature hunt/demotion next |

## Generated Files

- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2547_SOURCE_REGISTER.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2547_FIXED_REFERENCE_SELECTOR_THEOREM.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2547_DIRICHLET_ACTION_CONTRACT.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2547_SIGNATURE_AUDIT.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2547_DELTA_REF_BOUND_ROWS.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2547_DECISION_LEDGER.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2547_CLAIM_GATES.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2547_REFUSAL_RUNNER.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2547_NEXT_TARGET.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2547_BRANCH_COPIES.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_2547_VALIDATION.csv`

## Practical Status

This is a strong-but-private step.  The reference problem is no longer "please be quiet, B_ref"; it is now a signed
parent-boundary-condition problem.  If we can find this fixed-beta signature in the corpus, the reference leak has a
real derivation route.  If we cannot, the honest move is to demote the zero route to closure-only and fill finite
`Delta_ref` bounds.  That is the next hunt.
