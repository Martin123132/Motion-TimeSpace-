# 1731 - Aext Surface Pair Support Certificate Or Boundary Flux Row

## Verdict
- 1731 tries to sign the full `A_ext` source-free certificate needed by the vacuum-annulus route.
- Current result: the certificate is **not signed**. `W_source`, `S1`, `S2`, `A_ext cap W_source`, same-frame/tau lock, and boundary-flux handoff are all still missing or conditional.
- Useful progress: the missing object is now split into two precise nonclaim ledgers: geometry/support rows and boundary/Hamiltonian handoff rows.
- This protects the good GR-like idea: exterior bulk `T_obs=0` is allowed only if source mass reappears through `H_tau/M_H_ref/PiM/boundary` data.
- No WEP, R10, PPN, clock, orbital, Newton, local-GR, fixed-`tau`, `M_H_ref`, `J_H_total`, `N_domain`, or source-normalization claim is made.

## Conditional Logic
The route is still alive: a source-free exterior annulus can kill the bulk `T_obs` contribution to `C_Tobs_tau`. But this does not by itself derive Newton/GR. The source mass must be carried by a parent-owned boundary or Hamiltonian charge. So the next bottleneck is not just drawing `S1` and `S2`; it is proving the boundary-flux handoff.

## Source Register
| source_id | source_key | source_path | exists | needles_present |
| --- | --- | --- | --- | --- |
| SRC1731_0_1730_doc | 1730_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1730-Y5-R2FR-Tobs-support-annulus-split-or-first-norm-source-row.md | True | True |
| SRC1731_1_1730_next | 1730_next_target | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1730_NEXT_TARGET.csv | True | True |
| SRC1731_2_1730_annulus_audit | 1730_annulus_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1730_ANNULUS_SUPPORT_AUDIT.csv | True | True |
| SRC1731_3_1730_norm_rows | 1730_norm_rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1730_TOBS_NORM_SOURCE_ROWS.csv | True | True |
| SRC1731_4_1724_annulus_owner | 1724_annulus_owner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1724_ANNULUS_NORM_TAU_OWNER_AUDIT.csv | True | True |
| SRC1731_5_1718_worldtube_audit | 1718_worldtube_support_owner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1718_WORLDTUBE_SUPPORT_OWNER_AUDIT.csv | True | True |
| SRC1731_6_1718_domain_contract | 1718_domain_numerator_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1718_ICOMMUTATOR_DOMAIN_NUMERATOR_BOUND_CONTRACT.csv | True | True |
| SRC1731_7_1359_intake | 1359_surface_intake | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1359_ICOMMUTATOR_SOURCE_INTAKE_LEDGER.csv | True | True |
| SRC1731_8_1360_surface_rows | 1360_surface_rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1360_MHREF_SURFACE_INTAKE_ROWS.csv | True | True |
| SRC1731_9_662_bound_template | 662_boundary_flux_template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_662_BOUND_INPUT_TEMPLATE.csv | True | True |
| SRC1731_10_1013_obstructions | 1013_flux_obstructions_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md | True | True |
| SRC1731_11_mass_current_contract | mass_current_Hamiltonian_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv | True | True |
| SRC1731_12_683_same_frame | 683_same_frame_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv | True | True |
| SRC1731_13_1730_validation | 1730_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1730_VALIDATION.csv | True | True |

## Aext Certificate Audit
| audit_id | certificate_clause | current_status | blocking_gap | certificate_signed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| AEX1731_0_parent_worldtube | parent-owned W_source | WORLDTUBE_SUPPORT_OWNER_NOT_PROVED | 1718 keeps parent action, same frame, tau lock, compactness and coupling descent unsigned | False | False |
| AEX1731_1_surface_inner | inner linked surface S1 | MISSING_INNER_SURFACE | 1359/1360 record MISSING_INNER_RADIUS_OR_SURFACE | False | False |
| AEX1731_2_surface_outer | outer linked surface S2 | MISSING_OUTER_SURFACE | 1359/1360 record MISSING_OUTER_RADIUS_OR_SURFACE | False | False |
| AEX1731_3_annulus_homology | A_ext compact annulus and homology | MISSING_ANNULUS_HOMOLOGY_SOURCE | 1360 lacks annulus_A, boundary_relation, S1/S2 homology and source-free proof | False | False |
| AEX1731_4_support_exclusion | A_ext cap W_source empty | SUPPORT_EXCLUSION_NOT_SOURCED | no local row proves A_ext cap W_source empty or handles distributional boundary stress | False | False |
| AEX1731_5_boundary_flux_handoff | boundary flux handoff | BOUNDARY_FLUX_HANDOFF_MISSING | 662, 1013 and Hamiltonian charge contracts keep M_H_ref, B_zero_flux, Delta_symp, R_glue and PiM chain map unfilled | False | False |
| AEX1731_6_same_frame_tau | same frame and tau lock | SAME_FRAME_TAU_LOCK_UNSIGNED | 683 final gate remains blocked and tau/source-normal lock is still not parent-signed | False | False |
| AEX1731_7_verdict | A_ext source-free certificate verdict | AEXT_SOURCE_FREE_CERTIFICATE_NOT_SIGNED | geometry/support and boundary-flux handoff both remain nonclaim ledgers | False | False |

