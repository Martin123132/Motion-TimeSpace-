# 4583 - Charge/current normalization and EM readout tail owner or source bound

Marker: `PPC4161_CHARGE_CURRENT_NORMALIZATION_AND_EM_READOUT_TAIL_OWNER_OR_SOURCE_BOUND_4583`  
Branch: `MTS_R2FR_Y5_CHARGE_CURRENT_NORMALIZATION_AND_EM_READOUT_TAIL_OWNER_OR_SOURCE_BOUND_4583`  
Decision: `FIXED_QBASIC_EM_COUPLING_AND_READOUT_TAIL_ZERO_IMPORTED_OPEN_DYNAMIC_EM_TAIL_BOUND_RETAINED_NONCLAIM`  
Private/public status: private nonclaim; no GitHub action.

## Result

4583 does **not** reinvent the EM coupling result.  It imports the useful fixed-branch theorems already built at 4437/4438 and applies them to the 4582 material/readout tail:

```text
fixed q-basic + same Hodge + post-variation readout
+ no hidden S_eff/readout argument + closed collar no-flux
=> C_JQ = 0,
   C_EM_readout = 0,
   Phi_EM_rad = 0,
   C_EM_tail = 0.
```

Therefore, in that private branch:

```text
C_material_tail <= sum_X |C_X R_material_X| + |C_apparatus|
```

and the local readout envelope reduces to:

```text
C_readout <= sum_X |C_X R_material_X| + |C_apparatus| + C_kernel_active + C_EFT_active + C_tau_tail.
```

This is real progress, but it is not a local-GR claim.  The parent material tensor, apparatus support, active kernels, EFT tails and tau tails still have to close.

## Owner theorem rows

| checkpoint | theorem_id | claim | derivation | consequence | status | source | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4583 | CCO4583_0_rescaling_identity | The EM coupling drift is the owner ratio, not a removable field convention. | S_EM=-lambda_A/4 int F^2 + g_J int A.J; A_c=sqrt(lambda_A)A; alpha_eff proportional to g_J^2/lambda_A; b_alpha=D_X ln alpha_eff=2D_X ln g_J-D_X ln lambda_A. | A -> lambda A only moves normalization between kinetic and current slots. A real relative derivative is physical unless both slots are fixed by the same owner. | EXACT_IDENTITY_IMPORTED | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\225-PPC4161-Maxwell-normalization-charge-current-owner.md | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | CCO4583_1_CJQ_fixed_branch_zero | C_JQ=0 in the fixed q-basic standard visible branch. | If theta_obs={m_A,charges,alpha_EM,hbar,c,material labels}, g_J, lambda_A and readout labels are fixed before variation, and J_matter=J_Maxwell in the same action, then D_X ln g_J=D_X ln lambda_A=0 and deltaJ has no C_JQ component. | The 4582 material tail loses |C_JQ| only inside this private branch; dynamic/global current normalization remains a bound row. | PRIVATE_BRANCH_ZERO_IMPORTED_FROM_4437 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\453-PPC4161-EM-charge-current-unique-F2-owner-or-Kmactionscale-source-value.md | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | CCO4583_2_CEMreadout_strict_zero | C_EM_readout=0 in the strict postprocessing/no-hidden-S_eff branch. | If readout, clocks, spectroscopy, EFT reduction and material labels are post-variation maps with no hidden-field argument slot in S_parent or S_eff, then they cannot regenerate f_X F^2, alpha_X, Hodge readout, or EM binding response as a source coefficient. | The 4582 material tail loses |C_EM_readout| only under the 4438 strict readout-preservation conditions. | PRIVATE_BRANCH_ZERO_IMPORTED_FROM_4438 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4438_TOTAL_EM_ZERO_ROWS.csv | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | CCO4583_3_PhiEM_closed_collar_zero | Phi_EM_rad=0 only for fixed-orientation closed collars with pointwise no radiative/background Poynting flux. | Poynting is Maxwell-Hodge Hilbert stress flux. If P_rad_EM(tau)=0 on the collar boundary, no radiative EM boundary flux enters the local material/readout tail. If flux crosses the collar, it is routed as boundary/Hamiltonian energy, not erased. | The strict fixed branch removes |Phi_EM_rad|; open-radiation branches retain a source-energy or power-normalized bound row. | CLOSED_COLLAR_ZERO_WITH_OPEN_FLUX_FIREWALL | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4438-Y5-R2FR-radiative-readout-EM-closure-or-total-Kmactionscale-source-value.md | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | CCO4583_4_open_dynamic_bound | Open/dynamic EM tails are an absolute no-cancellation residual vector. | C_EM_tail := |C_JQ_dyn|+|C_EM_readout_eff|+|Phi_EM_rad|+|Delta_Hodge_EM|+|C_XF2|+|b_alpha|+|deltaJ_perp|. Ward mismatch obeys ||Delta_Ward|| <= ||F||_inf(|C_JQ| ||J||+||deltaJ_perp||)+||R_Hodge||+||R_Q||+||B_J||. | If any fixed-branch clause fails, the EM tail is retained as a sourced bound schema, never set to zero by convention. | BOUND_SCHEMA_DERIVED_VALUES_MISSING | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\329-PPC4161-EM-Ward-current-normalization-or-collar-residual-bound-values.md | 2026-07-06T12:28:50.995887+00:00 | False |

