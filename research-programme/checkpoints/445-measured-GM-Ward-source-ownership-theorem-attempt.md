# 445 - Measured-GM Ward Source-Ownership Theorem Attempt

Private Newton/source-ownership theorem checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, R10/R11, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 444 split measured `GM` into exact P8 residual components. This checkpoint attempts the derivation: can Ward/Bianchi ownership force `mu_extra=0` and make measured `GM` constant, or does it only give a conditional theorem with retained source rows?

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/measured_GM_Ward_source_ownership_theorem_attempt.py` |
| Run directory | `runs/20260602-144500-measured-GM-Ward-source-ownership-theorem-attempt` |
| Status | `measured_GM_Ward_source_ownership_theorem_attempt_written_conditional_identity_bianchi_not_enough_mu_extra_not_parent_derived_no_Newton_PPN_or_local_GR_pass` |
| Claim ceiling | `Ward_source_ownership_conditional_theorem_only_no_measured_GM_Newton_PPN_or_local_GR_pass` |
| Owner identity contract | `source-intake\mts_residuals\P8_Ward_source_owner_identity_CONTRACT.csv` |
| Next target | `446-source-owner-current-parent-action-contract.md` |

## 3. Source Register

| source_file | exists | role |
| --- | --- | --- |
| 382-parent-local-action-minimal-contract.md | True | parent-action Ward identity and source-normalized Newtonian limit contract |
| 402-EH-source-normalization-parent-pair.md | True | mu_obs = G_eff M_eff + mu_extra weak-field chain |
| 403-boundary-domain-flux-nohair-numeric-contract.md | True | alpha3/Gdot/source-charge flux locks and Ward-owned flux warning |
| 405-same-frame-EH-source-derived-stack-audit.md | True | Ward flux silence and source-normalized GM listed as open GR stack rungs |
| 419-boundary-exchange-coefficient-retained-evaluator.md | True | boundary/exchange coefficient retained evaluator |
| 425-EH-operator-retained-ledger-and-source-normalization-test-plan.md | True | source-normalization test plan and Ward/Bianchi next move |
| 428-MTS-local-residual-vector-input-contract.md | True | local residual vector and measured-GM requirements |
| 436-auxiliary-projector-local-Euler-equation-ledger.md | True | mass-flux projector and auxiliary/source Euler rows |
| 439-EH-only-exterior-parent-premise-ladder.md | True | P8 constant source-normalization premise |
| 441-extra-sector-nohair-priority-gate.md | True | source-normalization no-hair contract and priority |
| 444-source-normalization-residual-vector-refinement.md | True | P8 residual-vector refinement and next target |
| runs/20260602-044500-boundary-domain-flux-nohair-numeric-contract/results/family_rollup.csv | True | numeric family locks for flux/source/drift rows |
| runs/20260602-044500-boundary-domain-flux-nohair-numeric-contract/results/flux_balance_equations.csv | True | flux balance equations from boundary/domain checkpoint |
| runs/20260602-044500-boundary-domain-flux-nohair-numeric-contract/results/nohair_mechanism_tests.csv | True | boundary/domain/flux no-hair mechanism tests |
| runs/20260602-073500-boundary-exchange-coefficient-retained-evaluator/results/retained_coefficients.csv | True | retained boundary/exchange coefficient rows |
| runs/20260602-123000-auxiliary-projector-local-Euler-equation-ledger/results/Euler_ledger_rows.csv | True | Euler ledger row A7 mass-flux projector source identity |
| runs/20260602-143000-source-normalization-residual-vector-refinement/results/mu_obs_decomposition.csv | True | measured-GM decomposition from checkpoint 444 |
| runs/20260602-143000-source-normalization-residual-vector-refinement/results/P8_source_residual_template_rows.csv | True | P8 residual vector rows from checkpoint 444 |
| runs/20260602-143000-source-normalization-residual-vector-refinement/results/P8_gate_tests.csv | True | P8 source-normalization gate tests |
| source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv | True | P8 source residual template |
| source-intake/mts_residuals/R11_P8_source_normalization_rows_TEMPLATE.csv | True | P8 source-normalization R11 template |

## 4. Ward Theorem Statement

| part | statement | mathematical_form | status |
| --- | --- | --- | --- |
| conditional_theorem | Ward/Bianchi conservation plus explicit source ownership implies measured-GM constancy only if every residual source current is an exact owned divergence with zero boundary flux and no species/range/frame charge. | nabla_mu T_tot^{mu nu}=0; q_res^nu=nabla_mu K_owner^{mu nu}; n_i K_owner^{i0}\|partialSigma=0; partial_{A,lambda,r} q_res^0=0 => partial_{t,A,lambda,r} mu_obs=0 | proved_as_conditional_identity |
| non_theorem_warning | Bianchi conservation alone conserves the total stress-energy; it does not prove the observed matter/source monopole is conserved or equal to measured orbital GM. | nabla_mu(T_obs^{mu nu}+T_hidden^{mu nu})=0 does not imply nabla_mu T_obs^{mu nu}=0 | blocks_parent_promotion |
| P8_success_condition | Measured GM is derived only when G_eff is constant, M_eff is a closed calibrated monopole, and mu_extra integrates to zero with no residual source charge. | mu_obs=G_eff M_eff + mu_extra = GM_measured; partial_{t,r,A,lambda} mu_obs=0; mu_extra=0 | not_parent_derived |

## 5. Conditional Proof Steps

| step | claim | mathematical_step | status | gap |
| --- | --- | --- | --- | --- |
| 1 | Diffeomorphism invariance gives on-shell total conservation. | nabla_mu T_tot^{mu nu}=0 | structural_Ward_identity_available | total conservation does not select the observed measured-GM source. |
| 2 | Split the total source into observed matter/source plus owned residual sectors. | T_tot^{mu nu}=T_obs^{mu nu}+T_owner^{mu nu}+T_unowned^{mu nu} | decomposition_required | the parent action has not proved T_unowned^{mu nu}=0 or pure owned divergence. |
| 3 | Define the measured-GM residual source as the part of the weak-field source not equal to constant G_eff M_eff. | mu_extra = int_Sigma rho_extra d^3x + surface/projector/range/source-charge terms | definition_from_P8_refinement | rho_extra components are templated, not theorem-zero. |
| 4 | If the residual source density is an exact owned divergence, Gauss/Stokes pushes it to the boundary. | rho_extra = partial_i V_owner^i => int_Sigma rho_extra d^3x = int_partialSigma n_i V_owner^i dS | valid_conditional_math | exact-divergence ownership is not derived for boundary, bulk, domain, projector, or memory sectors. |
| 5 | If boundary flux vanishes or is a universal constant calibration, the residual monopole vanishes or is absorbable. | int_partialSigma n_i V_owner^i dS = 0 or constant universal calibration | valid_conditional_math | prior flux rows show alpha3/Gdot/source locks remain open. |
| 6 | If species, frame, radial, and range derivatives of the residual source vanish, measured GM is universal and range independent. | partial_A mu_obs=partial_r mu_obs=partial_lambda mu_obs=0 | valid_conditional_math | no-marker, no-finite-range-charge, and one-frame calibration are not parent-derived. |
| 7 | Then and only then the EH-to-Poisson chain becomes measured Newtonian gravity. | nabla^2 Phi=4 pi G_eff rho_eff with mu_obs=GM_measured | conditional_Newton_route | P8 conditions are open, so no Newton/PPN/local-GR promotion. |

## 6. Why Bianchi Alone Is Not Enough

| temptation | why_false | required_fix | affected_components |
| --- | --- | --- | --- |
| total conservation implies source conservation | hidden sectors can exchange energy-momentum with observed matter while total T remains conserved | derive separate observed-source current conservation or prove exchange is owned and boundary-silent | P8_Meff_conservation;P8_boundary_bulk_domain_mu_extra |
| divergence terms do not affect monopoles | a divergence integrates to a boundary flux, and boundary flux is exactly one of the dangerous retained channels | prove the surface integral vanishes or is a constant universal calibration | P8_boundary_bulk_domain_mu_extra;P8_radial_source_hair |
| constant calibration can absorb all source differences | time, species, radial, and range dependence are observables, not unit choices | prove partial_{t,A,r,lambda} mu_obs=0 before absorbing GM | P8_Geff_time_drift;P8_species_source_charge;P8_range_dependence;P8_radial_source_hair |
| direct WEP row clears source charge | direct geometry WEP is not the full source-normalization composite; hidden source/test charges can survive | derive species/source universality in the parent matter/source action | P8_species_source_charge |
| source-free exterior means no fifth force | finite-range fields can be sourced by the compact body and live in the exterior | derive zero source charge/screening or provide an executable alpha(lambda) curve | P8_range_dependence |
| cosmological memory success implies local memory silence | a cosmological kernel can still produce local Gdot, flux, or source drift unless compact-local silence is derived | derive local kernel silence or map Gdot/alpha3/R10 residuals | P8_Geff_time_drift;P8_boundary_bulk_domain_mu_extra;P8_range_dependence |

## 7. Owner Condition Audit

| condition_id | required_identity | mathematical_form | current_status | fallback |
| --- | --- | --- | --- | --- |
| W0_all_sectors_varied | all parent sectors are varied before any source residual is dropped | delta S_parent/delta Z_I=0 for X, P_D, boundary, domain, Pi_M J, nonmetric/source variables | ledger_available_not_solved | retain affected P8/R11 residual rows |
| W1_total_to_owned_split | Ward identity decomposes every force channel into owned zero/boundary/retained pieces | F_X^nu+F_P^nu+F_boundary^nu+F_domain^nu+F_nonmetric^nu = nabla_mu K_owner^{mu nu}+q_retained^nu | not_parent_derived | q_retained feeds P8_boundary_bulk_domain_mu_extra and R7/R9/R11 |
| W2_zero_boundary_flux | owned divergence has zero flux through the compact local boundary | int_partialSigma n_i K_owner^{i0} dS = 0 | fail_open | retain flux coefficients against alpha3/Gdot locks |
| W3_closed_mass_flux_projector | mass-flux projector gives a closed calibrated source monopole | d(Pi_M J)=0; M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J | conditional_flux_calibration_open | P8_Meff_conservation and P8_radial_source_hair remain active |
| W4_constant_coupling | G_eff/kappa_eff is constant and universal in the observed local branch | partial_t G_eff=partial_r G_eff=partial_A G_eff=0 | not_parent_derived | P8_Geff_time_drift and source-normalization R11 rows |
| W5_species_universality | no material marker, source charge, or species spurion enters the active gravitational source | partial_A mu_obs=0 | not_parent_derived | P8_species_source_charge |
| W6_no_range_or_radial_hair | source strength has no radial/range dependence after monopole extraction | partial_r mu_obs=partial_lambda mu_obs=0 | not_derived_symbolic | P8_range_dependence and P8_radial_source_hair |
| W7_same_frame_source_calibration | matter/source/clocks/metric use the same observed coframe and source calibration | e_source=e_matter=e_metric plus universal standards | conditional_not_parent_derived | P8_frame_calibration_split |
| W8_second_order_source_closure | source normalization remains closed at second post-Newtonian order | delta_beta_source=0 after measured-GM normalization | not_derived | P8_nonlinear_beta_source_residue |

## 8. Residual Current Ledger

| current_or_channel | symbolic_form | owner_success_condition | if_unowned_rows | current_status |
| --- | --- | --- | --- | --- |
| bulk_X_source_exchange | F_X^nu or q_X rho_source | positive source-free no-hair or mapped alpha_X(lambda_X) with source charge zero/below curve | R1;R3;R4;R9;R10;R11 | operator_and_sources_not_parent_derived |
| projector_domain_exchange | F_P^nu + F_domain^nu | projector/domain variables are topological/gauge or their stress is coefficient-mapped | R5;R6;R7;R8;R9;R10;R11 | retained_symbolic |
| boundary_flux | F_boundary^nu or n_i K_owner^{i nu} | class-only boundary with zero local flux/radial/shear/vector hair | R3;R4;R7;R8;R9;R11 | conditional_noangular_radial_flux_open |
| nonmetric_or_connection_source_exchange | F_matter_nonmetric^nu plus torsion/projective source charge | Levi-Civita/same-frame matter connection theorem or explicit P4/P8 rows below bounds | R0;R1;R2;R11 | P4_demoted_to_R11 |
| mass_flux_projector | d(Pi_M J) | closed calibrated source monopole with no radial/time/species leakage | R1;R4;R9;R10;R11 | conditional_flux_calibration_open |
| memory_kernel_drift | partial_t K_memory or local history kernel contribution | compact-local kernel silence or explicit Gdot/alpha3/R10 residual map | R7;R9;R10;R11 | retained |
| species_source_charge | partial_A mu_obs | no material marker/species spurion/source charge in parent source action | R1;R11 | not_parent_derived |
| finite_range_source_charge | partial_lambda mu_obs or alpha(lambda) | no finite-range source charge, exact screening, or executable alpha(lambda) curve below bounds | R10;R11 | not_derived_symbolic |

## 9. Owner Identity Contract

The source-owner contract has been written to `source-intake\mts_residuals\P8_Ward_source_owner_identity_CONTRACT.csv`.

| contract_id | required_identity | mathematical_form | affected_components | affected_rows | current_status | evidence_needed | fallback_if_missing |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C0_on_shell_total_Ward | parent action yields total on-shell Ward conservation after all variables are varied | nabla_mu T_tot^{mu nu}=0 | all_P8_components | R0-R11 | structural_available_not_sufficient | explicit parent variation with every sector included | no source-ownership theorem; retain residual vector |
| C1_exact_owner_decomposition | all residual force/source terms are exact owned divergences plus retained mapped rows | q_res^nu = nabla_mu K_owner^{mu nu} + q_retained^nu | P8_boundary_bulk_domain_mu_extra;P8_Meff_conservation | R4;R7;R9;R11 | not_parent_derived | formula for K_owner and proof q_retained=0 or mapped | retain mu_extra and alpha3/Gdot source residual rows |
| C2_zero_owner_flux | owned divergence has no compact exterior boundary flux | int_partialSigma n_i K_owner^{i0} dS = 0 | P8_boundary_bulk_domain_mu_extra;P8_radial_source_hair | R3;R4;R7;R8;R9;R11 | fail_open | class-only/topological boundary theorem with no radial/shear/vector/flux hair | boundary/exchange coefficient vector |
| C3_closed_calibrated_mass_current | mass-flux projector is closed and absolutely calibrated to the measured source monopole | d(Pi_M J)=0 and M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J | P8_Meff_conservation;P8_radial_source_hair | R1;R4;R9;R10;R11 | conditional_flux_calibration_open | Euler equation for Pi_M J plus calibration proof | source-normalization residual vector |
| C4_constant_universal_coupling | G_eff/kappa_eff carries no time/radius/species/frame dependence | partial_t G_eff=partial_r G_eff=partial_A G_eff=0 | P8_Geff_time_drift;P8_species_source_charge;P8_frame_calibration_split | R1;R2;R9;R11 | not_parent_derived | constant-coupling parent identity or numeric residuals | Gdot/source/clock residual rows |
| C5_no_species_or_marker_source_charge | active source has no material-marker or species spurion | partial_A mu_obs=0 | P8_species_source_charge | R1;R11 | not_parent_derived | selector-blind source action theorem | eta_source residual row |
| C6_no_range_or_radial_source_hair | active source has no radial or finite-range dependence beyond the constant monopole | partial_r mu_obs=partial_lambda mu_obs=0 | P8_range_dependence;P8_radial_source_hair | R3;R4;R10;R11 | not_derived_symbolic | no-hair theorem or executable alpha(lambda)/radial residual | R10 curve and P8 radial source row |
| C7_second_order_source_closure | first-order measured-GM normalization remains valid at beta/PPN order | delta_beta_source=0 | P8_nonlinear_beta_source_residue | R4;R11 | not_derived | second-order weak-field source solution in observed frame | beta source residual row |

## 10. Gate Tests

| gate | pass_condition | current_result | evidence |
| --- | --- | --- | --- |
| conditional_theorem_written | Ward ownership theorem is expressed as exact conditional identity | pass | conditional theorem and proof steps recorded |
| Bianchi_not_overclaimed | total conservation is not used as separate measured-GM conservation | pass | Bianchi insufficiency rows recorded |
| owner_current_derived | parent action supplies K_owner and proves q_retained=0 or mapped | fail | no explicit K_owner formula or q_retained zero proof in current corpus |
| zero_boundary_flux_derived | compact exterior boundary flux integral vanishes or is constant universal calibration | fail | alpha3/Gdot flux families remain not_parent_derived |
| closed_mass_current_derived | d(Pi_M J)=0 and absolute M_eff calibration are parent-derived | fail | A7 mass-flux projector remains conditional_flux_calibration_open |
| species_range_frame_silence_derived | partial_A mu_obs, partial_lambda mu_obs, and frame split vanish by theorem | fail | P8 species, range, and frame residual components remain template rows |
| measured_GM_promoted | partial_{t,r,A,lambda} mu_obs=0 and mu_extra=0 are parent-derived | fail | conditional theorem only; no parent-derived P8 |

## 11. Theorem Attempt Status

| claim | status | evidence |
| --- | --- | --- |
| Ward source-ownership conditional theorem written | pass | proof steps show Ward + exact owner + zero flux + universality implies P8 |
| Bianchi-only shortcut rejected | pass | total conservation does not imply observed source conservation |
| owner identity contract written | pass | source-intake\mts_residuals\P8_Ward_source_owner_identity_CONTRACT.csv |
| K_owner/q_retained parent-derived | fail | no explicit parent variation closes all exchange/source channels |
| mu_extra theorem-zero | fail | boundary, bulk, domain, memory, source-charge, and finite-range rows remain legal |
| measured GM parent-derived | fail | P8 remains conditional, not promoted |
| Newton/PPN/local-GR promoted | fail | theorem attempt only; no source residual data or PPN solution |

## 12. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| owner_contract_schema_matches | pass | owner identity contract columns match schema |
| Ward_theorem_statement_written | pass | conditional theorem statement recorded |
| proof_steps_written | pass | 7 proof steps recorded |
| Bianchi_insufficiency_written | pass | 6 no-cheat insufficiency rows recorded |
| owner_condition_audit_written | pass | 9 source-owner conditions audited |
| residual_current_ledger_written | pass | 8 residual current/source channels recorded |
| owner_identity_contract_written | pass | source-intake\mts_residuals\P8_Ward_source_owner_identity_CONTRACT.csv |
| K_owner_parent_derived | fail | no explicit K_owner/q_retained identity supplied by parent action |
| mu_extra_zero_derived | fail | zero boundary flux and source-current closure are not parent-derived |
| measured_GM_parent_derived | fail | conditional theorem only |
| Newtonian_reduction_promoted | fail | P8 remains open |
| local_GR_promoted | fail | Ward/source checkpoint only; no EH/Newton/PPN/local-GR pass |
| claim_ceiling_enforced | pass | Ward_source_ownership_conditional_theorem_only_no_measured_GM_Newton_PPN_or_local_GR_pass |

## 13. Decision

The measured-GM Ward route has been attempted. It produces a real conditional theorem: if the parent action derives an exact owned residual current, zero compact boundary flux, a closed calibrated mass-flux projector, constant universal G_eff, no species/range/frame source charge, and second-order source closure, then mu_extra=0 and measured GM is constant. The current corpus does not supply the owner current or the zero-flux/source-universality proofs. Therefore Bianchi/Ward conservation is useful but not sufficient; measured GM is not promoted and P8 remains a residual-vector/parent-contract problem.

Practical read: this is a good narrow miss, not a collapse. Ward/Bianchi is the right weapon, but it does not automatically knock out `mu_extra`. It wins only when the parent action shows exactly who owns every exchange current and why the compact boundary carries no source flux. Otherwise the source residual vector stays in the ring.

## 14. Next Queue

| rank | target | why_next |
| --- | --- | --- |
| 1 | 446-source-owner-current-parent-action-contract.md | write the exact parent-action terms/variations needed to produce K_owner and q_retained=0 |
| 2 | map P8_Ward_source_owner_identity_CONTRACT.csv into P8 residual-vector evaluator | if the theorem remains open, the evaluator needs to see which contract failures activate which residual rows |
| 3 | derive no-species/source-charge theorem from one-coframe matter action | species universality is the cleanest sub-gate inside P8 after owner-current closure |
