# 2246 - Y5/R2FR R_AB Parent Boundary Charge Formula B_R or Alpha3 Projection Bound

## Verdict
- 2246 turns the boundary leak into an explicit formula contract: `Q_R[epsilon]=int_partialSigma epsilon_AB B_R^AB dS`.
- The candidate density is `B_R^AB = sigma n_mu P_R^{mu AB} + B_ct^AB + B_ref^AB + B_exact^AB`, but this is not parent-owned until `L_R`, `Theta_R`, and `P_R` are derived or selected.
- The alpha3 fallback is now an exact inequality: `|K_boundary_alpha3 Phi_boundary_local| <= 4e-20`, still nonclaim because both MTS coefficients are missing.
- The GR boundary-charge guard is retained: observed ADM/time/rotation charges are not deleted by the representative `R_AB` compact-proper lemma.

## Source Register
| source_id | source_path | path_exists | validation_overall_pass | role |
| --- | --- | --- | --- | --- |
| SRC2246_0_2245_doc | 2245-Y5-R2FR-RAB-boundary-charge-QR-Kboundary-zero-or-beta-bound-first-row.md | True |  | current R2FR boundary-charge handoff |
| SRC2246_1_2245_validation | source-intake/mts_residuals/P8_Y5_BRR545_2245_VALIDATION.csv | True | True | current R2FR boundary-charge handoff |
| SRC2246_2_2245_next | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2245_NEXT_TARGET.csv | True |  | current R2FR boundary-charge handoff |
| SRC2246_3_2245_lemma | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2245_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv | True |  | current R2FR boundary-charge handoff |
| SRC2246_4_2245_projection | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2245_FIRST_BETA_PROJECTION_TEMPLATE.csv | True |  | current R2FR boundary-charge handoff |
| SRC2246_5_1040_doc | 1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md | True |  | older B_X/Q_X formula scaffold being specialized to R_AB |
| SRC2246_6_1040_validation | source-intake/mts_residuals/P8_Y5_BRR545_1040_VALIDATION.csv | True | True | older B_X/Q_X formula scaffold being specialized to R_AB |
| SRC2246_7_1040_formula | source-intake/mts_residuals/P8_Y5_R10_1040_PARENT_BOUNDARY_CHARGE_FORMULA.csv | True |  | older B_X/Q_X formula scaffold being specialized to R_AB |
| SRC2246_8_1040_owner_gate | source-intake/mts_residuals/P8_Y5_R10_1040_BX_OWNER_GATE.csv | True |  | older B_X/Q_X formula scaffold being specialized to R_AB |
| SRC2246_9_1040_alpha3 | source-intake/mts_residuals/P8_Y5_R10_1040_ALPHA3_PROJECTION_COEFFICIENT_TEMPLATE.csv | True |  | older B_X/Q_X formula scaffold being specialized to R_AB |
| SRC2246_10_667_variation | source-intake/mts_residuals/P8_Y5_R10_667_VARIATION_LEDGER.csv | True |  | boundary formula, owner, exactness, or alpha3 provenance evidence |
| SRC2246_11_668_owner | source-intake/mts_residuals/P8_Y5_R10_668_SECTOR_OWNER_AUDIT.csv | True |  | boundary formula, owner, exactness, or alpha3 provenance evidence |
| SRC2246_12_591_dc | source-intake/mts_residuals/P8_Y5_R10_591_DC_OPERATOR_FORMULA.csv | True |  | boundary formula, owner, exactness, or alpha3 provenance evidence |
| SRC2246_13_584_owner_repair | source-intake/mts_residuals/P8_Y5_R10_584_OWNER_REPAIR_ATTEMPT.csv | True |  | boundary formula, owner, exactness, or alpha3 provenance evidence |
| SRC2246_14_584_edge_law | source-intake/mts_residuals/P8_Y5_R10_584_EDGE_ENVELOPE_LAW.csv | True |  | boundary formula, owner, exactness, or alpha3 provenance evidence |
| SRC2246_15_671_owner_gate | source-intake/mts_residuals/P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv | True |  | boundary formula, owner, exactness, or alpha3 provenance evidence |
| SRC2246_16_1019_exactness | source-intake/mts_residuals/P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv | True |  | boundary formula, owner, exactness, or alpha3 provenance evidence |
| SRC2246_17_976_alpha3 | source-intake/mts_residuals/P8_Y5_R10_976_K_BOUNDARY_ALPHA3_SOURCE_ACQUISITION.csv | True |  | boundary formula, owner, exactness, or alpha3 provenance evidence |
| SRC2246_18_977_alpha3_status | source-intake/mts_residuals/P8_Y5_R10_977_K_BOUNDARY_ALPHA3_STATUS.csv | True |  | boundary formula, owner, exactness, or alpha3 provenance evidence |
| SRC2246_19_local_bounds | source-intake/local_bounds/local_bound_claims.csv | True |  | external local bound or runner ledger |
| SRC2246_20_r10_candidate | source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | True |  | external local bound or runner ledger |
| SRC2246_21_r10_runner | scripts/R10_alpha_lambda_bound_prediction_runner.py | True |  | external local bound or runner ledger |

