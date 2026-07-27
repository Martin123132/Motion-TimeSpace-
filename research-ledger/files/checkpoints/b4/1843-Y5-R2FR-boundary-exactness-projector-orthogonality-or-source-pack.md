# 1843 Y5 R2FR boundary exactness projector orthogonality or source pack

**Progress:** 1843 turns the edge/source leakage problem into exact local conditions: certified boundary domain, explicit `B_X=d_S b_X+h_X+r_X`, closed weighted-Stokes kernel, projector orthogonality, and a no-cancellation source pack if any theorem route fails.

**Current verdict:** no boundary-zero or projector-zero claim is allowed. The useful progress is that `Q_edge=0` now has exact conditions, and if those conditions fail the fallback is a finite weighted-Stokes bound, not a closure axiom.

**Claim ceiling:** no `Q_edge=0`, `Qbar_edge_XH=0`, R10/R11 pass, Newton/local-GR reduction, PPN pass, edge-source cancellation, GitHub action, or `formalization-workbench` edit is allowed from 1843.

## Source Register
| source_id | source_key | source_path | exists | needles_present | missing_needles | role |
| --- | --- | --- | --- | --- | --- | --- |
| SRC1843_0_1842_next | 1842_next_target | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1842_NEXT_TARGET.csv | True | True |  | 1842 selects boundary exactness/projector orthogonality or source pack. |
| SRC1843_1_1842_validation | 1842_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1842_VALIDATION.csv | True | True |  | confirms 1842 passed as a nonclaim checkpoint. |
| SRC1843_2_1842_owner_verdict | 1842_owner_verdict | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1842_OWNER_CLAUSES.csv | True | True |  | 1842 owner map is explicit but does not close current MTS. |
| SRC1843_3_1019_exactness | 1019_boundary_exactness | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv | True | True |  | 1019 boundary exactness route and failure. |
| SRC1843_4_1019_projector | 1019_projector_orthogonality | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1019_PROJECTOR_ORTHOGONALITY_CLAUSES.csv | True | True |  | 1019 projector orthogonality route and failure. |
| SRC1843_5_1019_source_pack | 1019_source_pack_schema | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv | True | True |  | 1019 source pack schema for FB5540/bulk/edge/R11 no-cancellation guard. |
| SRC1843_6_1020_domain | 1020_boundary_domain_certificate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1020_BOUNDARY_DOMAIN_CERTIFICATE.csv | True | True |  | 1020 boundary domain/cohomology certificate and current blocker. |
| SRC1843_7_1020_stokes | 1020_weighted_stokes | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1020_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv | True | True |  | 1020 weighted-Stokes theorem and fallback bound. |
| SRC1843_8_1020_BX | 1020_BX_primitive_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1020_BX_PRIMITIVE_AUDIT.csv | True | True |  | 1020 identifies explicit B_X primitive as next hard object. |

## Boundary Exactness Clauses
| clause_id | claim | mathematical_form | current_status | what_would_close | failure_mode | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BE1843_0_domain | edge integration domain has no untracked corner or domain dependence | partial S_edge=empty, or every corner C carries explicit Q_C in source pack | NOT_SIGNED | parent boundary class fixes S_edge and corner terms before readout | Stokes zero hides corner/domain charge | False |
| BE1843_1_exact_BX | boundary momentum is exact on the certified boundary class | B_X=d_S b_X with no residual r_X and no harmonic h_X | NOT_DERIVED | derive b_X from parent L_X/Theta_X/Q_X plus fixed counterterm | Q_edge remains live or must be bounded | False |
| BE1843_2_harmonic_residual | no harmonic or residual edge class survives | B_X=d_S b_X+h_X+r_X with h_X=r_X=0 | NOT_SIGNED | boundary cohomology/no-hair theorem or source-backed h_X/r_X bounds | closed but wrong edge mode feeds R10/R11 | False |
| BE1843_3_closed_weight | weighted Stokes derivative term vanishes | d_S(F_lambda epsilon_X)=0 on S_edge | NOT_SIGNED | kernel/gauge weight closure theorem or source-backed derivative norm | exact B_X still leaves weighted derivative residual | False |
| BE1843_4_counterterm_reference | boundary counterterm/reference cannot be tuned after readout | B_ct,B_ref fixed once; partial_source Delta_ref=0 | NOT_SIGNED | parent variational principle fixes counterterm and reference class | reference absorbs source calibration or edge charge | False |
| BE1843_5_verdict | boundary exactness kills edge branch | BE1843_0 through BE1843_4 imply Q_edge^H(lambda)=0 and K_boundary=0 | FAIL_CURRENT_CLAIM | all exactness clauses parent-signed in one boundary class | retain source-pack fallback rows for Qbar_edge_XH and K_edge | False |

