# 3304 - Source-projection overlap law for alpha factors under AX1090

Run UTC: `2026-06-27T18:39:56.816998+00:00`

## Verdict

The coupling problem is now a source-charge overlap law.

The finite-mode force between two bodies is not safely represented by one universal `alpha_i` unless the source-projection factors are universal:

`V_AB(r) = -G_cal m_A m_B/r [1 + alpha0_star Xi_0[A] Xi_0[B] exp(-r/lambda_0) + alpha2_star Xi_2[A] Xi_2[B] exp(-r/lambda_2)]`.

So the clean route to local GR is either:

1. prove `Xi_0[A]=Xi_2[A]=1` for all local matter from the parent Hilbert/source projector; or
2. keep the WEP/source-composition residuals alive and bound `Delta_Xi_i[A,B]`.

No universal-alpha or local-GR claim is made here.

## Source Register

- `SRC3304_0`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3303-Y5-R2FR-universal-Hilbert-source-check-for-quadratic-amplitudes-under-AX1090.md` — exists=true; role=3303 amplitude import decision
- `SRC3304_1`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3303_GENERALIZED_ALPHA_AMPLITUDE_LAW.csv` — exists=true; role=3303 alpha law
- `SRC3304_2`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3303_SOURCE_PROJECTION_REQUIREMENTS.csv` — exists=true; role=3303 projection requirements
- `SRC3304_3`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3303_DECISION_LEDGER.csv` — exists=true; role=3303 decision
- `SRC3304_4`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3303_NEXT_TARGET.csv` — exists=true; role=3303 next target
- `SRC3304_5`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3303_VALIDATION.csv` — exists=true; role=3303 validation
- `SRC3304_6`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv` — exists=true; role=3293 Hilbert source theorem
- `SRC3304_7`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3293_LOCAL_GR_MATTER_COUPLING_REDUCTION.csv` — exists=true; role=3293 local source coupling
- `SRC3304_8`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3294_LOCAL_GR_REDUCTION_CONTRACT.csv` — exists=true; role=3294 local GR contract

## Xi Definitions

- `XI3304_0_scalar_source_charge` `Xi_0[A]`: Xi_0[A] = Q_0[A] / Q_0^pure[A], where Q_0[A] is the scalar finite-mode charge obtained by projecting the descended matter source of body A onto the scalar mode
- `XI3304_1_spin2_source_charge` `Xi_2[A]`: Xi_2[A] = Q_2[A] / Q_2^pure[A], where Q_2[A] is the massive spin-2 finite-mode charge obtained by projecting the descended matter source of body A onto the spin-2 mode
- `XI3304_2_pair_charge` `Xi_i[A] Xi_i[B]`: finite-mode force between bodies A and B depends on the product of their normalized source charges, not on a body-independent alpha unless Xi_i is universal

## Pairwise Force Law

- `PAIR3304_0_general_pair_potential`: `V_AB(r) = -G_cal m_A m_B/r [1 + alpha0_star Xi_0[A] Xi_0[B] exp(-r/lambda_0) + alpha2_star Xi_2[A] Xi_2[B] exp(-r/lambda_2)]`
- `PAIR3304_1_universal_reduction`: `If Xi_i[A]=Xi_i[B]=1 for all bodies, the pair law reduces to the 3303 generalized alpha law with alpha_i=alpha_i_star`
- `PAIR3304_2_source_weight_warning`: `If Xi_i[A] != Xi_i[B] for different materials, alpha_i cannot be entered as one universal R10/PPN number`

## Universality Clauses

- `XIU3304_0_same_matter_action`: one descended matter action S_m[g_pub,Psi,theta] owns all local source tensors and currents Status: `EXACT_CONDITIONAL_FROM_3293_NOT_PARENT_SIGNED`.
- `XIU3304_1_no_species_weights`: no post-variation species weights, source labels, or hidden material selectors multiply finite-mode source charge Status: `CONDITIONAL_NOT_PARENT_SIGNED`.
- `XIU3304_2_projector_same_as_pure_limit`: finite scalar/spin-2 projectors act on the Hilbert stress in the same way as the pure metric quadratic branch Status: `MISSING_LINEARIZED_PARENT_PROJECTOR`.
- `XIU3304_3_EM_and_binding_energy_included`: EM stress, Poynting flow, binding energy, and clock/readout contributions enter the same Hilbert tensor with no double count Status: `CONDITIONAL_FROM_HILBERT_EM_BRANCH_NOT_FULLY_SIGNED`.
- `XIU3304_4_public_metric_readout`: the metric used to define matter stress is the same metric read by rods/clocks/orbital bodies Status: `CONDITIONAL_FROM_3294_NOT_PARENT_SIGNED`.

## WEP Residual Map

- `WEP3304_0_scalar_delta` `Delta_Xi_0[A,B] = Xi_0[A] - Xi_0[B]`: `eta_AB,E^(0) ~= alpha0_star Xi_0[E] Delta_Xi_0[A,B] (1+r/lambda_0) exp(-r/lambda_0)`
- `WEP3304_1_spin2_delta` `Delta_Xi_2[A,B] = Xi_2[A] - Xi_2[B]`: `eta_AB,E^(2) ~= alpha2_star Xi_2[E] Delta_Xi_2[A,B] (1+r/lambda_2) exp(-r/lambda_2)`
- `WEP3304_2_combined` `eta_AB,E`: `eta_AB,E ~= sum_i alpha_i_star Xi_i[E] Delta_Xi_i[A,B] (1+r/lambda_i) exp(-r/lambda_i) for small residuals`

## Promotion Gates

- `GATE3304_0_Xi_universal`: passed=false; claim=Xi_0[A]=Xi_2[A]=1 for all local matter bodies
- `GATE3304_1_WEP_safe`: passed=false; claim=composition residuals are below WEP/source bounds
- `GATE3304_2_universal_alpha_scoring`: passed=false; claim=finite quadratic branch can be scored with one universal alpha(lambda)

## Decision

- `DEC3304_0`: no — the exact universality clauses are written, but the parent action/projector/readout evidence is still conditional or missing
- `DEC3304_1`: the coupling gap is now a body-pair source-charge law plus an explicit WEP residual, not an undefined missing coupling — finite-mode tests now know whether they are universal-alpha tests or composition-dependent source tests

## Next Target

- `3305-Y5-R2FR-parent-projector-proof-for-Xi-universality-or-WEP-bound-pack-under-AX1090.md`
- `scripts/Y5_R2FR_3305_parent_projector_proof_for_Xi_universality_or_WEP_bound_pack.py`
- Objective: try to prove Xi_i[A]=1 from the parent matter projector; if not, build the WEP/source-composition bound pack for Delta_Xi_0 and Delta_Xi_2
