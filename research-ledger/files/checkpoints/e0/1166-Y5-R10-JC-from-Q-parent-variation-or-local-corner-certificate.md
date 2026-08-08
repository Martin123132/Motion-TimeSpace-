# 1166 — Y5/R10 J_C from Q parent variation or local corner certificate

**Current verdict:** this is genuine progress, but not a claim. If `J_C` is the lifted domain three-form from `det(Q)`/coframe volume, then local exactness is no longer a slogan: the obstruction reduces to the local domain integral `int_D delta J_C`. The missing parent law is now sharply named as a local volume-lock/domain-selector theorem.

**Main derivation:** `J_C=N_D^-1 det(Q) omega_0` gives `delta J_C = J_C Tr(Q^-1 delta Q) - J_C delta(log N_D)` up to domain/coframe-reference terms. Since `delta J_C` is a top 3-form on a 3-domain, it is kinematically closed. Local relative exactness/boundary silence requires the coherent integral obstruction to vanish: `int_D delta J_C = 0`, plus the boundary/corner/kernel certificates.

**No claim:** no local-GR, R10, PPN, WEP, clock, orbital, projected-metric theorem, or `c_g=0` result follows. The win is that the next missing theorem is precise.

## Source register

| source_id | relative_path | needle | exists | needle_found | role |
| --- | --- | --- | --- | --- | --- |
| SRC1166_0_1165_next | source-intake/mts_residuals/P8_Y5_R10_1165_NEXT_TARGET.csv | NEXT1165_0_1166 | True | True | handoff requiring J_C-from-Q variation or local corner certificate. |
| SRC1166_1_1165_origin | source-intake/mts_residuals/P8_Y5_R10_1165_LIFTED_C_PARENT_ACTION_CONTRACT.csv | LPC1165_1_origin_from_Q | True | True | origin-from-Q clause to attack. |
| SRC1166_2_1165_exactness | source-intake/mts_residuals/P8_Y5_R10_1165_LIFTED_C_PARENT_ACTION_CONTRACT.csv | LPC1165_5_exactness_law | True | True | delta J_C=dB_C exactness clause to reduce. |
| SRC1166_3_1165_boundary | source-intake/mts_residuals/P8_Y5_R10_1165_LIFTED_C_PARENT_ACTION_CONTRACT.csv | LPC1165_6_boundary_primitive_silence | True | True | boundary primitive silence clause. |
| SRC1166_4_1165_corner | source-intake/mts_residuals/P8_Y5_R10_1165_CCORNER_DSF_EPSILON_CERTIFICATE_ROWS.csv | CCZ1165_0_surface_without_corners | True | True | corner certificate row. |
| SRC1166_5_274_theorem_shape | 274-lifted-C-sector-form-holonomy-route.md | Let J_C be a domain 3-form memory current on a spatial domain D with boundary partial D. | True | True | lifted 3-form theorem shape. |
| SRC1166_6_274_delta | 274-lifted-C-sector-form-holonomy-route.md | delta J_C = dB_C | True | True | candidate exactness law. |
| SRC1166_7_275_volume | 275-JC-three-form-memory-current-from-Q.md | comes from the determinant / volume form of a 3D spatial domain. | True | True | J_C from determinant/volume form. |
| SRC1166_8_275_missing | 275-JC-three-form-memory-current-from-Q.md | boundary primitive / exactness law `delta J_C = dB_C` | not derived | True | True | exactness remains not derived in older checkpoint. |
| SRC1166_9_207_Bianchi | 207-domain-projector-action-and-Bianchi-identity.md | physical domain selection is still missing. | True | True | parent domain selector remains missing. |
| SRC1166_10_1020_surface | 1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md | BDC1020_0_surface_manifold | True | True | corner-free surface requirement. |
| SRC1166_11_1020_kernel | 1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md | BDC1020_4_kernel_weight | True | True | closed/bounded kernel weight requirement. |
| SRC1166_12_1020_stokes | 1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md | ETB1020_1_weighted_Stokes_identity | True | True | weighted Stokes identity. |
| SRC1166_13_1020_zero | 1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md | ETB1020_2_zero_conditions | True | True | full zero condition list. |

