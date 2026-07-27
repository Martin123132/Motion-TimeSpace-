# 602 Y5 R10 bound-domain selector or compact-shell unit-map fill

Generated: 2026-06-05T18:32:03.208090+00:00  
Status: `Y5_R10_bound_domain_selector_conditional_variation_written_parent_primitive_missing_unit_map_still_unfilled`  
Claim ceiling: `conditional_selector_theorem_attempt_only_no_q_loc_zero_R10_WEP_PPN_or_local_GR_pass`  
Next target: `603-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill.md`  
Run root: `runs/20260605-183203-Y5-R10-bound-domain-selector-or-compact-shell-unit-map-fill`

## Verdict
- A real conditional selector theorem can be written: if a parent scalar/topological primitive `N_D` exists, then `chi_D=N_D` plus a `p>=2` memory gate makes local `N_D=0` branches silent without adding hidden selector stress.
- This is better than the old domain-window problem because the missing object is now exact: derive `N_D` from projected MTS boundary/current/coherent determinant data, or demote the route.
- The derivation is not complete. Current MTS has not parent-derived `N_D`, `P_MTS,D`, local trivial relative class, boundary charge silence, or R11 source-normalization silence.
- The compact-shell proxy `7.432631961576971e-06` remains non-claim and unscored; unit-map fill is still the fallback, not the default.

## Selector Theorem Attempt
The candidate action is:

```text
S_D = integral sqrt(-g) lambda_D(chi_D - N_D)
    + integral sqrt(-g) chi_D^p L_mem,D
    + S_top[P_MTS,D,J_B],
with p >= 2.
```

The useful local consequence is:

```text
N_local = 0 -> chi_local = 0 -> lambda_local = 0 -> no bulk selector/memory stress.
```

The useful FLRW consequence is:

```text
N_FLRW > 0 -> chi_FLRW > 0 -> coherent expansion memory may remain active.
```

That is a proper theorem skeleton. It is not yet a parent theorem because `N_D` is not derived.

## Source Register
| source_file | exists | role |
| --- | --- | --- |
| 601-Y5-R10-relative-Hodge-projector-or-compact-shell-unit-map.md | True | immediate 601 handoff |
| source-intake/mts_residuals/P8_Y5_BRR545_601_VALIDATION.csv | True | prior validation gate |
| source-intake/mts_residuals/P8_Y5_R10_601_RELATIVE_HODGE_PARENT_OWNERSHIP.csv | True | relative-Hodge parent ownership blocker |
| source-intake/mts_residuals/P8_Y5_R10_601_COMPACT_SHELL_UNIT_MAP_SPEC.csv | True | unit-map fallback contract |
| 60-relative-cohomology-boundary-contract.md | True | local-zero/FLRW-nonzero relative class contract |
| 61-bound-domain-boundary-theorem-attempt.md | True | volume-flow identity and stationary bound-domain partial theorem |
| 62-domain-field-chiD-action-contract.md | True | chi_D selector action obligations |
| 63-chiD-variation-to-boundary-equation-attempt.md | True | advection is not selection failure |
| 64-binding-invariant-domain-selector-attempt.md | True | C_coh/C_exp kinematic separator |
| 67-auxiliary-selector-parent-contract.md | True | no-independent-stress auxiliary selector route |
| 143-domain-selector-variational-action-attempt.md | True | zero-knob action attempt and auxiliary C_coh route |
| 416-binding-invariant-domain-selector-repair.md | True | C_exp repair and unresolved threshold/Bianchi gates |
| 475-domain-selector-parent-action-clause-or-coefficient-fill.md | True | double-zero parent-action clause |
| 476-double-zero-memory-coupling-origin-or-coefficient-runner.md | True | p>=2 local-silence requirement |
| 478-determinant-current-parent-ownership-or-demotion.md | True | det(Q_coh) as best double-zero/current clue |
| scripts/Y5_R10_bound_domain_selector_or_compact_shell_unit_map_fill.py | True | this checkpoint generator |

