# 3846 - MTS to Visible Metric Bridge Or Action Candidate Reject

Private checkpoint. This attempts the bridge demanded by 3845: can motion/time/space produce one public Lorentzian metric `g_obs` strongly enough for the visible EH action candidate? It does not adopt the action or claim local GR.

Generated: `2026-07-01T03:40:31+00:00`

## Result

The algebraic bridge works conditionally:

`g_obs_ab = h_ab - c_*^2 tau_a tau_b`

with inverse

`g_obs^ab = h^ab - c_*^-2 u^a u^b`.

If `tau_a u^a=1`, `h_ab u^b=0`, `h_ab` is positive rank-3 on `ker(tau)`, and `c_*>0`, then in the adapted basis `{u,e_i}` the metric has block form `diag(-c_*^2,h_ij)` and is Lorentzian.

This is the good news: the motion/time/space-to-metric route is mathematically coherent. The bad news, honestly stated, is that current MTS has not yet parent-signed the full 4D `tau,h,u,c_*` package, connection lock, or no-shadow motion/readout frame. So the bridge is conditionally derived but not adopted.

## Source Register

| source_id | path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC3846_0_3845_doc | 3845-Y5-R2FR-visible-metric-parent-action-candidate-from-MTS-or-Lovelock-failure.md | True | True | input_for_MTS_to_visible_metric_bridge |
| SRC3846_1_3845_metric | source-intake\mts_residuals\P8_Y5_R2FR_3845_METRIC_BRIDGE_CANDIDATE.csv | True | True | input_for_MTS_to_visible_metric_bridge |
| SRC3846_2_3845_action | source-intake\mts_residuals\P8_Y5_R2FR_3845_VISIBLE_ACTION_CANDIDATE.csv | True | True | input_for_MTS_to_visible_metric_bridge |
| SRC3846_3_3845_clause | source-intake\mts_residuals\P8_Y5_R2FR_3845_LOVELOCK_CLAUSE_TEST.csv | True | True | input_for_MTS_to_visible_metric_bridge |
| SRC3846_4_3845_eh2 | source-intake\mts_residuals\P8_Y5_R2FR_3845_EH2_IMPLICATION_UPDATE.csv | True | True | input_for_MTS_to_visible_metric_bridge |
| SRC3846_5_3845_validation | source-intake\mts_residuals\P8_Y5_BRR545_3845_VALIDATION.csv | True | True | input_for_MTS_to_visible_metric_bridge |
| SRC3846_6_observer_contract | 10-observer-map-symplectic-contract.md | True | True | input_for_MTS_to_visible_metric_bridge |
| SRC3846_7_943_coframe | source-intake\mts_residuals\P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv | True | True | input_for_MTS_to_visible_metric_bridge |
| SRC3846_8_863_coframe_zero | source-intake\mts_residuals\P8_Y5_R10_863_COFRAME_ZERO_THEOREM.csv | True | True | input_for_MTS_to_visible_metric_bridge |
| SRC3846_9_1031_terminal | source-intake\mts_residuals\P8_Y5_R10_1031_TERMINAL_PUBLIC_METRIC_PROOF_AUDIT.csv | True | True | input_for_MTS_to_visible_metric_bridge |
| SRC3846_10_1045_matter | source-intake\mts_residuals\P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv | True | True | input_for_MTS_to_visible_metric_bridge |
| SRC3846_11_1030_doc | 1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md | True | True | input_for_MTS_to_visible_metric_bridge |

## Metric Bridge Theorem

| theorem_id | claim_piece | status | result |
| --- | --- | --- | --- |
| MBT3846_0_data | metric-bridge data | EXACT_ALGEBRAIC_PREMISE | data are sufficient to test Lorentzian metric construction |
| MBT3846_1_metric | visible Lorentzian metric | EXACT_CONDITIONAL_LORENTZIAN_METRIC | g_obs is nondegenerate with signature (-,+,+,+) |
| MBT3846_2_inverse | inverse metric | EXACT_CONDITIONAL_INVERSE | g_obs^ac g_obs_cb = delta^a_b |
| MBT3846_3_coframe_special_case | observer coframe special case | EXACT_CONDITIONAL_COFRAME_EMBEDDING | the existing T,S observer-map intuition embeds into the visible metric bridge |
| MBT3846_4_connection | connection ownership | EXACT_CONDITIONAL_CONNECTION_LOCK | non-Levi-Civita leakage is a named residual C_nonLC unless parent-signed zero |
| MBT3846_5_verdict | MTS-to-visible-metric bridge | CONDITIONAL_BRIDGE_PROVED_CURRENT_OWNERSHIP_UNSIGNED | bridge theorem is proved conditionally but not adopted for current MTS |

## MTS Primitive Ownership Audit

