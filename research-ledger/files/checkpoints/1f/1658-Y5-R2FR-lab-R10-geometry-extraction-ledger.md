# 1658 - lab R10 Geometry Extraction Ledger

**Private status:** nonclaim geometry extraction checkpoint. No `L_D`, `nabla_Ploc` numeric bound, `M_H_ref`, R10 pass, local-GR pass, Newton pass, PPN pass, WEP pass, or public claim is made.

## Verdict

`1658` extracts actual geometry fields from the cached arXiv primary text:

```text
detector-attractor separation range: 52 µm to 3.0 mm
hole-pattern diameter: 52 mm
detector/attractor thicknesses: 54 µm and 99 µm
isolation foil thickness: 10 µm
```

But it refuses the tempting shortcut: none of those fields is automatically the finite-domain `L_D` in the Fermi projector bound. The separation range is a source-backed scale hint; the hole-pattern radius is an apparatus extent; the test-body thicknesses are material geometry; the foil is a boundary component. A rule mapping extracted apparatus geometry to the compact Fermi tube radius is still missing.

## Source Register

| source_id | path | path_exists | needles_found | role |
| --- | --- | --- | --- | --- |
| 1657_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1657-Y5-R2FR-lab-R10-nablaPloc-MHref-source-pack.md | True | True | 1658 lab_R10 geometry extraction ledger |
| 1657_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1657_VALIDATION.csv | True | True | 1658 lab_R10 geometry extraction ledger |
| 1657_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1657_NEXT_TARGET.csv | True | True | 1658 lab_R10 geometry extraction ledger |
| 1657_web | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1657_WEB_SOURCE_REGISTER.csv | True | True | 1658 lab_R10 geometry extraction ledger |
| 1657_source_pack | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1657_LAB_R10_SOURCE_PACK.csv | True | True | 1658 lab_R10 geometry extraction ledger |
| 1657_nablaploc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1657_NABLAPLOC_SOURCE_ROW_CANDIDATE.csv | True | True | 1658 lab_R10 geometry extraction ledger |
| 1657_mhref | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1657_MHREF_SOURCE_ROW_CANDIDATE.csv | True | True | 1658 lab_R10 geometry extraction ledger |
| primary_pdf | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\lab-r10\Lee_Adelberger_2020_arXiv_2002_11761.pdf | True | True | 1658 lab_R10 geometry extraction ledger |
| primary_text | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\lab-r10\Lee_Adelberger_2020_arXiv_2002_11761.txt | True | True | 1658 lab_R10 geometry extraction ledger |

## Web Source Register

| web_id | url | role | status |
| --- | --- | --- | --- |
| WEB1658_0_arxiv_abs | https://arxiv.org/abs/2002.11761 | primary abstract page with detector-attractor separation range and arXiv identity | PRIMARY_PROVENANCE |
| WEB1658_1_arxiv_pdf | https://arxiv.org/pdf/2002.11761 | primary PDF cached locally for geometry extraction | PRIMARY_PDF_CACHED |
| WEB1658_2_aps_doi | https://link.aps.org/doi/10.1103/PhysRevLett.124.101101 | journal DOI landing page | JOURNAL_PROVENANCE |

## Intake Scan

| scan_id | folder_role | folder_path | csv_count | status |
| --- | --- | --- | --- | --- |
| SCAN1658_0_raw | raw_live_candidate_folder | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\raw | 0 | NO_RAW_LIVE_ROWS |
| SCAN1658_1_accepted | accepted_live_candidate_folder | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\accepted | 0 | NO_ACCEPTED_LIVE_ROWS |
| SCAN1658_2_queue | nonclaim_acquisition_queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue | 112 | QUEUE_PRESENT_NONCLAIM |

## Geometry Extraction Ledger