## Bound-Domain Selector Derivation Attempt
| step_id | object | mathematical_form | derivation_attempt | local_effect_if_true | FLRW_effect_if_true | current_status | blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BDS602_0_parent_selector_primitives | N_D and chi_D | chi_D = N_D, with N_D a scalar/topological norm of the MTS projected boundary-memory class | Replace an empirical domain window with a parent scalar N_D built from b_D, c_D, C_exp, or det(Q_coh) only after projection by P_MTS,D. | closed/gapped or exact local branch gives N_D=0 and chi_D=0 | coherent expansion branch gives N_D>0 and chi_D>0 | candidate_primitives_identified_not_parent_derived | N_D normalization, P_MTS,D ownership, and local zero class are still conditional | false |
| BDS602_1_candidate_action | selector action | S_D = int sqrt(-g) lambda_D(chi_D-N_D) + int sqrt(-g) chi_D^p L_mem,D + S_top[P_MTS,D,J_B], p>=2 | Use the 475/476 double-zero memory gate so local chi_D=0 also forces lambda_D=0 and removes hidden selector stress. | bulk memory stress, selector force, and domain-vector leakage vanish at chi_D=0 | memory sector can remain active where chi_D>0 | conditional_sufficient_clause | the action clause is still stipulated as a sufficient construction, not derived from deeper MTS variables | false |
| BDS602_2_variation_lambda | lambda_D variation | delta_lambda S_D = 0 -> chi_D - N_D = 0 | The selector is no longer chosen after a fit; it is tied to a predeclared scalar/topological source. | if parent proves N_local=0, the local branch is forced to chi_local=0 | if parent proves N_FLRW>0, FLRW is not silenced | formal_variation_pass_if_ND_owned | N_D itself remains the unowned primitive | false |
| BDS602_3_variation_chi | chi_D variation | delta_chi S_D = 0 -> lambda_D + p chi_D^(p-1)L_mem,D + chi_D^p partial_chi L_mem,D = 0 | For p>=2 and chi_local=0, lambda_local=0 follows without tuning. | constraint stress and memory stress vanish together in the local branch | lambda_D and memory stress may be nonzero in active coherent domains | formal_double_zero_pass | p>=2 is derived as a requirement, not as a parent-origin theorem | false |
| BDS602_4_boundary_embedding_variation | boundary level set or embedding | delta_X S_top -> n_mu P_MTS,D J_B^mu = 0 for trivial/exact local class, or retained topological charge for nontrivial class | A positive projected boundary-current norm has natural no-flux boundary equations on the trivial class instead of hand-drawn local collars. | stationary local compact shells get projected memory-boundary no-flux | nontrivial expansion class is not forced into the local no-flux representative | conditional_boundary_Euler_route | actual topological/boundary projector and variational domain labels are not parent-owned | false |
| BDS602_5_volume_flow_readout | coherent volume-memory channel | d ln V_D/dtau = <theta>_D; local chi_D=0 projects Q_coh off, while FLRW chi_D>0 keeps d ln V_D/dtau=3H | Feed the 61 volume-flow identity through the auxiliary selector rather than declaring a plateau. | local scalar volume-memory channel is silent in the selected bound domain | FLRW coherent expansion remains active | conditional_selector_theorem_if_BDS602_0_to_4_hold | does not prove observed q_loc=0 or kill harmonic/source/R11 rows | false |

## Local-FLRW Branch Gate
| gate_id | requirement | current_result | reason | blocking_issue | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| LFG602_0_no_empirical_window | selector cannot use residuals, PPN success, SPARC fits, or cosmology fits | pass_contract | N_D is restricted to parent scalar/topological/boundary-current ingredients | ingredient ownership still missing | false |
| LFG602_1_local_zero | compact stationary local domains force N_D=0 | not_parent_derived | closed/gapped b_D=0 and exact/trivial c_D=0 remain conditional from 308/309/601 | local spectral gap or trivial relative class theorem | false |
| LFG602_2_FLRW_active | coherent FLRW domains force N_D>0 and retain expansion memory | conditional_support | C_exp/det(Q_coh) give the right active shape, but Q_coh projection is not parent-owned | parent-owned Q_coh/P_coh and normalization | false |
| LFG602_3_no_selector_stress | local branch has chi_D=lambda_D=0 and no bulk selector stress | formal_if_p_ge_2_and_Nlocal_zero | double-zero memory gate kills the old linear-selector stress leak | p>=2 origin and Nlocal=0 are not parent-derived together | false |
| LFG602_4_boundary_charge | boundary/topological charge either vanishes locally or is routed to residuals | not_derived_route_retained | boundary Euler route is conditional and 582/601 keep edge charges alive | momentum-map/edge-charge/nohair certificate | false |
| LFG602_5_R11_source_normalization | domain source-normalization operators are zero or executable | blocked | 475/476/478 keep R11 source-normalization as a separate blocker | R11 zero-or-fill | false |

