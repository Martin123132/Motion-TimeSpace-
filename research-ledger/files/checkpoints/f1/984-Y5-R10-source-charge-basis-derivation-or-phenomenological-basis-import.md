# 984 Y5 R10: Source-Charge Basis Derivation Or Phenomenological Basis Import

Status: `Y5_R10_984_universal_Hilbert_source_gives_conditional_zero_nonzero_charge_basis_imported_nonclaim`

Claim ceiling: no WEP pass, no `b_kappa` bound, no `b_theta` bound, no source-charge theorem-zero promotion, and no local-GR claim.

## Readout

984 separates two things that must not be blurred. If the parent action truly has one observed coframe, one universal `kappa`, and one Hilbert stress current for all ordinary matter, then WEP source-charge residuals vanish conditionally. That is a zero theorem route.

But a nonzero source-charge basis is not derived by that universal-source theorem. A nonzero basis is a parameterization of deviations from universal source coupling. Therefore the finite branch can import a Damour-Donoghue-style phenomenological charge basis only as nonclaim scaffolding.

In blunt terms: either derive zero, or import a basis. Do not pretend the imported basis is MTS-derived.

## Local Source Register

| source_id | role | exists | needle_found | path |
| --- | --- | --- | --- | --- |
| 983_doc | handoff selecting source-charge basis derivation/import | true | true | 983-Y5-R10-WEP-source-charge-projection-matrix-MICROSCOPE-TiPt.md |
| 983_projection_attempt | WEP projection skeleton with missing C-source coefficients | true | true | source-intake/mts_residuals/P8_Y5_R10_983_PROJECTION_ATTEMPT.csv |
| 983_delta_vector | MICROSCOPE alloy differential proxy vector | true | true | source-intake/mts_residuals/P8_Y5_R10_983_DIFFERENTIAL_PROXY_VECTOR.csv |
| 983_identity_bounds | debug-only single-proxy bounds | true | true | source-intake/mts_residuals/P8_Y5_R10_983_IDENTITY_DEBUG_BOUNDS.csv |
| 575_constant_lock | constant/source lock contract | true | true | source-intake/mts_residuals/P8_Y5_R10_575_CONSTANT_SOURCE_LOCK_CONTRACT.csv |
| 622_doc | parent matter sector and source-weight slot definitions | true | true | 622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md |
| 447_doc | one-coframe not enough; source-charge theorem gap | true | true | 447-no-species-source-charge-one-coframe-theorem-attempt.md |
| 448_doc | constant-sector universality and theta_A(I_Q) warning | true | true | 448-constant-sector-universality-theorem-attempt.md |

## Web Source Register

| web_source_id | title | authors | year | url | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| WEB984_0_DAMOUR_DONOGHUE_DILATON_COUPLINGS | Phenomenology of the Equivalence Principle with Light Scalars | Damour and Donoghue | 2010 | https://arxiv.org/abs/1007.2790 | phenomenological scalar-composition charge basis; five dilaton parameters with dominant nuclear/electromagnetic directions | false |
| WEB984_1_DAMOUR_DONOGHUE_EPV | Equivalence Principle Violations and Couplings of a Light Dilaton | Damour and Donoghue | 2010 | https://arxiv.org/abs/1007.2792 | explicit EP-violation parameterization and dominant charge directions | false |
| WEB984_2_MICROSCOPE_DILATON_CONSTRAINTS | MICROSCOPE mission: first constraints on the violation of the weak equivalence principle by a light scalar dilaton | Berge et al. | 2018 | https://arxiv.org/abs/1712.00483 | MICROSCOPE use of scalar/dilaton WEP projection language | false |
| WEB984_3_DAMOUR_THEORETICAL_EP_REVIEW | Theoretical Aspects of the Equivalence Principle | Damour | 2012 | https://arxiv.org/abs/1202.6311 | review of EP-violation phenomenology dominated by Coulomb and nuclear binding effects | false |

## Derivation Attempt