| geometry_id | field | extracted_value | si_value_or_range | units | source_line | extraction_status | use_as_LD |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GEO1658_0_separation_range | detector_attractor_separation_s | 52 µm to 3.0 mm | 5.2e-5 to 3.0e-3 | m | 10 | SOURCE_BACKED_SCALE_HINT_NOT_LD | False |
| GEO1658_1_separation_definition | s_definition | s is separation between facing detector/attractor surfaces | not_numeric | definition | 46 | SOURCE_BACKED_DEFINITION | False |
| GEO1658_2_hole_pattern_diameter | hole_pattern_diameter | 52 mm | 5.2e-2 | m | 65 | SOURCE_BACKED_APPARATUS_SCALE_NOT_LD | False |
| GEO1658_3_azimuthal_symmetry | test_body_symmetries | 18-fold and 120-fold | not_numeric | dimensionless | 8 | SOURCE_BACKED_GEOMETRY_STRUCTURE | False |
| GEO1658_4_test_body_thicknesses | detector_attractor_thickness | 54 µm and 99 µm | 5.4e-5 and 9.9e-5 | m | -1 | SOURCE_BACKED_MATERIAL_THICKNESS_NOT_LD | False |
| GEO1658_5_isolation_foil | isolation_foil_thickness | 10 µm | 1.0e-5 | m | 202 | SOURCE_BACKED_BOUNDARY_COMPONENT_NOT_DOMAIN_RULE | False |
| GEO1658_6_calibration_geometry | calibration_sphere_geometry | 1.137 kg external spheres; 0.4816 g detector spheres; 16.48 mm and 19.05 cm radius circles | mixed | mixed | 138 | SOURCE_BACKED_CALIBRATION_NOT_MHREF | False |
| GEO1658_7_centering_offsets | x0_y0_centering | x0=(-102±2)µm; y0=(-2121±2)µm | mixed | m | 239 | SOURCE_BACKED_ALIGNMENT_NOT_DOMAIN_RULE | False |
| GEO1658_8_geometry_verdict | L_D_extraction_verdict | no extracted field is accepted as L_D | MISSING_LD_RULE | not_applicable | -1 | BLOCKED_BY_LD_SELECTION_RULE | False |

## L_D Candidate Gate

| gate_id | candidate | decision | reason |
| --- | --- | --- | --- |
| LDG1658_0_min_separation | 52 µm minimum separation | REJECT_AS_LD | separation floor is not support radius/tube size |
| LDG1658_1_max_separation | 3.0 mm maximum separation | REJECT_AS_LD | measurement scan range is not domain radius |
| LDG1658_2_pattern_radius | 26 mm inferred pattern radius from 52 mm diameter | REJECT_AS_LD_PENDING_RULE | apparatus extent needs a domain/support rule before becoming L_D |
| LDG1658_3_test_body_thickness | 54/99 µm material thickness | REJECT_AS_LD_PENDING_RULE | thickness is not the compact exterior tube radius |
| LDG1658_4_foil_thickness | 10 µm isolation foil | REJECT_AS_LD | shield thickness is a boundary component, not L_D |
| LDG1658_5_selection_verdict | accepted L_D | NOT_SELECTED | no noncircular mapping rule from extracted geometry to L_D exists yet |

## nablaPloc Geometry Template

| row_id | source_test_separation_range_m | hole_pattern_radius_m | detector_thickness_m | attractor_thickness_m | selected_L_D_m | current_status |
| --- | --- | --- | --- | --- | --- | --- |
| NPLG1658_0_geometry_backed_template | 5.2e-5_to_3.0e-3 | 2.6e-2 | 5.4e-5 | 9.9e-5 | MISSING_LD_SELECTION_RULE | GEOMETRY_EXTRACTED_LD_NOT_SELECTED |

## MHref Geometry Ledger

| row_id | extracted_or_needed | status | blocker |
| --- | --- | --- | --- |
| MHRG1658_0_calibration_spheres | calibration sphere masses and circle radii are source-backed | SOURCE_BACKED_CALIBRATION_ONLY | calibration masses/geometry cannot be substituted for H_tau-H_ref |
| MHRG1658_1_science_test_bodies | platinum test-body thicknesses are source-backed | SOURCE_BACKED_GEOMETRY_ONLY | test-body material geometry is not the Hamiltonian source denominator |
| MHRG1658_2_mhref_verdict | M_H_ref remains missing | MISSING_HAMILTONIAN_DENOMINATOR | no H_tau/H_ref/reference rule extracted from geometry paper |

## Refusal Runner

| run_id | quantity | runner_decision | reason |
| --- | --- | --- | --- |
| RUN1658_0_geometry | lab_R10 geometry extraction | PARTIAL_PASS_NONCLAIM | separation range, pattern diameter, thicknesses, shield thickness, and calibration geometry extracted |
| RUN1658_1_LD | L_D selection | REFUSE_SCORING | no rule maps extracted apparatus geometry to finite Fermi tube radius |
| RUN1658_2_nabla_Ploc | nabla_Ploc numeric row | REFUSE_SCORING | L_D, curvature norms, constants, and frame terms remain missing |
| RUN1658_3_MHref | M_H_ref row | REFUSE_SCORING | geometry paper does not supply H_tau-H_ref denominator |
| RUN1658_4_local | local_GR_Newton_PPN_R10_WEP | REFUSE_SCORING | geometry extraction is nonclaim and no normalized local residual bound exists |

