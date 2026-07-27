# 3693 - Vertical-horizontal Z split and local mass-gap suppression

Private checkpoint. No GitHub action. No public local-GR/Newton/R10/PPN/EM claim.

## Status
- `VERTICAL_HORIZONTAL_SPLIT_DERIVED_HORIZONTAL_LOCAL_SUPPRESSION_BOUND_STAGED`
- The local branch is no longer a plateau axiom. The vertical block has a conditional zero theorem; the horizontal block has a concrete coercivity/Yukawa suppression gate that can be scored once mu_H, J_y, Dq_H, projections and arena tolerances are sourced.

## Derivation
- Split the canonical response variable using the clean response-sector pairing: `T_Z F = V_Z \oplus H_Z`, with `V_Z:=im(R_C)` and `H_Z` the gauge-fixed complement.
- Write `Z^A = V^A_a chi^a + H^A_I y^I`, with projectors `P_V` and `P_H`.
- The Omega/q theorem gives `Dq[P_V Z]=0`; therefore `Dq[Z]=Dq[P_H Z]`.
- If matter/source/boundary data descend through the quotient, `J_chi=P_V^T J=0`; this is the exact zero theorem but only for the vertical gauge block.
- The horizontal current `J_y=P_H^T J` remains physical. It must be killed by extra symmetry, projection silence, or bounded by a mass gap/screening mechanism.

## Horizontal Operator
- Start from `L_AB Z^B := -D_mu(G_AB D^mu Z^B)+M_AB Z^B+O(Z^2)`.
- Gauge-fix/quotient first, then define `L_H := P_H^T L P_H`; include the Schur complement if vertical-horizontal mixing remains.
- If `<y,L_eff,H y> >= kappa_D ||D y||^2 + mu_H^2 ||y||^2 - R_domain ||y||^2`, then `||y|| <= C_H ||J_y+B_y|| + ||y_boundary|| + O(J_y^2)`.

## Local Suppression Law
- Main gate: `A_loc <= (||M_y||+||N_Dq||||Dq_H||) C_H ||J_y+B_y||/N_GR + ||B_edge||/N_GR`.
- Massive/Yukawa interface: `|R_A(r)|/|R_GR(r)| <= |alpha_A| exp(-r/ell_H)(1+r/ell_H)+R_edge_A+R_proj_A`, with `ell_H=1/mu_H`.
- Concrete transition ratio: `ell_H/L_cg <= (r_A/L_cg)/ln(|alpha_A|/epsilon_A)` when `|alpha_A|>epsilon_A` and edge/projection terms are subdominant.

## Why This Matters
- This is the cleanest non-smuggled route to local GR so far: vertical pieces can vanish by theorem; horizontal pieces must be quantitatively screened or projected.
- It keeps the field-theory route alive without pretending the coupling problem has disappeared.
- The next pressure point is `mu_H^2=lambda_min(G_H^-1 M_H)` and whether the parent action derives a local/environmental mass gap.

## Split Theorem Rows
- `ZST3693_0_field_space`: linearized canonical response space | `FORMAL_SPLIT_DERIVED_PARENT_BASIS_UNSIGNED` | T_Z F = V_Z ⊕ H_Z with V_Z:=im(R_C) and H_Z chosen G-orthogonal to V_Z after gauge fixing
- `ZST3693_1_projectors`: projector algebra | `PROJECTOR_LAW_DERIVED_REGULARITY_UNSIGNED` | P_V^2=P_V, P_H^2=P_H, P_V P_H=0, P_V+P_H=1 on the gauge-fixed response domain
- `ZST3693_2_vertical_readout`: vertical q silence | `VERTICAL_DQ_ZERO_CONDITIONAL` | Dq[P_V Z]=0 and Dq[Z]=Dq[P_H Z]
- `ZST3693_3_vertical_current`: vertical source current | `JCHI_ZERO_THEOREM_CONDITIONAL` | J_chi := P_V^T J = 0 under q-descent, source-current descent, and silent/proper boundary charge
- `ZST3693_4_horizontal_current`: horizontal source current | `JY_REMAINS_LIVE` | J_y := P_H^T J is not killed by gauge descent

## Horizontal Operator Rows
- `HOP3693_0_full_operator`: full response operator | `FORMAL_OPERATOR_AVAILABLE_PARENT_OWNER_UNSIGNED` | L_AB Z^B := -D_mu(G_AB D^mu Z^B)+M_AB Z^B+O(Z^2)
- `HOP3693_1_horizontal_operator`: horizontal block | `HORIZONTAL_OPERATOR_DEFINED` | L_H := P_H^T L P_H after gauge fixing and boundary-domain restriction
- `HOP3693_2_schur_mixing`: vertical-horizontal mixing | `MIXING_ACCOUNTED_NOT_NUMERIC` | L_eff,H = L_HH - L_HV L_VV^+ L_VH if the gauge-fixed block has residual algebraic mixing
- `HOP3693_3_coercivity`: mass gap/coercivity | `COERCIVITY_CONDITION_DERIVED_NUMERIC_GAP_MISSING` | <y,L_eff,H y> >= kappa_D ||D y||^2 + mu_H^2 ||y||^2 - R_domain ||y||^2
- `HOP3693_4_inverse_bound`: horizontal Green bound | `GREEN_BOUND_DERIVED_NUMERIC_INPUTS_MISSING` | ||y||_X <= C_H ||J_y+B_y||_{X*} + ||y_boundary||_X + O(||J_y||^2)

