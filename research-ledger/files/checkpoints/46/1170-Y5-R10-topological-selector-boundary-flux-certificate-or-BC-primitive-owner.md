# 1170 — Y5/R10 topological selector boundary-flux certificate or B_C primitive owner

**Current verdict:** 1170 keeps the topological selector alive, but it also exposes the hard obstruction cleanly: `H^3` can kill the local top class, yet Stokes leaves the exact-sector boundary primitive `int_partialD B_C`. Local zero is not proved until `B_C`/`Phi_C` boundary flux is parent-silent or source-bounded.

**Main progress:** the decomposition `J_C = d_D B_C + J_C^top` gives `int_D J_C = int_partialD B_C + int_D J_C^top`. This is a useful sharpening because it separates the cosmological/topological route from the local boundary route instead of mixing them.

**Important correction:** the degree argument cannot be used as a cheap win. `B_C` is naturally a boundary top form, but the weighted-Stokes residual still contains `d_S(F epsilon_C) wedge b_C` when an exact primitive is used. The weight has to be closed or bounded.

**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.

## Source register

| source_id | relative_path | needle | role | exists | needle_found |
| --- | --- | --- | --- | --- | --- |
| SRC1170_0_1169_next | source-intake/mts_residuals/P8_Y5_R10_1169_NEXT_TARGET.csv | NEXT1169_0_1170 | handoff to topological-selector boundary-flux certificate. | True | True |
| SRC1170_1_1169_summary | source-intake/mts_residuals/P8_Y5_BRR545_1169_VALIDATION.csv | V1169_SUMMARY | 1169 validation summary. | True | True |
| SRC1170_2_1169_top | source-intake/mts_residuals/P8_Y5_R10_1169_TOPOLOGICAL_SELECTOR_THEOREM.csv | TOP1169_4_verdict | topological selector best-route verdict. | True | True |
| SRC1170_3_1169_owner | source-intake/mts_residuals/P8_Y5_R10_1169_PARENT_SOURCE_OWNER_ATTEMPT.csv | PSO1169_4_boundary_flux_owner | Phi_C/B_C boundary owner remains missing. | True | True |
| SRC1170_4_1169_closed_weight | source-intake/mts_residuals/P8_Y5_R10_1169_CLOSED_WEIGHT_ZERO_ATTEMPT.csv | CWZ1169_1_closed_weight_route | closed-weight route to test. | True | True |
| SRC1170_5_1169_gate | source-intake/mts_residuals/P8_Y5_R10_1169_CLAIM_GATES.csv | G1169_2_boundary_flux | boundary flux gate remains blocked. | True | True |
| SRC1170_6_274_decomp | 274-lifted-C-sector-form-holonomy-route.md | J_C = dB_C + J_C^{top} | exact plus top-class decomposition. | True | True |
| SRC1170_7_274_CD | 274-lifted-C-sector-form-holonomy-route.md | C_D[D] = N_D^{-1} integral_D J_C | domain observable receiving boundary and top contributions. | True | True |
| SRC1170_8_1020_stokes | 1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md | ETB1020_1_weighted_Stokes_identity | weighted Stokes residual structure. | True | True |
| SRC1170_9_1020_zero | 1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md | ETB1020_2_zero_conditions | zero theorem conditions. | True | True |
| SRC1170_10_1020_bound | 1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md | ETB1020_3_residual_bound | finite bound fallback. | True | True |
| SRC1170_11_207_bianchi | 207-domain-projector-action-and-Bianchi-identity.md | Bianchi closure can be made formal; | stress/Ward guard. | True | True |

## Boundary split theorem

| split_id | object | statement | status | consequence | missing_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BST1170_0_stokes_split | int_D J_C | Using J_C = d_D B_C + J_C^top, the domain charge splits as int_D J_C = int_partialD B_C + int_D J_C^top, with orientation/sign convention fixed later. | DERIVED_STOKES_SPLIT | topology alone never proves local zero unless the boundary primitive term is zero or bounded. | B_C primitive owner, boundary condition, corner audit, units/norm | False |
| BST1170_1_local_top_zero_not_enough | local bounded D | On a contractible bounded local domain, the absolute top class can vanish, but int_partialD B_C can still be nonzero. | LOCAL_ZERO_REDUCED_TO_BOUNDARY | the local branch now lives or dies on Phi_C/B_C boundary flux, not on the topological selector itself. | no-flux/natural-boundary theorem or finite B_C edge bound | False |
| BST1170_2_FLRW_top_survives | closed/global FLRW D | On a closed/global top-class sector with no boundary, int_partialD B_C is absent while int_D J_C^top can survive. | FLRW_COMPATIBLE_WITH_TOPOLOGY | this keeps the desired asymmetry: local top killed by H^3, cosmological top allowed by H^3. | parent normalization and stress-energy of the top class | False |
| BST1170_3_time_evolution_split | L_tau J_C | If L_tau commutes with d_D up to known domain-motion terms, then L_tau J_C = d_D(L_tau B_C) + L_tau J_C^top + motion terms. | FORMAL_EVOLUTION_SPLIT | comparison with L_tau J_C = d_D Phi_C + Sigma_C suggests Phi_C is the exact-sector boundary transport and Sigma_C is the top/source sector. | commutator with moving domain, Phi_C sign convention, parent transport law | False |