## Parent Boundary Charge Formula
| formula_id | object | formula | derivation_status | owner_status | claim_effect |
| --- | --- | --- | --- | --- | --- |
| BRF2246_0_bulk_pairing | boundary pairing from D C_R | delta int_Sigma epsilon_AB C_R^AB contains - int_partialSigma n_mu epsilon_AB delta P_R^{mu AB} plus convention-dependent density terms | DERIVED_FROM_DCR_CONTRACT | P_R and density convention not parent-owned | identifies the boundary charge density that must be cancelled, exact, or bounded |
| BRF2246_1_candidate_charge_density | B_R surface density | B_R^AB = sigma n_mu P_R^{mu AB} + B_ct^AB + B_ref^AB + B_exact^AB, with sigma fixed by the G_bulk +/- Q convention | FORMULA_SHAPE_DERIVED_SIGN_CONVENTION_OPEN | P_R, counterterm, reference subtraction, and exact primitive missing | turns edge charge into a concrete coefficient contract rather than an undefined coupling |
| BRF2246_2_candidate_QR | Q_R boundary charge | Q_R[epsilon] = int_partialSigma epsilon_AB B_R^AB dS | CONTRACT_READY_NOT_PARENT_SIGNED | requires Theta_R/L_R sector owner and allowed boundary class | proper compact branch gives zero; source/large branch remains scoreable residual |
| BRF2246_3_exactness_route | exact/pure boundary repair | B_R = d_boundary b_R + B_R^pure and int_partialSigma epsilon d_boundary b_R = int_partialpartialSigma epsilon b_R - int_partialSigma d_boundary epsilon b_R | MATHEMATICAL_ROUTE_ONLY | b_R, harmonic sector, corner terms, and kernel derivative term not derived | exactness can close only with boundary-class and range-kernel conditions |
| BRF2246_4_verdict | parent B_R/Q_R formula status | B_R/Q_R formula shape is explicit, but parent ownership is not closed | FORMULA_CONTRACT_BUILT_FULL_CLAIM_BLOCKED | MISSING_PARENT_LR_THETAR_PR_REFERENCE_PROJECTOR | move to parent source row or alpha3/R10 nonclaim coefficient rows |

## B_R Owner Gate
| gate_id | needed_object | closure_test | current_status | if_missing |
| --- | --- | --- | --- | --- |
| BRG2246_0_LR_owner | parent L_R sector | L_R[g,R_AB,nabla R_AB] explicitly selected with field normalization and boundary class | MISSING_SECTOR_LAGRANGIAN_OWNER | Theta_R and P_R remain formal placeholders |
| BRG2246_1_ThetaR_owner | parent symplectic potential Theta_R | delta L_R = E_R delta R + d Theta_R(delta R) with finite boundary jet order | MISSING_THETA_R | Q_R differentiability and K_boundary bracket cannot be computed |
| BRG2246_2_PR_owner | boundary momentum P_R^{mu AB} | P_R is derived from L_R or parent variation, not inserted as a free tensor | MISSING_PR_OWNER | B_R=n.P_R is a contract only |
| BRG2246_3_density_convention | tensor versus densitized P convention | choose C_R=-nabla P_R+J or C_R=-(1/sqrt(g))partial Ptilde_R+J before scoring signs/units | CONVENTION_GATE_OPEN | B_R sign, volume terms, and units are ambiguous |
| BRG2246_4_source_boundary_class | allowed non-proper source boundary class | source worldtube, reference surface, and compact exterior boundary classes are separated | MISSING_SOURCE_BOUNDARY_CLASS | proper-gauge zero may be incorrectly promoted to a source/test theorem |
| BRG2246_5_verdict | claim-grade B_R owner package | BRG2246_0 through BRG2246_4 pass together | FAIL_CURRENT_CLAIM_BR_NOT_PARENT_OWNED | keep B_R/Q_R rows as nonclaim coefficient contracts |

