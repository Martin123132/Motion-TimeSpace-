# 787 - Y5 R10 Multifield Pregeometry Rank Gate Or Independent Metric Branch Decision

Current result: **the multifield/pregeometry route survives the algebraic rank problem, but only conditionally**. A single scalar `psi` cannot own generic local GR metric variations. A rank-four bundle `psi^A` or equivalent pregeometry can span the ten local symmetric metric components at first order, but an exact-gradient coframe with constant internal metric falls into the flat-pullback trap. So the next derivation must use a nonholonomic coframe, a covariant moment closure, or the conservative independent metric/tetrad branch.

## Status

| status | claim_ceiling | main_result | hard_blocker | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| Y5_R10_787_multifield_pregeometry_rank_gate_passes_conditionally_but_integrability_curvature_blocks_local_GR_claim | rank_gate_and_branch_decision_only_no_adopted_pregeometry_no_parent_action_no_local_GR_Newton_claim | multifield/pregeometry with N>=4 can conditionally solve the first-order metric-variation rank problem, but exact-gradient scalar/coframe maps with constant internal metric fall into a flat pullback trap | need nonholonomic coframe, covariant moment closure, or independent metric/tetrad branch plus parent action and matter-coupling proof | 788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md | false |

## Numerical Rank Smoke

| smoke_id | field_count_N | linearized_map | rank | target_symmetric_metric_components | rank_full | interpretation | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| N1_rank | 1 | deltaG_mu_nu = deltaV_muA H_AB V_nuB + V_muA H_AB deltaV_nuB at V=[I_4,0] | 4 | 10 | false | insufficient local metric-variation span | false |
| N2_rank | 2 | deltaG_mu_nu = deltaV_muA H_AB V_nuB + V_muA H_AB deltaV_nuB at V=[I_4,0] | 7 | 10 | false | insufficient local metric-variation span | false |
| N3_rank | 3 | deltaG_mu_nu = deltaV_muA H_AB V_nuB + V_muA H_AB deltaV_nuB at V=[I_4,0] | 9 | 10 | false | insufficient local metric-variation span | false |
| N4_rank | 4 | deltaG_mu_nu = deltaV_muA H_AB V_nuB + V_muA H_AB deltaV_nuB at V=[I_4,0] | 10 | 10 | true | full local symmetric-tensor span | false |
| N5_rank | 5 | deltaG_mu_nu = deltaV_muA H_AB V_nuB + V_muA H_AB deltaV_nuB at V=[I_4,0] | 10 | 10 | true | full local symmetric-tensor span | false |
| N6_rank | 6 | deltaG_mu_nu = deltaV_muA H_AB V_nuB + V_muA H_AB deltaV_nuB at V=[I_4,0] | 10 | 10 | true | full local symmetric-tensor span | false |

## Multifield Pregeometry Rank Gate

| gate_id | question | result | argument | repair_needed | branch_effect | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| MPR787_0_scalar_route | Can one scalar psi own generic local GR metric variations? | no | rank(deltaG/delta psi) is at most four local directions and the 786 scalar-gradient map is rank-one at a point | multifield psi^A, independent moment tensor, coframe variable, or independent metric | scalar-only psi demoted as sole GR owner | false |
| MPR787_1_minimal_multifield_rank | How many independent pregeometry directions are needed for first-order metric-variation rank? | N_at_least_4_conditional | for G=VHV^T, if V has rank four and H is nondegenerate on that image, deltaV spans all ten symmetric metric components | declare what the four directions physically are and why they are not arbitrary labels | multifield/pregeometry remains alive | false |
| MPR787_2_surjectivity_condition | What exact theorem must a future parent action prove? | local_surjectivity_contract | rank(delta G_mu_nu / delta psi^A) must cover symmetric tensor variations modulo diffeomorphism/gauge directions in the local GR domain | prove rank condition from parent background/coarse-grained state, not by tuning after the fact | precise acceptance gate set | false |
| MPR787_3_internal_signature | Can positive scalar covariance alone supply a Lorentzian metric? | not_without_signature_structure | a positive Gram correction alone does not own Lorentzian signature; an internal Lorentzian metric, background, or coframe signature rule is required | derive or declare internal signature and prove stability of local Lorentzian domain | signature remains a live gate | false |
| MPR787_4_matter_coupling | Does passing the rank gate prove matter-frame blindness? | no | rank only says metric variations can be represented; matter could still see psi^A, moments, or frame representatives directly | parent-signed S_matter[e_obs,omega,owned gauge fields] and no-spurion audit | b_g/c_g remains active | false |
| MPR787_5_rank_gate_verdict | Can multifield/pregeometry rescue the 786 rank obstruction? | yes_conditionally_not_adopted | N>=4 full-rank pregeometry can pass first-order rank, but curvature/integrability/action ownership still block local GR | 788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md | continue derivation via nonholonomic coframe or moment closure | false |

## Curvature Integrability Gate