## Branch gate matrix

| checkpoint | gate_id | branch | fixed_theta_obs | fixed_lambda_A | fixed_g_J | same_current_owner | same_Hodge_owner | readout_after_variation | no_hidden_S_eff_argument | closed_collar_no_flux | result | status | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4583 | BG4583_0_fixed_qbasic_sameHodge_closed_collar | fixed q-basic same-Hodge closed-collar branch | True | True | True | True | True | True | True | True | C_JQ=0; C_EM_readout=0; Phi_EM_rad=0; C_EM_tail=0 | PRIVATE_BRANCH_ZERO_READY_NONCLAIM | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | BG4583_1_dynamic_charge_current | dynamic/global charge-current normalization branch | False | False | False | True | False | False | False | True | C_JQ_dyn retained with Ward/current bound | BOUND_REQUIRED | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | BG4583_2_readout_regeneration | readout/EFT hidden-argument branch | True | True | True | True | True | False | False | True | C_EM_readout_eff retained | BOUND_REQUIRED | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | BG4583_3_open_radiation | open radiative/background Poynting collar | True | True | True | True | True | True | True | False | Phi_EM_rad retained as boundary/Hamiltonian flux | BOUND_REQUIRED | 2026-07-06T12:28:50.995887+00:00 | False |

## Tail reductions

| checkpoint | row_id | target | formula | branch_condition | status | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4583 | ETR4583_0_fixed_branch_EM_tail_zero | C_EM_tail | C_EM_tail=|C_JQ|+|C_EM_readout|+|Phi_EM_rad|+|Delta_Hodge_EM|+|C_XF2|+|b_alpha|+|deltaJ_perp|=0 | fixed q-basic + same Hodge + post-variation readout + no hidden S_eff argument + closed collar no-flux | PRIVATE_BRANCH_ZERO_NONCLAIM | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | ETR4583_1_material_tail_fixed_branch_update | C_material_tail | C_material_tail <= sum_X |C_X R_material_X| + |C_apparatus| | 4582 material owner zero plus 4583 fixed-branch EM tail zero | REDUCED_BOUND_PARENT_MATERIAL_AND_APPARATUS_REMAIN | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | ETR4583_2_Creadout_fixed_branch_update | C_readout | C_readout <= sum_X |C_X R_material_X| + |C_apparatus| + C_kernel_active + C_EFT_active + C_tau_tail | strict fixed EM branch only; active kernels and non-EM/material tails not closed | C_READOUT_REDUCED_NOT_CLOSED | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | ETR4583_3_open_dynamic_branch_update | C_readout_open | C_readout <= sum_X |C_X R_material_X| + |C_apparatus| + C_EM_tail + C_kernel_active + C_EFT_active + C_tau_tail | any dynamic current, hidden readout/EFT argument, Hodge mismatch, or open radiative collar | OPEN_BRANCH_BOUND_SCHEMA_VALUES_MISSING | 2026-07-06T12:28:50.995887+00:00 | False |

