# 439 - EH-Only Exterior Parent-Premise Ladder

Private EH/local-GR derivation checkpoint. This is not a public Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, cosmology, local-GR, or unified-field claim.

## 1. Purpose

Checkpoints 437 and 438 made the symbolic R10/R11 gates executable. This checkpoint turns the theorem-zero side of R11 into a precise parent-premise ladder. The question is no longer "can we say EH locally?" The question is:

```text
Exactly which parent-derived rungs force the surviving compact local exterior
to be Einstein-Hilbert plus Lambda, and which residual rows stay alive if a rung fails?
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/EH_only_exterior_parent_premise_ladder.py` |
| Run directory | `runs/20260602-131500-EH-only-exterior-parent-premise-ladder` |
| Status | `EH_only_exterior_parent_premise_ladder_written_Lovelock_route_exact_parent_premises_open_no_EH_Newton_PPN_or_local_GR_pass` |
| Claim ceiling | `EH_only_parent_premise_ladder_only_no_EH_Newton_PPN_fifth_force_or_local_GR_pass` |
| Next target | `440-metric-only-second-order-sector-reduction-attempt.md` |

## 3. Source Register

| source_file | exists | role |
| --- | --- | --- |
| 358-local-EH-exterior-operator-from-Ward-closed-action.md | True | original EH sufficiency stack: Ward closure plus no-hair plus metric-only second-order exterior |
| 375-EH-exterior-operator-or-residual-modified-gravity-ledger.md | True | operator-or-residual fork and coefficient-to-observable map |
| 382-parent-local-action-minimal-contract.md | True | minimal parent action blocks and required variation identities |
| 392-EH-operator-selection-under-identity-closure.md | True | same-frame identity does not imply EH; Lovelock-style route retained |
| 396-local-GR-reduction-sufficiency-stack-audit.md | True | local-GR sufficiency stack and promotion gates |
| 402-EH-source-normalization-parent-pair.md | True | same-frame EH/source theorem pair and Newtonian measured-GM obstruction |
| 405-same-frame-EH-source-derived-stack-audit.md | True | G0-G13 local GR/Newton stack partition |
| 424-same-frame-EH-source-Poisson-reduction-gate.md | True | conditional EH-to-Poisson bridge and no-promotion policy |
| 436-auxiliary-projector-local-Euler-equation-ledger.md | True | hidden-variable Euler ledger and retained R11 channels |
| 438-R11-nonEH-coefficient-vector-contract.md | True | R11 executable operator-vector contract and next target |
| runs/20260601-184500-local-EH-exterior-operator-from-Ward-closed-action/results/EH_sufficiency_assumptions.csv | True | machine-readable EH sufficiency assumptions |
| runs/20260601-184500-local-EH-exterior-operator-from-Ward-closed-action/results/operator_basis_audit.csv | True | operator basis audit showing conserved non-EH families |
| runs/20260601-235000-EH-exterior-operator-or-residual-modified-gravity-ledger/results/operator_basis_residual_ledger.csv | True | residual operator family ledger |
| runs/20260602-010500-parent-local-action-minimal-contract/results/local_GR_sufficiency_stack.csv | True | parent-action local-GR sufficiency stack |
| runs/20260602-034500-parent-action-contract-v2-after-identity-stack/results/required_variation_identities_v2.csv | True | variation identities required after identity-branch cleanup |
| runs/20260602-050500-same-frame-EH-source-derived-stack-audit/results/gate_results.csv | True | derived-stack audit showing no physics rung parent-derived enough for promotion |
| runs/20260602-130000-R11-nonEH-coefficient-vector-contract/results/operator_families.csv | True | current canonical R11 operator-family vector basis |
| runs/20260602-130000-R11-nonEH-coefficient-vector-contract/results/theorem_zero_routes.csv | True | current R11 theorem-zero route table |

## 4. EH-Only Premise Ladder

