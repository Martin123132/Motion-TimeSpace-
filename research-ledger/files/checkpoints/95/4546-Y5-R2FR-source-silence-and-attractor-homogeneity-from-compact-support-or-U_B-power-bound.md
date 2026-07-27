# 4546 - Source silence and attractor homogeneity from compact support or U_B power bound

Generated: `2026-07-06T10:13:18.797382+00:00`  
Marker: `PPC4161_SOURCE_SILENCE_AND_ATTRACTOR_HOMOGENEITY_FROM_COMPACT_SUPPORT_OR_UB_POWER_BOUND_4546`  
Decision: `STATIC_SOURCE_AND_ML_HOMOGENEITY_EXACT_ZERO_CONDITIONAL_UB2_BOUND_IMPORTED_ACTIVE_NONCLAIM`  
Claim: `L-388` remains private, conditional and nonclaim.

## What Moved

4545 made the time-derivative part of the local branch quieter. 4546 attacks the static leftovers:

```text
P_loc[U_B S_cg],
P_loc[D_m Delta_h m_L].
```

The exact-zero route is simple but not yet parent-owned:

```text
U_B=0 or S_cg=0  ->  P_loc[U_B S_cg]=0,
m_L=constant     ->  P_loc[D_m Delta_h m_L]=0.
```

The useful finite route is now sharper. If the local leakage coordinate satisfies

```text
D_L = U_B H_L,       ||H_L|| <= C_H,
```

and the coarse source is regular/silent at the local fixed point,

```text
S_cg(D_L,Y) = D_L S_1(Y) + O(D_L^2),
```

then:

```text
||P_loc[U_B S_cg]|| <= C_H A_1 U_B^2 + O(U_B^3).
```

For the attractor, if the local branch is even/smooth around the trivial leakage class,

```text
m_L = m_* + D_L^2 m_2 + O(D_L^3),
```

then, in the far-local collar:

```text
|D_m Delta_h m_L| <= D_m C_lap_m epsilon_U^2 / L_B^2.
```

So 4546 does not solve local GR, but it upgrades the static leftovers from open prose to an explicit residual vector:

```text
||P_loc J_res_static||
 <= C_H A_1 epsilon_U^2
  + D_m C_lap_m epsilon_U^2/L_B^2
  + ||P_loc boundary_in_static||
  + O(epsilon_U^3).
```

That is a real next scorer/bound object.

## Exact Zero Theorem

| theorem_id | target | statement | proof | current_status | why_not_claim | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EZ4546_0_source_exact_zero | P_loc[U_B S_cg]=0 | Exact source silence follows if U_B=0 on the compact local collar, or S_cg=0 on the local source kernel, or a parent projector identity kills P_loc S_cg. | Substitution in R_source=U_B S_cg. | not_parent_signed | logistic screening gives small U_B, not exact zero; S_cg kernel/projector theorem remains unsigned | False | False |
| EZ4546_1_attractor_exact_homogeneity | P_loc[D_m Delta_h m_L]=0 | Exact attractor homogeneity follows if the compact local branch has a trivial leakage class D_L=0 and m_L=m_* is spatially constant over the tested collar. | If m_L is constant, D_m Delta_h m_L=0. | not_parent_signed | local trivial class and spatially constant branch are conditional, not parent-owned | False | False |
| EZ4546_2_joint_local_Jres_zero | static P_loc J_res | If EZ4546_0, EZ4546_1 and boundary amplitude silence all hold, the static part of P_loc J_res vanishes. | P_loc J_res = P_loc[U_B S_cg] + P_loc[D_m Delta_h m_L] - P_loc[D_t m_L] + P_loc[boundary_in]; 4545 supplies conditional D_t m_L=0. | blocked_by_boundary_and_parent_signature | boundary amplitude and exact source/homogeneity clauses remain unsigned | False | False |


## U_B^2 Source Bound

