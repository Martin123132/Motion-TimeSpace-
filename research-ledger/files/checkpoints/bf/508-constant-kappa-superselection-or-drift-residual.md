# 508 — Constant Kappa Superselection or Drift Residual

Generated: 2026-06-04T03:00:24.661087+00:00  
Run: `runs/20260604-164500-constant-kappa-superselection-or-drift-residual`  
Status: `constant_kappa_topological_superselection_clause_built_conditional_current_MTS_not_derived_residual_map_written`  
Claim ceiling: `conditional_kappa_constancy_only_no_measured_GM_Newton_PPN_or_local_GR_promotion`

## 1. Verdict

The kappa/G_eff sector now has a precise non-cheat route:

```text
add or derive a parent topological zero-form/three-form sector
S_kappa_top = ∫ kappa_eff dA_3
variation in A_3 gives d kappa_eff = 0.
```

That would make `kappa_eff` an integration constant/global sector label rather than a local scalar hiding inside measured `GM`.

But this is still **conditional**. The current MTS corpus had the global-coupling contract; this checkpoint sharpens the parent clause that would derive it. It does not prove that the full MTS parent action already contains that clause.

So the honest branch is:

```text
conditional if topological/global kappa sector is adopted;
residual if kappa remains local or MTS-dependent.
```

## 2. Theorem Rows

| theorem_id | statement | mathematical_form | result | status | MTS_current_status |
| --- | --- | --- | --- | --- | --- |
| T508_0_global_sector | If kappa_eff belongs to a parent global/superselection sector, not a local field bundle, then compact-support local variations cannot generate d kappa_eff. | Q_parent = Q_dyn x K_global; kappa_eff in K_global; delta_local kappa_eff = 0 | D_X kappa_eff = 0 for local spacetime directions and local MTS variations, provided K_global is acted on trivially | conditional_parent_premise | not_parent_derived |
| T508_1_topological_zeroform | If the parent action contains a metric-independent topological zero-form/three-form pair, variation of the three-form can derive d kappa_eff=0 on connected local domains. | S_kappa_top = ∫ kappa_eff dA_3; delta_{A_3} S = -∫ d kappa_eff ∧ delta A_3 => d kappa_eff=0 | kappa_eff is an integration constant rather than a propagating scalar source | conditional_derivation_route | not_in_current_parent_action |
| T508_2_no_residual_if_closed | If T508_0 or T508_1 passes and kappa carries no species/range/frame/domain labels, then local G_eff derivative/source/range residuals from kappa vanish. | G_eff = kappa_eff c^4/(8π); D_X kappa_eff=0 => D_X G_eff=0 | P8_Geff_time_drift, kappa radial/range hair, and kappa species/source drift are zero from kappa sector only | conditional_corollary | not_promoted_because_parent_clause_not_adopted_or_derived |

## 3. Topological Zero-Form Clause

| clause_id | parent_clause | equation | required_ownership | if_missing |
| --- | --- | --- | --- | --- |
| K508_0_field_content | Introduce a metric-independent 3-form A_3 and a zero-form kappa_eff in a global/topological sector. | S_kappa_top = ∫_M kappa_eff dA_3 | A_3 and kappa_eff are not matter/source labels and do not vary with domain, memory, species, frame, or radial readout | kappa_eff remains a possible scalar/source-normalization residual |
| K508_1_variation_A3 | Varying A_3 gives the zero-gradient equation. | delta_{A_3} S = -∫_M d kappa_eff ∧ delta A_3 + boundary => d kappa_eff=0 | boundary variation of A_3 is fixed or topological and does not create measured-mass flux | zero-gradient proof becomes a boundary/closure assumption |
| K508_2_variation_kappa | Varying kappa_eff gives the companion topological/integration-constant equation and must not reintroduce local stress. | delta_kappa S gives dA_3 plus any allowed global-sector constraint | the companion equation is global/topological, not a local scalar force or source-current equation | the route becomes a dressed Lagrange multiplier patch |
| K508_3_metric_stress_silence | The topological sector is metric-independent or has only fixed background subtraction. | delta_g S_kappa_top = 0 in compact local exterior | no non-EH stress, no preferred-frame vector, no boundary mass-channel leakage | constant kappa may still be paid for by a new unowned stress sector |
| K508_4_matter_source_blindness | Matter/source action sees only the same constant kappa_eff and cannot carry species-specific kappa_A. | partial_A kappa_eff = partial_source kappa_eff = partial_m kappa_eff = 0 | source-current Ward universality and one observed coframe/source pullback | R1 source-charge and frame/source residuals remain active |

## 4. Residual Map

| residual_id | if_theorem_missing | symbol | observable_lock | target_bound | required_artifact | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| KR508_0_time_drift | dln_Geff_dt is retained | dln_Geff_dt | Gdot_over_G | 9.6e-15 yr^-1 or derived_zero | P8_time_drift_residual_or_zero.csv with separated G_eff, M_eff, and epsilon_mu terms | false |
| KR508_1_radial_hair | partial_r ln G_eff is retained | partial_r_ln_Geff | beta/gamma/radial source hair | zero radial hair or mapped local profile bound | P8_radial_mu_profile_or_zero.csv | false |
| KR508_2_range_dependence | alpha(lambda) from kappa running is retained | alpha_kappa(lambda) | R10_fifth_force | executable alpha(lambda) curve below inverse-square bounds | R10_alpha_lambda_curve_MTS_source_normalization.csv | false |
| KR508_3_species_source_charge | species/source dependence of kappa is retained | eta_source_AB or partial_A ln G_eff | R1_WEP_source_charge | 2.8e-15 or derived source universality | P8_species_source_charge_residual_or_zero.csv | false |
| KR508_4_frame_domain_split | frame/domain dependence of kappa is retained | delta_frame_source; partial_D ln G_eff | WEP/clock/R11/domain rows | one observed source frame or explicit residual below locks | P8_frame_source_split_residual_or_zero.csv | false |
| KR508_5_Bianchi_exchange | T_obs grad kappa exchange term is retained | delta_kappa_source | R4;R7;R9;R10;R11 | same-frame arbitrary-source conservation theorem or explicit exchange coefficient | P8_delta_kappa_source_exchange_residual.csv | false |

