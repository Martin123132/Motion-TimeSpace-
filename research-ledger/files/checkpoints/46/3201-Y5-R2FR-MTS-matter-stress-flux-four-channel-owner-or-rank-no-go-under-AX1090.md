# 3201 - MTS Matter Stress-Flux Four-Channel Owner Or Rank No-Go Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, rank-four proof, Maxwell/EM derivation, R10 pass, clock pass, orbital pass, or public-facing result.

## Result

3201 makes the important separation:

```text
matter/source/Poynting flux = local residual or theorem-zero channel;
K_hat/K_perp tensor response = only plausible internal four-channel owner.
```

This is not a defeat. It is a useful anti-cheat theorem: the same source flux cannot be both the hidden rank-four machinery and also absent from local tests.

## Separation Lemmas

### SRL3201_00 - local_source_rank_separation

For local-GR/PPN safety, matter-source flux and EM/Poynting flux must be theorem-zero or residual-bounded; therefore they cannot simultaneously be the unsuppressed rank-four owner of C1 gluing.

- Proof sketch: If a source flux supplies an O(1) independent row of J_Aa in a quiet local test, then the same channel contributes to B_obs/M_H unless a parent cancellation/zero theorem exists. No-cancellation scoring forbids using it as both a hidden rank owner and a vanished residual.
- Consequence: rank-four ownership must come from parent-internal tensor response K_hat/K_perp, or the finite-layer route remains closure-only.

### SRL3201_01 - trace_scalar_rank_limit

The scalar trace Gamma_eff can control the isotropic/exchange projection but cannot by itself own all four C1 mismatch slots.

- Proof sketch: A single scalar normal response produces at most one independent row unless a parent operator supplies independent boundary value and derivative channels; that additional structure is K_hat/K_perp, not Gamma_eff alone.
- Consequence: do not relabel Gamma_eff as the missing four-channel tensor owner.

### SRL3201_02 - Kperp_possible_owner_condition

A tensor elliptic boundary problem for K_perp can own rank-four only if left/right value and normal-derivative responses are independent, coercive, parent-derived, and free of zero modes.

- Proof sketch: The rank-four condition reduces to invertibility of the Dirichlet-to-Neumann/Jacobian map from z=(Delta_F_L,Delta_Fprime_L,Delta_F_R,Delta_Fprime_R) into four normal tensor-flux components.
- Consequence: the next derivation should target the K_perp operator and boundary map, not matter/Poynting flux.

## Channel Audit

- `CH3201_00`: `Gamma_eff trace projection` -> `not_four_channel_owner`; next: keep as exchange/trace source, not rank-four gluing owner
- `CH3201_01`: `K_hat / K_perp tensor stress-flux` -> `promising_conditional_not_parent_derived`; next: derive coercive tensor boundary operator L_T and its four-channel response map
- `CH3201_02`: `matter source flux` -> `cannot_be_unsuppressed_rank_owner`; next: place in Bobs/source-measure bound ledger unless a source-silence theorem closes
- `CH3201_03`: `boundary/source/projector B_obs flux` -> `live_residual_blocker`; next: do not use leakage as rank owner; source/bound it
- `CH3201_04`: `EM/Poynting flux` -> `demoted_by_3200`; next: keep in residual bound schema, not owner

## Rank Tests

- `FRT3201_00_exact_local_silence`: rank `0`, passes rank-four `false` - exact local-GR silence route; no finite-layer rank owner needed, but current corpus has not proved the zeros
- `FRT3201_01_trace_scalar_only`: rank `1`, passes rank-four `false` - scalar trace creates duplicated value response and cannot own derivative slots
- `FRT3201_02_source_silent_plus_radial_Khat`: rank `2`, passes rank-four `false` - spherical/radial symmetry duplicates left-right rows and gives rank two
- `FRT3201_03_unsuppressed_matter_flux`: rank `4`, passes rank-four `true` - rank can improve if unsuppressed source rows are admitted, but that reopens local PPN/source-coupling residuals
- `FRT3201_04_Kperp_independent_boundary_map`: rank `4`, passes rank-four `true` - rank four is possible if and only if the parent tensor boundary map supplies independent coefficients

There are two rank-four rows, and neither is a claim: arbitrary unsuppressed source flux is rejected by local-safety separation, while the `K_perp` independent boundary-map row is only a conditional target.

## Kperp Owner Gates

