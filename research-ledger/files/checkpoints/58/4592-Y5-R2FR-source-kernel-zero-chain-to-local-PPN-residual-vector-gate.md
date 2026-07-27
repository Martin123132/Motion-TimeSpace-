# 4592 - Source-kernel zero chain to local PPN residual vector gate

Marker: `PPC4161_SOURCE_KERNEL_ZERO_CHAIN_TO_LOCAL_PPN_RESIDUAL_VECTOR_GATE_4592`  
Branch: `MTS_R2FR_Y5_SOURCE_KERNEL_ZERO_CHAIN_TO_LOCAL_PPN_RESIDUAL_VECTOR_GATE_4592`  
Generated: `2026-07-06T13:29:45.483821+00:00`  
Public claim: `False`

## Result

4592 takes the strict source-worldtube result from 4591 and puts it where it matters: inside the local Newton/PPN residual vector.

The clean decomposition is:

```text
Delta_PPN =
  Delta_PPN^EH/EFT
  + Delta_PPN^source_kernel
  + Delta_PPN^boundary
  + Delta_PPN^projector
  + Delta_PPN^material
  + Delta_PPN^empirical.
```

The source-kernel piece is:

```text
Delta_PPN^source_kernel = Pi_PPN^K C_K_source_worldtube.
```

The 4587-4591 strict chain gives:

```text
C_K_source_worldtube = 0
=> Delta_PPN^source_kernel = 0.
```

That is a real forward step. It removes a whole subvector from the local Newton/PPN problem. But it is not full local GR:

```text
Delta_PPN != 0 by theorem
```

until the non-source survivor rows are also zero or source-backed below bounds.

If the source-kernel branch reopens:

```text
|Delta_PPN^source_kernel|
<= ||Pi_PPN^K|| L_K_source
   (E_rho_qbasic + E_boundary_birth + E_Dq_source
    + E_tau_eobs + E_Href + E_readout_mask + E_EM_flux).
```

## Integration theorem

| checkpoint | theorem_id | claim | derivation | consequence | status | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4592 | INT4592_0_residual_decomposition | The local Newton/PPN residual vector can be split into a source-kernel subvector plus non-source survivor subvectors. | Write Delta_PPN = Delta_PPN^EH/EFT + Delta_PPN^source_kernel + Delta_PPN^boundary + Delta_PPN^projector + Delta_PPN^material + Delta_PPN^empirical. The source-kernel piece is linear at this gate: Delta_PPN^source_kernel = Pi_PPN^K C_K_source_worldtube. | A strict source-kernel zero removes only Pi_PPN^K C_K_source_worldtube, not the other subvectors. | PPN_DECOMPOSITION_WRITTEN_NO_CANCELLATION | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | INT4592_1_strict_source_kernel_subvector_zero | The 4587-4591 strict chain sets the source-kernel contribution to the local PPN residual vector to zero. | 4591 gives C_K_source_worldtube=0 when the density/Poynting, support-boundary, denominator, Dq-source, readout-mask and tau/e_obs clauses all fire. Therefore Delta_PPN^source_kernel = Pi_PPN^K*0 = 0 for every PPN arena row. | source-kernel pieces of gamma, beta, alpha_i, xi, zeta_i, Gdot/G, clock/orbital/WEP/R10 side channels are removable inside the private strict branch. | SOURCE_KERNEL_SUBVECTOR_ZERO_PRIVATE_NONCLAIM | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | INT4592_2_open_branch_bound | If any source-kernel clause reopens, its PPN contribution is an explicit projection bound. | |Delta_PPN^source_kernel| <= ||Pi_PPN^K|| L_K_source*(E_rho_qbasic+E_boundary_birth+E_Dq_source+E_tau_eobs+E_Href+E_readout_mask+E_EM_flux). | The fallback remains scoreable without hiding the source kernel in calibrated G or orbital GM. | OPEN_SOURCE_KERNEL_PPN_BOUND_READY_VALUES_MISSING | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | INT4592_3_survivor_firewall | Source-kernel zero is not a local-GR pass. | Formal 188/294/295/463 and the 3110/3915 PPN-vector discipline retain EH principal/IR selector, residual EFT, cGamma, curvature-square, torsion, Lambda, nonEH/R11, material values and empirical projection rows. | Public promotion requires every survivor row to be parent-zero or source-backed below its arena bound. | SURVIVORS_RETAINED_NO_PUBLIC_CLAIM | 2026-07-06T13:29:45.483821+00:00 | False |