## J_C from Q/coframe variation derivation

| derivation_id | step | statement | result_status | what_it_proves | remaining_gap | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| JCV1166_0_candidate_definition | define lifted domain 3-form | On a spatial 3-domain D with reference volume form omega_0, take J_C = N_D^{-1} det(Q) omega_0, equivalently J_C = N_D^{-1} e^1∧e^2∧e^3 when Q maps the reference coframe to e. | FORMULA_SHAPE_DERIVED_CONDITIONALLY | J_C need not be invented as a disconnected repair field; it can be tied to Q/coframe volume. | Q, coframe, domain D, and normalization N_D must be parent-owned. | False |
| JCV1166_1_variation_formula | vary determinant/coframe volume | For invertible Q and fixed omega_0, delta J_C = J_C Tr(Q^{-1} delta Q) - J_C delta(log N_D), plus domain/coframe-reference terms if D or omega_0 varies. | KINEMATIC_VARIATION_FORMULA | the local source of lifted-C variation is a trace/load-volume variation, not an arbitrary scalar Cperp force. | parent variation must say whether D, omega_0, and N_D are fixed, dynamical, or constrained. | False |
| JCV1166_2_top_degree_closedness | closedness of top form | On a 3-domain, d(delta J_C)=0 kinematically because delta J_C is a top-degree 3-form. | MATH_CLOSEDNESS_DERIVED | the first d_rel entry condition is easier for a lifted top-form than for scalar Cperp. | closed does not mean relatively exact or boundary-silent. | False |
| JCV1166_3_absolute_exactness | absolute local exactness | If the local domain is contractible/topologically trivial so H^3(D)=0, closed top-form variations admit delta J_C=dB_C for some 2-form B_C. | CONDITIONAL_MATH_THEOREM | the lifted route has a real mathematical exactness path unavailable to ordinary scalar Cperp. | actual local domain topology and primitive choice must be certified. | False |
| JCV1166_4_relative_obstruction | relative cohomology obstruction | For an oriented compact connected 3-domain with boundary, the top relative class is measured by the domain integral: relative exactness with boundary silence requires the lifted variation to have zero coherent domain integral, int_D delta J_C = 0, up to certified boundary-class conventions. | KEY_OBSTRUCTION_IDENTIFIED | the missing theorem is not vague: it is a parent local volume-lock/domain-selector law. | derive int_D delta J_C=0 locally without killing the FLRW coherent class. | False |
| JCV1166_5_local_volume_lock | local branch lock | If the parent equations enforce delta C_D = delta(N_D^{-1} int_D J_C)=0 for stationary local domains, then the relative obstruction vanishes and the local lifted-C residual can be exact/boundary-silent subject to edge certificates. | CONDITIONAL_ROUTE_NOT_PARENT_DERIVED | a clean local-GR route exists in theorem shape. | no parent law currently enforces the volume lock and preserves physical charges. | False |
| JCV1166_6_FLRW_active_class | FLRW branch compatibility | The same criterion allows FLRW activity: a nonzero homogeneous H^3(D,partialD) class is exactly a nonzero domain integral rather than a local exact residual. | BRANCH_COMPATIBILITY_SHAPE | local silence and cosmological memory need not be hand-switched if the parent selector controls the integral class. | selector law and amplitude normalization remain missing. | False |
| JCV1166_7_verdict | derivation verdict | 1166 does not derive local GR; it reduces lifted-C exactness to the parent condition int_D delta J_C=0 on local stationary domains plus boundary/corner/kernel certificates. | PROGRESS_NOT_CLAIM | the next target is now precise: derive the local domain-volume lock or fill finite edge-bound rows. | parent action, P_D variation, boundary primitive, and local/FLRW selector. | False |

## Relative exactness criterion

