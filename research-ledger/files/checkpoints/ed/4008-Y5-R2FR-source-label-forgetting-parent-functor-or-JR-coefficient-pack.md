# 4008 - Source-Label-Forgetting Parent Functor Or J_R Coefficient Pack

- Timestamp: `2026-07-01T20:17:22+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

The dangerous coupling is now targeted at the right level: the parent matter object language.

The proposed ordinary-matter constructor is

`S_ord := sum_A int_M L_A(psi_A, D_obs psi_A, e_obs(q(Phi)), omega_obs(q(Phi)), theta_A) dmu_obs`.

Here `A` is only a direct-sum/representation label. It is not a field, not a source coordinate, not a scalar coupling slot, and not an argument of the parent action.

## No-Hom Rule

The constructor explicitly sets

`Hom(source/species/material label, R_+ source weight) = empty`

and also excludes `R_AB` from the ordinary matter argument list. Therefore

`S_matter = sum_A w_A(R_AB) S_A`

is ill-typed unless a new explicit source sector is added. That is the clean derivation route: do not tune `w_A`; ban the constructor that creates it.

## What This Closes

- source-label/prevariation weights are conditionally zero by type, not by optimism.
- `b_theta_R` is conditionally zero if constants are fixed representation data.
- `readout_regen_R` is conditionally zero if readout is post-variation or q-basic fixed.
- `epsilon_species_A` remains a bound scale only, not a derived parent coefficient.

## What This Does Not Close

This does not yet prove the full local branch. We still need the same parent branch to prove `v_R in ker(Dq)`, `e_obs=Obs_e(q(Phi))`, boundary/worldtube nohair, and later PPN/second-order source closure.

## Evaluator Results

- `CASE4008_0_packet_adopted_all_local_clauses`: constructor=`CONDITIONAL_BULK_SOURCE_WEIGHT_ZERO`, weight=`w_A BANNED_BY_TYPE`, J_R=`J_R_ORDINARY_MATTER_ZERO_CONDITIONAL`, next=`single-branch certificate then boundary/PPN closure`
- `CASE4008_1_packet_adopted_weight_requested`: constructor=`ILLEGAL_TERM_REJECTED`, weight=`w_A(R_AB) ILL_TYPED`, J_R=`J_R_PREF_WEIGHT_ZERO_CONDITIONAL`, next=`continue with q-kernel/coframe/boundary clauses`
- `CASE4008_2_packet_not_adopted`: constructor=`PACKET_WRITTEN_NOT_ADOPTED`, weight=`WEIGHT_NOT_BANNED_IN_PARENT_ACTION`, J_R=`J_R_NOT_ZEROED`, next=`adopt source-label-forgetting packet in one parent branch or keep coefficient pack`
- `CASE4008_3_q_kernel_open`: constructor=`MATTER_PACKET_OK_Q_KERNEL_OPEN`, weight=`w_A BANNED_CONDITIONAL`, J_R=`J_R_GEOMETRY_COMPONENT_OPEN`, next=`prove v_R in ker(Dq) for actual R_AB`
- `CASE4008_4_coframe_open`: constructor=`MATTER_PACKET_OK_COFRAME_OPEN`, weight=`w_A BANNED_CONDITIONAL`, J_R=`J_R_HILBERT_GEOMETRY_OPEN`, next=`prove observed coframe descends through q`
- `CASE4008_5_boundary_open`: constructor=`BULK_MATTER_ZERO_BOUNDARY_OPEN`, weight=`w_A BANNED_CONDITIONAL`, J_R=`J_R_BOUNDARY_WORLD_TUBE_OPEN`, next=`separate boundary/worldtube nohair pass`
- `CASE4008_6_numeric_pack`: constructor=`FINITE_COEFFICIENT_PACK_NONCLAIM`, weight=`WEIGHT_RETAINED_AS_NUMERIC_ROW`, J_R=`J_R_COMPONENT_ENVELOPE`, next=`source numeric coefficients and arena projections`

## Verdict

This is a real narrowing: the coupling leak is no longer a vague missing ingredient. It is either illegal by parent type signature, or it is a finite residual with named coefficients.

## Next Target

- `4009-Y5-R2FR-q-kernel-observed-coframe-single-branch-certificate-or-geom-JR-row.md`
- `scripts/Y5_R2FR_4009_q_kernel_observed_coframe_single_branch_certificate_or_geom_JR_row.py`

## Source Count

- source needles found: `32/32`
