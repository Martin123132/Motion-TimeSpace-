# 2385 - selector functional from relative boundary class or Delta-ref values

## Result

2385 builds the lowest-cheat selector-functional route found so far:

`S_sel = int_boundary <lambda_bc, F_bc(Sigma_ref; B_class, C_top, tau, e_infty)>_top`.

This is better than immediately using a norm-square/Hodge selector because it can be formulated as a constraint action;
the metric/source-dependent pairing problem is pushed into an explicit gate instead of hidden inside a norm.

The variation is clean as a future contract:

`delta_lambda S_sel = F_bc = 0`,

`delta_Sigma S_sel = (D_Sigma F_bc)^dagger lambda_bc = 0`.

If `F_bc` is source-free and `D_Sigma F_bc` is full rank after quotienting gauge/topological zero modes, then 2383's
implicit-function route gives source-blind `Sigma_ref`.  But current MTS still lacks parent-owned `F_bc` components,
source-free pairing, rank proof, and `M_H_ref`.  So this is a sharpened contract, not a proof.

No `Delta_ref=0`, `B_zero_flux=0`, Newton, local-GR, PPN, orbital, clock, R10, or public/GitHub claim is made.

## Source Register

| row_id | source_key | source_path | exists | needles_found | source_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2385_00_2384_doc | 2384_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2384-Y5-R2FR-boundary-stationarity-equation-for-Sigma-ref-or-source-pack-fill.md | true | true | 2384 handoff to selector functional construction | false |
| SRC2385_01_2384_stationarity | 2384_stationarity | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2384_BOUNDARY_STATIONARITY_ATTEMPT.csv | true | true | stationarity equation and sufficient selector-action contract | false |
| SRC2385_02_60_doc | 60_relative_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\60-relative-cohomology-boundary-contract.md | true | true | relative cohomology boundary contract precedent | false |
| SRC2385_03_71_doc | 71_relative_current | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\71-relative-boundary-current-construction-attempt.md | true | true | relative current construction precedent and nonclaim status | false |
| SRC2385_04_996_doc | 996_relative_owner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\996-Y5-R10-relative-boundary-class-owner-or-Bref-source-bound-pack.md | true | true | relative boundary class owner failure and contract | false |
| SRC2385_05_1020_doc | 1020_domain_certificate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md | true | true | boundary/cohomology/corner conditions | false |
| SRC2385_06_1020_domain_csv | 1020_domain_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1020_BOUNDARY_DOMAIN_CERTIFICATE.csv | true | true | machine-readable boundary class/cohomology certificates | false |
| SRC2385_07_667_ansatz | 667_ansatz | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv | true | true | parent boundary action scaffold | false |
| SRC2385_08_2384_next | 2384_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2384_NEXT_TARGET.csv | true | true | machine-readable 2385 target | false |

## Relative Selector Functional

| row_id | component | functional_form | why_this_route | current_status | missing_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RSF2385_0_constraint_map | relative boundary constraint map | F_bc(Sigma_ref;B_class,C_top,tau,e_infty)=(C_rel(Sigma_ref)-C_top, d_S B_ref-h_rel-r_rel, corner_lock, tau_lock, frame_lock, S0_lock) | turns reference selection into explicit constraints on relative class/domain data | CONSTRAINT_MAP_WRITTEN_NOT_PARENT_OWNED | parent-owned definitions of C_rel, h_rel, r_rel, corner_lock, tau_lock, frame_lock and S0_lock | false |
| RSF2385_1_multiplier_action | lower-scrutiny selector action | S_sel=int_boundary <lambda_bc,F_bc>_top | Lagrange multiplier constraints avoid importing a metric/Hodge norm into the selector unless a source-free pairing is proved | SUFFICIENT_CONTRACT_NOT_CURRENT_PARENT_ACTION | topological/source-free pairing, multiplier boundary conditions and parent action inclusion | false |
| RSF2385_2_stationarity | stationarity equations | delta_lambda S_sel=F_bc=0; delta_Sigma S_sel=(D_Sigma F_bc)^dagger lambda_bc=0 | regular constraints set the selector data before readout | FORMAL_VARIATION_DERIVED_CONDITIONAL | regularity/full-rank proof for D_Sigma F_bc and zero-mode quotient | false |
| RSF2385_3_source_blindness | source-blind selector proof | D_source F_bc=0 and rank(D_Sigma F_bc)=full => D_source Sigma_ref=0 | connects relative boundary class construction to 2383 implicit selector theorem | CONDITIONAL_THEOREM_SHAPE | source-free proof for each F_bc component and full-rank certificate | false |
| RSF2385_4_norm_square_variant | norm-square selector action | S_sel=1/2 <F_bc,A F_bc> | positive form can prove uniqueness if A is source-free positive | RISKIER_VARIANT_RETAINED_ONLY_IF_PAIRING_SOURCE_FREE | A/pairing must not depend on source/readout metric data | false |
| RSF2385_5_verdict | current selector functional verdict | relative-class Lagrange selector | best available low-cheat path to make Sigma_ref parent-selected | CONTRACT_ADVANCED_NOT_PROMOTED | explicit parent-owned F_bc components, source-free pairing and rank proof | false |

