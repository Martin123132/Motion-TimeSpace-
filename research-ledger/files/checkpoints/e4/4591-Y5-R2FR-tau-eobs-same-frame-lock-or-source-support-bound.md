# 4591 - Tau/e_obs same-frame lock or source-support bound

Marker: `PPC4161_TAU_EOBS_SAME_FRAME_LOCK_OR_SOURCE_SUPPORT_BOUND_4591`  
Branch: `MTS_R2FR_Y5_TAU_EOBS_SAME_FRAME_LOCK_OR_SOURCE_SUPPORT_BOUND_4591`  
Generated: `2026-07-06T13:23:08.443786+00:00`  
Public claim: `False`

## Result

4591 attacks the last live component left by 4590:

```text
C_K_source_worldtube <= L_K_source * E_tau_eobs.
```

The zero route is exact but conditional. Define one parent-selected observed branch before variation and before comparison:

```text
tau_* = tau_bar(q(Phi)),
e_*   = e_bar(q(Phi)).
```

Then require the same branch everywhere:

```text
tau_source=tau_support=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout=tau_*,
e_source=e_support=e_charge=e_clock=e_EM=e_readout=e_*.
```

For `v_X in ker(Dq)`:

```text
D_v tau_* = D tau_bar[Dq(v_X)] = 0,
D_v e_*   = D e_bar[Dq(v_X)] = 0,
E_tau_eobs = 0.
```

Combined with 4587-4590 strict clauses:

```text
C_K_source_worldtube = 0.
```

This is not a global theory-of-time claim and not a public local-GR claim. It is a private strict-branch source-kernel closure. If a clock, orbital frame, PPN gauge, source support, readout map, surface family, unit convention or private memory time splits from the common branch, the fallback is:

```text
E_tau_eobs <= (
  sum_r L_tau,r ||tau_r-tau_*||
  + sum_r L_e,r ||e_r-e_*||
  + L_S ||Delta S_link||
  + L_units |Delta_units|
  + L_private |R_private_memory_tau|
) / N_Y.
```

## Tau/e_obs theorem

| checkpoint | theorem_id | claim | derivation | zero_condition | consequence | status | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4591 | TE4591_0_common_observed_branch | The source-worldtube frame residual vanishes only when all roles use one parent-selected observed time/coframe branch. | Choose tau_* = tau_bar(q(Phi)) and e_* = e_bar(q(Phi)) before source variation and comparison, then set tau_source=tau_support=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout=tau_* and e_source=e_support=e_charge=e_clock=e_EM=e_readout=e_*. | one q-basic tau/e_obs branch, common units/orientation/normalization, fixed or tau-dragged surfaces and no post-fit frame convention | Delta_tau=0, Delta_e_obs=0 and C_frame=0 for the source-support bundle. | SAME_BRANCH_CONTRACT_DERIVED_NOT_GLOBAL_TIME_THEOREM | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | TE4591_1_chain_rule_zero | The same q-basic tau/e_obs branch is vertically silent. | For v_X in ker(Dq), D_v tau_* = D tau_bar[Dq(v_X)] = 0 and D_v e_* = D e_bar[Dq(v_X)] = 0. Therefore any functional Y_source[tau_*,e_*]=Ybar(q(Phi)) has no tau/e_obs vertical drift. | Dq(v_X)=0 plus common q-basic tau/e_obs branch for source density, support, Hamiltonian charge and readout | E_tau_eobs=0. | CONDITIONAL_ZERO_THEOREM_DERIVED | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | TE4591_2_source_kernel_strict_zero | 4591 closes the last named source-worldtube kernel component on the strict 4587-4591 branch. | 4587 removes E_rho_qbasic/E_EM_flux on the strict branch, 4588 removes E_boundary_birth, 4589 removes E_Href, 4590 removes E_Dq_source/E_readout_mask, and 4591 removes E_tau_eobs. | all strict clauses from 4587 through 4591 are active and selected before readout | C_K_source_worldtube=0 for the strict source-worldtube kernel branch. | STRICT_SOURCE_KERNEL_ZERO_CHAIN_DERIVED_NONCLAIM | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | TE4591_3_operator_bound_fallback | If clocks, source charge, support, PPN or readout use split frames, the mismatch is a finite residual. | E_tau_eobs is bounded by a no-cancellation sum of role differences and selector derivatives, not hidden in a convention choice. | None; this is the fallback when the common branch is unsigned or false. | E_tau_eobs <= (sum_r L_tau,r||tau_r-tau_*|| + sum_r L_e,r||e_r-e_*|| + L_S||delta S_link|| + L_units|delta u| + L_N|delta N|)/N_Y. | BOUND_FORMULA_DERIVED_VALUES_MISSING | 2026-07-06T13:23:08.443786+00:00 | False |

