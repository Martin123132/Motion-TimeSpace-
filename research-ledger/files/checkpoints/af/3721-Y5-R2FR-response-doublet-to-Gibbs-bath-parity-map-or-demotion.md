# 3721 — Response Doublet to Gibbs Bath Parity Map or Demotion

## Status
- `CONDITIONAL_BRIDGE_THEOREM_BUILT_RAW_FREE_ENERGY_GUARD_ADDED`
- The bridge can be made mathematically clean if `z=Z`, exchange is exact parity, and the positive operator is the KL/Legendre Hessian.
- Current MTS is not promoted: component map, unit map, operator equality, identifiability, and boundary/source silence remain unsigned.

## Main Result
- Conditional bridge: `z=Z=(R_+-R_-)/2`, `R_z=exchange`, and `q=q(R_even)` make the Fisher fibre a vertical response-doublet direction.
- Even action result: if `Gamma_eff=Gamma0+0.5 M_AB z^A z^B+O(z^4)` with no odd source/boundary term, then `F_1=0` and `B_QK=0` over the q patch.
- Positive gap result: `Psi_KL=Theta_H D_KL` gives Hessian `Theta_H I_H`; matching requires `M_AB=Theta_H I_AB+DeltaM_map` in the same unit basis.
- Sign guard: raw `-Theta log Z` is not automatically the positive KL penalty; its Hessian is `<A_AB>-(1/Theta)Cov(A_A,A_B)`.

## Bridge Theorems
- `THM3721_0_coordinate_identification` `CONDITIONAL_EXACT`: Assume z^A := Z^A=(R_+^A-R_-^A)/2 for every active local leakage component. Result: Then exchange E:R_+<->R_- acts as z^A -> -z^A.
- `THM3721_1_quotient_invisibility` `CONDITIONAL_EXACT`: Assume q=q(R_even) and R_even=(R_++R_-)/2. Result: Then Dq[partial_z]=0: z is a vertical/fibre coordinate, not an observed local matter/clock/EM variable.
- `THM3721_2_even_action_double_zero` `CONDITIONAL_EXACT`: Assume Gamma_eff(q,z)=Gamma0(q)+0.5 M_AB(q)z^A z^B+O(z^4) and no odd source/boundary term. Result: Then partial_z Gamma_eff|0=0 and partial_q partial_z Gamma_eff|0=0 over the q patch.
- `THM3721_3_KL_penalty_hessian` `DERIVED_FOR_KL_EFFECTIVE_ACTION`: For Psi_KL(q,z)=Theta_H(q) D_KL(p_z||p_0), Hessian_z Psi_KL|0=Theta_H I_H. Result: This gives a positive information-geometric fibre penalty if I_H has a positive local floor.
- `THM3721_4_operator_match` `DERIVED_BOUND`: If M_AB = Theta_H I_AB + DeltaM_map in the same G_H/U_H basis, then Xi_H >= lambda_min(M)-||DeltaM_map||-R_boundary. Result: This is the executable bridge from response-doublet operator to Fisher gap.
- `THM3721_5_raw_free_energy_warning` `ANTI_SHORTCUT_GUARD`: For raw F=-Theta log integral exp[-A/Theta]dmu, partial_AB F=<A_AB>-(1/Theta)Cov(A_A,A_B). Result: Raw partition free energy is not automatically the positive KL penalty; using it blindly can flip the sign.

## Current Bridge Audit
- `AUD3721_0_z_equals_Z` `PARTIAL` — z^A=Z^A: 3708 has z; 516/517 have Z; no source yet proves they are the same coordinate.
- `AUD3721_1_exchange_parity` `PARTIAL` — R_z=exchange: odd theorem has exchange candidate, but exact parent symmetry for all active channels is not derived.
- `AUD3721_2_q_even` `PARTIAL` — q=q(R_even): matter/even observed geometry is written as a route, not parent-derived for all readouts.
- `AUD3721_3_action_hessian` `NOT_SIGNED` — M_AB=Theta_H I_AB: response-doublet quadratic density and KL Hessian remain separate objects.
- `AUD3721_4_unit_basis` `MISSING` — same G_H/U_H basis: no same-basis unit map turns Fisher/operator Hessian into m^-2 local residual units.
- `AUD3721_5_source_boundary` `BLOCKED` — J_Z=B_Z=0: 516/517/1011 identify source-current and boundary work as hard blockers.
- `AUD3721_6_positive_floor` `NOT_PROVED` — lambda_min(I_H)>0: iota_H is defined but identifiability/eigenfloor is not parent-signed.

