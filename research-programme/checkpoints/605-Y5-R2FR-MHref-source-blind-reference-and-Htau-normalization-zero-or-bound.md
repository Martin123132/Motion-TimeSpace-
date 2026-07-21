# 4589 - MHref source-blind reference and Htau normalization zero or bound

Marker: `PPC4161_MHREF_SOURCE_BLIND_REFERENCE_AND_HTAU_NORMALIZATION_ZERO_OR_BOUND_4589`  
Branch: `MTS_R2FR_Y5_MHREF_SOURCE_BLIND_REFERENCE_AND_HTAU_NORMALIZATION_ZERO_OR_BOUND_4589`  
Decision: `MHREF_QBASIC_DIFFERENCE_AND_SOURCE_BLIND_REFERENCE_ZERO_CONTRACT_DERIVED_POSITIVE_DENOMINATOR_BOUND_RETAINED_NONCLAIM`  
Private/public status: private nonclaim; no GitHub action.

## Result

4589 attacks the denominator/reference component exposed by 4588.

The denominator is:

```text
M_H_ref := H_tau[S_link;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs].
```

If both pieces descend through the same quotient branch:

```text
H_tau=Hbar_tau(q(Phi)),
H_ref=Hbar_ref(q(Phi)),
v in ker(Dq),
```

then:

```text
D_v M_H_ref = 0,
epsilon_MHref = 0.
```

If that is not signed:

```text
epsilon_MHref <= (|D_v H_tau|+|D_v H_ref|)/M_lower.
```

The positive denominator guard is:

```text
M_lower = M_EH*(1-epsilon_abs),  M_EH>0,  epsilon_abs<1.
```

No orbital `GM`, measured `G`, fitted acceleration, or post-readout reference subtraction is allowed to define this denominator.

## MHref theorem

| checkpoint | theorem_id | claim | derivation | consequence | status | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4589 | MHR4589_0_definition | The source-worldtube denominator is the Hamiltonian/Hilbert charge difference, not orbital GM. | M_H_ref := H_tau[S_link;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs]. The same-object route identifies this with the dressed Hilbert worldtube source charge before readout. | Every source-worldtube bound must use the same tau/e_obs/source branch denominator, not a fitted acceleration or orbital mass. | DENOMINATOR_OBJECT_DEFINED | 2026-07-06T13:08:57.465298+00:00 | False |
| 4589 | MHR4589_1_qbasic_difference | If H_tau and H_ref descend through q on the same branch, then M_H_ref is q-basic. | H_tau=Hbar_tau(q(Phi)) and H_ref=Hbar_ref(q(Phi)) imply M_H_ref=Mbar_H_ref(q):=Hbar_tau(q)-Hbar_ref(q). Therefore D_v M_H_ref=dMbar_H_ref(Dq(v))=0 for v in ker(Dq). | E_Href=0 and the M_H_ref part of the source-support bundle is vertically silent on the strict branch. | CONDITIONAL_ZERO_THEOREM_DERIVED_NOT_GLOBAL_PARENT_SIGNED | 2026-07-06T13:08:57.465298+00:00 | False |
| 4589 | MHR4589_2_no_cancellation_bound | If q-basicness is unsigned, denominator drift is bounded without cancellation. | D_v M_H_ref=D_v H_tau-D_v H_ref, so |D_v M_H_ref| <= |D_v H_tau|+|D_v H_ref|. Normalized drift is epsilon_MHref <= (|D_v H_tau|+|D_v H_ref|)/M_lower. | The denominator problem becomes a sourceable H_tau/H_ref/M_lower vector. | BOUND_FORMULA_DERIVED_VALUES_MISSING | 2026-07-06T13:08:57.465298+00:00 | False |
| 4589 | MHR4589_3_positive_denominator_guard | A denominator bound is claim-eligible only with a positive same-frame lower bound. | Use M_H_ref >= M_EH*(1-epsilon_abs). If M_EH>0 and epsilon_abs<1, then M_lower:=M_EH*(1-epsilon_abs)>0. Otherwise normalized local bounds remain blocked. | No source-kernel or local-GR bound may divide by M_H_ref until the lower-bound row is signed or sourced. | POSITIVITY_GUARD_DERIVED_VALUES_MISSING | 2026-07-06T13:08:57.465298+00:00 | False |

## Source-blind reference clauses