## Frame-mismatch bound rows

| checkpoint | bound_id | symbol | definition | bound_or_status | units | numeric_value_present | source_path | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4591 | FB4591_0_tau_role_split | Delta_tau_roles | differences between tau_source, tau_support, tau_charge, tau_clock, tau_orbit, tau_PPN and tau_readout | MISSING_COMMON_TAU_CERTIFICATE_OR_NORM | time or normalized clock units | False |  | False | False | 2026-07-06T13:23:08.443786+00:00 |
| 4591 | FB4591_1_eobs_role_split | Delta_eobs_roles | coframe/frame differences between source density, EM stress, charge, clock, orbit, PPN and readout | MISSING_COMMON_EOBS_CERTIFICATE_OR_NORM | coframe norm | False |  | False | False | 2026-07-06T13:23:08.443786+00:00 |
| 4591 | FB4591_2_surface_motion | Delta_S_link | linking/support surfaces not fixed or Lie_tau-dragged before readout | MISSING_FIXED_SURFACE_FAMILY_OR_HAUSDORFF_BOUND | surface/Hausdorff norm | False |  | False | False | 2026-07-06T13:23:08.443786+00:00 |
| 4591 | FB4591_3_units_orientation | Delta_units | unit, lapse, orientation or source-normalization mismatch | MISSING_COMMON_UNIT_ORIENTATION_LOCK | dimensionless | False |  | False | False | 2026-07-06T13:23:08.443786+00:00 |
| 4591 | FB4591_4_private_memory_tau | R_private_memory_tau | private process/memory time leaking into observed source/clock/orbit/readout tau | ZERO_IF_INTERNAL_ONLY_OTHERWISE_BOUND_REQUIRED | dimensionless or time norm | False |  | False | False | 2026-07-06T13:23:08.443786+00:00 |
| 4591 | FB4591_5_clock_orbit_postfit | R_clock_orbit_postfit | clock/orbit/PPN convention selected after empirical comparison | REJECT_ZERO_RETAIN_RESIDUAL | dimensionless | False |  | False | False | 2026-07-06T13:23:08.443786+00:00 |
| 4591 | FB4591_6_E_tau_eobs | E_tau_eobs | normalized same-frame tau/eobs source-support leakage | E_tau_eobs <= (sum L_tau||Delta_tau|| + sum L_e||Delta_eobs|| + L_S||Delta_S|| + L_u|Delta_units| + L_N|deltaN|)/N_Y | dimensionless | False |  | False | False | 2026-07-06T13:23:08.443786+00:00 |
| 4591 | FB4591_7_CK_source_open | C_K_source_worldtube | source-worldtube active kernel with frame mismatch retained | C_K_source_worldtube <= L_K_source*E_tau_eobs after strict prior reductions, or full seven-term vector if earlier strict clauses fail | dimensionless or kernel units | False |  | False | False | 2026-07-06T13:23:08.443786+00:00 |

## Source-kernel closure update

| checkpoint | row_id | target | formula | branch_condition | status | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4591 | SKC4591_0_E_tau_eobs_zero | E_tau_eobs | E_tau_eobs=0 | source density, support, Hamiltonian charge, clocks, orbit, PPN, EM stress and readout use the same q-basic tau/e_obs branch with fixed units/surfaces | CONDITIONAL_ZERO_NOT_PUBLIC_CLAIM | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SKC4591_1_E_tau_eobs_bound | E_tau_eobs | E_tau_eobs <= (sum L_tau||Delta_tau|| + sum L_e||Delta_eobs|| + L_S||Delta_S|| + L_units|Delta_units| + L_private|R_private_memory_tau|)/N_Y | split tau/e_obs roles, moving surfaces, post-fit clock/orbit/readout convention or private time leakage | OPERATOR_BOUND_READY_VALUES_MISSING | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SKC4591_2_CKsource_strict_zero | C_K_source_worldtube | strict 4587+4588+4589+4590+4591 branch gives C_K_source_worldtube=0 | all source-kernel component zero contracts active before readout | STRICT_SOURCE_KERNEL_ZERO_CHAIN_DERIVED_NONCLAIM | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SKC4591_3_CKsource_reduced_open | C_K_source_worldtube | C_K_source_worldtube <= L_K_source*E_tau_eobs after strict 4587-4590 reductions | only tau/eobs same-frame lock is unsigned | REDUCED_OPEN_FRAME_BOUND | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SKC4591_4_CKsource_full_open | C_K_source_worldtube | C_K_source_worldtube <= L_K_source*(E_rho_qbasic+E_boundary_birth+E_Dq_source+E_tau_eobs+E_Href+E_readout_mask+E_EM_flux) | any earlier strict source-kernel clause fails | FULL_NO_CANCELLATION_VECTOR_RETAINED | 2026-07-06T13:23:08.443786+00:00 | False |