| owner_id | object | current_status | if_unsigned |
| --- | --- | --- | --- |
| MBO3846_0_tau_time | tau_a | LOCAL_RADIAL_TEMPLATE_NOT_FULL_PARENT_OBJECT | retain B_tau_owner |
| MBO3846_1_h_space | h_ab | RADIAL_LEG_NOT_FULL_SPATIAL_TRIAD | retain B_h_owner |
| MBO3846_2_c_star | c_* | CONSTANT_OWNER_REQUIRED | retain B_c_owner |
| MBO3846_3_signature | Lorentzian signature | EXACT_CONDITIONAL_NOT_PARENT_SIGNED | retain B_signature |
| MBO3846_4_quotient_coframe | e_obs(q(Phi)) | CONDITIONAL_CHAIN_RULE_NOT_PARENT_SIGNED | retain B_coframe_descent |
| MBO3846_5_motion_frame | motion/readout congruence | READOUT_FRAME_LOCK_REQUIRED | retain B_motion_frame |
| MBO3846_6_verdict | MTS metric bridge ownership | BRIDGE_NOT_ADOPTED_CURRENT_MTS | visible action candidate remains a target, not the MTS action |

## Residuals

| residual_id | observable | formula | status |
| --- | --- | --- | --- |
| MBR3846_0_metric_bridge_total | B_metric_bridge | B_metric_bridge <= B_tau_owner + B_h_owner + B_c_owner + B_signature + B_coframe_descent + B_nonLC + B_motion_frame | CURRENT_NONCLAIM_BOUND |
| MBR3846_1_nonLC | B_nonLC | B_nonLC <= \|\|Gamma_obs - LeviCivita[g_obs]\|\|_local_ppn | RETAIN_UNTIL_CONNECTION_LOCK_SIGNED |
| MBR3846_2_motion_frame | B_motion_frame | B_motion_frame <= \|delta g_matter/g_obs\| + \|A_g(Xhat)-1\| + \|B_g(Xhat)\| | RETAIN_UNTIL_NO_SHADOW_FRAME_SIGNED |
| MBR3846_3_action_adoption | B_action_adoption | B_action_adoption <= B_metric_bridge + B_action_descent + B_matter_source + B_silent_sector | ACTION_CANDIDATE_REMAINS_NONCLAIM |

## Action Adoption Update

| adoption_id | candidate | current_status | consequence |
| --- | --- | --- | --- |
| AD3846_0_if_bridge_signed | 3845 visible EH action candidate | EXACT_CONDITIONAL_ADOPTION_STEP | metric bridge obstruction B_metric_bridge=0 and the action candidate may proceed to action-descent/source/silence tests |
| AD3846_1_current | 3845 visible EH action candidate | NOT_ADOPTED_BRIDGE_UNSIGNED | not satisfied; the action candidate remains unadopted |
| AD3846_2_reject_condition | 3845 visible EH action candidate | REJECTION_CONDITION_DEFINED_NOT_TRIGGERED | reject Lovelock/EH visible-action route or retain it as explicit closure only |

## Claim Gates

| gate_id | status | claim_allowed | reason |
| --- | --- | --- | --- |
| GATE3846_0_algebraic_bridge | PASS_EXACT_CONDITIONAL_THEOREM | False | g_obs has signature (-,+,+,+) if the MTS primitives supply the required clock/spatial data |
| GATE3846_1_MTS_ownership | BLOCKED_PARENT_OWNERSHIP_CERTIFICATES_REQUIRED | False | radial T,S coframe exists, but full 4D tau/h/c ownership is not signed |
| GATE3846_2_connection_lock | BLOCKED_CONNECTION_LOCK_REQUIRED | False | independent connection/torsion/nonmetricity leakage remains a named residual |
| GATE3846_3_no_shadow_motion_frame | BLOCKED_NO_SHADOW_FRAME_PARENT_SIGNATURE_REQUIRED | False | ordinary matter/public coframe route is conditional but not parent-signed |
| GATE3846_4_action_adoption | BLOCKED_BRIDGE_UNSIGNED | False | the bridge theorem is exact but not owned by current MTS |
| GATE3846_5_next_action | PASS_ACTIONABLE_NEXT | False | 3846 identifies the first missing owner: full 4D tau/h/c coframe completion from the radial T,S observer map |

## Decisions

| decision_id | decision | consequence |
| --- | --- | --- |
| DEC3846_0 | the metric bridge theorem is conditionally proved | the visible-action route is mathematically coherent if MTS owns the coframe data |
| DEC3846_1 | current MTS does not yet adopt the bridge | no EH action adoption, no local-GR claim, and no beta claim |
| DEC3846_2 | next work should derive the full 4D coframe from T,S/MTS primitives | 3847 attacks the actual bridge owner rather than adding more beta ledgers |

## Bottom Line

This is progress, not a pass. We now have the exact bridge theorem MTS needs: own `tau_a`, `h_ab`, `u^a`, and `c_*`, then `g_obs` follows. The next derivation should not wander: it should try to complete the old `T,S` observer coframe into a full 4D public coframe/metric package, or demote the visible-action route to closure-only.

Next target: `3847-Y5-R2FR-observer-coframe-completion-from-TS-or-metric-bridge-demotion.md`.
