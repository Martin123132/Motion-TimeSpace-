# 4584 - Parent material tensor and apparatus support zero or bound

Marker: `PPC4161_PARENT_MATERIAL_TENSOR_AND_APPARATUS_SUPPORT_ZERO_OR_BOUND_4584`  
Branch: `MTS_R2FR_Y5_PARENT_MATERIAL_TENSOR_AND_APPARATUS_SUPPORT_ZERO_OR_BOUND_4584`  
Decision: `PRIVATE_SOURCE_UNIVERSALITY_KILLS_ACTIVE_MATERIAL_SOURCE_WEIGHT_APPARATUS_DOMAIN_ZERO_OR_BOUND_RETAINED_NONCLAIM`  
Private/public status: private nonclaim; no GitHub action.

## Result

4584 separates two things that were getting tangled:

1. **Material tensors as empirical/readout inventory** remain real and useful for WEP, clock and orbital tests.
2. **Material labels as active gravitational source coefficients** are zero inside the private GR-parity/PPC4161 source-universality branch.

The strict branch is:

```text
fixed EM tail zero
+ Hom(MaterialLabel,Coeff_active_source)=empty
+ source-label forgetting
+ material projections are readout inventory only
+ apparatus included in source/reference OR disjoint postprocessing
=> C_material_tail = 0.
```

So the current readout envelope reduces to:

```text
C_readout <= C_kernel_active + C_EFT_active + C_tau_tail.
```

This is not public local GR.  If source-universality or apparatus-domain declaration fails, the fallback is explicit:

```text
C_readout <= Xi_src_hidden_material + C_apparatus_active
           + C_EM_tail + C_kernel_active + C_EFT_active + C_tau_tail.
```

## Material theorem rows

| checkpoint | theorem_id | claim | derivation | consequence | status | source | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4584 | MAT4584_0_source_universality_import | Material labels do not define active gravitational source coefficients inside the private GR-parity/PPC4161 branch. | 4446 adopts one imported S_matter scalar density functor, Hilbert variation before readout, and Hom(MaterialLabel, Coeff_active_source)=empty inside PPC4161. 4447 propagates that source-universality subspace to WEP/PPN/clock/orbital source pieces. | Material composition can change the Hilbert mass value and empirical inventory, but it cannot multiply the active source coefficient in the local field equation inside this branch. | PRIVATE_BRANCH_SOURCE_WEIGHT_ZERO_IMPORTED | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\462-PPC4161-adopt-GR-parity-SM-import-or-source-backed-material-Req-value.md | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | MAT4584_1_material_product_zero | sum_X |C_X R_material_X|=0 for active-source material weights in the adopted private branch. | The product sum_X |C_X R_material_X| represents a material label or sensitivity re-entering Coeff_active_source. Under source-label forgetting and no MaterialLabel->Coeff_active_source morphism, each active-source C_X paired to material reentry is zero; hence the active-source material product vanishes. | The 4583 material tail loses its parent material tensor dot coefficient term in the private branch. Empirical material tensors remain required only for rejected/nonstandard branches or test readout inventory. | PRIVATE_BRANCH_ZERO_NOT_GLOBAL | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\463-PPC4161-GR-parity-source-universality-to-local-PPN-residual-vector-or-material-values.md | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | MAT4584_2_finite_material_fallback | If source-universality is rejected, the finite material branch is Delta_C_AB=sum_j Delta_s_AB,j b_j with no cancellation credit. | 4465 gives C_A=C_common+sum_j s_Aj b_j and Delta_C_AB=sum_j(s_Aj-s_Bj)b_j. The older R_material_X formula is the same role in a parent response basis: R_material_X(A,B)=partial_X ln M_A-partial_X ln M_B after common-mode projection. | Rejected branches need source-backed sensitivity vectors, parent b_j/C_X coefficients, range/profile/readout projection and units before WEP/clock/orbital scoring. | FALLBACK_OPERATOR_READY_VALUES_MISSING | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\481-PPC4161-source-charge-universality-zero-proof-or-WEP-material-vector-runner.md | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | MAT4584_3_public_firewall | This does not derive the Standard Model, internal constants, numerical material tensors, or public local GR. | The branch is a private GR-parity import/source-universality adoption. Strict motion-time-space primitive derivation and source-backed material/R_eq empirical values remain open in 4446/4447. | Material zero may be used only as a private local packet reduction; public claims require primitive derivation or empirical bound closure. | PUBLIC_CLAIM_BLOCK_RETAINED | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\462-PPC4161-adopt-GR-parity-SM-import-or-source-backed-material-Req-value.md | 2026-07-06T12:36:50.844132+00:00 | False |

## Apparatus theorem rows

