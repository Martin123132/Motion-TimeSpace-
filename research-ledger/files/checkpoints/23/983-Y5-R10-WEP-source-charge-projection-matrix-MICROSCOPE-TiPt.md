# 983 Y5 R10: WEP Source-Charge Projection Matrix MICROSCOPE TiPt

Status: `Y5_R10_983_MICROSCOPE_alloy_composition_proxy_projection_written_nonclaim_source_charge_basis_missing`

Claim ceiling: no WEP pass, no `b_kappa` bound, no `b_theta` bound, no local-GR promotion. This is a projection attempt and proxy ledger only.

## Readout

983 fixes an easy-to-miss trap: MICROSCOPE is not literally pure Ti versus pure Pt. The SUEP test compares PtRh10 against a Ti-Al-V alloy. This checkpoint uses the alloy mass fractions and computes simple source-charge proxies, then refuses to call them MTS coefficients until the source-charge basis is derived.

The useful formula shape is:

`eta_TiPt ~= DeltaQ_source dot C_source + S_marker*b_m + S_theta*b_theta + S_source*b_kappa`.

The proxy deltas are now available. The missing object is the actual MTS source-charge basis `C_source` and its mapping into `b_kappa`, `b_theta`, and marker slots.

## Local Source Register

| source_id | role | exists | needle_found | path |
| --- | --- | --- | --- | --- |
| 982_doc | handoff selecting WEP/source-charge projection first | true | true | 982-Y5-R10-coupling-bound-projection-matrix-skeleton-and-screening-runner.md |
| 982_projection | projection matrix skeleton row for MICROSCOPE WEP | true | true | source-intake/mts_residuals/P8_Y5_R10_982_PROJECTION_MATRIX_SKELETON.csv |
| 981_candidates | MICROSCOPE eta source envelope | true | true | source-intake/mts_residuals/P8_Y5_R10_981_COUPLING_PRIOR_CANDIDATES.csv |
| 981_web_sources | MICROSCOPE final result provenance | true | true | source-intake/mts_residuals/P8_Y5_R10_981_WEB_SOURCE_LEDGER.csv |
| 622_doc | b_kappa/b_theta/b_m component definitions | true | true | 622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md |

## Web Source Register

| web_source_id | title | year | url | source_use | recorded_fact | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| WEB983_0_MICROSCOPE_CQG_COMPOSITION | Result of the MICROSCOPE weak equivalence principle test | 2022 | https://elib.dlr.de/193667/2/Touboul_2022_Class._Quantum_Grav._39_204009.pdf | composition of SUEP PtRh10 and Ti alloy test masses plus eta definition | SUEP inner mass PtRh10: 90 percent Pt and 10 percent Rh by mass; outer mass: 90 percent Ti, 6 percent Al, 4 percent V by mass | false |
| WEB983_1_MICROSCOPE_PRL_FINAL | MICROSCOPE mission: final results of the test of the Equivalence Principle | 2022 | https://arxiv.org/abs/2209.15487 | eta(Ti,Pt) final result anchor | eta(Ti,Pt) = [-1.5 +- 2.3(stat) +- 1.5(syst)]e-15, used in 981 as nonclaim screening envelope 6.992e-15 | false |

## Material Constituents

| material_id | element | mass_fraction | A | Z | source |
| --- | --- | --- | --- | --- | --- |
| M983_0_PtRh10 | Pt | 0.90 | 195.1 | 78 | WEB983_0_MICROSCOPE_CQG_COMPOSITION |
| M983_0_PtRh10 | Rh | 0.10 | 102.9 | 45 | WEB983_0_MICROSCOPE_CQG_COMPOSITION |
| M983_1_TiAlloy | Ti | 0.90 | 47.9 | 22 | WEB983_0_MICROSCOPE_CQG_COMPOSITION |
| M983_1_TiAlloy | Al | 0.06 | 27.0 | 13 | WEB983_0_MICROSCOPE_CQG_COMPOSITION |
| M983_1_TiAlloy | V | 0.04 | 50.9 | 23 | WEB983_0_MICROSCOPE_CQG_COMPOSITION |

## Charge Basis Proxies

| basis_id | proxy | physical_read | projection_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| QB983_0_electron_fraction | Y_e = Z/A | electron/proton fraction per nucleon mass proxy | proxy_only_not_MTS_derived | false |
| QB983_1_neutron_excess | q_N = (A - 2Z)/A | neutron excess proxy highlighted by MICROSCOPE material contrast | proxy_only_not_MTS_derived | false |
| QB983_2_coulomb_proxy | q_C = Z(Z-1)/A^(4/3) | nuclear electrostatic energy proxy; debug basis, not a full dilaton charge model | proxy_only_not_MTS_derived | false |
| QB983_3_mean_A_proxy | A_bar = sum mass_fraction*A | coarse mass-number contrast sanity feature | proxy_only_not_MTS_derived | false |

