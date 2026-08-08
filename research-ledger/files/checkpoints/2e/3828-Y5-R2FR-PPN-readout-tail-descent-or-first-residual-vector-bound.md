# 3828 — PPN Readout Tail Descent Or First Residual-Vector Bound

Private checkpoint. This attempts the derivation route first. It does not claim local GR/Newton recovery.

Generated: `2026-07-01T01:52:25+00:00`

## Result

3828 converts the opaque blocker `R_PPN_readout_tail` into a residual vector:

`R_PPN_readout_tail = {delta_gamma, delta_beta, delta_alpha_pref, delta_tau, delta_acc}`.

Using `Phi=U/c^2` and a Newtonian temporal calibration, the minimal readout ansatz is:

`g00_obs = -1 + 2 C_t Phi - 2 B_t Phi^2 + r00_2 + r00_4`

`gij_obs = delta_ij (1 + 2 C_s Phi) + rij_2`

`g0i_obs = C_V1 V_i + C_V2 W_i + r0i`.

GR/PPN recovery then requires the scalar locks `C_s=C_t` and `B_t=C_t^2`, no preferred-frame vector hair, and clock/orbital projections tied to the same source readout.

## Source Register

| source_id | path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC3828_0_3827_doc | 3827-Y5-R2FR-local-kernel-scorecard-to-first-smoke-test-runner.md | True | True | input_for_PPN_readout_tail_derivation_or_bound |
| SRC3828_1_3827_ppn_rows | source-intake\mts_residuals\P8_Y5_R2FR_3827_PPN_READOUT_TAIL_FIRST_ROWS.csv | True | True | input_for_PPN_readout_tail_derivation_or_bound |
| SRC3828_2_3827_smoke | source-intake\mts_residuals\P8_Y5_R2FR_3827_SMOKE_RUN_RESULTS.csv | True | True | input_for_PPN_readout_tail_derivation_or_bound |
| SRC3828_3_3827_queue | source-intake\mts_residuals\P8_Y5_R2FR_3827_PRIORITY_SOURCE_FILL_QUEUE.csv | True | True | input_for_PPN_readout_tail_derivation_or_bound |
| SRC3828_4_3827_failure | source-intake\mts_residuals\P8_Y5_R2FR_3827_FAILURE_MODE_LEDGER.csv | True | True | input_for_PPN_readout_tail_derivation_or_bound |
| SRC3828_5_3827_validation | source-intake\mts_residuals\P8_Y5_BRR545_3827_VALIDATION.csv | True | True | input_for_PPN_readout_tail_derivation_or_bound |
| SRC3828_6_3826_scorecard | source-intake\mts_residuals\P8_Y5_R2FR_3826_KERNEL_CLAUSE_SCORECARD.csv | True | True | input_for_PPN_readout_tail_derivation_or_bound |
| SRC3828_7_3826_residuals | source-intake\mts_residuals\P8_Y5_R2FR_3826_SOURCE_KERNEL_RESIDUAL_BUNDLE.csv | True | True | input_for_PPN_readout_tail_derivation_or_bound |
| SRC3828_8_3818_Poisson | source-intake\mts_residuals\P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv | True | True | input_for_PPN_readout_tail_derivation_or_bound |

## Readout Ansatz

| ansatz_id | sector | readout_form | GR_value_after_Newton_calibration | source_status |
| --- | --- | --- | --- | --- |
| ANS3828_0_Newtonian_temporal | Newtonian temporal metric | g00_obs = -1 + 2 C_t Phi - 2 B_t Phi^2 + r00_2 + r00_4 | C_t=1; B_t=1 | C_t anchored by 3818 Poisson bridge; B_t not parent-signed |
| ANS3828_1_spatial_curvature | spatial curvature readout | gij_obs = delta_ij (1 + 2 C_s Phi) + rij_2 | C_s=C_t | C_s=C_t not parent-signed |
| ANS3828_2_vector_preferred_frame | vector/preferred-frame readout | g0i_obs = C_V1 V_i + C_V2 W_i + r0i | no extra preferred-frame vector hair | C_V1=C_V2=0 not parent-signed |
| ANS3828_3_clock_readout | clock/time transport | d tau_obs/dt = 1 - C_tau Phi + r_tau | C_tau=C_t | C_tau=C_t not parent-signed |
| ANS3828_4_orbital_acceleration | Newtonian/orbital acceleration | a_obs = - C_acc grad Phi + r_acc | C_acc=C_t with mu=GM used only as validation output | C_acc=C_t requires independent source lock and GM anti-smuggling guard |

