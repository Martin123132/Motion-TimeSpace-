# 1355-Y5-R10-RAB-Y5-source-functional-pullback-or-JZ-source-normalization-basis

**Current verdict:** 1355 does not derive Y5 measured-GM/source-normalization as a quotient pullback. The source functional still has open `J_Z` channels unless same-frame Hilbert current, parent `Pi_M`, flux closure, worldtube glue, and no-absorption calibration all close.

**Main progress:** the Y5 obstruction is now in a usable basis. The eight source-normalization channels are tied to exact obstruction objects (`-Pi_M dJ_extra`, `[d,Pi_M]J_H`, `A_parent`, `R_eq`, `B_zero_flux`, calibration tails) rather than vague fitted-G language.

## Source register

| source_id | source_path | exists | anchor_found | purpose |
| --- | --- | --- | --- | --- |
| SRC1355_0_1354_doc | 1354-Y5-R10-RAB-source-functional-evenness-theorem-or-Y5Y6-JZ-coefficient-fill.md | True | True | 1354 blocks source-functional evenness and selects Y5. |
| SRC1355_1_1354_next | source-intake/mts_residuals/P8_Y5_R10_1354_NEXT_TARGET.csv | True | True | handoff to Y5 source-functional pullback. |
| SRC1355_2_1354_y5_coeffs | source-intake/mts_residuals/P8_Y5_R10_1354_Y5Y6_JZ_COEFFICIENT_FILL.csv | True | True | Y5 source-normalization JZ coefficient rows. |
| SRC1355_3_1012_y5_doc | 1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md | True | True | prior Y5 owner theorem attempt and eight-channel vector. |
| SRC1355_4_1013_flux_doc | 1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md | True | True | measured-GM flux closure theorem attempt. |
| SRC1355_5_1013_vector | source-intake/mts_residuals/P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv | True | True | exact measured-GM obstruction vector. |
| SRC1355_6_1014_coeffs | source-intake/mts_residuals/P8_Y5_R10_1014_COEFFICIENT_BOUND_ROWS.csv | True | True | Pi_M commutator/projector coefficient debts. |
| SRC1355_7_1029_cg_doc | 1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md | True | True | frame relabel warning: couplings can move into source-normalization. |

## Y5 pullback theorem attempt

| clause_id | claim_piece | required_form | status | if_missing |
| --- | --- | --- | --- | --- |
| YPB1355_0_same_frame | same observed coframe for matter, clocks, source current, and orbit | S_matter[psi,e_obs] defines J_H[e_obs] and the same e_obs defines rods, clocks, orbital readout, and source measure | CONDITIONAL_NOT_PARENT_DERIVED | source pullback can hide a frame coupling as measured-GM drift |
| YPB1355_1_quotient_pullback | measured source functional factors through quotient-visible data and is even in Z | mu_obs = mu_bar[q(Phi),theta_source] with D_Z q=0 or Z exchange-even before readout | NOT_SUPPLIED | J_Z[Y5] remains a live coupling |
| YPB1355_2_PiM_parent_origin | Pi_M is parent-owned before readout | Pi_M maps J_H to an absolute/topological mass-flux class without post-fit masking | NOT_PARENT_DERIVED | projector can introduce source-normalization hair |
| YPB1355_3_flux_closure | compact-exterior projected Hilbert flux closes | d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H=0 or exact obstruction vector is scored | EXACT_OBSTRUCTION_NOT_ZERO | radial/time/source residuals survive |
| YPB1355_4_worldtube_glue | worldtube source measure equals exterior parent charge before orbital fitting | M_source[W]=int_S Q_M[tau]=M_eff with fixed calibration | NOT_DERIVED_CORE_MISSING_PIECE | closed wrong charge can mimic Newton recovery |
| YPB1355_5_no_extra_mu_channels | no extra source-normalization channels remain | mu_extra boundary/bulk/domain/projector/memory/nonEH/species/time/calibration terms are theorem-zero or bounded | RETAINED_DEBT | Y5 source functional is not even/quotient-only |
| YPB1355_6_no_absorption | J_Z is not absorbed into fitted G or source calibration | range/time/species/radial/frame derivatives are zero or carried as explicit residual rows | RULE_WRITTEN_NOT_SATISFIED | a coupling can disappear by notation and reappear as measured-GM |
| YPB1355_7_Newton_Poisson_orbit | same charge sources Poisson/Gauss and orbital acceleration | nabla^2 Phi=4pi G_ref rho_H and a_r=-G_ref M_ref/r^2 from the same parent charge | CONDITIONAL_NOT_PARENT_DERIVED | Newton recovery cannot be claimed even if a charge is conserved |
| YPB1355_8_verdict | Y5 source-functional pullback theorem | YPB1355_0 through YPB1355_7 all pass with source paths | PULLBACK_THEOREM_NOT_PROVED | retain Y5 J_Z basis as nonclaim |

