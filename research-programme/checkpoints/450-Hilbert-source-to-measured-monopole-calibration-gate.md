# 450 - Hilbert Source to Measured Monopole Calibration Gate

Private P8/R1/R4/R9/R10/R11 measured-GM checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 449 gave the useful conditional Hilbert/Ward source-current sublemma. This checkpoint asks the harder Newton question: when is that formal Hilbert current equal to the measured orbital monopole `GM`?

The answer is strict. A conserved Hilbert current helps, but Newton needs a closed, absolutely calibrated mass-flux projector and no hidden boundary, bulk, domain, memory, range, connection, species, radial, or time-dependent source contribution.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/Hilbert_source_to_measured_monopole_calibration_gate.py` |
| Run directory | `runs\20260602-160000-Hilbert-source-to-measured-monopole-calibration-gate` |
| Status | `Hilbert_source_to_measured_monopole_calibration_gate_written_conditional_Newton_bridge_calibration_not_parent_derived_P8_R1_R4_R9_R10_R11_retained_no_Newton_or_local_GR_pass` |
| Claim ceiling | `Hilbert_monopole_calibration_gate_only_no_measured_GM_Newton_PPN_or_local_GR_pass` |
| Contract | `source-intake\mts_residuals\P8_Hilbert_monopole_calibration_CONTRACT.csv` |
| Next target | `451-mass-flux-projector-Euler-calibration-attempt.md` |

## 3. Source Register

| source_file | exists | role |
| --- | --- | --- |
| 402-EH-source-normalization-parent-pair.md | True | EH/source weak-field chain and mu_obs decomposition |
| 424-same-frame-EH-source-Poisson-reduction-gate.md | True | Poisson bridge and measured-GM requirements |
| 445-measured-GM-Ward-source-ownership-theorem-attempt.md | True | Ward source ownership theorem and measured-GM caveats |
| 446-source-owner-current-parent-action-contract.md | True | A4 mass-flux projector and parent action calibration terms |
| 449-source-current-Ward-universality-theorem-attempt.md | True | Hilbert source-current sublemma and next target |
| source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv | True | SC6 closed calibrated mass projector requirement |
| source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv | True | C3 closed calibrated mass current requirement |
| source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv | True | A4 mass-flux projector parent action block |
| source-intake/mts_residuals/P8_q_retained_zero_conditions_CONTRACT.csv | True | legal residual-current zero routes |
| source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv | True | P8 source-normalization residual fallback |
| source-intake/local_bounds/local_bound_claims.csv | True | R1/R4/R9/R10 local source locks |
| runs/20260602-143000-source-normalization-residual-vector-refinement/results/mu_obs_decomposition.csv | True | mu_obs source-normalization decomposition |
| runs/20260602-143000-source-normalization-residual-vector-refinement/results/P8_source_residual_template_rows.csv | True | P8 measured-GM residual rows |
| runs/20260602-123000-auxiliary-projector-local-Euler-equation-ledger/results/Euler_ledger_rows.csv | True | A7 mass-flux projector Euler ledger |
| runs/20260602-154500-source-current-Ward-universality-theorem-attempt/results/source_current_Ward_contract.csv | True | machine source-current Ward contract rows |

## 4. Theorem Statement

| part | statement | mathematical_form | status |
| --- | --- | --- | --- |
| conditional_measured_monopole_theorem | If the Hilbert/coframe current is the only active source, the mass-flux projector is closed and absolutely calibrated, the coupling is constant and universal, and all boundary/bulk/domain/range/species residual currents vanish or are retained below locks, then measured orbital GM equals the Hilbert monopole. | mu_obs = G_eff M_eff[J_H] + mu_extra; d(Pi_M J_H)=0; mu_extra=0; partial_{t,r,A,lambda} mu_obs=0 => mu_obs=G_eff M_H | valid_conditional_Newton_source_bridge |
| calibration_limit | A conserved Hilbert current is not automatically the measured Newtonian monopole; conservation does not fix the absolute normalization, the surface flux, or the absence of finite-range/radial/source-charge corrections. | nabla_mu T_H^{mu nu}=0 does not imply M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J_H or mu_extra=0 | blocks_overclaim |
| current_corpus_status | The current corpus has the right calibration contracts and residual-vector rows, but it has not derived the mass-flux Euler equation, absolute calibration, zero compact-boundary flux, or constant universal coupling. | A4/C3/SC6 remain conditional_flux_calibration_open | not_parent_derived |

## 5. Calibration Chain

| step | chain_item | mathematical_form | needed_for | current_status |
| --- | --- | --- | --- | --- |
| 1 | Hilbert source current | J_H from T_H^{mu nu}=2/sqrt(-g) delta S_m/delta g_munu or coframe equivalent | formal matter source | conditional_from_449 |
| 2 | mass-flux projector | Pi_M J_H selects the compact source monopole current | separate mass monopole from stress/improvement/exchange terms | conditional_flux_calibration_open |
| 3 | closed current | d(Pi_M J_H)=0 or nabla_mu J_M^mu=0 | no source mass drift and no hidden exchange | not_parent_derived |
| 4 | absolute calibration | M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J_H | turn source current into measured orbital GM | not_parent_derived |
| 5 | constant universal coupling | G_eff=kappa_eff c^4/(8 pi), partial_{t,r,A,lambda}G_eff=0 | Newtonian constant G rather than source-dependent calibration | not_parent_derived |
| 6 | zero residual source monopole | mu_extra=mu_boundary+mu_bulk+mu_domain+mu_memory+mu_range+mu_connection=0 | no hidden source hair or measured-GM absorption | not_parent_derived |
| 7 | first-order Newton source | nabla^2 Phi=4 pi G_eff rho_H with mu_obs=G_eff M_H | Newtonian measured-GM force law | conditional_if_all_prior_steps_close |
| 8 | second-order stability | delta_beta_source=0 after the same normalization | PPN beta/local-GR completion | not_derived |

## 6. Monopole Requirements

| requirement_id | requirement | mathematical_form | failure_mode | affected_rows | current_status |
| --- | --- | --- | --- | --- | --- |
| M0_same_frame_current | Hilbert current is varied in the same observed frame used by matter, clocks, rods, and the EH/Poisson operator | e_source=e_matter=e_metric=e_obs | frame calibration split | R0;R2;R11 | conditional_not_parent_derived |
| M1_projector_defined_before_readout | Pi_M is a parent/source-normalization object, not a post-fit orbital readout mask | Pi_M in S_source_norm before scoring | readout-defined GM absorbs new physics | R1;R4;R9;R11 | conditional_no_cheat_contract |
| M2_flux_closure | projected mass current is closed in the compact local branch | d(Pi_M J_H)=0 | M_eff drift or exchange flux | R4;R7;R9;R11 | conditional_flux_calibration_open |
| M3_absolute_orbital_calibration | the surface/integral normalization equals the measured orbital monopole | M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J_H | conserved but misnormalized mass | R1;R4;R9;R10;R11 | not_parent_derived |
| M4_no_boundary_improvement_flux | stress improvements and owned divergences carry no compact boundary monopole | int_partialSigma n_i K_owner^{i0} dS=0 | boundary or improvement source hair | R3;R4;R7;R8;R9;R11 | fail_open |
| M5_no_nonHilbert_current | bulk, domain, memory, range, and connection sectors add no unowned source monopole | q_retained^0=0 or retained with units/bounds | mu_extra survives | R3;R4;R7;R9;R10;R11 | not_parent_derived |
| M6_no_derivative_hair | measured source strength has no time, radial, species, frame, or range derivatives | partial_t mu_obs=partial_r mu_obs=partial_A mu_obs=partial_lambda mu_obs=0 | Gdot, WEP-source charge, radial hair, or fifth force | R1;R4;R9;R10;R11 | not_parent_derived |
| M7_second_order_source_closure | the same measured-GM normalization survives weak-field second order | delta_beta_source=0 | PPN beta source residue | R4;R11 | not_derived |

## 7. Failure Modes

| failure_mode | construction | why_it_blocks_Newton | fallback | affected_rows |
| --- | --- | --- | --- | --- |
| conserved_but_not_calibrated | J_H is conserved but Pi_M and G_ref normalization are not fixed | Newtonian dynamics measures GM, not an arbitrary conserved current | P8_Meff_conservation/source-normalization residual row | R4;R9;R11 |
| surface_improvement_mass_shift | T_H -> T_H + nabla B with nonzero int_boundary B | local conservation survives while the compact monopole shifts | boundary/exchange coefficient vector | R3;R4;R7;R8;R9;R11 |
| source_charge_calibration_split | mu_obs(A)=G_eff M_H[A]+mu_extra[A] | species dependence is physical, not a unit convention | P8_species_source_charge and R1 source channel | R1;R11 |
| range_or_radial_hair_absorbed_into_GM | mu_obs(r,lambda)=G_eff M_H + delta_mu(r,lambda) | finite-range/radial dependence changes force law outside a pure monopole | R10 alpha(lambda) curve or radial source residual | R3;R4;R10;R11 |
| time_drift_hidden_in_Geff | G_eff(t)M_eff or memory flux drift is called measured GM | local Gdot lock is severe and cannot be waived by calibration language | Gdot/G residual row | R9;R11 |
| Poisson_first_order_only | first-order Poisson coefficient matches but beta/source nonlinear residue remains | Newtonian force is not full local GR/PPN completion | P8_nonlinear_beta_source_residue | R4;R11 |

## 8. Hilbert-Monopole Calibration Contract

The Hilbert-source-to-measured-monopole calibration contract has been written to `source-intake\mts_residuals\P8_Hilbert_monopole_calibration_CONTRACT.csv`.

| contract_id | required_identity | mathematical_form | closes_component | affected_rows | current_status | evidence_needed | fallback_if_missing |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HM0_Hilbert_current_input | ordinary matter source is the Hilbert/coframe current from the same observed matter action | J_H derived from T_H^{mu nu}=2/sqrt(-g) delta S_m/delta g_munu | formal source-current input | R1;R4;R11 | conditional_from_449 | one observed coframe and selector-blind matter/source action | source current remains readout/fitted and no Newton claim |
| HM1_parent_defined_mass_projector | mass-flux projector is part of the parent source-normalization structure | Pi_M J_H appears in S_source_norm before readout/scoring | no post-fit GM mask | R1;R4;R9;R11 | conditional_no_cheat_contract | explicit parent source-normalization term and variation | measured GM is calibration-only and not derived |
| HM2_mass_flux_closure | projected Hilbert mass current is closed in the compact local branch | d(Pi_M J_H)=0 | P8_Meff_conservation | R4;R7;R9;R11 | conditional_flux_calibration_open | Euler equation for Pi_M J_H or source-current Ward closure | M_eff drift/source-flux residual row |
| HM3_absolute_monopole_calibration | closed Hilbert mass current has the measured orbital GM normalization | M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J_H | measured-GM normalization | R1;R4;R9;R10;R11 | not_parent_derived | surface/integral calibration theorem tied to orbital GM | conserved current is not measured Newtonian mass |
| HM4_constant_universal_Geff | G_eff/kappa_eff is constant, universal, and not source/species/range/time dependent | G_eff=kappa_eff c^4/(8 pi); partial_{t,r,A,lambda}G_eff=0 | Gdot/source/range coupling drift | R1;R4;R9;R10;R11 | not_parent_derived | constant universal coupling identity | Gdot/source/fifth-force rows remain retained |
| HM5_zero_mu_extra | all non-Hilbert source contributions vanish, are universal constants, or are retained as residual data | mu_extra=mu_boundary+mu_bulk+mu_domain+mu_memory+mu_range+mu_connection=0 or mapped | P8_boundary_bulk_domain_mu_extra; P8_range_dependence; P8_radial_source_hair | R3;R4;R7;R8;R9;R10;R11 | not_parent_derived | K_owner formula, zero boundary flux, no-hair, or executable residual coefficients | P8 residual vector blocks measured-GM/Newton claim |
| HM6_no_derivative_source_hair | measured source strength is time/radial/species/range/frame independent | partial_t mu_obs=partial_r mu_obs=partial_A mu_obs=partial_lambda mu_obs=0 | P8_Geff_time_drift; P8_species_source_charge; P8_range_dependence; P8_frame_calibration_split | R0;R1;R2;R4;R9;R10;R11 | not_parent_derived | constant coupling, source-charge, no-range, and same-frame calibration theorems | activate row-specific residuals and forbid Newton/local-GR pass |
| HM7_second_order_source_stability | first-order measured-GM normalization survives PPN beta order | delta_beta_source=0 | P8_nonlinear_beta_source_residue | R4;R11 | not_derived | second-order weak-field source calculation | Poisson-only bridge cannot be local-GR promotion |
| HM8_empirical_retained_fallback | any nonzero calibration residual is made executable with units, source path, normalization, and row lock | dln_Geff_dt, dln_Meff_dt, eta_source_AB, alpha(lambda), partial_r ln mu_obs, mu_extra/(GM) | none; retained-data branch only | R1;R3;R4;R7;R8;R9;R10;R11 | template_policy_only | numeric residual or derived bound | no measured-GM/Newton/PPN/local-GR claim |

## 9. Gate Tests

| gate | pass_condition | current_result | evidence |
| --- | --- | --- | --- |
| conditional_monopole_theorem_written | Hilbert source plus closure/calibration/zero-residual premises imply measured GM | pass_conditional | calibration chain recorded |
| conservation_not_overclaimed | conserved Hilbert current is not treated as measured orbital monopole | pass | calibration limit and failure modes recorded |
| mass_projector_parent_derived | Pi_M J_H closure and absolute calibration are parent-derived | fail | A7/HM2/HM3 remain conditional/open |
| mu_extra_zero_derived | boundary/bulk/domain/memory/range/connection residual monopole is theorem-zero or retained below locks | fail | HM5 remains not_parent_derived |
| measured_GM_parent_derived | mu_obs=G_eff M_H with all derivatives zero | fail | constant G_eff, flux closure, absolute calibration, and zero hair remain open |
| local_GR_promoted | full R0-R11 vector and EH/PPN source premises are cleared | fail | monopole calibration gate only |

## 10. Theorem Status

| claim | status | evidence |
| --- | --- | --- |
| Hilbert-to-measured-monopole conditional theorem written | pass_conditional | calibration chain shows sufficient conditions for mu_obs=G_eff M_H |
| GM calibration overclaim blocked | pass | conserved current is distinguished from measured orbital monopole |
| Hilbert monopole calibration contract written | pass | source-intake\mts_residuals\P8_Hilbert_monopole_calibration_CONTRACT.csv |
| mass-flux projector parent-derived | fail | Pi_M closure and absolute calibration are not derived |
| measured GM parent-derived | fail | P8 residual components remain open |
| Newton/PPN/local-GR promoted | fail | source-normalization and second-order source closure remain retained |

## 11. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| contract_schema_matches | pass | Hilbert monopole calibration contract columns match schema |
| theorem_statement_written | pass | 3 theorem rows |
| calibration_chain_written | pass | 8 calibration chain rows |
| monopole_requirements_written | pass | 8 requirement rows |
| failure_modes_written | pass | 6 failure modes |
| contract_written | pass | source-intake\mts_residuals\P8_Hilbert_monopole_calibration_CONTRACT.csv |
| conservation_not_overclaimed | pass | conserved Hilbert current separated from measured orbital monopole |
| mass_projector_parent_derived | fail | Pi_M closure and absolute calibration remain open |
| absolute_calibration_parent_derived | fail | surface/integral calibration to orbital GM is not parent-derived |
| mu_extra_zero_derived | fail | boundary/bulk/domain/memory/range/connection residual monopoles remain open |
| derivative_hair_zero_derived | fail | time/radial/species/range/frame derivatives remain contract targets |
| second_order_source_stability | fail | delta_beta_source not derived |
| measured_GM_parent_derived | fail | HM2-HM7 not all closed |
| Newtonian_reduction_promoted | fail | measured-GM calibration gate only |
| local_GR_promoted | fail | P8 source-normalization and PPN rows remain retained |
| claim_ceiling_enforced | pass | Hilbert_monopole_calibration_gate_only_no_measured_GM_Newton_PPN_or_local_GR_pass |

## 12. Decision

The Hilbert-source-to-measured-monopole gate is now explicit. The conditional bridge is clean: if the Hilbert current is parent-owned, projected by a closed mass-flux operator, absolutely calibrated to the orbital monopole, multiplied by constant universal G_eff, and stripped of boundary/bulk/domain/memory/range/connection residual monopoles, then measured GM follows and the Poisson source is Newtonian at first order. The current corpus does not derive the mass-flux Euler equation, absolute calibration, zero mu_extra, derivative silence, or second-order beta stability. Therefore the source-current progress is real but measured GM, Newton, PPN, and local GR remain unpromoted.

Practical read: this is another good narrowing. The GR/Newton bridge is structurally clean if the parent action can make `Pi_M J_Hilbert` the measured monopole. But right now that equality is still the missing machine, not a theorem. The next best move is to attack the mass-flux projector Euler/calibration equation directly.

## 13. Next Queue

| rank | target | why_next |
| --- | --- | --- |
| 1 | 451-mass-flux-projector-Euler-calibration-attempt.md | Pi_M J_H closure plus absolute calibration is the central missing equation for measured GM |
| 2 | 452-constant-universal-Geff-kappa-identity-attempt.md | even a closed mass current is not Newtonian if G_eff/kappa drifts or carries source dependence |
| 3 | map HM0-HM8 into the P8 residual evaluator | failed calibration rows should automatically activate R1/R4/R9/R10/R11 source-normalization tests |