| attempt_id | claim | result | reason | missing_for_MTS_derivation | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SCB984_0_universal_Hilbert_source | If one observed coframe and one universal kappa couple to the Hilbert stress current of all ordinary matter, no composition-dependent source charge appears. | RELATIVE_ZERO_THEOREM | all test bodies source the same metric current; differential free fall needs an extra non-universal channel | parent proof of one kappa, one observed coframe, constant-sector trivial action, and measured-GM calibration | false |
| SCB984_1_source_charge_basis_not_from_universal_source | A nonzero source-charge basis cannot be derived from strict universal Hilbert-source coupling alone. | NO_NONZERO_BASIS_FROM_UNIVERSAL_SOURCE | the very purpose of a source-charge basis is to parameterize deviations from universal source coupling | parent term that couples MTS residuals to nuclear/EM mass contributions | false |
| SCB984_2_MTS_specific_basis_requirement | An MTS-derived basis must say which parent field changes which part of rest mass/source normalization. | MTS_PARENT_TERM_MISSING | current MTS corpus has coefficient slots, but not a parent Lagrangian term identifying nuclear/EM sensitivities | explicit parent coupling to QCD scale, quark-mass, EM/Coulomb, electron-mass, or marker source terms | false |
| SCB984_3_import_policy | Use an external phenomenological charge basis only as a nonclaim scaffold. | PHENOMENOLOGICAL_IMPORT_ALLOWED_NONCLAIM | this permits screening/debugging without pretending the basis is MTS-derived | derive or source the C_i-to-MTS coefficient map | false |
| SCB984_4_verdict | 984 source-charge basis status. | DERIVED_ZERO_OR_IMPORTED_NONCLAIM_BASIS_ONLY | we can derive the condition under which source charges vanish, but not the nonzero basis coefficients | parent source-charge deformation term or theorem-zero closure | false |

## Imported Phenomenological Basis

| basis_id | imported_charge | proxy_in_983 | phenomenological_role | maps_to_MTS_slot | source | import_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IMP984_0_universal_part | universal mass/source component | none; cancels in eta_AB | common coupling does not produce WEP contrast | universal kappa baseline, not b_kappa residual | WEB984_0_DAMOUR_DONOGHUE_DILATON_COUPLINGS | background_only | false |
| IMP984_1_nuclear_surface_light_quark | dominant nuclear binding/light-quark-mass direction | neutron_excess_proxy plus A_bar/A_surface proxy placeholders | composition-dependent nuclear binding sensitivity | b_theta if MTS changes matter constants; b_kappa only if source normalization becomes composition dependent | WEB984_0_DAMOUR_DONOGHUE_DILATON_COUPLINGS | phenomenological_nonclaim | false |
| IMP984_2_electromagnetic_Coulomb | electromagnetic/Coulomb direction | coulomb_proxy | fine-structure/Coulomb contribution to composition-dependent mass | b_theta/alpha_EM first; b_kappa only after source-normalization projection | WEB984_1_DAMOUR_DONOGHUE_EPV | phenomenological_nonclaim | false |
| IMP984_3_electron_fraction | electron/electromagnetic matter fraction proxy | Y_e_proxy | rough electron/proton fraction sensitivity; not full DD charge formula | b_theta or b_m only with explicit matter-sector coupling | WEB984_0_DAMOUR_DONOGHUE_DILATON_COUPLINGS | debug_proxy_nonclaim | false |
| IMP984_4_marker_or_material_charge | unclassified material marker/source-normalization charge | A_bar_proxy or user-defined material marker | captures non-standard composition/source weighting not in known charge basis | b_m or b_kappa | MTS_internal_gap_from_983 | MTS_placeholder_nonclaim | false |

## Basis To MTS Slot Map

| map_id | basis_id | MTS_slot | status | claim_effect | missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BMAP984_0_universal_kappa | IMP984_0_universal_part | baseline kappa | cancels_in_WEP | does not bound b_kappa | none for cancellation; parent derivation still needed for local GR | false |
| BMAP984_1_nuclear_to_btheta | IMP984_1_nuclear_surface_light_quark | b_theta | phenomenological_route | would bound matter-constant sensitivity, not source kappa directly | parent link between MTS field and quark/nuclear binding parameters | false |
| BMAP984_2_coulomb_to_btheta | IMP984_2_electromagnetic_Coulomb | b_theta | phenomenological_route | would bound alpha_EM-like sensitivity | parent EM/fine-structure coupling normal form | false |
| BMAP984_3_basis_to_bkappa | IMP984_1_nuclear_surface_light_quark;IMP984_2_electromagnetic_Coulomb;IMP984_4_marker_or_material_charge | b_kappa | not_derived | cannot bound source-weight splitting yet | source-normalization theorem or explicit non-universal gravitational charge term | false |
| BMAP984_4_marker_to_bm | IMP984_4_marker_or_material_charge | b_m | placeholder_only | marks unclassified material marker channel | marker taxonomy and no-extension theorem | false |

## Screening Policy

