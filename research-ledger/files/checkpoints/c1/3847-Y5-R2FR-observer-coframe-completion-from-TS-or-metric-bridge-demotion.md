# 3847 - Observer Coframe Completion From T,S Or Metric Bridge Demotion

Private checkpoint. This tests whether the old `T,S` observer map can become the concrete 4D coframe needed by the 3846 metric bridge. It does not claim local GR or adopt the 3845 action.

Generated: `2026-07-01T03:44:08+00:00`

## Result

The static spherical coframe completion is:

`theta^0=c_* T dt; theta^1=sqrt(S) dr; theta^2=r dtheta; theta^3=r sin(theta) dphi`.

The metric is:

`g_obs=-(theta^0)^2+(theta^1)^2+(theta^2)^2+(theta^3)^2`,

so the line element is:

`ds^2=-c_*^2 T(r)^2 dt^2 + S(r) dr^2 + r^2 dOmega^2`.

This is a genuine constructive step: the bridge is no longer abstract `tau,h`; it has a concrete local exterior coframe branch. But it remains nonclaim because T,S and the angular area-radius gauge still need parent ownership, and metric existence alone does not derive the dynamics of `T(r)` and `S(r)`.

## Source Register

| source_id | path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC3847_0_3846_doc | 3846-Y5-R2FR-MTS-to-visible-metric-bridge-or-action-candidate-reject.md | True | True | input_for_observer_coframe_completion_from_TS |
| SRC3847_1_3846_theorem | source-intake\mts_residuals\P8_Y5_R2FR_3846_METRIC_BRIDGE_THEOREM.csv | True | True | input_for_observer_coframe_completion_from_TS |
| SRC3847_2_3846_ownership | source-intake\mts_residuals\P8_Y5_R2FR_3846_MTS_PRIMITIVE_OWNERSHIP_AUDIT.csv | True | True | input_for_observer_coframe_completion_from_TS |
| SRC3847_3_3846_residuals | source-intake\mts_residuals\P8_Y5_R2FR_3846_CONNECTION_READOUT_RESIDUALS.csv | True | True | input_for_observer_coframe_completion_from_TS |
| SRC3847_4_3846_next | source-intake\mts_residuals\P8_Y5_R2FR_3846_NEXT_TARGET.csv | True | True | input_for_observer_coframe_completion_from_TS |
| SRC3847_5_3846_validation | source-intake\mts_residuals\P8_Y5_BRR545_3846_VALIDATION.csv | True | True | input_for_observer_coframe_completion_from_TS |
| SRC3847_6_3845_doc | 3845-Y5-R2FR-visible-metric-parent-action-candidate-from-MTS-or-Lovelock-failure.md | True | True | input_for_observer_coframe_completion_from_TS |
| SRC3847_7_3845_action | source-intake\mts_residuals\P8_Y5_R2FR_3845_VISIBLE_ACTION_CANDIDATE.csv | True | True | input_for_observer_coframe_completion_from_TS |
| SRC3847_8_observer_contract | 10-observer-map-symplectic-contract.md | True | True | input_for_observer_coframe_completion_from_TS |
| SRC3847_9_cell_derivation | 09-hamiltonian-radial-cell-derivation.md | True | True | input_for_observer_coframe_completion_from_TS |
| SRC3847_10_943_coframe | source-intake\mts_residuals\P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv | True | True | input_for_observer_coframe_completion_from_TS |

## Coframe Completion

| row_id | object | formula | status | result |
| --- | --- | --- | --- | --- |
| OCF3847_0_time_leg | theta^0 | theta^0=c_* T dt | EXACT_SPHERICAL_BRANCH_LEG | tau_time=T dt and theta^0=c_* tau_time |
| OCF3847_1_radial_leg | theta^1 | theta^1=sqrt(S) dr | EXACT_SPHERICAL_BRANCH_LEG | radial h_rr=S |
| OCF3847_2_angular_legs | theta^2,theta^3 | theta^2=r dtheta; theta^3=r sin(theta) dphi | EXACT_IF_AREA_RADIUS_GAUGE_OWNED | h_angle=r^2 dOmega^2 |
| OCF3847_3_metric | g_obs | g_obs=-(theta^0)^2+(theta^1)^2+(theta^2)^2+(theta^3)^2 | EXACT_STATIC_SPHERICAL_METRIC_CANDIDATE | ds^2=-c_*^2 T(r)^2 dt^2 + S(r) dr^2 + r^2 dOmega^2 |
| OCF3847_4_bridge_match | 3846 bridge variables | tau=T dt; h=S dr^2+r^2 dOmega^2; u=T^-1 partial_t; c_*=c_* | EXACT_CONDITIONAL_BRIDGE_MATCH | 3846 metric theorem applies on the static spherical exterior domain |
| OCF3847_5_verdict | coframe completion | theta^0=c_* T dt; theta^1=sqrt(S) dr; theta^2=r dtheta; theta^3=r sin(theta) dphi | SPHERICAL_COFRAME_COMPLETED_NONCLAIM | metric bridge narrowed from abstract tau/h to an explicit spherical exterior coframe |