| checkpoint | clause_id | clause | zero_condition | current_status | zero_certificate_signed | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4589 | MHC4589_0_same_tau_eobs | H_tau and H_ref use the same tau, coframe, surface branch and units. | same branch object before readout | CONDITIONAL_REQUIRED | False | False | False | 2026-07-06T13:08:57.465298+00:00 |
| 4589 | MHC4589_1_Htau_qbasic | H_tau descends through q. | D_v H_tau=0 for v in ker(Dq) | UNSIGNED_OR_BOUND_REQUIRED | False | False | False | 2026-07-06T13:08:57.465298+00:00 |
| 4589 | MHC4589_2_Href_qbasic | H_ref is source-blind and descends through q. | D_v H_ref=0; no source-dependent counterterm | UNSIGNED_OR_BOUND_REQUIRED | False | False | False | 2026-07-06T13:08:57.465298+00:00 |
| 4589 | MHC4589_3_no_fitted_GM | No orbital GM, acceleration fit or measured G defines H_tau/H_ref/M_H_ref. | anti-circularity guard | FIREWALL_REQUIRED | False | False | False | 2026-07-06T13:08:57.465298+00:00 |
| 4589 | MHC4589_4_positive_lower_bound | M_H_ref has a positive same-frame lower bound. | M_EH>0 and epsilon_abs<1 | MISSING_SOURCE_BACKED_LOWER_BOUND | False | False | False | 2026-07-06T13:08:57.465298+00:00 |
| 4589 | MHC4589_5_integrability | Hamiltonian charge is integrable on the chosen surface family. | curl/symplectic leakage zero or bounded | UNSIGNED_OR_BOUND_REQUIRED | False | False | False | 2026-07-06T13:08:57.465298+00:00 |
| 4589 | MHC4589_6_reference_fixed_before_readout | H_ref is selected before local residuals are inspected. | no fitted subtraction/counterterm | ANTI_TAUTOLOGY_GUARD_REQUIRED | False | False | False | 2026-07-06T13:08:57.465298+00:00 |

## Denominator drift bound rows

| checkpoint | bound_id | symbol | definition | bound_formula | current_status | numeric_value_present | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4589 | MDB4589_0_Dv_Htau | D_v H_tau | vertical derivative of Hamiltonian charge | |D_v H_tau| <= |E_theta|+|E_Qtau|+|E_curl|+|E_surface|+|E_sector|+|E_boundary| | MISSING_PARENT_HTAU_DERIVATIVE | False | False | False | 2026-07-06T13:08:57.465298+00:00 |
| 4589 | MDB4589_1_Dv_Href | D_v H_ref | vertical derivative of reference subtraction | |D_v H_ref| <= |E_ref_selector|+|E_ref_boundary|+|E_ref_frame|+|E_ref_readout| | MISSING_SOURCE_BLIND_HREF_DERIVATIVE | False | False | False | 2026-07-06T13:08:57.465298+00:00 |
| 4589 | MDB4589_2_Dv_MHref | D_v M_H_ref | source-worldtube denominator drift | |D_v M_H_ref| <= |D_v H_tau|+|D_v H_ref| | FORMULA_READY_VALUES_MISSING | False | False | False | 2026-07-06T13:08:57.465298+00:00 |
| 4589 | MDB4589_3_Mlower | M_lower | positive same-frame denominator lower bound | M_lower=M_EH*(1-epsilon_abs), requiring M_EH>0 and epsilon_abs<1 | MISSING_POSITIVE_LOWER_BOUND | False | False | False | 2026-07-06T13:08:57.465298+00:00 |
| 4589 | MDB4589_4_epsilon_MHref | epsilon_MHref | normalized denominator drift | epsilon_MHref <= (|D_v H_tau|+|D_v H_ref|)/M_lower | FORMULA_READY_VALUES_MISSING | False | False | False | 2026-07-06T13:08:57.465298+00:00 |
| 4589 | MDB4589_5_no_fitted_G | delta_Gfit | absorbed fitted-G/orbital-GM contamination | delta_Gfit=0 required; otherwise denominator branch rejected | ANTI_CIRCULARITY_GUARD | False | False | False | 2026-07-06T13:08:57.465298+00:00 |

## Reduction rows

