# 2527 - `q` Object / Vertical Generator Open-Branch Proof or Domain Bound

**Current verdict:** the matter-coupling contract from 2526 does not create `q`; it only says what happens if `q` already exists. The open-branch proof still fails under current evidence because the parent field chart, equivalence relation, smooth quotient map, constant-rank `Dq`, vertical basis, and local-generator decomposition are not jointly parent-signed.

**Main gain:** this narrows the missing geometry to one exact theorem contract: on an open branch `U`, construct `q: U -> Q_vis` as a constant-rank quotient and prove `X_loc in ker(Dq)` modulo owned EOM/boundary terms. If that cannot be done, the theory owes finite `Dq_vertical_leak` / domain-motion rows.

**Claim discipline:** no local-GR, Newton, PPN, R10, clock, orbital, GitHub, or public claim is allowed from 2527. This is a private proof gate and residual ledger.

## Source Register

| source_id | source_path | path_exists | needle_found | status | role |
| --- | --- | --- | --- | --- | --- |
| SRC2527_0_2526_doc | 2526-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md | True | True | SOURCE_OK | immediate handoff selecting q-object / vertical-generator proof |
| SRC2527_1_2526_validation | source-intake/mts_residuals/P8_Y5_BRR545_2526_VALIDATION.csv | True | True | SOURCE_OK | 2526 validation anchor |
| SRC2527_2_2526_signing | source-intake/mts_residuals/P8_Y5_NO_SHADOW_2526_ACTION_SIGNING_TESTS.csv | True | True | SOURCE_OK | q and verticality remain unsigned after matter coupling |
| SRC2527_3_2358_doc | 2358-Y5-R2FR-q-object-vertical-generator-open-branch-proof-or-domain-bound.md | True | True | SOURCE_OK | prior q/v proof attempt and failure mode |
| SRC2527_4_2358_validation | source-intake/mts_residuals/P8_Y5_BRR545_2358_VALIDATION.csv | True | True | SOURCE_OK | 2358 validation anchor |
| SRC2527_5_2358_audit | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2358_Q_VERTICAL_OPEN_BRANCH_AUDIT.csv | True | True | SOURCE_OK | q object and vertical basis audit rows |
| SRC2527_6_2358_kernel | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2358_DQ_KERNEL_GATE_MATRIX.csv | True | True | SOURCE_OK | Dq kernel gate precedent |
| SRC2527_7_2356_doc | 2356-Y5-R2FR-parent-source-current-descent-or-domain-motion-bound.md | True | True | SOURCE_OK | source-current descent clauses requiring q and verticality |
| SRC2527_8_2223_doc | 2223-Y5-R2FR-quotient-map-vertical-generator-frontier-import-or-finite-coupling-row.md | True | True | SOURCE_OK | older q/Dq frontier import and finite fallback |
| SRC2527_9_1541_doc | 1541-Y5-quotient-map-vertical-generator-kernel-certificate.md | True | True | SOURCE_OK | earlier q-map vertical-generator certificate attempt |

## Open-Branch `q` / Verticality Audit

| row_id | clause | required_statement | proof_attempt | current_evidence | status | blocks_claim |
| --- | --- | --- | --- | --- | --- | --- |
| QVA2527_0_parent_field_chart | parent field chart | there is an open parent branch U with field coordinates Phi^I and smooth transition rules | needed before q can be a differentiable map rather than a label on variables | 2358 and 2223 name the need but do not parent-sign the chart | PARENT_CHART_NOT_SIGNED | True |
| QVA2527_1_equivalence_relation | visible-state equivalence relation | Phi ~ Phi' iff every visible/ordinary-matter stack component agrees | must be parent-defined before any quotient map q exists | MCA2526 uses q(Phi), but does not derive the equivalence relation | EQUIVALENCE_RELATION_NOT_SIGNED | True |
| QVA2527_2_q_map | parent quotient map | q: U -> Q_vis is smooth and maps parent fields to quotient-owned observed data | candidate q is exactly the map needed by MCA2526 and source-current descent | uses q but no source gives q's component formula and target space | Q_OBJECT_NOT_PARENT_SIGNED | True |
| QVA2527_3_constant_rank_open_branch | submersion / constant-rank condition | rank Dq is constant on an open local branch, so ker(Dq) is a smooth vertical bundle | without constant rank, a one-point kernel identity is not a local theorem | no Dq matrix/rank certificate exists for the current MTS parent variables | OPEN_BRANCH_RANK_NOT_SIGNED | True |
| QVA2527_4_vertical_basis | vertical generator basis | there are smooth basis fields v_a spanning ker(Dq) on U | verticality must be a tangent-to-fibres statement, not a name given to a residual | 2358 retains Dq kernel rows because the basis is not parent-signed | VERTICAL_BASIS_NOT_SIGNED | True |
| QVA2527_5_local_generator_decomposition | local residual generator decomposition | X_loc = c^a v_a + EOM + boundary/support terms on U | only then does Dq[X_loc]=0 modulo owned EOM/boundary pieces | no source decomposes the physical local generator into the q-vertical basis | LOCAL_GENERATOR_DECOMPOSITION_NOT_SIGNED | True |
| QVA2527_6_kernel_conclusion | open-branch kernel theorem | Dq[X_loc]=0 throughout U, not only at a point or in a chosen representative | would close AST2526_0 and AST2526_1 and activate the coupling theorem | antecedents QVA2527_0..5 are unsigned | KERNEL_THEOREM_NOT_PROMOTED | True |