## Claim Gates

| gate_id | claim | gate_pass | status | blocker |
| --- | --- | --- | --- | --- |
| CG1658_0_geometry | lab/R10 geometry fields are extracted | PARTIAL_INTERNAL_ONLY | NONCLAIM | several fields are source-backed but not score-ready |
| CG1658_1_LD | L_D is selected | False | BLOCKED | mapping rule missing |
| CG1658_2_nabla | nabla_Ploc numeric/source row is accepted | False | BLOCKED | L_D and curvature inputs missing |
| CG1658_3_MHref | M_H_ref is accepted | False | BLOCKED | H_tau/H_ref missing |
| CG1658_4_local | local GR/Newton/PPN/R10/WEP follows | False | NO_CLAIM | geometry extraction does not imply theory reduction |

## Decisions

| decision_id | decision | reason | next_action |
| --- | --- | --- | --- |
| DEC1658_0_geometry | GEOMETRY_PARTIALLY_EXTRACTED | primary arXiv text supports separation range, pattern diameter, thicknesses, shield thickness, and calibration geometry | keep extracted fields as source-backed but nonclaim |
| DEC1658_1_LD | LD_NOT_SELECTED | no field is automatically the finite Fermi tube/support radius | derive or choose a conservative L_D mapping rule next |
| DEC1658_2_MHref | MHREF_NOT_FILLED_BY_GEOMETRY | calibration/test masses do not supply H_tau-H_ref | keep denominator acquisition separate |
| DEC1658_3_next | NEXT_1659_LD_RULE_OR_CONSERVATIVE_BOUND | nabla_Ploc cannot compute until L_D rule is declared | build L_D mapping-rule gate from extracted geometry |

## Next Target

| next_target | script | objective | success_condition |
| --- | --- | --- | --- |
| 1659-Y5-R2FR-LD-mapping-rule-or-conservative-geometry-bound.md | scripts/Y5_R2FR_LD_mapping_rule_or_conservative_geometry_bound.py | derive or choose a conservative rule mapping extracted lab_R10 geometry to L_D for the finite-domain nabla_Ploc bound, or refuse L_D with exact blockers | L_D rule is source/method-backed and noncircular, or L_D remains unselected and all scoring stays blocked |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1658_0_sources_exist | PASS | all cited 1658 source paths exist and needles are present |
| VAL1658_1_web_sources_recorded | PASS | web sources recorded as provenance/nonclaim |
| VAL1658_2_intake_scanned | PASS | raw and accepted live source folders are scanned |
| VAL1658_3_geometry_extracted | PASS | primary text backs extracted geometry rows |
| VAL1658_4_ld_not_selected | PASS | L_D is not selected by shortcut |
| VAL1658_5_nabla_template_blocked | PASS | nabla_Ploc template remains blocked by L_D rule |
| VAL1658_6_mhref_blocked | PASS | M_H_ref remains blocked |
| VAL1658_7_refusal_runner_blocks | PASS | refusal runner blocks scoring |
| VAL1658_8_claim_gates_safe | PASS | all claim gates keep MTS claims false |
| VAL1658_9_next_target_selected | PASS | next target selects L_D mapping rule |
| VAL1658_10_csv_parse | PASS | all generated 1658 CSVs parse |
| VAL1658_11_no_mts_claim_flags | PASS | all 1658 generated rows keep MTS claim/no-score flags false |
| VAL1658_12_branch_copies | PASS | branch/quarantine copies exist |
| VAL1658_13_queue_copies | PASS | acquisition queue nonclaim copies exist |
| VAL1658_14_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1658_15_formalization_untouched | PASS | no 1658 outputs found under formalization-workbench |
| VAL1658_OVERALL | PASS | 1658 lab_R10 geometry extraction ledger validation |

## Working Interpretation

We now have source-backed lab/R10 geometry, but not a domain radius. That is still progress: the next mathematical question is no longer vague source acquisition; it is whether MTS can define a conservative, noncircular `L_D` mapping rule from the extracted apparatus geometry.
