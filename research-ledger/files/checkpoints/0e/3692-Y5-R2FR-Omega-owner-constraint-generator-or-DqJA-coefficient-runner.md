# 3692 - Omega-owner constraint generator or Dq/J_A coefficient runner

Private checkpoint. No GitHub action. No R10, PPN, local-GR, Newton, EM, WEP, clock, or orbital claim.

## Status
- `OMEGA_OWNER_CONTRACT_DERIVED_Z_SPLIT_REQUIRED_PARENT_NOT_SIGNED`
- The Omega/constraint route gives an exact vertical-current theorem only for true gauge directions; canonical Z must now be split into vertical chi and physical horizontal y before local-GR suppression can be claimed.

## Main Derivation
- Start with a parent phase/configuration space `Phi`, presymplectic form `Omega=dTheta`, and first-class constraints `C_a(Phi)=0`.
- A proper vertical generator must satisfy `i_e Omega = delta G[epsilon]`, with `G[epsilon]=int_Sigma epsilon^a C_a + int_boundary Q_epsilon`.
- The quotient readout must be a Dirac observable: `{q,C_a}=0`, equivalently `Dq[e_epsilon]=0`.
- If matter/source actions descend as `S_matter+S_source=Sbar[q(Phi),Psi,theta,J_phys]`, and boundary charge is silent, then `delta_e S=0` and the vertical source current vanishes.
- This proves only `J_vertical=0`. It does **not** prove `J_A=0` for every canonical `Z^A` unless those `Z^A` directions are the parent vertical directions.

## Forced Z Split
- The clean law is `Z^A = V^A_a chi^a + H^A_I y^I`.
- Vertical block: `Dq[V_a]=0` and `J_chi,a=V^A_a J_A=0` under the parent Omega/q-descent theorem.
- Horizontal block: `J_y,I=H^A_I J_A` remains physical source response unless an extra symmetry, projection silence, mass gap, or screening mechanism suppresses it.
- Local-GR recovery therefore moves from a fake plateau axiom to a sharper bound: `R_local = M_y L_H^{-1}J_y + N_Dq Dq_H[y] + B_edge + O(y^2)`.

## What This Means
- The coupling problem is now narrowed: decide whether the live MTS `Z` variables are gauge, physical response, or mixed.
- If mixed, only the gauge block gets a zero theorem; the physical block must be bounded by mass gap/screening/projection data.
- This is progress because it stops the theory from smuggling `J_A=0` and gives the exact next derivation target.

## Omega Contract Rows
- `OOT3692_0_parent_space`: parent phase/configuration space | `CONTRACT_FORM_WRITTEN_PARENT_OWNER_MISSING` | Phi carries presymplectic form Omega=dTheta plus first-class constraints C_a(Phi)=0
- `OOT3692_1_generator`: Hamiltonian/Noether generator | `GENERATOR_CONTRACT_DERIVED_BOUNDARY_UNSIGNED` | i_{e_epsilon} Omega = delta G[epsilon], G[epsilon]=int_Sigma epsilon^a C_a + int_boundary Q_epsilon
- `OOT3692_2_quotient_observable`: quotient readout | `VERTICALITY_THEOREM_CONDITIONAL` | q:Phi->Q_phys is a Dirac observable: {q,C_a}=0, equivalently Dq[e_epsilon]=0
- `OOT3692_3_descent_action`: matter/source descent | `SOURCE_ORTHOGONALITY_THEOREM_CONDITIONAL` | S_matter+S_source=Sbar[q(Phi),Psi,theta,J_phys] with J_phys also invariant under e_epsilon
- `OOT3692_4_exact_theorem`: exact Omega-owner theorem | `EXACT_CONTRACT_DERIVED_NOT_PARENT_SIGNED` | If OOT3692_0..3 hold and boundary charge is silent, then e_epsilon=Omega^-1 DCdagger[epsilon] lies in ker(Dq) and J_vertical=0
- `OOT3692_5_no_magic`: anti-smuggling clause | `Z_SPLIT_FORCED_BY_THEOREM` | J_A=0 cannot be asserted for every canonical Z^A unless partial_ZA is inside ker(Dq) or is projected onto the vertical subbundle

