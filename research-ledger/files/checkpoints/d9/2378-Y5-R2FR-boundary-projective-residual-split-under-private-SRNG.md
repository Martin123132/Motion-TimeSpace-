# 2378 - Boundary / Projective Residual Split Under Private SRNG

## Result

Using the private `SRNG/OFC` branch, the connection residual now splits cleanly:

`Delta_abs_private = Delta_spin + Delta_boundary + Delta_improvement + 0_projective_private`.

Projective trace is zero only inside the private owned-coframe + SRNG branch, by variable absence.  This is not a public/global result; the affine/projective fallback remains retained.

Boundary/improvement flux is not solved by SRNG.  It is now the primary live blocker for the local Newton/GR source-normalization route:

`B_zero_flux` must either be derived zero by compact boundary/Hilbert flux closure, or filled as a finite source-backed bound row.

Spin/torsion remains a parallel guard.

## Residual Split Ledger

| row_id | component | private_SRNG_status | public_status | next_action |
| --- | --- | --- | --- | --- |
| RSL2378_0_private_total | Delta_abs_private_SRNG_branch | Delta_source/clock/light/orbit zeroed by private SRNG/OFC | not a public theorem | split spin, boundary, projective |
| RSL2378_1_spin | Delta_spin | still live unless owned-coframe spin connection is parent-signed | live | spin/coframe-owned connection theorem or axial-torsion bound |
| RSL2378_2_boundary | Delta_boundary + Delta_improvement | still live; SRNG does not fix integration-boundary flux | live | derive B_zero_flux=0 / compact flux closure or fill boundary bound |
| RSL2378_3_projective_private | Delta_projective | zero inside private owned-coframe+SRNG branch by variable absence | global affine fallback retained | record private zero switch and keep affine fallback policy |
| RSL2378_4_verdict | connection residual split | projective reduced; boundary remains hard live channel; spin remains separate guard | no local-GR/Newton claim | boundary no-flux/Hilbert flux closure first |

## Projective Status Under Private SRNG

| row_id | branch | projective_current | status | reason |
| --- | --- | --- | --- | --- |
| PRJ2378_0_candidate_zero | private owned-coframe + SRNG/OFC | 0 | ZERO_INSIDE_PRIVATE_BRANCH_ONLY | Gamma_ind is not a variable and source/readout exceptions are excluded by private SRNG |
| PRJ2378_1_public_global | full current corpus | not globally zero | PUBLIC_CERTIFICATE_BLOCKED | SRNG/OFC and owned-coframe are private working clauses, not public parent-signed theorems |
| PRJ2378_2_affine_fallback | independent affine fallback | P_projective[source,clock,WEP] | FALLBACK_RETAINED | if Gamma_ind is retained, projective trace needs an unobservable/gauge/fixed proof or numeric kernel |
| PRJ2378_3_verdict | decision | zero only in private branch | PRIVATE_ZERO_PUBLIC_NONCLAIM | private SRNG/owned-coframe collapses candidate-branch projective issue, not global affine branch |

## Boundary Improvement Queue

| row_id | boundary_object | status | needed_input |
| --- | --- | --- | --- |
| BND2378_0_B_zero_flux | B_zero_flux | MISSING_THEOREM_OR_VALUE | boundary no-flux theorem, compact support/falloff, source path, no-cancellation guard |
| BND2378_1_worldtube_flux | finite-annulus flux leakage | MISSING_TIME_RADIAL_PROFILE_OR_THEOREM | worldtube glue, Pi_M ownership, same-frame M_H_ref, flux closure |
| BND2378_2_projector_commutator | [d,Pi_M]J_H + R_eq | MISSING_COMMUTATOR_OR_EQUALITY_THEOREM | Pi_M J_H = J_M_top + dB_zero, I_commutator, Delta_PiM |
| BND2378_3_improvement_representative | improvement/superpotential representative | MISSING_FIXED_REPRESENTATIVE | fixed boundary/reference convention before readout |
| BND2378_4_priority | boundary first target | SELECTED_NEXT | derive compact boundary no-flux theorem or build first bound row |

## Reduced Connection Gate

| row_id | gate | status | claim_effect |
| --- | --- | --- | --- |
| RCG2378_0_private_formula | private SRNG reduced connection residual | PRIVATE_BRANCH_REDUCTION_ONLY | narrows internal work; no public pass |
| RCG2378_1_projective_private_zero | projective trace inside private branch | PRIVATE_ZERO_SWITCH | projective no longer first priority inside private branch |
| RCG2378_2_boundary_live | boundary/improvement closure | PRIMARY_LIVE_BLOCKER | Newton/GM/local-GR still blocked |
| RCG2378_3_public_gate | public local GR/Newton bridge | BLOCKED_NONCLAIM | do not publish as evidence |

## Claim Gates

| row_id | gate | gate_status | claim_effect |
| --- | --- | --- | --- |
| CG2378_0_projective_public_zero | projective trace globally zero | FAIL | private branch only |
| CG2378_1_boundary_zero | boundary/improvement flux zero | FAIL | primary blocker |
| CG2378_2_spin_zero | spin/torsion hypermomentum zero | FAIL | separate guard |
| CG2378_3_P4_score | remaining residuals score-ready | FAIL | values/maps/bounds missing |
| CG2378_4_local_GR_Newton | local GR/Newton recovery derived | FAIL | boundary/spin/formal adoption still open |
| CG2378_5_github | safe public evidence update | FAIL | private checkpoint only |

## Next Target

| row_id | next_file | success_condition | fallback_condition |
| --- | --- | --- | --- |
| NEXT2378_0_selected | 2379-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md | derive compact boundary no-flux / Hilbert flux closure theorem for B_zero_flux | if theorem fails, emit first source-backed B_zero_flux bound row in GM-flux or dimensionless units |
| NEXT2378_1_parallel | 2379b-Y5-R2FR-spin-coframe-owned-connection-proof-or-axial-torsion-bound.md | prove spin connection is coframe-owned or bound axial torsion source response | retain E_spin residual if not closed |
| NEXT2378_2_fallback | 2379c-Y5-R2FR-affine-projective-kernel-if-private-branch-rejected.md | build projective trace residual kernel for global affine fallback | keep nonclaim unless sourced and same-frame |

## Generated Files

- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2378_SOURCE_REGISTER.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2378_RESIDUAL_SPLIT_LEDGER.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2378_PROJECTIVE_STATUS_UNDER_PRIVATE_SRNG.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2378_BOUNDARY_IMPROVEMENT_QUEUE.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2378_REDUCED_CONNECTION_GATE.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2378_CLAIM_GATES.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2378_REFUSAL_RUNNER.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2378_NEXT_TARGET.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_2378_VALIDATION.csv`

## Practical Status

This is a useful reduction.  The private SRNG branch removes the source/readout/projective clutter from the immediate internal path, but does not create a public claim.  The main blocker is now boundary/improvement flux: prove no-flux or quantify `B_zero_flux`.
