# 2166 - Y5/R2FR Local-GR Reduction Contract And Residual Vector Prioritizer

## Current Verdict

2166 does **not** derive local GR/Newton, does **not** derive `D_R[MTS]=partial_r C_R-S_R`, and does **not** prove `S_R=0` or `Q_R=0`.

It does make the local-GR reduction contract sharp: `C_R=ln(T^2 S)=0` is the exact reciprocal target, and every live residual in `R_local^MTS` is forced into an `S_R` slot. Nothing can hide in fitted source normalization, readout, q_loc, boundary hair, or coupling language.

The carried-forward obstruction is important: a generic parent Euler difference is too weak. The missing gear is a parent-owned reciprocity-selector orientation/kernel or explicit `L_MTS_core/H_core` whose Euler equation selects `C_R` without importing GR.

This follows the 2165 handoff at line 107, imports the 1864 local-GR contract at line 45, and carries the 1865 `D_R` obstruction at line 52.

## Source Register

| source_id | source_path | path_exists | needles_found | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC2166_00_2165_handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2165-Y5-R2FR-single-parent-current-chain-synthesis-or-Ix-Jx-demotion.md | true | true | 2165 routes R_local^MTS into the local-GR contract. | false |
| SRC2166_01_2165_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2165_VALIDATION.csv | true | true | 2165 validation passed as nonclaim. | false |
| SRC2166_02_2165_next_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2165_NEXT_TARGET.csv | true | true | machine-readable 2166 handoff. | false |
| SRC2166_03_1864_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1864-Y5-R2FR-local-GR-reduction-contract-and-residual-vector-prioritizer.md | true | true | prior local-GR theorem contract and residual prioritizer. | false |
| SRC2166_04_1864_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1864_VALIDATION.csv | true | true | 1864 validation passed as nonclaim. | false |
| SRC2166_05_1865_dr_attempt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1865-Y5-R2FR-parent-Euler-difference-normal-form-or-SR-residual-decomposition.md | true | true | prior D_R derivation attempt finds generic Euler-difference obstruction and selects reciprocity selector/H_core. | false |
| SRC2166_06_1865_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1865_VALIDATION.csv | true | true | 1865 validation passed as nonclaim. | false |


## Local-GR Reduction Theorem

| theorem_id | object | statement | status | consequence | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| LGT2166_0_variables | local reciprocal variables | J_q:=T sqrt(S); C_R:=ln(T^2 S)=2 ln(J_q) | EXACT_DEFINITION | C_R=0 is equivalent to reciprocal local branch T^2 S=1 | false |
| LGT2166_1_parent_Euler_pair | parent E_time/E_radial | derive E_time=delta S_parent/delta ln(T), E_radial=delta S_parent/delta ln(sqrt(S)) from MTS parent action | MISSING_EULER_PAIR | legal variables for a reduction proof are not yet parent-owned | false |
| LGT2166_2_DR_normal_form | D_R[MTS] normal form | D_R=E_time-E_radial=partial_r C_R-S_R[R_local^MTS,source,boundary,readout]=0, or partial_r(W partial_r C_R)-J_R=0 | CONTRACT_READY_NOT_DERIVED | generic Euler difference does not force this form | false |
| LGT2166_3_SR_silence | S_R=0 or finite-bounded | all R_local^MTS components must vanish by theorem or be retained as finite absolute bounds | RESIDUAL_VECTOR_RETAINED | no coupling/source/readout term may be hidden in fitted GM | false |
| LGT2166_4_boundary_no_charge | Q_R=0 and normalization | boundary/source neutrality plus C_R(infinity)=0 integrates the source-free equation to C_R=0 | BOUNDARY_NO_CHARGE_UNSIGNED | conserved current alone leaves Q_R hair | false |
| LGT2166_5_reciprocal_consequence | local GR-style branch | if LGT2166_1 through LGT2166_4 close, C_R=0; with T^2=1-L and S=(1-L)^(-p), p=1 | EXACT_CONDITIONAL_NOT_ACTIVATED | would be the serious local GR/Newton reduction route | false |
| LGT2166_6_verdict | local GR/Newton derivation | current MTS has theorem contract but not parent Euler pair, D_R normal form, S_R silence or Q_R no-charge | LOCAL_GR_REDUCTION_CONTRACT_READY_NOT_DERIVED | select reciprocity-selector/H_core source equation as next missing gear | false |