## Component Gates

| row_id | constraint_component | needed_zero | current_status | failure_residual | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RCG2385_0_Crel | C_rel(Sigma_ref)-C_top | relative/topological class fixed before source/readout | C_TOP_CONTRACT_NOT_PARENT_SELECTED | epsilon_top_abs;Delta_ref_class_leak | false |
| RCG2385_1_exact_boundary | d_S B_ref-h_rel-r_rel | exact/proper boundary representative with harmonic/residual parts absent or bounded | B_REF_PRIMITIVE_NOT_PARENT_OWNED | B_zero_remainder;Delta_ref_functional_gap | false |
| RCG2385_2_corner | corner_lock | corner-free domain or included fixed corner charge | CORNER_CERTIFICATE_MISSING | epsilon_corner_abs | false |
| RCG2385_3_tau_frame | tau_lock and frame_lock | same tau/coframe for Q_tau, H_ref and M_H_ref | SAME_FRAME_LOCK_MISSING | epsilon_delta_tau_abs;M_H_ref non-score-ready | false |
| RCG2385_4_surface | S0_lock | source-independent linked surfaces and no retuning | SURFACE_NO_RETUNE_MISSING | Delta_ref_surface_component_over_MH | false |
| RCG2385_5_pairing | topological/source-free pairing <lambda,F> | no metric/source/readout stress from the selector action | PAIRING_SOURCE_FREE_CERTIFICATE_MISSING | selector_pairing_stress_leak | false |

## Delta Ref Value Rows

| row_id | quantity | formula | current_value | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DRV2385_0_class_leak | Delta_ref_class_leak_over_MH | abs(partial_source C_rel * K_class)/M_H_ref or theorem-zero via parent selected C_top | MISSING_CREL_SOURCE_DERIVATIVE;MISSING_K_CLASS;MISSING_M_H_REF | false | false |
| DRV2385_1_pairing_stress | selector_pairing_stress_leak_over_MH | abs(delta_metric <lambda,F_bc>_pairing)/M_H_ref | MISSING_PAIRING_METRIC_VARIATION;MISSING_M_H_REF | false | false |
| DRV2385_2_rank_leak | selector_rank_branch_leak_over_MH | norm(P_kernel D_source Sigma_ref)/M_H_ref | MISSING_RANK_CERTIFICATE;MISSING_KERNEL_PROJECTOR;MISSING_M_H_REF | false | false |
| DRV2385_3_total | Delta_ref_relative_selector_total_over_MH | absolute sum of class, primitive, corner, tau/frame, surface, pairing and rank leaks over M_H_ref | COMPONENTS_MISSING | false | false |

## Decision Ledger

| row_id | decision | reason | consequence | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC2385_0_best_functional | prefer Lagrange-multiplier relative-class selector over norm-square selector | it avoids smuggling a source/readout metric into the selector pairing unless the pairing is parent-proved source-free | S_sel=<lambda,F_bc> becomes the clean future parent-action contract | LOWER_SCRUTINY_SELECTOR_CONTRACT_SELECTED | false |
| DEC2385_1_no_promotion | do not promote selector functional theorem | F_bc components, pairing, rank/nondegeneracy and M_H_ref are not parent-owned | Delta_ref values remain missing/nonclaim | CONTRACT_NOT_PARENT_SIGNED | false |
| DEC2385_2_next | attack C_rel/C_top parent selection or fill values | the first concrete component is relative class selection; if that fails, no selector functional closes | 2386 should try to derive C_top superselection from parent topology/Ward data or source-pack class leak | SELECT_2386_CTOP_SUPERSELECTION | false |