## Reference/Projector Split
| split_id | sector | rule | missing | claim_status |
| --- | --- | --- | --- | --- |
| RPS2246_0_observed_GR_charge | observed EH/ADM/time/rotation charge | retain in Q_obs and do not force to zero by representative-R_AB proper-domain choice | Pi_EH/Pi_M reference action on the full gravitational boundary charge | GUARD_ONLY |
| RPS2246_1_representative_R_charge | proper compact representative-R_AB charge | Q_R^proper=0 from 2245 collar lemma | extension to non-proper/source boundary values | NARROW_ZERO_ONLY |
| RPS2246_2_edge_source_projection | edge/source residual charge | Qbar_edge_RH(lambda)=Pi_M^H[int_partialSigma F_lambda epsilon_AB B_R^AB]/M_H | Pi_M^H, F_lambda, B_R owner, source boundary class, units | RETAIN_NONCLAIM_RESIDUAL |
| RPS2246_3_no_double_count | bulk plus edge source split | alpha_total uses orthogonal split or absolute addition; no cancellation credit between bulk and edge rows | projection orthogonality proof or numeric split | RETAIN_ABSOLUTE_TAIL_POLICY |

## K_boundary Cocycle Contract
| cocycle_id | object | formula | needed_inputs | current_status |
| --- | --- | --- | --- | --- |
| KBC2246_0_contract | boundary cocycle | K_boundary[epsilon,eta]=delta_eta Q_R[epsilon]-delta_epsilon Q_R[eta]-Q_R[[epsilon,eta]] plus possible i_veta i_vepsilon Omega_boundary convention terms | differentiable G_R, parent Omega_Y, v_R action on all fields, sign convention | FORMULA_CONTRACT_ONLY |
| KBC2246_1_proper_zero | proper compact cocycle | K_boundary=0 when epsilon, eta, and required finite jets vanish on the boundary collar | same finite-jet boundary class as 2245 | NARROW_ZERO_INHERITED |
| KBC2246_2_source_alpha3 | preferred-frame flux projection | alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local | K_boundary_alpha3, Phi_boundary_local, projection normalization | SOURCE_ANCHOR_READY_COEFFICIENTS_MISSING |

## Alpha3 Projection Coefficient Template
| projection_id | observable | mts_formula | external_bound | units | reference | coefficient_bound_rule | current_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A3P2246_0_formula | alpha3 | alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local | 4e-20 | dimensionless | local_bound_claims.csv / Will 2014 PPN alpha3 anchor | if Phi_boundary_local is numeric and nonzero, \|K_boundary_alpha3\| <= 4e-20/\|Phi_boundary_local\| | COEFFICIENT_RULE_WRITTEN_PHI_AND_K_MISSING |
| A3P2246_1_theorem_zero_route | alpha3 | alpha3_MTS = 0 if K_boundary_alpha3=0 or Phi_boundary_local=0 from a parent theorem | 4e-20 | dimensionless | local_bound_claims.csv / Will 2014 PPN alpha3 anchor | theorem-zero must cite B_R exactness/no-flux or boundary flux amplitude zero | THEOREM_ZERO_NOT_SIGNED |
| A3P2246_2_numeric_route | alpha3 | \|K_boundary_alpha3 * Phi_boundary_local\| <= 4e-20 | 4e-20 | dimensionless | local_bound_claims.csv / Will 2014 PPN alpha3 anchor | requires source-backed K, Phi, normalization, uncertainty policy, and no-cancellation tail addition | NUMERIC_ROUTE_INPUTS_MISSING |