## PPN impact rows

| checkpoint | impact_id | observable | removed_source_kernel_piece | strict_branch_effect | still_not_removed | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4592 | PPN4592_0_Newton_source | Newton/G_cal source normalization | source-kernel monopole/readout dressing | zero on strict chain | calibrated universal G remains allowed; numeric G not predicted; EH operator and survivor rows still required | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | PPN4592_1_gamma | gamma-1 | source-support active-kernel shape contribution | zero on strict chain | spatial curvature/EH principal block, c_D/c_R2/cGamma tails still possible | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | PPN4592_2_beta | beta-1 | source-kernel nonlinear/source-dressing leakage | zero on strict chain | second-order EH stability, binding/stabilizer and residual EFT tails still possible | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | PPN4592_3_alpha_i | alpha1/alpha2/alpha3 | source-frame active-kernel vector/momentum leakage | zero on strict chain | preferred-frame/projector/boundary/torsion/cGamma survivors still possible | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | PPN4592_4_xi | xi | source-kernel preferred-location/external coupling leakage | zero on strict chain | boundary/local Lambda/cGamma/external-field survivor rows still possible | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | PPN4592_5_zeta_i | zeta1-zeta4 | source-exchange/double-counted Hilbert current leakage | zero on strict chain | EFT divergence, EM deformation, boundary flux and conservation rows still possible | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | PPN4592_6_Gdot | Gdot/G | source-kernel/source-measure time drift | zero on strict chain | delta_kappa, cGamma D_t Xi_0 and clock-readout survivor rows still possible unless separately closed | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | PPN4592_7_R10_clock_WEP_orbital | R10/clocks/WEP/orbital side arenas | source-worldtube active-kernel contaminant | zero on strict chain | arena projection coefficients, full R10 curve, material/R_eq and survivor coefficients remain nonclaim | False | False | 2026-07-06T13:29:45.483821+00:00 |

## Survivor blocker map

| checkpoint | survivor_id | residual_family | observable_targets | status_after_source_kernel_zero | next_action | blocker_class | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4592 | SURV4592_0_EH_principal | EH principal / Palatini IR selector | gamma,beta,Newton operator | conditional/private branch, not public parent adoption | derive/adopt parent selector or retain effective-GR label | ACTIVE_PUBLIC_BLOCKER | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | SURV4592_1_cGamma | c_Gamma local memory coupling | Gdot/G, xi, alpha3, R10/clock/orbital profiles | finite survivor | derive memory support/projector zero or fill cGamma/profile coefficients | ACTIVE_BOUND_OR_THEOREM_BLOCKER | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | SURV4592_2_cR2_MR | c_R2/M_R finite-range tail | R10, gamma/beta, orbital precession | finite survivor | derive parent mass gap or source-backed finite-range bounds | ACTIVE_BOUND_OR_THEOREM_BLOCKER | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | SURV4592_3_cT_spin | spin/torsion contact channel | preferred-frame, spin-clock, R10/contact, orbital | finite survivor and best next theorem target | prove torsion algebraic/spin-supported/heavy/contact-suppressed or bound it | SELECTED_NEXT_TARGET | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | SURV4592_4_Lambda_eff | Lambda_eff_local / tidal vacuum | xi, local acceleration/tidal terms | finite survivor | show local negligible bound or source cosmology-calibrated row | ACTIVE_BOUND_OR_THEOREM_BLOCKER | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | SURV4592_5_nonEH_R11_material | nonEH/R11/material/R_eq values | alpha_i, xi, WEP/clock/orbital compact rows | empirical/source-backed survivor | fill projection coefficients/material values if derivation route stalls | ACTIVE_EMPIRICAL_BLOCKER | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | SURV4592_6_projection_coefficients | arena projection matrices and threshold rows | PPN, R10, clocks, WEP, orbital | not supplied by source-kernel zero | source Pi_PPN/Pi_R10/Pi_clock/Pi_orbital rows and bounds | ACTIVE_EMPIRICAL_BLOCKER | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | SURV4592_7_global_parent_adoption | global/public parent adoption | all public claims | not proved | assemble parent-action signatures or keep branch private/nonclaim | PUBLIC_CLAIM_BLOCKER | False | False | 2026-07-06T13:29:45.483821+00:00 |

