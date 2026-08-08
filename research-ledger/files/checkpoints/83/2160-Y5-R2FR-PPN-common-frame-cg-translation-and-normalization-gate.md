# 2160 - Y5/R2FR PPN Common-Frame c_g Translation And Normalization Gate

## Current Verdict

2160 does **not** give a direct MTS `c_g` bound, PPN pass, local GR/Newton reduction, or public claim.

It does derive the active-branch comparison object: `alpha_eff_PPN = tau_PPN S_PPN(lambda_X,env) c_g/sqrt(Z_X) + alpha_vec_tail`, with Cassini giving the source-backed proxy `|alpha_eff_PPN| <= 0.00578801540146505` only under the scalar-tensor PPN assumptions.

Raw `c_g` is not observable by itself. The direct bound needs parent-owned `Z_X`, `tau_PPN`, `lambda_X`, `S_PPN`, and zero/bounded disformal, non-Hilbert, support, boundary and readout vector tails.

This follows the 2159 handoff at line 126, imports the 1853 normalization guard at line 24, and uses the 2158 residual-vector guard at line 66.

## Source Register

| source_id | source_path | path_exists | needles_found | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC2160_00_2159_handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2159-Y5-R2FR-parent-ordinary-matter-signature-or-first-coupling-bound-row.md | true | true | current 2159 selects active-branch PPN c_g translation and normalization gate. | false |
| SRC2160_01_2159_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2159_NEXT_TARGET.csv | true | true | machine-readable 2160 target. | false |
| SRC2160_02_2159_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2159_VALIDATION.csv | true | true | 2159 validation passed as nonclaim. | false |
| SRC2160_03_1852_ppn_proxy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1852-Y5-R2FR-PPN-common-frame-cg-translation-gate.md | true | true | 1852 gives Cassini scalar-tensor alpha proxy and c_g conditional formula. | false |
| SRC2160_04_1852_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1852_VALIDATION.csv | true | true | 1852 validation passed as nonclaim. | false |
| SRC2160_05_1853_normalization | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1853-Y5-R2FR-canonical-X-normalization-and-range-gate-for-cg.md | true | true | 1853 supplies normalization/range guard for c_g. | false |
| SRC2160_06_1853_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1853_VALIDATION.csv | true | true | 1853 validation passed as nonclaim. | false |
| SRC2160_07_2156_hessian | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2156-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md | true | true | 2156 keeps parent Xhat/Hessian ownership unsigned. | false |
| SRC2160_08_2157_metric | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2157-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md | true | true | 2157 freezes finite route and rejects beta mode-count shortcut. | false |
| SRC2160_09_2158_vector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2158-Y5-R2FR-JX-qbarXT-source-zero-or-bounded-coupling-component-pack.md | true | true | 2158 supplies PPN-relevant source-current component envelope. | false |


## Scalar-Tensor PPN Map

| step_id | target | equation | status | missing_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| STM2160_0_common_frame_ansatz | universal common-frame coupling | g_matter=A_g(Xhat)^2 g_E and A_g=exp(c_g Xhat+O(Xhat^2)) | CONDITIONAL_ANSATZ_ONLY | parent matter signature/no-shadow theorem must select this as the only matter frame | false |
| STM2160_1_canonical_field | canonical scalar normalization | varphi=M_Pl sqrt(Z_X) Xhat, so N_X=dXhat/d(varphi/M_Pl)=1/sqrt(Z_X) | EXACT_IF_PARENT_QUADRATIC_BLOCK_SIGNED | Z_X and Xhat owner remain unsigned | false |
| STM2160_2_effective_ppn_charge | PPN charge seen by Cassini | alpha_eff_PPN = tau_PPN S_PPN(lambda_X,env) N_X c_g + alpha_vec_tail | FORMULA_READY_INPUTS_MISSING | tau_PPN, S_PPN, lambda_X and residual vector missing | false |
| STM2160_3_gamma_law | single massless unscreened scalar-tensor limit | gamma-1=-2 alpha_eff_PPN^2/(1+alpha_eff_PPN^2) | STANDARD_CONDITIONAL_RELATION | MTS has not proven this limit | false |
| STM2160_4_proxy_bound | Cassini scalar proxy | \|alpha_eff_PPN\| <= 0.00578801540146505 | SOURCE_BACKED_PROXY | not direct c_g bound until STM2160_0 through STM2160_3 close | false |
| STM2160_5_verdict | active-branch PPN map | \|tau_PPN S_PPN c_g/sqrt(Z_X) + alpha_vec_tail\| <= 0.00578801540146505 | CONDITIONAL_MAP_DERIVED_NOT_CLAIM_GRADE | normalization/range/vector gates remain open | false |