## Domain And Limits

| domain_id | domain_clause | condition | if_missing |
| --- | --- | --- | --- |
| OCD3847_0_static | static exterior branch | T=T(r), S=S(r), no g_ti shift, no explicit time dependence | retain B_shift_time and do not use spherical coframe as full local metric |
| OCD3847_1_area_radius | area-radius angular gauge | theta^2=r dtheta, theta^3=r sin(theta)dphi are parent/geometry-owned rather than fitted | retain B_area_radius_owner |
| OCD3847_2_positivity | Lorentzian exterior signs | T>0, S>0, r>0, 0<theta<pi | retain B_signature_domain |
| OCD3847_3_parent_owner | T,S are parent fields/readouts before local fitting | T and S are supplied by the MTS parent branch, not chosen to fit PPN coefficients | retain B_TS_parent_owner |
| OCD3847_4_scope | not full arbitrary local metric | branch is static spherical exterior only | do not overclaim global/local-GR completeness |

## Metric Bridge Update

| update_id | observable | formula | status |
| --- | --- | --- | --- |
| MBU3847_0_coframe_completion | B_tau_owner+B_h_owner+B_signature | on static spherical branch, tau=T dt and h=S dr^2+r^2 dOmega^2 satisfy the 3846 bridge if T>0,S>0 and area-radius gauge is owned | CONDITIONAL_COMPONENT_COLLAPSE |
| MBU3847_1_current_bridge_bound | B_metric_bridge | B_metric_bridge <= B_TS_parent_owner + B_area_radius_owner + B_shift_time + B_connection_LC + B_no_shadow_readout + B_general_branch_gap | REFINED_STATIC_SPHERICAL_NONCLAIM_BOUND |
| MBU3847_2_next_physics | T,S dynamics | local GR/Newton now requires field equations or parent constraints for T(r), S(r), not merely a metric bridge | NEXT_DYNAMICAL_TARGET |

## Action Candidate Update

| adoption_id | candidate | current_status | reason |
| --- | --- | --- | --- |
| ACU3847_0_action_candidate_status | 3845 visible EH action candidate | STILL_NOT_ADOPTED | T,S dynamics, parent ownership, source glue, and silent-sector clauses remain unsigned |
| ACU3847_1_if_TS_dynamics_close | local exterior GR/Newton route | CONDITIONAL_FUTURE_ADOPTION_PRESSURE | metric branch now has a concrete coframe and line element to vary/test |

## Claim Gates

| gate_id | status | claim_allowed | reason |
| --- | --- | --- | --- |
| GATE3847_0_coframe_completion | PASS_EXACT_CONDITIONAL_COMPLETION | False | theta^0,theta^1 plus angular area legs produce a Lorentzian metric candidate |
| GATE3847_1_parent_owner | BLOCKED_PARENT_OWNERSHIP_REQUIRED | False | coframe completion is exact but not signed as a parent-derived branch |
| GATE3847_2_scope | BLOCKED_STATIC_SPHERICAL_ONLY | False | this is the first exterior test branch, not arbitrary local geometry |
| GATE3847_3_dynamics | BLOCKED_FIELD_EQUATION_OR_CONSTRAINT_REQUIRED | False | metric existence alone does not derive T(r), S(r), gamma, or beta |
| GATE3847_4_no_overclaim | PASS_NO_CLAIM_PROMOTED | False | all rows remain nonclaim and scope-limited |
| GATE3847_5_next_action | PASS_ACTIONABLE_NEXT | False | the bridge has a line element; next derive or bound equations for T(r), S(r) |

## Decisions

| decision_id | decision | consequence |
| --- | --- | --- |
| DEC3847_0 | do not demote the metric bridge yet | the bridge has an exact static spherical coframe completion worth pursuing |
| DEC3847_1 | do not adopt the visible action yet | coframe existence is weaker than parent dynamics/source/action descent |
| DEC3847_2 | next target is T,S dynamics and observer-cell constraint | try to derive R_AB=ln(T^2 S)=0 or the weak-field T,S equations from MTS, otherwise keep residuals |

## Bottom Line

Do not throw this route away. The 3846 bridge now has an explicit 3847 coframe on the static spherical branch. The next hard question is dynamics: does MTS derive `R_AB=ln(T^2 S)=0`, or derive weak-field equations for `T` and `S` that reproduce Newton/gamma/beta without importing Schwarzschild?

Next target: `3848-Y5-R2FR-TS-dynamics-RAB-zero-or-weak-field-equation-bound.md`.