## Zero Conditions

| condition_id | zero_condition | mathematical_role | current_status | if_unsigned |
| --- | --- | --- | --- | --- |
| ZPPN3828_0_same_source_potential | Phi is the same compact-exterior source potential in g00, gij, g0i, clock, and orbital readouts | prevents arena-specific potentials from hiding fitted coefficients | PARTIAL_FROM_3818_3826 | retain R_source_ledger + R_PPN_readout_tail |
| ZPPN3828_1_gamma_lock | C_s = C_t | sets gamma_MTS - 1 = 0 up to spatial residual rij_2/Phi | UNSIGNED | delta_gamma_bound = abs(C_s/C_t - 1) + eps_spatial/Phi |
| ZPPN3828_2_beta_lock | B_t = C_t^2 | sets beta_MTS - 1 = 0 after Newtonian calibration | UNSIGNED | delta_beta_bound = abs(B_t/C_t^2 - 1) + eps_temporal4/Phi^2 |
| ZPPN3828_3_no_preferred_frame_hair | C_V1 = C_V2 = 0 and r0i has no arena-fixed vector remainder | blocks alpha1/alpha2 preferred-frame residuals | UNSIGNED | alpha_pref_bound = abs(C_V1) + abs(C_V2) + eps_vector |
| ZPPN3828_4_clock_orbital_lock | C_tau = C_acc = C_t | ties clock redshift and Newtonian acceleration to the same metric source readout | UNSIGNED | delta_clock_orbital_bound = abs(C_tau/C_t-1) + abs(C_acc/C_t-1) + eps_tau + eps_acc |
| ZPPN3828_5_no_GM_input_smuggling | fitted orbital mu=GM is never used to set C_t, C_acc, M_source, or G | keeps Newtonian recovery from becoming circular | GUARD_ACTIVE_NOT_CLOSED | orbital rows stay validation-output only |

## Residual Vector Bound

| residual_id | observable | residual_formula | zero_if | bound_if_unsigned |
| --- | --- | --- | --- | --- |
| RPPN3828_0_gamma | gamma-1 | delta_gamma = C_s/C_t - 1 + eps_spatial/Phi | C_s=C_t and eps_spatial/Phi -> 0 on the local exterior domain | abs(delta_gamma) <= abs(C_s/C_t - 1) + abs(eps_spatial/Phi) |
| RPPN3828_1_beta | beta-1 | delta_beta = B_t/C_t^2 - 1 + eps_temporal4/Phi^2 | B_t=C_t^2 and eps_temporal4/Phi^2 -> 0 on the local exterior domain | abs(delta_beta) <= abs(B_t/C_t^2 - 1) + abs(eps_temporal4/Phi^2) |
| RPPN3828_2_preferred_frame | alpha1, alpha2 | delta_alpha_pref = C_V1 V_i + C_V2 W_i + eps_vector | C_V1=C_V2=0 and eps_vector -> 0 | alpha_pref_norm <= abs(C_V1) + abs(C_V2) + norm(eps_vector) |
| RPPN3828_3_clock | clock redshift/time transport | delta_tau = C_tau/C_t - 1 + eps_tau + R_boundary_MHref | C_tau=C_t, eps_tau -> 0, and boundary/MHref row closes | abs(delta_tau) <= abs(C_tau/C_t - 1) + abs(eps_tau) + abs(R_boundary_MHref) |
| RPPN3828_4_orbital | Newtonian/orbital acceleration | delta_acc = C_acc/C_t - 1 + eps_acc + R_GM_guard | C_acc=C_t, eps_acc -> 0, and independent source normalization replaces fitted mu input | abs(delta_acc) <= abs(C_acc/C_t - 1) + abs(eps_acc) + abs(R_GM_guard) |
| RPPN3828_5_total | R_PPN_readout_tail | R_PPN_readout_tail = {delta_gamma, delta_beta, delta_alpha_pref, delta_tau, delta_acc} | ZPPN3828_0 through ZPPN3828_5 all close on the same compact exterior source kernel | norm(R_PPN_readout_tail) <= weighted norm of the five residual bounds above |

