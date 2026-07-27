# 2541 - Source-Readout noGamma Action-Argument Certificate

## Result

The source/readout no-Gamma certificate is now explicit:

`SRNG`: source support, clocks, light, orbits and readout maps may use the observed coframe/metric, `omega_LC[e_obs]`, owned gauge fields, constants and solved fields, but not an independent `Gamma_ind` argument inside the variational source/action.

Under SRNG plus the no-Gamma ordinary matter branch:

`Delta_source = Delta_clock = Delta_light = Delta_orbit = 0`

without cancellation.

But SRNG is a private contract, not yet a derived parent theorem. Boundary/improvement and projective trace also remain separate residual channels. So this improves the connection route, but it does not close local GR/Newton.

## SRNG Argument Certificate

| row_id | sector | status | closes_delta | remaining_gap |
| --- | --- | --- | --- | --- |
| SRNG2541_0_total_clause | total source/readout branch | CERTIFICATE_WRITTEN_NOT_PARENT_SIGNED | Delta_source+Delta_clock+Delta_light+Delta_orbit | parent adoption or deeper quotient/naturality derivation |
| SRNG2541_1_source_worldtube | source worldtube and GM support | CONDITIONAL_FROM_WORLDTUBE_SELECTOR_NOT_SIGNED | Delta_source | compactness, boundary/reference lock, M_H_ref and coupling descent are not parent-signed |
| SRNG2541_2_clock | clock and frequency readout | CONTRACT_FORM_WRITTEN_NOT_PARENT_SIGNED | Delta_clock | clock model and tau/frame lock still need explicit parent signature |
| SRNG2541_3_light | light, EM, Shapiro and deflection readout | CONTRACT_FORM_WRITTEN_NOT_PARENT_SIGNED | Delta_light | Maxwell/WKB and detector readout need parent-side statement in MTS language |
| SRNG2541_4_orbit | orbital/test-body readout | CONTRACT_FORM_WRITTEN_NOT_PARENT_SIGNED | Delta_orbit | test-body reduction and marker/domain map still need parent certificate |
| SRNG2541_5_boundary | boundary/domain/improvement | NOT_CLOSED_REQUIRES_SEPARATE_BOUNDARY_CERTIFICATE | Delta_boundary | worldtube flux and improvement current zero theorem/bound is still live |
| SRNG2541_6_verdict | all source/readout sectors | PARTIAL_CERTIFICATE_READY_NOT_DERIVED | conditional: Delta_source+Delta_clock+Delta_light+Delta_orbit | derive SRNG from quotient/naturality or adopt it as a private working parent clause; boundary/projective remain separate |

## SRNG Theorem Attempt

| row_id | claim_piece | result | obstruction |
| --- | --- | --- | --- |
| THM2541_0_downstream_readout | downstream readout lemma | EXACT_CONDITIONAL_LEMMA | must prove clocks/light/orbits are downstream functors, not hidden action/source terms |
| THM2541_1_hilbert_source_selector | Hilbert source selector lemma | EXACT_CONDITIONAL_LEMMA | compactness, M_H_ref, boundary/reference lock and same-frame tau are unsigned |
| THM2541_2_orbit_test_body | test-body no-autoparallel lemma | EXACT_CONDITIONAL_LEMMA | test-body limit and marker/domain maps must be written in parent variables |
| THM2541_3_SRNG_sum | SRNG zero sum | CONDITIONAL_THEOREM_READY | SRNG is written here as a contract, not derived or adopted as active MTS parent action |
| THM2541_4_boundary_warning | boundary warning | LIMIT_EXPLICIT | Delta_boundary and Delta_projective remain live |

## P4 Delta Status After SRNG

| row_id | component | status_after_SRNG | current_status | needed_for_score |
| --- | --- | --- | --- | --- |
| P4S2541_0_source | Delta_source | ZERO_IF_SRNG_PARENT_SIGNED_ELSE_BOUND | SRNG_CONTRACT_NOT_SIGNED | source/worldtube no-Gamma adoption or finite source-current bound |
| P4S2541_1_clock | Delta_clock | ZERO_IF_DOWNSTREAM_CLOCK_FUNCTOR_SIGNED_ELSE_BOUND | CLOCK_ARGUMENT_LIST_NOT_SIGNED | clock readout parent functor or frequency residual bound |
| P4S2541_2_light | Delta_light | ZERO_IF_EM_LIGHT_READOUT_SIGNED_ELSE_BOUND | LIGHT_ARGUMENT_LIST_NOT_SIGNED | EM/WKB/null readout certificate or PPN light bound |
| P4S2541_3_orbit | Delta_orbit | ZERO_IF_TEST_BODY_LIMIT_SIGNED_ELSE_BOUND | ORBIT_ARGUMENT_LIST_NOT_SIGNED | test-body/marker parent map or orbital residual bound |
| P4S2541_4_boundary | Delta_boundary | STILL_OPEN_SEPARATE_CERTIFICATE | BOUNDARY_ZERO_OR_BOUND_MISSING | boundary no-flux/improvement theorem or source-backed bound |
| P4S2541_5_projective | Delta_projective | STILL_OPEN_PARALLEL_CERTIFICATE | PROJECTIVE_TRACE_POLICY_MISSING | projective gauge/fixed/unobservable certificate or residual policy |
| P4S2541_6_reduced_total | Delta_abs_reduced | IF_SRNG_AND_MATTER_BRANCH_SIGNED_THEN_REDUCE_TO_DELTA_SPIN_BOUNDARY_PROJECTIVE | REDUCTION_CONDITIONAL_ONLY | SRNG adoption plus spin/boundary/projective closure |

