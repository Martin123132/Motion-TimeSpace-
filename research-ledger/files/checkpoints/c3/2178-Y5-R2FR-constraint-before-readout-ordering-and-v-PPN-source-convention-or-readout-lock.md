# 2178 - Y5/R2FR Constraint-Before-Readout Ordering And V PPN Source Convention Or Readout Lock

## Current Verdict

2178 makes a real forward cut: it derives the **exact source-normalization contract** that the parent theory must satisfy for the `v` branch to become Newton/PPN rather than a pretty readout shape.

After 2177, the constrained readout is:

`A=T^2=exp(v)`, `B=S=exp(-v)`.

The weak slow-particle readout gives:

`Phi_N=(c^2/2)v`, so `a=-(c^2/2) grad(v)`.

Therefore, with positive `U=GM/r`, Newton requires:

`v=-2U/c^2+O(U^2/c^4)`.

The clean non-GR-import parent-action contract is:

`L_v=-(c^4/32piG)(grad v)^2`, and `L_matter=-rho c^2 v/2`.

Varying that weak-field action gives:

`laplacian(v)=8piG rho/c^2`,

so a point source gives `v=-2GM/(c^2 r)` with `v(infinity)=0`.

That is a sharp target, not a claim. The corpus still has to derive those coefficients from the parent action and prove the same source obeys conservation and matter universality.

The PPN sting in the tail is also now exact. If:

`v=-2x+kappa_v x^2+O(x^3)`, with `x=U/c^2`,

then:

`beta=1+kappa_v/2`.

So gamma is the easier part now; beta lives or dies on whether `kappa_v=0` is derived, gauge-owned, or finite-and-tested.

## Source Register

| source_id | source_path | path_exists | needles_found | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 2177_handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2177-Y5-R2FR-v-only-visible-quotient-readout-owner-or-current-readout-lock.md | True | True | 2177 selects constraint-before-readout plus v source convention as the next gate. | False |
| 2177_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2177_VALIDATION.csv | True | True | 2177 validation passed before 2178 continues the chain. | False |
| 2174_second_class | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2174-Y5-R2FR-Hcore-canonical-bracket-closure-or-auxiliary-route-demotion.md | True | True | 2174 supplies the conditional second-class u-sector elimination pattern. | False |
| 2175_even_u | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2175-Y5-R2FR-parent-even-u-sector-no-source-theorem-or-Iu-Ju-residuals.md | True | True | 2175 shows the I_u/J_u zero route is exact conditional but source seams remain live. | False |
| observer_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\10-observer-map-symplectic-contract.md | True | True | observer contract states the Newton, gamma and beta completion requirements. | False |
| hamiltonian_cell | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\09-hamiltonian-radial-cell-derivation.md | True | True | 09 records that Newton fixes the clock/load side first and PPN still needs beta. | False |
| motion_load_reduction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\02-motion-load-local-GR-reduction.md | True | True | 02 supplies the older weak-field target and parent-principle warning. | False |

## Constraint-Before-Readout Order Contract

| order_id | gate | statement | status | implication | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| ORD2178_0_reduced_phase_space_rule | Dirac/reduced readout ordering | If u≈0 and p_u≈0 form a stable second-class pair and all ordinary observables descend to the reduced phase space, local readout is evaluated after imposing u=0. | EXACT_CONDITIONAL_REDUCTION_RULE | this is the formal ordering route that makes 2177 useful. | False |
| ORD2178_1_current_mechanism | current auxiliary mechanism | 2174 gives a controlled second-class pattern only when A_u is admissible and I_u, J_u, matter, boundary and readout leaks vanish. | CONDITIONAL_ONLY_FROM_2174 | the corpus has a mechanism shape but not a parent theorem. | False |
| ORD2178_2_even_source_support | even/source-free u sector | 2175 proves I_u=J_u=0 only under parent-owned R_u/evenness/no-source-slot premises. | CONDITIONAL_ONLY_FROM_2175 | the source seam is still the biggest danger. | False |
| ORD2178_3_v_readout_link | v-only coframe after reduction | 2177 proves T=exp(v/2) and sqrt(S)=exp(-v/2) on u=0, so current readout can be reconstructed from v after reduction. | EXACT_CONDITIONAL_LINK | no readout rebuild is needed if ordering is parent-signed. | False |
| ORD2178_4_order_gap | parent order status | Current corpus does not yet prove stable reduced phase-space ordering for matter, clocks, photons, orbits, sources and boundary endpoints. | UNSIGNED_PARENT_ORDER | no local-GR or Newton claim is allowed from ordering alone. | False |
| ORD2178_5_failure_mode | current readout lock | If any ordinary observable reads off-shell T or sqrt(S) before u=0, the 2172/1878 coframe obstruction returns. | READOUT_LOCK_RESIDUAL_REQUIRED_IF_ORDER_FAILS | finite residual rows remain live. | False |