## `Dq` Kernel Gate Matrix

| row_id | object | zero_condition | current_status | finite_fallback | claim_ready |
| --- | --- | --- | --- | --- | --- |
| DQM2527_0_q_component_formula | q^A(Phi) | component formulas are parent-derived and differentiable | MISSING_Q_COMPONENT_FORMULA | record q_component_source and q_component_uncertainty before scoring | False |
| DQM2527_1_Dq_matrix | partial q^A / partial Phi^I | Dq matrix exists on U and has constant rank | MISSING_DQ_MATRIX_AND_RANK_CERTIFICATE | epsilon_Dq_rank_or_projection_leak | False |
| DQM2527_2_vertical_basis_matrix | v_a^I | basis spans ker(Dq) on U | MISSING_VERTICAL_BASIS_SOURCE | basis_completeness_defect | False |
| DQM2527_3_kernel_product | Dq_A_I v_a^I | all Dq[v_a] vanish as symbolic identities on U | KERNEL_PRODUCT_UNSIGNED | max_a ||Dq[v_a]||_Q / ||v_a||_F | False |
| DQM2527_4_local_generator_projection | Dq[X_loc] | X_loc lies in span{v_a}+EOM+boundary with bounded support terms | LOCAL_GENERATOR_PROJECTION_UNSIGNED | epsilon_Dq_Xloc_abs | False |
| DQM2527_5_kernel_total | open-branch Dq kernel gate | DQM2527_0..4 close on the same branch and norm | Dq_KERNEL_UNSIGNED_RETAIN_BOUND_ROWS | Dq_vertical_leak_total | False |

## Finite Domain Bound Rows

| row_id | quantity | definition | required_inputs | units | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| DQB2527_0_Dq_vertical_leak_total | epsilon_Dq_vertical_total | max_a ||Dq[v_a]||_Q / ||v_a||_F on the selected open branch | q_component_formula;Dq_matrix;vertical_basis;Q_norm;F_norm;open_branch_domain | dimensionless after norm declaration | MISSING_COMPONENT_VALUES | False |
| DQB2527_1_Xloc_projection_leak | epsilon_Dq_Xloc_abs | ||Dq[X_loc]||_Q / ||X_loc||_F including owned EOM and boundary remainder contract | Xloc_formula;generator_decomposition;Dq_matrix;boundary_remainder_bound | dimensionless after norm declaration | MISSING_XLOC_FORMULA_AND_PROJECTION | False |
| DQB2527_2_rank_defect | epsilon_rank_branch | measure of constant-rank failure or singular-set proximity on U | rank_Dq;domain_U;singular_set_distance;regularity_class | dimensionless or declared chart units | MISSING_RANK_CERTIFICATE | False |
| DQB2527_3_domain_current_bound | J_domain_Dq_abs | K_Dq * epsilon_Dq_Xloc_abs * A_source * S_link / M_H_ref | K_Dq;epsilon_Dq_Xloc_abs;A_source;S_link;M_H_ref | dimensionless only after M_H_ref and source norm are parent-signed | MISSING_DQ_AND_SOURCE_NORMALIZATION_INPUTS | False |
| DQB2527_4_arena_projection | arena Dq leak rows | R10/PPN/clock/orbital projections of the same Dq leak quantity | arena_projectors;units;source_path;row_id;validity_flags | arena-specific | MISSING_ARENA_PROJECTIONS | False |

## Claim Gates

| row_id | claim | allowed | blocked_by |
| --- | --- | --- | --- |
| CG2527_0_q_object | parent q object exists before matter/readout | False | QVA2527_0_parent_field_chart;QVA2527_1_equivalence_relation;QVA2527_2_q_map |
| CG2527_1_vertical_generator | local generator is in ker(Dq) on an open branch | False | QVA2527_3_constant_rank_open_branch;QVA2527_4_vertical_basis;QVA2527_5_local_generator_decomposition |
| CG2527_2_source_current_descent | MCA2526 coupling theorem fires for current MTS | False | CG2527_0_q_object;CG2527_1_vertical_generator;MCA2526_adoption_missing |
| CG2527_3_local_GR_Newton | local GR/Newton branch derived | False | CG2527_2_source_current_descent;M_H_ref;boundary_support;domain_motion_rows |
| CG2527_4_public_or_github | public claim or GitHub update recommended from 2527 | False | all q/Dq rows nonclaim |