## R_local To S_R Map

| slot_id | sr_slot | residual_symbol | symbolic_entry | current_status | arena_links | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RSM2166_0_Delta_Hsrc | S_R_source_measure | Delta_Hsrc | c_H Delta_Hsrc/M_H_ref | CENTRAL_Y5_RESIDUAL_RETAINED | orbital;Gauss;PPN;Newton | false |
| RSM2166_1_I_X | S_R_current_curl | I_X | c_I I_X/M_H_ref | NOT_THEOREM_ZERO | orbital;PPN;source_normalization;local_GR | false |
| RSM2166_2_J_X_qbarXT | S_R_matter_source | J_X/qbar_XT | c_J J_X + c_q qbar_XT | SOURCE_ZERO_NOT_PROVED_COMPONENT_VALUES_MISSING | R10;WEP;clock;PPN;orbital | false |
| RSM2166_3_constants | S_R_constant_composition | b_alpha,b_mu,b_mA,b_nuc,b_clock_i | c_alpha b_alpha + c_mu b_mu + c_A b_mA + c_nuc b_nuc + Sigma_i c_clock_i b_clock_i | ALPHA_MASS_CLOCK_CHANNELS_RETAINED | fine_structure;WEP;clock;R10 | false |
| RSM2166_4_boundary_history | S_R_boundary_history | J_boundary,J_history,qbar_nonH | c_B B_R + c_hist H_R + c_nonH qbar_nonH | TAILS_NOT_ZERO_NOT_BOUNDED | orbital;source_normalization;R10;local_GR | false |
| RSM2166_5_q_loc | S_R_extra_sector | epsilon_GK_q_loc | c_GK epsilon_GK_q_loc | RETAIN_NONCLAIM | local_GR;PPN;clock;orbital;WEP;R10 | false |
| RSM2166_6_reciprocal_hair | S_R_QR_hair | Q_R,J_R | Q_R or int J_R dr after operator integration | NO_CHARGE_THEOREM_NOT_DERIVED | PPN_gamma;orbital;lightcone;local_GR | false |
| RSM2166_7_readout | S_R_readout_projection | C_readout,Delta_Pi | c_readout C_readout + c_proj Delta_Pi | PURE_POSTPROCESSING_SAFE_NOT_GENERAL | Pantheon;BAO;SPARC;R10;WEP;clock;PPN | false |
| RSM2166_8_total | S_R_total_abs | S_R[R_local^MTS] | \|S_R\| <= sum absolute values of RSM2166_0 through RSM2166_7 | SYMBOLIC_READY_VALUES_MISSING | local_GR;PPN;orbital;R10;WEP;clock | false |


## Proof Attack Prioritizer

| priority_id | target | impact | tractability | dependency | scrutiny_risk | rationale | selection | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR2166_0_reciprocity_selector | derive selector orientation/kernel or H_core source equation | 5 | 4 | 5 | 5 | generic Euler difference no-go means this is the missing gear | SELECT_FIRST | false |
| PR2166_1_q_loc_live_pair | Gamma_eff/K_hat live metric-response pair or S_R source row | 5 | 3 | 4 | 4 | q_loc contaminates S_R, but selector must first define its slot | SECOND_AFTER_SELECTOR | false |
| PR2166_2_no_extra_matter_vertices | forbid extra F2/mass/binding/source-weight vertices | 4 | 3 | 5 | 5 | coupling gut-punch, held parallel until S_R coefficients are oriented | HELD_PARALLEL_HIGH_VALUE | false |
| PR2166_3_boundary_no_charge | prove Q_R=0 and boundary/reference normalization | 4 | 3 | 3 | 3 | necessary after S_R silence, but needs operator form | THIRD_OR_PARALLEL_AFTER_OPERATOR | false |
| PR2166_4_source_coefficients | source finite S_R coefficients and units | 3 | 4 | 4 | 4 | empirical backstop after selector/source map exists | BACKSTOP_AFTER_OPERATOR | false |


