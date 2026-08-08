# 1513 - Parent Primitive Minimality / No-Higher-Derivative Theorem or R11 Vector Lock

## Verdict
- The primitive minimality/no-natural-marker theorem still does not close: fixed spurions are conditionally excluded, but covariant material markers and local invariant generators remain live.
- Therefore the higher-curvature/R2-fR leak is not theorem-zero; the non-EH R11 vector is now the active local operator branch until each family is zeroed or bounded.
- The next derivation target is local invariant generator elimination, starting with the domain selector chi_D / projector branch.

## Primitive Theorem Audit
| attempt_id | theorem_piece | current_status | consequence |
| --- | --- | --- | --- |
| PM1513_0_target | primitive minimal parent object | NOT_DERIVED | covariant extensions remain legal |
| PM1513_1_fixed_spurion | fixed active labels | CONDITIONAL_PASS_IF_STRICT_QUOTIENT | kills only fixed labels, not transforming markers |
| PM1513_2_no_natural_marker | no-natural-marker functor | NOT_DERIVED | finite-cell spectra, domain/class data, memory scalars, species constants remain admissible |
| PM1513_3_local_invariant_algebra | local invariant algebra triviality | NOT_DERIVED | extra generators can source marker-prefactors or local residuals |
| PM1513_4_no_integrated_tower | no integrated-out higher-curvature tower | NOT_DERIVED | EH+R2 and auxiliary scalar countermodels remain legal |
| PM1513_5_second_order_activation | activate R2/fR relative zero theorem | RELATIVE_THEOREM_EXISTS_ABSOLUTE_PREMISE_UNSIGNED | R2/fR zero cannot promote |
| PM1513_6_verdict | primitive minimality/no-higher-derivative theorem | THEOREM_NOT_PROVEN_CURRENT_CORPUS | lock R11 vector as active local operator branch |

## Local Invariant Generator Lock
| generator_id | generator | local_status | blocks_no_marker |
| --- | --- | --- | --- |
| GEN1513_0_observed_geometry | observed geometry jets J^k(e_obs) | ALLOWED_GEOMETRY | False |
| GEN1513_1_universal_constants | universal constants | ALLOWED_IF_SOURCE_INDEPENDENT | False |
| GEN1513_2_finite_cell_spectrum | finite-cell/fibre spectrum | NOT_ELIMINATED | True |
| GEN1513_3_domain_selector | domain selector chi_D | NOT_ELIMINATED | True |
| GEN1513_4_memory_class_scalar | memory/class scalar | NOT_ELIMINATED | True |
| GEN1513_5_species_constants | species constants theta_A(I_Q) | NOT_ELIMINATED | True |
| GEN1513_6_orientation_time_arrow | orientation/time-arrow marker | NOT_CLASSIFIED | True |
| GEN1513_7_readout_projector | post-readout projector/reduced-action marker | POLICY_BLOCKED_NOT_THEOREM_BLOCKED | True |
| GEN1513_8_boundary_topological_marker | boundary/topological marker | CONDITIONALLY_SAFE_NOT_DERIVED | True |
| GEN1513_9_verdict | I_loc(Q_MTS)=I_geom plus constants | NOT_DERIVED | True |

## Countermodel Ledger
| counter_id | countermodel | current_status | required_blocker |
| --- | --- | --- | --- |
| CM1513_0_EH_plus_R2 | S=S_EH+epsilon int sqrt(-g) R^2 | LIVE | parent second-order/minimality theorem |
| CM1513_1_auxiliary_scalar | hidden auxiliary scalar integrated out into f(R) | LIVE | no-integrated-out-tower theorem |
| CM1513_2_marker_prefactor | F(sigma)R with quotient-invariant scalar sigma | LIVE | local invariant algebra triviality |
| CM1513_3_comoving_marker | co-moving material marker m varied with matter | LIVE | primitive universal-property no-extension theorem |
| CM1513_4_domain_selector | domain selector chi_D in local/cosmology split | LIVE | domain selector theorem |
| CM1513_5_nonlocal_memory | R Box^-1 R or history kernel | LIVE | compact-local memory silence theorem |
| CM1513_6_topological_marker | boundary/topological marker | CONDITIONALLY_SAFE | topological stress-free no-flux theorem |

