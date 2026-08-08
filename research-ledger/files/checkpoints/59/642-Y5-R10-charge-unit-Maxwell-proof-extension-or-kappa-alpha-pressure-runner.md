# 642 Y5/R10 Charge-Unit Maxwell Proof Extension or Kappa-Alpha Pressure Runner

## Verdict

- Status: `Y5_R10_U1_charge_structure_partial_coupling_normalization_still_blocks_kappa_alpha_zero_pressure_runner_nonclaim`
- Claim ceiling: `compact_U1_and_Maxwell_form_partial_only_no_alpha_EM_value_no_kappa_alpha_zero_no_R10_WEP_clock_PPN_or_local_GR_pass`
- The theorem-zero attempt gets a real partial result: compact `U(1)` structure can give integer charge labels and the `dF = 0` half of Maxwell, if it is parent-signed.
- The proof still blocks at the actual coupling: the base `g_EM` / `alpha_EM` normalization is not fixed by compactness alone.
- Therefore `kappa_alpha = 0` is not claimable. The finite-coupling pressure runner is now schema-ready but remains nonclaim.

## Source Register

| source_id | label | path | exists | role |
| --- | --- | --- | --- | --- |
| S642_0 | checkpoint_641_doc | 641-Y5-R10-kappa-alpha-pressure-envelope-and-charge-topology-next-proof.md | true | immediate prior coupling-pressure checkpoint |
| S642_1 | validation_641 | source-intake/mts_residuals/P8_Y5_BRR545_641_VALIDATION.csv | true | prior checkpoint validation |
| S642_2 | charge_next_proof_641 | source-intake/mts_residuals/P8_Y5_R10_641_CHARGE_UNIT_NEXT_PROOF.csv | true | charge-unit blocker input |
| S642_3 | maxwell_next_proof_641 | source-intake/mts_residuals/P8_Y5_R10_641_MAXWELL_NORMALIZATION_NEXT_PROOF.csv | true | Maxwell normalization blocker input |
| S642_4 | pressure_envelope_641 | source-intake/mts_residuals/P8_Y5_R10_641_KAPPA_ALPHA_PRESSURE_ENVELOPE.csv | true | finite coupling pressure factors |
| S642_5 | cross_arena_reaction_641 | source-intake/mts_residuals/P8_Y5_R10_641_CROSS_ARENA_REACTION_MATRIX.csv | true | cross-arena symbolic reaction matrix |
| S642_6 | boundary_current_charge_287 | 287-boundary-current-charge-owner-attempt.md | true | relative current and charge-unit obstruction |
| S642_7 | k9_ward_index_288 | 288-k9-Ward-index-level-attempt.md | true | index/level theorem obstruction |
| S642_8 | andersen_charge_contract | source-intake/external_papers/Andersen_2026_phase_current_CHARGE_CONTRACT.csv | true | external clue audit: phase/current/Maxwell contract |
| S642_9 | generator_script_642 | scripts/Y5_R10_charge_unit_Maxwell_proof_extension_or_kappa_alpha_pressure_runner.py | true | this checkpoint generator |

## Theorem-Zero Attempt