## Open/dynamic EM bound schema

| checkpoint | bound_id | symbol | definition | bound_formula | current_status | source_anchor | numeric_value_present | source_backed | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4583 | OBS4583_0_CJQ_dyn | C_JQ_dyn | dynamic charge/current normalization multiplier outside fixed branch | |C_JQ_dyn| <= source-backed current normalization bound | MISSING_DYNAMIC_CURRENT_OWNER_OR_NUMERIC_BOUND | EMB3503_3_C_JQ | False | False | False | False | 2026-07-06T12:28:50.995887+00:00 |
| 4583 | OBS4583_1_deltaJ_perp | deltaJ_perp | current mismatch orthogonal to pure normalization | ||deltaJ_perp||_dual sourced in same collar/current units | MISSING_CURRENT_MISMATCH_NORM | EB4313_0_deltaJ | False | False | False | False | 2026-07-06T12:28:50.995887+00:00 |
| 4583 | OBS4583_2_CEMreadout_eff | C_EM_readout_eff | readout/EFT/spectroscopy regenerated EM coefficient | |C_EM_readout_eff| <= source-backed readout/EFT closure bound | MISSING_READOUT_CLOSURE_OR_BOUND | EMB3503_5_C_EM_readout | False | False | False | False | 2026-07-06T12:28:50.995887+00:00 |
| 4583 | OBS4583_3_PhiEMrad | Phi_EM_rad | open radiative/background Poynting boundary flux | |Phi_EM_rad|/(M_H c^2) or power-window analogue | MISSING_FLUX_OR_CLOSED_COLLAR_ZERO | EMF3502_1_radiative_poynting_flux | False | False | False | False | 2026-07-06T12:28:50.995887+00:00 |
| 4583 | OBS4583_4_DeltaHodge | Delta_Hodge_EM | EM Hodge/constitutive mismatch | ||Delta_Hodge_EM|| <= source-backed same-Hodge residual bound | MISSING_SAME_HODGE_PARENT_SIGNATURE_OR_BOUND | EMB3503_0_Delta_Hodge_EM | False | False | False | False | 2026-07-06T12:28:50.995887+00:00 |
| 4583 | OBS4583_5_CXF2 | C_XF2 | hidden visible F^2/F*F coefficient | |C_XF2| <= parent operator-domain or numeric bound | MISSING_OPERATOR_DOMAIN_EXCLUSION_OR_BOUND | EMB3503_2_C_XF2 | False | False | False | False | 2026-07-06T12:28:50.995887+00:00 |
| 4583 | OBS4583_6_balpha | b_alpha | fine-structure/coupling drift | |2Dln g_J-Dln lambda_A| <= sourced drift bound | MISSING_ALPHA_LEVEL_OWNER_OR_BOUND | EAC3464_1_alpha_level | False | False | False | False | 2026-07-06T12:28:50.995887+00:00 |
| 4583 | OBS4583_7_CEMtail_abs | C_EM_tail | absolute no-cancellation EM tail | sum_abs of the preceding open/dynamic EM rows | SCHEMA_READY_VALUES_MISSING | CCO4583_4_open_dynamic_bound | False | False | False | False | 2026-07-06T12:28:50.995887+00:00 |

## Controls

