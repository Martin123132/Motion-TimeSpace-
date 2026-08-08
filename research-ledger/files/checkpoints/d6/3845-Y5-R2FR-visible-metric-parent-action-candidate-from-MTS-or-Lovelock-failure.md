# 3845 - Visible Metric Parent Action Candidate From MTS Or Lovelock Failure

Private checkpoint. This tries the constructive route forced by 3844: write the minimal visible parent action candidate and test whether MTS currently owns it. It does not adopt the action or claim local GR.

Generated: `2026-07-01T03:34:01+00:00`

## Result

The minimal candidate is:

`S_candidate = (1/(2*kappa_MTS))*int sqrt(-g_obs(q(Phi)))*(R[g_obs]-2*Lambda_eff) + S_matter[Psi,g_obs(q(Phi)),theta(q)] + S_GHY[g_obs] + S_silent[Phi_perp;q]`.

The required MTS-to-metric bridge is:

`g_obs = h_space(M,T,S) - c_*^2 tau_time(M,T,S) otimes tau_time(M,T,S)`.

If MTS derives that bridge, the matter/source domain, and silent extra sectors, then the 3844 Lovelock route can collapse EH2. Current MTS does not yet own those clauses, so the candidate is a target, not a claim.

## Source Register

| source_id | path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC3845_0_3844_doc | 3844-Y5-R2FR-parent-action-second-variation-EH2-vertex-proof-or-source-bound.md | True | True | input_for_visible_metric_parent_action_candidate |
| SRC3845_1_3844_route | source-intake\mts_residuals\P8_Y5_R2FR_3844_LOVELOCK_EH2_ROUTE.csv | True | True | input_for_visible_metric_parent_action_candidate |
| SRC3845_2_3844_clauses | source-intake\mts_residuals\P8_Y5_R2FR_3844_PARENT_CLAUSE_AUDIT.csv | True | True | input_for_visible_metric_parent_action_candidate |
| SRC3845_3_3844_update | source-intake\mts_residuals\P8_Y5_R2FR_3844_EH2_BOUND_UPDATE.csv | True | True | input_for_visible_metric_parent_action_candidate |
| SRC3845_4_3844_validation | source-intake\mts_residuals\P8_Y5_BRR545_3844_VALIDATION.csv | True | True | input_for_visible_metric_parent_action_candidate |
| SRC3845_5_1030_doc | 1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md | True | True | input_for_visible_metric_parent_action_candidate |
| SRC3845_6_1030_public | source-intake\mts_residuals\P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv | True | True | input_for_visible_metric_parent_action_candidate |
| SRC3845_7_637_parent | source-intake\mts_residuals\P8_Y5_R10_637_PARENT_ACTION_DERIVATION_ATTEMPT.csv | True | True | input_for_visible_metric_parent_action_candidate |
| SRC3845_8_1008_doc | 1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md | True | True | input_for_visible_metric_parent_action_candidate |
| SRC3845_9_1008_parent | source-intake\mts_residuals\P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv | True | True | input_for_visible_metric_parent_action_candidate |
| SRC3845_10_3818_poisson | source-intake\mts_residuals\P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv | True | True | input_for_visible_metric_parent_action_candidate |
| SRC3845_11_3828_beta_lock | source-intake\mts_residuals\P8_Y5_R2FR_3828_ZERO_CONDITION_THEOREM.csv | True | True | input_for_visible_metric_parent_action_candidate |

## Metric Bridge Candidate

| bridge_id | object | candidate_formula | current_status | would_close |
| --- | --- | --- | --- | --- |
| MB3845_0_metric_schema | g_obs | g_obs = h_space(M,T,S) - c_*^2 tau_time(M,T,S) otimes tau_time(M,T,S) | SCHEMA_WRITTEN_NOT_PARENT_DERIVED | turns motion/time/space primitives into the public metric object needed by 3844 |
| MB3845_1_connection | Gamma_obs | Gamma_obs = Levi-Civita[g_obs] + C_nonLC | NONLC_RESIDUAL_RETAINED | blocks torsion/nonmetricity from masquerading as EH2 beta shift |
| MB3845_2_motion_readout | motion field / flow | motion data defines observer congruence/readout on g_obs, not an independent matter frame | READOUT_NATURALITY_REQUIRED | keeps the action from becoming multi-frame after metric construction |
| MB3845_3_verdict | MTS-to-visible-metric bridge | M,T,S -> (tau_time,h_space,c_*) -> g_obs | BRIDGE_NOT_CLAIMED_NEXT_TARGET | would let the visible action candidate be tested as MTS rather than imported GR notation |

## Visible Action Candidate

| candidate_id | candidate_name | current_status | not_a_claim_because |
| --- | --- | --- | --- |
| VAC3845_0_minimal_visible_EH_candidate | minimal visible MTS parent action candidate | CANDIDATE_WRITTEN_NOT_ADOPTED | g_obs(M,T,S), kappa_MTS, matter functor domain, and S_silent silence are not parent-derived in current corpus |
| VAC3845_1_silent_sector_rule | silent representative sector | SILENCE_CERTIFICATE_REQUIRED | 637/1008 do not yet supply the full parent action descent and boundary-domain silence |
| VAC3845_2_no_smuggle_guard | not-GR-by-copying guard | GUARD_ACTIVE | candidate needs MTS-to-metric bridge and parent ownership before it becomes the theory action |