## N_X Normalization Gate

| gate_id | needed_input | formula_or_role | current_status | if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NX2160_0_Xhat_owner | same Xhat owns c_g and local quadratic block | c_g=d ln A_g/dXhat and S_X^(2) uses same Xhat | NOT_PARENT_SIGNED | prevents comparing c_g to canonical PPN charge | false |
| NX2160_1_ZX_positive | Z_X>0 parent kinetic coefficient | varphi=M_Pl sqrt(Z_X) Xhat | MISSING_ZX | N_X cannot be numeric | false |
| NX2160_2_rescaling_invariant | field rescaling guard | Xhat->aXhat gives c_g->c_g/a and Z_X->Z_X/a^2, so c_g/sqrt(Z_X) is invariant | GUARDRAIL_ACTIVE | raw c_g alone is not observable | false |
| NX2160_3_tau_PPN | PPN projection/readout factor | tau_PPN maps canonical common-frame charge into gamma observable | MISSING_TAU_PPN | PPN response may not equal unit scalar-tensor response | false |
| NX2160_4_verdict | normalization gate | \|tau_PPN c_g/sqrt(Z_X)\| can be bounded only after Z_X and tau_PPN are signed | FAIL_CURRENT_CLAIM_INPUTS_MISSING | direct c_g bound remains blocked | false |


## Range/Screening Transfer Gate

| gate_id | target | formula_or_condition | current_status | if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RSG2160_0_mass_gap | same parent Hessian fixes mass/range | mu_X^2=M_X^2/Z_X | MISSING_MX2_AND_ZX | range class unknown | false |
| RSG2160_1_lambda | range relation | lambda_X=sqrt(Z_X/M_X^2) with units fixed by parent block | EXACT_CONDITIONAL_RELATION_VALUES_MISSING | cannot route PPN vs R10 vs orbital | false |
| RSG2160_2_long_range_transfer | solar-system long-range branch | S_PPN(lambda_X,env)≈1 only if lambda_X is long compared with the Cassini source/readout scale and unscreened | NOT_CLASSIFIED | Cassini proxy cannot be applied unsuppressed | false |
| RSG2160_3_finite_range_transfer | finite/lab range branch | S_PPN may be Yukawa-suppressed; R10/lab or orbital finite-geometry bounds may dominate | NOT_CLASSIFIED | do not use Cassini as universal bound | false |
| RSG2160_4_screening_plateau | environmental screening/plateau branch | S_PPN is an effective screened transfer derived from parent equations, not an inserted plateau | NOT_DERIVED | screening cannot rescue c_g by assertion | false |
| RSG2160_5_verdict | range/screening gate | alpha_eff_PPN=tau_PPN c_g S_PPN(lambda_X,env)/sqrt(Z_X) | FAIL_CURRENT_CLAIM_TRANSFER_MISSING | M_X^2, lambda_X and S_PPN remain missing | false |


## PPN Residual Vector Envelope

