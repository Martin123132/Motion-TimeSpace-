# 2342 - source charge equals measured GM or selector bound

## Summary

2342 attacks the bridge that decides whether the EH-anchor/Hamiltonian charge is the **measured** Newtonian source.

The desired theorem is:

`GM_orbit = G_ref M_H_ref`,

where `M_H_ref = H_tau[S_outer] - H_ref` is selected before orbital fitting and equals the observed Hilbert/source
charge in the same frame.

That bridge is not derived yet. The blocker is not cosmetic: a conserved charge is not automatically measured `GM`.
The theory still needs a parent-signed worldtube selector, same-frame Hilbert source current, fixed `M_H_ref`,
Poisson/Gauss orbital readout, and a constant universal coupling with no relative source/species/profile prefactors.

So 2342 stages selector/source-GM bound rows and chooses the coupling/source-GM descent theorem as the next best attack.

## Source Register

| row_id | source_key | source_path | exists | required | needles_found | source_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC2342_00_2341_doc | 2341_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2341-Y5-R2FR-EH-anchor-residual-charge-zero-or-coefficient-row.md | true | true | true | 2341 selected source-charge measured-GM bridge | false |
| SRC2342_01_2341_validation | 2341_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2341_VALIDATION.csv | true | true | true | 2341 validation | false |
| SRC2342_02_2341_next | 2341_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2341_NEXT_TARGET.csv | true | true | true | machine-readable 2342 target | false |
| SRC2342_03_2341_components | 2341_components | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2341_DELTA_QRES_COMPONENT_MAP.csv | true | true | true | Delta_Q source/coupling residual components | false |
| SRC2342_04_1016_doc | 1016_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md | true | true | true | parent worldtube/source-measure selector | false |
| SRC2342_05_hsm_contract | hsm_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv | true | true | true | Hamiltonian source-measure contract | false |
| SRC2342_06_hsm_scorecard | hsm_scorecard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_HAMILTONIAN_SOURCE_MEASURE_SCORECARD.csv | true | true | true | source-measure scorecard | false |
| SRC2342_07_source_measure_attempt | source_measure_attempt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_SOURCE_MEASURE_THEOREM_ATTEMPT.csv | true | true | true | source-measure theorem attempt | false |
| SRC2342_08_hilbert_worldtube | hilbert_worldtube | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv | true | true | true | Hilbert worldtube glue attempt | false |
| SRC2342_09_poisson_gauss | poisson_gauss | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv | true | true | true | Poisson/Gauss orbital bridge contract | false |
| SRC2342_10_hilbert_mono | hilbert_mono | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Hilbert_monopole_calibration_CONTRACT.csv | true | true | true | Hilbert monopole calibration contract | false |
| SRC2342_11_gm_obstruction | gm_obstruction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2203_MEASURED_GM_OBSTRUCTION_VECTOR.csv | true | true | true | measured-GM obstruction vector | false |
| SRC2342_12_source_gm_universality | source_gm_universality | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2327_SOURCE_GM_UNIVERSALITY_ATTEMPT.csv | true | true | true | source-GM universality attempt | false |
| SRC2342_13_gm_absorption_refusal | gm_absorption_refusal | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2125_GM_ABSORPTION_REFUSAL.csv | true | true | true | measured-G/GM hiding refusal | false |
| SRC2342_14_same_frame_gate | same_frame_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv | true | true | true | same-frame GM denominator gate | false |

## Source-GM Bridge Audit