## Decision Ledger

| row_id | decision | status | consequence |
| --- | --- | --- | --- |
| DEC2541_0_SRNG_contract | SRNG source-readout no-Gamma contract is now explicit | CONTRACT_READY_NONCLAIM | several leak paths can close together if adopted or derived |
| DEC2541_1_no_public_promotion | do not promote SRNG as current MTS theorem | NO_PROMOTION | no local-GR/Newton/WEP/PPN claim |
| DEC2541_2_best_next | try to derive downstream observation functor naturality next | SELECT_DOWNSTREAM_FUNCTOR_DERIVATION_NEXT | otherwise adopt SRNG privately or fill P4 component bounds |
| DEC2541_3_public_policy | no GitHub evidence update | NO_GITHUB_EVIDENCE_UPDATE | continue in post-checkpoint-work |

## Claim Gates

| row_id | gate | gate_status | claim_effect |
| --- | --- | --- | --- |
| CG2541_0_SRNG_active | SRNG active in parent action | FAIL | contract only |
| CG2541_1_source_readout_zero | Delta_source/clock/light/orbit theorem-zero | FAIL | zero only if SRNG parent-signed |
| CG2541_2_boundary_projective | boundary/projective residuals closed | FAIL | still open |
| CG2541_3_P4_score | P4 components score-ready | FAIL | no numeric units/maps/bounds yet |
| CG2541_4_local_GR_Newton | local GR/Newton recovery derived | FAIL | connection/EH/GM gates remain |
| CG2541_5_github | safe public evidence update | FAIL | private checkpoint only |

## Next Target

| row_id | priority | next_file | success_condition | fallback_condition |
| --- | --- | --- | --- | --- |
| NEXT2541_0_selected | selected | 2542-Y5-R2FR-downstream-observation-functor-naturality-or-SRNG-adoption.md | prove clocks/light/orbits/readouts are downstream natural functors of q-observed solved fields, not new source-current arguments | if not derived, retain SRNG as private branch contract or fill P4 component bounds |
| NEXT2541_1_parallel | parallel | 2542b-Y5-R2FR-boundary-projective-residual-split.md | split boundary/improvement and projective trace into independent zero/bound policies | retain E_boundary/Delta_projective residuals if unsigned |
| NEXT2541_2_fallback | fallback | 2542c-Y5-R2FR-P4-source-readout-component-bounds.md | fill Delta_source/clock/light/orbit units, weak-field maps and source-backed bounds | keep nonclaim until same-frame and source-backed |

## Validation

| row_id | status | detail |
| --- | --- | --- |
| VAL2541_00_required_sources_exist | PASS | all required source paths exist |
| VAL2541_01_required_needles_found | PASS | all source needles found |
| VAL2541_02_outputs_exist | PASS | all 2541 output files written |
| VAL2541_03_csv_parse | PASS | all generated CSV files parse and contain rows |
| VAL2541_04_SRNG_written | PASS | SRNG total contract written as nonclaim |
| VAL2541_05_SRNG_not_promoted | PASS | SRNG not promoted as derived |
| VAL2541_06_theorem_limits | PASS | boundary/projective limitation explicit |
| VAL2541_07_p4_status_components | PASS | source/readout/boundary/projective P4 status rows present |
| VAL2541_08_next_derivation_selected | PASS | downstream observation functor derivation selected next |
| VAL2541_09_local_claims_block | PASS | local GR/Newton claim gate remains false |
| VAL2541_10_github_blocked | PASS | public GitHub evidence update remains blocked |
| VAL2541_11_branch_copies | PASS | all nonclaim branch copies exist |
| VAL2541_12_no_positive_claim_flags | PASS | all generated claim/readiness flags remain negative |
| VAL2541_13_formalization_untouched | PASS | project is not a git worktree here; generator writes only under post-checkpoint-work |
| VAL2541_14_pycache_absent | PASS | scripts __pycache__ absent |
| VAL2541_OVERALL | PASS | 2541 valid: SRNG source/readout no-Gamma certificate written nonclaim, conditional zero effect recorded, boundary/projective/P4 retained, downstream functor derivation selected |

## Generated Files

- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2541_SOURCE_REGISTER.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2541_SOURCE_READOUT_ARGUMENT_CERTIFICATE.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2541_SRNG_THEOREM_ATTEMPT.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2541_P4_DELTA_STATUS_AFTER_SRNG.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2541_DECISION_LEDGER.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2541_CLAIM_GATES.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2541_REFUSAL_RUNNER.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2541_NEXT_TARGET.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2541_BRANCH_COPIES.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_2541_VALIDATION.csv`

## Practical Status

This is a real structural gain. We now have a compact clause that would zero the source/readout Gamma components together. The remaining honest question is whether SRNG can be derived from downstream observation functor naturality, or whether it must stay as a private parent-action restriction with P4 fallback bounds.