## First Attack Status

| attack_id | target | statement | status | consequence | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| FAS2166_0_generic_action | generic parent action slice | for S=int dr L(x,y,x',y'), E_x-E_y=(partial_x-partial_y)L-d/dr[(partial_xprime-partial_yprime)L] | DERIVED_GENERIC_IDENTITY | too weak to imply partial_r C_R-S_R | false |
| FAS2166_1_orientation | Euler orientation/sign | which parent variation combination selects C_R must be parent-signed | ORIENTATION_CERTIFICATE_REQUIRED | cannot infer from GR equation difference | false |
| FAS2166_2_selector | reciprocity selector/operator | need parent kernel yielding partial_r C_R or partial_r(W partial_r C_R) | MISSING_RECIPROCITY_SELECTOR_OR_PARENT_KERNEL | no no-hair/local reciprocity theorem can run | false |
| FAS2166_3_SR_decomposition | S_R residual source map | all known local residuals have symbolic S_R slots | SYMBOLIC_DECOMPOSITION_READY_NONCLAIM | coefficients/units/source maps missing | false |
| FAS2166_4_verdict | first proof attack | D_R normal form was attempted through generic variation and did not derive | DR_NORMAL_FORM_NOT_DERIVED_CURRENT_CORPUS | target H_core/selector/source equation next | false |


## Claim Gates

| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG2166_0_contract_ready | local-GR reduction theorem contract is exact conditional | true | C_R=0 consequence is clean if premises close | false | false |
| CG2166_1_DR_derived | D_R[MTS]=partial_r C_R-S_R is derived | false | selector/orientation/H_core missing | false | false |
| CG2166_2_SR_zero | S_R=0 on local branch | false | all residual slots remain nonclaim | false | false |
| CG2166_3_QR_zero | Q_R boundary/no-charge theorem closes | false | boundary/source neutrality unsigned | false | false |
| CG2166_4_local_GR | MTS derives local GR/Newton branch | false | D_R/S_R/Q_R premises not closed | false | false |
| CG2166_5_empirical_ready | S_R residual vector can be scored | false | coefficients/units/arena projections missing | false | false |


## Refusal Runner

| refusal_id | attempted_claim | input_status | runner_result | blocked_by | score_eligible | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REF2166_0_gr_import | use GR radial identity as MTS proof | FORBIDDEN_GR_IMPORT | BLOCKED | EH fixed point not derived first | false | false | false |
| REF2166_1_generic_euler | claim generic Euler difference gives C_R operator | GENERIC_DIFFERENCE_TOO_WEAK | BLOCKED | selector/orientation missing | false | false | false |
| REF2166_2_hide_residuals | drop R_local^MTS outside S_R | RESIDUAL_MAP_REQUIRED | BLOCKED | every residual has an S_R slot | false | false | false |
| REF2166_3_nocharge_by_words | set Q_R=0 by local-vacuum wording | NO_CHARGE_THEOREM_UNSIGNED | BLOCKED | conservation leaves Q_R constant | false | false | false |
| REF2166_4_local_gr | claim local GR/Newton now | D_R_SR_QR_OPEN | BLOCKED | contract ready but not derived | false | false | false |


## Decision Ledger

| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2166_0_contract | The local-GR reduction theorem is now a precise contract, not a claim. | C_R=0 follows only after parent D_R, S_R silence and Q_R no-charge close. | use as proof checklist | false |
| DEC2166_1_obstruction | Generic Euler variation is insufficient. | E_time-E_radial does not automatically select partial_r C_R. | derive reciprocity selector/H_core kernel next | false |
| DEC2166_2_residual_map | R_local^MTS must enter S_R explicitly. | Delta_Hsrc, I_X/J_X, constants, boundary/history, q_loc, reciprocal hair and readout all have slots. | no residual hiding | false |
| DEC2166_3_next | Next checkpoint is reciprocity-selector operator or H_core source equation. | this is the missing gear that could make D_R a real MTS equation rather than a closure benchmark. | 2167-Y5-R2FR-reciprocity-selector-operator-or-Hcore-source-equation.md | false |


## Next Target

