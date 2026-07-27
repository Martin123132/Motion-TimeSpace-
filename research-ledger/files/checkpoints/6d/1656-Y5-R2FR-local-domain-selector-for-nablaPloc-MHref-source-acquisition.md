# 1656 - Local Domain Selector For nablaPloc MHref Source Acquisition

**Private status:** nonclaim domain-selection checkpoint. No local domain theorem, `nabla_Ploc` bound, `M_H_ref`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

`1656` selects the first acquisition domain, not a proof domain:

```text
selected domain: lab_R10_compact_fermi_tube
||nabla P_loc|| <= C_Fermi L_D ||Riemann|| + C_Fermi2 L_D^2 ||nabla Riemann|| + non-geodesic lab terms
M_H_ref = H_tau[S_outer] - H_ref
```

The lab/R10 compact Fermi tube is selected because it is the cleanest finite local arena for the first `nabla_Ploc` source row and avoids using orbital `GM` as the first denominator. Solar-system PPN is deferred because it is too easy to smuggle orbital calibration into `M_H_ref`; clocks/WEP are deferred because readout/species responses add extra coupling coefficients first.

This is not a pass. The selected domain still lacks `L_D`, curvature norms, frame/acceleration terms, source profile, and the same-frame Hamiltonian denominator. It is just the first disciplined ring to fight in.

## Source Register

| source_id | path | path_exists | needles_found | role |
| --- | --- | --- | --- | --- |
| 1655_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1655-Y5-R2FR-nablaPloc-Icommutator-bound-row-or-MHref-denominator-fill.md | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| 1655_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1655_VALIDATION.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| 1655_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1655_NEXT_TARGET.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| 1655_readiness | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1655_BOUND_ROW_READINESS_MATRIX.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| 1655_nablaploc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1655_NABLAPLOC_CANDIDATE_ROW.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| 1655_mhref | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1655_MHREF_DENOMINATOR_CANDIDATE_ROW.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| 1655_acquisition | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1655_ACQUISITION_QUEUE.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| domain_scope_874 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_874_DOMAIN_SCOPE_AUDIT.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| readout_tests_893 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_893_READOUT_DOMAIN_TESTS.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| readout_cert_969 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_969_READOUT_DOMAIN_CERTIFICATE.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| einstein_classifier_1195 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1195_EINSTEIN_DOMAIN_CLASSIFIER.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| fermi_domain_1209 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1209_FERMI_DOMAIN_DERIVATION.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| domain_motion_1209 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1209_DOMAIN_MOTION_PROJECTOR_STRESS_AUDIT.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| typed_domain_1235 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1235_TYPED_DOMAIN_REQUIREMENTS.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| support_1547 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1547_SUPPORT_DOMAIN_CONVENTIONS.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| nablaploc_row_1208 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1208_SOURCE_READY_NABLAPLOC_ROW.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| mhref_gate_1652 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1652_MHREF_FIRST_ROW_GATE.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| queue_1655_acquisition | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR1655_ACQUISITION_QUEUE_NONCLAIM.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |
| queue_1655_nablaploc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR1655_NABLAPLOC_CANDIDATE_ROW_NONCLAIM.csv | True | True | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition |

## Intake Scan

| scan_id | folder_role | folder_path | csv_count | status |
| --- | --- | --- | --- | --- |
| SCAN1656_0_raw | raw_live_candidate_folder | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\raw | 0 | NO_RAW_LIVE_ROWS |
| SCAN1656_1_accepted | accepted_live_candidate_folder | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\accepted | 0 | NO_ACCEPTED_LIVE_ROWS |
| SCAN1656_2_queue | nonclaim_acquisition_queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue | 102 | QUEUE_PRESENT_NONCLAIM |

## Domain Candidate Selector

| domain_id | physical_domain | selection | reason | blockers |
| --- | --- | --- | --- | --- |
| DOM1656_0_lab_R10 | compact lab/R10 finite-range source-test domain | SELECT_FOR_ACQUISITION | finite local tube, direct short-range arena, independent apparatus geometry, no orbital GM needed for first acquisition template | MISSING_SOURCE_PROFILE;MISSING_FERMI_DOMAIN;MISSING_CURVATURE_NORMS;MISSING_MHREF_DENOMINATOR |
| DOM1656_1_solar_system_PPN | solar-system weak-field exterior domain | DEFER | excellent PPN relevance but source mass is easily contaminated by orbital-GM calibration | NO_ORBITAL_GM_IMPORT;MISSING_PARENT_MHREF;MISSING_DOMAIN_BOUNDARY_LOCK |
| DOM1656_2_clock_WEP | local clock/material-species domain | DEFER | good readout/coupling relevance but species response introduces extra matter/EM coefficients before projector row is filled | MISSING_READOUT_RESPONSE;MISSING_SPECIES_CHARGE;MISSING_PARENT_DOMAIN |
| DOM1656_3_orbital_sources | orbital/binary source-normalization domain | REJECT_FOR_FIRST_ROW | too close to forbidden orbital-GM denominator shortcut | NO_ORBITAL_GM_IMPORT |

