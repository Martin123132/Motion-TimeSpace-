# 460 - Source-Normalized Newton Branch Theorem Stack

Private GR/Newton reduction checkpoint. This is not a public Newtonian-limit, measured-GM, PPN, local-GR, cosmology, EM, or unified-field claim.

## 1. Purpose

Checkpoint 459 mapped the failed Poisson/Gauss conditions into explicit P8/R11 residual rows. This checkpoint assembles the finite theorem stack for a source-normalized Newton branch.

The question is precise:

```text
What exact identities must a parent MTS action satisfy before the branch is allowed to say it derives Newton?
```

The answer is also precise: SN0-SN10 are required for first-order measured-GM Newton. SN11 is required before any local-GR/PPN promotion.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/source_normalized_Newton_branch_theorem_stack.py` |
| Run directory | `runs\20260602-193000-source-normalized-Newton-branch-theorem-stack` |
| Status | `source_normalized_Newton_branch_theorem_stack_written_conditional_theorem_only_PG_residual_bindings_visible_no_measured_GM_Newton_PPN_or_local_GR_pass` |
| Claim ceiling | `conditional_Newton_theorem_stack_only_no_measured_GM_Newton_PPN_or_local_GR_pass` |
| Stack CSV | `source-intake\mts_residuals\P8_source_normalized_Newton_branch_STACK.csv` |
| Next target | `461-PG-residual-input-derive-or-fill-gate.md` |

## 3. Source Register

| source_file | exists | role |
| --- | --- | --- |
| 424-same-frame-EH-source-Poisson-reduction-gate.md | True | same-frame EH/source-to-Poisson reduction gate |
| 425-EH-operator-retained-ledger-and-source-normalization-test-plan.md | True | EH/operator residual ledger and source-normalization transition rules |
| 438-R11-nonEH-coefficient-vector-contract.md | True | non-EH operator vector contract required if EH-only is not derived |
| 439-EH-only-exterior-parent-premise-ladder.md | True | EH-only local exterior parent-premise ladder |
| 440-metric-only-second-order-sector-reduction-attempt.md | True | second-order metric/PPN sector reduction attempt |
| 450-Hilbert-source-to-measured-monopole-calibration-gate.md | True | Hilbert source to measured monopole calibration gate |
| 451-mass-flux-projector-Euler-calibration-attempt.md | True | mass-flux projector and Euler closure attempt |
| 452-constant-universal-Geff-kappa-identity-attempt.md | True | constant universal Geff/kappa identity attempt |
| 453-global-coupling-superselection-parent-action-contract.md | True | global coupling superselection parent-action contract |
| 455-PiM-flux-closure-Ward-or-topological-current-attempt.md | True | Pi_M flux closure Ward/topological current attempt |
| 457-mass-current-Hamiltonian-boundary-charge-attempt.md | True | Hamiltonian boundary charge route to mass current |
| 458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md | True | PG0-PG10 Hamiltonian charge to Poisson/Gauss calibration gate |
| 459-PG-calibration-residual-mapper.md | True | PG failures mapped into explicit P8/R11 residual components |
| source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv | True | machine-readable PG0-PG10 calibration contract |
| source-intake/mts_residuals/P8_PG_calibration_residual_MAP.csv | True | machine-readable PG-to-residual map |
| source-intake/mts_residuals/P8_PG_calibration_residual_INPUT_TEMPLATE.csv | True | fillable residual input template for failed PG rows |
| runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv | True | canonical local R0-R11 residual components |
| runs/20260602-181500-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate/results/Poisson_Gauss_calibration_contract.csv | True | run artifact for PG0-PG10 rows |
| runs/20260602-191500-PG-calibration-residual-mapper/results/PG_to_residual_map.csv | True | run artifact for PG-to-residual bindings |
| runs/20260602-191500-PG-calibration-residual-mapper/results/PG_residual_input_template.csv | True | run artifact for fillable PG residual rows |

## 4. Conditional Theorem Statement

| claim | statement | math_form | current_status |
| --- | --- | --- | --- |
| conditional_source_normalized_Newton_theorem | If SN0-SN10 are parent-derived theorem-zero identities, or are filled by valid residual evidence with zero effective residue, the local weak-field branch reduces to the Newtonian measured-GM force law. | nabla^2 Phi = 4 pi G0 rho_H; surface_integral grad Phi dot dS = 4 pi G0 M_H; a = -grad Phi = -G0 M_H rhat/r^2; mu_obs = G0 M_H | theorem_stack_written_conditionally_not_satisfied |
| residualized_failure_theorem | If any SN rung fails, the failed premise must appear as a P8/R11 residual component rather than being absorbed into GM by prose. | mu_obs = G_eff M_eff + mu_extra; d ln mu_obs = d ln G_eff + d ln M_eff + d[mu_extra/(G_eff M_eff)] | mapper_available_but_inputs_unfilled |
| Newton_not_local_GR | A first-order Poisson/Gauss success would still not promote local GR unless SN11 also kills the second-order beta/gamma/source/operator residues. | gamma - 1 = 0 and delta_beta_source = 0 after measured-GM normalization | not_derived |
| current_corpus_status | The current corpus has the finite theorem target and residual bindings, but not parent-derived measured GM, not a Newton pass, and not local GR. | exists stack; not exists filled theorem-zero or numeric residual certificate for all required rungs | no_promotion |

## 5. Newton Stack

The stack CSV has been written to `source-intake\mts_residuals\P8_source_normalized_Newton_branch_STACK.csv`.

| rung_id | required_identity | math_form | theorem_use | depends_on | residual_if_failed | current_status | valid_for_Newton_claim | valid_for_local_GR_claim | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SN0_same_observed_frame | matter, clocks, rods, photons, and metric-source variation use one observed coframe/frame | e_obs = e_matter = e_source; delta_frame_source = 0 | lets orbital acceleration read the same Phi sourced by the weak-field equation | 424;459-PG2;459-PG8 | delta_frame_source;eta_WEP_direct_geometry;alpha_clock_redshift;c_nonEH_operator_vector | conditional_not_parent_derived | false | false | derive same-frame source variation or fill frame residual input |
| SN1_EH_or_R11_operator_zero | local exterior operator is EH-only, or every non-EH R11 coefficient is theorem-zero or scored | E_munu = G_munu + Lambda g_munu + sum_i c_i O_i; require c_i O_i -> 0 in local branch | allows the 00 weak-field equation to reduce to a Poisson operator | 425;438;439;459-PG0;459-PG3;459-PG9 | c_nonEH_operator_vector;gamma_minus_1;delta_beta_source;alpha(lambda) | conditional_EH_only_not_parent_derived_R11_vector_unfilled | false | false | derive EH-only exterior from parent action or fill executable R11 vector |
| SN2_observed_time_Hamiltonian_charge | the boundary charge is well-defined, conserved, and generated by observed time | H_xi = B_xi on shell with xi normalized in the observed frame | gives a candidate source charge before attempting measured-GM identification | 457;458-PG0;459-PG0 | c_nonEH_operator_vector;dln_Meff_dt;delta_frame_source | conditional_from_457_not_parent_derived | false | false | prove observed-time Hamiltonian charge or keep charge/reference residuals |
| SN3_charge_equals_Hilbert_mass_current | Hamiltonian boundary charge equals the projected Hilbert mass current | B_xi/G_eff = M_eff[Pi_M J_H] and delta B_xi = delta integral_S Pi_M J_H | turns a conserved geometric charge into the source mass that appears in Newton's law | 450;457;458-PG1;459-PG1 | dln_Meff_dt;mu_extra_boundary_bulk_domain;c_nonEH_operator_vector;eta_source_AB | not_parent_derived | false | false | derive charge-current equality or fill measured-source residual rows |
| SN4_closed_Meff_flux | projected mass flux is closed and conserved in the compact local exterior | d(Pi_M J_H) = 0; partial_t M_eff = 0; partial_r M_eff = 0 outside compact support | prevents hidden time drift, radial hair, and boundary flux from entering measured GM | 451;455;458-PG4;459-PG4;459-PG8 | dln_Meff_dt;partial_r_ln_mu_obs;mu_extra_boundary_bulk_domain;alpha3 | not_parent_derived | false | false | derive closed Pi_M flux or fill mass drift/radial hair residuals |
| SN5_EH_to_Poisson_coefficient | same-frame weak-field EH 00 equation has the standard source coefficient | g_00 = -1 + 2 Phi/c^2; T_00 = rho_H c^2; nabla^2 Phi = (kappa_eff c^4/2) rho_H = 4 pi G_eff rho_H | sets the curvature-to-Newton coupling normalization | 424;452;458-PG3;459-PG3;459-PG7 | c_nonEH_operator_vector;mu_extra_boundary_bulk_domain;alpha(lambda);dln_Geff_dt | conditional_formula_inside_EH_source_stack_only | false | false | tie kappa_eff to one constant G_eff after source purity is proved |
| SN6_zero_mu_extra_and_source_residuals | boundary, bulk, domain, memory, projector, range, and connection pieces add no unowned monopole | mu_obs = G_eff M_eff + mu_extra with mu_extra = 0 and S_res = 0 | stops extra source terms from masquerading as measured mass | 438;450;458-PG6;459-PG6 | mu_extra_boundary_bulk_domain;partial_r_ln_mu_obs;alpha(lambda);c_nonEH_operator_vector | not_parent_derived | false | false | derive Ward/no-hair/topological zero route or fill mu_extra map |
| SN7_constant_universal_Geff | G_eff/kappa_eff is constant, universal, source-blind, range-blind, and frame-blind | partial_t,r,A,lambda,frame G_eff = 0 | allows one calibrated G0 instead of hidden Gdot, fifth-force, source-charge, or frame dependence | 452;453;458-PG7;459-PG7 | dln_Geff_dt;eta_source_AB;alpha(lambda);c_nonEH_operator_vector | conditional_not_parent_derived | false | false | derive global coupling superselection or fill derivative/source/range residuals |
| SN8_Gauss_surface_integral | Poisson source integrates to the same enclosed source mass with no residual volume or boundary terms | surface_integral grad Phi dot dS = 4 pi G_eff M_eff | connects local source density to the monopole measured outside the source | 450;451;458-PG4;459-PG4 | partial_r_ln_mu_obs;mu_extra_boundary_bulk_domain;dln_Meff_dt | not_parent_derived | false | false | prove Gauss equality for Pi_M source or fill radial/boundary residual envelope |
| SN9_orbital_inverse_square_readout | slow test bodies read the Gauss monopole as a pure inverse-square acceleration in the observed frame | a_r = -partial_r Phi = -G_eff M_eff/r^2 and v^2 r = G_eff M_eff | turns the source-normalized Poisson branch into measured Kepler/Newton GM | 424;458-PG5;459-PG5 | alpha(lambda);partial_r_ln_mu_obs;eta_source_AB;delta_frame_source | not_parent_derived | false | false | derive slow-particle geodesic readout plus zero range/source/frame terms |
| SN10_no_derivative_hair | measured source strength has no time, radial, species, range, frame, or domain derivative | partial_t mu_obs = partial_r mu_obs = partial_A mu_obs = partial_lambda mu_obs = partial_frame mu_obs = 0 | prevents a fitted constant GM from hiding real local residual physics | 452;459-PG8 | dln_Geff_dt;dln_Meff_dt;eta_source_AB;alpha(lambda);partial_r_ln_mu_obs;delta_frame_source | not_parent_derived | false | false | derive derivative-zero identities or fill row-specific residual values |
| SN11_second_order_PPN_source_stability | first-order source calibration survives beta/gamma/PPN order in the same observed frame | gamma - 1 = 0 and delta_beta_source = 0 after measured-GM normalization | required for local GR; not enough to have only first-order Newton | 440;458-PG9;459-PG9 | delta_beta_source;gamma_minus_1;c_nonEH_operator_vector | not_derived | not_required_for_first_order_Newton_but_required_for_GR_promotion | false | perform second-order weak-field source/operator calculation |

## 6. Proof Chain

| step | move | mathematical_content | requires | failure_mode |
| --- | --- | --- | --- | --- |
| 1 | Choose the observed local frame | all matter readouts and the source variation use e_obs | SN0 | frame split residual |
| 2 | Linearize the retained local operator | EH-only gives the Poisson operator; non-EH terms become R11 coefficients | SN1 | operator vector residual |
| 3 | Insert the nonrelativistic Hilbert source | T_00 = rho_H c^2 and G_eff = kappa_eff c^4/(8 pi) | SN3;SN5;SN7 | source-normalization or G_eff residual |
| 4 | Identify the Hamiltonian charge with the source mass | B_xi/G_eff = M_eff[Pi_M J_H] | SN2;SN3;SN4 | charge-current split or M_eff drift |
| 5 | Kill extra monopole pieces | mu_extra = 0 and source_residuals = 0 | SN6;SN10 | boundary/bulk/domain/range/source hair |
| 6 | Integrate Poisson over a sphere | surface_integral grad Phi dot dS = 4 pi G_eff M_eff | SN8 | Gauss surface residual |
| 7 | Read the slow-particle acceleration | a = -grad Phi = -G_eff M_eff rhat/r^2 | SN9 | range/source/frame readout residual |
| 8 | Decide whether local GR is also claimed | gamma - 1 = 0 and delta_beta_source = 0 | SN11 | Newton-only or no-promotion branch |

## 7. PG Residual Bindings

| pg_id | stack_rungs | residual_symbol | affected_rows | current_status | valid_for_claim | why_it_blocks_Newton_or_GR |
| --- | --- | --- | --- | --- | --- | --- |
| PG0_Hamiltonian_charge_input | SN1;SN2 | c_nonEH_operator_vector;dln_Meff_dt;delta_frame_source | R2;R4;R5;R6;R8;R9;R11 | retained_missing_parent_charge | false | without a real observed-time charge, no source mass can be calibrated |
| PG1_charge_equals_projected_Hilbert_source | SN3;SN4;SN6 | dln_Meff_dt;mu_extra_boundary_bulk_domain;c_nonEH_operator_vector | R1;R4;R9;R10;R11 | retained_charge_current_split | false | a conserved geometric charge is not yet the Newton source |
| PG2_same_frame_weak_field_potential | SN0;SN5;SN9 | delta_frame_source;eta_WEP_direct_geometry;alpha_clock_redshift;c_nonEH_operator_vector | R0;R1;R2;R11 | retained_frame_split | false | the orbiting body may not read the same potential sourced by the equation |
| PG3_EH_to_Poisson_coefficient | SN1;SN5;SN6 | c_nonEH_operator_vector;mu_extra_boundary_bulk_domain;alpha(lambda) | R3;R4;R8;R10;R11 | retained_operator_source_residual | false | operator/source residues change the Poisson coefficient |
| PG4_Gauss_surface_integral | SN4;SN8;SN10 | partial_r_ln_mu_obs;mu_extra_boundary_bulk_domain;dln_Meff_dt | R3;R4;R7;R8;R9;R10;R11 | retained_Gauss_surface_residual | false | the enclosed mass may include unowned boundary or volume hair |
| PG5_orbital_inverse_square_readout | SN0;SN9;SN10 | alpha(lambda);partial_r_ln_mu_obs;eta_source_AB;delta_frame_source | R1;R2;R4;R10;R11 | retained_orbital_readout_residual | false | the observed acceleration can contain non-inverse-square or source-dependent terms |
| PG6_zero_mu_extra_and_source_residuals | SN1;SN6;SN8;SN10 | mu_extra_boundary_bulk_domain;partial_r_ln_mu_obs;alpha(lambda);c_nonEH_operator_vector | R3;R4;R7;R8;R9;R10;R11 | retained_mu_extra_source_residual | false | extra source terms are physical unless theorem-zero or scored |
| PG7_constant_universal_Geff | SN5;SN7;SN10 | dln_Geff_dt;eta_source_AB;alpha(lambda);c_nonEH_operator_vector | R1;R4;R9;R10;R11 | retained_Geff_derivative_residual | false | a nonconstant or nonuniversal G_eff cannot be hidden inside one measured GM |
| PG8_no_derivative_hair | SN0;SN4;SN7;SN10 | dln_Geff_dt;dln_Meff_dt;eta_source_AB;alpha(lambda);partial_r_ln_mu_obs;delta_frame_source | R0;R1;R2;R4;R8;R9;R10;R11 | retained_derivative_hair_vector | false | time, radial, species, range, or frame derivatives are observable residuals |
| PG9_second_order_source_stability | SN1;SN11 | delta_beta_source;gamma_minus_1;c_nonEH_operator_vector | R3;R4;R11 | retained_second_order_source_residual | false | first-order Poisson cannot be promoted to local GR without beta/gamma stability |
| PG10_retained_residual_fallback | SN0-SN11 | dln_Geff_dt;dln_Meff_dt;eta_source_AB;alpha(lambda);partial_r_ln_mu_obs;mu_extra/(GM);delta_beta_source;c_nonEH_operator_vector | R1;R3;R4;R7;R8;R9;R10;R11 | template_policy_only | false | unfilled residual rows mean no theorem credit |

## 8. Current Blocker Ranking

| rank | blocker | dominant_stack_rungs | dominant_pg_rows | why_it_matters | best_next_action |
| --- | --- | --- | --- | --- | --- |
| 1 | charge-current equality | SN2;SN3;SN4 | PG0;PG1;PG4 | without this, Hamiltonian charge is not measured source mass | derive B_xi/G_eff = M_eff[Pi_M J_H] or fill dln_Meff_dt/mu_extra residuals |
| 2 | zero mu_extra and derivative hair | SN6;SN10 | PG6;PG8 | hidden boundary, radial, range, species, or time terms invalidate constant GM absorption | derive theorem-zero for mu_extra and derivative rows or put numbers into the PG input template |
| 3 | EH-only or complete R11 operator vector | SN1;SN5 | PG3;PG9 | the Poisson coefficient and beta/gamma order depend on operator purity | derive EH-only exterior or fill c_nonEH_operator_vector |
| 4 | constant universal Geff | SN7;SN10 | PG7;PG8 | one Newton constant is legal only after time/range/species/frame derivatives vanish | derive global coupling superselection or score Gdot/source/fifth-force residuals |
| 5 | second-order PPN source stability | SN11 | PG9 | Newton first order is not local GR unless beta/gamma/source normalization survive | perform second-order weak-field source/operator calculation after first-order rows are filled |

## 9. What Would Count as a Newton Pass

To promote the first-order Newton branch, the corpus needs one of these for every SN0-SN10 rung:

```text
parent-derived identity,
derived-zero residual theorem,
or valid numeric/source residual evidence with the effective row below its lock.
```

The current corpus does not have that certificate. The branch is therefore a theorem target and residual map, not a Newton claim.

## 10. What Would Count as a Local-GR Pass

Local GR needs the Newton certificate plus SN11:

```text
gamma - 1 = 0,
delta_beta_source = 0,
and c_nonEH_operator_vector = 0
```

after measured-GM normalization in the same observed frame. A Poisson/Gauss success alone would be first order only.

## 11. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | missing source paths = 0 |
| stack_csv_written | pass | source-intake\mts_residuals\P8_source_normalized_Newton_branch_STACK.csv |
| Newton_stack_rungs | pass | 12 rungs written; SN0-SN11 expected |
| PG_bindings_cover_PG0_to_PG10 | pass | 11 PG residual bindings written |
| conditional_theorem_written | pass | source-normalized Newton theorem statement written as conditional theorem |
| all_current_claim_flags_blocked | pass | no stack rung grants current Newton or local-GR claim credit |
| residual_fallback_visible | pass | failed rungs bind to P8/R11 PG residual components |
| measured_GM_parent_derived | fail | SN3/SN4/SN6/SN8/SN10 remain not parent-derived |
| Newtonian_reduction_promoted | fail | conditional theorem stack only; no theorem-zero or filled residual certificate |
| local_GR_claim_allowed | fail | SN11 second-order PPN source stability not derived |
| claim_ceiling_enforced | pass | conditional_Newton_theorem_stack_only_no_measured_GM_Newton_PPN_or_local_GR_pass |

## 12. Theorem Status

| claim | status | evidence |
| --- | --- | --- |
| finite Newton branch theorem target | pass | SN0-SN11 theorem stack written |
| PG failure rows bound to residuals | pass | PG0-PG10 mapped into stack rungs and P8/R11 residual symbols |
| measured GM parent-derived | fail | charge-current equality, Gauss calibration, mu_extra=0, derivative hair, and constant Geff remain open |
| Newtonian limit promoted | fail | no current rung has valid theorem credit for the full branch |
| local GR/PPN promoted | fail | SN11 beta/gamma/source stability remains not derived |

## 13. Decision

The Newton branch is now in the right mathematical shape: not a vibe, not a loose analogy, and not a hidden calibration trick. It is a finite stack. If SN0-SN10 are derived or residual-scored to zero, MTS gets a legal first-order Newton reduction:

```text
nabla^2 Phi = 4 pi G0 rho_H
surface_integral grad Phi dot dS = 4 pi G0 M_H
a = -grad Phi = -G0 M_H rhat/r^2
mu_obs = G0 M_H
```

But the current state is not there yet. The hardest blockers are charge-current equality, zero `mu_extra`, derivative-hair silence, constant universal `G_eff`, and second-order PPN source stability.

Practical read: this is actually good news, because the route is no longer mushy. We know exactly what has to be proved, and exactly what row gets punched if it is not proved. Right now the branch is conditional theorem architecture, not a pass. The next useful move is to attack the PG residual input rows directly: derive them, fill them, or keep them as no-claim residuals.

## 14. Next Queue

| rank | target | why_next |
| --- | --- | --- |
| 1 | 461-PG-residual-input-derive-or-fill-gate.md | the theorem stack is only useful once the active PG residual inputs are either derived-zero or filled with real residual evidence |
| 2 | second-order PPN source stability attempt | SN11 is the required bridge from Newton/Poisson to local GR |
| 3 | EH-only parent action or R11 coefficient vector | operator purity controls both Poisson coefficient and PPN promotion |