## 5. Gate Tests

| gate_id | gate | result | evidence |
| --- | --- | --- | --- |
| G508_0_conditional_theorem | topological/global kappa route is mathematically sufficient | pass_conditional | T508_0/T508_1 and K508_0-K508_4 |
| G508_1_parent_adoption | current MTS parent action actually contains the global/topological kappa clause | fail_for_current_claim | 453 says P0/P1 not established; 508 writes the clause but does not prove it is already in MTS |
| G508_2_residual_fallback | all failed kappa identities map to explicit residual rows | pass | residual_rows=6 |
| G508_3_no_local_GR_claim | constant kappa alone cannot promote measured-GM/Newton/local-GR | pass | M_eff, mu_extra, source measure, and EH operator rows remain open |

## 6. Decision

| decision_id | decision | meaning | claim_status |
| --- | --- | --- | --- |
| D508_0 | conditional_topological_zeroform_route_is_the_clean_derivation_path | kappa can be made constant without a plateau axiom if the parent action owns the topological zero-form/three-form sector | conditional_not_current_MTS_promotion |
| D508_1 | current_MTS_has_not_yet_earned_constant_kappa | the route is now exact, but the present corpus has not derived or adopted the required parent clause | kappa_Geff_silence_derived_false |
| D508_2 | if_not_adopted_run_residual_branch | dln_Geff_dt, radial/range/source/frame/domain and Bianchi exchange rows must stay visible and testable | residual_map_written |
| D508_3 | move_to_source_measure_after_kappa_gate | even with constant kappa as a conditional/global premise, measured GM still needs M_eff flux closure and source matching | 509-source-measure-Meff-flux-closure-after-kappa-gate.md |

## 7. Source Register

| source_file | role | exists |
| --- | --- | --- |
| 507-field-specific-silence-queue-kappa-domain-memory-motion.md | selects kappa/G_eff as first field-specific silence target | True |
| 453-global-coupling-superselection-parent-action-contract.md | existing global/superselection kappa parent-action contract | True |
| 452-constant-universal-Geff-kappa-identity-attempt.md | conditional constant G_eff/kappa theorem and Bianchi overclaim warning | True |
| source-intake/mts_residuals/P8_global_coupling_superselection_CONTRACT.csv | GS0-GS8 superselection requirements | True |
| source-intake/mts_residuals/P8_constant_universal_Geff_kappa_CONTRACT.csv | CU0-CU8 constant universal kappa/G_eff requirements | True |
| source-intake/mts_residuals/P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv | constant measured-GM theorem attempt and open Z1 global-coupling row | True |
| source-intake/mts_residuals/P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv | derivative-hair identity for measured mu_obs | True |
| source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv | local residual runner input rows for Gdot, radial, range, source, frame, and mu_extra | True |
| source-intake/mts_residuals/P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv | local bound matrix for source-normalization residuals | True |
| source-intake/local_bounds/local_bound_claims.csv | empirical lock table including Gdot and local PPN/fifth-force rows | True |
| scripts/constant_kappa_superselection_or_drift_residual.py | this checkpoint generator | True |

## 8. Validation

| check_id | result | detail |
| --- | --- | --- |
| V508_0_source_paths_exist | pass | missing=0 |
| V508_1_topological_clause_complete | pass | clause_rows=5 |
| V508_2_residual_map_complete | pass | residual_rows=6 |
| V508_3_no_overclaim | pass | kappa_Geff_silence_derived_for_MTS=false |
| V508_4_local_GR_claim_blocked | pass | local_GR_claim_allowed=false |

## 9. Route Update

| route_id | status | update | next_target |
| --- | --- | --- | --- |
| RU508_0 | conditional_kappa_derivation_route_sharpened | topological zero-form/three-form clause is the cleanest derivation route for d kappa_eff=0 | 509-source-measure-Meff-flux-closure-after-kappa-gate.md |
| RU508_1 | residual_fallback_active | if the clause is not adopted/derived, kappa becomes explicit local residual data rather than hidden measured-GM calibration | 509-source-measure-Meff-flux-closure-after-kappa-gate.md |

## 10. Claim Ceiling

Allowed:

```text
MTS has a precise conditional parent clause that would derive constant kappa.
MTS has a residual fallback map if kappa is local or MTS-dependent.
```

Forbidden:

```text
MTS has proved kappa_eff is constant in the current parent action.
MTS has derived measured GM, Newtonian recovery, PPN, or local GR.
MTS has hidden kappa drift inside fitted GM.
```

## 11. Next Target

`509-source-measure-Meff-flux-closure-after-kappa-gate.md`

If we carry constant kappa as a conditional global/topological premise, the next blocker is no longer G_eff. It is whether `M_eff` is the conserved parent source charge and whether source-measure matching is derived before orbital readout.