| component_id | component | ppn_leg | current_status | observable_link | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PPV2160_0_cg | common conformal frame | tau_g S_PPN c_g/sqrt(Z_X) | MISSING_ZX_TAU_RANGE | Cassini gamma; Shapiro/time-delay | false |
| PPV2160_1_bdis | disformal/preferred-frame matter metric | tau_dis b_dis | MISSING_DISFORMAL_PPN_PROJECTION | PPN gamma; alpha1/alpha2; clocks | false |
| PPV2160_2_qnonH | non-Hilbert/source-tail current | tau_nonH q_nonH | MISSING_NONHILBERT_PPN_PROJECTION | PPN gamma; orbital source normalization | false |
| PPV2160_3_support | support/domain/local projection shift | tau_support Delta_W_support + tau_domain q_domain | MISSING_SUPPORT_DOMAIN_PPN_PROJECTION | preferred-location/source geometry | false |
| PPV2160_4_boundary | boundary/local flux tail | tau_boundary q_boundary | MISSING_BOUNDARY_PPN_PROJECTION | PPN/orbital/local-GR boundary terms | false |
| PPV2160_5_readout | post-variation readout or measured-G calibration tail | tau_readout C_readout | MISSING_READOUT_PPN_PROJECTION | measured GM/gamma extraction | false |
| PPV2160_6_total_abs_guard | absolute PPN residual vector | \|alpha_PPN_total\| <= \|cg leg\|+\|bdis leg\|+\|nonH leg\|+\|support leg\|+\|boundary leg\|+\|readout leg\| | SCHEMA_READY_VALUES_MISSING | no one-parameter c_g pass until vector is controlled | false |


## c_g Bound Status

| bound_id | quantity | formula | numeric_or_status | units | status | direct_mts_component_bound | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CGB2160_0_delta_gamma | gamma_minus_1_bound | Cassini conservative envelope carried from 1851/1852/2159 | 6.7e-05 | dimensionless | SOURCE_BACKED_OBSERVABLE | false | false |
| CGB2160_1_alpha_proxy | alpha_PPN_proxy | sqrt(delta_gamma/(2-delta_gamma)) | 0.005788015401465051 | dimensionless | SOURCE_BACKED_PROXY | false | false |
| CGB2160_2_effective_invariant | alpha_eff_PPN | tau_PPN S_PPN c_g/sqrt(Z_X) + alpha_vec_tail | abs(alpha_eff_PPN)<=0.00578801540146505 | dimensionless | CONDITIONAL_EFFECTIVE_BOUND | false | false |
| CGB2160_3_raw_cg | c_g | abs(c_g)<=alpha_proxy*sqrt(Z_X)/(abs(tau_PPN*S_PPN)) only when alpha_vec_tail=0 | MISSING_ZX_TAU_RANGE_VECTOR | dimensionless_per_Xhat | FORMULA_READY_COMPONENT_BOUND_MISSING | false | false |
| CGB2160_4_verdict | direct MTS c_g bound | direct bound requires Z_X,tau_PPN,S_PPN,lambda_X and vector-tail zero/bounds | DIRECT_CG_BOUND_NOT_CLAIMED | gate | FAIL_CURRENT_CLAIM_TRANSLATION_MISSING | false | false |


## PPN Branch Classifier

| class_id | branch | implication | current_status | next_need | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PBC2160_0_pure_long_range | universal conformal, massless/solar-long, unscreened, vector tails zero | Cassini constrains alpha_eff and then c_g/sqrt(Z_X) | CONDITIONAL_COMPETITIVE_BRANCH | not current claim | false |
| PBC2160_1_short_range | lambda_X lab scale or shorter | R10/Yukawa bounds dominate; Cassini suppressed | ROUTE_DEPENDS_ON_MISSING_LAMBDA | needs Z_X/M_X^2 | false |
| PBC2160_2_orbital_range | lambda_X Earth-Moon/AU/source-support scale | LLR/orbital/finite-source geometry needed | ROUTE_DEPENDS_ON_MISSING_LAMBDA | needs transfer matrix | false |
| PBC2160_3_screened | nonlinear screening/plateau suppresses solar-system charge | Cassini bounds screened effective charge only | SCREENING_NOT_DERIVED | do not insert plateau axiom | false |
| PBC2160_4_multi_component | PPN vector has nonzero disformal/nonH/support/boundary/readout legs | absolute residual vector must be scored | VECTOR_SCHEMA_READY_VALUES_MISSING | single c_g bound forbidden | false |
| PBC2160_5_current | current active branch | source-backed Cassini proxy exists; MTS translation incomplete | SOURCE_PROXY_ONLY | selected current status | false |