| row_id | claim_piece | formal_statement | status | proof_or_obstruction | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SGM2342_0_target | source charge equals measured GM | G_ref M_H_ref = GM_orbit and the same H_tau-H_ref charge sources the weak-field Poisson/Gauss monopole read by orbits. | TARGET_SHARPENED | this is the bridge from EH-anchor charge to Newtonian measured mass | selector/source-measure residual vector | false |
| SGM2342_1_Htau_MHref | integrable dressed Hamiltonian charge | M_H_ref := H_tau[S_outer]-H_ref is finite, positive, fixed-reference and same-frame before readout. | MISSING_MHREF_SOURCE_ROW | 2339/2340 staged the row but H_tau, H_ref and parent certificates are missing | epsilon_MHref_missing_abs | false |
| SGM2342_2_worldtube_selector | pre-readout source worldtube | W_source=closure(supp J_H[tau]) and linked surfaces enclose the same source before orbital fitting. | CONDITIONAL_SELECTOR_NOT_PARENT_SIGNED | 1016/HWT536 keep compactness, support selector and same-frame source measure open | epsilon_worldtube_selector_abs | false |
| SGM2342_3_Hilbert_charge | Hamiltonian charge equals observed Hilbert/source charge | M_H_ref = integral_S Q_tau = integral_W J_H[tau] after fixed reference and boundary lock. | MISSING_HILBERT_NOETHER_EQUALITY | Pi_M/Hilbert/topological equality, R_eq and I_commutator remain unsigned | epsilon_source_measure_abs | false |
| SGM2342_4_Poisson_Gauss | Poisson/Gauss/orbital readout | the same charge appears in nabla^2 Phi=4*pi*G_ref rho and a_r=-G_ref M_H_ref/r^2 for test bodies. | CONDITIONAL_NOT_PARENT_DERIVED | PG0-PG10 are contract rows; HSM541 scorecard keeps Gauss/orbital readout failed | epsilon_PG_orbit_abs | false |
| SGM2342_5_constant_G | constant universal G_ref | partial_t,r,source,species,range,frame G_ref=0 and no relative source prefactor survives fitted common-mode GM. | MISSING_UNIVERSAL_COUPLING_DESCENT | 2327 and 2125 keep NoSourceOnlySpeciesSlot and measured-G hiding refusal active | epsilon_source_GM_rel_abs | false |
| SGM2342_6_verdict | promote source-charge equals measured-GM bridge now | SGM2342_1 through SGM2342_5 all parent-signed would permit GM_orbit to be a derived readout of M_H_ref rather than a denominator input. | BRIDGE_NOT_DERIVED_RETAIN_SELECTOR_BOUNDS | current corpus has conditional lemmas and obstruction vectors, not the source-GM theorem | stage selector/source-GM bound rows | false |

## Selector Source-Measure Contract

| row_id | selector_clause | formula | required_for_claim | current_status | residual_if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SSC2342_0_selector | source worldtube | W_source := closure(supp J_H[tau]) | same observed coframe, compact support, linked surfaces and pre-readout rule | CONDITIONAL_NOT_SIGNED | Delta_worldtube_domain | false |
| SSC2342_1_charge | dressed charge | M_source[W]=M_H_ref=H_tau[S_outer]-H_ref | integrable H_tau, fixed H_ref, positive same-frame M_H_ref | MISSING_M_H_REF | epsilon_MHref_missing_abs | false |
| SSC2342_2_Hilbert | Hilbert/source equality | M_H_ref = integral_W J_H[tau] = integral_S Q_tau | parent Hilbert current, Pi_M/source map, R_eq=0 and I_commutator=0 or bounds | MISSING_SOURCE_MEASURE_EQUALITY | epsilon_source_measure_abs | false |
| SSC2342_3_Gauss | orbital readout | GM_orbit=G_ref M_H_ref after Poisson/Gauss bridge | PG0-PG10 and HM0-HM8 pass; no non-Hilbert channels | MISSING_POISSON_GAUSS_BRIDGE | epsilon_PG_orbit_abs | false |
| SSC2342_4_universal_G | universal coupling | D_source,species,range,frame G_ref = 0 up to a single common-mode calibration | NoSourceOnlySpeciesSlot and source/profile GM universality | MISSING_NO_SOURCE_ONLY_SPECIES_SLOT | epsilon_source_GM_rel_abs | false |

## Source-GM Obstruction Vector

| row_id | obstruction | symbol | source_anchor | blocks | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SGO2342_0_extra_current | projected extra current | -Pi_M dJ_extra | MGV2203_0_projected_extra_current | fixed-before-readout GM/PPN map | retained_unfilled | false |
| SGO2342_1_PiM_commutator | projector commutator | [d,Pi_M]J_H | MGV2203_1_PiM_commutator | source charge equality and R_eq normalization | retained_unfilled | false |
| SGO2342_2_R_eq | topological/Hilbert equality residual | R_eq | MGV2203_3_topological_equality_residual | closed charge equals observed mass | retained_unfilled | false |
| SGO2342_3_boundary | boundary zero flux | B_zero_flux | MGV2203_4_boundary_zero_flux | fixed reference/source charge equality | retained_unfilled | false |
| SGO2342_4_flux_leak | radial/time source-measure flux leakage | dln_Meff_dt or epsilon_radial_Meff | MGV2203_6_flux_leak | radially stable measured GM | retained_unfilled | false |
| SGO2342_5_calibration_tail | Gauss/orbital/PPN calibration tail | Delta_cal + Delta_PPN | MGV2203_7_calibration_PPN_tail | Newton/PPN followthrough | retained_unfilled | false |
| SGO2342_6_relative_source_GM | relative source/profile/composition GM residual | epsilon_sigma_source_GM | UGM2327_6_verdict | universal coupling and source-label forgetting | not_proved_use_bound_route | false |