| checkpoint | row_id | target | formula | branch_condition | status | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4589 | MHRD4589_0_EHref_zero | E_Href / epsilon_MHref | D_v M_H_ref=0 and epsilon_MHref=0 | H_tau and H_ref q-basic, source-blind, same tau/e_obs/surface branch, positive lower bound, no fitted GM | CONDITIONAL_ZERO_NOT_PUBLIC_CLAIM | 2026-07-06T13:08:57.465298+00:00 | False |
| 4589 | MHRD4589_1_EHref_bound | epsilon_MHref | epsilon_MHref <= (|D_v H_tau|+|D_v H_ref|)/M_lower | any H_tau/H_ref q-basic or reference source-blind clause unsigned | DENOMINATOR_DRIFT_BOUND_READY_VALUES_MISSING | 2026-07-06T13:08:57.465298+00:00 | False |
| 4589 | MHRD4589_2_CKsource_update | C_K_source_worldtube | strict 4587+4588+4589 branch removes E_rho_qbasic, E_EM_flux, E_boundary_birth and E_Href; remaining blockers are E_Dq_source+E_tau_eobs+E_readout_mask | density/Poynting, support-boundary and denominator zero branches | PARTIAL_SOURCE_KERNEL_REDUCTION_DERIVED | 2026-07-06T13:08:57.465298+00:00 | False |
| 4589 | MHRD4589_3_next_Dq_mask | E_Dq_source and E_readout_mask | prove actual source residual is vertical and readout mask is fixed q-basic, or bound both operator components | next source-worldtube components after denominator lock | SELECTED_NEXT_DERIVATION_TARGET | 2026-07-06T13:08:57.465298+00:00 | False |

## Controls

| checkpoint | control_id | case | expected_result | status | generated_utc | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4589 | CTRL4589_clean_qbasic | H_tau and H_ref both q-basic same branch | D_v M_H_ref=0 | SYMBOLIC_CONTROL_PASS | 2026-07-06T13:08:57.465298+00:00 | False | False |
| 4589 | CTRL4589_fitted_reference | H_ref chosen to cancel a residual after readout | reject zero; retain D_v H_ref/delta_Gfit | COUNTERMODEL_CAUGHT | 2026-07-06T13:08:57.465298+00:00 | False | False |
| 4589 | CTRL4589_orbital_GM | orbital GM or measured G used as denominator input | reject denominator branch | FIREWALL_PASS | 2026-07-06T13:08:57.465298+00:00 | False | False |
| 4589 | CTRL4589_nonintegrable_Htau | Hamiltonian charge has curl/symplectic leakage | retain D_v H_tau bound | FIREWALL_PASS | 2026-07-06T13:08:57.465298+00:00 | False | False |
| 4589 | CTRL4589_zero_denominator | M_lower missing or nonpositive | block normalized claims | COUNTERMODEL_CAUGHT | 2026-07-06T13:08:57.465298+00:00 | False | False |
| 4589 | CTRL4589_no_claim | theorem exists but parent adoption/values missing | no local-GR/R10/PPN claim | FIREWALL_PASS | 2026-07-06T13:08:57.465298+00:00 | False | False |

## Promotion gates

| checkpoint | gate_id | gate | status | generated_utc | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 4589 | PROM4589_0_definition | M_H_ref denominator object defined without orbital GM. | PASSED | 2026-07-06T13:08:57.465298+00:00 | False | False |
| 4589 | PROM4589_1_qbasic_difference | q-basic difference zero theorem derived conditionally. | PASSED_CONDITIONAL | 2026-07-06T13:08:57.465298+00:00 | False | False |
| 4589 | PROM4589_2_no_cancellation | open branch denominator drift bound emitted. | PASSED | 2026-07-06T13:08:57.465298+00:00 | False | False |
| 4589 | PROM4589_3_positive_guard | positive denominator lower-bound guard emitted. | PASSED | 2026-07-06T13:08:57.465298+00:00 | False | False |
| 4589 | PROM4589_4_values | H_tau/H_ref/M_lower clauses or numeric values are source-backed. | BLOCKED | 2026-07-06T13:08:57.465298+00:00 | False | False |
| 4589 | PROM4589_5_no_claim | No local-GR/R10/PPN claim from 4589 alone. | PASSED_FIREWALL | 2026-07-06T13:08:57.465298+00:00 | False | False |

## Decision