| rung | required_parent_statement | mathematical_form | current_status | if_failed |
| --- | --- | --- | --- | --- |
| P0_compact_ordinary_exterior | ordinary local test region has compact matter support and a well-defined exterior domain | rho_matter=0 in E_ext except calibrated conserved monopole/boundary data | definition_plus_source_conditions_open | radial source hair, boundary charge, or fifth-force/source-normalization residuals remain |
| P1_parent_selected_observed_frame | one observed metric/coframe is selected by the parent action for matter, photons, clocks, rods, and the metric core | S_matter=sum_A S_A[Psi_A,e,omega[e],theta_A] with e not a post-readout relabel | closure_branch_not_parent_derived | WEP, clock, nonmetric light, and frame-pullback residuals remain |
| P2_full_Ward_Euler_ownership | all hidden/projector/domain/boundary/source variables are varied and on shell, pure gauge/topological, harmless, or retained | nabla_mu T_total^{mu nu}+sum_A E_A nabla^nu Z_A+F_boundary^nu+F_domain^nu=0 | mapped_not_closed | q_loc, alpha3, Gdot, source, fifth-force, and operator rows remain retained |
| P3_no_extra_local_propagating_fields | scalar, vector, bulk-X, projector/domain, torsion, nonmetricity, and nonlocal kernels are absent, gauge, topological, no-haired, or residualized | Phi_extra={phi,V_mu,X,P_D,chi_D,T,Q,K_nonlocal}=0/gauge/topological in E_ext | not_derived | R11 coefficient vector and induced R3-R10 residuals required |
| P4_metric_compatibility_connection | the local observed connection is Levi-Civita and universally used by matter/light/spin | nabla_mu g_{alpha beta}=0 and T^alpha_{mu nu}=0 in the observed local branch | not_parent_derived | torsion/nonmetricity WEP, clock, spin, and light-cone channels remain |
| P5_local_4D_diffeomorphic_metric_action | the surviving exterior bulk action is local, four-dimensional, diffeomorphism invariant, and built only from the observed metric/coframe | S_ext=int_E d^4x sqrt(-g) L(g,Riemann,nabla Riemann,...) + boundary | structural_target_not_parent_derived | nonlocal/memory, extra-dimensional, fixed-background, or domain operators remain in R11 |
| P6_second_order_metric_equations | the surviving local metric equations are at most second order through local tested scales | E_ext^{mu nu}=E_ext^{mu nu}(g,partial g,partial^2 g), no independent higher-derivative propagating modes | central_blocker_not_derived | R2/f(R), Ricci/Weyl squared, and nonlocal operators remain legal |
| P7_boundary_topological_harmlessness | boundary and class terms are pure boundary/topological or Ward-owned with no local stress, shear, flux, radial hair, or preferred-location leakage | delta S_boundary -> boundary terms only; T_boundary^{mu nu}\|_local=0 or constant universal monopole | conditional_not_derived | gamma, beta, alpha3, xi, Gdot, and boundary/operator coefficients remain retained |
| P8_constant_source_normalization | kappa, G_eff, M_eff, and measured GM are constant, conserved, universal, and range independent | mu_obs=G_eff M_eff, partial_{t,r,A,lambda} mu_obs=0, mu_extra=0 | conditional_not_parent_derived | Newtonian source, beta, WEP-source, Gdot, and fifth-force rows remain |
| P9_weak_field_PPN_completion | the EH/source branch is solved through second post-Newtonian order in the observed matter frame | gamma=1, beta=1, alpha1=alpha2=alpha3=xi=0 plus metric redshift/WEP in same frame | not_promoted | local GR and Newtonian reduction remain unclaimed even if first-order Poisson algebra is clean |

## 5. Parent Variation Tests

| test_id | variation_or_identity | must_show | rungs_controlled | current_status |
| --- | --- | --- | --- | --- |
| V0_metric_variation | delta S_parent/delta g_{mu nu} | E_ext^{mu nu}=a G^{mu nu}+b g^{mu nu} plus only theorem-zero or retained H_i^{mu nu} | P3;P5;P6;P7;P9 | not_satisfied |
| V1_matter_frame_variation | delta S_matter/delta Z_I at fixed observed e | no direct MTS matter vertices, no species spurions, and one observed coframe selected before readout | P1;P4;P9 | closure_only |
| V2_hidden_Euler_equations | E_A=delta S_parent/delta Z_A for all hidden/projector/domain/source variables | E_A=0 locally or Z_A pure gauge/topological/harmless; otherwise residual rows are emitted | P2;P3;P7 | ledger_written_not_closed |
| V3_connection_variation | delta S_parent/delta Gamma or spin connection | Levi-Civita compatibility and zero torsion/nonmetricity in observed branch | P4 | not_parent_derived |
| V4_boundary_variation | delta S_boundary/delta boundary data | boundary terms are topological/class-only/Ward-owned with no local hair | P0;P7 | conditional_open |
| V5_source_normalization_variation | delta S_source_norm/delta{kappa,G_eff,M_eff,Pi_M J} | constant universal measured-GM with mu_extra=0 and no range/time/species leakage | P0;P8;P9 | conditional_open |
| V6_second_order_restriction | parent symmetry/regularity/low-energy theorem forbids higher derivatives as local propagating equations | R2/f(R)/Ricci^2/Weyl^2/nonlocal kernels are zero, topological, decoupled, or coefficient-mapped | P5;P6;R11 | central_open |