## Y5 JZ basis

| basis_id | basis_symbol | basis_formula | dominant_obstruction | observable_link | current_status | accepted_for_scoring |
| --- | --- | --- | --- | --- | --- | --- |
| Y5JZ1355_0_radial_Meff_hair | j_Z_radial_Meff | M_eff^-1 int_A[-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent]_radial | OBS1013_6_flux_leak;PCC1014_5_epsilon_radial_Meff | partial_r ln(mu_obs); beta_minus_1; alpha(lambda); R11 | MISSING_RADIAL_PROFILE_OR_THEOREM | False |
| Y5JZ1355_1_boundary_monopole | j_Z_boundary | M_eff^-1 int_boundary B_zero_flux or boundary/source-reference shift | OBS1013_4_boundary_zero_flux;PCC1014_2_B_zero_flux | beta_minus_1; alpha3; xi; Gdot_over_G; R11 | MISSING_BOUNDARY_ZERO_OR_VALUE | False |
| Y5JZ1355_2_domain_projector_mass | j_Z_domain_projector | M_eff^-1 int_A [d,Pi_M]J_H + delta_g Pi_M stress source projected onto domain selector | OBS1013_1_PiM_commutator;OBS1013_5_projector_stress;PCC1014_1_I_commutator | alpha1; alpha2; alpha3; xi; R11 | MISSING_PROJECTOR_COMMUTATOR_OR_STRESS_MAP | False |
| Y5JZ1355_3_bulk_X_Yukawa | j_Z_bulk_X | finite-range X/source tail contribution to mu_extra(lambda) | OBS1013_0_projected_extra_current plus R10 alpha(lambda) source map | alpha(lambda); R10; R11 | MISSING_BULK_GAP_OR_ALPHA_CURVE | False |
| Y5JZ1355_4_nonEH_operator | j_Z_nonEH_source | non-EH/source operator vector projected into measured-GM and PPN response | OBS1013_0_projected_extra_current;OBS1013_7_calibration_PPN_tail | gamma_minus_1; beta_minus_1; alpha(lambda); R11 | MISSING_NONEH_OPERATOR_COEFFICIENT_MAP | False |
| Y5JZ1355_5_species_source | j_Z_species_A | species/material source charge vector after source-worldtube/readout projection | OBS1013_0_projected_extra_current; 1029 frame/source relabel warning | eta_WEP_source_charge; clock source residual; R11 | MISSING_SPECIES_CHARGE_VECTOR | False |
| Y5JZ1355_6_time_drift | j_Z_time_drift | d ln M_eff/dt or d ln mu_obs/dt from finite-annulus flux leakage | OBS1013_6_flux_leak; constant-GM residual rows | Gdot_over_G; R11 | MISSING_TIME_DRIFT_PROFILE_OR_STATIONARITY | False |
| Y5JZ1355_7_calibration_offset | j_Z_calibration | Delta_cal + Delta_PPN from closed-charge-to-orbit calibration mismatch | OBS1013_7_calibration_PPN_tail; Y5O1012_6 no-absorption rule | beta_minus_1; Gdot_over_G; R11 | MISSING_CALIBRATION_THEOREM_OR_OFFSET | False |

## Obstruction links

| link_id | source_object | exact_form | basis_rows | status |
| --- | --- | --- | --- | --- |
| LINK1355_0_exact_obstruction | d(Pi_M J_H) | Pi_M dJ_H + [d,Pi_M]J_H; with extra channels: -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent | Y5JZ1355_0;Y5JZ1355_2;Y5JZ1355_6 | RETAINED_UNFILLED |
| LINK1355_1_worldtube_glue | M_source[W]=int_S Q_M[tau]=M_eff | worldtube/exterior equality before orbital fitting | all Y5JZ1355 rows | NOT_DERIVED_CORE_MISSING_PIECE |
| LINK1355_2_no_absorption | G/calibration/readout separation | constant calibration may be absorbed; Z-dependent radial/time/species/frame terms may not | Y5JZ1355_5;Y5JZ1355_6;Y5JZ1355_7 | RULE_WRITTEN_NOT_SATISFIED |