## Phi/B_C relation

| relation_id | clause | statement | status | blocks | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PBC1170_0_exact_sector_match | Phi_C relation | Exact-sector matching gives d_D(Phi_C - L_tau B_C - motion_B_C)=0. On a simple local domain this means Phi_C = L_tau B_C + motion_B_C + d_D zeta_C plus possible harmonic 2-form. | RELATION_DERIVED_CONDITIONAL | domain-motion term, harmonic 2-form, and boundary values are not parent-signed | False | False |
| PBC1170_1_no_flux_condition | local no-flux | A sufficient local silence condition is pullback_boundary(Phi_C)=0 and pullback_boundary(B_C)=0, or a parent natural-boundary condition implying the same integrated flux vanishes. | SUFFICIENT_NOT_DERIVED | natural boundary condition from parent action; proof it preserves physical charges | False | False |
| PBC1170_2_finite_bound | finite boundary fallback | If no-flux fails, the local exact-sector contribution is bounded by |int_partialD B_C| <= ||1||_* ||B_C||_* plus weighted-Stokes derivative, harmonic, residual, and corner terms. | BOUND_SCHEMA_READY_VALUES_MISSING | B_C norm, boundary area/norm convention, weighted kernel derivative, harmonic/residual terms | False | False |
| PBC1170_3_charge_guard | do-not-kill-physics guard | Boundary silence cannot be imposed by deleting the physical mass/time/rotation/charge generator; it must be a natural condition on the lifted-C residual sector only. | GUARD_ACTIVE | separation of proper C-boundary gauge from physical Hamiltonian generators | False | False |

## Local zero certificate

| cert_id | requirement | current_status | detail | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| LZC1170_0_top_class | absolute top class vanishes locally | PARTIAL_PASS_FROM_TOPOLOGY | contractible bounded local domains support the H^3 zero part of the selector | False | False |
| LZC1170_1_boundary_primitive | int_partialD B_C = 0 or source-bounded | BLOCKED_MAIN_GAP | Stokes leaves the exact-sector boundary primitive even when top class vanishes | False | False |
| LZC1170_2_boundary_flux | pullback_partialD Phi_C = 0 or source-bounded | BLOCKED | time evolution/no-flux condition is not owned by parent action | False | False |
| LZC1170_3_relative_classes | relative cohomology/corner/harmonic residuals absent or bounded | BLOCKED | absolute H^3 zero does not erase relative or boundary cohomology by itself | False | False |
| LZC1170_4_bianchi | source/flux stress ledger closes | BLOCKED | even a boundary theorem must carry its stress/Ward bookkeeping | False | False |

## Weighted-Stokes C-sector guard

| stokes_id | clause | statement | status | missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| WSC1170_0_C_boundary_degree | C-sector boundary degree | For the C sector, B_C is naturally a 2-form primitive in D whose pullback to the two-surface partialD is top degree. This makes int_partialD B_C meaningful, but not automatically zero. | DEGREE_CLARIFIED | parent B_C construction and pullback convention | False |
| WSC1170_1_weighted_exact_boundary | weighted Stokes residual | If pullback(B_C)=d_S b_C, then int_S F epsilon_C d_S b_C = int_partialS F epsilon_C b_C - int_S d_S(F epsilon_C) wedge b_C. | MATCHES_1020_GUARD | b_C primitive, corner term partialS, d_S(F epsilon_C) zero/bound | False |
| WSC1170_2_degree_zero_limit | degree-zero caution | The fact that d_S of an intrinsic top two-form is zero does not by itself remove the weighted-Stokes derivative term when the exact primitive is written as d_S b_C with scalar/zero-form weight. | NO_FAKE_DEGREE_SHORTCUT | form-degree ledger for F epsilon_C and b_C | False |
| WSC1170_3_zero_or_bound | acceptance rule | The boundary route closes only if corner=0, harmonic/residual=0, and d_S(F epsilon_C)=0, or if every term gets a sourced finite bound. | STRICT_ACCEPTANCE_RULE | numeric/source-backed bound rows or parent zero theorem | False |