| checkpoint | theorem_id | claim | derivation | consequence | status | source | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4584 | APP4584_0_apparatus_domain_law | Apparatus support is zero only when it is either included in the Hilbert source/reference before variation or disjoint postprocessing outside the fixed collar. | 4580 already gives fixed support/domain zero for compact no-flux collars, but CDG4580_2 keeps apparatus declaration open. The missing declaration is a branch selector: included-in-source, disjoint-postprocessing, or active apparatus. | C_apparatus is not silently erased by C_support=0; it closes only with an explicit apparatus-domain declaration. | DOMAIN_LAW_DERIVED_DECLARATION_REQUIRED | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4580_CLOSED_DOMAIN_GUARDS.csv | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | APP4584_1_included_source_zero | C_apparatus=0 when apparatus stress/energy is inside the same Hilbert source or fixed reference branch before variation. | If T_app is part of T_total^H and the source charge/reference H_ref is fixed before readout, apparatus energy is source content or common reference, not a post-readout coupling multiplier. | Included apparatus does not create a separate readout tail; it changes the declared source model/reference instead. | CONDITIONAL_ZERO_BRANCH | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | APP4584_2_disjoint_postprocessing_zero | C_apparatus=0 when apparatus is disjoint from W_loc and readout is pure postprocessing with no boundary flux. | For supp(T_app) cap W_loc=empty, Pi_app fixed before variation, no sector pullback, and no normal flux across the collar, O_f Pi_app=0 and the apparatus has no local source-probe derivative. | A purely external/postprocessing apparatus contributes no local readout source tail in the fixed no-flux branch. | CONDITIONAL_ZERO_BRANCH | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | APP4584_3_active_apparatus_bound | Active apparatus remains a bound row. | If apparatus mass/fields, calibration current, thermal/EM flux, moving support, or post-fit selector enters W_loc or S_eff, retain C_apparatus <= K_app M_app_eff/M_H_ref + Phi_app/M_H_ref + R_app_selector. | Active apparatus cannot be cancelled against material, EM, kernel, EFT or tau rows. | BOUND_SCHEMA_DERIVED_VALUES_MISSING | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4580_CLOSED_DOMAIN_GUARDS.csv | 2026-07-06T12:36:50.844132+00:00 | False |

## Reduction rows

| checkpoint | row_id | target | formula | branch_condition | status | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4584 | MAR4584_0_material_active_source_zero | sum_X |C_X R_material_X| | sum_X |C_X R_material_X|=0 | PPC4161 private GR-parity source-universality branch; Hom(MaterialLabel,Coeff_active_source)=empty; source-label forgetting; material projections are readout inventory only | PRIVATE_BRANCH_ZERO_NONCLAIM | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | MAR4584_1_Capparatus_domain_zero | C_apparatus | C_apparatus=0 | apparatus included in same Hilbert source/reference before variation OR disjoint postprocessing outside fixed no-flux collar | CONDITIONAL_ZERO_BRANCH_DECLARATION_REQUIRED | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | MAR4584_2_Cmaterial_tail_strict_zero | C_material_tail | C_material_tail=0 | 4583 fixed EM tail zero plus MAT4584_1 material source-weight zero plus APP4584_1/2 apparatus zero | PRIVATE_STRICT_BRANCH_ZERO_NONCLAIM | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | MAR4584_3_Creadout_update | C_readout | C_readout <= C_kernel_active + C_EFT_active + C_tau_tail | strict fixed EM + source-universal material + declared apparatus-zero branch | C_READOUT_REDUCED_TO_KERNEL_EFT_TAU | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | MAR4584_4_fallback_open_branch | C_readout_open | C_readout <= Xi_src_hidden_material + C_apparatus_active + C_EM_tail + C_kernel_active + C_EFT_active + C_tau_tail | source-universality rejected, apparatus active, or open/dynamic EM branch | OPEN_BRANCH_BOUND_SCHEMA_VALUES_MISSING | 2026-07-06T12:36:50.844132+00:00 | False |

## Fallback bound schema