## Refusal Runner

| row_id | shortcut | verdict | reason | required_repair |
| --- | --- | --- | --- | --- |
| REF2527_0_q_by_name | declare q because the matter action uses q(Phi) | REJECT | using q in MCA2526 is not a parent construction of q | field chart, equivalence relation, target space and component formulas |
| REF2527_1_vertical_by_label | call X_loc vertical because it is hidden/local | REJECT | vertical means tangent to fibres of q: Dq[X_loc]=0 on an open branch | Dq matrix and generator decomposition |
| REF2527_2_point_kernel | prove Dq[v]=0 at one point or one representative | REJECT | source-current descent requires an open-branch theorem, not a point identity | constant-rank certificate and open-domain statement |
| REF2527_3_no_pole_selector_as_q | use no-pole/no-shadow selector as the quotient map without a smooth quotient construction | REJECT_AS_CURRENT_PROOF | it may become a route, but it must define the same q target and Dq kernel | convert selector into a field chart/equivalence relation or keep it as a finite selector leak |
| REF2527_4_observed_stack_backfill | define q by observed GR/Newton variables already known to work | REJECT | that imports the desired local limit instead of deriving it | parent-owned construction before fitting/readout |

## Decision Ledger

| row_id | decision | reason | next_action | status |
| --- | --- | --- | --- | --- |
| DEC2527_0_theorem_shape | retain exact q-vertical theorem contract | if q is a constant-rank parent quotient and X_loc is tangent to q-fibres, source-current descent becomes a real theorem instead of an axiom | prove the parent field chart/equivalence relation or demote to finite Dq leak rows | ACTIVE |
| DEC2527_1_no_promotion | do not claim q/v closure | current evidence still lacks q component formulas, Dq matrix, rank certificate, and local generator decomposition | keep CG2527 gates false | BLOCK_CLAIM |
| DEC2527_2_selected_route | select parent field-chart/equivalence construction next | that is the upstream missing object; another coupling ansatz cannot create q after the fact | 2528 field-chart/equivalence relation or no-pole selector conversion | SELECTED |
| DEC2527_3_fallback | preserve finite Dq/domain rows | if the quotient cannot be derived, the theory must pay a measurable residual rather than hide the leak | source DQB2527 rows with units and arena projections | HELD_PARALLEL |

## Next Target

| row_id | priority | next_target | script | objective | acceptance_gate | do_not |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2527_0_selected | selected | 2528-Y5-R2FR-parent-q-field-chart-equivalence-relation-or-no-pole-selector.md | scripts/Y5_R2FR_parent_q_field_chart_equivalence_relation_or_no_pole_selector_2528.py | construct a parent field chart and equivalence relation that makes q a smooth constant-rank quotient, or convert the no-pole/no-shadow selector into an explicit finite selector leak | q target, component formulas, Dq matrix, rank certificate, and equivalence relation are all parent-signed on one open branch, otherwise no q/v claim | do not define q by observed GR variables; do not use one-point verticality; do not claim local GR/Newton |
| NEXT2527_1_fallback | fallback_nonclaim | 2528b-Y5-R2FR-Dq-domain-bound-input-pack.md | scripts/Y5_R2FR_Dq_domain_bound_input_pack_2528b.py | source every finite Dq/domain leak input with units, norms, and arena projections | all DQB2527 rows have numeric values or remain explicitly blocked nonclaim | do not score missing Dq rows or use placeholders as local-GR evidence |
| NEXT2527_2_later | queued_after_q_route | 2529-Y5-R2FR-fibre-Bh-finite-row-or-hidden-visible-grammar-reentry.md | scripts/Y5_R2FR_fibre_Bh_finite_row_or_hidden_visible_grammar_reentry_2529.py | return to the fibre B_h residual after the q/source-current lane is narrowed | B_h is theorem-zero or finite nonclaim rows are sourced | do not erase independent fibre residuals with the matter-coupling contract |

## Branch Copies