## Unit-Map Fork Status
| fork_id | route | status | why | required_next_input | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| UMF602_0_derivation_priority | continue selector derivation before scoring | preferred_next | BDS602 gives a sharper parent primitive target N_D; scoring before this would be closure-only | derive N_D from parent boundary/current variables or explicitly demote | false |
| UMF602_1_unit_map_not_filled | compact-shell unit map | deferred_still_blocked | proxy 7.432631961576971e-06 still has no observable channel, coefficient, sign, range, or units | choose R10 alpha(lambda), PPN vector, WEP, or clock channel if N_D route stalls | false |
| UMF602_2_no_score | local-bound evidence | no_claim | 602 is a derivation attempt, not a data/score pass | source-backed coefficient rows or accepted theorem-zero gates | false |

## Runner Update
| runner_id | previous_status | new_status | reason | still_needed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RU602_0_bound_domain_selector | parent_selected_stationary_bound_domain_missing | conditional_selector_variation_written | an auxiliary scalar/topological selector can force chi_local=0 if N_local=0 and p>=2 | parent derivation of N_D and local zero/FLRW active branch | false |
| RU602_1_relative_Hodge_route | parent_ownership_not_derived | blocked_on_ND_and_P_MTS_ownership | relative-Hodge/projector ownership needs the same parent projector/domain machinery | parent-owned P_MTS,D, relative complex, and boundary inner product | false |
| RU602_2_q_loc_zero | observed_q_loc_still_open | still_open | selector theorem would silence coherent volume/domain leakage only under premises; harmonic/source/R11/boundary pieces remain | q_loc exchange-owner terms zeroed or bounded row by row | false |
| RU602_3_compact_shell_unit_map | fallback_spec_written_not_filled | still_unfilled | derivation route remains live enough to attack N_D first | observable channel and coefficient if N_D cannot be parent-derived | false |

## Decision
| decision_id | decision | meaning | claim_status | next_target |
| --- | --- | --- | --- | --- |
| D602_0_conditional_selector_theorem | accept BDS602 as a conditional theorem skeleton | if N_D is parent-owned and local N_D=0 while FLRW N_D>0, the auxiliary p>=2 selector gives local scalar-domain silence without a plateau axiom | conditional_not_promoted | 603-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill.md |
| D602_1_missing_key | do not claim parent selector derivation | the real missing key is now N_D: a parent scalar/topological primitive that owns b_D/c_D/C_exp/det(Q_coh) and its normalization | no_claim | 603-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill.md |
| D602_2_unit_map_deferred | defer compact-shell unit-map fill one more step | the derivation path gained a sharper target, so scoring remains fallback rather than the next default | blocked_until_filled | 603-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill.md |
| D602_3_no_local_GR | forbid local-GR/PPN/R10 promotion | q_loc, R11, boundary charge, and source-normalization rows remain open | forbidden | 603-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill.md |

## Route Update
| route_id | allowed_after_602 | forbidden_after_602 | next_action |
| --- | --- | --- | --- |
| RU602_0_allowed | try to derive N_D as a parent primitive from projected boundary current/coherent determinant data | treat N_D as an empirical threshold or arena label | 603-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill.md |
| RU602_1_allowed | use p>=2 auxiliary selector as a sufficient local-stress-silence clause | claim the p>=2 clause has parent origin | 603-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill.md |
| RU602_2_allowed | switch to unit-map scoring if N_D parent origin fails | score compact-shell proxy without observable channel and unit conversion | 603-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill.md |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V602_0_source_paths_exist | pass | missing=0 |
| V602_1_prior_601_clean | pass | prior_rows=8;prior_failures=0;hodge_rows=5;unit_rows=6 |
| V602_2_selector_variation_written | pass | selector_rows=6;double_zero_visible=True |
| V602_3_ND_parent_blocker_visible | pass | N_D primitive/normalization/projector ownership not parent-derived |
| V602_4_local_FLRW_split_not_smuggled | pass | local_zero_not_claimed=True;FLRW_retained=True |
| V602_5_q_loc_and_unit_map_still_open | pass | q_loc_open=True;unit_map_unfilled=True;proxy=7.432631961576971e-06 |
| V602_6_no_claim_rows | pass | claim_rows=0 |
| V602_7_no_R10_or_local_GR_claim | pass | claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false |

## Practical Read
This is a decent move. Not checkmate, but definitely not flailing. The selector problem has been converted from "how do we choose the local box?" into "derive the scalar/topological primitive `N_D`." If `N_D` can be owned by the parent action, the local/FLRW split becomes a theorem-shaped thing rather than a hand switch. If it cannot, we stop punching the same wall and go to the unit-map scorer.