| checkpoint | bound_id | symbol | definition | formula | status | source_anchor | numeric_value_present | source_backed | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4584 | BND4584_0_Xi_material_hidden | Xi_src_hidden_material | hidden source/material prefactor budget feeding material reentry | Xi_src_hidden or source-backed subvector | MISSING_NO_HIDDEN_SLOT_SIGNATURE_OR_NUMERIC_TAILS | F4324_0_master_tail | False | False | False | False | 2026-07-06T12:36:50.844132+00:00 |
| 4584 | BND4584_1_material_sensitivity | Delta_s_AB,j | finite material sensitivity vector in rejected branch | Delta_C_AB=sum_j Delta_s_AB,j b_j | MISSING_SOURCE_BACKED_MATERIAL_SENSITIVITY_VECTOR | DER4465_1_composite_decomposition | False | False | False | False | 2026-07-06T12:36:50.844132+00:00 |
| 4584 | BND4584_2_parent_coeff | b_j or C_X | parent coefficient multiplying material response | |C_X R_material_X| with units/source path | MISSING_PARENT_COEFFICIENT_VECTOR | WMI1894_4_parent_coefficient_dependency | False | False | False | False | 2026-07-06T12:36:50.844132+00:00 |
| 4584 | BND4584_3_apparatus_active | C_apparatus_active | active apparatus/readout support tail | K_app M_app_eff/M_H_ref + Phi_app/M_H_ref + R_app_selector | MISSING_APPARATUS_DOMAIN_DECLARATION_OR_BOUND | CDG4580_2_apparatus | False | False | False | False | 2026-07-06T12:36:50.844132+00:00 |
| 4584 | BND4584_4_common_mode | C_common | composition-blind common source mode | routes to R10/PPN/orbital common-mode bounds, not WEP material tensor | COMMON_MODE_R10_PPN_ORBITAL_PRESSURE_RETAINED | DEC4465_1_common_mode_result | False | False | False | False | 2026-07-06T12:36:50.844132+00:00 |
| 4584 | BND4584_5_total_open | C_material_apparatus_open | absolute fallback material/apparatus tail | |Xi_src_hidden_material|+|C_apparatus_active| | SCHEMA_READY_VALUES_MISSING | MAR4584_4_fallback_open_branch | False | False | False | False | 2026-07-06T12:36:50.844132+00:00 |

## Controls

| checkpoint | control_id | case | expected_result | status | generated_utc | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4584 | CTRL4584_material_inventory | material composition changes mass/readout inventory | do not turn inventory into active source coefficient | CONTROL_PASS | 2026-07-06T12:36:50.844132+00:00 | False | False |
| 4584 | CTRL4584_private_import | GR-parity standard matter import is private branch adoption | do not claim strict MTS primitive derivation | FIREWALL_PASS | 2026-07-06T12:36:50.844132+00:00 | False | False |
| 4584 | CTRL4584_finite_WEP | source-universality rejected | finite material sensitivity vector retained | COUNTERMODEL_CAUGHT | 2026-07-06T12:36:50.844132+00:00 | False | False |
| 4584 | CTRL4584_common_mode | C_A=C_B=C_common nonzero | WEP material differential zero does not imply R10/PPN safety | FIREWALL_PASS | 2026-07-06T12:36:50.844132+00:00 | False | False |
| 4584 | CTRL4584_apparatus_not_support | fixed C_support but undeclared apparatus | C_apparatus remains until included/disjoint declaration or bound | COUNTERMODEL_CAUGHT | 2026-07-06T12:36:50.844132+00:00 | False | False |
| 4584 | CTRL4584_active_apparatus | apparatus flux/mass/support enters source collar | active apparatus bound retained | COUNTERMODEL_CAUGHT | 2026-07-06T12:36:50.844132+00:00 | False | False |

## Promotion gates

| checkpoint | gate_id | gate | status | generated_utc | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 4584 | PROM4584_0_material_active_source | Material active-source weight zero in private source-universality branch. | PASSED_PRIVATE_BRANCH | 2026-07-06T12:36:50.844132+00:00 | False | False |
| 4584 | PROM4584_1_apparatus_zero_contract | Apparatus zero requires included-source or disjoint-postprocessing declaration. | CONDITIONAL | 2026-07-06T12:36:50.844132+00:00 | False | False |
| 4584 | PROM4584_2_Cmaterial_tail | C_material_tail zero only when material and apparatus branches both close. | CONDITIONAL | 2026-07-06T12:36:50.844132+00:00 | False | False |
| 4584 | PROM4584_3_open_material | Rejected/nonstandard material branch requires source-backed material sensitivity vector and parent coefficients. | BLOCKED | 2026-07-06T12:36:50.844132+00:00 | False | False |
| 4584 | PROM4584_4_active_apparatus | Active apparatus branch requires source-backed apparatus support/flux bound. | BLOCKED | 2026-07-06T12:36:50.844132+00:00 | False | False |
| 4584 | PROM4584_5_no_public_claim | No public local-GR/R10/PPN/WEP/clock/orbital claim from 4584. | PASSED_FIREWALL | 2026-07-06T12:36:50.844132+00:00 | False | False |

## Decision