## Selector Bound Rows

| row_id | quantity | formula | current_value | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SGB2342_0_selector_abs | epsilon_selector_GM_abs | abs(Delta_worldtube_domain)+abs(Delta_frame_source)+abs(R_eq)/M_H_ref+abs(I_commutator)/M_H_ref+abs(B_zero_flux)/M_H_ref | MISSING_COMPONENT_INPUTS;MISSING_M_H_REF | false | false |
| SGB2342_1_source_GM_abs | epsilon_source_GM_abs | abs(GM_orbit/G_ref/M_H_ref - 1) with no orbital-GM backfill | MISSING_GM_BRIDGE;MISSING_M_H_REF | false | false |
| SGB2342_2_relative_G_abs | epsilon_source_GM_rel_abs | norm(relative source/species/profile weights after one common GM calibration) | MISSING_NO_SOURCE_ONLY_SPECIES_SLOT;MISSING_PROFILE_VECTOR | false | false |
| SGB2342_3_total_bridge_abs | epsilon_GM_bridge_abs | epsilon_selector_GM_abs + epsilon_source_GM_abs + epsilon_source_GM_rel_abs + epsilon_PG_orbit_abs | MISSING_COMPONENT_INPUTS | false | false |

## Decision Ledger

| row_id | decision | reason | consequence | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC2342_0_bridge_result | do not claim source charge equals measured GM | M_H_ref, worldtube selector, Hilbert/source equality, Poisson/Gauss readout and universal-G descent are all unsigned | Newton/local-GR recovery remains blocked by the source-measure bridge | SOURCE_GM_BRIDGE_NOT_DERIVED | false |
| DEC2342_1_bound_rows | stage selector/source-GM bound rows | the failed bridge decomposes into executable selector, calibration and relative-source residuals | future work can prove or fill one source-measure component at a time | SELECTOR_BOUND_ROWS_STAGED_NONCLAIM | false |
| DEC2342_2_next | attack NoSourceOnlySpeciesSlot plus same-frame GM descent next | a single fitted GM can hide only common mode; relative source weights are the sharpest coupling countermodel | next target goes after the coupling key directly before using measured GM as evidence | SELECT_COUPLING_SOURCE_GM_DESCENT_NEXT | false |
| DEC2342_3_public_policy | no GitHub update from 2342 | this is private bridge triage and residual plumbing, not a public claim checkpoint | continue private derivation sequence | NO_GITHUB_EVIDENCE_UPDATE | false |

## Claim Gates

