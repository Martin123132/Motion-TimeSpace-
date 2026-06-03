# 430 - Ward Source-Residual Zero Route Gate

Private route-ranking checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 429 gave the conditional Ward/Bianchi identity for `q_loc^nu`. This checkpoint ranks the C0-C7 zero conditions by route: what looks theorem-derivable, what is mixed, what is only empirically boundable for now, and what remains a hard symbolic blocker.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/Ward_source_residual_zero_route_gate.py` |
| Run directory | `runs/20260602-103000-Ward-source-residual-zero-route-gate` |
| Status | `Ward_source_residual_zero_route_gate_written_C0_C7_ranked_derivation_vs_bound_routes_no_zero_promotion_no_local_GR_pass` |
| Claim ceiling | `Ward_source_residual_zero_route_gate_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass` |
| Next target | `431-MTS-local-residual-vector-evaluator.md` |

## 3. Source Register

| source_file | exists | role |
| --- | --- | --- |
| 429-Ward-Bianchi-exchange-owner-for-Poisson-source.md | True | conditional Ward/Bianchi q_loc identity and C0-C7 zero conditions |
| 428-MTS-local-residual-vector-input-contract.md | True | 12-component residual-vector contract |
| 425-EH-operator-retained-ledger-and-source-normalization-test-plan.md | True | EH/source-normalization retained ledger |
| 358-local-EH-exterior-operator-from-Ward-closed-action.md | True | Ward closure not enough for EH operator selection |
| 357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md | True | Ward-force fates and no-hair/retained residual map |
| 356-parent-action-ward-identity-and-projector-variation.md | True | parent Ward force ledger and projector variation fork |
| runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source/results/exchange_owner_conditions.csv | True | C0-C7 machine-readable conditions |
| runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source/results/source_residual_decomposition.csv | True | source_residuals term decomposition |
| runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source/results/mu_extra_decomposition.csv | True | mu_extra channel decomposition |
| runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv | True | R0-R11 residual vector components |
| runs/20260602-093000-local-bound-runner-v4-evaluate-smoke/results/evaluation_digest.csv | True | sourced local-bound row locks |

## 4. C0-C7 Route Ranking

| rank | condition_id | route_class | derivation_status | blocks_rows |
| --- | --- | --- | --- | --- |
| 1 | C1_auxiliary_on_shell | best_theorem_route | structurally_available_not_supplied | R7;R9;R10;R11 |
| 2 | C0_same_frame | hard_theorem_route | not_parent_derived | R0;R1;R2;R3;R4;R11 |
| 3 | C5_constant_kappa_Geff | hard_source_normalization_route | not_derived | R1;R4;R9;R10 |
| 4 | C6_mu_extra_zero | hard_measured_source_route | not_derived | R1;R4;R5;R6;R7;R8;R9;R10 |
| 5 | C2_projector_covariant | mixed_theorem_or_bound_route | conditional_open | R5;R6;R7;R8;R11 |
| 6 | C3_boundary_nohair | mostly_bound_until_nohair_theorem | not_derived | R3;R4;R7;R8;R9 |
| 7 | C4_nonEH_divergence_silent | operator_selection_or_bound_route | retained | R3;R4;R5;R6;R8;R10;R11 |
| 8 | C7_R10_R11_resolved | executable_symbolic_blocker | symbolic_deferred | R10;R11 |

The useful read is:

```text
best theorem pressure: C1, C0, C5, C6
mixed theorem/bound pressure: C2, C3, C4
hard symbolic blocker: C7, plus unresolved C4
```

## 5. Zero Route Gate

| gate_id | route_type | conditions | action |
| --- | --- | --- | --- |
| G0_forbidden_route | forbid | C0;C2 | reject branch, not merely bound |
| G1_direct_Ward_zero | derive | C1 | promote only the specific force term, not full local GR |
| G2_same_frame_zero | derive | C0 | allow WEP/clock frame rows to seek theorem-zero |
| G3_source_normalization_zero | derive | C5;C6 | allow source_residuals/mu_extra rows to seek theorem-zero |
| G4_nohair_zero | derive_or_bound | C2;C3 | if not theorem-zero, carry coefficients into residual evaluator |
| G5_operator_zero | derive_or_bound | C4;C7 | block local-GR promotion while symbolic |

## 6. Source-Residual Route Matrix

| source_residual_term | current_route_status | next_required_artifact |
| --- | --- | --- |
| delta_kappa_source | bound_route_ready_derivation_missing | kappa/G_eff local constancy lemma |
| nonEH_divergence | symbolic_blocker | R10-R11 curve/operator-vector contract |
| auxiliary_offshell_force | best_derivation_target_open | parent local auxiliary Euler-equation ledger |
| projector_domain_force | mixed_route | projector no-vector/no-shear lemma |
| boundary_flux | mostly_bound_route | boundary class-only nohair theorem attempt |
| nonmetric_matter_exchange | hard_theorem_route_open | same-frame matter functor theorem attempt |

## 7. `mu_extra` Route Matrix

| mu_channel | zero_route | bound_route | current_route_status |
| --- | --- | --- | --- |
| species_source_charge | derive material/species blindness of source coupling | R1 direct/full source-charge residual | hard_theorem_route_open |
| time_drift | derive stationary local kappa and conserved measured mass | R9 Gdot/G residual | bound_route_ready_derivation_missing |
| range_dependence | prove no finite-range local force | R10 alpha(lambda) curve | symbolic_blocker |
| boundary_monopole_shift | prove only universal fixed calibration survives | R4/R9 source-normalization residuals | mostly_bound_route |
| domain_projector_mass | derive no preferred-frame/location/domain mass correction | R5/R6/R7/R8/R11 residuals | mixed_route |

## 8. Promotion Decision Tree

| decision_node | test | outcome | local_GR_credit |
| --- | --- | --- | --- |
| D0_invalid | fixed external projector, hidden frame split, dropped stress, or placeholder symbolic pass exists | reject branch | none |
| D1_empirical_viability | all numeric residuals below bounds and R10/R11 executable but derivation statuses include fitted/phenomenological/closure | viable modified-gravity/MTS stress-test branch | empirical_only_no_derived_GR |
| D2_partial_theorem | some C0-C7 conditions theorem-zero but others bounded/retained | partial local-GR support with retained residual vector | partial_no_promotion |
| D3_derived_local_GR_candidate | C0-C7 theorem-zero or harmless universal calibration plus EH/local PPN completion | candidate derived local GR reduction | candidate_only_pending independent audit |

## 9. Next Derivation Queue

| queue_id | target | conditions | suggested_next_file |
| --- | --- | --- | --- |
| Q1 | same-frame matter functor theorem | C0 | 431-same-frame-matter-functor-zero-route.md |
| Q2 | kappa/G_eff local constancy lemma | C5 | 431-kappa-Geff-local-constancy-lemma.md |
| Q3 | mu_extra measured-source nohair theorem | C6 | 431-mu-extra-measured-source-nohair-theorem.md |
| Q4 | MTS local residual-vector evaluator | all | 431-MTS-local-residual-vector-evaluator.md |

## 10. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | 0 missing source paths |
| C0_C7_ranked | pass | 8 ranked conditions |
| zero_route_gate_written | pass | 6 route gates |
| source_residual_route_matrix_written | pass | 6 source-residual routes |
| mu_extra_route_matrix_written | pass | 5 mu_extra routes |
| promotion_decision_tree_written | pass | 4 decision nodes |
| symbolic_blockers_identified | pass | C7_R10_R11_resolved |
| theorem_zero_promoted | pass | 0 theorem-zero promotions |
| local_GR_promoted | fail | route gate only; C0-C7 not solved |
| claim_ceiling_enforced | pass | Ward_source_residual_zero_route_gate_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass |

## 11. Decision

C0-C7 have been ranked into theorem, mixed, bound, and symbolic-blocker routes. The strongest derivation path is C1 auxiliary on-shell plus C0 same-frame plus C5/C6 source normalization. The weakest immediate path is C4/C7, which must become an executable non-EH/fifth-force coefficient contract or remain a hard local-GR blocker. No zero route is promoted yet.

Practical read: this is where the work stops being vague. We either push theorem routes C1/C0/C5/C6, or we build the residual evaluator and let the retained rows fight the sourced bounds. Both are legitimate. What is no longer legitimate is pretending a Ward identity alone hands us local GR.

## 12. Next Target

`431-MTS-local-residual-vector-evaluator.md`