## Lovelock Clause Test

| test_id | clause | test_result | current_mts_status | remaining_gap |
| --- | --- | --- | --- | --- |
| LCT3845_0_formal_lovelock_shape | candidate action has EH visible operator | PASS_IF_CANDIDATE_ADOPTED | FORMAL_SHAPE_ONLY | derive candidate from MTS primitives, not from GR preference |
| LCT3845_1_metric_bridge | M,T,S parent-derive one public metric g_obs | FAIL_CURRENT_CLAIM | MB3845 schema exists but is not parent-signed | prove tau_time, h_space, c_*, and nondegenerate Lorentzian metric from MTS |
| LCT3845_2_action_descent | S_parent descends to S_candidate plus silent sectors | FAIL_CURRENT_CLAIM | 637 action descent is conditional and 1008 says parent current-chain action is missing | supply explicit parent Lagrangian/current chain or reject adoption |
| LCT3845_3_matter_source | matter couples only to g_obs with Hilbert source | FAIL_CURRENT_CLAIM | 1030 public-metric action contract is written but not parent-signed | derive no shadow frame/no source-only weight/no marker constant clause |
| LCT3845_4_silent_extra_sectors | extra/projector/boundary sectors do not vary into visible beta vertex | FAIL_CURRENT_CLAIM | silence certificates not supplied | prove R_silent_mu_nu=0 or retain explicit EH2 residual |
| LCT3845_5_newtonian_kappa | kappa_MTS fixes G_ref before beta | CONDITIONAL_FROM_3818 | first-order Poisson bridge exists but source normalization guards remain | same-source measure and no fitted GM smuggling |
| LCT3845_6_verdict | candidate can be adopted as current MTS parent action | NOT_ADOPTED_CURRENTLY | constructive target written; adoption fails until bridge/action/source/silence clauses close | 3846 must derive or reject MTS-to-visible-metric bridge |

## EH2 Implication

| row_id | observable | formula | status |
| --- | --- | --- | --- |
| EHI3845_0_candidate_success | B_EH2_vertex | if VAC3845_0 is parent-adopted and LCT3845_1..5 pass, then B_EH2_vertex <= B_field_redef_gauge | EXACT_CONDITIONAL_EH2_COLLAPSE |
| EHI3845_1_current_bound | B_EH2_vertex | B_EH2_vertex <= B_metric_bridge + B_action_descent + B_matter_source + B_silent_sector + B_kappa_source + B_field_redef_gauge | CURRENT_NONCLAIM_ADOPTION_FAILURE_BOUND |
| EHI3845_2_bridge_focus | B_metric_bridge | B_metric_bridge=0 requires M,T,S -> tau_time,h_space,c_* -> g_obs to be parent-signed and unique | NEXT_PROOF_TARGET |

## Claim Gates

| gate_id | status | claim_allowed | reason |
| --- | --- | --- | --- |
| GATE3845_0_candidate_written | PASS_CANDIDATE_WRITTEN | False | the action target is explicit instead of a vague missing parent action |
| GATE3845_1_metric_bridge | BLOCKED_MTS_TO_VISIBLE_METRIC_BRIDGE_NOT_PROVED | False | tau_time, h_space, c_*, and Lorentzian nondegeneracy are schema-level only |
| GATE3845_2_action_adoption | BLOCKED_PARENT_DERIVATION_NOT_SIGNED | False | current corpus has conditional descent contracts but not a signed current-chain Lagrangian |
| GATE3845_3_no_smuggle | PASS_GUARD | False | all adoption rows remain nonclaim until MTS owns the bridge/action/source clauses |
| GATE3845_4_next_action | PASS_ACTIONABLE_NEXT | False | the first adoption failure is the metric bridge from motion/time/space to g_obs |

## Decisions

| decision_id | decision | consequence |
| --- | --- | --- |
| DEC3845_0 | write the minimal visible action candidate but do not adopt it | we now know exactly what MTS must derive to reduce to GR locally |
| DEC3845_1 | the bridge from motion/time/space to one public Lorentzian metric is the next bottleneck | 3846 should try to derive g_obs from MTS primitives before any more beta bookkeeping |
| DEC3845_2 | EH action shape is a target, not an imported proof | no local-GR claim until MTS owns the bridge, source, and silence clauses |

## Bottom Line

This is the cleanest leap forward so far on the GR-reduction branch: the action target is now explicit. The project has not proven it, but the next bottleneck is no longer vague. It is the bridge from motion/time/space primitives to one public Lorentzian metric `g_obs`. If that bridge closes, the EH/local-GR route becomes serious. If it fails, the visible-action route should be rejected cleanly.

Next target: `3846-Y5-R2FR-MTS-to-visible-metric-bridge-or-action-candidate-reject.md`.