## 6. Lovelock Selection Contract

| stage | statement | mathematical_form | status |
| --- | --- | --- | --- |
| 1 | Assume P1-P7 hold in the compact ordinary exterior. | one observed metric, local 4D diffeo invariant metric-only second-order bulk equations | conditional_premises_not_parent_derived |
| 2 | The only local symmetric divergence-free rank-2 metric tensor with up-to-second derivatives in 4D is EH plus Lambda, up to boundary/topological pieces. | E_ext^{mu nu}=a G^{mu nu}+b g^{mu nu} | conditional_theorem_shape |
| 3 | If a is constant and source-normalized, identify kappa_eff=1/a and Lambda_eff=-b/a. | G^{mu nu}+Lambda_eff g^{mu nu}=kappa_eff T^{mu nu} | requires_P8 |
| 4 | If Lambda_eff is negligible on local PPN scales and measured GM is constant/universal, recover Newtonian Poisson and GR PPN baseline. | nabla^2 Phi=4 pi G_measured rho; gamma=beta=1; alpha_i=xi=0 | requires_P8_P9 |
| 5 | If any premise fails, EH is not derived; the failed premise emits retained residuals or R11 coefficient-vector rows. | E_ext^{mu nu}=aG^{mu nu}+bg^{mu nu}+sum_i c_i H_i^{mu nu} | current_branch_policy |

Compact theorem shape:

```text
If the parent action derives P1-P7 in the compact ordinary exterior,
then the surviving local bulk equation has the form

  E_ext^{mu nu} = a G^{mu nu} + b g^{mu nu}.

If P8 also holds, this becomes

  G^{mu nu} + Lambda_eff g^{mu nu} = kappa_eff T^{mu nu}

in the observed matter frame. If P9 is solved, the local Newton/PPN
baseline follows. If any rung fails, the failed rung emits retained
R0-R11 residuals rather than a GR claim.
```

## 7. Dependency Edges

| from | to | edge |
| --- | --- | --- |
| P1_parent_selected_observed_frame | R0/R2/WEP_clock_same_frame | without one frame, local observables are not GR-comparable |
| P2_full_Ward_Euler_ownership | R7/R9/source_flux_rows | unowned hidden Euler terms source q_loc and flux residuals |
| P3_no_extra_local_propagating_fields | R11_operator_vector | extra fields are non-EH operator families unless theorem-zero |
| P4_metric_compatibility_connection | R0/R1/R2/R11 | torsion/nonmetricity affects WEP, clocks, light, spin, and operator ledger |
| P5_local_4D_diffeomorphic_metric_action | Lovelock_selection | EH selection requires local 4D diffeo metric action |
| P6_second_order_metric_equations | R2_fR_Ricci_Weyl_rows | higher derivatives are legal non-EH operators if not forbidden |
| P7_boundary_topological_harmlessness | R3/R4/R7/R8 | boundary hair contaminates gamma, beta, alpha3, and xi |
| P8_constant_source_normalization | Newtonian_measured_GM | EH equation alone is not measured Newtonian gravity |
| P9_weak_field_PPN_completion | local_GR_claim | first-order Poisson is not a full PPN/local-GR reduction |

## 8. Rejected EH Shortcuts

| shortcut | why_rejected | correct_route |
| --- | --- | --- |
| same_frame_matter_implies_EH | a scalar-tensor, f(R), vector, or nonlocal gravity branch can share one matter frame | derive separate EH operator-selection premises P3-P6 |
| Bianchi_or_Ward_conservation_implies_EH | conserved non-EH tensors exist | derive metric-only local 4D second-order exterior or retain c_i H_i^{mu nu} |
| first_order_Poisson_implies_GR | gamma, beta, preferred-frame, source-normalization, and fifth-force rows can still fail | solve weak-field expansion through PPN order in the observed frame |
| set_all_nonEH_coefficients_to_zero | typed zeros are placeholders unless parent-derived or sourced | supply derived_zero sources or a valid R11 coefficient vector |
| boundary_terms_are_harmless_by_name | boundary/class terms can leave radial, shear, flux, and preferred-location hair | prove class-only topological/Ward-owned boundary no-hair |
| EFT_small_means_local_GR | suppressed coefficients may be empirically viable but are not theorem-zero GR reduction | declare units/cutoff, map residuals, and score as retained modified-gravity branch |
| field_redefinition_hides_nonEH_sector | renaming the metric can move residues into source, matter, or operator sectors | show the whole parent action is EH-only in the observed frame |

## 9. Row Implications

