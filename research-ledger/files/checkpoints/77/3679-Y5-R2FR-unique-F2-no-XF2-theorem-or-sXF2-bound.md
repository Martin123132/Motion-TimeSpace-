# 3679 - Unique-F2/no-XF2 theorem or s_XF2 bound

**Status:** UNIQUE_F2_ZERO_NOT_PROVED_SXF2_CANONICAL_ALPHA_IDENTITY_PROMOTED_NONCLAIM

This checkpoint takes the 3678 throat seriously rather than just writing another missing-piece note. The unique-F2/no hidden-XF2 theorem is attempted and rejected under the current parent grammar: a hidden scalar multiplier `f_X(X_N)F_Q^2` is **not killed by gauge/diffeomorphism symmetry**.

## Main result

`s_XF2 = D_Xhat ln lambda_A` is promoted as the canonical scalar Maxwell-kinetic residual.

The fine-structure/current identity is:

`b_alpha_X = 2 z_g - s_XF2`, with `z_g = D_Xhat ln g_J`.

Therefore alpha/clock/WEP evidence cannot be used as a direct `s_XF2` bound unless the parent theory first proves `z_g=0`. If `z_g=0`, then `s_XF2 = -b_alpha_X`.

## Theorem audit
- `UF23679_0_target_theorem`: TARGET_NOT_PROVED - unique Maxwell F2/no hidden XF2 theorem -> the desired zero would set s_XF2=0
- `UF23679_1_visible_rank_reduction`: USEFUL_REDUCTION_NOT_ZERO - visible U(1), locality, reciprocity, and observed Hodge reduce the principal EM action to Maxwell form up to scalar/topological coefficients -> the problem is narrowed to a scalar gauge-kinetic owner, not solved
- `UF23679_2_counterterm_legality`: COUNTERTERM_LEGAL_WITH_CURRENT_PARENT_GRAMMAR - Delta L = -(1/4) f_X(X_N) F_Q^2 -> s_XF2 is not killed by gauge/diffeomorphism symmetry
- `UF23679_3_no_hidden_visible_hom`: NO_PARENT_SIGNATURE_FOUND - Hom(hidden residual scalars, visible F_Q^2)=0 -> hidden scalar lambda branch remains live
- `UF23679_4_operator_domain_exhaustion`: NOT_DERIVED_CURRENT_CORPUS - visible F2 image exhaustion -> ordinary symmetry cannot distinguish parent-owned lambda_A from an independent scalar dressing
- `UF23679_5_source_owner_packet`: OWNER_PACKET_UNSIGNED - F2/current/source coupling must close together -> the coupling can migrate from F2 into current normalization
- `UF23679_6_verdict`: THEOREM_NOT_PROVED_RETAIN_CANONICAL_BOUND_BRANCH - s_XF2 theorem-zero -> s_XF2=0 is not claimed; s_XF2 is promoted to a canonical component with exact alpha/current identity

## Canonical map
- `MAP3679_0_action_block`: DEFINITION_BRANCH_NONCLAIM - `S_EM,J = -1/4 int lambda_A(X_hat) F_Q wedge *_obs F_Q + int g_J(X_hat) A_Q.J_Q`
- `MAP3679_1_sXF2_definition`: PROMOTED_CANONICAL_COMPONENT - `s_XF2 = D_Xhat ln lambda_A`
- `MAP3679_2_current_leg`: LIVE_OWNER_THROAT - `z_g = D_Xhat ln g_J`
- `MAP3679_3_alpha_identity`: DERIVED_IDENTITY - `b_alpha_X = D_Xhat ln alpha_eff = 2 z_g - s_XF2`
- `MAP3679_4_zg_zero_branch`: CONDITIONAL_DIRECT_BOUND_ROUTE - `if z_g=0 then s_XF2 = -b_alpha_X`
- `MAP3679_5_zg_live_branch`: RETAIN_TWO_KNOB_ROUTE - `s_XF2 = 2 z_g - b_alpha_X`
- `MAP3679_6_canonicalization_warning`: NO_CONVENTION_SHORTCUT - `F(A)=lambda_A^(-1/2)[F_c - 1/2 dln(lambda_A) wedge A_c]`

## Bound/input rows
- `SXF23679_0_equal_budget_O1`: PRIVATE_TARGET_NOT_EVIDENCE - `abs(s_XF2)` -> `3.724015406785e-06`; budget only; not a measurement or parent derivation
- `SXF23679_1_equal_budget_4pi`: PRIVATE_TARGET_NOT_EVIDENCE - `abs(s_XF2)` -> `2.963477300701e-07`; stricter budget only; not a measurement or parent derivation
- `SXF23679_2_alpha_clock_route`: MISSING_SOURCE_AND_ZG_OWNER - `b_alpha_X = 2 z_g - s_XF2` -> `MISSING_ALPHA_CLOCK_BOUND_VALUE`; cannot isolate s_XF2 until z_g is zeroed or jointly fitted
- `SXF23679_3_WEP_R10_route`: MISSING_SOURCE_MAP_AND_ARENA_PROJECTION - `composition/source response from alpha sector` -> `MISSING_ALPHA_SOURCE_COMPOSITION_MAP`; requires material/source projection and z_g bookkeeping
- `SXF23679_4_parent_zg_zero_route`: CONDITIONAL_DIRECT_BOUND_ROUTE - `abs(s_XF2) = abs(b_alpha_X)` -> `MISSING_ZG_ZERO_THEOREM_AND_ALPHA_BOUND`; valid only if parent proves z_g=0 without reintroducing readout/source coefficients