| checkpoint | branch | generated_utc | decision | plain_english | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 4589 | MTS_R2FR_Y5_MHREF_SOURCE_BLIND_REFERENCE_AND_HTAU_NORMALIZATION_ZERO_OR_BOUND_4589 | 2026-07-06T13:08:57.465298+00:00 | MHREF_QBASIC_DIFFERENCE_AND_SOURCE_BLIND_REFERENCE_ZERO_CONTRACT_DERIVED_POSITIVE_DENOMINATOR_BOUND_RETAINED_NONCLAIM | 4589 locks the denominator problem into a theorem-or-bound form. If H_tau and H_ref are q-basic on the same tau/e_obs/surface branch and H_ref is source-blind before readout, then M_H_ref is vertically silent. If not, denominator drift is bounded by |D_v H_tau|+|D_v H_ref| over a positive lower bound. Fitted GM/orbital mass is explicitly banned as denominator evidence. | False | False |

## Next target

| checkpoint | branch | generated_utc | next_target | reason | derive_first | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4589 | MTS_R2FR_Y5_MHREF_SOURCE_BLIND_REFERENCE_AND_HTAU_NORMALIZATION_ZERO_OR_BOUND_4589 | 2026-07-06T13:08:57.465298+00:00 | 4590-Y5-R2FR-Dq-source-vertical-basis-and-readout-mask-zero-or-bound.md | After density, support-boundary and denominator components, the remaining source-worldtube kernel blockers are actual verticality and readout-mask fixed-domain status. | prove the source residual direction is genuinely in ker(Dq) and Pi_readout/source mask is fixed q-basic before variation | emit finite E_Dq_source and E_readout_mask rows with operator norms, units, support and no residual-fit masks | False |

## Source register

| checkpoint | source_id | path | path_exists | needle | needle_found | role | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4589 | SRC4589_00_4588_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4588-Y5-R2FR-regular-source-support-boundary-zero-or-Reynolds-shell-bound.md | True | 4589-Y5-R2FR-MHref-source-blind-reference-and-Htau-normalization-zero-or-bound.md | True | 4588 selected MHref target | 2026-07-06T13:08:57.465298+00:00 | False |
| 4589 | SRC4589_01_4588_reduction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4588_SOURCE_KERNEL_REDUCTION_UPDATE.csv | True | RSR4588_3_next_MHref | True | 4588 next denominator reduction | 2026-07-06T13:08:57.465298+00:00 | False |
| 4589 | SRC4589_02_3560_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3560-Y5-R2FR-source-support-qbasic-worldtube-descent-or-bound-vector.md | True | SCL3560_3_MHref_qbasic | True | 3560 MHref q-basic clause | 2026-07-06T13:08:57.465298+00:00 | False |
| 4589 | SRC4589_03_3560_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3560_BOUND_VECTOR.csv | True | BF3560_4_E_Href | True | 3560 Href leakage bound row | 2026-07-06T13:08:57.465298+00:00 | False |
| 4589 | SRC4589_04_3551_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3551_MHREF_DESCENT_THEOREM.csv | True | MHD3551_1_sum_difference_descent | True | 3551 MHref descent theorem | 2026-07-06T13:08:57.465298+00:00 | False |
| 4589 | SRC4589_05_3551_leak | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3551_MHREF_LEAKAGE_BOUND_PACK.csv | True | LB3551_3_normalized_mass_leak | True | 3551 normalized mass leak bound | 2026-07-06T13:08:57.465298+00:00 | False |
| 4589 | SRC4589_06_186_glue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md | True | M_H^dress[W_H;tau] = H_tau[S_link] - H_ref | True | Hamiltonian worldtube mass glue | 2026-07-06T13:08:57.465298+00:00 | False |
| 4589 | SRC4589_07_194_calibration | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md | True | No orbital `GM` | True | calibrated source-coupling anti-circularity | 2026-07-06T13:08:57.465298+00:00 | False |
| 4589 | SRC4589_08_236_positive | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\236-PPC4161-MHref-positive-source-denominator-stability-or-bound-pack.md | True | M_H_ref >= M_EH | True | positive denominator stability law | 2026-07-06T13:08:57.465298+00:00 | False |
| 4589 | SRC4589_09_4170_identity | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4170_SAME_OBJECT_IDENTITY.csv | True | SO4170_1_identity | True | same-object Hamiltonian identity | 2026-07-06T13:08:57.465298+00:00 | False |
| 4589 | SRC4589_10_claim_430 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\02-claims-register.csv | True | L-430 | True | prior claim register handoff | 2026-07-06T13:08:57.465298+00:00 | False |