| gate_id | issue | result | why_it_matters | escape_route | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CIG787_0_flat_pullback_trap | If e^a_mu = partial_mu psi^a and internal H_ab is constant, g_mu_nu is locally the pullback of a flat target metric. | curvature_block | an invertible exact-gradient coframe is just a coordinate pullback and cannot produce generic curved GR geometry | nonholonomic coframe, nonconstant/internal curved metric, or coarse-grained independent moment tensor | false |
| CIG787_1_nonholonomic_coframe | Promote e^a_mu or distortion E^a_mu to a field not constrained to be d psi^a. | viable_low_scrutiny_branch | generic tetrads can carry curvature and recover standard GR machinery | derive e from motion/time/space parent variables or accept independent tetrad/metric branch | false |
| CIG787_2_moment_closure | Treat <partial psi^A partial psi^B> as a coarse-grained covariance/moment field with independent dynamics. | viable_but_unsigned | this preserves the motion-flow intuition while escaping the exact-gradient flatness trap | derive a covariant moment evolution equation and closure from parent dynamics | false |
| CIG787_3_independent_metric | Keep g_mu_nu as independent/effective metric with psi/memory as stress-exchange fields. | conservative_fallback | this most cleanly protects local GR and Newton but weakens the pure-emergent claim | write standard EH metric sector plus MTS exchange stress and prove conservation/limits | false |
| CIG787_4_curvature_verdict | Does the multifield rank gate alone derive GR? | no | rank solves one algebraic obstruction but not curvature, dynamics, covariance, or coupling ownership | 788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md | false |

## Branch Decision

| decision_id | decision | reason | result | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| D787_0_scalar_only_demoted | demote single-scalar psi as sole local-GR owner | fails rank and exact-gradient curvature tests | demoted_not_dead_as_component | 788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md | false |
| D787_1_multifield_kept | keep multifield/pregeometry route alive | N>=4 full-rank bundle can pass local variation rank if the field content and signature are real | conditional_route_retained | 788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md | false |
| D787_2_no_adoption | do not adopt multifield pregeometry yet | curvature, covariance, parent action, and matter coupling are not derived | not_adopted | 788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md | false |
| D787_3_fallback | retain independent metric/tetrad as fallback | it is the least-scrutiny path to local GR/Newton if emergent ownership keeps failing | fallback_retained | 788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md | false |
| D787_4_next_target | try nonholonomic coframe or moment-closure parent action next | that is the smallest route that can pass rank without falling into flat pullback geometry | next_target_selected | 788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md | false |

## Source Register

| source_id | path | exists | needle_check | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 786_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\786-Y5-R10-parent-action-metric-map-ownership-or-bg-bound-source-pack.md | true | true | immediate 787 handoff | false |
| 786_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_786_VALIDATION.csv | true | true | prior validation guard | false |
| 786_candidates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_786_PARENT_ACTION_OWNERSHIP_CANDIDATES.csv | true | true | candidate branch inputs | false |
| 786_rank_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_786_VARIATIONAL_RANK_GATE.csv | true | true | rank obstruction input | false |
| 785_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_785_PSI_METRIC_COFRAME_CONTRACT.csv | true | true | coframe and parent-action contract | false |
| spine_07 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\07-unification-spine.md | true | true | unification spine and GR/Newton chain | false |
| testing_145 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\145-testing-readiness-and-gr-limit-map.md | true | true | local GR-limit demand | false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V787_0_source_paths_exist | pass | source_rows=7 |
| V787_1_source_needles_present | pass | all source needles present |
| V787_2_prior_665_786_clean | pass | 665-786 validation rows have no failures |
| V787_3_rank_smoke_complete | pass | numerical rank smoke rows complete |
| V787_4_scalar_rank_insufficient | pass | N=1 does not span ten metric components |
| V787_5_N4_rank_full | pass | N=4 full-rank bundle spans ten metric components in smoke gate |
| V787_6_rank_gate_complete | pass | multifield rank gate rows complete |
| V787_7_multifield_conditional | pass | multifield route retained conditionally, not adopted |
| V787_8_curvature_gate_complete | pass | curvature/integrability rows complete |
| V787_9_flat_pullback_block | pass | exact-gradient flat pullback trap recorded |
| V787_10_no_adoption | pass | no multifield/pregeometry branch adopted |
| V787_11_next_target_selected | pass | 788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md |
| V787_12_no_claim_rows_promoted | pass | all generated rows valid_for_claim=false |
| V787_13_claim_artifacts_absent | pass | no adopted-pregeometry/parent-action/local-GR/Newton claim artifact fabricated |
| V787_14_outputs_scoped | pass | all outputs under post-checkpoint-work |
| V787_15_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V787_16_validation_rows_ready | pass | validation table constructed |

## Verdict

This is a real improvement in the map. The route "motion/time/space only" is not dead, but it cannot mean one thin scalar doing all the metric work. It must mean a rank-carrying pregeometry: at least four independent directions, plus a nonholonomic or moment-based mechanism so the metric can actually curve. If that cannot be derived, the serious field-theory route is to keep a standard metric/tetrad sector and let MTS enter through controlled stress, memory, and exchange terms.

## Next Target

`788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md`