## Projector Orthogonality Clauses
| clause_id | claim | mathematical_form | current_status | what_would_close | failure_mode | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PO1843_0_projector_definition | Pi_M^H is the fixed Hamiltonian source-mass projector | Pi_M^H[J] = component of J paired with same-frame M_H_ref | NOT_SIGNED | M_H_ref and Pi_M^H defined from parent Hamiltonian charge before readout | projector can select wrong object | False |
| PO1843_1_edge_mass_independence | edge charge has no same-frame source-mass dependence | partial Q_edge^H(lambda)/partial M_H_ref \|_{tau,reference,surface}=0 | NOT_DERIVED | Q_edge depends only on fixed boundary cohomology/gauge data, not source worldtube data | Qbar_edge_XH(lambda) remains live | False |
| PO1843_2_symplectic_block | source and edge sectors are symplectically orthogonal | Omega(delta_M Phi,delta_edge Phi)=0 and Pi_M^H[delta_edge Q]=0 | NOT_DERIVED | block-diagonal reduced symplectic form or exact mixed term | edge/source mixing feeds FB5540 or R10/R11 | False |
| PO1843_3_reference_silence | reference subtraction does not reroute edge charge into mass readout | Pi_M^H[Delta_ref+Delta_symp+B_class]=0 | NOT_SIGNED | B_ref derivative-silent theorem plus boundary class certificate | projector orthogonality broken by reference movement | False |
| PO1843_4_conditional_zero | projector clauses kill edge Hamiltonian source charge | PO1843_0 through PO1843_3 imply Qbar_edge_XH(lambda)=0 | CONDITIONAL_THEOREM_ONLY | parent-signed projector definition, mass-independence, block and reference lemmas | cannot zero edge projection row | False |
| PO1843_5_verdict | projector orthogonality kills edge source projection | Pi_M^H[Q_edge]=0 with no reference, tau, or surface leakage | FAIL_CURRENT_CLAIM | PO1843_0 through PO1843_4 signed by same parent action/boundary class | retain Qbar_edge_XH source-pack row | False |

## Boundary Domain Certificate
| certificate_id | object | required_certificate | mathematical_test | current_status | failure_if_missing | feeds | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BDC1843_0_surface_manifold | edge surface S_edge | compact oriented smooth codim-2 surface with no active corner boundary | partial S_edge=empty or every corner C has explicit corner charge Q_C | NOT_SIGNED | Stokes zero can hide corner charge | Q_edge_zero;corner_source_row | False |
| BDC1843_1_boundary_class | allowed boundary class B_class | same B_class used by L_X,Q_X,B_ref,Pi_M^H and R10/R11 readout | delta B_class=0 along source variation and no retuning between source/test systems | NOT_SIGNED | reference or boundary class can absorb the signal | FB5540;Qbar_edge_XH | False |
| BDC1843_2_relative_cohomology | relative edge cohomology H_edge | harmonic/non-exact edge class absent or separately measured as h_X | B_X=d_S b_X+h_X with h_X=0, or \|int_S F_lambda epsilon h_X\| source-bounded | NOT_SIGNED | exactness misses a harmonic edge mode | harmonic_edge_bound;Q_edge_zero | False |
| BDC1843_3_allowed_epsilon | epsilon_X domain | epsilon_X is a proper X-representative gauge while physical tau/mass/rotation generators remain admissible | epsilon_X\|S_edge=0 or d_S(F_lambda epsilon_X)=0 without constraining tau_source or ADM charges | CLOSURE_ONLY | proper-gauge zero may erase real physical charges | Q_edge_zero;projector_definition | False |
| BDC1843_4_kernel_weight | F_lambda epsilon_X | edge kernel/gauge weight closed on S_edge or derivative term source-bounded | d_S(F_lambda epsilon_X)=0, or \|\|d_S(F_lambda epsilon_X)\|\|_* and \|\|b_X\|\|_* are supplied | NOT_SIGNED | weighted Stokes identity leaves derivative residual | kernel_derivative_bound | False |
| BDC1843_5_verdict | boundary domain certificate | BDC1843_0 through BDC1843_4 signed in one parent boundary class | closed/corner-free plus cohomology plus epsilon/kernel conditions imply no untracked edge domain term | FAIL_CURRENT_CLAIM | Q_edge cannot be set to zero by Stokes alone | 1844_BX_primitive_or_edge_bound | False |