## Claim Gates

| row_id | gate | gate_status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2385_0_selector_functional_shape | relative-class selector functional shape written | PASS_CONTRACT_ONLY | future parent action target | false |
| CG2385_1_Fbc_parent_owned | F_bc components parent-owned and source-free | FAIL | Sigma_ref not proved source-blind | false |
| CG2385_2_pairing_source_free | selector pairing/source measure source-free | FAIL_UNSIGNED | selector stress/source leak remains possible | false |
| CG2385_3_rank | regular/full-rank constraint map after quotient | FAIL | branch leak remains possible | false |
| CG2385_4_MHref | positive same-frame M_H_ref | FAIL | Delta_ref values remain non-score-ready | false |
| CG2385_5_local_GR_Newton | local GR/Newton recovery | FAIL_NONCLAIM | reference/source-measure/denominator gates remain open | false |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2385_0_contract_as_claim | treat S_sel=<lambda,F_bc> contract as current MTS proof | false | F_bc and pairing are not parent-owned in the active corpus | RSF2385_1_multiplier_action;CG2385_1_Fbc_parent_owned | false |
| REF2385_1_metric_norm_shortcut | use norm-square selector without proving source-free pairing | false | metric/Hodge pairing can reintroduce source/readout stress | RSF2385_4_norm_square_variant;RCG2385_5_pairing | false |
| REF2385_2_score_values | score Delta_ref values now | false | component values and M_H_ref are missing | DRV2385_0_class_leak;DRV2385_3_total;CG2385_4_MHref | false |

## Next Target

| row_id | next_file | success_condition | fallback_condition | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2385_0_selected | 2386-Y5-R2FR-Ctop-superselection-from-parent-topology-or-class-leak-row.md | derive parent-owned C_top/relative class superselection with D_source C_top=0 before readout | fill Delta_ref_class_leak_over_MH with finite source derivative, units, source path and valid_for_claim=false | false |
| NEXT2385_1_parallel | 2386b-Y5-R2FR-source-free-pairing-for-selector-or-pairing-stress-row.md | prove <lambda,F_bc> pairing is topological/source-free and has no metric/readout stress | retain selector_pairing_stress_leak row | false |
| NEXT2385_2_parallel | 2386c-Y5-R2FR-selector-rank-zero-mode-quotient-or-branch-leak-row.md | prove D_Sigma F_bc is full rank after quotienting gauge/topological zero modes | retain selector_rank_branch_leak row | false |

## Validation

| row_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL2385_00_sources_exist | PASS | all required source paths exist | false |
| VAL2385_01_needles_found | PASS | all source needles found | false |
| VAL2385_02_multiplier_functional_present | PASS | Lagrange-multiplier relative selector functional present | false |
| VAL2385_03_component_gates_present | PASS | Crel/exact-boundary/pairing component gates present | false |
| VAL2385_04_value_rows_nonready | PASS | Delta_ref value rows remain non-score-ready | false |
| VAL2385_05_global_claims_blocked | PASS | global/local gates remain blocked | false |
| VAL2385_06_csv_parse | PASS | generated CSVs parse and have rows | false |
| VAL2385_07_no_claim_flags | PASS | no generated row has valid_for_claim=true | false |
| VAL2385_08_formalization_untouched_by_script | PASS | script writes only post-checkpoint-work outputs | false |
| VAL2385_09_next_selected | PASS | C_top superselection selected next | false |
| VAL2385_OVERALL | PASS | 2385 constructs the lower-scrutiny relative-class Lagrange selector contract, refuses promotion without parent-owned Fbc/pairing/rank/MHref, and selects Ctop superselection next | false |

## Practical Status

This is a useful leap, not a close.  We now have a less fragile selector-action architecture: a relative-class
constraint action rather than a fitted reference or metric norm-square.  The first real component to attack is
`C_top` superselection.  If `C_top` cannot be parent-selected before readout, the whole selector branch must become a
source-pack branch.