## Geometry Support Rows
| row_id | quantity | current_status | missing_inputs | numeric_or_theorem_value | units | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AGS1731_0_W_source | W_source | GEOMETRY_SOURCE_ROW_TEMPLATE | MISSING_PARENT_ACTION;MISSING_PARENT_SIGNED_JH;MISSING_PARENT_SIGNED_TAU_OBS;MISSING_COMPACT_SUPPORT;MISSING_NO_READOUT_MASK | MISSING_W_SOURCE | worldtube_or_support_identifier_MISSING | False | False |
| AGS1731_1_S1_inner_surface | S1_or_r1 | GEOMETRY_SOURCE_ROW_TEMPLATE | MISSING_SYSTEM_ID;MISSING_INNER_SURFACE;MISSING_R1;MISSING_LINKS_W_SOURCE;MISSING_FIXED_BEFORE_READOUT;MISSING_SOURCE_PATH | MISSING_INNER_RADIUS_OR_SURFACE | length_or_surface_identifier_MISSING | False | False |
| AGS1731_2_S2_outer_surface | S2_or_r2 | GEOMETRY_SOURCE_ROW_TEMPLATE | MISSING_SYSTEM_ID;MISSING_OUTER_SURFACE;MISSING_R2;MISSING_HOMOLOGY_CLASS;MISSING_FIXED_BEFORE_READOUT;MISSING_SOURCE_PATH | MISSING_OUTER_RADIUS_OR_SURFACE | length_or_surface_identifier_MISSING | False | False |
| AGS1731_3_Aext_homology | A_ext_and_homology_class | GEOMETRY_SOURCE_ROW_TEMPLATE | MISSING_SYSTEM_ID;MISSING_ANNULUS_A;MISSING_BOUNDARY_RELATION;MISSING_S1_HOMOLOGY;MISSING_S2_HOMOLOGY;MISSING_SOURCE_FREE_CERTIFICATE;MISSING_ANNULUS_MEASURE | MISSING_ANNULUS_HOMOLOGY_SOURCE | topological_class_plus_domain_metadata_MISSING | False | False |
| AGS1731_4_support_exclusion | A_ext_cap_W_source_empty | SUPPORT_CERTIFICATE_ROW_TEMPLATE | MISSING_TOBS_SUPPORT;MISSING_A_EXT;MISSING_W_SOURCE;MISSING_REGULARITY_CLASS;MISSING_SURFACE_DISTRIBUTION_POLICY;MISSING_SOURCE_PATH | MISSING_SOURCE_FREE_CERTIFICATE | boolean_theorem_or_support_metadata_MISSING | False | False |

## Boundary Flux Handoff Rows
| row_id | quantity | current_status | missing_inputs | numeric_or_theorem_value | units | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BFH1731_0_M_H_ref | M_H_ref | BOUNDARY_HANDOFF_ROW_TEMPLATE | MISSING_TAU_ID;MISSING_SURFACE_OUTER;MISSING_Q_TAU_INTEGRAL;MISSING_G_REF;MISSING_H_REF;MISSING_M_H_REF;MISSING_UNITS | MISSING_M_H_REF | mass_or_energy_source_charge_MISSING | False | False |
| BFH1731_1_B_zero_flux | B_zero_flux | BOUNDARY_HANDOFF_ROW_TEMPLATE | MISSING_BOUNDARY_RULE;MISSING_B_ZERO_FLUX;MISSING_SURFACE_PAIR;MISSING_CORNER_TERMS;MISSING_M_H_REF;MISSING_SOURCE_PATH | MISSING_B_ZERO_FLUX | GM_flux_or_dimensionless_after_MHref_MISSING | False | False |
| BFH1731_2_Delta_symp | Delta_symp | BOUNDARY_HANDOFF_ROW_TEMPLATE | MISSING_SYMPLECTIC_CURRENT;MISSING_BOUNDARY_CONDITIONS;MISSING_INTEGRABILITY_CERTIFICATE;MISSING_M_H_REF;MISSING_UNITS | MISSING_DELTA_SYMP | dimensionless_after_MHref_MISSING | False | False |
| BFH1731_3_R_glue | R_glue | BOUNDARY_HANDOFF_ROW_TEMPLATE | MISSING_PIM_CHAIN_MAP;MISSING_J_H;MISSING_J_M_TOP;MISSING_B_ZERO;MISSING_SURFACE_PAIR;MISSING_M_H_REF | MISSING_R_GLUE | dimensionless_after_MHref_MISSING | False | False |
| BFH1731_4_PiM_chain_map | PiM_H_chain_map | BOUNDARY_HANDOFF_ROW_TEMPLATE | MISSING_PIM_DEFINITION;MISSING_Q_TAU;MISSING_SURFACE_PAIR;MISSING_ICOMMUTATOR_ZERO_OR_BOUND;MISSING_M_H_REF | MISSING_PIM_H_CHAIN_MAP | operator_or_charge_map_units_MISSING | False | False |
| BFH1731_5_handoff_acceptance | boundary_flux_handoff_acceptance | CLAIM_BLOCKED | MISSING_BOUNDARY_FLUX_HANDOFF_STACK | BLOCKED | dimensionless_gate | False | False |