## Readout Gates

| gate_id | gate | condition | status | next_action |
| --- | --- | --- | --- | --- |
| RGATE3828_0_gamma | gamma channel | C_s=C_t | BLOCKED_PARENT_SIGNATURE_REQUIRED | derive scalar readout lock from parent metric descent |
| RGATE3828_1_beta | beta channel | B_t=C_t^2 | BLOCKED_SECOND_ORDER_COUPLING_REQUIRED | derive nonlinear self-coupling owner from parent action |
| RGATE3828_2_preferred_frame | preferred-frame channel | C_V1=C_V2=0 | BLOCKED_FRAME_DESCENT_REQUIRED | prove no vector hair or emit finite vector source rows |
| RGATE3828_3_clock_orbital | clock/orbital readout lock | C_tau=C_acc=C_t | BLOCKED_READOUT_LOCK_REQUIRED | tie clock/orbital projections to same metric source readout |
| RGATE3828_4_total | local GR/Newton readout tail | all scalar, vector, clock, orbital, and GM guard gates close | BLOCKED_BUT_NOW_FORMULATED | 3829 should attack scalar readout locks first |

## Claim Gates

| gate_id | status | claim_allowed | reason |
| --- | --- | --- | --- |
| GATE3828_0_derivation_attempt | PASS_NONCLAIM_BOUND_FORM | False | zero conditions and finite residual vector formulas are explicit |
| GATE3828_1_local_GR_Newton_claim | BLOCKED | False | C_s=C_t, B_t=C_t^2, vector hair zero, and clock/orbital locks are not parent-signed |
| GATE3828_2_PPN_claim | BLOCKED_FIRST_VECTOR_BOUND_ONLY | False | formulas exist but no numeric/source-backed coefficient bounds exist |
| GATE3828_3_no_GM_smuggling | PASS_GUARD | False | orbital mu remains output validation only |
| GATE3828_4_next_target | PASS_ACTIONABLE_NEXT | False | gamma and beta scalar locks are the cleanest route under least scrutiny |

## Decisions

| decision_id | decision | consequence |
| --- | --- | --- |
| DEC3828_0_partial_derivation_success | R_PPN_readout_tail is no longer opaque | the project now has a concrete readout-tail target instead of a generic local-GR blocker |
| DEC3828_1_no_local_GR_claim | do not claim local GR/Newton recovery | 3828 is a real forward step but still a nonclaim derivation contract |
| DEC3828_2_best_next_attack | attack scalar readout locks before vector/EM extensions | 3829 should try to derive the scalar locks from parent metric/action descent or emit coefficient-bound rows |

## Bottom Line

This is closer to derivation than the previous blocker state. We still cannot claim local GR, but we now know exactly what must be proved:

- `C_s=C_t` gives `gamma -> 1`;
- `B_t=C_t^2` gives `beta -> 1`;
- `C_V1=C_V2=0` kills preferred-frame tails;
- `C_tau=C_acc=C_t` ties clocks and Newtonian acceleration to the same metric readout;
- fitted orbital `mu=GM` remains a validation output, not the source normalization.

Next target: `3829-Y5-R2FR-scalar-readout-lock-Ct-Cs-Bt-owner-or-bound-fill.md`.
