# 2517 - c_R2 Effective Coefficient Owner Split and First-Term Zero/Bound

**Current verdict:** `c_R2_eff` is now split into named limbs. The bare higher-curvature limb `c_bare` is not parent-zeroed because the current parent normal-form grammar still retains `c_HD` unless a stronger derivative-grammar/no-extension theorem is supplied.

**Main gain:** this avoids circling the same R2/f(R) theorem. The next work can attack one coefficient limb at a time: bare slot, hidden Schur term, measure, boundary, and frame/readout transfer.

**Claim discipline:** no R2/f(R), scalaron, beta, gamma, R10, EH, Newton, local-GR, WEP, clock, orbit, or conservation claim is made.

## Source Register
| source_id | source_path | path_exists | found_needles | source_pass | role |
| --- | --- | --- | --- | --- | --- |
| SRC2517_0_2516_next | source-intake/mts_residuals/P8_Y5_NO_SHADOW_2516_NEXT_TARGET.csv | True | NEXT2516_0_selected;c_R2_eff | True | authoritative handoff to c_R2_eff component split |
| SRC2517_1_2516_scalaron | source-intake/mts_residuals/P8_Y5_NO_SHADOW_2516_R2FR_SCALARON_MAP.csv | True | SC2516_0_effective_coefficient;c_bare | True | effective coefficient law from the current branch |
| SRC2517_2_2516_zero_attempt | source-intake/mts_residuals/P8_Y5_NO_SHADOW_2516_R2FR_ZERO_THEOREM_ATTEMPT.csv | True | R2Z2516_4_effective_coefficient_guard;ZERO_SIGNATURE_REFINED_NOT_SIGNED | True | no-cancellation guard for the full coefficient |
| SRC2517_3_2485_normal_form | source-intake/local_bounds/Parent_normal_form_contract_2485_NONCLAIM.csv | True | NF2485_0_parent_action_skeleton;sum_i c_i O_i | True | parent action skeleton retains residual operator slots |
| SRC2517_4_2485_coeff_slots | source-intake/local_bounds/Parent_coefficient_slot_ledger_2485_NONCLAIM.csv | True | CS2485_2_c_HD;RETAIN_NONCLAIM | True | higher-curvature coefficient slot remains retained |
| SRC2517_5_2485_derivative_grammar | 2485-Y5-R2FR-parent-normal-form-field-symmetry-derivative-grammar.md | True | DG2485_3_higher_curvature;RETAIN_AS_c_HD | True | derivative grammar says higher-curvature terms need forbid-or-bound owner |
| SRC2517_6_964_countermodel | 964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md | True | CM964_0_EH_plus_R2;THEOREM_NOT_PROVEN_CURRENT_CORPUS | True | EH plus epsilon R^2 remains legal without a parent no-extension theorem |
| SRC2517_7_2509_loop_guard | 2509-Y5-R2FR-parent-constructor-exhaustion-from-MTS-primitives-or-source-weight-residual-pivot.md | True | PARENT_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED_PIVOT_REQUIRED;LOOP_GUARD_ENFORCED | True | do not restate constructor exhaustion as if it zeroed coefficients |
| SRC2517_8_2516_validation | source-intake/mts_residuals/P8_Y5_BRR545_2516_VALIDATION.csv | True | VAL2516_OVERALL;PASS | True | previous checkpoint validation gate |