## V Newton Source Convention Derivation

| source_id | object | statement | status | implication | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| VS2178_0_constrained_readout | metric/readout shape | On u=0, A=T^2=exp(v) and B=S=exp(-v). | EXACT_FROM_2177 | the local branch has one visible scalar readout variable. | False |
| VS2178_1_slow_particle | Newtonian acceleration from readout | For g_tt=-exp(v)c^2 at weak field and low speed, Phi_N=(c^2/2)v and a=-grad Phi_N=-(c^2/2)grad v. | EXACT_WEAK_FIELD_READOUT | Newton requires a parent source equation for v, not just reciprocal geometry. | False |
| VS2178_2_required_solution | observed mass convention | For a positive U=GM/r convention, Newton requires v=-2U/c^2+O(U^2/c^4), equivalently Phi_N=-U. | REQUIRED_SOURCE_NORMALIZATION | this fixes the sign and amplitude target. | False |
| VS2178_3_action_contract | minimal weak-field v action | If L_v=-(c^4/32piG)(grad v)^2 and L_matter=-rho c^2 v/2 at leading order, variation gives laplacian(v)=8piG rho/c^2. | EXACT_CONDITIONAL_ACTION_DERIVATION | this is the clean non-GR-import source-normalization contract to hunt for in the parent action. | False |
| VS2178_4_point_mass | exterior solution | laplacian(v)=8piG rho/c^2 gives v=-2GM/(c^2 r) outside a point source with v(infinity)=0. | EXACT_CONDITIONAL_POINT_SOURCE | the Newton amplitude follows if the action normalization is parent-derived. | False |
| VS2178_5_current_parent_status | parent v action | Current corpus has not parent-derived the coefficient c^4/32piG, the matter coupling -rho c^2 v/2, or the conservation identity for the same source. | MISSING_PARENT_V_ACTION_NORMALIZATION | 2178 cannot claim Newton; it turns the missing piece into an exact coefficient target. | False |

## V PPN Expansion Gate

| ppn_id | object | statement | status | implication | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PPN2178_0_parameterize_v | weak-field v expansion | Let x=U/c^2 and v=-2x+kappa_v x^2+O(x^3). | EXACT_PARAMETERIZATION | kappa_v captures the first nonlinear source/readout drift. | False |
| PPN2178_1_A_expansion | time component | A=exp(v)=1-2x+(2+kappa_v)x^2+O(x^3). | EXACT_EXPANSION | compare with A=1-2x+2 beta x^2+O(x^3). | False |
| PPN2178_2_beta_law | PPN beta law | beta=1+kappa_v/2 in the constrained v-readout branch. | EXACT_BETA_DRIFT_LAW | beta=1 requires kappa_v=0 or a compensating parent gauge theorem, not wishful thinking. | False |
| PPN2178_3_B_expansion | radial component | B=exp(-v)=1+2x+(2-kappa_v)x^2+O(x^3). | EXACT_EXPANSION | the first-order spatial coefficient gives gamma=1 once v source normalization is fixed. | False |
| PPN2178_4_gamma_law | PPN gamma law | gamma=1 at first order for any finite kappa_v if v=-2U/c^2+O(U^2/c^4). | GAMMA_CONDITIONAL_PASS | gamma is no longer the hardest gate; beta/source/conservation are. | False |
| PPN2178_5_beta_gate | beta and nonlinear source gate | kappa_v must be parent-derived as zero, gauge-removable, or finite-and-tested. | MISSING_KAPPA_V_ZERO_THEOREM | next target should hunt the parent v action normalization and nonlinear beta drift. | False |

## V Source/Order Residual Rows

