# 1857: Auxiliary/Constraint X Local-GR Route

**Current verdict:** the constraint/auxiliary route has a clean conditional theorem: if the residual is eliminated before physical phase space and ordinary matter readout, local scalar hair is absent and GR/Newton can be the reduced local branch. But the route is not yet proven for MTS: parent phase space, constraint origin, generator or auxiliary solve, boundary charge, degree count, matter descent and physical-component lock remain unsigned.

## Source Register
| source_id | source_path | needle | use | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC1857_0_1856_handoff | 1856-Y5-R2FR-derive-X-sector-from-MTS-primitives-or-reject-physical-scalar.md | NEXT1856_0_primary | selected auxiliary/constraint local-GR route | FOUND | False |
| SRC1857_1_first_class_contract | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1555_FIRST_CLASS_CONSTRAINT_CONTRACT.csv | FCC1555_7_no_GR_import | first-class constraint acceptance requirements | FOUND | False |
| SRC1857_2_constraint_class | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1562_CONSTRAINT_CLASS_GATE.csv | CLASS1562_5_second_class | first-class vs second-class constraint class gate | FOUND | False |
| SRC1857_3_constraint_action | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1668_CONSTRAINT_FIRST_ACTION_ATTEMPT.csv | CFA1668_8_verdict | constraint-first action attempt | FOUND | False |
| SRC1857_4_descent_theorem | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1675_CONSTRAINT_FIRST_DESCENT_THEOREM_ATTEMPT.csv | constraint_first_DqZ_zero_descent_theorem | conditional descent theorem attempt | FOUND | False |
| SRC1857_5_exclusion_gate | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1783_CONSTRAINT_FIRST_EXCLUSION_GATE.csv | CFE1783_7_verdict | constraint-first exclusion gate | FOUND | False |
| SRC1857_6_nonprop_constraint | 07-nonpropagating-reciprocity-constraint.md | best route = hard constraint or phase-volume balance | nonpropagating reciprocity route | FOUND | False |
| SRC1857_7_qmap_guard | 1157-Y5-R10-parent-q-map-null-generator-proof-or-cg-bound-first-fill.md | no local physical X mode | quotient/null guard for no physical scalar | FOUND | False |

## Constraint Local-GR Conditional Theorem
| theorem_id | statement | mathematical_role | proof_status | current_mts_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CLG1857_0_setup | Let parent phase space P contain a residual coordinate Z/X and a constraint C_X(Phi)=0. | defines the candidate nonpropagating local residual | SETUP | NEEDS_PARENT_PHASE_SPACE | False |
| CLG1857_1_elimination_before_readout | If C_X eliminates Z/X before physical phase space and before ordinary matter/readout functors are defined, then Dq(v_X)=0 for the eliminated direction. | turns X from physical scalar hair into a null/removed representative | CONDITIONAL_THEOREM_VALID | NEEDS_CONSTRAINT_AND_Q_MAP | False |
| CLG1857_2_first_class_case | If G_X[epsilon] is differentiable, has zero/proper boundary charge, and closes first-class, then P_red=C_X^{-1}(0)/Gauge_X contains no physical X pair. | removes local scalar degree by gauge quotient | CONDITIONAL_THEOREM_VALID | NEEDS_GENERATOR_BRACKET_BOUNDARY_DEGREE_COUNT | False |
| CLG1857_3_second_class_auxiliary_case | If X and its multiplier form an algebraic second-class auxiliary pair, solve them before phase space and substitute back into the action. | removes local scalar degree by elimination rather than gauge | CONDITIONAL_THEOREM_VALID | NEEDS_ALGEBRAIC_SOLVE_AND_NO_NONLOCAL_TAIL | False |
| CLG1857_4_matter_descent | If S_matter and observed coframe depend only on reduced variables q(Phi), ordinary test bodies cannot source the eliminated X direction. | prevents fifth-force/source charge return after elimination | CONDITIONAL_THEOREM_VALID | NEEDS_MATTER_READOUT_DESCENT | False |
| CLG1857_5_local_GR_consequence | If CLG1857_0 through CLG1857_4 all close, local GR/Newton can be the reduced branch without physical X scalar hair. | local-GR theorem target | EXACT_CONDITIONAL_TARGET | FAIL_CURRENT_CLAIM_PREMISES_UNSIGNED | False |

## Constraint Gate Audit
| gate_id | needed_gate | acceptance | current_status | blocks_local_gr_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CGA1857_0_parent_phase_space | parent phase space and symplectic form | fields, symplectic/current form and constraints are declared without importing GR as conclusion | NOT_PARENT_SIGNED | True | False |
| CGA1857_1_constraint_equation | constraint equation C_X=0 | constraint follows from MTS parent action/motion-load/phase-volume law | PARENT_ORIGIN_OPEN | True | False |
| CGA1857_2_generator | differentiable generator or algebraic auxiliary solve | delta G_X is well-defined, or auxiliary equations solve locally without nonlocal tail | NOT_DERIVED | True | False |
| CGA1857_3_boundary_charge | zero/proper boundary charge | Q_X is zero, exact, fixed, or retained as explicit boundary residual | BOUNDARY_SILENCE_UNSIGNED | True | False |
| CGA1857_4_bracket_degree | constraint class and degree count | first-class pair removes two phase-space dimensions, or second-class auxiliary pair is eliminated | DEGREE_COUNT_NOT_CLOSED | True | False |
| CGA1857_5_matter_readout_descent | ordinary matter/readout descends after elimination | S_matter=Sbar[q(Phi),Psi,theta] and no hidden marker/source tail returns | MATTER_DESCENT_UNSIGNED | True | False |
| CGA1857_6_physical_component_lock | removed variable is exactly the dangerous local X/c_g direction | physical-component lock maps the eliminated residual to the PPN/R10/local coupling direction | PHYSICAL_COMPONENT_LOCK_MISSING | True | False |
| CGA1857_7_verdict | all constraint-first gates close | CGA1857_0 through CGA1857_6 pass from one parent branch | FAIL_CURRENT_CLAIM | True | False |

