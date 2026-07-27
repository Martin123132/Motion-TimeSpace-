# 1120 - Domain Alpha3 Factor Ledger Zero Chain Or Numeric Source Pack

**Current verdict:** domain `alpha3` is now factorized but not closed. The row is no longer one mystery number; it is a product/sum of specific debts: gate origin, flux, weak-field weight, and R11 source leakage.

**Best next move:** kill or fill the R11 leakage factor first. It remains live even when the selector-vector route is conditionally quiet, and it directly touches the `4e-20` alpha3 bound.

**No claim:** no domain `alpha3` pass, no local-GR/R10 safety, and no numeric source-pack pass follows from 1120.

## Source Register
| source_id | relative_path | exists | needle | needle_found | note |
| --- | --- | --- | --- | --- | --- |
| SRC1120_0_1119_next | source-intake/mts_residuals/P8_Y5_R10_1119_NEXT_TARGET.csv | true | NEXT1119_0_1120 | true | 1119 handoff to domain alpha3 factor ledger. |
| SRC1120_1_1119_premises | source-intake/mts_residuals/P8_Y5_R10_1119_DOMAIN_ALPHA3_PREMISE_LEDGER.csv | true | A3P1119_3_R11_source | true | R11 source premise fails current corpus. |
| SRC1120_2_1119_fills | source-intake/mts_residuals/P8_Y5_R10_1119_DOMAIN_ALPHA3_PRODUCT_FILL_ROWS_NONCLAIM.csv | true | A3F1119_0_alpha3_product | true | alpha3 product fill row is missing. |
| SRC1120_3_double_zero | source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv | true | O6_verdict | true | p>=2 double-zero origin is not parent-derived. |
| SRC1120_4_no_vector | source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv | true | T2_no_flux_local_representative | true | local flux zero is conditional not parent-derived. |
| SRC1120_5_r11_zero | source-intake/mts_residuals/R11_DOMAIN_SOURCE_THEOREM_ZERO_ATTEMPT.csv | true | Z6_verdict | true | R11 domain source zero is rejected. |
| SRC1120_6_alpha3_link | source-intake/mts_residuals/P8_DOMAIN_ALPHA3_R11_LINK.csv | true | L2_alpha3_flux | true | alpha3 flux link is missing highest pressure. |
| SRC1120_7_vector_coeffs | source-intake/mts_residuals/P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv | true | W_domain_alpha3_epsilon_domain_flux | true | weak-field alpha3 coefficient is not scoreable. |
| SRC1120_8_1118_candidate | source-intake/mts_residuals/P8_Y5_R10_1118_R11_DOMAIN_CANDIDATE_ROWS_NONCLAIM.csv | true | W_domain_alpha3_epsilon_domain_flux | true | 1118 alpha3/domain leakage candidate row remains missing. |

## Factor Ledger
| factor_id | factor | role | formula_piece | zero_route | numeric_route | current_status | highest_priority | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FAC1120_0_total | P_domain_alpha3 | total alpha3 domain contribution | W_domain_alpha3 * epsilon_domain_flux + P_R11_source_alpha3 | all factors zero by parent theorem | abs(total)<=4e-20 with source-backed value | MISSING_TOTAL_PRODUCT_OR_THEOREM_ZERO | true | false |
| FAC1120_1_p_ge_2 | p>=2 domain/memory gate origin | removes linear local activation and first-derivative domain coupling | f(0)=0 and f'(0)=0 | derive double-zero from parent determinant/current, norm-square, or topological pairing | if not derived, retain domain/memory coupling width | REQUIREMENT_KNOWN_BUT_ORIGIN_NOT_PARENT_DERIVED | false | false |
| FAC1120_2_flux | epsilon_domain_flux | projected domain flux feeding alpha3 | P_loc^i_mu F_D^mu | derive compact exact/trivial local representative and no active coherent FLRW memory class | source-backed flux coefficient with units/map | CONDITIONAL_NOT_PARENT_DERIVED | true | false |
| FAC1120_3_weight | W_domain_alpha3 | weak-field map from domain flux/source leakage into PPN alpha3 | alpha3_domain = W_domain_alpha3 * epsilon_domain_flux | derive W=0 from parent weak-field map | source-backed W coefficient; no unity shortcut | MISSING_NUMERIC_WEIGHT_OR_THEOREM_ZERO | true | false |
| FAC1120_4_R11_source | c_domain_source_normalization_operator | R11 source-normalization leakage into alpha3/local source | P_R11_source_alpha3 | derive c_domain_source_normalization_operator=0 | canonical executable R11 row with source-backed coefficient | FAIL_CURRENT_CORPUS | true | false |
| FAC1120_5_projector_stress | projector/domain STF or stress leakage | additional R7/R8/R11 leakage if projector/domain stress is not topological zero | delta_g P_D, delta_g chi_D, or domain-wall/readout-mask stress | derive parent-owned metric-independent topological projector | source-backed projector stress coefficient | CONDITIONAL_NOT_PARENT_OWNED | false | false |