## Selected Domain Requirements

| requirement_id | field | selected_requirement | why_needed | status |
| --- | --- | --- | --- | --- |
| LDR1656_0_domain_id | domain_id | lab_R10_compact_fermi_tube | fixed label for first local finite-domain acquisition | CHOSEN_TEMPLATE_LABEL |
| LDR1656_1_physical_system | physical_system | short-range laboratory source/test apparatus exterior tube | matches R10/local finite-source arena without orbital-GM import | SOURCE_DETAILS_MISSING |
| LDR1656_2_LD | L_D | MISSING_VALUE_METERS | tube radius/diameter scale entering finite-domain Fermi bound | MISSING_NUMERIC_SOURCE |
| LDR1656_3_boundary_rule | boundary_rule | compact tube with source support excised and fixed support weight | needed to keep boundary/domain motion explicit | MISSING_PARENT_OR_APPARATUS_SOURCE |
| LDR1656_4_curvature | Riemann_norm;nabla_Riemann_norm | MISSING_VALUES_IN_m^-2_AND_m^-3 | fills nabla_Ploc Fermi-curvature row | MISSING_CURVATURE_SOURCE |
| LDR1656_5_frame | central_worldline;transport_rule | free-fall/Fermi-Walker idealization or non-geodesic lab correction | decides whether acceleration/rotation terms enter | MISSING_FRAME_SOURCE |
| LDR1656_6_mhref | M_H_ref | MISSING_HAMILTONIAN_DENOMINATOR | normalizes projector/source leakage without orbital GM | MISSING_HTAU_HREF_PARENT_ROW |

## Unit Convention

| unit_id | quantity | unit | role | status |
| --- | --- | --- | --- | --- |
| UNIT1656_0_length | L_D | meter | SI length for local tube size | numeric value required |
| UNIT1656_1_curvature | Riemann_norm | meter^-2 | curvature norm in local domain | numeric value required |
| UNIT1656_2_curvature_derivative | nabla_Riemann_norm | meter^-3 | first curvature derivative norm | numeric value required |
| UNIT1656_3_projector_gradient | nabla_Ploc_Linf | meter^-1 | finite-domain projector drift bound | computed only after lower inputs |
| UNIT1656_4_mass_denominator | M_H_ref | kg or J/c^2 with explicit conversion | same-frame Hamiltonian source mass denominator | must not be orbital GM |
| UNIT1656_5_joined_bound | B_obs_projector_source_over_MH | dimensionless | all local source/projector residuals normalized by M_H_ref | requires no-cancellation components |

## nablaPloc Source Template

| row_id | domain_id | formula | L_D_m | Riemann_norm_m2 | nabla_Riemann_norm_m3 | current_status |
| --- | --- | --- | --- | --- | --- | --- |
| NPLT1656_0_lab_R10_fermi_candidate | lab_R10_compact_fermi_tube | nabla_Ploc_Linf <= C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm + non_geodesic_terms | MISSING | MISSING | MISSING | DOMAIN_SELECTED_VALUES_MISSING |

## MHref Source Template

| row_id | domain_id | definition | allowed_source_mass_proxy | forbidden_source_mass_proxy | current_status |
| --- | --- | --- | --- | --- | --- |
| MHRT1656_0_lab_R10_same_frame_candidate | lab_R10_compact_fermi_tube | M_H_ref = H_tau[S_outer] - H_ref | ordinary apparatus/source mass may be recorded only as an input to be matched to H_tau, not as proof of M_H_ref | orbital GM or post-fit Newtonian source mass | DENOMINATOR_DOMAIN_SELECTED_VALUES_MISSING |

## Refusal Runner

| run_id | quantity | runner_decision | reason |
| --- | --- | --- | --- |
| RUN1656_0_domain_selection | lab_R10 compact Fermi tube | SELECTED_FOR_ACQUISITION_NOT_CLAIM | domain chosen only as first source-row target; no parent domain theorem |
| RUN1656_1_nabla_Ploc | nabla_Ploc_Linf row | REFUSE_SCORING | MISSING_LD;MISSING_CURVATURE_NORMS;MISSING_CONSTANTS;MISSING_SOURCE_PATH |
| RUN1656_2_MHref | M_H_ref denominator row | REFUSE_SCORING | MISSING_HTAU;MISSING_HREF;MISSING_REFERENCE_RULE;MISSING_PARENT_CURRENT;NO_ORBITAL_GM_IMPORT |
| RUN1656_3_joined_local | local_GR_Newton_PPN_R10_WEP | REFUSE_SCORING | DOMAIN_SELECTED_ONLY;NABLAPLOC_VALUES_MISSING;MHREF_MISSING;NO_LOCAL_CLAIM |