## Theorem Attempt
| attempt_id | statement | current_status | current_blocker | would_close | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| AST1731_0_geometry_antecedent | If W_source is parent-owned, S1/S2 are fixed linked surfaces, and A_ext cap W_source is empty, the bulk annulus is source-free. | CONDITIONAL_THEOREM_SHAPE | geometry/source rows AGS1731_0 through AGS1731_4 are all missing or conditional | bulk T_obs zero antecedent | False |
| AST1731_1_bulk_Tobs_zero | If the geometry antecedent and same-frame ordinary T_obs definition are signed, T_obs\|A_ext=0 in the bulk. | CONDITIONAL_EFFECT_ONLY | same-frame T_obs/J_H and tau lock remain unsigned | bulk C_Tobs_tau zero | False |
| AST1731_2_boundary_handoff | Bulk T_obs zero is legal only when H_tau/M_H_ref/PiM/boundary flux rows carry the excluded mass information. | HANDOFF_NOT_FILLED | boundary flux rows BFH1731_0 through BFH1731_5 are nonclaim templates | mass preservation guard for vacuum exterior route | False |
| AST1731_3_current_verdict | Current MTS cannot yet claim A_ext source-free or bulk C_Tobs_tau=0. | FAIL_CURRENT_CLAIM | A_ext certificate and boundary-flux handoff are both unsigned | no local-GR promotion; retain finite/nonclaim Tobs norm path | False |

## Runner Refusal
| run_id | quantity | runner_decision | refusal_reasons | accepted_for_scoring | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| RUN1731_0_Aext_certificate | A_ext source-free certificate | REFUSE_CLAIM | MISSING_W_SOURCE;MISSING_S1;MISSING_S2;MISSING_AEXT_HOMOLOGY;MISSING_SUPPORT_EXCLUSION;MISSING_SAME_FRAME_TAU_LOCK | False | False |
| RUN1731_1_boundary_handoff | boundary flux handoff | ACCEPT_SCHEMA_REFUSE_SCORING | MISSING_M_H_REF;MISSING_B_ZERO_FLUX;MISSING_DELTA_SYMP;MISSING_R_GLUE;MISSING_PIM_CHAIN_MAP | False | False |
| RUN1731_2_C_Tobs_tau_zero | bulk C_Tobs_tau theorem-zero | BLOCKED_NO_CLAIM | AEXT_SOURCE_FREE_CERTIFICATE_NOT_SIGNED;BOUNDARY_FLUX_HANDOFF_MISSING | False | False |
| RUN1731_3_Newton_local_GR | Newton/local-GR reduction | BLOCKED_NO_CLAIM | NO_AEXT_CERTIFICATE;NO_BOUNDARY_HANDOFF;NO_MHREF;NO_SOURCE_NORMALIZATION;PPN_VECTOR_OPEN | False | False |

## Decision Ledger
| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DEC1731_0_certificate_status | do not sign A_ext source-free certificate | W_source, S1, S2, homology, support exclusion, same-frame tau and boundary flux are all unsigned | use geometry/support rows as the exact certificate checklist |
| DEC1731_1_boundary_handoff_priority | boundary flux handoff is the next derivation bottleneck | even if the exterior bulk is vacuum, GR recovers mass through a surface/Hamiltonian charge rather than local matter stress | derive or source M_H_ref, B_zero_flux, Delta_symp, R_glue and PiM_H_chain_map |
| DEC1731_2_geometry_parallel | keep S1/S2/A_ext geometry intake parallel | surface data are necessary, but without boundary handoff they can only prove empty exterior, not measured mass or local GR | parallel row can fill surface identifiers and support metadata without scoring |