| step_id | derivation_status | candidate_statement | what_it_derives | what_it_does_not_derive | effect_on_kappa_alpha_zero |
| --- | --- | --- | --- | --- | --- |
| TA642_0_parent_U1_bundle | partial_structural_success | Introduce a compact charge phase as a U(1) principal-bundle fibre with theta_Q ~ theta_Q + 2pi. | charge sectors can be labelled by U(1) representations or winding classes rather than a free sign label | the observed charge unit e or the fine-structure value alpha_EM | support_only |
| TA642_1_integer_charge_labels | partial_structural_success_if_U1_is_parent_signed | For compact U(1), single-valued matter wavefunctions transform as exp(i n theta_Q), so representation labels n are integers. | integer relative charge labels Q = n Q_star once a base normalization Q_star exists | Q_star itself, its equality to electron charge e, or a level/index denominator k | does_not_close |
| TA642_2_connection_and_curvature | conditional_Maxwell_form_success | A parent U(1) connection A has curvature F = dA, giving the Bianchi identity dF = 0. | no-monopole/Faraday half of Maxwell in differential-form language if A is the observed EM connection | Gauss/Ampere source normalization, epsilon0, c, hbar, or Lorentz readout | support_only |
| TA642_3_Maxwell_action_variation | closure_form_not_parent_derivation | Vary S_EM = -1/(4 g_EM^2) int F wedge *F + int A wedge *J to obtain d*F = g_EM^2 *J. | the shape of Gauss/Ampere equations after an EM action is assumed | why MTS parent action contains this term, why g_EM is fixed, or why * is the observed coframe Hodge star | blocked_by_free_g_EM |
| TA642_4_coupling_normalization | failed_current_corpus | alpha_EM = g_EM^2/(4 pi hbar c) must be quotient/topological or parent-fixed to make D_v alpha_EM = 0. | nothing new; it names the exact missing owner of the coupling | a parent level, anomaly cancellation, monopole quantization, or Ward/index theorem fixing g_EM | hard_blocker |
| TA642_5_vertical_silence | conditional_theorem_only | If g_EM, hbar, c, and the charge lattice live on quotient/topological data, then vertical local Xhat motion gives D_v alpha_EM = 0. | a clean sufficient condition for local alpha silence | that the sufficient condition is actually satisfied by the MTS parent action | theorem_template_not_claim |

## Maxwell Descent Attempt

| gate_id | equation | descent_attempt | status | missing_owner |
| --- | --- | --- | --- | --- |
| MD642_0_Bianchi | dF = 0 | F=dA from a U(1) connection | conditional_success | parent proof that A is the observed EM connection rather than an added closure field |
| MD642_1_Gauss_Ampere | d*F = g_EM^2 *J | variation of assumed Maxwell action | closure_success_not_parent_success | g_EM, source current normalization, and observed-coframe Hodge star |
| MD642_2_current_conservation | d*J = 0 or nabla_mu J^mu = 0 | Noether/Ward current from compact phase | conditional_support | identification of relative boundary current with EM source current |
| MD642_3_Lorentz_readout | m a^mu = q F^mu_nu u^nu | minimal coupling q int A_mu dx^mu | closure_form_not_parent_derivation | ordinary matter coupling derived from MTS coframe without hidden material marker |
| MD642_4_alpha_constant | alpha_EM = g_EM^2/(4 pi hbar c) | demand quotient-invariant or topological g_EM | blocked | no sourced level, index, anomaly, monopole, or Ward theorem fixes g_EM |

## Zero Verdict

| verdict_id | claim_tested | current_result | reason | allowed_next_branch |
| --- | --- | --- | --- | --- |
| ZV642_0 | kappa_alpha = D_local ln(alpha_EM)/D Xhat = 0 | not_proved | compact U(1) gives integer labels but leaves the base coupling g_EM free; Maxwell form can be written but not parent-owned | finite_coupling_pressure_runner_nonclaim |

## Pressure Runner Smoke

The runner now combines every 641 pressure-envelope row with every 641 cross-arena row. These are symbolic response rows only; none are numeric scores.

| smoke_id | branch_id | arena_id | normalized_abs_kappa_alpha_factor | numeric_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PRS642_00 | KAE641_0_theorem_zero | R0_R1_WEP | 0 | false | false |
| PRS642_01 | KAE641_0_theorem_zero | R2_clocks | 0 | false | false |
| PRS642_02 | KAE641_0_theorem_zero | EM_spectra | 0 | false | false |
| PRS642_03 | KAE641_0_theorem_zero | R10_short_range | 0 | false | false |
| PRS642_04 | KAE641_0_theorem_zero | PPN_Gdot_orbital | 0 | false | false |
| PRS642_05 | KAE641_1_unit_response | R0_R1_WEP | 1 | false | false |
| PRS642_06 | KAE641_1_unit_response | R2_clocks | 1 | false | false |
| PRS642_07 | KAE641_1_unit_response | EM_spectra | 1 | false | false |
| PRS642_08 | KAE641_1_unit_response | R10_short_range | 1 | false | false |
| PRS642_09 | KAE641_1_unit_response | PPN_Gdot_orbital | 1 | false | false |

