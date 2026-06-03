# 433 - Kappa/G_eff Local Constancy Lemma

Private C5/source-normalization derivation checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 432 sharpened the same-frame matter functor but did not derive it. This checkpoint attacks the next source-normalization pressure point: can `kappa_eff/G_eff` be derived constant, universal, and source/species/range independent, or must it remain a retained residual?

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/kappa_Geff_local_constancy_lemma.py` |
| Run directory | `runs/20260602-114500-kappa-Geff-local-constancy-lemma` |
| Status | `kappa_Geff_local_constancy_lemma_written_Bianchi_forces_constancy_only_under_same_frame_conserved_source_premises_not_parent_derived_no_local_GR_pass` |
| Claim ceiling | `kappa_Geff_local_constancy_lemma_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass` |
| Next target | `434-measured-GM-mu-extra-zero-route.md` |

## 3. Source Register

| source_file | exists | role |
| --- | --- | --- |
| 402-EH-source-normalization-parent-pair.md | True | EH/source-normalization pair and kappa-to-G_eff bridge |
| 424-same-frame-EH-source-Poisson-reduction-gate.md | True | Poisson reduction requires constant universal kappa and measured GM |
| 425-EH-operator-retained-ledger-and-source-normalization-test-plan.md | True | source-normalization channel plan and local bound rows |
| 429-Ward-Bianchi-exchange-owner-for-Poisson-source.md | True | Bianchi identity with T_obs nabla kappa_eff source residual term |
| 430-Ward-source-residual-zero-route-gate.md | True | C5 constant kappa/G_eff route ranking |
| 432-same-frame-matter-functor-zero-route.md | True | C0 same-frame matter functor remains conditional |
| runs/20260602-025500-source-normalized-Newtonian-limit-under-identity-closure/results/source_normalization_contract.csv | True | machine-readable source-normalization contracts |
| runs/20260602-025500-source-normalized-Newtonian-limit-under-identity-closure/results/weak_field_derivation_steps.csv | True | weak-field chain defining G_eff and mu_obs |
| runs/20260602-002500-source-normalization-Geff-Meff-GM-absorption-theorem/results/absorption_gate_matrix.csv | True | GM absorption gates including G_eff constancy and universality |
| runs/20260602-002500-source-normalization-Geff-Meff-GM-absorption-theorem/results/failure_modes.csv | True | source-normalization failure modes |
| runs/20260602-002500-source-normalization-Geff-Meff-GM-absorption-theorem/results/decision.csv | True | previous decision retaining deltaG/Gdot/WEP/beta/fifth-force rows |
| runs/20260602-103000-Ward-source-residual-zero-route-gate/results/route_ranking.csv | True | C5 hard source-normalization route |

## 4. Constancy Lemma Chain

| step | claim | status | meaning |
| --- | --- | --- | --- |
| 1 | Work in one observed frame with an EH-shaped local exterior equation. | conditional_branch_only | this is not yet parent-derived; it is the local GR-corner test branch |
| 2 | Take the covariant divergence in the observed frame. | identity_pass | Bianchi exposes the kappa-gradient exchange term |
| 3 | Impose same-frame matter conservation and no extra exchange. | conditional_not_parent_derived | requires C0/C1/C3/C4/C7 debts to be silent or retained |
| 4 | For arbitrary ordinary matter stresses, kappa_eff must be locally constant. | conditional_theorem | Bianchi can force constancy only when matter stress has enough rank and the branch is source-universal |
| 5 | Vacuum alone cannot prove the plateau. | counterexample_warning | a pure local-vacuum plateau axiom would be smuggled, not derived |
| 6 | Convert constant kappa_eff to constant G_eff only in the EH/source unit convention. | algebra_pass_conditional_context | absolute calibration and physical mass units remain separate source-normalization debts |
| 7 | Species, source, and range independence are not automatic from spacetime constancy. | not_parent_derived | universality needs its own theorem or retained empirical rows |

Exact conditional lemma:

```text
Assume a same-frame local EH branch:

G_munu[g_obs] + Lambda g_obs_munu
  = kappa_eff(x,Z,A,lambda) T_obs_munu + S_extra_munu.

Bianchi gives

0 = (nabla_mu kappa_eff) T_obs^mu_nu
    + kappa_eff nabla_mu T_obs^mu_nu
    + nabla_mu S_extra^mu_nu.

If nabla_mu T_obs^mu_nu=0, if S_extra is zero or separately conserved,
and if ordinary local matter stresses span the tested directions,
then nabla_mu kappa_eff=0.
```

This proves only a conditional spacetime-constancy lemma. It does not prove species, source, range, or absolute measured-GM universality.

## 5. Kappa Constancy Requirements

| requirement | current_status | if_missing | rows_at_risk |
| --- | --- | --- | --- |
| same_observed_frame | conditional_from_C0_not_parent_derived | kappa can look constant in one frame while measured matter sees another | R0;R2;R3;R4;R11 |
| EH_or_Bianchi_closed_operator | conditional_Lovelock_route_not_parent_derived | non-EH divergence can cancel kappa drift | R3;R4;R10;R11 |
| separate_matter_conservation | conditional_on_same_frame_matter_functor | matter exchange can absorb nabla kappa | R1;R7;R9;R10 |
| no_extra_exchange_stress | not_derived | boundary, domain, projector, or auxiliary exchange cancels T nabla kappa | R3;R4;R7;R8;R9;R10;R11 |
| arbitrary_matter_stress_domain | assumption_needed_for_theorem | T^mu_nu nabla_mu kappa=0 may only constrain one projection | R1;R2;R4;R9 |
| species_universal_coupling | not_parent_derived | source-normalization WEP charge survives | R1 |
| range_independent_coupling | symbolic_deferred | finite-range force is hidden as G_eff(r,lambda) | R10 |
| absolute_unit_calibration | not_parent_derived | constant kappa is fitted normalization, not measured Newton source proof | R4;R9 |

## 6. Bianchi Case Analysis

| case_id | result | verdict |
| --- | --- | --- |
| vacuum_only | Bianchi gives no constraint on kappa_eff gradient | reject_as_plateau_proof |
| single_dust_flow | u^mu nabla_mu kappa_eff=0 along that flow only | partial_projection_not_full_constancy |
| arbitrary_matter_family | nabla_mu kappa_eff=0 in the tested local domain | conditional_constancy_theorem |
| exchange_owned_but_nonzero | total Ward identity holds while measured G_eff drifts | retained_residual_not_GR |
| scalar_kappa_field | can be covariant but becomes scalar-tensor/fifth-force branch unless phi is constant | modified_gravity_or_bound_route |
| species_or_range_dependent_kappa | spacetime Bianchi constancy is insufficient for measured universality | R1_R10_retained |

## 7. Source-Residual Implications

| term | zero_route | current_status | residual_rows |
| --- | --- | --- | --- |
| delta_kappa_source | derive nabla_mu kappa_eff=0 and partial_A/source/lambda kappa_eff=0 | conditional_spacetime_constancy_only_not_parent_derived | R1;R4;R9;R10 |
| T_obs nabla kappa_eff | Bianchi plus same-frame separate matter conservation plus arbitrary stress | conditional_theorem_shape | R9;R10 |
| species_source_charge | derive one universal kappa/source normalization for all compositions | not_derived | R1 |
| time_drift | derive partial_t ln(G_eff M_eff)=0 | not_derived | R9 |
| range_dependence | derive no finite-range mediator or supply alpha(lambda) curve | symbolic_deferred | R10 |
| absolute_calibration | derive parent-fixed physical units and Pi_M-to-M_eff calibration | not_parent_derived | R4;R9 |

## 8. Bound Fallback Matrix

| quantity_if_not_derived | runner_row | bound_or_required_data | action |
| --- | --- | --- | --- |
| partial_t ln G_eff | R9_Gdot | 9.6e-15 yr^-1 source lock from local ledger | score numeric drift; no theorem-zero credit |
| partial_A ln mu_obs | R1_WEP_source_charge | 2.8e-15 source-normalization/WEP lock from local ledger | keep four-channel R1 source subscore |
| range-dependent delta G or alpha(lambda) | R10_fifth_force | executable alpha(lambda) curve required | symbolic row cannot pass |
| nonlinear source-normalization shift | R4_beta | 7.8e-05 beta/source-normalization lock from local ledger | score beta/source residual separately from direct Poisson algebra |
| boundary/domain/projector mass flux | R3;R4;R7;R8;R9;R11 | retained coefficient vector plus Ward-owned flux evidence | do not absorb as measured GM |

## 9. Theorem Attempt Status

| claim | status | evidence |
| --- | --- | --- |
| Bianchi can force local spacetime constancy of kappa_eff | conditional_pass | if same-frame matter is separately conserved, extra exchange is zero, and matter stresses are arbitrary |
| vacuum plateau derives kappa constancy | fail | T_obs=0 makes the kappa-gradient term vanish identically |
| current MTS parent action derives constant universal G_eff | fail | C0 same-frame, EH selection, exchange silence, and source normalization remain unproved |
| spacetime constancy solves species/source/range universality | fail | partial_A, source calibration, and alpha(lambda) debts are independent of nabla_mu kappa |
| C5 row can be promoted to local-GR theorem-zero | fail | 0 residual row upgrades; bound fallback remains required |

## 10. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| constancy_lemma_chain_written | pass | 7 Bianchi/constancy stages recorded |
| vacuum_plateau_rejected | pass | vacuum T=0 cannot constrain kappa_eff gradient |
| conditional_Bianchi_constancy_written | conditional_pass | T_obs^mu_nu nabla_mu kappa_eff=0 implies nabla kappa=0 only for arbitrary conserved same-frame stresses |
| same_frame_parent_derived | fail | C0 remains closure/conditional from checkpoint 432 |
| EH_operator_parent_derived | fail | non-EH operator ledger remains retained |
| extra_exchange_silenced | fail | boundary/domain/projector/auxiliary exchange terms remain retained or open |
| species_source_range_universality_derived | fail | spacetime Bianchi constancy does not prove partial_A/source/lambda independence |
| absolute_calibration_derived | fail | Pi_M-to-M_eff and physical GM calibration remain source-normalization debts |
| runner_rows_promoted_to_theorem_zero | fail | 0 row upgrades; R1/R4/R9/R10 remain retained or symbolic |
| local_GR_promoted | fail | C5 lemma attempt only; no Newton/PPN/local-GR pass |
| claim_ceiling_enforced | pass | kappa_Geff_local_constancy_lemma_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass |

## 11. Decision

The C5 kappa/G_eff route gets a real conditional lemma: in a same-frame EH branch with separately conserved matter, no extra exchange stress, and arbitrary ordinary matter stresses, Bianchi forces nabla_mu kappa_eff=0, so G_eff=kappa_eff c^4/(8 pi) is locally spacetime-constant in that branch. But vacuum alone cannot prove this, and the current MTS parent action has not derived the required same-frame, EH-selection, exchange-silence, species-universality, range-independence, or absolute source-calibration premises. Therefore C5 is sharpened but not promoted; R1/R4/R9/R10 remain retained or symbolic.

Practical read: this is one of the better derivation moves so far. Bianchi gives us a genuine pressure mechanism, but only after we stop asking empty vacuum to do the work. The theory has to earn same-frame conserved matter and no extra exchange; then `kappa_eff` has nowhere left to hide.

## 12. Next Queue

| rank | target | why_next |
| --- | --- | --- |
| 1 | 434-measured-GM-mu-extra-zero-route.md | even constant kappa does not prove mu_obs=G_eff M_eff with no hidden source/time/range/species correction |
| 2 | auxiliary/projector local Euler-equation ledger | C1 is still the highest-ranked Ward route for killing off-shell exchange terms |
| 3 | filled MTS local residual vector smoke | any non-derived kappa/source terms need numeric or executable residual entries |