## Next Target
| route_id | next_target | script | objective | selection_status |
| --- | --- | --- | --- | --- |
| NEXT1731_0_primary | 1732-Y5-R2FR-boundary-flux-handoff-to-Htau-or-MHref-source-row.md | scripts/Y5_R2FR_boundary_flux_handoff_to_Htau_or_MHref_source_row.py | derive the boundary/Hamiltonian handoff that carries source mass when bulk T_obs vanishes, or fill nonclaim M_H_ref/B_zero_flux/Delta_symp/R_glue/PiM rows | selected |
| NEXT1731_1_parallel_geometry_intake | 1732b-Y5-R2FR-Aext-geometry-support-intake-row.md | scripts/Y5_R2FR_Aext_geometry_support_intake_row.py | fill W_source, S1, S2, A_ext support-exclusion and homology metadata as nonclaim geometry rows | held_parallel |
| NEXT1731_2_later_CdeltaTau | 1733-Y5-R2FR-CdeltaTau-source-piece-stack-runner.md | scripts/Y5_R2FR_CdeltaTau_source_piece_stack_runner.py | combine Z_Tobs_Aext or sup_A_Tobs with C_Tobs_tau only after geometry and boundary handoff close | later |

## Claim Gates
| claim_id | claim | status | reason |
| --- | --- | --- | --- |
| CG1731_0_Aext_source_free | A_ext is parent-certified source-free | BLOCKED_NO_CLAIM | AEX1731_7 says the A_ext source-free certificate is not signed |
| CG1731_1_boundary_handoff | boundary/Hamiltonian handoff carries the excluded source mass | BLOCKED_NO_CLAIM | BFH1731 rows have missing M_H_ref, B_zero_flux, Delta_symp, R_glue and PiM chain map |
| CG1731_2_bulk_C_Tobs_zero | bulk C_Tobs_tau is theorem-zero | BLOCKED_NO_CLAIM | geometry and boundary handoff certificates are both missing |
| CG1731_3_Tobs_finite_source | sup_A \|\|T_obs\|\|_op finite row can score | BLOCKED_NO_CLAIM | A_ext geometry, norm units and stress bound remain unfilled |
| CG1731_4_Newton_local_GR | Newton/local-GR reduction is derived | BLOCKED_NO_CLAIM | no A_ext certificate, no boundary handoff, no source-normalization denominator, PPN vector open |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1731_0_sources_exist | PASS | all cited source paths exist |
| VAL1731_1_needles_present | PASS | required source needles are present |
| VAL1731_2_1730_handoff_preserved | PASS | 1730 selected Aext support/boundary handoff route |
| VAL1731_3_certificate_audit_complete | PASS | certificate audit covers worldtube, surfaces, annulus, support, boundary handoff, frame/tau and verdict |
| VAL1731_4_certificate_blocked | PASS | Aext source-free certificate remains unsigned |
| VAL1731_5_geometry_rows_nonclaim | PASS | geometry/support rows carry missing markers and remain nonclaim |
| VAL1731_6_boundary_rows_nonclaim | PASS | boundary flux handoff rows carry missing markers and remain nonclaim |
| VAL1731_7_theorem_fails_current_claim | PASS | theorem attempt explicitly fails current claim |
| VAL1731_8_runner_refusals_cover_chain | PASS | runner refusals cover Aext, handoff, C_Tobs and local-GR |
| VAL1731_9_decision_next | PASS | decision selects boundary handoff priority |
| VAL1731_10_next_selected | PASS | next target row selects 1732 primary route |
| VAL1731_11_claim_gates_blocked | PASS | claim gates remain blocked |
| VAL1731_12_csv_parse | PASS | all generated 1731 CSVs parse |
| VAL1731_13_no_claim_flags | PASS | all generated scoring and claim flags remain false |
| VAL1731_14_branch_copies | PASS | branch/quarantine/queue copies exist |
| VAL1731_15_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1731_16_formalization_untouched | PASS | no 1731 outputs found under formalization-workbench |
| VAL1731_OVERALL | PASS | 1731 Aext/boundary flux validation |

## Working Interpretation
1731 keeps the good route alive and blocks the bad shortcut. If we can derive the boundary/Hamiltonian handoff, then a vacuum exterior annulus becomes a strength rather than a loophole: no bulk matter stress outside the source, but a nonzero mass charge on the boundary. If we cannot derive it, `C_Tobs_tau` stays finite/nonclaim and local GR remains blocked. Next shot: derive or source the boundary handoff stack.