| copy_id | source_path | destination_path | destination_exists | status |
| --- | --- | --- | --- | --- |
| open_branch_audit | source-intake\mts_residuals\P8_Y5_NO_SHADOW_2527_Q_VERTICAL_OPEN_BRANCH_REENTRY_AUDIT.csv | source-intake\beta-source\docs\Q_vertical_open_branch_reentry_2527_NONCLAIM.csv | True | COPIED_NONCLAIM |
| kernel_gate | source-intake\mts_residuals\P8_Y5_NO_SHADOW_2527_DQ_KERNEL_GATE_MATRIX.csv | source-intake\local_bounds\Dq_vertical_kernel_gate_2527_NONCLAIM.csv | True | COPIED_NONCLAIM |
| domain_bound_rows | source-intake\mts_residuals\P8_Y5_NO_SHADOW_2527_DQ_DOMAIN_BOUND_ROWS.csv | source-intake\rab-sector\acquisition-queue\DQ2527_DOMAIN_BOUND_ROWS_NONCLAIM.csv | True | COPIED_NONCLAIM |
| next_target | source-intake\mts_residuals\P8_Y5_NO_SHADOW_2527_NEXT_TARGET.csv | source-intake\rab-sector\acquisition-queue\DQ2527_NEXT_TARGET_NONCLAIM.csv | True | COPIED_NONCLAIM |

## Validation

| check_id | status | details |
| --- | --- | --- |
| VAL2527_00_sources_exist | PASS | every required source path exists |
| VAL2527_01_source_needles | PASS | required source needles found |
| VAL2527_02_open_branch_blockers | PASS | q/v open branch clauses remain honest blockers |
| VAL2527_03_q_and_verticality_unsigned | PASS | q object and vertical basis are explicitly unsigned |
| VAL2527_04_kernel_gate_nonclaim | PASS | Dq kernel matrix rows remain nonclaim |
| VAL2527_05_bound_rows_nonclaim | PASS | finite Dq/domain rows remain nonclaim |
| VAL2527_06_claim_gates_blocked | PASS | all claim gates blocked |
| VAL2527_07_refusals_cover_shortcuts | PASS | shortcuts refused |
| VAL2527_08_next_selected | PASS | field-chart/equivalence target selected |
| VAL2527_09_no_claim_flags | PASS | no generated row enables claim flags |
| VAL2527_10_branch_copies | PASS | branch copies exist |
| VAL2527_11_no_formalization_artifacts | PASS | no outputs target formalization-workbench |
| VAL2527_12_pycache_absent | PASS | scripts __pycache__ absent |
| VAL2527_CSV_P8_Y5_NO_SHADOW_2527_SOURCE_REGISTER | PASS | P8_Y5_NO_SHADOW_2527_SOURCE_REGISTER.csv parses |
| VAL2527_CSV_P8_Y5_NO_SHADOW_2527_Q_VERTICAL_OPEN_BRANCH_REENTRY_AUDIT | PASS | P8_Y5_NO_SHADOW_2527_Q_VERTICAL_OPEN_BRANCH_REENTRY_AUDIT.csv parses |
| VAL2527_CSV_P8_Y5_NO_SHADOW_2527_DQ_KERNEL_GATE_MATRIX | PASS | P8_Y5_NO_SHADOW_2527_DQ_KERNEL_GATE_MATRIX.csv parses |
| VAL2527_CSV_P8_Y5_NO_SHADOW_2527_DQ_DOMAIN_BOUND_ROWS | PASS | P8_Y5_NO_SHADOW_2527_DQ_DOMAIN_BOUND_ROWS.csv parses |
| VAL2527_CSV_P8_Y5_NO_SHADOW_2527_CLAIM_GATES | PASS | P8_Y5_NO_SHADOW_2527_CLAIM_GATES.csv parses |
| VAL2527_CSV_P8_Y5_NO_SHADOW_2527_REFUSAL_RUNNER | PASS | P8_Y5_NO_SHADOW_2527_REFUSAL_RUNNER.csv parses |
| VAL2527_CSV_P8_Y5_NO_SHADOW_2527_DECISION_LEDGER | PASS | P8_Y5_NO_SHADOW_2527_DECISION_LEDGER.csv parses |
| VAL2527_CSV_P8_Y5_NO_SHADOW_2527_NEXT_TARGET | PASS | P8_Y5_NO_SHADOW_2527_NEXT_TARGET.csv parses |
| VAL2527_CSV_P8_Y5_NO_SHADOW_2527_BRANCH_COPIES | PASS | P8_Y5_NO_SHADOW_2527_BRANCH_COPIES.csv parses |
| VAL2527_COPY_CSV_open_branch_audit | PASS | Q_vertical_open_branch_reentry_2527_NONCLAIM.csv parses |
| VAL2527_COPY_CSV_kernel_gate | PASS | Dq_vertical_kernel_gate_2527_NONCLAIM.csv parses |
| VAL2527_COPY_CSV_domain_bound_rows | PASS | DQ2527_DOMAIN_BOUND_ROWS_NONCLAIM.csv parses |
| VAL2527_COPY_CSV_next_target | PASS | DQ2527_NEXT_TARGET_NONCLAIM.csv parses |
| VAL2527_OVERALL | PASS | 2527 imports the prior q/v failure, writes the exact open-branch quotient theorem contract, keeps Dq/domain rows nonclaim, and selects parent field-chart/equivalence construction next. |