## Claim Gates

| gate_id | claim | gate_pass | status | blocker |
| --- | --- | --- | --- | --- |
| CG1656_0_domain | lab_R10 compact Fermi tube is selected for acquisition | INTERNAL_SELECTION_ONLY | NONCLAIM | selection is not a domain theorem |
| CG1656_1_nabla_Ploc | nabla_Ploc bound row is source-backed | False | BLOCKED | values and source path missing |
| CG1656_2_MHref | M_H_ref denominator is source-backed | False | BLOCKED | Hamiltonian charge/reference row missing |
| CG1656_3_local_GR | local GR/Newton/PPN/R10/WEP follows from 1656 | False | NO_CLAIM | 1656 chooses an acquisition domain only |

## Decisions

| decision_id | decision | reason | next_action |
| --- | --- | --- | --- |
| DEC1656_0_select_lab_R10 | SELECT_LAB_R10_COMPACT_FERMI_TUBE_FOR_ACQUISITION | it is the cleanest finite local domain for the first nabla_Ploc source row and avoids orbital-GM as first denominator input | build a lab_R10 source pack for L_D, curvature norms, frame terms, and M_H_ref requirements |
| DEC1656_1_defer_solar | DEFER_SOLAR_SYSTEM_PPN_DOMAIN | high value but too easy to contaminate the denominator with orbital GM | return after M_H_ref discipline is source-backed |
| DEC1656_2_unit_convention | USE_SI_LENGTH_AND_MASS_WITH_DIMENSIONLESS_JOINED_BOUND | keeps nabla_Ploc in m^-1 and normalized leakage dimensionless | future data rows must declare conversions and no-cancellation normalization |
| DEC1656_3_next | NEXT_1657_LAB_R10_SOURCE_PACK | selected domain now needs actual sourced lower inputs | create lab_R10 finite-domain source pack for L_D/curvature/frame/M_H_ref |

## Next Target

| next_target | script | objective | success_condition |
| --- | --- | --- | --- |
| 1657-Y5-R2FR-lab-R10-nablaPloc-MHref-source-pack.md | scripts/Y5_R2FR_lab_R10_nablaPloc_MHref_source_pack.py | build the lab_R10 source pack for L_D, curvature norms, frame terms, projector constants, and same-frame M_H_ref requirements; no scoring unless real source-backed rows exist | either a lab_R10 source row gets numeric source-backed fields without orbital-GM import, or every field remains explicit MISSING_* with valid_for_claim=false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1656_0_sources_exist | PASS | all cited 1656 source paths exist and needles are present |
| VAL1656_1_intake_scanned | PASS | raw and accepted live source folders are scanned |
| VAL1656_2_domain_selected | PASS | lab_R10 compact Fermi tube selected for acquisition |
| VAL1656_3_selected_requirements_complete | PASS | selected domain requirements include geometry and M_H_ref fields |
| VAL1656_4_unit_convention_complete | PASS | unit convention fixes nabla_Ploc and normalized bound units |
| VAL1656_5_templates_nonclaim | PASS | source templates are selected but remain value-missing |
| VAL1656_6_refusal_runner_blocks | PASS | refusal runner blocks scoring |
| VAL1656_7_claim_gates_safe | PASS | all claim gates keep MTS claims false |
| VAL1656_8_next_target_selected | PASS | next target selects lab_R10 source pack |
| VAL1656_9_csv_parse | PASS | all generated 1656 CSVs parse |
| VAL1656_10_no_mts_claim_flags | PASS | all 1656 generated rows keep MTS claim/no-score flags false |
| VAL1656_11_branch_copies | PASS | branch/quarantine copies exist |
| VAL1656_12_queue_copies | PASS | acquisition queue nonclaim copies exist |
| VAL1656_13_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1656_14_formalization_untouched | PASS | no 1656 outputs found under formalization-workbench |
| VAL1656_OVERALL | PASS | 1656 local domain selector for nabla_Ploc/M_H_ref source acquisition validation |

## Working Interpretation

The local branch now has a concrete first empirical target: a lab/R10 compact Fermi tube source pack. If that pack can source `L_D`, curvature/frame terms, and a noncircular `M_H_ref`, we can finally start testing whether the projector leakage is small rather than merely assumed zero.