## Controls

| checkpoint | control_id | scenario | expected_result | status | generated_utc | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4591 | CTRL4591_clean_same_branch | one tau/e_obs branch fixed before variation for source, charge, clocks, orbit, PPN and readout | E_tau_eobs=0 and strict source-kernel branch reaches C_K_source_worldtube=0 | SYMBOLIC_CONTROL_PASS | 2026-07-06T13:23:08.443786+00:00 | False | False |
| 4591 | CTRL4591_clock_after_fit | clock normalization chosen after seeing residuals | reject zero; retain R_clock_orbit_postfit | COUNTERMODEL_CAUGHT | 2026-07-06T13:23:08.443786+00:00 | False | False |
| 4591 | CTRL4591_orbit_frame_split | orbital coordinates use a frame not used by Hilbert source charge | retain Delta_tau_roles/Delta_eobs_roles | COUNTERMODEL_CAUGHT | 2026-07-06T13:23:08.443786+00:00 | False | False |
| 4591 | CTRL4591_private_time_internal | private memory/process time exists but does not enter observed source/readout tau | no observed tau residual from private time alone | FIREWALL_PASS | 2026-07-06T13:23:08.443786+00:00 | False | False |
| 4591 | CTRL4591_private_time_leaks | private memory/process time enters clock/source/orbit/readout definitions | retain R_private_memory_tau | COUNTERMODEL_CAUGHT | 2026-07-06T13:23:08.443786+00:00 | False | False |
| 4591 | CTRL4591_moving_surface | linking surface reselected or moved independently of tau drag | retain Delta_S_link/surface motion row | COUNTERMODEL_CAUGHT | 2026-07-06T13:23:08.443786+00:00 | False | False |
| 4591 | CTRL4591_units_lapse_split | source and readout use different lapse/unit/orientation normalization | retain Delta_units and reject denominator/source-kernel promotion | COUNTERMODEL_CAUGHT | 2026-07-06T13:23:08.443786+00:00 | False | False |

## Promotion gates

| checkpoint | gate_id | gate | status | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4591 | PROM4591_0_sources_exist | Every cited 4590/3560/232/285/4216/4269/3558/3249/4580 source exists. | PASS | False | False | 2026-07-06T13:23:08.443786+00:00 |
| 4591 | PROM4591_1_tau_eobs_theorem | Same tau/e_obs chain-rule zero theorem derived. | PASSED_CONDITIONAL | False | False | 2026-07-06T13:23:08.443786+00:00 |
| 4591 | PROM4591_2_frame_bound | Split-frame fallback bound rows are explicit and no-cancellation. | PASS | False | False | 2026-07-06T13:23:08.443786+00:00 |
| 4591 | PROM4591_3_source_kernel_zero_chain | Strict source-worldtube kernel zero chain is written but nonclaim. | PASS | False | False | 2026-07-06T13:23:08.443786+00:00 |
| 4591 | PROM4591_4_no_global_time_claim | No global theory of time or public local-GR claim is promoted. | PASS | False | False | 2026-07-06T13:23:08.443786+00:00 |
| 4591 | PROM4591_5_next_gate | Next target assembles source-kernel zero into local PPN residual-vector gate. | PASS | False | False | 2026-07-06T13:23:08.443786+00:00 |

## Decision

| checkpoint | branch | generated_utc | decision | summary | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 4591 | MTS_R2FR_Y5_TAU_EOBS_SAME_FRAME_LOCK_OR_SOURCE_SUPPORT_BOUND_4591 | 2026-07-06T13:23:08.443786+00:00 | TAU_EOBS_SOURCE_CHARGE_READOUT_FRAME_LOCK_DERIVED_SOURCE_KERNEL_STRICT_ZERO_RETAINED_NONCLAIM | 4591 derives the same-frame tau/e_obs lock needed by the 4590 source-kernel reduction. If one q-basic observed tau and coframe define source density, support, Hamiltonian charge, clocks, orbit, PPN, EM stress and readout before variation, then E_tau_eobs=0. Combined with 4587-4590 strict clauses, the source-worldtube active-kernel branch reaches C_K_source_worldtube=0. Split clocks, frames, surfaces, units or private-time leakage remain finite bound rows. No local-GR claim is promoted. | False | False |