| route_id | next_target | script | objective | selection_status | success_condition | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2166_0_2167 | 2167-Y5-R2FR-reciprocity-selector-operator-or-Hcore-source-equation.md | scripts/Y5_R2FR_reciprocity_selector_operator_or_Hcore_source_equation_2167.py | try to derive the parent reciprocity-selector orientation/kernel that makes the time/radial Euler combination select C_R; if unavailable, demote D_R to a closure-only benchmark and emit source-ready Z_R/J_R/S_R coefficient requirements | selected | parent-owned L_MTS_core/H_core yields the C_R operator without GR import, or all missing selector/source/operator inputs become explicit nonclaim rows | false |
| NEXT2166_1_parallel_QR | 2167b-Y5-R2FR-reciprocal-no-charge-boundary-theorem-or-QR-source-row.md | scripts/Y5_R2FR_reciprocal_no_charge_boundary_theorem_or_QR_source_row_2167b.py | attempt Q_R=0 from boundary/source neutrality; if not, create finite Q_R/J_R source rows for PPN/orbital/lightcone comparison | held | Q_R no-charge theorem or finite sourced reciprocal-hair residual rows | false |
| NEXT2166_2_parallel_q_loc | 2167c-Y5-R2FR-epsilon-GK-q-loc-to-SR-coefficient-map.md | scripts/Y5_R2FR_epsilon_GK_qloc_to_SR_coefficient_map_2167c.py | map epsilon_GK_q_loc into S_R with a declared coefficient/unit convention or prove the q_loc source slot vanishes | held | q_loc term is parent-zero or source-ready as an S_R component | false |


## Branch Copies

| copy_id | destination | path_exists | row_count | parse_ok | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| COPY2166_0_source_weight_docs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\AFRAME_LOCAL_GR_CONTRACT_2166_NONCLAIM.csv | true | 12 | true | false |
| COPY2166_1_branch_locked_wep | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_2166_SR_VECTOR_NONCLAIM.csv | true | 9 | true | false |
| COPY2166_2_acquisition_queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2166_RECIPROCITY_SELECTOR_OR_HCORE_QUEUE.csv | true | 8 | true | false |


## Validation

| check_id | status | detail | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- |
| VAL2166_00_sources | PASS | 2165 plus 1864/1865 source paths and needles validate | false | false |
| VAL2166_01_theorem | PASS | local-GR theorem contract is ready but not derived | false | false |
| VAL2166_02_sr_map | PASS | R_local^MTS components all enter S_R slots | false | false |
| VAL2166_03_prioritizer | PASS | reciprocity selector/H_core target selected first | false | false |
| VAL2166_04_first_attack | PASS | generic Euler-difference obstruction is carried forward | false | false |
| VAL2166_05_claim_gates | PASS | contract can pass while D_R/local-GR claims remain blocked | false | false |
| VAL2166_06_refusals | PASS | refusal runner blocks GR import, generic Euler shortcut, residual hiding, no-charge and local-GR claims | false | false |
| VAL2166_07_decision | PASS | decision ledger selects 2167 reciprocity selector/H_core | false | false |
| VAL2166_08_next | PASS | 2167 next target selected | false | false |
| VAL2166_09_branch_copies | PASS | branch copies exist and parse | false | false |
| VAL2166_10_csv_parse | PASS | all generated 2166 CSVs parse cleanly | false | false |
| VAL2166_11_no_claim_flags | PASS | no generated row allows a claim | false | false |
| VAL2166_12_formalization_clean | PASS | formalization-workbench untouched by 2166 | false | false |
| VAL2166_13_no_pycache | PASS | scripts __pycache__ removed | false | false |
| VAL2166_OVERALL | PASS | 2166 builds the local-GR contract, maps R_local into S_R, and selects the reciprocity selector/H_core gate. | false | false |


## Working Interpretation

This is the right kind of grim-but-good progress. We are not pretending the local GR branch is derived; we are specifying exactly what would derive it. The next proof is not 'more coupling hunting' in the fog. It is the reciprocity selector: find the parent operator or `H_core` that makes the time/radial equation difference select `C_R`. If that fails, the branch becomes a closure benchmark with explicit source-ready residual coefficients.