| criterion_id | criterion | status | proof_role | missing_piece | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REC1166_0_domain_assumptions | D is compact, oriented, connected, smooth, three-dimensional, with smooth boundary S=partialD and no active corners. | ASSUMPTION_NOT_ARENA_CERTIFIED | needed before applying the top-form relative exactness criterion | actual local MTS domain representative | False |
| REC1166_1_JC_top_form | J_C is a true lifted top 3-form tied to Q/coframe volume, not a scalar residual relabelled as a form. | FORMULA_SHAPE_ONLY | prevents scalar Cperp resurrection | parent-owned J_C[Q,e,D] | False |
| REC1166_2_exactness_condition | delta J_C=dB_C locally if the absolute H^3 obstruction vanishes; in the relative/boundary-silent branch, the decisive obstruction is int_D delta J_C. | MATH_CRITERION_WRITTEN | turns exactness into a measurable/cohomological parent condition | parent law setting int_D delta J_C=0 locally | False |
| REC1166_3_boundary_primitive | boundary primitive silence requires a primitive B_C whose boundary readout is zero or source-bounded in the same boundary class. | NOT_CERTIFIED | prevents exact bulk terms from leaking into local edge force | B_C trace/norm and boundary class | False |
| REC1166_4_branch_selector | local branch has int_D delta J_C=0 while FLRW branch may carry nonzero coherent integral class. | PARENT_SELECTOR_MISSING | prevents hand-switching between local silence and cosmological activity | same-parent domain-volume selector | False |

## Local corner certificate attempt

| corner_id | target | certificate_attempt | status | missing_piece | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| LC1166_0_boundary_of_boundary | C_corner | If S=partialD is a smooth closed boundary of a smooth local 3-domain, then partialS=partial(partialD)=empty, so the pure Stokes corner term is mathematically zero. | CONDITIONAL_MATH_ZERO_NOT_ARENA_CERTIFIED | prove the actual readout surface is a smooth closed partialD without regulator/cutoff joints | False |
| LC1166_1_regulator_joints | C_corner | If local readout uses annuli, excised bodies, matched patches, or finite cutoffs, all joints must be enumerated and either zeroed or bounded. | NOT_CERTIFIED | corner/joint ledger for actual arena | False |
| LC1166_2_closed_weight | norm_dS_Feps | d_S(F_lambda epsilon_C)=0 would remove the weighted-Stokes derivative term; otherwise a norm bound is required. | NOT_CERTIFIED | F_lambda, epsilon_C, and surface derivative on the certified lifted-C boundary | False |
| LC1166_3_zero_verdict | edge zero | C_corner can be conditionally zeroed by smooth closed surface geometry, but full edge zero also needs closed weight, B_C primitive, h_C/r_C silence, and cocycle/projector silence. | FULL_EDGE_ZERO_NOT_PROVED | all non-corner edge terms | False |

## Runner dry-run

| run_id | test | status | blocked_by | detail | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| RUN1166_0_JC_variation | J_C from Q/coframe variation | PARTIAL_PASS_FORMULA_AND_OBSTRUCTION_DERIVED | parent domain-volume lock;domain representative;P_D variation;normalization | variation formula and relative obstruction are written, but no parent law enforces int_D delta J_C=0 | False |
| RUN1166_1_relative_exactness | delta J_C=dB_C promotion | REFUSED_RELATIVE_EXACTNESS_NOT_PARENT_SIGNED | int_D_delta_JC_zero;B_C_boundary_trace;Hrel_selector | exactness reduces to a precise integral obstruction rather than closing | False |
| RUN1166_2_corner_certificate | C_corner=0 certificate | PARTIAL_PASS_MATH_ZERO_NOT_ARENA_CERTIFIED | actual_smooth_closed_surface;regulator_joint_ledger;fixed_boundary_class | boundary-of-boundary zero is available only after the actual readout surface is certified | False |
| RUN1166_3_local_claim | local GR/R10/PPN/WEP/clock/orbital promotion | REFUSED_NO_LOCAL_CLAIM | RUN1166_0_JC_variation;RUN1166_1_relative_exactness;RUN1166_2_corner_certificate | 1166 is a real derivation reduction but not a local-physics pass | False |