| checkpoint | control_id | case | expected_result | status | generated_utc | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4583 | CTRL4583_rescale | field rescaling A->lambda A only moves normalization | do not treat convention as physical zero | CONTROL_PASS | 2026-07-06T12:28:50.995887+00:00 | False | False |
| 4583 | CTRL4583_no_alpha_prediction | fixed calibrated alpha_EM branch | no numerical alpha_EM prediction is claimed | FIREWALL_PASS | 2026-07-06T12:28:50.995887+00:00 | False | False |
| 4583 | CTRL4583_dynamic_current | g_J(Phi) or lambda_A(Phi) before variation | C_JQ_dyn retained | COUNTERMODEL_CAUGHT | 2026-07-06T12:28:50.995887+00:00 | False | False |
| 4583 | CTRL4583_hidden_readout | S_eff or readout map has hidden-field argument | C_EM_readout_eff retained | COUNTERMODEL_CAUGHT | 2026-07-06T12:28:50.995887+00:00 | False | False |
| 4583 | CTRL4583_open_flux | nonzero Poynting flux crosses collar | Phi_EM_rad routed as boundary/Hamiltonian flux | FIREWALL_PASS | 2026-07-06T12:28:50.995887+00:00 | False | False |
| 4583 | CTRL4583_nonEM_residuals | EM tail zero alone | does not close parent material tensor, apparatus, active kernel, EFT, tau tails | FIREWALL_PASS | 2026-07-06T12:28:50.995887+00:00 | False | False |

## Promotion gates

| checkpoint | gate_id | gate | status | generated_utc | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 4583 | PROM4583_0_CJQ_fixed | C_JQ zero imported for fixed q-basic branch. | PASSED_PRIVATE_BRANCH | 2026-07-06T12:28:50.995887+00:00 | False | False |
| 4583 | PROM4583_1_CEMreadout_fixed | C_EM_readout zero imported for strict postprocessing/no-hidden-S_eff branch. | PASSED_PRIVATE_BRANCH | 2026-07-06T12:28:50.995887+00:00 | False | False |
| 4583 | PROM4583_2_Phi_closed | Phi_EM_rad zero only on closed collar no-flux branch. | PASSED_PRIVATE_BRANCH | 2026-07-06T12:28:50.995887+00:00 | False | False |
| 4583 | PROM4583_3_open_dynamic | Open/dynamic EM bound rows require sourced values. | BLOCKED | 2026-07-06T12:28:50.995887+00:00 | False | False |
| 4583 | PROM4583_4_nonEM_tail | Parent material tensor, apparatus, active kernel, EFT and tau tails still block local-GR claim. | BLOCKED | 2026-07-06T12:28:50.995887+00:00 | False | False |
| 4583 | PROM4583_5_no_public_claim | No local-GR/R10/PPN/Maxwell/public claim from 4583. | PASSED_FIREWALL | 2026-07-06T12:28:50.995887+00:00 | False | False |

## Decision

| checkpoint | branch | generated_utc | decision | plain_english | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 4583 | MTS_R2FR_Y5_CHARGE_CURRENT_NORMALIZATION_AND_EM_READOUT_TAIL_OWNER_OR_SOURCE_BOUND_4583 | 2026-07-06T12:28:50.995887+00:00 | FIXED_QBASIC_EM_COUPLING_AND_READOUT_TAIL_ZERO_IMPORTED_OPEN_DYNAMIC_EM_TAIL_BOUND_RETAINED_NONCLAIM | 4583 imports the already-derived fixed-branch C_JQ=0 and C_EM_readout=0 results, adds the closed-collar Phi_EM_rad=0 guard, and reduces the 4582 material/readout envelope. Open radiation, hidden readout/EFT regeneration and dynamic/global current branches remain explicit bound rows. | False | False |

## Next target