## Next target

| checkpoint | branch | generated_utc | next_target | reason | derive_first | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4591 | MTS_R2FR_Y5_TAU_EOBS_SAME_FRAME_LOCK_OR_SOURCE_SUPPORT_BOUND_4591 | 2026-07-06T13:23:08.443786+00:00 | 4592-Y5-R2FR-source-kernel-zero-chain-to-local-PPN-residual-vector-gate.md | The source-worldtube active-kernel chain now has a strict zero route; the next useful move is to assemble it into the wider local PPN/Newton residual vector and identify which non-source-kernel components still block a claim. | propagate the strict C_K_source_worldtube=0 chain into the local PPN residual map without touching geometry/EH/cGamma rows | write a residual-vector gate showing source-kernel zero, remaining non-source-kernel blockers, arena projections and first source-backed score inputs | False |

## Source register

| checkpoint | source_id | path | path_exists | needle | needle_found | role | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4591 | SRC4591_00_4590_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4590-Y5-R2FR-Dq-source-vertical-basis-and-readout-mask-zero-or-bound.md | True | E_tau_eobs | True | 4590 leaves same tau/e_obs as live source-kernel blocker | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SRC4591_01_4590_reduction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4590_SOURCE_KERNEL_REDUCTION_UPDATE.csv | True | DQMR4590_4_CKsource_strict_update | True | 4590 strict kernel reduction to E_tau_eobs | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SRC4591_02_3560_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3560-Y5-R2FR-source-support-qbasic-worldtube-descent-or-bound-vector.md | True | SCL3560_5_same_frame_tau_eobs | True | 3560 same-frame tau/eobs clause | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SRC4591_03_3560_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3560_BOUND_VECTOR.csv | True | BF3560_3_E_tau_eobs | True | 3560 E_tau_eobs bound row | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SRC4591_04_232_tau_surface | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\232-PPC4161-tau-surface-frame-lock-or-bound.md | True | tau_source=tau_charge | True | tau/surface/frame lock formal theorem | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SRC4591_05_285_dq_tau | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\285-PPC4161-Dq-tau-reference-time-lock-or-tau-residual-bound.md | True | tau_obs = tau_bar(q) | True | q-basic observed tau theorem | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SRC4591_06_4216_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4216-Y5-R2FR-tau-surface-frame-lock-or-curl-bound-row.md | True | one tau + fixed/tau-dragged S_link + one e_obs(q) | True | 4216 tau/surface/frame lock checkpoint | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SRC4591_07_4216_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4216_TAU_SURFACE_FRAME_THEOREM.csv | True | TSF4216_4_curl_zero | True | 4216 curl zero row | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SRC4591_08_4269_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4269-Y5-R2FR-Dq-tau-reference-time-lock-or-tau-residual-bound.md | True | Dq_tau = 0.0 | True | 4269 Dq_tau adoption checkpoint | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SRC4591_09_4269_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4269_TAU_LOCK_THEOREM.csv | True | TAU4269_2_role_lock | True | 4269 role-lock theorem | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SRC4591_10_4269_split | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4269_TAU_RESIDUAL_SPLIT_ROWS.csv | True | R_private_memory_tau | True | 4269 split residual rows | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SRC4591_11_3558_Hilbert_current | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3558-Y5-R2FR-same-frame-Hilbert-source-current-closure-or-coefficient-fill.md | True | same observed coframe/time/source branch | True | same-frame Hilbert source-current closure | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SRC4591_12_3249_Wsource | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3249-Y5-R2FR-Wsource-JH-tau-eobs-selector-or-source-worldtube-Poynting-bound-row-under-AX1090.md | True | same e_obs/tau package | True | source worldtube tau/eobs selector | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SRC4591_13_4580_tau_protocol | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4580_PI_READOUT_DOMAIN_CERTIFICATE.csv | True | PDC4580_2_qbasic_tau_protocol | True | readout-domain q-basic tau protocol | 2026-07-06T13:23:08.443786+00:00 | False |
| 4591 | SRC4591_14_claim_432 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\02-claims-register.csv | True | L-432 | True | claim-register handoff from 4590 | 2026-07-06T13:23:08.443786+00:00 | False |

## Validation