| row_id | symbol | definition | status | units | observable_link | value | source_path | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VRR2178_0_order | epsilon_order_u_readout | residual if readout happens before u=0 reduction | MISSING_ORDER_THEOREM_OR_BOUND | dimensionless_log_readout_leak | clock;PPN;orbital;local_GR | MISSING_NUMERIC_VALUE | MISSING_SOURCE_PATH | False | False |
| VRR2178_1_source_norm | delta_v_source_norm | relative mismatch in laplacian(v)=8piG rho/c^2 normalization | MISSING_PARENT_SOURCE_NORMALIZATION_OR_VALUE | dimensionless_relative_source_coefficient | Newton;PPN;orbital | MISSING_NUMERIC_VALUE | MISSING_SOURCE_PATH | False | False |
| VRR2178_2_kappa | kappa_v | quadratic weak-field drift in v=-2U/c^2+kappa_v U^2/c^4 | MISSING_KAPPA_V_ZERO_OR_VALUE | dimensionless | PPN_beta;local_GR | MISSING_NUMERIC_VALUE | MISSING_SOURCE_PATH | False | False |
| VRR2178_3_matter | epsilon_v_matter_nonuniversal | species/source mismatch in the v matter coupling | MISSING_MATTER_UNIVERSALITY_ZERO_OR_BOUND | dimensionless_species_norm | WEP;clock;R10;PPN | MISSING_NUMERIC_VALUE | MISSING_SOURCE_PATH | False | False |
| VRR2178_4_boundary | epsilon_v_boundary_endpoint | boundary or endpoint re-entry after v reduction | MISSING_BOUNDARY_ENDPOINT_ZERO_OR_BOUND | boundary_projection_norm | orbital;light_time;PPN | MISSING_NUMERIC_VALUE | MISSING_SOURCE_PATH | False | False |
| VRR2178_5_conservation | epsilon_v_conservation | Bianchi-like source conservation failure in the v equation | MISSING_CONSERVATION_IDENTITY_OR_BOUND | dimensionless_divergence_norm | local_GR;PPN;cosmology | MISSING_NUMERIC_VALUE | MISSING_SOURCE_PATH | False | False |
| VRR2178_6_total | epsilon_v_source_order_abs | absolute no-cancellation envelope for order/source/kappa/matter/boundary/conservation residuals | MISSING_COMPONENT_VALUES | declared_common_norm | all_local_arenas | MISSING_NUMERIC_VALUE | MISSING_SOURCE_PATH | False | False |

## Claim Gate

| gate_id | gate | status | implication | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2178_0_order | constraint-before-readout is parent-signed | UNSIGNED | no claim until reduced phase-space ordering covers ordinary observables | False |
| CG2178_1_source | v source normalization derives laplacian(v)=8piG rho/c^2 | UNSIGNED | no Newton claim until field coefficient and matter coupling are parent-derived | False |
| CG2178_2_gamma | gamma=1 shape after source normalization | CONDITIONAL_PASS | useful but not independently sufficient | False |
| CG2178_3_beta | beta=1 through kappa_v=0 or parent gauge theorem | UNSIGNED | beta remains a hard gate | False |
| CG2178_4_matter | same v couples to all ordinary matter/readout sectors | UNSIGNED | WEP and clock gates remain blocked | False |
| CG2178_5_conservation | Bianchi-like source conservation identity | UNSIGNED | field theory status remains incomplete | False |
| CG2178_6_verdict | Newton/local-GR claim | BLOCKED_NONCLAIM | 2178 supplies exact conditional laws, not a claim | False |

## Decision Ledger

| decision_id | decision | rationale | selection_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2178_0_gain_order | ORDERING_THEOREM_CONTRACT_EXACT | If the u,p_u constraints are parent-stable and observables descend to the reduced phase space, readout-after-u=0 is mathematically legitimate. | selected | False |
| DEC2178_1_gain_source | V_NEWTON_SOURCE_CONVENTION_CONTRACT_DERIVED | A non-GR-import weak-field action with -(c^4/32piG)(grad v)^2 and -rho c^2 v/2 gives laplacian(v)=8piG rho/c^2 and v=-2GM/(c^2r). | selected | False |
| DEC2178_2_gain_ppn | BETA_DRIFT_LAW_DERIVED | With v=-2U/c^2+kappa_v U^2/c^4, the constrained branch gives beta=1+kappa_v/2 while gamma=1 at first order. | selected | False |
| DEC2178_3_no_claim | PARENT_V_ACTION_AND_KAPPA_ZERO_UNSIGNED | The parent source coefficient, matter universality, conservation identity and kappa_v=0 theorem are missing. | selected | False |
| DEC2178_4_next | PARENT_V_ACTION_NORMALIZATION_AND_BETA_ZERO_NEXT | The next leap is to derive the v kinetic/source action and nonlinear beta zero, not to rerun the same readout gate. | selected | False |

## Next Target

| route_id | selection_status | target_file | target_script | objective | success_condition | do_not_do | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT2178_0_2179 | selected | 2179-Y5-R2FR-parent-v-field-action-normalization-and-beta-quadratic-zero-or-finite-row.md | scripts/Y5_R2FR_parent_v_field_action_normalization_and_beta_quadratic_zero_or_finite_row_2179.py | derive the parent weak-field v action normalization, matter source coupling and nonlinear kappa_v=0 beta condition, or demote them to finite residual rows | parent action yields L_v coefficient c^4/32piG, matter coupling -rho c^2 v/2, conservation identity and kappa_v=0 or sourced finite kappa_v row | do not import Einstein equations, do not fit G or beta from tests, do not claim local GR from gamma shape alone | False |
| NEXT2178_1_finite_parallel | held_parallel | 2179b-Y5-R2FR-first-v-source-beta-finite-row-acquisition.md | scripts/Y5_R2FR_first_v_source_beta_finite_row_acquisition_2179b.py | if derivation fails, acquire one finite source-backed delta_v_source_norm or kappa_v row with units and arena projection | one finite row has source path, units, convention, projection and remains nonclaim | do not score placeholder residual rows | False |