## Weighted Stokes Theorem And Bound
| theorem_id | statement | formula | current_result | missing_for_claim | bound_if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ETB1843_0_decomposition | boundary momentum decomposes into exact, harmonic and residual pieces | B_X=d_S b_X+h_X+r_X | FORMAL_DECOMPOSITION | parent L_X/Theta_X/Q_X must prove r_X=0 and identify h_X | \|Q_edge\| keeps \|int_S F epsilon h_X\| + \|int_S F epsilon r_X\| | False |
| ETB1843_1_weighted_Stokes_identity | exactness kills edge charge only when kernel/gauge weight has no surface derivative term | int_S F epsilon d_S b_X = int_partialS F epsilon b_X - int_S d_S(F epsilon) wedge b_X | MATH_IDENTITY_WRITTEN | partialS=empty or corner row, plus d_S(F epsilon)=0 or a derivative bound | \|int_S F epsilon d_S b_X\| <= \|\|d_S(F epsilon)\|\|_* \|\|b_X\|\|_* + \|corner_term\| | False |
| ETB1843_2_zero_conditions | genuine edge-zero theorem needs exactness, no harmonic/residual/corner terms, and closed weight | partialS=empty, h_X=0, r_X=0, d_S(F epsilon)=0 => Q_edge^H(lambda)=0 | CONDITIONAL_THEOREM | all hypotheses unsigned in current MTS | use ETB1843_3 residual bound instead of zero | False |
| ETB1843_3_residual_bound | if exact zero fails, edge charge has a finite source-pack bound | \|Q_edge(lambda)\| <= C_corner + \|\|d_S(F_lambda epsilon_X)\|\|_* \|\|b_X\|\|_* + \|int_S F_lambda epsilon_X h_X\| + \|int_S F_lambda epsilon_X r_X\| | BOUND_LAW_STAGED | numeric/source-backed norms for each term and units | first nonclaim source row stores terms with valid_for_claim=false | False |
| ETB1843_4_projector_bound | Hamiltonian/source projection is bounded after M_H_ref and Pi_M norm are owned | \|Qbar_edge_XH(lambda)\| <= \|\|Pi_M^H\|\| \|Q_edge(lambda)\| / M_H_ref_min | CONDITIONAL_BOUND | Pi_M^H definition, M_H_ref_min and source-backed Q_edge bound | Qbar_edge_XH remains MISSING_SOURCE_BACKED_QBAR_EDGE_XH | False |
| ETB1843_5_verdict | exact local condition and fallback bound are derived, but not the zero theorem | Q_edge=0 conditional; Q_edge_bound schema-ready; no claim promoted | FAIL_CURRENT_CLAIM_BUT_DERIVATION_PROGRESS | B_X primitive, h_X/r_X zero or bounds, kernel derivative bound, corner audit, M_H_ref/Pi_M | move to 1844 B_X primitive or first source-bound term | False |

## Source Pack Schema
| pack_id | quantity | definition | required_columns | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SP1843_0_M_H_ref | M_H_ref | same-frame Hamiltonian source denominator | system_id;tau_id;surface;Q_tau_integral;G_ref;H_ref;M_H_ref;units;reference_rule;source_path;valid_for_claim | MISSING_STABLE_MH_REF | False |
| SP1843_1_FB5540_components | delta_H_tau_nonintegrable_over_MH;Delta_ref_over_MH;symplectic_boundary_flux_over_MH | componentwise FB5540 numerator rows normalized by M_H_ref | system_id;component_id;value_abs;M_H_ref;units;source_path;assumptions;valid_for_claim | MISSING_FB5540_COMPONENT_VALUES | False |
| SP1843_2_edge_bound_terms | C_corner;norm_dS_Feps;norm_bX;harmonic_edge_abs;residual_edge_abs | weighted-Stokes bound terms for Q_edge(lambda) | system_id;lambda;C_corner;norm_dS_Feps;norm_bX;harmonic_edge_abs;residual_edge_abs;units;source_path;valid_for_claim | MISSING_EDGEBOUND_TERMS | False |
| SP1843_3_projected_edge_bound | Qbar_edge_XH_bound(lambda) | projected edge bound after Pi_M^H norm and M_H_ref_min | system_id;lambda;PiM_norm;Q_edge_bound;M_H_ref_min;Qbar_edge_XH_bound;units;source_path;valid_for_claim | MISSING_PIM_NORM_OR_MHREF_MIN | False |
| SP1843_4_bulk_X_coefficients | Z_X;M_X2;J_X;lambda_X;K_X;Qbar_XH;qbar_XT | bulk X residual coefficients if no-pole/source-free theorem fails | system_id;field_id;Z_X;M_X2;J_X;lambda_X;K_X;Qbar_XH;qbar_XT;units;source_path;valid_for_claim | MISSING_PARENT_INPUT_OR_ARENA_PROJECTION | False |
| SP1843_5_edge_coefficients | lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;alpha_edge(lambda) | edge residual amplitude if boundary/projector theorem fails | system_id;lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;alpha_edge;units;source_path;valid_for_claim | MISSING_EDGE_PROJECTION | False |
| SP1843_6_total_guard | alpha_total_guard(lambda) | absolute no-cancellation envelope across FB5540, bulk X, edge X and R11 | system_id;lambda;abs_alpha_bulk;abs_alpha_edge;abs_FB5540;abs_alpha_R11;component_sum_abs;bound;source_path;valid_for_claim | NOT_COMPUTED_COMPONENTS_MISSING | False |

