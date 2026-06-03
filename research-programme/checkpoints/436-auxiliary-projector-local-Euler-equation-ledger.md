# 436 - Auxiliary/Projector Local Euler-Equation Ledger

Private C1/local-Ward derivation checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 435 routed every exterior extra source. This checkpoint attacks the highest-ranked theorem route from checkpoint 430: C1, the requirement that every hidden auxiliary/projector/domain variable has a parent Euler equation and is either on shell locally or retained as a force.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/auxiliary_projector_local_Euler_equation_ledger.py` |
| Run directory | `runs/20260602-123000-auxiliary-projector-local-Euler-equation-ledger` |
| Status | `auxiliary_projector_local_Euler_equation_ledger_written_C1_owner_contract_no_all_on_shell_no_local_GR_pass` |
| Claim ceiling | `auxiliary_projector_local_Euler_equation_ledger_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass` |
| Next target | `437-R10-alpha-lambda-executable-curve-contract.md` |

## 3. Source Register

| source_file | exists | role |
| --- | --- | --- |
| 356-parent-action-ward-identity-and-projector-variation.md | True | parent variation sectors and explicit Ward force ledger |
| 357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md | True | force fate map and retained PPN residual vector |
| 403-boundary-domain-flux-nohair-numeric-contract.md | True | boundary/domain/flux numeric locks and alpha3 severity |
| 429-Ward-Bianchi-exchange-owner-for-Poisson-source.md | True | C1 auxiliary-on-shell condition in q_loc identity |
| 430-Ward-source-residual-zero-route-gate.md | True | C1 ranked as best theorem route |
| 435-exterior-extra-source-nohair-owner-gate.md | True | R_extra owner gate and C1 next target |
| runs/20260601-181500-parent-action-ward-identity-and-projector-variation/results/parent_variation_terms.csv | True | machine-readable parent variation terms |
| runs/20260601-181500-parent-action-ward-identity-and-projector-variation/results/force_ledger.csv | True | machine-readable force origins and zero conditions |
| runs/20260601-181500-parent-action-ward-identity-and-projector-variation/results/projector_variation_forks.csv | True | projector variation fork validity table |
| runs/20260601-183000-Ward-owned-local-nohair-or-retained-PPN-residual-map/results/force_fate_map.csv | True | Ward-force fates and retained residual targets |
| runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source/results/exchange_owner_conditions.csv | True | C0-C7 conditions including C1 |
| runs/20260602-103000-Ward-source-residual-zero-route-gate/results/route_ranking.csv | True | C1 ranked first in zero-route queue |
| runs/20260602-121500-exterior-extra-source-nohair-owner-gate/results/exterior_source_owner_gate.csv | True | E5 auxiliary-offshell gate and R_extra routing |

## 4. C1 Identity Chain

| step | claim | status | meaning |
| --- | --- | --- | --- |
| 1 | Write the local parent configuration with every hidden variable included. | ledger_contract | fixed external or readout-only variables cannot secretly source local equations |
| 2 | Vary every hidden variable before reducing to readout. | required_not_fully_supplied | C1 can only be theorem-level if every E_A exists as a parent equation |
| 3 | The Ward identity exposes off-shell forces. | structural_identity_imported | off-shell hidden variables are not small by default; they are force sources |
| 4 | On-shell auxiliary equations kill only their own off-shell force term. | conditional_theorem_shape | stress, boundary, non-EH, and source-normalization debts can still remain |
| 5 | Constraint/topological variables need a stronger proof than E_A=0. | not_parent_derived | a solved constraint can still choose a preferred frame or location if the selector is physical |
| 6 | Boundary-supported equations are not bulk no-hair by themselves. | not_derived | boundary flux can be owned but nonzero in local observables |
| 7 | If any E_A is missing, symbolic, or not solved, its force is retained. | retained_policy | no row gets theorem-zero credit from an unnamed auxiliary equation |

Core local identity:

```text
For hidden variables Z_A, define E_A := delta S_parent / delta Z_A.

The local Ward/Bianchi force contains

q_loc^nu superset sum_A E_A nabla^nu Z_A
                 + F_projector^nu + F_boundary^nu + F_domain^nu.

C1 passes only if each E_A is explicitly supplied and either:
  E_A=0 in the local exterior,
  Z_A is pure gauge/topological with no local stress,
  the source is harmless constant universal calibration,
  or the residual is retained and scored.