## Branch Copies

| copy_id | source_path | target_path | copied | valid_for_claim |
| --- | --- | --- | --- | --- |
| queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2178_V_SOURCE_ORDER_RESIDUAL_ROWS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2178_V_SOURCE_ORDER_RESIDUAL_ROWS_NONCLAIM.csv | True | False |
| branch_wep | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2178_CONSTRAINT_BEFORE_READOUT_ORDER_CONTRACT.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_2178_CONSTRAINT_ORDER_CONTRACT_NONCLAIM.csv | True | False |
| source_weight | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2178_V_NEWTON_SOURCE_CONVENTION_DERIVATION.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\beta-source\docs\V_NEWTON_SOURCE_CONVENTION_2178_NONCLAIM.csv | True | False |

## Validation

| validation_id | status | detail | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- |
| VAL2178_00_sources_exist | PASS | 7/7 sources exist | False | False |
| VAL2178_01_needles_found | PASS | 7/7 source needle sets found | False | False |
| VAL2178_02_order_contract | PASS | constraint-before-readout rule is exact conditional but parent order remains unsigned | False | False |
| VAL2178_03_v_source_derivation | PASS | v Newton source convention derived as a parent-action coefficient contract | False | False |
| VAL2178_04_ppn_expansion | PASS | beta drift law beta=1+kappa_v/2 derived; gamma is conditional | False | False |
| VAL2178_05_residual_rows | PASS | v source/order residual rows=7 remain score_ready=false | False | False |
| VAL2178_06_claim_gate | PASS | local claim remains blocked despite conditional gamma/source gains | False | False |
| VAL2178_07_decision | PASS | decision selects parent v-action and beta-zero target next | False | False |
| VAL2178_08_next_target | PASS | 2179 parent v-action normalization target selected | False | False |
| VAL2178_09_claim_flags_false | PASS | all generated rows keep valid_for_claim=false and claim_allowed=false | False | False |
| VAL2178_10_csv_parse | PASS | P8_Y5_PARENT_QLOC_2178_SOURCE_REGISTER.csv:7; P8_Y5_PARENT_QLOC_2178_CONSTRAINT_BEFORE_READOUT_ORDER_CONTRACT.csv:6; P8_Y5_PARENT_QLOC_2178_V_NEWTON_SOURCE_CONVENTION_DERIVATION.csv:6; P8_Y5_PARENT_QLOC_2178_V_PPN_EXPANSION_GATE.csv:6; P8_Y5_PARENT_QLOC_2178_V_SOURCE_ORDER_RESIDUAL_ROWS.csv:7; P8_Y5_PARENT_QLOC_2178_CLAIM_GATE.csv:7; P8_Y5_PARENT_QLOC_2178_DECISION_LEDGER.csv:5; P8_Y5_PARENT_QLOC_2178_NEXT_TARGET.csv:2; P8_Y5_PARENT_QLOC_2178_BRANCH_COPIES.csv:3 | False | False |
| VAL2178_11_branch_copies | PASS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2178_V_SOURCE_ORDER_RESIDUAL_ROWS_NONCLAIM.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_2178_CONSTRAINT_ORDER_CONTRACT_NONCLAIM.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\beta-source\docs\V_NEWTON_SOURCE_CONVENTION_2178_NONCLAIM.csv | False | False |
| VAL2178_12_formalization_clean | PASS | formalization-workbench has no 2178 artifacts | False | False |
| VAL2178_13_pycache_absent | PASS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\__pycache__ | False | False |
| VAL2178_OVERALL | PASS | 2178 derives the v Newton source convention contract and beta drift law while keeping local-GR claim blocked | False | False |

## Working Interpretation

This is a good kind of narrowing. We are not asking the theory to magically "be GR". We now have a concrete parent-action target:

1. reduce first, so `u=0` is imposed before ordinary readout;
2. produce the weak-field `v` kinetic coefficient `c^4/32piG`;
3. produce the universal matter coupling `-rho c^2 v/2`;
4. prove the nonlinear beta drift coefficient `kappa_v` is zero, gauge, or finite.

That is the leap-forward route. If it works, the local branch starts looking serious. If it fails, the failure is crisp: `delta_v_source_norm` and `kappa_v` become finite residuals that have to face PPN/Newton tests.
