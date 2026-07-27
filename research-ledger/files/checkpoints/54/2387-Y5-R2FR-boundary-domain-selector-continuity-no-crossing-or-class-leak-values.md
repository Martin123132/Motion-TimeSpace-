# 2387 - boundary-domain selector continuity no-crossing or class-leak values

## Result

2387 connects the `C_top` local-constancy route to the GR-like compact-source/worldtube route:

`W_source := closure(supp J_H[tau])`,

with linked surfaces `S_inner` and `S_outer` enclosing the same source and a source-free annulus between them.

If the parent action owns `J_H`, source support is compact, the linked surfaces are fixed before readout, and no source
support crosses the annulus along the allowed variation, then the linking/domain class is continuous and `C_top` cannot
jump.  That gives a conditional no-crossing route to `D_source C_top=0`.

But current MTS still lacks parent-owned `J_H`, compact support, linking/no-crossing/no-retune certificates, and
positive same-frame `M_H_ref`.  So this is not promoted.  The class/domain leak rows remain nonclaim.

No `C_top` pass, `Delta_ref=0`, Newton, local-GR, PPN, orbital, clock, R10, or public/GitHub claim is made.

## Source Register

| row_id | source_key | source_path | exists | needles_found | source_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2387_00_2386_doc | 2386_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2386-Y5-R2FR-Ctop-superselection-from-parent-topology-or-class-leak-row.md | true | true | 2386 selected domain/no-crossing as next gate | false |
| SRC2387_01_2386_certs | 2386_certs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2386_SELECTOR_CERTIFICATE_MATRIX.csv | true | true | domain/no-crossing certificate gaps | false |
| SRC2387_02_domain_parent_clause | domain_parent_clause | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv | true | true | older parent domain selector clause | false |
| SRC2387_03_668_boundary_lock | 668_boundary_lock | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_668_BOUNDARY_CONDITION_LOCK.csv | true | true | relative class and worldtube linking-surface lock | false |
| SRC2387_04_2183_doc | 2183_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2183-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R_eq-fill.md | true | true | worldtube/Hilbert selector and source-free annulus route | false |
| SRC2387_05_1016_doc | 1016_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md | true | true | parent worldtube/source-measure selector contract | false |
| SRC2387_06_61_doc | 61_bound_domain | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\61-bound-domain-boundary-theorem-attempt.md | true | true | domain selector not derived precedent | false |
| SRC2387_07_1760_doc | 1760_worldtube | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md | true | true | worldtube support owner open | false |

## Domain No-Crossing Theorem

| row_id | step | statement | condition | result | current_gap | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| DNC2387_0_worldtube_selector | parent worldtube selector | Define W_source := closure(supp J_H[tau]) before readout; admissible S_inner,S_outer link the same W_source. | parent action owns J_H, tau, compact support and same-frame source measure | domain is selected by Hilbert support rather than fitted radius/mass | J_H/worldtube owner remains unsigned | false |
| DNC2387_1_no_crossing | source-free annulus no-crossing | If A is the annulus with boundary S_outer-S_inner and A cap W_source is empty, source variations that keep supp(J_H) inside W_source do not change the linking class. | compact support, no source crossing S_inner/S_outer, fixed tau/frame and continuous source path | C_top is constant along that path | no-crossing and support-continuity certificate missing | false |
| DNC2387_2_domain_continuity | domain continuity | A continuous family of admissible domains in the same exterior homology class has no class jump unless support crosses the boundary or topology changes. | domain selector is continuous and does not retune surfaces after readout | D_source C_top=0 conditionally follows from domain continuity | parent continuity/no-retune rule missing | false |
| DNC2387_3_failure_modes | failure modes | If support crosses the annulus, surfaces are retuned, J_H is not parent-owned, or a topology-changing event occurs, class leak rows are required. | none | class leak is the honest fallback | finite class-leak values missing | false |
| DNC2387_4_verdict | current verdict | The domain/no-crossing theorem is sharp but conditional; current MTS does not parent-sign the worldtube/domain selector. | J_H ownership, support compactness, no-crossing and same-frame M_H_ref remain missing | do not promote C_top superselection; keep class leak rows nonclaim | parent worldtube selector and M_H_ref | false |

## Domain Certificate Matrix

| row_id | certificate | required_test | status | residual_if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DCC2387_0_JH | parent-owned Hilbert current J_H[tau] | J_H derived from parent matter variation before readout | MISSING_PARENT_JH_OWNER | worldtube_selector_leak | false |
| DCC2387_1_support | compact regular source support | W_source compact/regular and selected before source/readout | MISSING_COMPACT_SUPPORT_CERTIFICATE | support_tail_leak | false |
| DCC2387_2_linking_surfaces | linked homologous surfaces | S_inner and S_outer are homologous in the exterior and link the same W_source | MISSING_LINKING_SURFACE_CERTIFICATE | domain_linking_leak | false |
| DCC2387_3_no_crossing | no source crossing annulus | A cap W_source remains empty along the allowed source-variation path | MISSING_NO_CROSSING_CERTIFICATE | class_jump_leak | false |
| DCC2387_4_no_retune | no post-readout domain retune | domain/surface rule fixed before residual, GM, orbit or PPN readout | MISSING_NO_RETUNE_CERTIFICATE | domain_retune_leak | false |
| DCC2387_5_MHref | positive same-frame M_H_ref | finite positive denominator in same tau/frame as domain and C_top | MISSING_POSITIVE_MHREF | all class leak rows non-score-ready | false |

## Class Domain Leak Values