## Route Verdicts
| route_id | route | status | requires | result | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RVT1843_0_boundary_exactness | derive Q_edge=0 from exact boundary form | CONDITIONAL_NOT_PROMOTED | BE1843 clauses plus BDC1843 certificates and ETB1843 zero conditions | FAIL_CURRENT_CLAIM | retain edge source-pack rows | False |
| RVT1843_1_projector_orthogonality | derive Qbar_edge_XH=0 from mass-projector orthogonality | CONDITIONAL_NOT_PROMOTED | PO1843 clauses plus M_H_ref/Pi_M^H owner | FAIL_CURRENT_CLAIM | source or bound Pi_M^H[Q_edge] | False |
| RVT1843_2_weighted_stokes_bound | finite edge residual bound from derivative/harmonic/corner terms | BEST_CURRENT_FALLBACK | C_corner,norm_dS_Feps,norm_bX,harmonic_edge_abs,residual_edge_abs,M_H_ref_min,PiM_norm | SOURCE_PACK_SCHEMA_READY_NO_VALUES | 1844 B_X primitive or first edge-bound term | False |
| RVT1843_3_no_double_count | orthogonal source split prevents duplicate scoring | GUARD_WRITTEN_NOT_DERIVED | bulk/edge/FB5540/R11 projectors and source currents | BLOCKS_CURRENT_CLAIM | absolute no-cancellation envelope | False |
| RVT1843_4_verdict | 1843 branch closure | FAIL_CURRENT_CLAIM_BUT_NARROWS_GAP | theorem-zero route or complete source pack | no R10/R11/Newton/local-GR pass | 1844 explicit B_X primitive from parent variation or edge-bound term fill | False |

## GR Bridge Status
| status_id | bridge_piece | current_status | evidence | remaining_gap | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| GB1843_0_edge_zero | edge/boundary zero theorem | CONDITIONAL_NOT_PROMOTED | BE1843;BDC1843;ETB1843 | B_X primitive, cohomology, corner, kernel-weight and reference certificates missing | False |
| GB1843_1_projector_zero | edge-source projector orthogonality | CONDITIONAL_NOT_PROMOTED | PO1843 | Pi_M^H, M_H_ref, source/edge symplectic block and reference silence unsigned | False |
| GB1843_2_source_pack | FB5540/bulk/edge/R11 source pack | SCHEMA_READY_NO_VALUES | SP1843 rows | all source-backed numeric/theorem-zero terms missing | False |
| GB1843_3_Newton_GR | Newton/local-GR bridge | BLOCKED | RVT1843_4 | edge/source leakage and M_H_ref normalization still open | False |
| GB1843_4_next | next derivation owner | BX_PRIMITIVE_FROM_PARENT_VARIATION_OR_EDGE_BOUND_TERM_FILL_IS_NEXT | ETB1843_5;1020 B_X primitive audit | derive explicit b_X primitive or fill first weighted-Stokes bound term | False |

## Claim Gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1843_0_boundary_exactness_closed | boundary exactness theorem closes Q_edge | False | domain, B_X primitive, harmonic/residual, kernel-weight and reference clauses are unsigned | False | False |
| CG1843_1_projector_orthogonality_closed | projector orthogonality theorem closes Qbar_edge_XH | False | Pi_M^H definition, edge mass-independence, symplectic block and reference silence are unsigned | False | False |
| CG1843_2_weighted_stokes_zero | weighted Stokes gives Q_edge=0 | False | d_S(F_lambda epsilon_X)=0, h_X=r_X=0 and no-corner conditions are not proved | False | False |
| CG1843_3_source_pack_complete | FB5540/bulk/edge/R11 source pack is complete | False | source pack rows remain missing or not computed | False | False |
| CG1843_4_first_bound_rows_staged | first edge bound row schema is staged as nonclaim | True | weighted-Stokes bound terms are explicit but missing source values | False | False |
| CG1843_5_R10_R11_Newton_GR | R10/R11/Newton/local-GR can pass | False | no theorem-zero or complete source-backed comparator row exists | False | False |