## Z Split Rows
- `ZS3692_0_split`: vertical-horizontal split | `SPLIT_LAW_DERIVED` | Z^A = V^A_a chi^a + H^A_I y^I
- `ZS3692_1_vertical_current`: pure gauge current | `CONDITIONAL_ZERO_FOR_VERTICAL_CURRENT` | J_chi,a = V^A_a J_A
- `ZS3692_2_horizontal_current`: physical response current | `HORIZONTAL_CURRENT_REMAINS_LIVE` | J_y,I = H^A_I J_A
- `ZS3692_3_local_GR_gate`: local GR gate | `Z_SPLIT_REQUIRED_BEFORE_LOCAL_GR_CLAIM` | R_local = M_y L_H^{-1} J_y + N_Dq Dq_H[y] + B_edge + O(y^2)
- `ZS3692_4_interpretation`: coupling knot | `COUPLING_PROBLEM_REDUCED_TO_BASIS_AND_MASS_GAP` | the coupling is not one missing number; it is the choice of whether canonical Z is gauge, physical response, or mixed

## Dq/J_A Runner Rows
- `DQR3692_0_DqV`: `Dq_V_norm` | `BLOCKED_UNTIL_PARENT_Q_OMEGA_SUPPLIED` | Dq_V_norm := ||Dq[V]||/||V||
- `DQR3692_1_DqH`: `Dq_H_norm` | `ACQUISITION_ROW_READY_VALUES_MISSING` | Dq_H_norm := ||Dq[H]||/||H||
- `DQR3692_2_Jvertical`: `J_chi` | `CONDITIONAL_ZERO_VALUES_MISSING` | J_chi = V^A_a J_A
- `DQR3692_3_Jhorizontal`: `J_y` | `ACQUISITION_ROW_READY_VALUES_MISSING` | J_y = H^A_I J_A
- `DQR3692_4_mass_gap`: `L_H_inverse` | `MISSING_MASS_GAP_OR_SCREENING_BOUND` | ||y|| <= ||L_H^{-1}|| ||J_y|| + boundary + O(J_y^2)
- `DQR3692_5_arena_score`: `R_local_horizontal` | `SCORING_FORM_READY_NUMERIC_INPUTS_MISSING` | R_local <= ||M_y||||L_H^{-1}||||J_y|| + ||N_Dq||||Dq_H||||y|| + ||B_edge||

## Claim Gates
- `CG3692_0_vertical`: `BLOCKED` - Dq[e]=0 is theorem-derived but not parent-owned
- `CG3692_1_JA_zero`: `BLOCKED` - J_A=0 applies only to vertical block, not to physical horizontal response
- `CG3692_2_local_GR`: `BLOCKED` - local GR needs horizontal response suppression/projection after Z split
- `CG3692_3_public`: `BLOCKED` - private derivation checkpoint only; no public claim

## Decisions
- `DEC3692_0`: `ADOPT_AS_PARENT_CONTRACT_NOT_AS_CLAIM` - Use Omega-owner constraint generator as the clean route: e=Omega^-1 DCdagger, Dq[e]=0, J_vertical=0.
- `DEC3692_1`: `NEXT_DERIVATION_REQUIRED` - Stop treating all Z components as one thing; split Z=V chi + H y.
- `DEC3692_2`: `LOCAL_GR_ROUTE_REFINED` - Do not demand J_y=0 unless extra symmetry exists; derive mass-gap/screening/projection bound for y.

## Source Register
- `handoff_3691`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3691_NEXT_TARGET.csv`
- `vertical_3691`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3691_VERTICAL_QMAP_GATE_ROWS.csv`
- `orthogonality_3691`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3691_SOURCE_ORTHOGONALITY_ROWS.csv`
- `coefficients_3691`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3691_JA_COEFFICIENT_ACQUISITION_ROWS.csv`
- `dcdagger_3631`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3631_DCDAGGER_VERTICAL_GENERATOR_MAP.csv`
- `vertical_3631`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3631_VERTICAL_GENERATOR_TEST.csv`
- `source_identity_2642`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_SOURCE_CURRENT_IDENTITY_2642_PROOF_ATTEMPT.csv`
- `leak_bound_2643`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_COMMON_DESCENT_DQZ_2643_DQZ_JH_LEAK_BOUND_ROWS.csv`

## Next Target
- `3693-Y5-R2FR-vertical-horizontal-Z-split-and-local-mass-gap-suppression.md`
- Objective: derive the Z=V chi+H y split, prove J_chi=0 under Omega/q descent, then derive or bound ||L_H^{-1}J_y|| and its PPN/Newton/R10/clock/WEP/EM/orbital residuals