## Alpha/current links
- `ALINK3679_0_canonical_normalization`: DERIVED_FROM_3507 - `g_eff = g_J/sqrt(lambda_A)` -> this is the exact reason F2 and current normalization cannot be treated independently
- `ALINK3679_1_alpha_residual`: DERIVED_IDENTITY - `b_alpha_X = 2 z_g - s_XF2` -> alpha bounds constrain the difference between current drift and F2 drift
- `ALINK3679_2_sXF2_direct_if_zg_zero`: CONDITIONAL_ON_PARENT_OWNER - `z_g=0 => s_XF2=-b_alpha_X` -> this is the cleanest way to convert alpha/clock/WEP evidence into s_XF2 evidence
- `ALINK3679_3_two_knob_if_zg_live`: BOUND_VECTOR_REQUIRED - `z_g live => s_XF2=2z_g-b_alpha_X` -> if z_g survives, the next test must fit or bound the two-dimensional vector rather than hammer only MTS

## Decisions
- `DEC3679_0_unique_F2`: REJECT_ZERO_FOR_NOW - unique-F2/no-XF2 theorem does not close under current parent grammar -> do not circle; carry the finite scalar coefficient forward in canonical units
- `DEC3679_1_progress`: PROMOTE_SXF2_ZG_IDENTITY - the live obstruction is now a two-knob identity, not a vague missing coupling -> attack z_g owner or build a source-backed two-knob bound runner
- `DEC3679_2_best_next`: DERIVATION_FIRST_ROUTE - derive z_g=0 before importing alpha bounds if possible -> next checkpoint should target current owner or alpha bound route
- `DEC3679_3_claim_discipline`: PRIVATE_NONCLAIM - no local-GR, Maxwell, WEP/R10, or public claim -> keep work private and avoid GitHub promotion from this checkpoint

## Claim gates
- `CG3679_0_sXF2_zero`: BLOCKED_NONCLAIM - claim s_XF2=0 because unique-F2/no-XF2 theorem is not parent-signed
- `CG3679_1_sXF2_numeric`: BLOCKED_SOURCE_MISSING - score finite s_XF2 because alpha/clock/WEP source rows and z_g owner are missing
- `CG3679_2_alpha_direct_bound`: BLOCKED_ZG_LIVE - treat alpha bound as direct s_XF2 bound because b_alpha_X=2 z_g-s_XF2 unless z_g=0 is proved
- `CG3679_3_local_GR`: BLOCKED_NONCLAIM - claim local-GR/PPN pass because EM/source coupling residual vector remains open
- `CG3679_4_public_or_github`: BLOCKED_PRIVATE - public/GitHub promotion because private derivation checkpoint only

## Next target
`3680-Y5-R2FR-zg-current-owner-or-alpha-bound-route-for-sXF2.md` via `scripts/Y5_R2FR_3680_zg_current_owner_or_alpha_bound_route_for_sXF2.py`.

## Sources
- `handoff_3678`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3678_NEXT_TARGET.csv` exists=True needle_found=True
- `component_3678`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3678_SEM_COMPONENT_BOUND_REQUIREMENTS.csv` exists=True needle_found=True
- `allocation_3678`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3678_SEM_TARGET_ALLOCATION_ROWS.csv` exists=True needle_found=True
- `proof_3664`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3664_UNIQUE_F2_PROOF_ATTEMPT.csv` exists=True needle_found=True
- `closure_3665`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3665_UNIQUE_F2_CLOSURE_AUDIT.csv` exists=True needle_found=True
- `gates_3528`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3528_UNIQUE_F2_INHERITANCE_GATES.csv` exists=True needle_found=True
- `domain_3528`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3528_OPERATOR_DOMAIN_RESULT.csv` exists=True needle_found=True
- `owner_3620`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3620_EM_SOURCE_OWNER_THEOREM_ATTEMPT.csv` exists=True needle_found=True
- `finite_3620`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3620_FINITE_F2_SOURCE_COEFFICIENT_ROWS.csv` exists=True needle_found=True
- `alpha_identity_3507`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3507_ALPHA_COUPLING_IDENTITY.csv` exists=True needle_found=True
- `owner_gate_3507`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3507_PARENT_OWNER_GATE.csv` exists=True needle_found=True
- `doc_3506`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3506-Y5-R2FR-parent-visible-EM-generator-signature-or-first-constitutive-bound-runner.md` exists=True needle_found=True
- `doc_3620`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3620-Y5-R2FR-EM-source-coupling-owner-or-F2-coefficient-bound.md` exists=True needle_found=True