## R10 Edge Input Contract
| edge_id | symbol | formula | missing_inputs |
| --- | --- | --- | --- |
| R10E2246_0_Qbar_edge | Qbar_edge_RH(lambda) | Pi_M^H[int_partialSigma F_lambda(s) epsilon_AB B_R^AB(s) dS]/M_H | B_R owner; F_lambda; Pi_M^H; source boundary class; units |
| R10E2246_1_alpha_edge | alpha_edge(lambda) | alpha_edge(lambda)=K_edge(lambda) Qbar_edge_RH(lambda) qbar_RT(lambda) | K_edge; Qbar_edge_RH; qbar_RT; lambda support; promoted R10 bound curve |

## MTS Alpha Smoke Template
| model_id | template_branch | lambda_value | alpha_predicted | force_law_form | derivation_status |
| --- | --- | --- | --- | --- | --- |
| MTS_source_normalized_Newton_branch | BR_QR_formula_contract | MISSING_SOURCE_BOUNDARY_CLASS | MISSING_BR_OWNER_AND_EDGE_PROJECTION | Q_R[epsilon]=int_partialSigma epsilon_AB(sigma n_mu P_R^{mu AB}+B_ct^AB+B_ref^AB+B_exact^AB)dS | template_invalid_formula_shape_not_parent_owned |
| MTS_source_normalized_Newton_branch | boundary_alpha3_projection_bound_rule | MISSING_NOT_R10_RANGE | MISSING_K_BOUNDARY_ALPHA3_TIMES_PHI_BOUNDARY_LOCAL | alpha3_MTS=K_boundary_alpha3 Phi_boundary_local; \|K\|<=4e-20/\|Phi\| if Phi is sourced nonzero | template_invalid_alpha3_coefficients_missing |
| MTS_source_normalized_Newton_branch | R10_edge_contract | MISSING_EDGE_LAMBDA_SUPPORT | MISSING_KEDGE_QBAR_EDGE_QBAR_RT | alpha_edge(lambda)=K_edge(lambda) Qbar_edge_RH(lambda) qbar_RT(lambda) | template_invalid_edge_inputs_missing |

## Runner Smoke Status
| smoke_id | valid_mts_rows | valid_bound_rows | comparison_rows | R10_pass_for_claim | claim_allowed | expected_result |
| --- | --- | --- | --- | --- | --- | --- |
| SMOKE2246_0_runner_status | 0 | 0 | 1 | False | False | blocked_nonclaim |