## R2/fR Higher-Curvature Status
| status_id | object | current_status | claim_effect |
| --- | --- | --- | --- |
| R2FR1513_0_relative_zero | R2/fR scalar-mode zero theorem | RELATIVE_THEOREM_ONLY | cannot set c_R2=c_fR=0 until primitive minimality/second-order premise is parent-signed |
| R2FR1513_1_finite_branch | finite R2/fR scalar branch | NONCLAIM_RUNNER_ONLY | no R10/PPN/local-GR score |
| R2FR1513_2_operator_branch | higher-curvature leakage | LOCK_IN_R11_VECTOR | EH operator remains conditional |

## R11 Vector Lock
| lock_id | operator_family | lock_status |
| --- | --- | --- |
| R11LOCK1513_00 | boundary_topological_terms | ACTIVE_LOCAL_OPERATOR_BRANCH_UNTIL_ZERO_OR_BOUND |
| R11LOCK1513_01 | R2_fR_scalar_mode | ACTIVE_LOCAL_OPERATOR_BRANCH_UNTIL_ZERO_OR_BOUND |
| R11LOCK1513_02 | Ricci_Weyl_squared | ACTIVE_LOCAL_OPERATOR_BRANCH_UNTIL_ZERO_OR_BOUND |
| R11LOCK1513_03 | scalar_tensor_class_metric | ACTIVE_LOCAL_OPERATOR_BRANCH_UNTIL_ZERO_OR_BOUND |
| R11LOCK1513_04 | vector_preferred_frame | ACTIVE_LOCAL_OPERATOR_BRANCH_UNTIL_ZERO_OR_BOUND |
| R11LOCK1513_05 | torsion_nonmetricity | ACTIVE_LOCAL_OPERATOR_BRANCH_UNTIL_ZERO_OR_BOUND |
| R11LOCK1513_06 | bulk_X_force_law | ACTIVE_LOCAL_OPERATOR_BRANCH_UNTIL_ZERO_OR_BOUND |
| R11LOCK1513_07 | nonlocal_memory_kernel | ACTIVE_LOCAL_OPERATOR_BRANCH_UNTIL_ZERO_OR_BOUND |
| R11LOCK1513_08 | source_normalization_operator | ACTIVE_LOCAL_OPERATOR_BRANCH_UNTIL_ZERO_OR_BOUND |
| R11LOCK1513_09 | projector_domain_stress | ACTIVE_LOCAL_OPERATOR_BRANCH_UNTIL_ZERO_OR_BOUND |

## Operator Branch Decision
| decision_id | decision | result |
| --- | --- | --- |
| DEC1513_0_minimality | primitive minimality/no-higher-derivative theorem not proven | NO_EH_OPERATOR_PROMOTION |
| DEC1513_1_R11_lock | lock non-EH vector as active local operator branch | R11_VECTOR_ACTIVE |
| DEC1513_2_next | attack local invariant generators directly | NEXT_1514_GENERATOR_ELIMINATION |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1513_0_sources | PASS | all cited minimality/no-marker/R11 source paths exist |
| VAL1513_1_theorem_not_proven | PASS | primitive minimality theorem remains explicitly unproven |
| VAL1513_2_live_generators | PASS | local invariant generator blockers remain live |
| VAL1513_3_live_countermodels | PASS | live countermodels remain recorded |
| VAL1513_4_r2fr_locked | PASS | R2/fR higher-curvature leakage is locked into R11 vector |
| VAL1513_5_r11_locked | PASS | R11 vector lock covers at least 10 operator families |
| VAL1513_6_next_generator | PASS | next target attacks generator elimination |
| VAL1513_7_csv_parse | PASS | all generated 1513 CSVs parse cleanly |
| VAL1513_8_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1513_9_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1513_10_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1513_11_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1513_12_overall | PASS | 1513 refused primitive-minimality overclaim, locked the R11 vector, and selected local invariant generator elimination next |

## Next Target
| next_id | next_target | script | objective |
| --- | --- | --- | --- |
| NEXT1513_0_1514 | 1514-Y5-parent-local-invariant-generator-elimination-or-domain-selector-lock.md | scripts/Y5_parent_local_invariant_generator_elimination_or_domain_selector_lock.py | attack the surviving local invariant generators directly, starting with the domain selector chi_D / projector branch; prove it is geometry/gauge/constant/silent, or lock it as an explicit R11 residual family |
