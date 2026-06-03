# 446 - Source-Owner Current Parent-Action Contract

Private parent-action/source-ownership checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, R10/R11, measured-GM, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 445 proved only a conditional Ward source-ownership theorem. This checkpoint writes the exact parent-action structures and variation identities needed to turn that conditional theorem into a real derivation of `K_owner` and `q_retained=0`.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/source_owner_current_parent_action_contract.py` |
| Run directory | `runs/20260602-150000-source-owner-current-parent-action-contract` |
| Status | `source_owner_current_parent_action_contract_written_exact_terms_needed_K_owner_not_parent_derived_q_retained_not_zero_no_measured_GM_Newton_or_local_GR_pass` |
| Claim ceiling | `source_owner_parent_action_contract_only_no_K_owner_measured_GM_Newton_PPN_or_local_GR_pass` |
| Action contract | `source-intake\mts_residuals\P8_source_owner_parent_action_terms_CONTRACT.csv` |
| q-retained zero contract | `source-intake\mts_residuals\P8_q_retained_zero_conditions_CONTRACT.csv` |
| Next target | `447-no-species-source-charge-one-coframe-theorem-attempt.md` |

## 3. Source Register

| source_file | exists | role |
| --- | --- | --- |
| 382-parent-local-action-minimal-contract.md | True | minimal parent action blocks and required Ward/source variation identities |
| 402-EH-source-normalization-parent-pair.md | True | EH/source weak-field chain and measured-GM obstruction |
| 403-boundary-domain-flux-nohair-numeric-contract.md | True | boundary/domain/flux no-hair numeric locks |
| 425-EH-operator-retained-ledger-and-source-normalization-test-plan.md | True | source-normalization test plan and no symbolic pass policy |
| 436-auxiliary-projector-local-Euler-equation-ledger.md | True | hidden-variable Euler ledger including A7 mass-flux projector |
| 444-source-normalization-residual-vector-refinement.md | True | P8 source residual components |
| 445-measured-GM-Ward-source-ownership-theorem-attempt.md | True | conditional Ward source-ownership theorem and owner contract |
| runs/20260602-044500-boundary-domain-flux-nohair-numeric-contract/results/family_rollup.csv | True | flux/source/drift family lock rollup |
| runs/20260602-073500-boundary-exchange-coefficient-retained-evaluator/results/retained_coefficients.csv | True | retained boundary/exchange coefficient map |
| runs/20260602-123000-auxiliary-projector-local-Euler-equation-ledger/results/Euler_ledger_rows.csv | True | Euler ledger row A7 and hidden-variable zero conditions |
| runs/20260602-143000-source-normalization-residual-vector-refinement/results/P8_source_residual_template_rows.csv | True | P8 residual rows activated if source ownership fails |
| runs/20260602-144500-measured-GM-Ward-source-ownership-theorem-attempt/results/owner_identity_contract.csv | True | C0-C7 Ward source-owner identity contract |
| runs/20260602-144500-measured-GM-Ward-source-ownership-theorem-attempt/results/residual_current_ledger.csv | True | residual source/exchange current ledger |
| source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv | True | checkpoint 445 source-owner contract |
| source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv | True | P8 residual vector fallback |
| source-intake/mts_residuals/R11_P8_source_normalization_rows_TEMPLATE.csv | True | P8 R11 source-normalization fallback |

## 4. Parent-Action Problem

| item | statement | mathematical_form | current_status |
| --- | --- | --- | --- |
| target | write the exact parent-action structures that would make K_owner and q_retained=0 derivable rather than assumed | S_parent must vary to q_res^nu=nabla_mu K_owner^{mu nu} and q_retained^nu=0 or retained mapped | contract_needed_not_solution |
| non_cheat_rule | a multiplier that simply sets every dangerous residual to zero is not a derivation unless the constraint is fixed by parent symmetry, topology, gauge, or an already-defined physical conservation law | lambda_nu q_retained^nu is closure-only unless q_retained=0 is a parent configuration constraint | enforced_by_this_checkpoint |
| legal_success | every exchange/source channel is either absent, gauge/topological, exact-owned with zero boundary flux, positive source-free no-haired, or explicitly retained as residual data | q_res^nu=nabla_mu K_owner^{mu nu}; int_boundary K_owner=0; q_retained^nu=0 or vector_row | not_parent_derived |
| legal_failure | if any action block lacks the variation identity, the linked P8 residual row remains active | P8_source_owner_parent_action_terms_CONTRACT.csv plus P8_q_retained_zero_conditions_CONTRACT.csv | contracts_written_by_this_checkpoint |

## 5. Required Parent-Action Blocks

The parent-action source-owner term contract has been written to `source-intake\mts_residuals\P8_source_owner_parent_action_terms_CONTRACT.csv`.

| term_id | parent_block | required_action_structure | variation_target | euler_identity_required | produces_or_kills | affected_contracts | affected_rows | current_status | fallback_if_missing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0_total_covariant_parent | S_core + S_matter + S_source_norm + S_X + S_projector + S_boundary + S_domain + S_memory | single diffeomorphic parent action; all local fields varied before readout/scoring | g/e and every Z_I | nabla_mu T_tot^{mu nu}=0 on shell with no unvaried hidden force channel | legal basis for Ward accounting, not separate measured-GM conservation | C0_on_shell_total_Ward | R0-R11 | structural_available_not_sufficient | reject branch or retain all affected residual rows |
| A1_source_owner_decomposition | S_owner_current | parent-derived Noether/source current decomposition, not a fitted readout split | K_owner^{mu nu}, q_res^nu, q_retained^nu, or equivalent current variables | q_res^nu = nabla_mu K_owner^{mu nu} + q_retained^nu | defines the exact owner current and exposes retained leakage | C1_exact_owner_decomposition | R4;R7;R9;R11 | not_parent_derived | P8_boundary_bulk_domain_mu_extra and R11 source rows remain active |
| A2_no_retained_source_constraint | S_owner_current or parent configuration space | q_retained is absent by symmetry/topology/gauge, or has a source-free positive operator forcing zero | q_retained^nu | q_retained^nu=0 from legal zero route, not by ad hoc multiplier | kills unowned residual source current | C1_exact_owner_decomposition;C2_zero_owner_flux | R4;R7;R9;R11 | not_parent_derived | retain q_retained vector with alpha3/Gdot/source locks |
| A3_boundary_class_topological | S_boundary[g/e\|partialD, class data] | class-only/topological boundary action with no B_TF, B_0i, radial hair, or local flux | boundary variables and induced boundary data | int_partialSigma n_i K_owner^{i0} dS=0 and no shear/vector/radial boundary source | kills boundary contribution to mu_extra and alpha3/Gdot leakage | C2_zero_owner_flux;C6_no_range_or_radial_source_hair | R3;R4;R7;R8;R9;R11 | conditional_noangular_radial_flux_open | boundary/exchange coefficient vector |
| A4_mass_flux_projector | S_source_norm[kappa,G_eff,M_eff,Pi_M J] | closed calibrated mass-flux projector, defined before fitting/readout | Pi_M J, M_eff, source-normalization multipliers | d(Pi_M J)=0 and M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J | gives the measured source monopole and kills M_eff drift/radial leakage | C3_closed_calibrated_mass_current | R1;R4;R9;R10;R11 | conditional_flux_calibration_open | P8_Meff_conservation and P8_radial_source_hair remain active |
| A5_constant_universal_coupling | S_source_norm[kappa,G_eff] | G_eff/kappa_eff is a global constant, parent-selected coupling or derived constant local branch | G_eff, kappa_eff, calibration standards | partial_t G_eff=partial_r G_eff=partial_A G_eff=0 | kills Gdot and species/radial coupling drift | C4_constant_universal_coupling | R1;R2;R9;R11 | not_parent_derived | Gdot/source/clock residual rows |
| A6_selector_blind_source_action | S_matter + S_source_norm | no material marker, species spurion, readout mask, torsion/projective source charge, or class label in active gravitational source | species/source labels and matter-source couplings | partial_A mu_obs=0 | kills source-charge WEP component | C5_no_species_or_marker_source_charge | R1;R11 | not_parent_derived | P8_species_source_charge |
| A7_bulk_X_nohair_or_curve | S_X[g/e, X, P, J_eff] | bulk/memory/load fields are source-free positive no-hair in compact exterior, or become executable alpha_X(lambda_X) | X_A | (-Delta + m_X^2)X=0 with m_X^2>0 and regular boundary, or mapped sourced force law | kills or maps finite-range/source hair | C6_no_range_or_radial_source_hair | R1;R3;R4;R9;R10;R11 | operator_and_sources_not_parent_derived | R10 alpha(lambda) curve and P8 range/radial rows |
| A8_projector_domain_topological | S_projector + S_domain | projector/domain selectors are covariant, first-class/topological, or metric-independent with no local stress/flux | P_D, lambda_P, chi_D, n_mu, L_cg | F_P^nu+F_domain^nu=0 or exact-owned zero-flux divergence | kills domain/projector contribution to mu_extra and preferred-frame leakage | C1_exact_owner_decomposition;C2_zero_owner_flux | R5;R6;R7;R8;R9;R10;R11 | retained_symbolic | projector/domain stress residual vector |
| A9_memory_kernel_local_silence | S_memory or nonlocal kernel sector | compact-local memory kernel is silent, screened, or constant universal calibration | memory kernel/history variables | partial_t mu_obs from memory = 0 and no local alpha3/R10 leakage | kills memory Gdot/source drift | C4_constant_universal_coupling;C6_no_range_or_radial_source_hair | R7;R9;R10;R11 | retained | Gdot/alpha3/R10 memory residual map |
| A10_second_order_source_closure | weak-field solution of S_parent through PPN order | same source-normalization identities survive the second-order weak-field expansion | second-order metric/source perturbations | delta_beta_source=0 after measured-GM normalization | kills beta/source nonlinear residue | C7_second_order_source_closure | R4;R11 | not_derived | P8_nonlinear_beta_source_residue |

## 6. Variation Identity Requirements

| variation_id | vary | identity | must_show | status |
| --- | --- | --- | --- | --- |
| V0_metric_diffeomorphism | g/e plus all dynamical sectors | nabla_mu T_tot^{mu nu}=0 on shell | no unvaried readout/mask/projector/source variable is contributing a hidden force | structural_available_not_sufficient |
| V1_owner_current | owner current variables or derive Noether current from existing sectors | q_res^nu=nabla_mu K_owner^{mu nu}+q_retained^nu | K_owner is formula-level, covariant, and not chosen after the residual is known | not_parent_derived |
| V2_retained_current_zero | q_retained or its underlying sector | q_retained^nu=0 | zero follows by absence, gauge/topological identity, first-class constraint, or positive source-free no-hair | not_parent_derived |
| V3_boundary_flux | boundary class variables | int_partialSigma n_i K_owner^{i0} dS=0 | no B_TF, B_0i, radial hair, or exchange flux survives | conditional_noangular_radial_flux_open |
| V4_mass_flux_projector | Pi_M J and M_eff | d(Pi_M J)=0 and calibrated M_eff integral | absolute calibration and no radial/time/species leakage | conditional_flux_calibration_open |
| V5_coupling_constant | G_eff/kappa_eff or prove they are global constants not fields | partial_t G_eff=partial_r G_eff=partial_A G_eff=0 | not a local field absorbing residual physics | not_parent_derived |
| V6_species_blindness | matter/source species labels or prove absent | partial_A mu_obs=0 | no material marker or source charge enters active gravitational source | not_parent_derived |
| V7_range_radial_nohair | bulk/range/radial source sectors | partial_r mu_obs=partial_lambda mu_obs=0 | finite-range field is zero/screened or executable as alpha(lambda) | not_derived_symbolic |
| V8_second_order_source | second-order source and metric perturbations | delta_beta_source=0 | first-order source normalization is stable at PPN beta order | not_derived |

## 7. q-retained Zero Conditions

The legal zero-condition contract has been written to `source-intake\mts_residuals\P8_q_retained_zero_conditions_CONTRACT.csv`.

| condition_id | channel | zero_route | required_parent_evidence | forbidden_shortcut | affected_components | affected_rows | current_status | fallback_if_missing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q0_absent_by_configuration | any residual current | the parent configuration space never contains the residual source channel | field/source variable absent before variation and not recreated by readout | dropping a field after writing it in S_parent | all_P8_components | R0-R11 | not_shown_for_all_channels | retain channel-specific residual row |
| Q1_gauge_or_topological | projector/domain/boundary owner current | first-class gauge or topological identity removes local stress/flux | constraint algebra or topological invariant with zero local variation | calling a chosen domain/projector covariant without varying it | P8_boundary_bulk_domain_mu_extra | R5;R6;R7;R8;R9;R11 | conditional_open | projector/domain/boundary residual vector |
| Q2_exact_owned_zero_flux | boundary/source exchange | residual is exact divergence and compact-boundary flux vanishes | K_owner formula plus boundary no-flux theorem | using Bianchi to erase a nonzero surface integral | P8_boundary_bulk_domain_mu_extra;P8_radial_source_hair | R3;R4;R7;R8;R9;R11 | fail_open | boundary/exchange coefficient vector |
| Q3_positive_source_free_nohair | bulk_X or auxiliary load | positive elliptic/massive source-free equation with regular decay gives zero exterior field | operator sign, source-free exterior, boundary regularity, and no source charge | mass gap without proving q_X=0 | P8_range_dependence;P8_radial_source_hair | R1;R3;R4;R9;R10;R11 | operator_and_sources_not_parent_derived | R10 curve and P8 source residual rows |
| Q4_constant_universal_calibration | constant source monopole | only a constant universal monopole is absorbed into measured GM | partial_{t,r,A,lambda} mu_obs=0 and mu_extra constant/universal | absorbing time/species/range/radial dependence into GM | P8_Geff_time_drift;P8_species_source_charge;P8_range_dependence;P8_radial_source_hair | R1;R4;R9;R10;R11 | not_parent_derived | P8 residual vector |
| Q5_executable_retained_vector | any nonzero q_retained | not a zero route; nonzero channel is retained and scored | coefficient/residual value, units, normalization, source path, and weak-field map | symbolic residual counted as pass | all_nonzero_P8_components | R1;R3;R4;R7;R8;R9;R10;R11 | template_only | no measured-GM/Newton/local-GR claim |

## 8. No-Cheat Action Tests

| test_id | bad_move | legal_if | current_result |
| --- | --- | --- | --- |
| N0_no_ad_hoc_multiplier_zero | add lambda_nu q_retained^nu only to force the desired result | q_retained=0 is a parent symmetry/topological/gauge/configuration constraint already required independently | not_satisfied |
| N1_no_readout_after_variation_backreaction | use P_read/P_active or fitted masks inside S_parent to cancel source residuals | readout variables enter only after variation and cannot backreact | conditional_no_cheat_contract |
| N2_no_Bianchi_monopole_shortcut | claim total conservation makes the measured matter/source monopole constant | observed source current is separately conserved or exchange is exact-owned with zero flux | blocked_by_445 |
| N3_no_constant_GM_absorbing_physics | absorb radial/time/species/range source effects into measured GM | all derivatives partial_{t,r,A,lambda} mu_obs are theorem-zero | not_satisfied |
| N4_no_mass_gap_without_no_charge | use a massive auxiliary as no fifth force while retaining source charge | source charge is zero/screened or alpha(lambda) curve is supplied | not_satisfied |
| N5_no_boundary_class_name_only | call boundary data class-only while retaining radial/shear/vector/flux hair | boundary variation proves no local flux, no B_TF, no B_0i, no radial hair | not_satisfied |

## 9. Residual Activation Map

| failed_action_term | activated_component | activated_rows | runner_action |
| --- | --- | --- | --- |
| A1_source_owner_decomposition | P8_boundary_bulk_domain_mu_extra | R4;R7;R9;R11 | load P8/R11 source residual row or keep no-pass |
| A3_boundary_class_topological | P8_boundary_bulk_domain_mu_extra;P8_radial_source_hair | R3;R4;R7;R8;R9;R11 | score boundary/exchange coefficient vector against alpha3/Gdot/xi/gamma/beta locks |
| A4_mass_flux_projector | P8_Meff_conservation;P8_radial_source_hair | R1;R4;R9;R10;R11 | require source-normalization residuals before Newton claim |
| A5_constant_universal_coupling | P8_Geff_time_drift | R9;R11 | score Gdot/G or no-pass if missing |
| A6_selector_blind_source_action | P8_species_source_charge | R1;R11 | report source-charge WEP composite separately from direct WEP |
| A7_bulk_X_nohair_or_curve | P8_range_dependence;P8_radial_source_hair | R3;R4;R10;R11 | require alpha(lambda) curve or theorem-zero source |
| A10_second_order_source_closure | P8_nonlinear_beta_source_residue | R4;R11 | keep beta source residual active |

## 10. Gate Tests

| gate | pass_condition | current_result | evidence |
| --- | --- | --- | --- |
| parent_action_terms_written | all needed action blocks and variations are explicit | pass | 11 parent action contract terms recorded |
| q_retained_zero_conditions_written | legal zero routes are distinguished from retained-vector fallback | pass | 6 zero-condition rows recorded |
| no_cheat_tests_written | fake multiplier/readout/Bianchi/GM absorption shortcuts are blocked | pass | 6 no-cheat tests recorded |
| K_owner_action_term_derived | current parent action supplies formula-level K_owner from variation/Noether current | fail | contract written, not parent-derived |
| q_retained_zero_parent_derived | all q_retained channels are absent/gauge/topological/no-haired or mapped | fail | multiple channels remain conditional/open/template-only |
| measured_GM_promoted | P8 owner-current contract is satisfied and source residual vector is theorem-zero or evaluated | fail | parent action contract only |

## 11. Theorem Status

| claim | status | evidence |
| --- | --- | --- |
| exact parent-action term contract written | pass | source-intake\mts_residuals\P8_source_owner_parent_action_terms_CONTRACT.csv |
| q_retained legal-zero conditions written | pass | source-intake\mts_residuals\P8_q_retained_zero_conditions_CONTRACT.csv |
| no-cheat action policy enforced | pass | ad hoc multipliers, readout masks, Bianchi shortcuts, and GM absorption shortcuts are blocked |
| K_owner parent-derived | fail | no formula-level owner current from current parent action |
| q_retained zero parent-derived | fail | source, boundary, domain, bulk, memory, and range channels remain open or template-only |
| measured GM/Newton/local-GR promoted | fail | contract only; no P8 proof or residual-data pass |

## 12. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| action_contract_schema_matches | pass | action contract columns match schema |
| zero_conditions_schema_matches | pass | q_retained zero-condition columns match schema |
| problem_statement_written | pass | parent-action source-owner target and non-cheat rule recorded |
| parent_action_blocks_written | pass | 11 action blocks recorded |
| variation_identity_requirements_written | pass | 9 variation identities recorded |
| q_retained_zero_conditions_written | pass | source-intake\mts_residuals\P8_q_retained_zero_conditions_CONTRACT.csv |
| no_cheat_action_tests_written | pass | 6 no-cheat tests recorded |
| residual_activation_map_written | pass | 7 failure-to-row mappings recorded |
| K_owner_parent_derived | fail | contract specifies required action term but does not derive it from corpus |
| q_retained_zero_parent_derived | fail | legal zero routes remain unsatisfied for all channels |
| measured_GM_parent_derived | fail | source-owner contract only |
| Newtonian_reduction_promoted | fail | P8 remains open |
| local_GR_promoted | fail | parent-action contract only; no EH/Newton/PPN/local-GR pass |
| claim_ceiling_enforced | pass | source_owner_parent_action_contract_only_no_K_owner_measured_GM_Newton_PPN_or_local_GR_pass |

## 13. Decision

The source-owner current is now expressed as an exact parent-action contract. To earn measured GM, the parent action must produce a formula-level owner current K_owner, prove q_retained=0 by a legal zero route, close the mass-flux projector, fix G_eff as constant/universal, remove species/range/radial/frame source charges, and keep the result through second-order beta. The current corpus does not derive those terms or variations. Therefore this checkpoint sharpens the path but does not promote K_owner, measured GM, Newton, PPN, or local GR.

Practical read: this is the engineering drawing for the Ward/source win. It does not win the round yet, but it now says exactly what machine has to exist. No magic multiplier, no readout backreaction, no Bianchi shortcut, no hiding range/species/time dependence in `GM`.

## 14. Next Queue

| rank | target | why_next |
| --- | --- | --- |
| 1 | 447-no-species-source-charge-one-coframe-theorem-attempt.md | species/source-charge blindness is the crispest sub-theorem inside the P8 contract |
| 2 | map P8_source_owner_parent_action_terms_CONTRACT.csv into evaluator | contract failures should automatically activate P8 residual rows |
| 3 | derive or demote mass-flux projector d(Pi_M J)=0 | closed calibrated M_eff is the central measured-GM object |