## Controls

| checkpoint | control_id | scenario | expected_result | status | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4592 | CTRL4592_clean_strict_chain | all 4587-4591 source-kernel clauses active | Delta_PPN^source_kernel=0 but Delta_PPN full vector remains gated by survivors | SYMBOLIC_CONTROL_PASS | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | CTRL4592_gamma_smuggling | claim gamma=1 solely from source-kernel zero | reject; EH principal/spatial curvature and EFT rows still required | COUNTERMODEL_CAUGHT | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | CTRL4592_cGamma_survives | c_Gamma profile row finite or unsigned | retain Gdot/xi/alpha3/R10/clock/orbital survivor channels | COUNTERMODEL_CAUGHT | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | CTRL4592_torsion_survives | c_T_spin finite or unsigned | retain preferred-frame/spin-clock/contact rows | COUNTERMODEL_CAUGHT | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | CTRL4592_open_source_kernel | any source-kernel clause reopens | use ||Pi_PPN^K|| L_K_source sum(E_i) fallback | BOUND_BRANCH_PASS | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | CTRL4592_calibrated_G | numeric Newton G not derived | allowed as calibrated universal coupling but not as source-kernel/PPN proof | FIREWALL_PASS | False | False | 2026-07-06T13:29:45.483821+00:00 |

## Promotion gates

| checkpoint | gate_id | gate | status | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4592 | PROM4592_0_sources_exist | Every cited source path exists and source needles are present. | PASS | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | PROM4592_1_source_kernel_integrated | C_K_source_worldtube=0 is propagated into Delta_PPN^source_kernel=0. | PASS | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | PROM4592_2_survivors_retained | Residual EFT and non-source survivor rows are retained. | PASS | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | PROM4592_3_no_full_ppn_claim | No full R_PPN=0 public claim is made. | PASS | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | PROM4592_4_open_branch_bound | If source-kernel clauses reopen, projection-bound fallback is explicit. | PASS | False | False | 2026-07-06T13:29:45.483821+00:00 |
| 4592 | PROM4592_5_next_derivation | c_T_spin torsion/contact branch selected as the next clean theorem target. | PASS | False | False | 2026-07-06T13:29:45.483821+00:00 |

## Decision

| checkpoint | branch | generated_utc | decision | summary | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 4592 | MTS_R2FR_Y5_SOURCE_KERNEL_ZERO_CHAIN_TO_LOCAL_PPN_RESIDUAL_VECTOR_GATE_4592 | 2026-07-06T13:29:45.483821+00:00 | SOURCE_KERNEL_SUBVECTOR_REMOVED_FROM_LOCAL_PPN_VECTOR_SURVIVORS_RETAINED_NONCLAIM | 4592 integrates the strict 4587-4591 source-worldtube kernel zero chain into the local Newton/PPN residual vector. The removable piece is Delta_PPN^source_kernel = Pi_PPN^K C_K_source_worldtube, so C_K_source_worldtube=0 kills only that subvector. The full local-GR/PPN claim remains blocked by EH principal/IR selector status, c_Gamma, c_R2/M_R, c_T_spin, Lambda_eff, nonEH/R11/material values, projection coefficients and public parent adoption. c_T_spin is selected as the next clean derivation target. | False | False |

## Next target

| checkpoint | branch | generated_utc | next_target | reason | derive_first | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4592 | MTS_R2FR_Y5_SOURCE_KERNEL_ZERO_CHAIN_TO_LOCAL_PPN_RESIDUAL_VECTOR_GATE_4592 | 2026-07-06T13:29:45.483821+00:00 | 4593-Y5-R2FR-cT-spin-torsion-zero-or-contact-bound-after-source-kernel-closure.md | After source-kernel zero, the cleanest remaining local-GR theorem target in the survivor set is the torsion/spin contact channel c_T_spin. | prove torsion is auxiliary/algebraic and sourced only by microscopic spin current, hence zero/contact-suppressed for spinless macroscopic local branches | write preferred-frame, spin-clock, R10/contact and orbital bound rows for finite c_T_spin with no cancellation credit | False |

## Source register

