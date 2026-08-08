# 2543 - Boundary / Projective Residual Split Under Private SRNG

## Result

Using the private `SRNG/OFC` branch, the connection residual now splits cleanly:

`Delta_abs_private = Delta_spin + Delta_boundary + Delta_improvement + 0_projective_private`.

Projective trace is zero only inside the private owned-coframe + SRNG branch, by variable absence. This is not a public/global result; the affine/projective fallback remains retained.

Boundary/improvement flux is not solved by SRNG. It is now the primary live blocker for the local Newton/GR source-normalization route:

`B_zero_flux` must either be derived zero by compact boundary/Hilbert flux closure, or filled as a finite source-backed bound row.

Spin/torsion remains a parallel guard.

## Residual Split Ledger

| row_id | component | private_SRNG_status | public_status | next_action |
| --- | --- | --- | --- | --- |
| RSL2543_0_private_total | Delta_abs_private_SRNG_branch | Delta_source/clock/light/orbit zeroed by private SRNG/OFC | not a public theorem | split spin, boundary, projective |
| RSL2543_1_spin | Delta_spin | still live unless owned-coframe spin connection is parent-signed | live | spin/coframe-owned connection theorem or axial-torsion bound |
| RSL2543_2_boundary | Delta_boundary + Delta_improvement | still live; SRNG does not fix integration-boundary flux | live | derive B_zero_flux=0 / compact flux closure or fill boundary bound |
| RSL2543_3_projective_private | Delta_projective | zero inside private owned-coframe+SRNG branch by variable absence | global affine fallback retained | record private zero switch and keep affine fallback policy |
| RSL2543_4_verdict | connection residual split | projective reduced; boundary remains hard live channel; spin remains separate guard | no local-GR/Newton claim | boundary no-flux/Hilbert flux closure first |

## Projective Status Under Private SRNG

| row_id | branch | projective_current | status | reason |
| --- | --- | --- | --- | --- |
| PRJ2543_0_candidate_zero | private owned-coframe + SRNG/OFC | 0 | ZERO_INSIDE_PRIVATE_BRANCH_ONLY | Gamma_ind is not a variable and source/readout exceptions are excluded by private SRNG |
| PRJ2543_1_public_global | full current corpus | not globally zero | PUBLIC_CERTIFICATE_BLOCKED | SRNG/OFC and owned-coframe are private working clauses, not public parent-signed theorems |
| PRJ2543_2_affine_fallback | independent affine fallback | P_projective[source,clock,WEP] | FALLBACK_RETAINED | if Gamma_ind is retained, projective trace needs an unobservable/gauge/fixed proof or numeric kernel |
| PRJ2543_3_verdict | decision | zero only in private branch | PRIVATE_ZERO_PUBLIC_NONCLAIM | private SRNG/owned-coframe collapses candidate-branch projective issue, not global affine branch |

## Boundary Improvement Queue

| row_id | boundary_object | status | needed_input |
| --- | --- | --- | --- |
| BND2543_0_B_zero_flux | B_zero_flux | MISSING_THEOREM_OR_VALUE | boundary no-flux theorem, compact support/falloff, source path, no-cancellation guard |
| BND2543_1_worldtube_flux | finite-annulus flux leakage | MISSING_TIME_RADIAL_PROFILE_OR_THEOREM | worldtube glue, Pi_M ownership, same-frame M_H_ref, flux closure |
| BND2543_2_projector_commutator | [d,Pi_M]J_H + R_eq | MISSING_COMMUTATOR_OR_EQUALITY_THEOREM | Pi_M J_H = J_M_top + dB_zero, I_commutator, Delta_PiM |
| BND2543_3_improvement_representative | improvement/superpotential representative | MISSING_FIXED_REPRESENTATIVE | fixed boundary/reference convention before readout |
| BND2543_4_priority | boundary first target | SELECTED_NEXT | derive compact boundary no-flux theorem or build first bound row |

## Reduced Connection Gate