## Claim Gates

| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG2160_0_cassini_source | Cassini observable bound is source-backed | true | gamma envelope and scalar proxy are numeric | false | false |
| CG2160_1_scalar_map_math | scalar-tensor gamma inversion is written | true | conditional standard map is explicit | false | false |
| CG2160_2_NX_owned | N_X=1/sqrt(Z_X) is numeric and parent-owned | false | Z_X/Xhat owner missing | false | false |
| CG2160_3_range_owned | lambda_X/S_PPN route is parent-owned | false | M_X^2/lambda/screening transfer missing | false | false |
| CG2160_4_vector_controlled | PPN residual vector is zero or bounded | false | b_dis/q_nonH/support/boundary/readout legs missing | false | false |
| CG2160_5_direct_cg_bound | Cassini gives direct MTS c_g bound | false | normalization/range/vector gates fail | false | false |
| CG2160_6_local_GR_PPN | local GR/PPN pass is derived | false | no direct c_g bound or full PPN metric expansion | false | false |


## Refusal Runner

| refusal_id | attempted_claim | input_status | runner_result | blocked_by | score_eligible | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REF2160_0_raw_cg_bound | raw c_g <= alpha_proxy | NORMALIZATION_MISSING | BLOCKED | must use c_g/sqrt(Z_X) with tau_PPN and S_PPN | false | false | false |
| REF2160_1_long_range_assumption | Cassini applies unsuppressed | RANGE_TRANSFER_MISSING | BLOCKED | lambda_X and screening/environment map missing | false | false | false |
| REF2160_2_one_parameter_ppn | c_g is the only PPN leg | VECTOR_TAILS_MISSING | BLOCKED | b_dis/q_nonH/support/boundary/readout components retained | false | false | false |
| REF2160_3_local_gr_claim | local GR/PPN recovered | PPN_METRIC_EXPANSION_MISSING | BLOCKED | gamma proxy is not full PPN beta/preferred-frame/conservation proof | false | false | false |
| REF2160_4_empirical_pass | MTS passes Cassini/PPN | DIRECT_COMPONENT_BOUND_MISSING | BLOCKED | source-backed proxy only | false | false | false |


## Decision Ledger

| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2160_0_map_result | The PPN scalar-tensor map is derived only conditionally. | It gives the right comparison object alpha_eff_PPN, not a raw c_g bound. | use alpha_eff or c_g/sqrt(Z_X), never raw c_g | false |
| DEC2160_1_current_block | Direct MTS c_g remains unbounded by Cassini in the current branch. | Z_X, tau_PPN, lambda/S_PPN and vector-tail controls are missing. | keep Cassini as source-backed pressure, not claim | false |
| DEC2160_2_no_circling | Do not re-argue the same scalar-tensor proxy again. | The exact next missing objects are now N_X/lambda and PPN residual vector legs. | 2161 should choose parent Hessian/range extraction or PPN vector fill | false |
| DEC2160_3_next_target | Next target is parent N_X/lambda extraction with PPN vector fallback. | Without Z_X/M_X^2, every PPN/R10/orbital route is only source-backed proxy; without the vector, one-parameter c_g is fake. | 2161-Y5-R2FR-parent-NX-lambda-extraction-or-PPN-vector-envelope.md | false |


## Next Target