## Suppression Law Rows
- `SPL3693_0_exact_silence`: exact horizontal silence | `SUFFICIENT_CONDITION_FORMAL_NOT_SIGNED` | J_y+B_y=0 or M_y=N_Dq=0 on the local arena
- `SPL3693_1_norm_bound`: operator-norm suppression | `LOCAL_SUPPRESSION_BOUND_DERIVED_VALUES_MISSING` | A_loc <= (||M_y||+||N_Dq||||Dq_H||) C_H ||J_y+B_y||/N_GR + ||B_edge||/N_GR
- `SPL3693_2_yukawa_kernel`: massive local kernel | `YUKAWA_INTERFACE_DERIVED_ALPHA_ELL_VALUES_MISSING` | |R_A(r)|/|R_GR(r)| <= |alpha_A| exp(-r/ell_H)(1+r/ell_H)+R_edge_A+R_proj_A
- `SPL3693_3_transition_ratio`: local/cosmological length separation | `ELL_RATIO_GATE_DERIVED_VALUES_MISSING` | ell_H/L_cg <= (r_A/L_cg)/ln(|alpha_A|/epsilon_A) when |alpha_A|>epsilon_A and edge/projection terms are subdominant
- `SPL3693_4_environmental_gap`: density/arena dependent gap | `ENVIRONMENTAL_SCREENING_ROUTE_IDENTIFIED_NOT_CLAIMED` | mu_H^2(local)=lambda_min(G_H^{-1}M_H)[rho_local,theta,J_phys] and mu_H^2(cosmic)=lambda_min(...)[rho_cosmic]

## Arena Gates
- `ASG3693_0_PPN`: PPN gamma/beta/preferred-frame | `NEEDS_PPN_PROJECTION_NUMBERS` | A_PPN := |Delta gamma|+|Delta beta|+sum_i |Delta alpha_i|+|Delta xi|
- `ASG3693_1_Newton_R10`: Newton/R10 short-range | `NEEDS_REAL_ALPHA_BOUND_AND_K_N` | alpha_eff(lambda=ell_H) := K_N (||M_y||+||N_Dq||||Dq_H||) C_H ||J_y||
- `ASG3693_2_clocks_WEP_Gdot`: clock/WEP/Gdot | `NEEDS_SPECIES_AND_CLOCK_PROJECTIONS` | A_clock/WEP := K_clock/WEP C_H ||J_y|| + K_Dq Dq_H C_H ||J_y||
- `ASG3693_3_EM_Maxwell`: Maxwell/EM stress | `NEEDS_EM_STRESS_AND_CHARGE_NORMALIZATION` | A_EM := ||Delta T_EM||/||T_EM|| <= K_EM C_H||J_y^EM|| + K_charge |beta_source_alpha|
- `ASG3693_4_orbital`: orbital/ephemeris | `NEEDS_ORBITAL_KERNEL_AND_SOURCE_PROFILE` | A_orb := |delta a_r/a_N|+|delta dot_omega|/dot_omega_bound

## Decisions
- `DEC3693_0`: `ADOPTED_FOR_PRIVATE_FRAMEWORK` - All future local-GR claims must be stated on the horizontal quotient block; vertical zero theorem alone is insufficient.
- `DEC3693_1`: `NEXT_HIGH_VALUE_TARGET` - Derive or source mu_H^2=lambda_min(G_H^-1 M_H) and its environmental dependence from the parent action.
- `DEC3693_2`: `PLATEAU_AXIOM_AVOIDED` - The local vacuum plateau is replaced by either exact projection silence or a quantified Green/Yukawa suppression bound.

## Claim Gates
- `CG3693_0_vertical_zero`: `BLOCKED` - J_chi=0 is conditional on parent Omega/q/source/boundary descent
- `CG3693_1_horizontal_suppression`: `BLOCKED` - J_y suppression needs mu_H, C_H, projections and source norms
- `CG3693_2_local_GR`: `BLOCKED` - local GR not claimed until A_loc <= epsilon_A in PPN/Newton/R10/clocks/WEP/EM/orbital arenas
- `CG3693_3_public`: `BLOCKED` - private checkpoint; no GitHub/public claim

## Source Register
- `handoff_3692`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3692_NEXT_TARGET.csv`
- `split_3692`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3692_VERTICAL_HORIZONTAL_Z_SPLIT_ROWS.csv`
- `runner_3692`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3692_DQJA_COEFFICIENT_RUNNER_ROWS.csv`
- `omega_3692`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3692_OMEGA_OWNER_CONTRACT_ROWS.csv`
- `clean_action_3686`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3686-Y5-R2FR-GK-q_loc-action-existence-Helmholtz-or-RGK-action-bound-row.md`
- `helmholtz_3687`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3687-Y5-R2FR-clean-response-action-Helmholtz-matrix-or-DeltaK-bound-row.md`
- `green_3690`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3690-Y5-R2FR-canonical-source-coupling-JA-zero-theorem-or-Green-profile-bound.md`
- `arena_3690`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3690_JA_ARENA_TEMPLATE_ROWS.csv`

## Next Target
- `3694-Y5-R2FR-horizontal-mass-gap-parent-origin-or-arena-Yukawa-bound-runner.md`
- Objective: derive mu_H^2=lambda_min(G_H^-1 M_H) from the parent action or convert it into arena-specific Yukawa/nonclaim rows for PPN, Newton/R10, clocks, WEP, EM and orbital tests