## Material Proxy Charge Vectors

| material_id | mass_fraction_sum | Y_e_proxy | neutron_excess_proxy | coulomb_proxy | A_bar_proxy | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M983_0_PtRh10 | 1.000000 | 4.035472577e-01 | 1.929054847e-01 | 5.187582949e+00 | 1.858800000e+02 | proxy_charge_vector_computed | false |
| M983_1_TiAlloy | 1.000000 | 4.603247142e-01 | 7.935057164e-02 | 2.613068278e+00 | 4.676600000e+01 | proxy_charge_vector_computed | false |

## Differential Proxy Vector

| delta_id | feature | definition | delta_value | absolute_delta | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| DEL983_Y_e_proxy | Y_e_proxy | Y_e_proxy(TiAlloy outer) - Y_e_proxy(PtRh10 inner) | 5.677745650e-02 | 5.677745650e-02 | nonzero_proxy_contrast | false |
| DEL983_neutron_excess_proxy | neutron_excess_proxy | neutron_excess_proxy(TiAlloy outer) - neutron_excess_proxy(PtRh10 inner) | -1.135549131e-01 | 1.135549131e-01 | nonzero_proxy_contrast | false |
| DEL983_coulomb_proxy | coulomb_proxy | coulomb_proxy(TiAlloy outer) - coulomb_proxy(PtRh10 inner) | -2.574514671e+00 | 2.574514671e+00 | nonzero_proxy_contrast | false |
| DEL983_A_bar_proxy | A_bar_proxy | A_bar_proxy(TiAlloy outer) - A_bar_proxy(PtRh10 inner) | -1.391140000e+02 | 1.391140000e+02 | nonzero_proxy_contrast | false |

## Projection Attempt

| projection_id | formula | known_inputs | missing_inputs | result | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| WEP983_0_vector_projection | eta_TiPt ~= DeltaY_e*C_e + Deltaq_N*C_N + Deltaq_C*C_C + DeltaAbar*C_A + S_marker*b_m + S_theta*b_theta + S_source*b_kappa | DeltaY_e,Deltaq_N,Deltaq_C,DeltaAbar,eta_screening_envelope | C_e,C_N,C_C,C_A,S_marker,S_theta,S_source,MTS_source_charge_basis | PROJECTION_SKELETON_READY | false |
| WEP983_1_bkappa_path | b_kappa contribution enters through source-normalization/composition sensitivity S_source | eta_envelope=6.992e-15 | S_source(TiAlloy,PtRh10),universal-Hilbert-source deviation definition | MISSING_SOURCE_CHARGE_PROJECTION | false |
| WEP983_2_btheta_path | b_theta contribution enters through material constants/EM/mass-ratio sensitivities | composition proxies | clock/EM/mass sensitivity model linking theta_A to Ti/Pt free-fall contrast | MISSING_CONSTANT_SENSITIVITY_PROJECTION | false |
| WEP983_3_identity_debug_bounds | if one proxy coefficient dominates, \|C_i\| <= eta_envelope/\|DeltaQ_i\| | DeltaY_e=5.678e-02;Deltaq_N=-1.136e-01;Deltaq_C=-2.575e+00 | proof that the chosen proxy coefficient equals an MTS residual slot | IDENTITY_DEBUG_ONLY | false |

## Identity Debug Bounds

| identity_bound_id | feature | eta_envelope | absolute_delta | identity_debug_bound | why_not_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| IB983_Y_e_proxy | Y_e_proxy | 6.992e-15 | 5.677745650e-02 | 1.231474679e-13 | identity single-proxy dominance is a debug assumption, not an MTS source-charge projection | false |
| IB983_neutron_excess_proxy | neutron_excess_proxy | 6.992e-15 | 1.135549131e-01 | 6.157373388e-14 | identity single-proxy dominance is a debug assumption, not an MTS source-charge projection | false |
| IB983_coulomb_proxy | coulomb_proxy | 6.992e-15 | 2.574514671e+00 | 2.715851682e-15 | identity single-proxy dominance is a debug assumption, not an MTS source-charge projection | false |
| IB983_A_bar_proxy | A_bar_proxy | 6.992e-15 | 1.391140000e+02 | 5.026093707e-17 | identity single-proxy dominance is a debug assumption, not an MTS source-charge projection | false |