| checkpoint | source_id | path | path_exists | needle | needle_found | role | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4592 | SRC4592_00_4591_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4591-Y5-R2FR-tau-eobs-same-frame-lock-or-source-support-bound.md | True | C_K_source_worldtube = 0 | True | 4591 source-kernel strict zero result | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_01_4591_formal | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\607-PPC4161-tau-eobs-same-frame-lock-or-source-support-bound.md | True | C_K_source_worldtube=0 | True | 607 formal source-kernel zero bridge | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_02_4591_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4591_SOURCE_KERNEL_CLOSURE_UPDATE.csv | True | SKC4591_2_CKsource_strict_zero | True | machine-readable strict source-kernel zero row | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_03_188_ppn | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\188-PPC4161-full-PPN-readout-vector.md | True | R_PPN = | True | private full PPN vector target | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_04_189_empirical | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\189-PPC4161-local-empirical-validation-pack.md | True | R_PPN = 0, | True | private comparator pack warning | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_05_294_left_hand | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\294-PPC4161-left-hand-EH-Newton-limit-or-residual-EFT-bound-gate.md | True | Residual EFT fork | True | left-hand EH/Newton residual fork | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_06_295_survivors | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\295-PPC4161-residual-EFT-coefficient-zero-or-local-test-bound-pack.md | True | survivor / bound subset | True | residual EFT survivor subset | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_07_463_source_univ | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\463-PPC4161-GR-parity-source-universality-to-local-PPN-residual-vector-or-material-values.md | True | does **not** erase non-source residuals | True | source subspace warning | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_08_3110_ppn_vector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3110-Y5-R2FR-local-PPN-residual-vector-from-Eres-and-RHsrc-under-AX1090.md | True | local GR reduction = source-mass bridge + PPN residual vector closure | True | PPN vector projection discipline | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_09_3915_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3915-Y5-R2FR-stationary-local-branch-contract-and-PPN-residual-vector.md | True | Delta_PPN_GR | True | stationary branch PPN promotion gate | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_10_4172_ppn_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4172_PPN_VECTOR_DERIVATION.csv | True | gamma-1=0 | True | private PPN derivation rows | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_11_4172_reactivate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4172_RESIDUAL_CLOSE_OR_REACTIVATE.csv | True | source_backed_empirical_bound_row_required | True | reactivation rule | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_12_4278_eft_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4278_RESIDUAL_EFT_COEFFICIENT_MAP.csv | True | RES4278_3_memory | True | left-hand residual EFT coefficient map | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_13_4279_survivor_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4279_SURVIVOR_BOUND_PACK.csv | True | SURV4279_6_spin_torsion | True | survivor bound pack | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_14_4447_rollup | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4447_RESIDUAL_ROLLUP.csv | True | RU4447_1_full_PPN_vector | True | source subvector not full vector warning | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_15_4448_survivor_map | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4448_SURVIVOR_MAP_OUTPUT.csv | True | SURV4448_7_material_Req_values | True | non-source survivor map | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_16_4555_scorecard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4555_LOCAL_PPN_SCORECARD_REFRESH.csv | True | SC4555_alpha3 | True | local PPN scorecard thresholds | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_17_4561_eft_refresh | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4561_RESIDUAL_EFT_ENVELOPE_REFRESH.csv | True | RE4561_0_cT | True | latest residual EFT envelope refresh | 2026-07-06T13:29:45.483821+00:00 | False |
| 4592 | SRC4592_18_claim_433 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\02-claims-register.csv | True | L-433 | True | claim-register handoff from 4591 | 2026-07-06T13:29:45.483821+00:00 | False |

## Validation