| checkpoint | branch | generated_utc | next_target | reason | derive_first | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4583 | MTS_R2FR_Y5_CHARGE_CURRENT_NORMALIZATION_AND_EM_READOUT_TAIL_OWNER_OR_SOURCE_BOUND_4583 | 2026-07-06T12:28:50.995887+00:00 | 4584-Y5-R2FR-parent-material-tensor-and-apparatus-support-zero-or-bound.md | After the fixed-branch EM terms are removed, the leading non-EM material/readout debt is the parent material tensor dot coefficient vector plus apparatus support. | prove R_material_X*C_X=0 or apparatus support zero by parent source-domain ownership | source finite parent material tensor and apparatus/readout support bounds without cancellation credit | False |

## Source register

| checkpoint | source_id | path | path_exists | needle | needle_found | role | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4583 | SRC4583_00_4582_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4582-Y5-R2FR-material-response-tail-and-active-kernel-first-bound-or-owner-zero.md | True | C_material_tail | True | 4582 material tail handoff | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | SRC4583_01_4582_tail | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4582_MATERIAL_TAIL_REDUCTION_ROWS.csv | True | MTR4582_3_Creadout_update | True | 4582 C_readout update | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | SRC4583_02_4582_decision | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4582_DECISION.csv | True | C_JQ | True | 4582 surviving EM/material terms | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | SRC4583_03_4582_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4582_NEXT_TARGET.csv | True | charge-current-normalization-and-EM-readout-tail | True | 4582 selected 4583 | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | SRC4583_04_225_norm | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\225-PPC4161-Maxwell-normalization-charge-current-owner.md | True | alpha_eff proportional to g_J^2/lambda_A | True | Maxwell normalization identity | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | SRC4583_05_278_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\278-PPC4161-visible-EM-readout-guard-or-charge-normalization-bound.md | True | C_JQ = 0 | True | fixed visible EM readout guard | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | SRC4583_06_329_ward | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\329-PPC4161-EM-Ward-current-normalization-or-collar-residual-bound-values.md | True | CN4313_1_fixed_visible_branch | True | Ward current normalization branch | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | SRC4583_07_4437_formal | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\453-PPC4161-EM-charge-current-unique-F2-owner-or-Kmactionscale-source-value.md | True | ZERO4437_1_C_JQ | True | 4437 fixed branch C_JQ zero | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | SRC4583_08_4438_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4438-Y5-R2FR-radiative-readout-EM-closure-or-total-Kmactionscale-source-value.md | True | TOTAL_FIXED_BRANCH_EM_PRODUCT_ZERO | True | 4438 total fixed EM zero | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | SRC4583_09_4438_zero | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4438_TOTAL_EM_ZERO_ROWS.csv | True | ZERO4438_1_C_EM_readout | True | 4438 C_EM_readout zero | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | SRC4583_10_4438_survivors | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4438_OPEN_EM_SURVIVOR_ROWS.csv | True | SURV4438_1_readout_regeneration | True | 4438 readout survivor | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | SRC4583_11_Maxwell_Hodge | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md | True | Poynting vector is not a separate background field | True | Poynting/Hilbert stress owner | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | SRC4583_12_EM_CJQ | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv | True | EMB3503_3_C_JQ | True | live C_JQ ledger | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | SRC4583_13_EM_CEMreadout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv | True | EMB3503_5_C_EM_readout | True | live C_EM_readout ledger | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | SRC4583_14_EM_Phi | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_EM_Poynting_source_flux_or_cross_term_vector.csv | True | EMF3502_1_radiative_poynting_flux | True | Poynting flux survivor | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | SRC4583_15_EM_readout_regen | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_EM_Poynting_source_flux_or_cross_term_vector.csv | True | EMF3502_6_readout_radiative_regeneration | True | readout regeneration survivor | 2026-07-06T12:28:50.995887+00:00 | False |
| 4583 | SRC4583_16_claim_424 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\02-claims-register.csv | True | L-424 | True | prior claim register handoff | 2026-07-06T12:28:50.995887+00:00 | False |