| route_id | next_target | script | objective | selection_status | success_condition | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2160_0_2161 | 2161-Y5-R2FR-parent-NX-lambda-extraction-or-PPN-vector-envelope.md | scripts/Y5_R2FR_parent_NX_lambda_extraction_or_PPN_vector_envelope_2161.py | try to source or derive parent Z_X and M_X^2 enough to define N_X and lambda_X; if unavailable, fill the PPN residual-vector no-cancellation envelope over c_g, b_dis, q_nonH, support, boundary and readout terms | selected | either N_X/lambda_X become parent-owned inputs, or the PPN c_g branch is demoted to vector-only source proxy with explicit missing component rows | false |
| NEXT2160_1_parallel | 2161b-Y5-R2FR-no-hidden-visible-hom-operator-domain-theorem.md | scripts/Y5_R2FR_no_hidden_visible_hom_operator_domain_theorem_2161b.py | try to derive the operator-domain theorem that would zero shadow-frame, alpha/mass, marker and source-tail PPN legs | held | vector tails vanish by theorem, reopening a cleaner c_g/PPN path | false |


## Branch Copies

| copy_id | destination | path_exists | row_count | parse_ok | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| COPY2160_0_source_weight_docs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\AFRAME_PPN_CG_2160_NONCLAIM.csv | true | 11 | true | false |
| COPY2160_1_branch_locked_wep | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_2160_PPN_CG_NONCLAIM.csv | true | 12 | true | false |
| COPY2160_2_acquisition_queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2160_NX_LAMBDA_OR_PPN_VECTOR_QUEUE.csv | true | 9 | true | false |


## Validation

| check_id | status | detail | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- |
| VAL2160_00_sources | PASS | 2159 handoff plus 1852/1853 and active local gates validate | false | false |
| VAL2160_01_scalar_map | PASS | scalar-tensor PPN map is conditional and nonclaim | false | false |
| VAL2160_02_normalization_gate | PASS | N_X/Z_X normalization gate blocks direct c_g claim | false | false |
| VAL2160_03_range_gate | PASS | lambda/S_PPN range gate blocks unsuppressed Cassini use | false | false |
| VAL2160_04_ppn_vector | PASS | PPN residual vector no-cancellation envelope is staged | false | false |
| VAL2160_05_cg_bound | PASS | Cassini proxy numeric; direct c_g bound blocked | false | false |
| VAL2160_06_branch_classifier | PASS | current branch classified as source proxy only | false | false |
| VAL2160_07_claim_gates | PASS | source/proxy math exists but no MTS/local claim allowed | false | false |
| VAL2160_08_refusals | PASS | refusal runner blocks raw c_g, long-range, one-parameter PPN, local-GR and pass claims | false | false |
| VAL2160_09_decision_next | PASS | decision ledger selects N_X/lambda or PPN vector target | false | false |
| VAL2160_10_next | PASS | 2161 next target selected | false | false |
| VAL2160_11_branch_copies | PASS | branch copies exist and parse | false | false |
| VAL2160_12_csv_parse | PASS | all generated 2160 CSVs parse cleanly | false | false |
| VAL2160_13_missing_not_ready | PASS | MISSING_* rows stay nonclaim | false | false |
| VAL2160_14_no_claim_flags | PASS | no generated row allows a claim | false | false |
| VAL2160_15_formalization_clean | PASS | formalization-workbench untouched by 2160 | false | false |
| VAL2160_16_no_pycache | PASS | scripts __pycache__ removed | false | false |
| VAL2160_OVERALL | PASS | 2160 derives conditional PPN c_g map and keeps Cassini as source-backed proxy only. | false | false |


## Working Interpretation

This is the useful Cassini result without cheating: Cassini is real pressure on a long-range, unscreened, universal common-frame branch, but it does not yet bind raw MTS `c_g`. The next move is not another proxy; it is either parent-own `Z_X/M_X^2` so `N_X` and `lambda_X` exist, or turn the PPN channel into a full no-cancellation residual vector.