- `KPG3201_00`: `parent_tensor_operator` - derive L_T[K_perp]=J_perp from parent action/coarse-graining, not postulated boundary smoothing
- `KPG3201_01`: `coercive_positive_operator` - prove L_T is coercive/positive in the local static weak-field limit
- `KPG3201_02`: `no_zero_modes` - exclude homogeneous transverse tensor modes/topological modes on the local domain
- `KPG3201_03`: `independent_boundary_response` - the Dirichlet/Neumann response map from four C1 mismatch slots to four tensor-flux components has rank four
- `KPG3201_04`: `local_safety_compatibility` - the same K_perp response either vanishes in exact local GR or is bounded below PPN/source-coupling limits

## Acquisition Queue

- `ACQ3201_00`: `partial C_left_value/partial Delta_F_L` -> `MISSING_KPERP_PARENT_COEFFICIENT`
- `ACQ3201_01`: `partial C_left_derivative/partial Delta_Fprime_L` -> `MISSING_KPERP_PARENT_COEFFICIENT`
- `ACQ3201_02`: `partial C_right_value/partial Delta_F_R` -> `MISSING_KPERP_PARENT_COEFFICIENT`
- `ACQ3201_03`: `partial C_right_derivative/partial Delta_Fprime_R` -> `MISSING_KPERP_PARENT_COEFFICIENT`
- `ACQ3201_04`: `B_obs_source_measure/projector/boundary leakage` -> `MISSING_BOBS_SOURCE_ROWS`

## Decision

`CURRENT_MTS_MATTER_FLUX_DOES_NOT_CLOSE_RANK4_OWNER`.

Claim status: `NO_LOCAL_GR_NEWTON_PPN_OR_RANK4_CLAIM`.

Decision: matter/source/Poynting flux cannot honestly be used as unsuppressed rank-four owner in local tests; only K_hat/K_perp tensor boundary response remains a plausible internal owner

Best next route: derive the K_perp elliptic boundary operator and Dirichlet-to-Neumann rank map, or demote finite-layer rank route and proceed with Bobs residual acquisition

Next target:

```text
3202-Y5-R2FR-Kperp-elliptic-boundary-operator-or-Bobs-residual-acquisition-under-AX1090
```

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3201_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3201_SOURCE_RANK_SEPARATION_LEMMA.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3201_STRESS_FLUX_CHANNEL_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3201_FOUR_CHANNEL_RANK_TESTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3201_KPERP_ELLIPTIC_OWNER_GATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3201_COEFFICIENT_ACQUISITION_QUEUE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3201_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3201_VALIDATION.csv`

## Validation

- `VAL3201_00_inputs_exist`: `true` - inputs=9
- `VAL3201_01_separation_lemma_present`: `true` - source flux cannot be both hidden rank owner and vanished residual
- `VAL3201_02_channels_cover_internal_and_source_flux`: `true` - channels=5
- `VAL3201_03_rank4_only_conditional`: `true` - FRT3201_03_unsuppressed_matter_flux=REJECT_AS_LOCAL_SAFETY_OWNER;FRT3201_04_Kperp_independent_boundary_map=CONDITIONAL_BEST_ROUTE_NOT_PROVED
- `VAL3201_04_source_flux_rejected_as_owner`: `true` - rank can improve if unsuppressed source rows are admitted, but that reopens local PPN/source-coupling residuals
- `VAL3201_05_kperp_gates_open`: `true` - parent_tensor_operator;coercive_positive_operator;no_zero_modes;independent_boundary_response;local_safety_compatibility
- `VAL3201_06_queue_nonclaim`: `true` - ACQ3201_00;ACQ3201_01;ACQ3201_02;ACQ3201_03;ACQ3201_04
- `VAL3201_07_no_claim_leak`: `true` - no local-GR, Newton, PPN, or rank-four claim
- `VAL3201_08_csv_parse`: `true` - P8_Y5_R2FR_3201_INPUTS.csv;P8_Y5_R2FR_3201_SOURCE_RANK_SEPARATION_LEMMA.csv;P8_Y5_R2FR_3201_STRESS_FLUX_CHANNEL_AUDIT.csv;P8_Y5_R2FR_3201_FOUR_CHANNEL_RANK_TESTS.csv;P8_Y5_R2FR_3201_KPERP_ELLIPTIC_OWNER_GATE.csv;P8_Y5_R2FR_3201_COEFFICIENT_ACQUISITION_QUEUE.csv;P8_Y5_R2FR_3201_DECISION.csv

All generated rows remain `valid_for_claim=false`.