## Decisions
| decision_id | decision | reason | next_action |
| --- | --- | --- | --- |
| DEC1843_0_theorem_attempt | BOUNDARY_PROJECTOR_ROUTE_PRECISE_BUT_NOT_CLOSED | Stokes/projector arguments can kill edge leakage only after boundary domain, B_X primitive, cohomology, kernel and reference clauses are parent-signed | derive explicit B_X primitive from parent variation or fill bound terms |
| DEC1843_1_weighted_stokes | WEIGHTED_STOKES_IS_THE_CORRECT_LOCAL_BOUND_LAW | exactness alone is insufficient when F_lambda epsilon_X has a surface derivative, harmonic piece, residual piece, or corner term | carry C_corner, norm_dS_Feps, norm_bX, harmonic_edge_abs and residual_edge_abs explicitly |
| DEC1843_2_source_pack | NO_CANCELLATION_SOURCE_PACK_REQUIRED_IF_THEOREM_FAILS | edge, bulk, FB5540 and R11 components cannot cancel while inputs are unknown | do not run comparators until source pack terms are real |
| DEC1843_3_best_next | BX_PRIMITIVE_FROM_PARENT_VARIATION_OR_EDGE_BOUND_TERM_FILL_IS_NEXT | without b_X, both the zero theorem and weighted-Stokes bound lack their central object | 1844-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md |

## Next Target
| route_id | next_target | script | objective | selection_status | success_condition |
| --- | --- | --- | --- | --- | --- |
| NEXT1843_0_primary | 1844-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md | scripts/Y5_R2FR_BX_primitive_from_parent_variation_or_edge_bound_term_fill_1844.py | derive the explicit B_X primitive from parent L_X/Theta_X/Q_X and boundary counterterm, or fill the first EDGEBOUND term with source-backed units | selected | b_X is derived with boundary/cohomology certificates, or C_corner/norm_dS_Feps/norm_bX/harmonic/residual terms are source-backed nonclaim rows |
| NEXT1843_1_parallel | 1844b-Y5-R2FR-MHref-PiM-norm-edge-bound-acquisition.md | scripts/Y5_R2FR_MHref_PiM_norm_edge_bound_acquisition_1844b.py | stage M_H_ref_min and Pi_M^H norm inputs needed to project Q_edge_bound to Qbar_edge_XH_bound | parallel_held | projected edge bound remains nonclaim until denominator, projector norm and edge bound are all source-backed |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1843_0_sources_exist | PASS | all cited source paths exist |
| VAL1843_1_needles_present | PASS | all cited source needles are present |
| VAL1843_2_exactness_blocks_claim | PASS | boundary exactness theorem remains nonclaim |
| VAL1843_3_projector_blocks_claim | PASS | projector orthogonality theorem remains nonclaim |
| VAL1843_4_domain_certificate_complete | PASS | domain certificate covers surface, cohomology, kernel and verdict |
| VAL1843_5_weighted_stokes_written | PASS | weighted-Stokes theorem and fallback bound are written |
| VAL1843_6_source_pack_nonclaim | PASS | source pack rows are explicit and nonclaim |
| VAL1843_7_bridge_next | PASS | bridge status selects B_X primitive/edge-bound next |
| VAL1843_8_claim_gates_blocked | PASS | all claim gates remain blocked except nonclaim staging row |
| VAL1843_9_no_claim_flags | PASS | no generated claim flags are true |
| VAL1843_10_missing_not_ready | PASS | no MISSING_* row is marked ready |
| VAL1843_11_decision_next | PASS | decision selects B_X primitive or edge-bound fill |
| VAL1843_12_next_selected | PASS | next target selected |
| VAL1843_13_csv_parse | PASS | all generated 1843 CSVs parse |
| VAL1843_14_branch_copies | PASS | branch/quarantine/queue copies exist |
| VAL1843_15_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1843_16_formalization_untouched | PASS | no 1843 outputs found under formalization-workbench |
| VAL1843_OVERALL | PASS | 1843 boundary exactness projector orthogonality or source pack |

## Working Interpretation
This is real progress toward a derivable GR/Newton bridge: the edge sector is no longer a vague 'boundary effect'. It is now an explicit weighted-Stokes problem. The next hard object is `b_X`; without it, both zero and bound routes are missing their central primitive.
