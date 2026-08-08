# 3720 — Corpus Hunt: Parent Bath, Scale, and Parity Clauses

## Status
- `PARTIAL_CORPUS_SUPPORT_BRIDGE_REQUIRED`
- The corpus is not empty: it has partial support from Fisher/bath rows and response-doublet parity/even-action rows.
- The important result is that these are not yet one parent-owned mechanism; the bridge proof is now the next exact target.

## Main Result
- `3708` supports a conditional Fisher/exponential-family bath: `p_z` and `D_KL` exist as a structural route.
- `516/517` support a conditional response-doublet even action: exchange-odd `Z` has a quadratic density and no linear term if source/boundary clauses vanish.
- `541/542` support source-measure/GM work, but that is not the same as the unresolved-bath measure `mu_H`.
- Therefore the next serious derivation is the bridge `z=Z`, `R_z=exchange`, and `Theta_H I_H = M_AB` in the same units/basis.

## Clause Adjudication
- `ADJ3720_0_parent_bath_action` `PARTIAL_NOT_SIGNED` — parent bath action/free energy A_B(q,z,xi): P8_GAMMA_OWNER_CANDIDATE_ACTION.csv supplies an even Gamma_eff/action-density candidate, but not a full Gibbs bath action A_B(q,z,xi) with xi, measure, and Theta_H. Next: map response-doublet Gamma_eff to A_B or keep it as a separate local action branch.
- `ADJ3720_1_bath_family` `PARTIAL_SUPPORTED` — p_z bath distribution: 3708 already has p_z(xi|X_B,q)=p_0 exp[z^A Y_A^perp-W], so the exponential-family/Fisher object exists as a conditional construction. Next: derive this p_z from parent A_B/Z rather than declaring it.
- `ADJ3720_2_measure_normalization` `NOT_SIGNED` — mu_H/dmu_H bath measure: The source-measure files concern Hamiltonian/worldtube mass measure, not the unresolved-bath measure needed by the Fisher KL construction. Next: do not confuse source measure with bath measure; build the bath measure or demote to coefficient row.
- `ADJ3720_3_scale_theta` `SYMBOL_EXISTS_UNITS_MISSING` — Theta_H or T_eff scale with units: 3708/3709 provide T_eff/Theta_H*iota_H structure, but the parent origin and unit map into local m^-2 operator units remain unsigned. Next: derive scale from parent coarse-grain/free-energy normalization or keep Xi_H symbolic.
- `ADJ3720_4_parity_involution` `BEST_SUPPORTED_CANDIDATE_NOT_COMPONENT_DERIVED` — z parity / exchange involution: Response-doublet and odd-residual files contain exchange symmetry/even action rows, but they explicitly say component coverage and matter/boundary odd-charge zeros are not derived. Next: attempt response-doublet -> Gibbs z-parity map next.
- `ADJ3720_5_identifiability` `FORMULA_EXISTS_PROOF_MISSING` — positive Fisher floor iota_H: 3708 defines iota_H/lambda_min but does not prove a positive lower bound for all active local fibre directions. Next: prove no active z-direction is bath-invisible or retain a finite lower-bound row.
- `ADJ3720_6_boundary_silence` `CURRENTLY_BLOCKED` — boundary/source silence: 516/517/1011 all identify J_Z/B_Z or boundary/source work as the hard open clause. Next: derive parity-even boundary/no odd source charge or keep F_loss/QK_loss active.
- `ADJ3720_7_unit_map` `MISSING` — U_H same-basis unit map: No corpus row found that maps Fisher Hessian units into the local R10/PPN operator basis without remaining symbolic. Next: construct U_H from the same field metric G_H and local residual projection, or keep nonclaim.