| bound_id | quantity | formula | derivation | needed_inputs | current_status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UB24546_0_power_convention | R_source | R_source = U_B S_cg; if S_cg = U_B^p_int S_* then R_source = U_B^(1+p_int) S_* | Direct from 1752/1753 bookkeeping. | p_int and \|\|S_*\|\| in shared source norm | exact_bookkeeping | False | False |
| UB24546_1_linear_silence | source leakage | If S_cg(D_L,Y)=D_L S_1(Y)+O(D_L^2), D_L=U_B H_L, \|\|H_L\|\|<=C_H, \|\|S_1\|\|<=A_1, then \|\|P_loc[U_B S_cg]\|\| <= C_H A_1 U_B^2 + O(U_B^3). | Regular source map around the local fixed branch plus leakage-distance lock. | source-silent fixed point, regularity, C_H, A_1, shared norm and arena projection | conditional_theorem_imported_and_current_chain_bound | False | False |
| UB24546_2_envelope_epsilon | source amplitude envelope | If U_B <= epsilon_U on D_loc, then \|\|P_loc[U_B S_cg]\|\| <= C_H A_1 epsilon_U^2 + O(epsilon_U^3). | Take the supremum over D_loc. | epsilon_U, C_H, A_1 and local domain D_loc | formula_ready_values_missing | False | False |


## m_L Homogeneity Bound

| bound_id | quantity | formula | derivation | needed_inputs | current_status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ML4546_0_moving_extremum | m_L-m_* | If m_L=m_*+D_L^2 m_2+O(D_L^3), D_L=U_B H_L, \|\|H_L\|\|<=H0 and \|\|m_2\|\|<=M20, then \|m_L-m_*\| <= epsilon_U^2 H0^2 M20 + O(epsilon_U^3). | Even/smooth local attractor around the trivial leakage class. | H0, M20, epsilon_U and proof of quadratic/even attractor dependence | conditional_U_B2_amplitude_bound | False | False |
| ML4546_1_gradient | \|grad m_L\| | \|grad m_L\| <= C_grad_m epsilon_U^2/L_B under far-local bounds grad U_B=O(U_B/L_B), grad H_L=O(1/L_B), grad m_2=O(M21/L_B). | Differentiate m_L=m_*+U_B^2 H_L^2 m_2 and use far-local gradient scaling. | C_grad_m, L_B or the detailed H0/H1A/M20/M21A constants from 1975/1978 | new_current_chain_gradient_bound_shape | False | False |
| ML4546_2_laplacian | \|D_m Delta_h m_L\| | \|D_m Delta_h m_L\| <= D_m C_lap_m epsilon_U^2/L_B^2 in the far-local collar, with transition-shell U_B=O(1) excluded. | Apply the same U_B^2 regularity to second spatial derivatives and multiply by D_m. | D_m, C_lap_m, L_B, domain regularity and transition-shell quarantine | first_explicit_static_attractor_homogeneity_bound | False | False |


## Static J_res Budget

| budget_id | budget | applies_to | closed_terms | retained_terms | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SJ4546_0_static_budget | \|\|P_loc J_res_static\|\| <= C_H A_1 epsilon_U^2 + D_m C_lap_m epsilon_U^2/L_B^2 + \|\|P_loc boundary_in_static\|\| + O(epsilon_U^3) | static source leakage and attractor homogeneity after 4545 derivative silence | P_loc[D_t m_L] conditional zero from 4545 | boundary amplitude, source constants, spatial-gradient constants | False | False |
| SJ4546_1_exact_zero_branch | P_loc J_res_static=0 if U_B=0, S_cg kernel zero, m_L spatially constant, and boundary_in=0 all hold as parent theorems. | strict compact local zero branch | none promoted as current claim | all parent signatures required | False | False |
| SJ4546_2_transition_shell_warning | U_B^2 far-local bounds cannot be used inside transition shells where U_B=O(1); those require exact projector cancellation or quarantine. | screening transition/local-vacuum collar boundaries | none | transition-shell current and boundary amplitude | False | False |


## Input Requirements