| row_id | gate | passed | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2342_0_MHref | M_H_ref exists as positive fixed source charge | false | H_tau/H_ref row remains unfilled | false |
| CG2342_1_worldtube_selector | source worldtube selector parent-signed | false | support/same-frame/linking clauses conditional | false |
| CG2342_2_Hilbert_charge | Hamiltonian charge equals Hilbert/source charge | false | R_eq/I_commutator/projector still open | false |
| CG2342_3_Poisson_Gauss | same charge gives orbital GM | false | PG/HM bridge remains conditional | false |
| CG2342_4_universal_G | constant universal source-blind G_ref | false | NoSourceOnlySpeciesSlot not parent-signed | false |
| CG2342_5_bridge_score | selector/source-GM bound rows score-ready | false | component values and M_H_ref missing | false |
| CG2342_6_local_GR_Newton | local GR/Newton recovery derived | false | source-measure bridge remains open | false |
| CG2342_7_github | safe public GitHub update | false | private checkpoint only | false |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2342_0_orbital_GM_backfill | use observed GM_orbit/G_ref to fill M_H_ref | false | this borrows Newton to prove the Newton/source normalization bridge | SGM2342_1_Htau_MHref;SGM2342_4_Poisson_Gauss | false |
| REF2342_1_common_mode_hiding | absorb all source/coupling differences into fitted GM | false | only one universal common mode can be calibrated; relative source/profile/species components remain observable | SGM2342_5_constant_G;SGB2342_2_relative_G_abs | false |
| REF2342_2_bulk_profile_shortcut | use bulk composition/profile as the source worldtube vector | false | the source profile must be orbit/worldtube/support weighted or theorem-cancelled | SSC2342_0_selector;SGB2342_2_relative_G_abs | false |
| REF2342_3_closed_charge_equals_measured_mass | a conserved charge is automatically measured GM | false | closed charge can be the wrong conserved object without Hilbert/source and Poisson/Gauss bridges | SGM2342_3_Hilbert_charge;SGM2342_4_Poisson_Gauss | false |
| REF2342_4_local_claim | 2342 proves Newton/local-GR recovery | false | 2342 stages a nonclaim bridge and bound rows; it does not derive measured-GM equality | DEC2342_0_bridge_result;CG2342_6_local_GR_Newton | false |

## Next Target

| row_id | next_target | why | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2342_0 | 2343-Y5-R2FR-NoSourceOnlySpeciesSlot-and-same-frame-GM-descent-or-sourceGM-bound.md | relative source weights are the sharpest coupling countermodel; proving their absence is the cleanest next derivation step. | private_derivation_next_step | false |
| NEXT2342_1 | 2343b-Y5-R2FR-Poisson-Gauss-orbital-bridge-or-DeltaPG-row.md | parallel bridge: derive that the same charge produces the Poisson/Gauss monopole read by orbits. | parallel_nonclaim | false |
| NEXT2342_2 | 2343c-Y5-R2FR-selector-sourceGM-bound-row-runner.md | fallback route: fill selector/source-GM residual rows with units, source paths and component maps. | fallback_nonclaim | false |

## Branch Copies

| row_id | source_csv | branch_copy_path | copy_exists | row_count | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| COPY2342_0_bridge | source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2342_SOURCE_GM_BRIDGE_AUDIT.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\beta-source\docs\SOURCE_GM_BRIDGE_AUDIT_2342_NONCLAIM.csv | true | 7 | false |
| COPY2342_1_bounds | source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2342_SELECTOR_BOUND_ROWS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\SELECTOR_BOUND_ROWS_2342_NONCLAIM.csv | true | 4 | false |
| COPY2342_2_decision | source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2342_DECISION_LEDGER.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2342_SOURCE_GM_DECISION_LEDGER_NONCLAIM.csv | true | 4 | false |

## Validation

| row_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL2342_00_required_sources_exist | PASS | every required source path exists | false |
| VAL2342_01_required_needles_found | PASS | all required source needles were found | false |
| VAL2342_02_bridge_not_promoted | PASS | source-GM bridge not promoted | false |
| VAL2342_03_selector_contract_written | PASS | selector/source-measure contract includes universal-G clause | false |
| VAL2342_04_obstruction_vector_written | PASS | measured-GM obstruction vector includes relative source residual | false |
| VAL2342_05_bound_rows_nonready | PASS | selector/source-GM bound rows remain non-score-ready | false |
| VAL2342_06_claim_gates_blocked | PASS | all claim gates remain blocked | false |
| VAL2342_07_refusals_block_shortcuts | PASS | shortcut claims refused | false |
| VAL2342_08_next_selected | PASS | 2343 NoSourceOnlySpeciesSlot next target recorded | false |
| VAL2342_09_github_blocked | PASS | public GitHub update not recommended from 2342 | false |
| VAL2342_10_branch_copies_parse | PASS | branch copies exist and parse | false |
| VAL2342_11_outputs_exist | PASS | CSV outputs and branch copies exist before doc render | false |
| VAL2342_12_no_claim_flags | PASS | no generated row is valid_for_claim=true | false |
| VAL2342_13_formalization_untouched_by_2342 | PASS | no 2342 checkpoint output appears in formalization-workbench | false |
| VAL2342_OVERALL | PASS | 2342 tests the source-charge measured-GM bridge, rejects shortcut promotion, stages selector/source-GM bounds, and selects coupling/source-GM descent next. | false |