## Placeholder Refusal Runner
| refusal_id | object | current_status | refusal_status | failure_reasons | score_eligible | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| REF2246_BRF_0_bulk_pairing | boundary pairing from D C_R | DERIVED_FROM_DCR_CONTRACT | formula_not_claim_promoted | P_R and density convention not parent-owned | False | False |
| REF2246_BRF_1_candidate_charge_density | B_R surface density | FORMULA_SHAPE_DERIVED_SIGN_CONVENTION_OPEN | formula_not_claim_promoted | P_R, counterterm, reference subtraction, and exact primitive missing | False | False |
| REF2246_BRF_2_candidate_QR | Q_R boundary charge | CONTRACT_READY_NOT_PARENT_SIGNED | formula_not_claim_promoted | requires Theta_R/L_R sector owner and allowed boundary class | False | False |
| REF2246_BRF_3_exactness_route | exact/pure boundary repair | MATHEMATICAL_ROUTE_ONLY | formula_not_claim_promoted | b_R, harmonic sector, corner terms, and kernel derivative term not derived | False | False |
| REF2246_BRF_4_verdict | parent B_R/Q_R formula status | FORMULA_CONTRACT_BUILT_FULL_CLAIM_BLOCKED | formula_not_claim_promoted | MISSING_PARENT_LR_THETAR_PR_REFERENCE_PROJECTOR | False | False |
| REF2246_BRG_0_LR_owner | parent L_R sector | MISSING_SECTOR_LAGRANGIAN_OWNER | owner_gate_failed | Theta_R and P_R remain formal placeholders | False | False |
| REF2246_BRG_1_ThetaR_owner | parent symplectic potential Theta_R | MISSING_THETA_R | owner_gate_failed | Q_R differentiability and K_boundary bracket cannot be computed | False | False |
| REF2246_BRG_2_PR_owner | boundary momentum P_R^{mu AB} | MISSING_PR_OWNER | owner_gate_failed | B_R=n.P_R is a contract only | False | False |
| REF2246_BRG_3_density_convention | tensor versus densitized P convention | CONVENTION_GATE_OPEN | owner_gate_failed | B_R sign, volume terms, and units are ambiguous | False | False |
| REF2246_BRG_4_source_boundary_class | allowed non-proper source boundary class | MISSING_SOURCE_BOUNDARY_CLASS | owner_gate_failed | proper-gauge zero may be incorrectly promoted to a source/test theorem | False | False |
| REF2246_BRG_5_verdict | claim-grade B_R owner package | FAIL_CURRENT_CLAIM_BR_NOT_PARENT_OWNED | owner_gate_failed | keep B_R/Q_R rows as nonclaim coefficient contracts | False | False |
| REF2246_A3P_0_formula | alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local | COEFFICIENT_RULE_WRITTEN_PHI_AND_K_MISSING | alpha3_projection_not_scoreable | if Phi_boundary_local is numeric and nonzero, \|K_boundary_alpha3\| <= 4e-20/\|Phi_boundary_local\| | False | False |
| REF2246_A3P_1_theorem_zero_route | alpha3_MTS = 0 if K_boundary_alpha3=0 or Phi_boundary_local=0 from a parent theorem | THEOREM_ZERO_NOT_SIGNED | alpha3_projection_not_scoreable | theorem-zero must cite B_R exactness/no-flux or boundary flux amplitude zero | False | False |
| REF2246_A3P_2_numeric_route | \|K_boundary_alpha3 * Phi_boundary_local\| <= 4e-20 | NUMERIC_ROUTE_INPUTS_MISSING | alpha3_projection_not_scoreable | requires source-backed K, Phi, normalization, uncertainty policy, and no-cancellation tail addition | False | False |
| REF2246_R10E_0_Qbar_edge | Qbar_edge_RH(lambda) | B_R owner; F_lambda; Pi_M^H; source boundary class; units | R10_edge_row_not_scoreable | B_R owner; F_lambda; Pi_M^H; source boundary class; units | False | False |
| REF2246_R10E_1_alpha_edge | alpha_edge(lambda) | K_edge; Qbar_edge_RH; qbar_RT; lambda support; promoted R10 bound curve | R10_edge_row_not_scoreable | K_edge; Qbar_edge_RH; qbar_RT; lambda support; promoted R10 bound curve | False | False |

## Claim Gates
| gate_id | claim | gate_pass | reason | claim_allowed |
| --- | --- | --- | --- | --- |
| CGATE2246_0_BR_formula | B_R/Q_R is parent-derived | False | formula shape is explicit, but L_R, Theta_R, P_R, density convention, reference terms, and boundary class are not parent-owned | False |
| CGATE2246_1_local_GR_boundary | full local-GR boundary silence is closed | False | proper compact silence remains narrow; non-proper/source boundary and projection rows remain active | False |
| CGATE2246_2_alpha3 | alpha3 projection row is executable | False | source-backed alpha3 bound exists but K_boundary_alpha3 and Phi_boundary_local are missing | False |
| CGATE2246_3_R10_edge | R10 edge contract is score-ready | False | K_edge, Qbar_edge_RH, qbar_RT, lambda support, and promoted bound curve are missing | False |

## Decision Ledger
| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DEC2246_0_formula_status | B_R/Q_R is now a concrete formula contract, not a vague missing coupling. | D C_R boundary pairing fixes the required surface density up to sign/density/reference conventions | select or derive the parent L_R/Theta_R/P_R package, or retain the formula as a nonclaim coefficient contract |
| DEC2246_1_alpha3_status | alpha3 has a usable bound rule but no MTS coefficient yet. | \|K_boundary_alpha3 Phi_boundary_local\| <= 4e-20 is the exact scoring inequality once K and Phi exist | derive theorem-zero for K/Phi or source numeric values with normalization |
| DEC2246_2_next_target | Next target should try to source the parent R_AB-sector symplectic potential. | Theta_R is the upstream object that would fix P_R, B_R, differentiability, K_boundary, and the alpha3 projection coefficient | 2247-Y5-R2FR-RAB-parent-R-sector-ThetaR-PR-owner-or-boundary-coefficient-prior.md |

