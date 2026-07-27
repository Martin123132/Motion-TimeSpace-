# 3900 - Single-Coframe Maxwell Calibration Lock or Scalar Runner Fill

Generated: `2026-07-01T09:11:10+00:00`

## Result

3900 connects the local-GR route to the Maxwell/EM and calibrated-source side.

Candidate visible action:

`S_vis=S_EH[g_obs]+S_Maxwell[A,e_obs,alpha_*]+sum_A S_A[psi_A,e_obs,omega[e_obs],theta_*]`

Same-frame rule:

`all visible rods, clocks, photons, EM stress, orbital motion, and source variation use the same e_obs(q(Phi))`

Maxwell stress rule:

`S_Maxwell=-1/4 int sqrt(-g_obs) alpha_*^{-1} F_{mu nu}F^{mu nu}; T_EM is included in the same Hilbert source variation`

What improves: ordinary EM stress/Poynting energy can live inside the same Hilbert source, so it is not an extra arbitrary mass channel. What does not close yet: same-frame descent is weaker than the no-disformal condition needed for gamma zero, and compact U(1)/Maxwell alone does not prove the fine-structure coefficient cannot run.

## Single Coframe Lock Attempt

| row_id | clause | statement | result | status |
| --- | --- | --- | --- | --- |
| COF3900_0_visible_action | visible-sector action | S_vis=S_EH[g_obs]+S_Maxwell[A,e_obs,alpha_*]+sum_A S_A[psi_A,e_obs,omega[e_obs],theta_*] | candidate branch has one public observed geometry for EH, matter, and Maxwell sectors | PASS_CANDIDATE_BRANCH_FROM_3890 |
| COF3900_1_single_frame | same observed coframe | all visible rods, clocks, photons, EM stress, orbital motion, and source variation use the same e_obs(q(Phi)) | kills matter/source frame split if parent adopts the same-frame contract | CANDIDATE_SAME_FRAME_LOCK_PARENT_UNSIGNED |
| COF3900_2_no_hidden_frame | no hidden matter frame | Hom_parent(H_hidden,M_source)=0 forbids hidden e_A(X), w_A(X), m_A(X), alpha_A(X) source-only slots | direct hidden frame/source derivative vanishes in the candidate object language | PASS_IF_OBJECT_LANGUAGE_SIGNED |
| COF3900_3_no_disformal | no-disformal/lapse-space equality | no independent tau-tau, spatial, hidden-frame, or disformal X-dependent coframe slot is allowed beyond e_obs | this is stronger than same-frame descent; it is what would force c_space=c_lapse | OPEN_STRONGER_THAN_CURRENT_GRAMMAR |
| COF3900_4_verdict | coframe verdict | same-frame is structurally supported; conformal/no-disformal response remains an explicit next proof obligation | gamma cannot be claimed zero yet, but the missing condition is now precise | PARTIAL_LOCK_NO_GAMMA_CLAIM |

## Maxwell/EM Stress Calibration Gate

| row_id | channel | statement | result | status |
| --- | --- | --- | --- | --- |
| EM3900_0_minimal_Maxwell | Maxwell action and stress | S_Maxwell=-1/4 int sqrt(-g_obs) alpha_*^{-1} F_{mu nu}F^{mu nu}; T_EM is included in the same Hilbert source variation | ordinary EM field energy belongs to the same Hilbert source, not an extra fitted mass channel | PASS_IF_MINIMAL_MAXWELL_SIGNED |
| EM3900_1_Poynting | Poynting flux | stationary closed-surface Poynting flux is included in T_total or zero; radiative/relic flux is retained as explicit leakage | user's Poynting-vector intuition is handled as Hilbert-source dressing or scored residual, not ignored | CONDITIONAL_ZERO_OR_RESIDUAL |
| EM3900_2_alpha_vertex | alpha_EM and F^2 vertex | no alpha_EM(X)F^2 vertex is needed for minimal Maxwell, but existing alpha-level work says compact U(1) alone does not fix the gauge kinetic coefficient | alpha/clock calibration remains open unless quotient-owned constants are parent-signed | OPEN_ALPHA_CALIBRATION |
| EM3900_3_clock | clock/spectroscopy calibration | clock ratios descend through e_obs and quotient-owned constants; if alpha/mass ratios run with X, fill c_clock and b_alpha rows | clock/EM stress can support the single-frame route but also supplies the sharp residual if constants run | CLOCK_CALIBRATION_UNSIGNED |
| EM3900_4_verdict | EM/source coupling verdict | minimal same-coframe Maxwell is enough to include ordinary EM stress in the Newton/Hilbert source; it does not by itself prove no-disformal gamma or no alpha drift | EM helps source coupling; gamma/Gdot/clock still need coefficient rows or stronger parent lock | PARTIAL_EM_LOCK_SCALAR_BOUNDS_RETAINED |

## Scalar Runner Fill Rows