## Attack Order
| attack_id | factor | recommended_order | why | derive_attempt | fallback_fill | current_verdict | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATK1120_0_R11_first | c_domain_source_normalization_operator | 1 | 1118 already shows this is the hard failed clause and it can leak into alpha3 even when vector/flux routes are quiet | prove EH-only/local-boundary silence or parent-owned R11 source zero | canonical R11 source-normalization row with coefficient, units, normalization, weak-field map, source path | NOT_DERIVED_NEEDS_ZERO_OR_EXECUTABLE_ROW | false |
| ATK1120_1_flux | epsilon_domain_flux | 2 | if flux is theorem-zero, W factor becomes irrelevant for alpha3 product | prove compact exact/trivial local representative and no coherent local memory class | numeric projected flux coefficient | CONDITIONAL_NOT_PARENT_DERIVED | false |
| ATK1120_2_weight | W_domain_alpha3 | 3 | needed only if flux survives; cannot be set to unity | derive weak-field alpha3 map coefficient from parent perturbation theory | numeric weak-field map coefficient with source path | MISSING_NUMERIC_WEIGHT_OR_THEOREM_ZERO | false |
| ATK1120_3_p_ge_2 | p>=2 gate origin | 4 | important for broad domain/memory silence, but alpha3 still blocked by R11 even if p>=2 holds | derive double-zero origin from determinant/current, norm-square, or topological pairing | finite domain/memory coupling width | REQUIREMENT_KNOWN_BUT_ORIGIN_NOT_PARENT_DERIVED | false |

## Numeric Source Pack
| pack_id | row | required_quantity | required_value | units | bound | source_requirement | current_status | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRCF1120_0_total | R7_alpha3 | P_domain_alpha3 | numeric or theorem-zero | dimensionless PPN alpha3 convention | 4e-20 | source-backed total product or theorem-zero certificate | MISSING | false |
| SRCF1120_1_R11 | R7/R11 | P_R11_source_alpha3 or c_domain_source_normalization_operator | numeric or theorem-zero | dimensionless mapped alpha3 contribution or declared operator units | combined <=4e-20 | canonical executable R11 coefficient row | MISSING | false |
| SRCF1120_2_flux | R7_alpha3 | epsilon_domain_flux | numeric or theorem-zero | dimensionless projected flux convention | inherited through product | local representative theorem or measured/sourced flux coefficient | MISSING | false |
| SRCF1120_3_weight | R7_alpha3 | W_domain_alpha3 | numeric or theorem-zero | dimensionless weak-field coefficient | inherited through product | parent weak-field map derivation/source | MISSING | false |
| SRCF1120_4_gate | domain/memory gate | p>=2 origin | parent theorem | not applicable | zero-chain premise | determinant/current, norm-square, or topological-pairing parent derivation | MISSING_PARENT_ORIGIN | false |

## Claim Gates
| gate_id | claim | gate_pass | reason | claim_allowed |
| --- | --- | --- | --- | --- |
| CG1120_0_factorized | alpha3 factorization is explicit | true_nonclaim | factor ledger separates total product, flux, weight, R11 leakage, gate origin, and projector stress | false |
| CG1120_1_zero_chain | alpha3 zero chain is derived | false | R11 source zero, local flux zero, p>=2 origin, and projector ownership are not all parent-derived | false |
| CG1120_2_numeric_pack | numeric alpha3 source pack is score-ready | false | all factor source-pack rows remain missing | false |
| CG1120_3_local_gr | domain alpha3 permits local-GR/R10 claim | false | highest-pressure row remains blocked at 4e-20 | false |

## Decisions
| decision_id | decision | because | next_action | claim_allowed |
| --- | --- | --- | --- | --- |
| DEC1120_0_result | domain alpha3 is factorized but not closed | the product now has named factors, but no factor is claim-ready enough to score alpha3 | attack R11 source-normalization leakage first | false |
| DEC1120_1_best_next | R11 source leakage remains the first factor to kill/fill | it survives even if the domain selector is scalar/stationary and it feeds the tight alpha3 row | derive P_R11_source_alpha3=0 or fill executable R11 alpha3 leakage row | false |
| DEC1120_2_policy | no unity shortcuts for W_domain_alpha3 or flux | alpha3 has a 4e-20 target and must use sourced factors or theorem-zero | keep all factor rows nonclaim until real values or proofs exist | false |

## Validation
| check_id | result | detail | valid_for_claim |
| --- | --- | --- | --- |
| V1120_0_sources_exist | pass | all cited local source paths exist and needles are found | false |
| V1120_1_factor_coverage | pass | key alpha3 factors are covered | false |
| V1120_2_r11_first | pass | R11 source leakage is first attack | false |
| V1120_3_source_pack_missing | pass | source-pack rows remain missing-input nonclaim rows | false |
| V1120_4_bound_explicit | pass | alpha3 4e-20 bound is explicit | false |
| V1120_5_gates_blocked | pass | claim gates remain blocked except nonclaim factorization | false |
| V1120_6_no_claim_rows | pass | all generated rows remain nonclaim | false |
| V1120_7_next_target | pass | 1121 handoff targets domain alpha3 R11 leakage | false |
| V1120_8_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work | false |
| V1120_9_csv_parse | pass | all 1120 CSV outputs parse cleanly | false |
| V1120_10_formalization_untouched | pass | generator writes no outputs under formalization-workbench | false |
| V1120_SUMMARY | pass | 1120 factorizes domain alpha3 and prioritizes R11 leakage kill/fill | false |

## Next Target
| next_id | next_target | objective | include | exclude | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| NEXT1120_0_1121 | 1121-Y5-R10-domain-alpha3-R11-leakage-zero-or-executable-row.md | attack the R11 source leakage factor first: derive P_R11_source_alpha3=0/c_domain_source_normalization_operator=0, or build one canonical executable R11 alpha3 leakage row | P_R11_source_alpha3; c_domain_source_normalization_operator; R11 schema; units; normalization; weak-field map; target 4e-20; source path | symbolic product pass; Ward/Bianchi shortcut; local-GR claim; tau=1; source-unity; GitHub; formalization edits | false |