## Runner dry-run

| run_id | test | status | result | blocked_by | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RUN1170_0_stokes_split | J_C exact/top split | PASS_DERIVED_SPLIT | int_D J_C splits into boundary primitive plus top-class contribution | none for identity; claim blocked by boundary values | False | False |
| RUN1170_1_local_zero | local topological zero | REFUSED_BOUNDARY_UNSILENCED | H^3 local zero does not erase int_partialD B_C | B_C_boundary;Phi_C_boundary;relative_cohomology;corner_terms | False | False |
| RUN1170_2_FLRW_activity | FLRW top activity | COMPATIBLE_NONCLAIM | closed/global top class can survive with no boundary term | parent_normalization;top_source_stress;amplitude_law | False | False |
| RUN1170_3_weighted_stokes | closed-weight shortcut | REFUSED_DEGREE_SHORTCUT | degree clarifies the forms but does not remove the kernel derivative residual without a degree/weight certificate | dS_Fepsilon;corner;harmonic;residual;b_C_norm | False | False |

## Claim gates

| gate_id | gate | current_status | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| G1170_0_split_identity | Stokes exact/top split | PASS_IDENTITY_ONLY | the split is mathematical, but not a local-physics claim | False | False |
| G1170_1_local_zero | local exact boundary silence | BLOCKED | int_partialD B_C and Phi_C boundary flux remain unsigned | False | False |
| G1170_2_FLRW_selector | FLRW top-class activity | PARTIAL_PASS_NONCLAIM | closed/global top class can exist, but source amplitude and stress are not parent-owned | False | False |
| G1170_3_weighted_stokes | closed-weight/finite-bound route | BLOCKED | kernel derivative, primitive norm, harmonic/residual, and corner terms remain missing | False | False |
| G1170_4_local_promotion | local-GR/R10/PPN/WEP/clock/orbital promotion | BLOCKED_NO_LOCAL_CLAIM | boundary primitive and parent source gates remain open | False | False |

## Decision ledger

| decision_id | decision | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| D1170_0_boundary_is_live_gap | topology_route_survives_but_reduces_to_boundary | local H^3 zero is useful, but Stokes exposes int_partialD B_C as the exact-sector obstruction | derive natural boundary condition for B_C/Phi_C or fill finite B_C bound row | False |
| D1170_1_no_degree_cheat | do_not_use_degree_zero_as_shortcut | top-form degree helps classify B_C, but weighted Stokes still leaves d_S(F epsilon_C) wedge b_C unless the weight is closed | write form-degree/weight certificate before using closed-weight zero | False |
| D1170_2_best_next | attack_parent_natural_boundary_condition | a natural boundary condition would be stronger and cleaner than sourcing finite local bounds | try to derive no-flux from parent variational principle; fallback to first finite boundary source row | False |

## Validation

| check_id | result | detail | claim_allowed |
| --- | --- | --- | --- |
| V1170_0_sources_exist | pass | all cited local source paths exist and needles are found | False |
| V1170_1_stokes_split_written | pass | domain charge split includes boundary primitive and top-class contribution | False |
| V1170_2_phi_bc_relation_written | pass | Phi_C/B_C exact-sector relation is written with caveats | False |
| V1170_3_local_zero_blocked | pass | local zero is explicitly blocked by boundary primitive gap | False |
| V1170_4_weighted_stokes_guard | pass | degree shortcut is rejected unless weighted-Stokes guard is certified | False |
| V1170_5_runner_refuses_claim | pass | runner refuses local and weighted-Stokes claims | False |
| V1170_6_claim_gates_blocked | pass | all claim gates remain nonclaim | False |
| V1170_7_no_claim_rows | pass | all generated science rows remain nonclaim | False |
| V1170_8_next_target | pass | 1171 handoff targets natural boundary condition or first finite bound row | False |
| V1170_9_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work | False |
| V1170_10_formalization_untouched | pass | generator writes no outputs under formalization-workbench | False |
| V1170_SUMMARY | pass | 1170 derives the exact/top Stokes split and shows the topological route now hinges on B_C/Phi_C boundary silence or finite source-backed bounds | False |

## Next target

| next_id | next_target | objective | include | exclude | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT1170_0_1171 | 1171-Y5-R10-natural-boundary-condition-for-BC-or-first-finite-bound-row.md | try to derive a parent natural-boundary/no-flux condition for B_C and Phi_C; if it fails, create the first finite B_C boundary-bound source row | parent variation boundary term; B_C pullback; Phi_C no-flux; physical-charge guard; weighted-Stokes form-degree ledger; finite norm row | assuming B_C=0; deleting physical charges; local claim; c_g zero; invented numeric values; GitHub; formalization edits | False | False |