| checkpoint | branch | generated_utc | decision | plain_english | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 4584 | MTS_R2FR_Y5_PARENT_MATERIAL_TENSOR_AND_APPARATUS_SUPPORT_ZERO_OR_BOUND_4584 | 2026-07-06T12:36:50.844132+00:00 | PRIVATE_SOURCE_UNIVERSALITY_KILLS_ACTIVE_MATERIAL_SOURCE_WEIGHT_APPARATUS_DOMAIN_ZERO_OR_BOUND_RETAINED_NONCLAIM | 4584 imports the private GR-parity/source-universality branch to remove active material source weights from C_material_tail, while keeping empirical material tensors as test inventory. Apparatus support is sharpened into an included-source/disjoint-postprocessing zero contract or an active apparatus bound. In the strict branch C_readout is reduced to active kernel, EFT and tau tails. | False | False |

## Next target

| checkpoint | branch | generated_utc | next_target | reason | derive_first | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4584 | MTS_R2FR_Y5_PARENT_MATERIAL_TENSOR_AND_APPARATUS_SUPPORT_ZERO_OR_BOUND_4584 | 2026-07-06T12:36:50.844132+00:00 | 4585-Y5-R2FR-active-kernel-first-zero-or-operator-bound.md | After fixed EM, material source weights, and apparatus support are closed in the strict branch, the leading live C_readout term is C_kernel_active. | prove the active source/readout kernels are fixed q-basic, same-source, or projector-natural zero rows | fill explicit operator-norm bounds for source_worldtube, WEP, clock, light, orbital_GM and projective kernels | False |

## Source register

| checkpoint | source_id | path | path_exists | needle | needle_found | role | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4584 | SRC4584_00_4583_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4583-Y5-R2FR-charge-current-normalization-and-EM-readout-tail-owner-or-source-bound.md | True | C_material_tail <= sum_X |C_X R_material_X| + |C_apparatus| | True | 4583 reduced handoff | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | SRC4584_01_4583_tail | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4583_EM_TAIL_REDUCTION_ROWS.csv | True | ETR4583_1_material_tail_fixed_branch_update | True | 4583 material/apparatus live row | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | SRC4584_02_4583_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4583_NEXT_TARGET.csv | True | parent-material-tensor-and-apparatus-support-zero-or-bound | True | 4583 selected 4584 | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | SRC4584_03_4446_adoption | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\462-PPC4161-adopt-GR-parity-SM-import-or-source-backed-material-Req-value.md | True | ADOPT4446_2_material_reentry_killed | True | GR-parity material reentry killed | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | SRC4584_04_4447_ppn | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\463-PPC4161-GR-parity-source-universality-to-local-PPN-residual-vector-or-material-values.md | True | source-universality pieces of the local residual vector are zero | True | source-universality propagation | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | SRC4584_05_4465_source_charge | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\481-PPC4161-source-charge-universality-zero-proof-or-WEP-material-vector-runner.md | True | Delta_C_AB=0 | True | source-charge differential theorem | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | SRC4584_06_material_intake | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1894_WEP_MATERIAL_TENSOR_INTAKE_NONCLAIM.csv | True | WMI1894_3_full_parent_tensor | True | material tensor intake blocker | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | SRC4584_07_material_basis | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1895_PARENT_MATERIAL_TENSOR_BASIS_NONCLAIM.csv | True | PMTB1895_3_tensor_formula | True | parent material tensor formula | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | SRC4584_08_typing_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1895_SOURCE_PREFACTOR_TYPING_GATE.csv | True | TYP1895_1_no_species_to_source_coeff | True | no material/species source morphism gate | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | SRC4584_09_hidden_tail | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4324_MASTER_TAIL_FORMULAS.csv | True | Xi_src_hidden | True | hidden source-prefactor fallback budget | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | SRC4584_10_no_hidden_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4324_NO_HIDDEN_SLOT_AUDIT.csv | True | AUD4324_3_zero | True | conditional no-hidden-slot zero | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | SRC4584_11_boundary_collar | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md | True | Dq_boundary_projector = 0 | True | fixed collar/domain support law | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | SRC4584_12_apparatus_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4580_CLOSED_DOMAIN_GUARDS.csv | True | CDG4580_2_apparatus | True | apparatus declaration guard | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | SRC4584_13_domain_cert | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4580_PI_READOUT_DOMAIN_CERTIFICATE.csv | True | PDC4580_1_fixed_qbasic_domain | True | fixed support/domain certificate | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | SRC4584_14_Csupport | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4580_CREADOUT_REDUCTION_ROWS.csv | True | CRV4580_1_C_support | True | support zero source | 2026-07-06T12:36:50.844132+00:00 | False |
| 4584 | SRC4584_15_claim_425 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\02-claims-register.csv | True | L-425 | True | prior claim register handoff | 2026-07-06T12:36:50.844132+00:00 | False |