## c_R2_eff Component Split
| component_id | symbol | definition | required_zero_owner | current_status | next_action |
| --- | --- | --- | --- | --- | --- |
| CR2C2517_0_cbare | c_bare | bare local higher-curvature coefficient written directly in the parent public-geometry action | parent derivative grammar excludes R^2, f_extra(R), R Box R, and higher-curvature public operators except topological/boundary combinations | NOT_ZEROED_RETAIN_FINITE_ROW | attempt c_bare zero theorem first; otherwise keep finite row |
| CR2C2517_1_hidden_vertex | 1/2 B^T L^-1 B | integrated-out hidden, memory, fibre, or auxiliary curvature-linear vertex contribution | B_X=0 or L^-1 decoupling/theorem-zero for every hidden curvature-linear vertex | OPEN_NEXT_AFTER_CBARE | attack hidden curvature vertex after c_bare row |
| CR2C2517_2_measure | c_measure | Jacobian, measure, local subtraction, or field-redefinition curvature-square residue | measure/readout/redefinition identity proving no observable residual | OPEN_RETAINED | defer until c_bare and hidden vertex are classified |
| CR2C2517_3_boundary | c_boundary | boundary, corner, topological, reference, or no-flux leakage into the local operator | boundary class/topological/no-flux theorem including metric variation and source readout | OPEN_RETAINED | defer to boundary/projector branch if not zeroed earlier |
| CR2C2517_4_frame | c_frame | observed-frame, coframe, conformal/disformal or readout transfer residue that mimics an f(R) coefficient | single observed coframe/frame-transfer theorem with variation-before-readout order | OPEN_RETAINED | defer to observed-frame/readout branch after coefficient rows are split |
| CR2C2517_5_total | c_R2_eff | componentwise effective coefficient entering scalaron range and Yukawa/PPN maps | all components zeroed individually or by a sourced Ward/topological identity; no cancellation by preference | MISSING_COMPONENT_VALUES_OR_ZERO_THEOREMS | fill each limb in order |

## c_bare Zero Attempt
| attempt_id | claim_attempted | result | logic | blocking_gap |
| --- | --- | --- | --- | --- |
| CBZ2517_0_target | prove c_bare=0 from parent derivative grammar | TARGET_DEFINED | c_bare is zero if the parent object language has no public higher-curvature operator slot beyond EH, Lambda and harmless topological/boundary terms | 2485 still writes sum_i c_i O_i and keeps c_HD retained |
| CBZ2517_1_allowed_operator_inventory | restrict public local geometry to a0+a1 R only | CONDITIONAL_ROUTE_IDENTIFIED_NOT_SIGNED | a strict derivative grammar plus local metric-only second-order premise would exclude R^2 and generic f(R) | derivative grammar is a contract, not a derived parent action inventory |
| CBZ2517_2_constructor_exhaustion | use ParentGenerate exhaustion to make c_bare unformable | REJECTED_LOOP_GUARD | if c_bare is not in Image(ParentGenerate[q(Phi),theta,topological/universal data]), then it cannot appear | 2509 says ParentGenerate membership/no-extension is not derived and should not be repeated without new source |
| CBZ2517_3_topological_exception | allow only topological/boundary higher-curvature combinations | SAFE_EXCEPTION_NOT_CURRENT_ROW | a precise 4D Gauss-Bonnet/boundary class could be harmless if variation/readout silence is proved | current R2/f(R) row is generic scalar curvature-square/f_extra(R), not a sourced topological combination |
| CBZ2517_4_countermodel | exclude EH + epsilon R^2 | COUNTERMODEL_REMAINS_LEGAL | S = S_EH + epsilon int sqrt(-g) R^2 respects locality, 4D covariance and metric-only structure while violating second-order EH unless epsilon=0 | no parent no-extension/minimality theorem forbids epsilon |
| CBZ2517_5_verdict | set c_bare=0 as MTS-owned | CBARE_ZERO_NOT_DERIVED_CURRENT_CORPUS | conditional theorem is exact, but current evidence retains the c_HD/c_bare slot | create finite c_bare row and move to hidden curvature vertex limb |

## c_bare Finite Row
| row_id | quantity | required_units | required_value_or_formula | current_status | observable_links |
| --- | --- | --- | --- | --- | --- |
| CBFIN2517_0_cbare_value | c_bare | length^2 or inverse_mass_squared after EH normalization | numeric value or exact zero theorem with source path | MISSING_NUMERIC_OR_THEOREM_ZERO | R10;PPN_gamma;PPN_beta |
| CBFIN2517_1_normalization | EH normalization | declared a1/kappa convention | coefficient must be normalized relative to the parent EH term a1 R | MISSING_A1_KAPPA_OWNER | Newton;PPN;scalaron_mass |
| CBFIN2517_2_sign | sign(c_bare) | dimensionless sign with stability convention | positive simple R+cR2 branch gives non-tachyonic scalaron; negative requires explicit stability treatment | MISSING_SIGN_AND_STABILITY_BRANCH | R10;stability;local_branch |
| CBFIN2517_3_scalar_map | m_s;lambda_s;alpha_s | eV/meters/dimensionless | m_s^2=1/(6c_bare) only if c_bare dominates c_R2_eff and simple unscreened metric-f(R) branch applies | MISSING_COMPONENT_DOMINANCE_AND_REGIME | R10_alpha_lambda;gamma |
| CBFIN2517_4_beta_map | delta_beta_cbare | dimensionless | second-order scalar/source/readout map in fixed observed-GM convention | MISSING_SECOND_ORDER_BETA_MAP | PPN_beta_bound_7.8e-05 |
| CBFIN2517_5_source_path | provenance | path/URL plus assumptions | source path for coefficient, normalization, units and branch regime | MISSING_SOURCE_PATH | all_future_scoring |