| row_id | quantity | formula | current_value | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DLV2387_0_worldtube_selector | epsilon_W_selector_class | abs(Delta C_top_from_W_selector * K_class)/M_H_ref | MISSING_WORLDTUBE_SELECTOR_DELTA;MISSING_K_CLASS;MISSING_M_H_REF | false | false |
| DLV2387_1_crossing | epsilon_crossing_class | abs(Delta C_top_crossing * K_crossing)/M_H_ref | MISSING_CROSSING_EVENT_SCALE;MISSING_K_CROSSING;MISSING_M_H_REF | false | false |
| DLV2387_2_retune | epsilon_domain_retune | abs(partial_readout C_top * readout_retune_scale)/M_H_ref | MISSING_RETUNE_DERIVATIVE;MISSING_RETUNE_SCALE;MISSING_M_H_REF | false | false |
| DLV2387_3_total | Delta_ref_class_domain_total_over_MH | absolute sum of worldtube selector, crossing, topology-change and retune leaks over M_H_ref | COMPONENTS_MISSING | false | false |

## Decision Ledger

| row_id | decision | reason | consequence | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC2387_0_conditional_gain | accept no-crossing domain theorem as conditional route | a parent-owned Hilbert worldtube and source-free annulus make the relative class locally constant | C_top zero route is tied to worldtube/Hilbert selector, not arbitrary topology words | CONDITIONAL_DOMAIN_THEOREM_ACCEPTED | false |
| DEC2387_1_no_promotion | do not promote domain/no-crossing theorem | parent-owned J_H, compact support, linking surfaces, no-crossing, no-retune and M_H_ref remain missing | class leak values remain nonclaim | DOMAIN_SELECTOR_NOT_PARENT_SIGNED | false |
| DEC2387_2_next | attack parent-owned J_H/worldtube support or fill values | without J_H ownership, W_source is a label not a derived selector | 2388 should try to derive parent Hilbert current/worldtube support or source-pack selector leak values | SELECT_2388_PARENT_JH_WORLDTUBE | false |

## Claim Gates

| row_id | gate | gate_status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2387_0_no_crossing_shape | domain no-crossing theorem shape | PASS_CONDITIONAL_THEOREM_ONLY | future route for C_top continuity | false |
| CG2387_1_parent_JH | parent-owned Hilbert current/worldtube selector | FAIL | W_source not claim-grade | false |
| CG2387_2_no_crossing | no source crossing linked annulus | FAIL | class jump leak remains | false |
| CG2387_3_no_retune | domain/surface rule fixed before readout | FAIL_UNSIGNED | retune leak remains | false |
| CG2387_4_MHref | positive same-frame M_H_ref | FAIL | domain leak rows non-score-ready | false |
| CG2387_5_local_GR_Newton | local GR/Newton recovery | FAIL_NONCLAIM | domain/source/reference gates remain open | false |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2387_0_pick_domain | choose source domain after readout and call C_top fixed | false | domain must be selected by parent J_H/support before residual or orbital data | DCC2387_0_JH;DCC2387_4_no_retune | false |
| REF2387_1_ignore_crossing | ignore source crossing/topology-change events | false | class local constancy only holds within one admissible no-crossing component | DNC2387_3_failure_modes;DCC2387_3_no_crossing | false |
| REF2387_2_score_leaks | score class/domain leak rows now | false | component values and M_H_ref are missing | DLV2387_0_worldtube_selector;DLV2387_3_total;CG2387_4_MHref | false |

## Next Target

| row_id | next_file | success_condition | fallback_condition | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2387_0_selected | 2388-Y5-R2FR-parent-Hilbert-current-worldtube-support-or-selector-leak-values.md | derive parent-owned J_H[tau] and W_source=closure(supp J_H[tau]) with compact support before readout | fill epsilon_W_selector_class and crossing/retune class leak values with units/source paths and valid_for_claim=false | false |
| NEXT2387_1_parallel | 2388b-Y5-R2FR-source-free-pairing-for-selector-or-pairing-stress-row.md | prove selector pairing is topological/source-free and has no metric/readout stress | retain selector_pairing_stress_leak row | false |
| NEXT2387_2_parallel | 2388c-Y5-R2FR-MHref-sidecar-or-normalized-residual-stays-unscored.md | derive positive same-frame M_H_ref | keep normalized rows non-score-ready | false |

## Validation

| row_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL2387_00_sources_exist | PASS | all required source paths exist | false |
| VAL2387_01_needles_found | PASS | all source needles found | false |
| VAL2387_02_no_crossing_theorem_present | PASS | no-crossing theorem row present | false |
| VAL2387_03_certificates_missing_explicit | PASS | JH/support/linking/no-crossing/no-retune/MHref gaps explicit | false |
| VAL2387_04_value_rows_nonready | PASS | class/domain leak rows remain non-score-ready | false |
| VAL2387_05_global_claims_blocked | PASS | global/local gates remain blocked | false |
| VAL2387_06_csv_parse | PASS | generated CSVs parse and have rows | false |
| VAL2387_07_no_claim_flags | PASS | no generated row has valid_for_claim=true | false |
| VAL2387_08_formalization_untouched_by_script | PASS | script writes only post-checkpoint-work outputs | false |
| VAL2387_09_next_selected | PASS | parent Hilbert current/worldtube support selected next | false |
| VAL2387_OVERALL | PASS | 2387 derives conditional domain/no-crossing route, refuses promotion without parent JH/worldtube/support/MHref, and selects parent Hilbert current next | false |

## Practical Status

The no-crossing route is a serious bridge toward GR/Newton source normalization because it uses a parent Hilbert
worldtube rather than an arbitrary boundary.  But the next missing object is now unavoidable: parent-owned `J_H[tau]`
and `W_source`.  Without that, the domain is still a label and not a theorem.