## Auxiliary/Constraint Route Comparison
| route_id | route | strength | weakness | current_status | next_requirement | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ACR1857_0_first_class | first-class quotient constraint | best if generator/boundary/brackets close; clean no-hair by quotient | hardest algebra and boundary proof | CONDITIONAL_NOT_CLOSED | parent phase-space/generator/bracket package | False |
| ACR1857_1_second_class_auxiliary | second-class algebraic auxiliary elimination | simpler elimination if equations solve locally | can leave nonlocal tails or hidden source/readout terms | CONDITIONAL_NOT_CLOSED | local algebraic solve plus no-tail proof | False |
| ACR1857_2_nonprop_reciprocity | hard nonpropagating reciprocity constraint | closest to prior local metric reciprocity work | parent origin/multiplier still open | PROMISING_PARENT_ORIGIN_OPEN | derive from motion-load/phase-volume law | False |
| ACR1857_3_current_selection | constraint-first proof package | least dangerous route to derived local GR | still many unsigned gates | SELECT_FOR_NEXT_GATE_BUILD | build parent constraint package with no GR import | False |

## Local-GR Status
| status_id | branch | local_gr_status | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| LGS1857_0_physical_scalar | physical scalar | DEMOTED_TO_EFT_CLOSURE | 1856 rejected primitive derivation | False |
| LGS1857_1_constraint | constraint/auxiliary | EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED | 1857 theorem is clean but gates fail current claim | False |
| LGS1857_2_project | overall local-GR route | NARROWED_TO_CONSTRAINT_PACKAGE | we now know the proof package required instead of chasing scalar coefficients | False |

## Claim Gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1857_0_conditional_theorem | constraint/auxiliary route has a valid conditional theorem shape | True | reduced phase space or algebraic elimination would remove physical X hair before readout | True | False |
| CG1857_1_parent_constraint | MTS parent action supplies the constraint | False | parent origin and no-GR-import proof remain open | False | False |
| CG1857_2_boundary_degree_matter | boundary charge, degree count and matter descent all close | False | CGA1857 gates remain unsigned | False | False |
| CG1857_3_local_GR | local GR/Newton reduction is derived | False | constraint theorem is conditional only | False | False |

## Decisions
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC1857_0_theorem_status | Constraint-first local GR is an exact conditional theorem target. | if X is eliminated before physical phase space and matter readout, there is no physical scalar hair to test locally. | build the parent constraint package rather than returning to physical scalar coefficients | False |
| DEC1857_1_current_block | The route is not yet a local-GR derivation. | parent origin, generator/boundary/bracket/degree/matter descent and physical-component lock are unsigned. | derive or reject the parent constraint package | False |
| DEC1857_2_next | Next target is the parent constraint package with no GR import. | that package is the bottleneck that decides whether the selected route is real MTS or another closure. | 1858-Y5-R2FR-parent-constraint-package-no-GR-import-gate.md | False |

## Next Target
| route_id | next_target | script | objective | selection_status | success_condition |
| --- | --- | --- | --- | --- | --- |
| NEXT1857_0_primary | 1858-Y5-R2FR-parent-constraint-package-no-GR-import-gate.md | scripts/Y5_R2FR_parent_constraint_package_no_GR_import_gate_1858.py | derive or reject the parent constraint package: phase space, constraint, generator/auxiliary solve, bracket/degree count, boundary charge, matter descent and no-GR-import proof | selected | constraint package closes from MTS primitives, or the constraint route is demoted to closure-only |
| NEXT1857_1_parallel | 1858b-Y5-R2FR-motion-load-phase-volume-parent-origin.md | scripts/Y5_R2FR_motion_load_phase_volume_parent_origin_1858b.py | derive the nonpropagating reciprocity constraint from motion-load/phase-volume balance | held | constraint multiplier/origin is derived without importing GR reciprocity as an axiom |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1857_0_sources_exist | PASS | all cited source paths exist |
| VAL1857_1_needles_present | PASS | all cited source needles are present |
| VAL1857_2_conditional_theorem | PASS | local-GR conditional theorem target is present |
| VAL1857_3_gate_audit_blocks | PASS | all constraint gates block local-GR claim until signed |
| VAL1857_4_route_selected | PASS | constraint-first proof package remains selected |
| VAL1857_5_local_status_nonclaim | PASS | local-GR status remains conditional and nonclaim |
| VAL1857_6_claim_gates_safe | PASS | conditional theorem gate passes but local-GR claim does not |
| VAL1857_7_next_target_selected | PASS | next target selected |
| VAL1857_8_no_claim_flags | PASS | no valid_for_claim flags are true |
| VAL1857_9_csv_parse | PASS | all generated 1857 CSVs parse |
| VAL1857_10_branch_copies | PASS | branch/quarantine/queue copies exist |
| VAL1857_11_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1857_12_formalization_untouched | PASS | no 1857 outputs found under formalization-workbench |
| VAL1857_OVERALL | PASS | 1857 auxiliary constraint X local-GR route |

## Working Interpretation
This is the route we wanted: no fifth-force scalar to hide. But it is only earned if the constraint package is real. The next checkpoint should try to build that package without importing GR as the answer.