## No-Cancellation Gate
| gate_id | policy | forbidden_move | allowed_exception | status |
| --- | --- | --- | --- | --- |
| NC2517_0_componentwise | evaluate c_R2_eff by componentwise zero or bound rows | set c_bare + hidden + measure + boundary + frame = 0 by tuning | sourced Ward/topological/redefinition identity with source path and readout proof | ACTIVE |
| NC2517_1_hidden_vertex | do not cancel c_bare against B^T L^-1 B | use opposite signs without parent identity | derived Schur-complement identity or positive/zero theorem for each piece | ACTIVE |
| NC2517_2_boundary_measure | measure and boundary terms cannot silently remove public curvature residues | call them gauge/topological without variation/readout silence | boundary class plus no-flux plus variation-before-readout theorem | ACTIVE |
| NC2517_3_claim | no local-GR or scalaron score from an unsigned component split | treat bookkeeping as evidence of a pass | all components have real zero/bound rows and comparator maps | ACTIVE |

## Dry Run
| case_id | case_description | result_status | blocking_markers | pass_fail |
| --- | --- | --- | --- | --- |
| DRY2517_0_derivative_taste | set c_bare=0 because higher derivatives are ugly | REFUSED_NO_DERIVATIVE_BY_TASTE | MISSING_PARENT_DERIVATIVE_GRAMMAR_SIGNATURE | BLOCKED_NONCLAIM |
| DRY2517_1_EH_import | use EH target branch to delete c_bare | REFUSED_EH_IMPORT_AS_COEFFICIENT_OWNER | EH_PREMISES_UNSIGNED;C_HD_RETAINED | BLOCKED_NONCLAIM |
| DRY2517_2_constructor_loop | repeat ParentGenerate exhaustion without new source | REFUSED_LOOP_GUARD | PARENT_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED | BLOCKED_NONCLAIM |
| DRY2517_3_finite_score | score finite c_bare row without value, units or beta/gamma/R10 map | REJECTED_MISSING_FINITE_INPUTS | MISSING_VALUE;MISSING_UNITS;MISSING_MAPS;MISSING_SOURCE_PATH | BLOCKED_NONCLAIM |
| DRY2517_4_component_cancellation | cancel c_bare against hidden/measure/boundary/frame terms | REFUSED_UNSOURCED_CANCELLATION | NO_CANCELLATION_GATE_ACTIVE | BLOCKED_NONCLAIM |
| DRY2517_5_future_complete_template | future c_bare row has theorem-zero or sourced numeric coefficient and maps | WOULD_ACCEPT_SCHEMA_IF_REAL_VALUES_AND_FILES_EXIST | CURRENT_ROW_STILL_MISSING_REAL_INPUTS | BLOCKED_NONCLAIM |

## Decision Ledger
| decision_id | decision | rationale | status |
| --- | --- | --- | --- |
| DEC2517_0_split | CR2_EFFECTIVE_COMPONENT_SPLIT_LOCKED | c_R2_eff is now split into c_bare, hidden Schur term, measure, boundary and frame limbs with separate owners. | retained_tooling |
| DEC2517_1_cbare | CBARE_ZERO_NOT_DERIVED | 2485 still retains c_HD and 964's EH+R2 countermodel remains legal without a stronger parent derivative grammar. | claim_blocked |
| DEC2517_2_finite | CBARE_FINITE_ROW_STAGED_NONCLAIM | If c_bare survives, it needs value, units, sign, normalization, scalaron maps, beta map and source path before any scoring. | selected_nonclaim |
| DEC2517_3_next | ATTACK_HIDDEN_CURVATURE_VERTEX_NEXT | The next largest limb is the integrated-out hidden/memory/fibre term B^T L^-1 B, which can regenerate R2 even if c_bare is absent. | selected |
| DEC2517_4_claim | NO_CBARE_R2FR_OR_LOCAL_GR_CLAIM | No component has a claim-ready zero theorem or finite value; this checkpoint is coefficient discipline only. | enforced |