## Screening Runner

| screen_id | requirement | result | claim_allowed | detail | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SCREEN983_0_schema | composition rows sum to one and produce nonzero proxy deltas | pass | false | schema/proxy sanity only | false |
| SCREEN983_1_identity_debug_bounds | identity debug bounds are finite for every proxy | pass | false | bounds are not MTS coefficient bounds | false |
| SCREEN983_2_real_projection | actual MTS source-charge projection supplied | blocked_missing_projection | false | C_e,C_N,C_C,C_A,S_source,S_theta,S_marker are not derived | false |
| SCREEN983_3_WEP_claim | WEP/source-splitting branch pass | blocked_no_claim | false | MICROSCOPE source anchor is ready, projection is not | false |

## Claim Gates

| gate_id | claim | gate_pass | claim_allowed | why_not |
| --- | --- | --- | --- | --- |
| CGATE983_0_composition_proxies | MICROSCOPE material proxy deltas are computed | true | false | proxy deltas are bookkeeping, not MTS predictions |
| CGATE983_1_bkappa_bound | MICROSCOPE bounds b_kappa | false | false | S_source projection from source-normalization residual to Ti/Pt Eotvos signal is missing |
| CGATE983_2_btheta_bound | MICROSCOPE bounds b_theta | false | false | theta_A/material-constant sensitivity model is missing |
| CGATE983_3_WEP_or_local_GR | WEP/local-GR branch passes | false | false | projection attempt only; no parent universal-source theorem and no scored coefficient row |

## Decision Ledger

| decision_id | topic | result | reason | next_action |
| --- | --- | --- | --- | --- |
| DEC983_0_composition | MICROSCOPE materials | real_alloy_composition_used | PtRh10 and Ti alloy mass fractions are used instead of pure-element shorthand | keep pure Ti/Pt language out of coefficient scoring |
| DEC983_1_projection | source-charge projection | proxy_vector_ready_projection_missing | Delta composition proxies are computable, but MTS source-charge coefficients are not derived | derive a source-charge basis from the parent matter action or import a conservative phenomenological basis explicitly |
| DEC983_2_best_next | next checkpoint | source_charge_basis_derivation_or_phenomenological_basis_import | without C_e,C_N,C_C,C_A and S_source, WEP cannot score b_kappa | write 984 source-charge basis derivation attempt from Hilbert-source universality; fallback to labelled phenomenological basis |

## Validation

| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V983_0_sources | pass | all local sources exist and needles are found | 2026-06-14T01:44:38.930197+00:00 |
| V983_1_web_sources | pass | web source rows are recorded and nonclaim | 2026-06-14T01:44:38.930209+00:00 |
| V983_2_constituents_written | pass | 5 constituent rows written | 2026-06-14T01:44:38.930212+00:00 |
| V983_3_mass_fractions_sum | pass | mass fractions sum to one for each material | 2026-06-14T01:44:38.930215+00:00 |
| V983_4_delta_proxies_nonzero | pass | all proxy charge deltas are nonzero and nonclaim | 2026-06-14T01:44:38.930217+00:00 |
| V983_5_projection_nonclaim | pass | projection rows do not claim MTS coefficient bounds | 2026-06-14T01:44:38.930220+00:00 |
| V983_6_identity_debug_nonclaim | pass | identity debug bounds are finite and nonclaim | 2026-06-14T01:44:38.930222+00:00 |
| V983_7_screening_claims_blocked | pass | screening runner blocks WEP/local-GR claims | 2026-06-14T01:44:38.930225+00:00 |
| V983_8_claim_gates_safe | pass | claim gates remain false except bookkeeping existence | 2026-06-14T01:44:38.930227+00:00 |
| V983_9_decision_next_target | pass | 984 source-charge basis target selected | 2026-06-14T01:44:38.930230+00:00 |
| V983_10_next_target_written | pass | next target row is present and nonclaim | 2026-06-14T01:44:38.930232+00:00 |
| V983_11_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T01:44:38.930234+00:00 |
| V983_READY | pass | 983 checkpoint pack validation summary | 2026-06-14T01:44:38.930237+00:00 |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 984-Y5-R10-source-charge-basis-derivation-or-phenomenological-basis-import.md | derive the source-charge basis linking composition proxies to MTS b_kappa/b_theta/b_m slots, or import it explicitly as phenomenological nonclaim structure | Hilbert-source universality, composition-charge basis C_e/C_N/C_C/C_A, Ti/Pt projection, claim gates | WEP pass, invented coefficients, theorem-zero promotion, GitHub action, formalization-workbench edits | false |