## Bridge Contract
- `BRIDGE3720_0_identify_z` `z^A := Z^A=(R_+^A-R_-^A)/2` | turns the response-doublet odd coordinate into the Fisher bath fibre coordinate | needs: needs component map through all active local residual channels
- `BRIDGE3720_1_identify_parity` `R_z corresponds to exchange E:R_+^A<->R_-^A` | makes the 3719 z -> -z parity a parent exchange symmetry | needs: needs exchange to be exact parent symmetry, not notation
- `BRIDGE3720_2_identify_action` `A_B or Delta S_fibre reduces to Gamma_eff even quadratic density` | connects GO516/AV517 action candidate to the Fisher KL potential | needs: needs xi/bath variables or a proof that integrating xi yields the even density
- `BRIDGE3720_3_identify_scale` `Theta_H I_H equals the quadratic operator M_AB after same-basis normalization` | turns Fisher floor into the response-doublet positive operator | needs: needs unit map U_H and field metric G_H
- `BRIDGE3720_4_boundary_guard` `J_Z=B_Z=0 corresponds to R_odd,F1=R_odd,BQK=B_boundary=0` | collapses 3718 correction budgets if signed | needs: currently open in 516/517/1011

## Decisions
- `DEC3720_0_not_empty` `CORPUS_HAS_PARTIAL_SUPPORT` | The corpus contains Fisher bath/exponential-family structure and a separate response-doublet parity/even-action structure.
- `DEC3720_1_not_signed` `3719_MECHANISM_NOT_SIGNED_AS_CURRENT_MTS` | No source currently supplies the full combined parent Gibbs bath, measure, Theta/unit map, exact parity, identifiability, and boundary silence package.
- `DEC3720_2_best_route` `MAP_RESPONSE_DOUBLET_TO_GIBBS_PARITY_NEXT` | The strongest route is to identify Fisher z with the exchange-odd doublet coordinate Z and prove the quadratic even action is the KL/free-energy Hessian.
- `DEC3720_3_source_measure_warning` `SOURCE_MEASURE_IS_NOT_BATH_MEASURE` | Hamiltonian/worldtube source-measure work remains crucial for Newton/GM, but it does not by itself supply mu_H for the Fisher bath.

## Claim Gates
- `CG3720_0_A_B` `BLOCKED` | parent A_B or free-energy action is matched to response/Fisher variables
- `CG3720_1_mu_H` `BLOCKED` | bath measure/partition normalization is owned
- `CG3720_2_Theta_UH` `BLOCKED` | Theta_H/T_eff and U_H unit map are parent-owned
- `CG3720_3_parity` `BLOCKED` | exchange-doublet parity equals z -> -z for all active local components
- `CG3720_4_identifiability` `BLOCKED` | positive Fisher/operator floor is proved
- `CG3720_5_boundary` `BLOCKED` | source-current and boundary odd work vanish or are bounded
- `CG3720_6_claim` `BLOCKED` | local GR/R10/PPN screening claim allowed

## Source Register
- `doc_3719`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3719-Y5-R2FR-parent-bath-normalization-and-z-parity-proof.md`
- `next_3719`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3719_NEXT_TARGET.csv`
- `fisher_3708`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv`
- `fill_3709`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3709_PARENT_FILL_ROWS.csv`
- `gamma_action_516`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_GAMMA_OWNER_CANDIDATE_ACTION.csv`
- `doublet_variation_517`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv`
- `doublet_contract_516`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv`
- `odd_contract`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_ODD_RESIDUAL_EXCHANGE_CONTRACT.csv`
- `odd_theorem`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_ODD_RESIDUAL_EXCHANGE_THEOREM.csv`
- `hamiltonian_source_measure`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv`
- `source_measure_attempt`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_SOURCE_MEASURE_THEOREM_ATTEMPT.csv`
- `doc_1010`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md`
- `doc_1011`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md`
- `doc_1016`: exists=True needle_found=True path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md`

## Automated Scan
- See `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3720_AUTOMATED_CORPUS_HITS.csv` for ranked source hits by requirement.

## Next Target
- `3721-Y5-R2FR-response-doublet-to-Gibbs-bath-parity-map-or-demotion.md`
- Objective: try the bridge proof directly; if it fails, demote the 3719 mechanism to a conditional closure and retain finite coefficient rows.

## Validation
- See `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3720_VALIDATION.csv`.
