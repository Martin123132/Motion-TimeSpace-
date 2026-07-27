# 1510 - Reviewed Figure Digitization Protocol or Return to GR Derivation

## Verdict
- Fig. 5b is local and can be digitized later, but digitization alone cannot unlock R10 because tau_R10(lambda) and parent alpha_predicted(lambda) are still missing.
- The R10 scoring branch stays frozen as nonclaim; this is a scoring freeze, not a theory failure.
- The selected next route is to return to the parent GR/Newton derivation spine and inventory the strongest local-limit artifacts.

## Digitization Protocol
| protocol_id | step | current_status |
| --- | --- | --- |
| DIG1510_0_source_lock | lock source artifact | READY_SOURCE_LOCAL |
| DIG1510_1_axis_calibration | calibrate axes | NOT_DONE |
| DIG1510_2_curve_trace | trace 2020 upper envelope | NOT_DONE |
| DIG1510_3_review_delta | review discrepancy | NOT_DONE |
| DIG1510_4_metadata | write provenance | NOT_DONE |
| DIG1510_5_tau | derive tau_R10(lambda) | NOT_DONE |
| DIG1510_6_parent_alpha | connect parent alpha_predicted(lambda) | NOT_DONE |
| DIG1510_7_acceptance | promote to live R10 curve | BLOCKED |

## Route Decision
| route_id | route | decision | cost_or_limit |
| --- | --- | --- | --- |
| ROUTE1510_0_digitize_now | reviewed R10 Fig. 5 digitization now | DEFER | still does not supply tau_R10 or parent alpha_predicted; risks token sink away from GR/Newton derivability |
| ROUTE1510_1_return_to_gr | return to parent GR/Newton derivation spine | SELECTED | R10 remains frozen until curve/tau/alpha inputs are acquired |

## Freeze Confirmation
| freeze_id | object | status | unfreeze_condition |
| --- | --- | --- | --- |
| FREEZE1510_0 | R10/local fifth-force scoring branch | FROZEN_NONCLAIM_CONFIRMED | complete reviewed digitization or supplemental table, tau kernel, and parent alpha prediction/zero theorem |

## GR/Newton Reentry Plan
| reentry_id | target | current_status | objective |
| --- | --- | --- | --- |
| GR1510_0_inventory | inventory existing EH/Newton/local-GR files | NEXT | find the strongest current parent-spine documents and residual ledgers |
| GR1510_1_parent_action | minimal parent action contract | PENDING | identify which fields remain fundamental and which must descend/decouple locally |
| GR1510_2_bianchi | Bianchi/conservation gate | PENDING | show extra residual stress is conserved, constrained, or zero in local branch |
| GR1510_3_eh_limit | Einstein-Hilbert local limit | PENDING | derive when the metric sector reduces to EH/Levi-Civita dynamics |
| GR1510_4_newton_limit | Newton/PPN weak-field limit | PENDING | derive Poisson equation, PPN residual vector, and zero/bound conditions |
| GR1510_5_reopen_tests | reopen empirical local tests | PENDING | only after parent GR/Newton branch supplies alpha/PPN residual predictions |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1510_0_sources | PASS | all cited 1509 and R10 figure source paths exist |
| VAL1510_1_fig_available | PASS | Fig. 5b source artifact is local and nonempty |
| VAL1510_2_protocol_blocks_live | PASS | digitization acceptance remains blocked until reviewed steps close |
| VAL1510_3_route_selected | PASS | return-to-GR/Newton route selected |
| VAL1510_4_r10_frozen | PASS | R10 scoring freeze confirmed |
| VAL1510_5_gr_next | PASS | GR reentry inventory is the next derivation action |
| VAL1510_6_live_targets_absent | PASS | live R10 curve/kernel files remain absent |
| VAL1510_7_csv_parse | PASS | all generated 1510 CSVs parse cleanly |
| VAL1510_8_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1510_9_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1510_10_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1510_11_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1510_12_overall | PASS | 1510 froze R10 scoring, preserved a reviewed digitization protocol, and selected GR/Newton derivation reentry |

## Next Target
| next_id | next_target | script | objective |
| --- | --- | --- | --- |
| NEXT1510_0_1511 | 1511-Y5-parent-GR-Newton-reentry-spine-inventory-and-strongest-local-limit-contract.md | scripts/Y5_parent_GR_Newton_reentry_spine_inventory_and_strongest_local_limit_contract.py | inventory the strongest existing EH/Newton/local-GR derivation artifacts, extract the minimal local-limit contract, and select the next derivation target |