| policy_id | branch | allowed_action | current_status | claim_allowed |
| --- | --- | --- | --- | --- |
| SPOL984_0_theorem_zero_branch | parent-derived universal Hilbert source | set WEP source-charge basis to zero only if 575/622/979 source-universality gates are parent-signed | not_signed | false |
| SPOL984_1_phenomenological_branch | imported Damour-Donoghue-like charge basis | screen eta_AB against proxy charge deltas using labelled C_i coefficients | allowed_nonclaim_scaffold | false |
| SPOL984_2_identity_debug | single-proxy identity assumption | use 983 identity bounds only for debugging scale intuition | debug_only | false |
| SPOL984_3_MTS_claim | MTS coefficient bound | requires explicit C_i-to-b_slot map or theorem-zero proof | blocked | false |

## Claim Gates

| gate_id | claim | gate_pass | claim_allowed | why_not |
| --- | --- | --- | --- | --- |
| CGATE984_0_universal_source_zero | universal Hilbert source would zero WEP source charges | relative_only | false | the parent source-universality gates are not signed |
| CGATE984_1_imported_basis_ready | phenomenological charge basis is available for nonclaim screening | true | false | available scaffold is not an MTS derivation |
| CGATE984_2_bkappa_bound | MICROSCOPE bounds MTS b_kappa | false | false | C_i-to-b_kappa source-normalization projection is missing |
| CGATE984_3_btheta_bound | MICROSCOPE bounds MTS b_theta | false | false | MTS-to-matter-constant coupling normal form is missing |
| CGATE984_4_WEP_local_GR | WEP/local-GR branch passes | false | false | 984 is basis discipline only; no scored MTS coefficient |

## Decision Ledger

| decision_id | topic | result | reason | next_action |
| --- | --- | --- | --- | --- |
| DEC984_0_derivation | Hilbert-source derivation | zero_theorem_conditional_nonzero_basis_not_derived | universal Hilbert source removes composition dependence rather than producing a finite source-charge basis | separate theorem-zero branch from phenomenological finite branch |
| DEC984_1_import | phenomenological basis | Damour_Donoghue_style_basis_imported_nonclaim | known EP phenomenology supplies charge directions for screening, but not MTS coefficients | wire imported C_i scaffold into a screening-only WEP runner |
| DEC984_2_best_next | next checkpoint | WEP_screening_runner_with_imported_basis | we now have composition deltas plus imported nonclaim charge basis; next step is a runner that refuses claims unless C_i-to-b_slot map is supplied | write 985 WEP imported-basis screening runner for MICROSCOPE Ti/Pt |

## Validation

| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V984_0_sources | pass | all local sources exist and needles are found | 2026-06-14T01:49:19.160735+00:00 |
| V984_1_web_sources | pass | phenomenological web source rows are recorded and nonclaim | 2026-06-14T01:49:19.160747+00:00 |
| V984_2_derivation_verdict | pass | zero theorem/import-only verdict is recorded | 2026-06-14T01:49:19.160750+00:00 |
| V984_3_imports_nonclaim | pass | imported basis rows are nonclaim scaffolds | 2026-06-14T01:49:19.160753+00:00 |
| V984_4_maps_nonclaim | pass | basis-to-slot maps are nonclaim rows | 2026-06-14T01:49:19.160755+00:00 |
| V984_5_policy_safe | pass | screening policies do not allow claims | 2026-06-14T01:49:19.160758+00:00 |
| V984_6_claim_gates_safe | pass | claim gates block WEP/local-GR claims | 2026-06-14T01:49:19.160760+00:00 |
| V984_7_next_decision | pass | 985 imported-basis screening runner selected | 2026-06-14T01:49:19.160763+00:00 |
| V984_8_next_target_written | pass | next target row is present and nonclaim | 2026-06-14T01:49:19.160765+00:00 |
| V984_9_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T01:49:19.160768+00:00 |
| V984_READY | pass | 984 checkpoint pack validation summary | 2026-06-14T01:49:19.160771+00:00 |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 985-Y5-R10-WEP-imported-basis-screening-runner-MICROSCOPE-TiPt.md | build a nonclaim WEP screening runner using the imported phenomenological charge basis and MICROSCOPE alloy proxy deltas | C_i placeholder vector, eta prediction formula, identity/debug scenarios, hard claim gates for missing C_i-to-MTS map | WEP pass, b_kappa/b_theta bound claim, invented coefficients, GitHub action, formalization-workbench edits | false |