## Next Target
| next_target | script | objective | include | exclude |
| --- | --- | --- | --- | --- |
| 2247-Y5-R2FR-RAB-parent-R-sector-ThetaR-PR-owner-or-boundary-coefficient-prior.md | scripts/Y5_R2FR_RAB_parent_R_sector_ThetaR_PR_owner_or_boundary_coefficient_prior_2247.py | try to derive or select the parent R_AB-sector symplectic potential Theta_R and momentum P_R that own B_R; if this cannot close, create nonclaim priors/templates for K_boundary_alpha3 and Phi_boundary_local | candidate L_R blocks, delta L_R, Theta_R, P_R tensor/density convention, boundary finite-jet order, no-flux theorem-zero route, alpha3 coefficient prior schema | invented numeric K/Phi values, deleting GR charges, naked linear c_g scoring, cancellation between residuals, R10/local-GR pass claim, formalization-workbench edits, GitHub action |

## Branch Copies
| copy_id | source_path | target_path | copied | parse_ok |
| --- | --- | --- | --- | --- |
| queue_formula | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2246_PARENT_BOUNDARY_CHARGE_FORMULA.csv | source-intake/rab-sector/acquisition-queue/JR2246_PARENT_BR_QR_FORMULA_NONCLAIM.csv | True | True |
| queue_alpha3 | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2246_ALPHA3_PROJECTION_COEFFICIENT_TEMPLATE.csv | source-intake/rab-sector/acquisition-queue/JR2246_ALPHA3_COEFFICIENT_RULE_NONCLAIM.csv | True | True |
| branch_wep | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2246_ALPHA3_PROJECTION_COEFFICIENT_TEMPLATE.csv | source-intake/microscope/branch_locked_wep/residuals/parent_BR_QR_alpha3_nonclaim_2246.csv | True | True |
| beta_docs | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2246_ALPHA3_PROJECTION_COEFFICIENT_TEMPLATE.csv | source-intake/beta-source/docs/PARENT_BR_QR_ALPHA3_2246_NONCLAIM.csv | True | True |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL2246_00_sources_exist | PASS | all direct and registered 2246 source paths exist |
| VAL2246_01_prior_validations | PASS | 2245 and 1040 validations pass overall |
| VAL2246_02_BR_formula_contract | PASS | B_R/Q_R formula contract is written but not parent-promoted |
| VAL2246_03_owner_gates_fail_safely | PASS | owner gates identify missing L_R/Theta_R/P_R package |
| VAL2246_04_reference_projector_guard | PASS | reference/projector split protects GR charges and keeps edge residual separate |
| VAL2246_05_cocycle_contract | PASS | K_boundary cocycle and alpha3 projection contracts are present |
| VAL2246_06_alpha3_bound_rule | PASS | alpha3 coefficient bound rule uses source-backed anchor but remains nonclaim |
| VAL2246_07_R10_edge_contract_nonclaim | PASS | R10 edge contract remains nonclaim and non-scoreable |
| VAL2246_08_mts_template_nonclaim | PASS | MTS smoke template has no claim-valid rows |
| VAL2246_09_runner_smoke_refuses_claim | PASS | runner smoke status refuses a claim |
| VAL2246_10_claim_gates_blocked | PASS | all empirical/local-GR claim gates remain blocked |
| VAL2246_11_next_target_written | PASS | next target row is present |
| VAL2246_12_csv_parse | PASS | all generated 2246 CSVs parse cleanly |
| VAL2246_13_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL2246_14_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL2246_15_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL2246_16_formalization_no_2246 | PASS | formalization-workbench has no non-venv 2246 artifacts |
| VAL2246_17_formalization_untouched | PASS | formalization-workbench untouched during 2246 run |
| VAL2246_OVERALL | PASS | 2246 builds the R_AB B_R/Q_R boundary-charge formula contract, blocks parent ownership claims, writes alpha3/R10 edge nonclaim bounds, and selects Theta_R/P_R ownership next |

## Working Interpretation

This is good movement: the boundary problem is no longer a nameless crack in the wall. It is now a named surface density `B_R` with explicit missing owners. That means the next step is not to guess a number for `K_boundary_alpha3`; it is to derive or select the `R_AB` sector symplectic potential `Theta_R` and momentum `P_R`. If those close, no-pole gets stronger. If they do not, the alpha3/R10 edge rows stay as honest bounded residuals.