| input_id | symbol | definition | status | needed_for | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REQ4546_0_epsilon_U | epsilon_U | sup_Dloc U_B | missing_local_range_or_parent_bound | numeric source and m_L U_B^2 envelopes | False |
| REQ4546_1_source_norm | C_H, A_1 | D_L/U_B bound and first source-map coefficient norm | missing_parent_signature_and_source_norm | \|\|P_loc[U_B S_cg]\|\| <= C_H A_1 epsilon_U^2 | False |
| REQ4546_2_gradient_scale | L_B, C_grad_m, C_lap_m | far-local environmental length and derivative constants for m_L | missing_numeric_or_theorem_bound | P_loc[D_m Delta_h m_L] bound | False |
| REQ4546_3_boundary_static | \|\|P_loc boundary_in_static\|\| | static trace/shear/vector boundary amplitude after derivative silence | retained_from_4545 | full P_loc J_res_static budget | False |
| REQ4546_4_worldtube_profile | W_src/J_q shared profile | one source profile feeding R10, PPN, clock, orbital and local-GR arenas | template_exists_no_profile | arena projections without retuning | False |


## Claim Gates

| claim_gate_id | gate | status | meaning | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG4546_0_source_exact_zero | P_loc[U_B S_cg]=0 | BLOCKED_EXACT_ZERO_NOT_PARENT_SIGNED | exact zero needs U_B=0, source-kernel silence or parent projector identity | False | False |
| CG4546_1_source_UB2_bound | source U_B^2 finite bound | PASS_FORMULA_NONCLAIM | conditional U_B^2 theorem is now imported into the current chain, but constants are missing | False | False |
| CG4546_2_mL_homogeneity | P_loc[D_m Delta_h m_L] | PASS_BOUND_SHAPE_NONCLAIM | first explicit U_B^2 spatial/laplacian bound shape is written | False | False |
| CG4546_3_local_GR | full local GR/Newton/PPN | BLOCKED_BOUNDARY_AND_NUMERIC_PROJECTION_INPUTS | static residual budget is improved but not yet projected/numeric/claim-safe | False | False |


## Decision

| decision_id | decision | meaning | next_action | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC4546_0 | STATIC_SOURCE_AND_ML_HOMOGENEITY_EXACT_ZERO_CONDITIONAL_UB2_BOUND_IMPORTED_ACTIVE_NONCLAIM | 4546 closes the algebraic shape of the two static leftovers. Exact zero remains conditional, but the finite branch now has source and attractor-homogeneity residuals suppressed as U_B^2 under a regular leakage-coordinate theorem. The next step is projection/numeric acquisition, not another broad missing-input loop. | 4547-Y5-R2FR-local-static-residual-vector-projection-to-PPN-Gdot-R10-or-first-numeric-Ubound-row.md | False | False |


## Next Target

| next_id | target | objective | derive_first | fallback | avoid | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NT4546_0 | 4547-Y5-R2FR-local-static-residual-vector-projection-to-PPN-Gdot-R10-or-first-numeric-Ubound-row.md | project the 4546 static residual vector into PPN/Gdot/R10 rows or fill the first numeric epsilon_U/source-norm bound row | turn SJ4546_0 into arena residual formulas with shared source profile and no retuning | acquire epsilon_U, C_H A_1, D_m C_lap_m/L_B^2 and boundary_static as explicit nonclaim numeric rows | claiming local GR from U_B^2 formulas without constants and arena kernels | False |


## Status

| timestamp_utc | branch_id | checkpoint_id | result | source_exact_zero_parent_signed | source_UB2_bound_written | mL_exact_homogeneity_parent_signed | mL_spatial_UB2_bound_written | static_Jres_budget_written | numeric_projection_ready | public_local_GR_claim_allowed | next_target | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-06T10:13:18.594803+00:00 | MTS_R2FR_Y5_SOURCE_SILENCE_ATTRACTOR_HOMOGENEITY_4546 | 4546 | STATIC_SOURCE_AND_ML_HOMOGENEITY_EXACT_ZERO_CONDITIONAL_UB2_BOUND_IMPORTED_ACTIVE_NONCLAIM | False | True | False | True | True | False | False | 4547-Y5-R2FR-local-static-residual-vector-projection-to-PPN-Gdot-R10-or-first-numeric-Ubound-row.md | False | False |