| row_id | ladder_dependency | current_transition |
| --- | --- | --- |
| R0_identity_coframe_direct | P1;P4 | closure_control_only_not_parent_derived |
| R1_WEP_source_charge | P1;P4;P8 | source_charge_retained |
| R2_clock_redshift | P1;P4;P8;P9 | same_frame_clock_budget_not_promoted |
| R3_gamma | P3;P5;P6;P7;P9 | EH_operator_slip_retained |
| R4_beta | P3;P6;P7;P8;P9 | source_and_nonlinear_operator_retained |
| R5_alpha1 | P2;P3;P9 | preferred_frame_vector_retained |
| R6_alpha2 | P2;P3;P9 | preferred_frame_vector_retained |
| R7_alpha3 | P2;P7;P9 | Ward_flux_contingent_retained |
| R8_xi | P3;P6;P7;P9 | domain_boundary_location_retained |
| R9_Gdot | P2;P7;P8 | source_memory_drift_retained |
| R10_fifth_force | P0;P3;P7;P8 | R10_curve_or_theorem_zero_required |
| R11_EH_operator_ledger | P3;P4;P5;P6;P7;P8 | R11_vector_or_EH_only_theorem_required |

## 10. Theorem Attempt Status

| claim | status | evidence |
| --- | --- | --- |
| EH-only parent-premise ladder written | pass | 10 rungs P0-P9 with variation tests and dependencies recorded |
| Lovelock-style conditional route identified | pass_conditional | P1-P7 would select EH plus Lambda up to harmless boundary/topological terms |
| same-frame matter parent-selected | fail | identity/coframe row is closure-labelled, not parent-derived |
| all hidden sectors varied and locally on shell/harmless | fail | C1 Euler ledger remains open for projector/domain/boundary/source/nonEH rows |
| metric-only exterior variables derived | fail | scalar, vector, bulk, projector/domain, torsion/nonmetricity, and nonlocal sectors are retained |
| local 4D second-order metric operator derived | fail | R2/f(R), Ricci/Weyl squared, and nonlocal operators are not parent-forbidden |
| source-normalized Newtonian measured-GM derived | fail | kappa/G_eff/M_eff/mu_extra constancy remains conditional |
| PPN/local-GR promoted | fail | R0-R11 still include closure, retained, contingent, unscored, and symbolic rows |

## 11. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| EH_only_premise_ladder_written | pass | P0-P9 parent-premise ladder recorded |
| parent_variation_tests_written | pass | 7 parent variation tests recorded |
| Lovelock_selection_contract_written | pass | 5-stage conditional EH selection route recorded |
| fake_EH_shortcuts_rejected | pass | 7 common false shortcuts explicitly rejected |
| row_implications_written | pass | R0-R11 dependencies mapped to ladder rungs |
| EH_only_parent_derived | fail | central P1-P8 rungs remain closure, conditional, retained, or open |
| R11_theorem_zero_promoted | fail | R11 still requires EH-only theorem-zero or executable coefficient vector |
| Newtonian_reduction_promoted | fail | source-normalized measured-GM remains conditional |
| local_GR_promoted | fail | premise ladder only; no EH/Newton/PPN/fifth-force/local-GR pass |
| claim_ceiling_enforced | pass | EH_only_parent_premise_ladder_only_no_EH_Newton_PPN_fifth_force_or_local_GR_pass |

## 12. Decision

The EH-only exterior route is now an explicit parent-premise ladder. If the parent action derives one observed frame, full Ward/Euler ownership, no extra local propagating fields, Levi-Civita compatibility, a local 4D diffeomorphic metric-only exterior, second-order metric equations, harmless boundary/topological terms, and constant source normalization, then the Lovelock-style route selects EH plus Lambda and the weak-field GR/Newton baseline follows conditionally. The current corpus does not derive those rungs. Therefore this checkpoint sharpens the route but does not promote EH, Newton, PPN, R11, or local GR.

Practical read: this is the GR route with the referee holding the scorecard. If the rungs close, EH follows cleanly. If they do not, MTS is not dead; it is a retained residual/modified-gravity branch that must fight on the measured rows. No shortcut gets to wear the belt.

## 13. Next Queue

| rank | target | why_next |
| --- | --- | --- |
| 1 | 440-metric-only-second-order-sector-reduction-attempt.md | P3 and P6 are the central EH blockers: either reduce all extra sectors to gauge/topological/no-hair, or retain R11 coefficients |
| 2 | filled R11 nonEH operator vector | if P3/P6 cannot be derived, the branch must become an executable modified-gravity coefficient vector |
| 3 | local residual scorer curve/vector mode | R10/R11 templates are now written; scorer should eventually parse real curve/vector files |