## Next Target
| route_id | selection_status | target_file | target_script | objective | success_condition | do_not_do |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2517_0_selected | selected | 2518-Y5-R2FR-hidden-curvature-vertex-BTLinvB-zero-or-finite-row.md | scripts/Y5_R2FR_hidden_curvature_vertex_BTLinvB_zero_or_finite_row_2518.py | try to prove every hidden/memory/fibre curvature-linear vertex B_X vanishes or decouples; if not, create finite B_X, L_X, Z_X, M_X rows with units and observable maps | B^T L^-1 B term is theorem-zero or each retained vertex has finite nonclaim coefficient, operator inverse/range, units, source path and R10/PPN/Qnorm link | do not assume c_bare=0 closes R2/f(R), do not cancel Schur terms by hand, and do not score symbolic B_X rows |
| NEXT2517_1_reentry | reentry_only_if_new_source | 2517b-Y5-R2FR-parent-derivative-grammar-new-source-reentry.md | scripts/Y5_R2FR_parent_derivative_grammar_new_source_reentry_2517b.py | reopen c_bare zero only if a new source proves the parent derivative grammar excludes higher curvature from the constructor image | new source path proves c_HD is unformable rather than retained | do not repeat 2485/2509/964 conditionals as fresh evidence |

## Validation
| check_id | status | detail |
| --- | --- | --- |
| VAL2517_00_sources_exist | PASS |  |
| VAL2517_01_source_needles | PASS |  |
| VAL2517_02_component_split | PASS | c_R2_eff limbs are explicit |
| VAL2517_03_cbare_not_zeroed | PASS | bare higher-curvature zero theorem remains unsigned |
| VAL2517_04_finite_row_rejects | PASS | finite c_bare rows are schema-only |
| VAL2517_05_no_cancellation_gate | PASS | component cancellation is forbidden without a parent identity |
| VAL2517_06_dryruns_block_claims | PASS | dry run rejects derivative-taste, EH import, loop and cancellation routes |
| VAL2517_07_next_target | PASS | hidden curvature vertex selected next |
| VAL2517_08_no_claim_flags | PASS |  |
| VAL2517_09_branch_copies | PASS |  |
| VAL2517_10_no_formalization_artifacts | PASS |  |
| VAL2517_11_pycache_absent | PASS |  |
| VAL2517_CSV_P8_Y5_NO_SHADOW_2517_SOURCE_REGISTER | PASS | OK; rows=9 |
| VAL2517_CSV_P8_Y5_NO_SHADOW_2517_CR2_COMPONENT_SPLIT | PASS | OK; rows=6 |
| VAL2517_CSV_P8_Y5_NO_SHADOW_2517_CBARE_ZERO_ATTEMPT | PASS | OK; rows=6 |
| VAL2517_CSV_P8_Y5_NO_SHADOW_2517_CBARE_FINITE_ROW | PASS | OK; rows=6 |
| VAL2517_CSV_P8_Y5_NO_SHADOW_2517_NO_CANCELLATION_GATE | PASS | OK; rows=4 |
| VAL2517_CSV_P8_Y5_NO_SHADOW_2517_DRYRUN_RESULTS | PASS | OK; rows=6 |
| VAL2517_CSV_P8_Y5_NO_SHADOW_2517_DECISION_LEDGER | PASS | OK; rows=5 |
| VAL2517_CSV_P8_Y5_NO_SHADOW_2517_NEXT_TARGET | PASS | OK; rows=2 |
| VAL2517_CSV_P8_Y5_NO_SHADOW_2517_BRANCH_COPIES | PASS | OK; rows=4 |
| VAL2517_COPY_CSV_component_split | PASS | OK; rows=6 |
| VAL2517_COPY_CSV_cbare_zero_attempt | PASS | OK; rows=6 |
| VAL2517_COPY_CSV_cbare_finite_row | PASS | OK; rows=6 |
| VAL2517_COPY_CSV_next_target | PASS | OK; rows=2 |
| VAL2517_OVERALL | PASS | 2517 splits c_R2_eff, refuses c_bare zero promotion, stages finite c_bare rows, and selects hidden curvature vertex B^T L^-1 B next |