## Claim gates

| gate_id | gate | current_status | reason | claim_allowed |
| --- | --- | --- | --- | --- |
| G1166_0_JC_origin | J_C[Q,e,D] is parent-owned and varied | PARTIAL_FORMULA_ONLY | det(Q)/coframe variation formula exists but parent action/domain variation is missing | False |
| G1166_1_local_volume_lock | int_D delta J_C=0 on stationary local domains | BLOCKED_KEY_OBSTRUCTION | no parent volume-lock/domain-selector law yet | False |
| G1166_2_FLRW_selector | nonzero FLRW integral class allowed by the same parent law | BLOCKED | local/FLRW branch selector still missing | False |
| G1166_3_edge_certificates | corner, closed-weight, B_C primitive, harmonic/residual/cocycle terms certified | BLOCKED | only conditional C_corner math zero is identified | False |
| G1166_4_local_promotion | GR/Newton/R10/PPN/WEP/clock/orbital promotion | BLOCKED_NO_LOCAL_CLAIM | relative exactness and edge certificates remain nonclaim | False |

## Decision ledger

| decision_id | decision | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| D1166_0_real_progress | lifted_C_exactness_reduced_to_domain_integral_obstruction | J_C as a top 3-form gives kinematic closedness; relative silence hinges on int_D delta J_C=0 | derive the parent local volume-lock/domain-selector law | False |
| D1166_1_corner_progress | Ccorner_has_conditional_boundary_of_boundary_zero | smooth S=partialD gives partialS=empty, but actual local readout surfaces may have cutoffs/corners | certify the actual local surface or keep corner row bounded | False |
| D1166_2_best_next | target_parent_volume_lock_or_finite_edge_bound | this is now the narrowest missing law behind derived local GR for lifted C | 1167 should try the local volume-lock selector first, then fill finite edge norms if it fails | False |

## Validation

| check_id | result | detail | claim_allowed |
| --- | --- | --- | --- |
| V1166_0_sources_exist | pass | all cited local source paths exist and needles are found | False |
| V1166_1_variation_formula_written | pass | J_C from det(Q)/coframe variation formula is recorded | False |
| V1166_2_relative_obstruction_identified | pass | relative exactness is reduced to int_D delta J_C=0 plus boundary certificates | False |
| V1166_3_volume_lock_blocked | pass | parent local volume-lock law remains blocked rather than assumed | False |
| V1166_4_corner_partial_only | pass | C_corner has conditional boundary-of-boundary zero but no arena certificate | False |
| V1166_5_runner_refuses_claim | pass | runner refuses relative-exactness, corner, and local promotion claims | False |
| V1166_6_no_claim_rows | pass | all generated rows remain nonclaim | False |
| V1166_7_next_target | pass | 1167 handoff targets parent volume-lock selector or finite edge-bound fill | False |
| V1166_8_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work | False |
| V1166_9_csv_parse | pass | all 1166 CSV outputs parse cleanly | False |
| V1166_10_formalization_untouched | pass | generator writes no outputs under formalization-workbench | False |
| V1166_SUMMARY | pass | 1166 derives the lifted-JC variation/relative-obstruction shape, conditionally zeros pure corners, and names parent volume-lock as the next hard law | False |

## Next target

| next_id | next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NEXT1166_0_1167 | 1167-Y5-R10-parent-volume-lock-selector-or-finite-edge-bound-fill.md | derive or reject the parent law enforcing int_D delta J_C=0 on local stationary domains while allowing nonzero FLRW H^3 class; if rejected, fill finite edge-bound rows for C_corner and norm_dS_Feps | domain-volume functional; local stationarity; FLRW homogeneous class; P_D variation; N_D normalization; boundary class; C_corner surface certificate; dS_Feps bound; runner dry-run | scalar Cperp promotion; local/FLRW hand switch; projected metric theorem; invented constants; local-GR claim; c_g zero claim; GitHub; formalization edits | False |