| checkpoint | check_id | status | detail | generated_utc |
| --- | --- | --- | --- | --- |
| 4592 | VAL4592_00_doc_written | PASS | checkpoint doc exists | 2026-07-06T13:29:45.594598+00:00 |
| 4592 | VAL4592_01_formal_written | PASS | formal bridge exists | 2026-07-06T13:29:45.594697+00:00 |
| 4592 | VAL4592_02_marker_doc | PASS | doc marker present | 2026-07-06T13:29:45.594709+00:00 |
| 4592 | VAL4592_03_marker_formal | PASS | formal marker present | 2026-07-06T13:29:45.594718+00:00 |
| 4592 | VAL4592_04_all_sources_exist | PASS | all cited local paths exist | 2026-07-06T13:29:45.594735+00:00 |
| 4592 | VAL4592_05_all_source_needles | PASS | all source needles found | 2026-07-06T13:29:45.594747+00:00 |
| 4592 | VAL4592_csv_P8_Y5_R2FR_4592_SOURCE_REGISTER | PASS | P8_Y5_R2FR_4592_SOURCE_REGISTER.csv parses with rows | 2026-07-06T13:29:45.611667+00:00 |
| 4592 | VAL4592_csv_P8_Y5_R2FR_4592_SOURCE_KERNEL_PPN_INTEGRATION_THEOREM | PASS | P8_Y5_R2FR_4592_SOURCE_KERNEL_PPN_INTEGRATION_THEOREM.csv parses with rows | 2026-07-06T13:29:45.632976+00:00 |
| 4592 | VAL4592_csv_P8_Y5_R2FR_4592_PPN_VECTOR_IMPACT_ROWS | PASS | P8_Y5_R2FR_4592_PPN_VECTOR_IMPACT_ROWS.csv parses with rows | 2026-07-06T13:29:45.648404+00:00 |
| 4592 | VAL4592_csv_P8_Y5_R2FR_4592_SURVIVOR_BLOCKER_MAP | PASS | P8_Y5_R2FR_4592_SURVIVOR_BLOCKER_MAP.csv parses with rows | 2026-07-06T13:29:45.664271+00:00 |
| 4592 | VAL4592_csv_P8_Y5_R2FR_4592_CONTROL_ROWS | PASS | P8_Y5_R2FR_4592_CONTROL_ROWS.csv parses with rows | 2026-07-06T13:29:45.679694+00:00 |
| 4592 | VAL4592_csv_P8_Y5_R2FR_4592_PROMOTION_GATES | PASS | P8_Y5_R2FR_4592_PROMOTION_GATES.csv parses with rows | 2026-07-06T13:29:45.694580+00:00 |
| 4592 | VAL4592_csv_P8_Y5_R2FR_4592_DECISION | PASS | P8_Y5_R2FR_4592_DECISION.csv parses with rows | 2026-07-06T13:29:45.709015+00:00 |
| 4592 | VAL4592_csv_P8_Y5_R2FR_4592_NEXT_TARGET | PASS | P8_Y5_R2FR_4592_NEXT_TARGET.csv parses with rows | 2026-07-06T13:29:45.724427+00:00 |
| 4592 | VAL4592_csv_P8_Y5_R2FR_4592_STATUS | PASS | P8_Y5_R2FR_4592_STATUS.csv parses with rows | 2026-07-06T13:29:45.746157+00:00 |
| 4592 | VAL4592_20_no_generated_claim_true | PASS | generated rows do not promote claims | 2026-07-06T13:29:45.749223+00:00 |
| 4592 | VAL4592_21_ppn_source_kernel_zero_present | PASS | PPN source-kernel zero appears | 2026-07-06T13:29:45.749238+00:00 |
| 4592 | VAL4592_22_open_bound_present | PASS | open source-kernel projection bound appears | 2026-07-06T13:29:45.749247+00:00 |
| 4592 | VAL4592_23_survivors_retained | PASS | survivor rows retained | 2026-07-06T13:29:45.749273+00:00 |
| 4592 | VAL4592_24_next_target_present | PASS | next target appears | 2026-07-06T13:29:45.749283+00:00 |
| 4592 | VAL4592_25_spine_marker | PASS | spine updated once | 2026-07-06T13:29:45.774267+00:00 |
| 4592 | VAL4592_26_packet_marker | PASS | packet updated once | 2026-07-06T13:29:45.793139+00:00 |
| 4592 | VAL4592_27_claim_register | PASS | claim register updated | 2026-07-06T13:29:45.817462+00:00 |
| 4592 | VAL4592_28_no_github_action | PASS | local-only checkpoint; no git push performed | 2026-07-06T13:29:45.817480+00:00 |
| 4592 | VAL4592_29_formal_workbench_updated_only_via_declared_files | PASS | formal updates limited to declared bridge/spine/packet/claim files | 2026-07-06T13:29:45.817739+00:00 |
| 4592 | VAL4592_OVERALL | PASS | 4592 source-kernel to PPN residual vector validation | 2026-07-06T13:29:45.817758+00:00 |