```

## 5. Euler Ledger Rows

| ledger_id | field_or_selector | current_status | if_not_zero_rows | next_action |
| --- | --- | --- | --- | --- |
| A0_bulk_X_memory_load | X_A bulk/memory/load fields | operator_and_sources_not_parent_derived | R3;R4;R9;R10 | derive local X operator/sign/source-free exterior or supply alpha_X(lambda_X) |
| A1_projector_PD | P_D relative-chain/cohomology projector | conditional_open | R5;R6;R7;R8;R11 | derive P_D as parent-owned covariant object or retain projector stress vector |
| A2_projector_constraint_multiplier | lambda_P enforcing relative-chain/projector constraint | not_supplied | R5;R6;R7;R8;R11 | write explicit constraint and show first-class/topological or retain |
| A3_boundary_class_variables | Y_partialD, boundary class, induced boundary data | conditional_noangular_radial_flux_open | R3;R4;R7;R8;R9 | derive class-only boundary action and radial/time no-hair or retain coefficients |
| A4_domain_selector | chi_D coherent-domain selector | not_parent_derived | R5;R6;R7;R8;R10 | derive zero-knob covariant domain selector or retain domain residuals |
| A5_domain_normal_frame | n_mu, local frame, domain vector data | not_derived | R5;R6;R8 | prove no preferred-frame/location vector survives or retain alpha1/alpha2/xi rows |
| A6_coarse_graining_scale | L_cg coarse-graining/domain scale | not_derived | R8;R9;R10 | derive local constancy/decoupling of L_cg or supply gradient residual |
| A7_mass_flux_projector | Pi_M J source-normalization flux | conditional_flux_calibration_open | R1;R4;R9;R10 | derive flux closure plus absolute calibration or retain source-normalization residuals |
| A8_nonEH_operator_coefficients | c_nonEH or non-EH operator auxiliaries | retained_symbolic | R3;R4;R8;R10;R11 | derive EH-only selection or provide c_nonEH vector for scorer |
| A9_readout_active_masks | P_read, P_active, fitted masks | conditional_no_cheat_contract | R0;R1;R5;R11 | reject any branch where readout masks backreact through S_parent |

## 6. Legal Fates

| fate | required_evidence | row_policy |
| --- | --- | --- |
| on_shell_theorem_zero | explicit E_A from parent action plus proof E_A=0 in local exterior | only the E_A nabla Z_A term can receive theorem-zero credit |
| gauge_or_topological | first-class/gauge/topological proof with no local stress or force | can demote local bulk force, but boundary/source remnants still audited |
| boundary_only_harmless | support only on boundary plus class/topological constant monopole | may become calibration only if universal/time/range/species independent |
| retained_residual | coefficient, amplitude, or curve mapped to R rows | score or block depending on executable data |
| invalid_hidden_variable | fixed external projector/domain/mask or dropped metric stress | reject branch rather than retain as small |

## 7. Invalid Forks

| fork | why_invalid | required_repair |
| --- | --- | --- |
| fixed_external_projector_or_domain | not varied and explicitly breaks the Ward identity while looking like a definition | make it covariant/dynamical/topological or reject branch |
| metric_dependent_projector_without_stress | delta_g P_D contributes physical stress | retain T_projector/F_P or prove metric independence |
| solved_auxiliary_but_stress_dropped | E_A=0 does not imply T_A=0 or div T_A=0 | show stress is zero/pure gauge/topological or retain coefficient |
| boundary_EOM_used_as_bulk_nohair | flux balance can still leave radial/vector/shear hair | derive boundary no-hair or retain boundary multipoles |
| readout_mask_backreacts | post-readout fitting mask becomes a hidden parent source | readout after variation only |
| symbolic_Euler_equation_counts_as_zero | an unnamed E_A=0 cannot be scored or audited | write explicit equation, solution class, and residual fallback |

## 8. Row Implications

| row_id | C1_channel | current_transition |
| --- | --- | --- |
| R5_alpha1 | projector/domain vector and fixed-frame selector | retained_not_upgraded |
| R6_alpha2 | projector/domain vector and normal-frame data | retained_not_upgraded |
| R7_alpha3 | unowned off-shell auxiliary/projector/domain momentum flux | conditional_route_not_pass |
| R8_xi | domain/boundary/projector anisotropy | retained_not_upgraded |
| R9_Gdot | time-dependent auxiliary/source/boundary/domain flux | retained_contingent_not_upgraded |
| R10_fifth_force | bulk X, L_cg gradient, radial hair, finite-range auxiliary tail | symbolic_deferred_not_upgraded |
| R11_EH_operator_ledger | projector stress and non-EH auxiliary/operator coefficients | retained_symbolic_not_upgraded |

## 9. Residual Input Schema

| column | meaning | required |
| --- | --- | --- |
| ledger_id | matches one A0-A9 Euler ledger row | True |
| derivation_status | theorem_zero, gauge_topological, harmless_calibration, retained_numeric, retained_symbolic, invalid | True |
| equation_source | path to derivation/equation source or run artifact | True |
| residual_rows | semicolon-separated R rows affected if not theorem-zero | True |
| coefficient_or_curve_source | path to numeric coefficient, alpha(lambda), or c_nonEH vector if retained | False |
| claim_allowed | false unless all relevant rows are theorem-zero or scored below locks | True |

## 10. Theorem Attempt Status

| claim | status | evidence |
| --- | --- | --- |
| C1 Euler owner ledger written | pass | 10 hidden-variable ledger rows and 5 legal fates recorded |
| C1 is structurally the best theorem route | pass | route ranking imports C1 as direct owner of E_A nabla Z_A |
| all auxiliary/projector/domain equations are parent-derived and solved | fail | explicit equations, signs, constraints, and solution classes are not supplied for A0-A8 |
| off-shell force term is theorem-zero | fail | no all-channel E_A=0 proof; retained residuals remain |
| local GR/Newton/PPN promoted | fail | 0 row upgrades; R7/R9/R10/R11 remain retained or symbolic |

## 11. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| C1_identity_chain_written | pass | 7 identity stages recorded |
| Euler_ledger_written | pass | 10 hidden-variable rows recorded |
| legal_fates_written | pass | 5 legal fates recorded |
| invalid_forks_forbidden | pass | 6 fake-zero forks rejected |
| all_auxiliary_equations_parent_supplied | fail | explicit parent Euler equations missing for several hidden variables |
| all_auxiliary_equations_on_shell_locally | fail | no proof E_A=0 for A0-A8 in compact ordinary exterior |
| projector_domain_covariance_derived | fail | P_D/chi_D/n_mu/L_cg local silence not parent-derived |
| auxiliary_stress_zero_or_harmless | fail | E_A=0 does not yet imply T_A/div T_A harmless for all sectors |
| residual_input_schema_written | pass | template schema for retained C1 rows recorded |
| runner_rows_promoted_to_theorem_zero | fail | 0 row upgrades; C1 remains owner contract |
| local_GR_promoted | fail | Euler ledger only; no EH/Newton/PPN/local-GR pass |
| claim_ceiling_enforced | pass | auxiliary_projector_local_Euler_equation_ledger_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass |

## 12. Decision

C1 is now an explicit Euler owner ledger. This is the best structural route for the off-shell Ward force because q_loc contains the terms E_A nabla Z_A, and those terms vanish only when the parent action supplies and solves every hidden-variable Euler equation. The current corpus does not yet provide explicit local equations, signs, constraint algebra, source-free exterior conditions, stress harmlessness, or residual coefficients for all auxiliary/projector/domain sectors. Therefore C1 is sharpened but not promoted: hidden-variable forces are either future theorem targets or retained residuals, and local GR remains unclaimed.

Practical read: this is good plumbing. C1 is where hidden machinery stops being mystique and becomes engineering: write the equation, solve it, or carry the force. No local-GR belt until that ledger closes.

## 13. Next Queue

| rank | target | why_next |
| --- | --- | --- |
| 1 | 437-R10-alpha-lambda-executable-curve-contract.md | R10 is still symbolic; finite-range auxiliary tails need theorem-zero or an executable alpha(lambda) curve |
| 2 | 438-R11-nonEH-coefficient-vector-contract.md | R11 remains symbolic unless EH-only exterior is derived or c_nonEH is supplied |
| 3 | filled local residual vector smoke | C1 retained rows need actual coefficients/curves before empirical local testing |