- Full pressure-smoke rows: `25`

## Runner Schema Blocks

| input_id | needed_input | status | why_needed | blocks_numeric_score |
| --- | --- | --- | --- | --- |
| RS642_0 | physical Xhat unit | missing | turns normalized pressure factors into a derivative with units | true |
| RS642_1 | tau_R10, tau_WEP, tau_clock, tau_EM | missing | projects parent/local alpha response into each arena observable | true |
| RS642_2 | composition and clock alpha sensitivities | missing | WEP and clocks cannot score alpha pressure without material/transition sensitivity coefficients | true |
| RS642_3 | source/test-body EM binding normalization for R10 | missing | short-range force limits constrain body-level residuals, not raw alpha_EM derivatives | true |
| RS642_4 | parent owner of g_EM or explicit finite prior | missing | chooses theorem-zero route or honest finite-coupling route | true |

## Decision

| decision_id | route | result | reason | next_action |
| --- | --- | --- | --- | --- |
| D642_0 | theorem_zero | blocked | compact U(1) and connection geometry do not fix g_EM or alpha_EM | hunt owner of alpha normalization: level/index/anomaly/monopole/Ward or explicit finite prior |
| D642_1 | finite_coupling_pressure_runner | schema_ready_nonclaim | pressure rows and cross-arena symbolic reactions can be combined, but all score-critical inputs are missing | 643-Y5-R10-alpha-normalization-owner-or-finite-coupling-bound-input-fill.md |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V642_0_source_paths_exist | pass | all cited local source paths exist |
| V642_1_prior_641_validation_clean | pass | 641 validation remains clean |
| V642_2_theorem_has_partial_success | pass | U1 route records real partial structural successes |
| V642_3_theorem_still_blocks_claim | pass | coupling normalization blocker remains explicit |
| V642_4_maxwell_alpha_blocked | pass | alpha constant gate remains blocked |
| V642_5_zero_verdict_nonclaim | pass | zero verdict is not claim-valid |
| V642_6_pressure_smoke_row_count | pass | pressure smoke covers every 641 envelope x arena pair |
| V642_7_pressure_rows_nonclaim | pass | pressure smoke rows remain nonclaim |
| V642_8_schema_blocks_numeric_score | pass | runner schema keeps numeric score blocked |
| V642_9_decisions_nonclaim | pass | decision rows do not claim a pass |
| V642_10_summary_nonclaim | pass | summary stays nonclaim |
| V642_11_formalization_workbench_unchanged | pass | formalization files changed after cutoff: 0 |

## Interpretation

- This is a useful narrowing, not a dead end: the EM branch is not missing everything; it is missing the owner of the coupling.
- The cleanest possible route is now sharply defined: find a parent level/index/anomaly/monopole/Ward reason that fixes `g_EM` or makes it quotient-invariant.
- If that owner cannot be found, the honest route is finite `kappa_alpha`, but it must be projected through real `Xhat` units, `tau` maps, and material sensitivities before any comparison score.

## Nonclaim Summary

| status | theorem_zero_claim | maxwell_claim | pressure_runner_claim | numeric_score_allowed | hardest_blocker | next_target |
| --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_U1_charge_structure_partial_coupling_normalization_still_blocks_kappa_alpha_zero_pressure_runner_nonclaim | false | false | false | false | the base EM coupling g_EM/alpha_EM is still free unless a parent level/index/anomaly/monopole/Ward owner is found | 643-Y5-R10-alpha-normalization-owner-or-finite-coupling-bound-input-fill.md |