## Retained Coefficients
- `RC3721_0_coordinate_mismatch` `Delta_zZ`: ||z-Z|| in active local residual basis | impact: feeds DeltaM_map and residual projection error
- `RC3721_1_operator_mismatch` `DeltaM_map`: M_AB-Theta_H I_AB in same G_H/U_H basis | impact: reduces Xi_H lower bound
- `RC3721_2_unit_mismatch` `Delta_UH`: basis/unit mismatch between Fisher Hessian and local operator | impact: blocks R10/PPN conversion
- `RC3721_3_odd_source` `J_Z`: exchange-odd source current | impact: creates F_1,total
- `RC3721_4_boundary_work` `B_Z+B_boundary`: odd boundary/source work | impact: creates F_1,total and B_QK,total
- `RC3721_5_identifiability_loss` `iota_loss`: zero-score active fibre directions | impact: can close Xi_H gap

## Decisions
- `DEC3721_0_bridge_survives` `BRIDGE_THEOREM_CONSTRUCTED_CONDITIONAL` | If z=Z, exchange is exact, and M_AB=Theta_H I_H in one basis, the 3719 mechanism becomes a real parent route.
- `DEC3721_1_current_not_signed` `CURRENT_MTS_NOT_PROMOTED` | The corpus does not yet sign the coordinate map, operator equality, unit map, identifiability, or boundary/source silence.
- `DEC3721_2_raw_free_energy_refined` `RAW_GIBBS_FREE_ENERGY_NOT_ENOUGH` | The positive gap should be a KL/Legendre effective action or otherwise prove the sign; naive -Theta log Z is unsafe.
- `DEC3721_3_next` `ADVANCE_TO_KL_LEGENDRE_EFFECTIVE_ACTION_OWNER` | Before further local scoring, lock whether the parent action owns the KL penalty, the Legendre transform, and the M=Theta I operator sign.

## Claim Gates
- `CG3721_0_zZ` `BLOCKED` | z=Z component map is parent-signed
- `CG3721_1_parity` `BLOCKED` | exchange is exact fibre parity for all active components
- `CG3721_2_KL_action` `BLOCKED` | positive KL/Legendre effective action is parent-owned
- `CG3721_3_operator` `BLOCKED` | M_AB=Theta_H I_AB in same basis, with units
- `CG3721_4_boundary` `BLOCKED` | J_Z and boundary odd work vanish or are bounded
- `CG3721_5_gap` `BLOCKED` | Xi_H lower bound positive and local-unit converted
- `CG3721_6_claim` `BLOCKED` | local-GR/R10/PPN screening claim allowed

## Source Register
- `doc_3720`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3720-Y5-R2FR-corpus-hunt-parent-bath-scale-parity-clauses.md`
- `next_3720`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3720_NEXT_TARGET.csv`
- `bridge_3720`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3720_BRIDGE_CONTRACT_ROWS.csv`
- `adjudication_3720`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3720_CLAUSE_ADJUDICATION_ROWS.csv`
- `fisher_3708`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv`
- `gamma_action_516`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_GAMMA_OWNER_CANDIDATE_ACTION.csv`
- `doublet_variation_517`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv`
- `doublet_contract_516`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv`
- `odd_theorem`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_ODD_RESIDUAL_EXCHANGE_THEOREM.csv`
- `doc_3719`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3719-Y5-R2FR-parent-bath-normalization-and-z-parity-proof.md`

## Next Target
- `3722-Y5-R2FR-KL-Legendre-effective-action-sign-owner-or-free-energy-demotion.md`
- Objective: lock the sign and ownership of the positive KL/Legendre effective action before using the Fisher gap in local screening claims.

## Validation
- See `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3721_VALIDATION.csv`.