## Source Register

| checkpoint | source_id | label | path | exists | needle | needle_found | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4546 | SRC4546_00_4545_status | 4545 status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4545_STATUS.csv | True | source_static_amplitude_closed | True | imports the remaining source/homogeneity gaps | False |
| 4546 | SRC4546_01_4545_retained | 4545 retained residuals | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4545_RETAINED_RESIDUALS.csv | True | P_loc[D_m Delta_h m_L] | True | selects static source and spatial attractor residuals | False |
| 4546 | SRC4546_02_1752_support_audit | 1752 source-support audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1752_SOURCE_SUPPORT_ZERO_BOUND_AUDIT.csv | True | R_source = (1-Pi_B) S_cg = U_B S_cg | True | defines source residual and exact conditional finite bound | False |
| 4546 | SRC4546_03_1753_power_convention | 1753 source-power convention | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1753_SOURCE_POWER_CONVENTION_AUDIT.csv | True | p_total=1+p_int | True | prevents double-counting U_B powers | False |
| 4546 | SRC4546_04_1754_silence_attempt | 1754 source silence attempt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1754_SOURCE_SILENCE_THEOREM_ATTEMPT.csv | True | \|\|R_source\|\| <= C_H A_1 U_B^2 | True | imports U_B^2 source-residual theorem shape | False |
| 4546 | SRC4546_05_1754_ZL_contract | 1754 Z_L/D_L contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1754_ZL_DL_LEAKAGE_VECTOR_CONTRACT.csv | True | D_L=sqrt | True | imports D_L=U_B H_L distance-bound route | False |
| 4546 | SRC4546_06_1975_envelope | 1975 U_B suppression envelope | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1975_UB_SUPPRESSION_BOUND_ENVELOPE.csv | True | U_B S_cg amplitude | True | imports source and m_L U_B^2 bound formulas | False |
| 4546 | SRC4546_07_1978_mL_inputs | 1978 m_L derivative inputs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1978_ML_DERIVATIVE_ENVELOPE_INPUTS.csv | True | mL_A_bar | True | imports m_L derivative envelope and missing constants | False |
| 4546 | SRC4546_08_2224_Scg_gate | 2224 S_cg provenance gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2224_SCG_TERM_PROVENANCE_GATE.csv | True | S_cg_norm <= 1/2*T_source_norm*C_qm | True | keeps S_cg finite provenance noncomputable until source terms are filled | False |
| 4546 | SRC4546_09_2224_worldtube | 2224 worldtube profile gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2224_WORLDTUBE_PROFILE_GATE.csv | True | one compact profile should feed all local arenas | True | prevents per-arena retuning of source support | False |


## Validation

| validation_id | status | detail |
| --- | --- | --- |
| VAL4546_00_sources | PASS | all source paths exist and needles found |
| VAL4546_01_exact_zero_honest | PASS | exact zero theorem is stated but not promoted |
| VAL4546_02_source_UB2 | PASS | source U_B^2 finite bound written |
| VAL4546_03_mL_laplacian | PASS | m_L spatial/laplacian U_B^2 bound written |
| VAL4546_04_static_budget | PASS | static Jres budget retains boundary amplitude |
| VAL4546_05_requirements | PASS | missing numeric/profile inputs are explicit and nonclaim |
| VAL4546_06_claim_firewall | PASS | local GR remains blocked until constants/projections/boundary rows close |
| VAL4546_07_csv_parse | PASS | all generated CSV files parse and have rows |
| VAL4546_08_pycache_absent | PASS | scripts __pycache__ absent after cleanup |
| VAL4546_OVERALL | PASS | 4546 source silence and attractor homogeneity exact-zero/U_B^2 bound |

