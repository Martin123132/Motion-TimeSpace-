# 412 - Runner-v4 Source-Charge Channel Map Review

Private R1/local-bound checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 409 flagged a fairness issue: `source_charge_1e_minus_14` scores four R1 channels, giving severity `14.2857` instead of the earlier three-channel `10.7143`. This checkpoint decides whether that fourth channel is a mistake, a conservative guardrail, or a separate subscore.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/v4_source_charge_channel_map_review.py` |
| Run directory | `runs/20260602-062500-v4-source-charge-channel-map-review` |
| Status | `v4_source_charge_channel_map_review_written_four_channel_guardrail_retained_direct_WEP_subscore_defined_no_claim_leak_no_local_GR_pass` |
| Claim ceiling | `v4_source_charge_channel_map_review_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass` |
| Next target | `413-no-marker-parent-action-theorem-attempt.md` |

## 3. R1 Channel Roles

| channel | role | full | direct |
| --- | --- | --- | --- |
| source_charge_species_split | direct_WEP_source_charge | True | True |
| bulk_X_composition_charge | direct_WEP_bulk_composition | True | True |
| boundary_species_charge | direct_WEP_boundary_composition | True | True |
| source_normalization_species_split | source_normalization_cross_channel | True | False |

## 4. Subscore Check

| subscore | channels | residual | severity | class |
| --- | --- | --- | --- | --- |
| four_channel_composite_guardrail | 4 | 4.000e-14 | 14.2857 | over_budget |
| three_channel_direct_WEP_subscore | 3 | 3.000e-14 | 10.7143 | over_budget |
| source_normalization_single_channel | 1 | 1.000e-14 | 3.57143 | over_budget |
| max_single_channel_conservative_floor | 4 | 1.000e-14 | 3.57143 | over_budget |

## 5. Policy Decision

| policy | decision | anti_cheat |
| --- | --- | --- |
| full_R1_composite_guardrail | retain_four_channel_sum | conservative guardrail; not an empirical pass/fail claim by itself |
| direct_WEP_subscore | define_three_channel_direct_subscore | subscore must be reported beside full R1 guardrail, not used to hide source-normalization debt |
| source_normalization_cross_channel | keep_visible_as_R1_cross_channel | do not double-count it inside one empirical claim, but do not delete it from the theory ledger |
| no_promotion_from_channel_split | claim_state_unchanged | changing channel grouping cannot produce theorem_zero or local-GR credit |

## 6. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| R1_channel_map_loaded | pass | 4 R1 channels found |
| four_channel_guardrail_retained | pass | 4 channels included in full guardrail |
| direct_WEP_three_channel_subscore_defined | pass | 3 channels included in direct-WEP subscore |
| source_normalization_not_hidden | pass | source_normalization_cross_channel |
| subscore_result_materially_unchanged | pass | all source_charge_1e_minus_14 subscore views remain over budget |
| severity_difference_explained | pass | four=14.285714285714285 three=10.714285714285714 |
| R1_state_unchanged | pass | R1 runner-v4 state remains retained_contingent_budget |
| no_theorem_credit_or_claim_leaks | pass | theorem_credit=0 claim_allowed=0 |
| local_GR_promoted | fail | channel-count review only; no local-GR pass |
| claim_ceiling_enforced | pass | v4_source_charge_channel_map_review_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass |

## 7. Decision

The R1 four-channel severity is intentional as a conservative composite guardrail, not an accidental claim leak. The fourth term, source_normalization_species_split, is not direct-only WEP composition charge, so future real-data reporting should split R1 into a three-channel direct-WEP subscore plus a visible source-normalization cross-channel. However, the full four-channel guardrail remains the correct stress profile when all R1 hazards are activated. The numerical result is unchanged in spirit: at 1e-14 per channel, three-channel, four-channel, and source-normalization-only views are all over the 2.8e-15 lock. No row is promoted and no local-GR claim is allowed.

Practical read: this was a good catch, but it is not a rescue loophole and not a hidden failure. The fair move is to report both views: three-channel direct WEP for direct composition tests, and four-channel full R1 when testing all source-charge hazards.

## 8. Next Target

`413-no-marker-parent-action-theorem-attempt.md`