| fill_id | runner_target | branch | fill_value_or_formula | required_parent_signature | row_status |
| --- | --- | --- | --- | --- | --- |
| RUN3900_0_gamma_zero_candidate | K_gamma | single_coframe_plus_no_disformal | K_gamma=0 | COF3900_1 same frame plus COF3900_3 no-disformal/lapse-space equality | CANDIDATE_ZERO_NOT_RUNNABLE_FOR_CLAIM |
| RUN3900_1_gamma_bound | K_gamma | nonconformal scalar | |gamma-1| <= |c_space-c_lapse| X_bound <= 2.3e-5, with c_space-c_lapse=0 only on the signed conformal/no-disformal branch | numeric/source-backed c_space-c_lapse and X_bound | RUNNER_FORMULA_READY_INPUTS_MISSING |
| RUN3900_2_Gdot_zero_candidate | K_Gdot | stationary memory plus fixed calibration | K_Gdot=0 and calibration_source_drift=0 | stationary/Killing collar, no incoming memory, quotient-owned G/clock calibration | CANDIDATE_ZERO_NOT_RUNNABLE_FOR_CLAIM |
| RUN3900_3_Gdot_bound | Gdot/G | nonstationary or drifting calibration | |Gdot/G| <= |c_G||partial_t X| + |X partial_t c_G| + |calibration_source_drift| <= 9.6e-15 yr^-1 | c_G, partial_t X bound, partial_t c_G or zero, calibration drift bound | RUNNER_FORMULA_READY_INPUTS_MISSING |
| RUN3900_4_alpha_clock_bound | clock/alpha_EM | nonminimal EM calibration | Delta ln alpha_EM or clock ratio <= |b_alpha_X| X_bound + clock gradient terms | b_alpha_X=0 by quotient-owned Maxwell coefficient or numeric spectroscopy/clock bound | RUNNER_FORMULA_READY_ALPHA_INPUTS_MISSING |

## Local-GR Decision Gate

| gate_id | gate | result | status | claim_allowed |
| --- | --- | --- | --- | --- |
| LGG3900_0_same_frame | same observed coframe/source frame | structurally supported in candidate grammar but still parent-unsigned globally | CANDIDATE_PASS_PARENT_UNSIGNED | False |
| LGG3900_1_no_disformal | no-disformal conformal response | not yet proved by same-frame descent alone | OPEN_REQUIRED_FOR_GAMMA_ZERO | False |
| LGG3900_2_Maxwell | minimal Maxwell stress/source coupling | ordinary EM stress is Hilbert-source dressed if minimal Maxwell and same coframe are signed | CANDIDATE_PASS_EM_STRESS | False |
| LGG3900_3_alpha_clock | alpha/clock calibration | gauge kinetic and clock constants remain quotient-ownership/coefficient rows | OPEN_ALPHA_CLOCK_CALIBRATION | False |
| LGG3900_4_local_GR | local-GR/Newton/EM promotion | no claim until no-disformal, stationary/calibration, and EM constant ownership close or are scored | BLOCKED_NO_CLAIM_EM_COHERENCE_ADVANCED | False |

## Source Register

Resolved `12/12` source rows.

| source_id | path | needle_found | role |
| --- | --- | --- | --- |
| SRC3900_00_next | source-intake\mts_residuals\P8_Y5_R2FR_3899_NEXT_TARGET.csv | True | 3899 selected single-coframe/Maxwell target |
| SRC3900_01_conformal | source-intake\mts_residuals\P8_Y5_R2FR_3899_CONFORMAL_READOUT_PROOF_ATTEMPT.csv | True | 3899 conformal gamma branch |
| SRC3900_02_bounds | source-intake\mts_residuals\P8_Y5_R2FR_3899_SCALAR_GAMMA_GDOT_BOUND_ROWS.csv | True | 3899 scalar bound rows |
| SRC3900_03_matter | source-intake\mts_residuals\P8_Y5_R2FR_2674_MATTER_CHANNEL_DESCENT_AUDIT.csv | True | matter/EM/clock descent audit |
| SRC3900_04_action | source-intake\mts_residuals\P8_Y5_R2FR_3890_PARENT_ACTION_GRAMMAR_INSERTION.csv | True | candidate parent action grammar |
| SRC3900_05_object | source-intake\mts_residuals\P8_Y5_R2FR_3889_PARENT_OBJECT_LANGUAGE_NO_DIRECT_SOURCE_THEOREM.csv | True | object-language no hidden source arrow |
| SRC3900_06_source_current | source-intake\mts_residuals\P8_source_current_Ward_universality_CONTRACT.csv | True | same observed coframe source current contract |
| SRC3900_07_no_species | source-intake\mts_residuals\P8_no_species_source_charge_CONTRACT.csv | True | one observed coframe/no species source charge contract |
| SRC3900_08_em_qmap | source-intake\mts_residuals\P8_EM_actual_q_map_vertical_basis_candidate.csv | True | public geometry/coframe q-map candidate |
| SRC3900_09_alpha_status | source-intake\mts_residuals\P8_EM_alpha_level_current_owner_status.csv | True | alpha-level current owner no-go |
| SRC3900_10_alpha_residual | source-intake\mts_residuals\P8_EM_current_source_Ward_alpha_source_residual.csv | True | alpha/current residual coefficient |
| SRC3900_11_poynting | source-intake\mts_residuals\P8_mu_extra_over_Geff_Meff_vector.csv | True | Poynting/Hilbert EM stress row |

## Next Target

| next_id | target_checkpoint | objective | why_next |
| --- | --- | --- | --- |
| NEXT3900_0 | 3901-Y5-R2FR-no-disformal-coframe-response-equation-or-gamma-Gdot-runner-score.md | derive the coframe response equation that forbids independent lapse/spatial X coefficients; if not derivable, add gamma/Gdot/alpha-clock rows to the executable suppression runner as physical nonclaim inputs | 3900 shows same-frame Maxwell/source coupling is structurally plausible, but gamma-zero still hinges on the stronger no-disformal coframe response |

## Bottom Line

This is genuine forward motion toward the full goal: EM stress and source coupling are now tied into the same-coframe Hilbert-source route. But gamma-zero still needs the stronger no-disformal coframe-response equation, and clock/alpha calibration still needs either quotient ownership or a bound.