| checkpoint | check_id | status | detail | generated_utc |
| --- | --- | --- | --- | --- |
| 4591 | VAL4591_00_doc_written | PASS | checkpoint doc exists | 2026-07-06T13:23:08.542907+00:00 |
| 4591 | VAL4591_01_formal_written | PASS | formal bridge exists | 2026-07-06T13:23:08.542988+00:00 |
| 4591 | VAL4591_02_marker_doc | PASS | doc marker present | 2026-07-06T13:23:08.542999+00:00 |
| 4591 | VAL4591_03_marker_formal | PASS | formal marker present | 2026-07-06T13:23:08.543005+00:00 |
| 4591 | VAL4591_04_all_sources_exist | PASS | all cited local paths exist | 2026-07-06T13:23:08.543019+00:00 |
| 4591 | VAL4591_05_all_source_needles | PASS | all source needles found | 2026-07-06T13:23:08.543028+00:00 |
| 4591 | VAL4591_csv_P8_Y5_R2FR_4591_SOURCE_REGISTER | PASS | P8_Y5_R2FR_4591_SOURCE_REGISTER.csv parses with rows | 2026-07-06T13:23:08.558612+00:00 |
| 4591 | VAL4591_csv_P8_Y5_R2FR_4591_TAU_EOBS_LOCK_THEOREM | PASS | P8_Y5_R2FR_4591_TAU_EOBS_LOCK_THEOREM.csv parses with rows | 2026-07-06T13:23:08.574091+00:00 |
| 4591 | VAL4591_csv_P8_Y5_R2FR_4591_FRAME_MISMATCH_BOUND_ROWS | PASS | P8_Y5_R2FR_4591_FRAME_MISMATCH_BOUND_ROWS.csv parses with rows | 2026-07-06T13:23:08.593401+00:00 |
| 4591 | VAL4591_csv_P8_Y5_R2FR_4591_SOURCE_KERNEL_CLOSURE_UPDATE | PASS | P8_Y5_R2FR_4591_SOURCE_KERNEL_CLOSURE_UPDATE.csv parses with rows | 2026-07-06T13:23:08.608314+00:00 |
| 4591 | VAL4591_csv_P8_Y5_R2FR_4591_CONTROL_ROWS | PASS | P8_Y5_R2FR_4591_CONTROL_ROWS.csv parses with rows | 2026-07-06T13:23:08.623520+00:00 |
| 4591 | VAL4591_csv_P8_Y5_R2FR_4591_PROMOTION_GATES | PASS | P8_Y5_R2FR_4591_PROMOTION_GATES.csv parses with rows | 2026-07-06T13:23:08.635645+00:00 |
| 4591 | VAL4591_csv_P8_Y5_R2FR_4591_DECISION | PASS | P8_Y5_R2FR_4591_DECISION.csv parses with rows | 2026-07-06T13:23:08.649910+00:00 |
| 4591 | VAL4591_csv_P8_Y5_R2FR_4591_NEXT_TARGET | PASS | P8_Y5_R2FR_4591_NEXT_TARGET.csv parses with rows | 2026-07-06T13:23:08.663050+00:00 |
| 4591 | VAL4591_csv_P8_Y5_R2FR_4591_STATUS | PASS | P8_Y5_R2FR_4591_STATUS.csv parses with rows | 2026-07-06T13:23:08.673790+00:00 |
| 4591 | VAL4591_20_no_generated_claim_true | PASS | generated rows do not promote claims | 2026-07-06T13:23:08.676091+00:00 |
| 4591 | VAL4591_21_tau_zero_present | PASS | tau/eobs zero contract appears | 2026-07-06T13:23:08.676109+00:00 |
| 4591 | VAL4591_22_kernel_zero_present | PASS | strict source-kernel zero appears | 2026-07-06T13:23:08.676117+00:00 |
| 4591 | VAL4591_23_bound_formula_present | PASS | frame mismatch fallback appears | 2026-07-06T13:23:08.676127+00:00 |
| 4591 | VAL4591_24_next_target_present | PASS | next target appears | 2026-07-06T13:23:08.676138+00:00 |
| 4591 | VAL4591_25_spine_marker | PASS | spine updated once | 2026-07-06T13:23:08.696281+00:00 |
| 4591 | VAL4591_26_packet_marker | PASS | packet updated once | 2026-07-06T13:23:08.714995+00:00 |
| 4591 | VAL4591_27_claim_register | PASS | claim register updated | 2026-07-06T13:23:08.738578+00:00 |
| 4591 | VAL4591_28_no_github_action | PASS | local-only checkpoint; no git push performed | 2026-07-06T13:23:08.738609+00:00 |
| 4591 | VAL4591_29_formal_workbench_updated_only_via_declared_files | PASS | formal updates limited to declared bridge/spine/packet/claim files | 2026-07-06T13:23:08.739026+00:00 |
| 4591 | VAL4591_OVERALL | PASS | 4591 tau/eobs same-frame source-kernel closure validation | 2026-07-06T13:23:08.739049+00:00 |