## Claim gates

| gate_id | claim | current_status | reason | claim_allowed |
| --- | --- | --- | --- | --- |
| GATE1355_0_Y5_pullback | Y5 measured-GM/source-normalization is a quotient pullback even in Z | BLOCKED | same-frame, Pi_M origin, flux closure, worldtube glue, and no-extra-channel clauses fail | False |
| GATE1355_1_Y5_JZ_zero | all Y5 J_Z source-normalization coefficients vanish | BLOCKED | eight J_Z basis rows are missing values or theorem-zero certificates | False |
| GATE1355_2_Newton_GR_recovery | Newton/GR source normalization is derived | BLOCKED | measured-GM pullback and obstruction score are not claim-ready | False |

## Decision ledger

| decision_id | decision | why | next_action |
| --- | --- | --- | --- |
| DEC1355_0_pullback_not_closed | Y5 source-functional pullback is not closed. | quotient pullback alone is missing; the exact Pi_M/J_H obstruction and worldtube glue are still open | attack Pi_M/J_H/worldtube equality or score the obstruction basis |
| DEC1355_1_basis_installed | The Y5 J_Z basis is installed row-by-row. | this prevents measured-GM/source-normalization from being hidden inside a fitted G | derive or source each basis coefficient before any Newton/local-GR claim |
| DEC1355_2_best_next_target | Best next target is the worldtube/Hilbert equality route. | without M_source[W]=int_S Q_M=M_eff, a conserved charge can still be the wrong Newtonian source | try worldtube-Hilbert source equality or retain R_eq/I_commutator rows |

## Next target

| next_id | target_file | target_script | task | success_condition | do_not |
| --- | --- | --- | --- | --- | --- |
| NEXT1355_0_1356 | 1356-Y5-R10-RAB-worldtube-Hilbert-source-equality-or-R_eq-Icommutator-fill.md | scripts/Y5_R10_RAB_worldtube_Hilbert_source_equality_or_Req_Icommutator_fill.py | try to prove worldtube source measure equals the exterior Hilbert/topological mass charge before orbital fitting; if not, retain R_eq, I_commutator, and calibration rows as nonclaim | worldtube-Hilbert equality theorem, or explicit nonclaim R_eq/I_commutator/calibration source rows with units | do not absorb residuals into fitted G; do not use closed wrong charge as Newton recovery; do not edit formalization-workbench or use GitHub |

## Validation

| check_id | check | status | details |
| --- | --- | --- | --- |
| VAL1355_0_sources_exist | registered source paths exist and anchors are found | PASS | SRC1355_0_1354_doc=True/True;SRC1355_1_1354_next=True/True;SRC1355_2_1354_y5_coeffs=True/True;SRC1355_3_1012_y5_doc=True/True;SRC1355_4_1013_flux_doc=True/True;SRC1355_5_1013_vector=True/True;SRC1355_6_1014_coeffs=True/True;SRC1355_7_1029_cg_doc=True/True |
| VAL1355_1_pullback_not_proved | Y5 pullback theorem is not promoted | PASS | retain Y5 J_Z basis as nonclaim |
| VAL1355_2_basis_has_eight_rows | Y5 JZ basis has eight source-normalization rows | PASS | rows=8 |
| VAL1355_3_basis_nonclaim | basis rows remain missing/unscored/nonclaim | PASS | all basis rows reject scoring |
| VAL1355_4_obstruction_links_present | obstruction links connect basis to PiM/worldtube/no-absorption debts | PASS | links=3 |
| VAL1355_5_claim_gates_blocked | all claim gates remain blocked | PASS | GATE1355_0_Y5_pullback=BLOCKED;GATE1355_1_Y5_JZ_zero=BLOCKED;GATE1355_2_Newton_GR_recovery=BLOCKED |
| VAL1355_6_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false across generated rows |
| VAL1355_7_formalization_untouched | formalization-workbench untouched by generated outputs | PASS | formalization_generated_output_count=0 |
| VAL1355_8_next_target_1356 | next target routes to worldtube-Hilbert equality | PASS | 1356-Y5-R10-RAB-worldtube-Hilbert-source-equality-or-R_eq-Icommutator-fill.md |
| VAL1355_9_overall | overall 1355 validation | PASS | 1355 blocks Y5 pullback claim and installs source-normalization JZ basis |