| row_id | gate | status | claim_effect |
| --- | --- | --- | --- |
| RCG2543_0_private_formula | private SRNG reduced connection residual | PRIVATE_BRANCH_REDUCTION_ONLY | narrows internal work; no public pass |
| RCG2543_1_projective_private_zero | projective trace inside private branch | PRIVATE_ZERO_SWITCH | projective no longer first priority inside private branch |
| RCG2543_2_boundary_live | boundary/improvement closure | PRIMARY_LIVE_BLOCKER | Newton/GM/local-GR still blocked |
| RCG2543_3_public_gate | public local GR/Newton bridge | BLOCKED_NONCLAIM | do not publish as evidence |

## Claim Gates

| row_id | gate | gate_status | claim_effect |
| --- | --- | --- | --- |
| CG2543_0_projective_public_zero | projective trace globally zero | FAIL | private branch only |
| CG2543_1_boundary_zero | boundary/improvement flux zero | FAIL | primary blocker |
| CG2543_2_spin_zero | spin/torsion hypermomentum zero | FAIL | separate guard |
| CG2543_3_P4_score | remaining residuals score-ready | FAIL | values/maps/bounds missing |
| CG2543_4_local_GR_Newton | local GR/Newton recovery derived | FAIL | boundary/spin/formal adoption still open |
| CG2543_5_github | safe public evidence update | FAIL | private checkpoint only |

## Next Target

| row_id | priority | next_file | success_condition | fallback_condition |
| --- | --- | --- | --- | --- |
| NEXT2543_0_selected | selected | 2544-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md | derive compact boundary no-flux / Hilbert flux closure theorem for B_zero_flux | if theorem fails, emit first source-backed B_zero_flux bound row in GM-flux or dimensionless units |
| NEXT2543_1_parallel | parallel | 2544b-Y5-R2FR-spin-coframe-owned-connection-proof-or-axial-torsion-bound.md | prove spin connection is coframe-owned or bound axial torsion source response | retain E_spin residual if not closed |
| NEXT2543_2_fallback | fallback | 2544c-Y5-R2FR-affine-projective-kernel-if-private-branch-rejected.md | build projective trace residual kernel for global affine fallback | keep nonclaim unless sourced and same-frame |

## Validation

| row_id | status | detail |
| --- | --- | --- |
| VAL2543_00_required_sources_exist | PASS | all required source paths exist |
| VAL2543_01_required_needles_found | PASS | all source needles found |
| VAL2543_02_outputs_exist | PASS | all 2543 output files written |
| VAL2543_03_csv_parse | PASS | all generated CSV files parse and contain rows |
| VAL2543_04_split_verdict | PASS | residual split verdict recorded |
| VAL2543_05_projective_private_zero | PASS | projective zero switch private only |
| VAL2543_06_projective_fallback_retained | PASS | affine projective fallback retained |
| VAL2543_07_boundary_queue_live | PASS | B_zero boundary row remains live |
| VAL2543_08_boundary_primary | PASS | boundary selected as primary live blocker |
| VAL2543_09_local_claims_block | PASS | local GR/Newton claim gate remains false |
| VAL2543_10_next_boundary_no_flux | PASS | boundary no-flux target selected next |
| VAL2543_11_github_blocked | PASS | public GitHub evidence update remains blocked |
| VAL2543_12_branch_copies | PASS | all nonclaim branch copies exist |
| VAL2543_13_no_positive_claim_flags | PASS | all generated claim/readiness flags remain negative |
| VAL2543_14_formalization_untouched | PASS | project is not a git worktree here; generator writes only under post-checkpoint-work |
| VAL2543_15_pycache_absent | PASS | scripts __pycache__ absent |
| VAL2543_OVERALL | PASS | 2543 valid: residuals split under private SRNG, projective zero private only, affine fallback retained, boundary no-flux selected next |

## Generated Files

- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2543_SOURCE_REGISTER.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2543_RESIDUAL_SPLIT_LEDGER.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2543_PROJECTIVE_STATUS_UNDER_PRIVATE_SRNG.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2543_BOUNDARY_IMPROVEMENT_QUEUE.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2543_REDUCED_CONNECTION_GATE.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2543_CLAIM_GATES.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2543_REFUSAL_RUNNER.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2543_NEXT_TARGET.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2543_BRANCH_COPIES.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_2543_VALIDATION.csv`

## Practical Status

This is a useful reduction. The private SRNG branch removes the source/readout/projective clutter from the immediate internal path, but does not create a public claim. The main blocker is now boundary/improvement flux: prove no-flux or quantify `B_zero_flux`.
