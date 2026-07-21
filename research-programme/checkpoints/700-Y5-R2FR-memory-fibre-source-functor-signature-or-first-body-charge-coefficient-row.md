# 4684 - Y5/R2FR Memory/Fibre Source-Functor Signature Or First Body-Charge Coefficient Row

Marker: `PPC4161_MEMORY_FIBRE_SOURCE_KERNEL_INSERTION_CURRENT_BRANCH_4684`

Decision: `STRICT_SOURCE_KERNEL_INSERTED_INTO_MEMORY_FIBRE_J_VECTOR_LIVE_CX_JLIVE_ENVELOPE_REDUCED_CURRENT_BRANCH_NONCLAIM`

## Result

4684 imports the source-kernel insertion into the current memory/fibre branch.

```text
J_X = J_X^source_kernel + J_X^Hilbert_stationary + J_X^EM_open
    + J_X^nonHilbert + J_X^dyn_exchange + J_X^boundary_readout

strict branch => J_X^source_kernel = 0

J_X^live = J_X^EM_open + J_X^nonHilbert
         + J_X^dyn_exchange + J_X^boundary_readout.
```

The matter-trace coefficient has the clean chain-rule route:

```text
S_src = Sbar_src[q(Phi), Psi, A, theta],  v_X in ker(Dq)
=> C_X = 0
```

but only when source standards, EM Hodge/current owner, support and readout maps are q-basic/h-blind before variation.

## Source Register

| checkpoint | source_id | path | path_exists | needle | needle_found | line_number | role | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4684 | SRC4684_00_4683_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4683_NEXT_TARGET.csv | True | 4684-Y5-R2FR-memory-fibre-source-functor-signature-or-first-body-charge-coefficient-row.md | True | 2 | 4683 selected source-functor target. | False | 2026-07-07T18:30:51+00:00 |
| 4684 | SRC4684_01_4683_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4683_STATUS.csv | True | MEMORY_FIBRE_ZERO_SWITCH | True | 2 | 4683 status. | False | 2026-07-07T18:30:51+00:00 |
| 4684 | SRC4684_02_4596_insertion | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4596_SOURCE_KERNEL_TO_JMEM_INSERTION.csv | True | INS4596_0_common_split | True | 2 | source-kernel insertion law. | False | 2026-07-07T18:30:51+00:00 |
| 4684 | SRC4684_03_4596_descent | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4596_CMEM_CH_SOURCE_DESCENT_CONTRACT.csv | True | DS4596_0_chain_rule | True | 2 | C_X chain-rule descent contract. | False | 2026-07-07T18:30:51+00:00 |
| 4684 | SRC4684_04_4596_jvector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4596_JMEM_JH_REDUCED_RESIDUAL_VECTOR.csv | True | J4596_5_live_total | True | 7 | J_live reduced vector. | False | 2026-07-07T18:30:51+00:00 |
| 4684 | SRC4684_05_4596_body | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4596_BODY_CHARGE_ENVELOPE_UPDATE.csv | True | BU4596_1_memory_amplitude | True | 3 | A_mem/A_h envelope update. | False | 2026-07-07T18:30:51+00:00 |
| 4684 | SRC4684_06_4596_coeff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4596_FIRST_BODY_CHARGE_COEFFICIENT_ROWS.csv | True | CO4596_6_Qboundary | True | 8 | first coefficient rows staged. | False | 2026-07-07T18:30:51+00:00 |
| 4684 | SRC4684_07_4596_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4596_STATUS.csv | True | STRICT_SOURCE_KERNEL_INSERTED | True | 2 | 4596 status. | False | 2026-07-07T18:30:51+00:00 |
| 4684 | SRC4684_08_4596_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4596_NEXT_TARGET.csv | True | 4597-Y5-R2FR-Cmem-Ch-parent-source-descent-or-Jlive-first-norm.md | True | 2 | 4596 next target. | False | 2026-07-07T18:30:51+00:00 |
| 4684 | SRC4684_09_4596_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4596_VALIDATION.csv | True | VAL4596_OVERALL | True | 18 | 4596 validation passed. | False | 2026-07-07T18:30:51+00:00 |
| 4684 | SRC4684_10_4597_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4597_STATUS.csv | True | CMEM_CH_QBASIC_SOURCE_DESCENT | True | 2 | 4597 q-basic descent already exists. | False | 2026-07-07T18:30:51+00:00 |
| 4684 | SRC4684_11_4597_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4597_NEXT_TARGET.csv | True | constant-standard-source-weight-zero-or-CXlive-first-norm | True | 2 | 4597 next target. | False | 2026-07-07T18:30:51+00:00 |
| 4684 | SRC4684_12_4597_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4597_VALIDATION.csv | True | VAL4597_OVERALL | True | 18 | 4597 validation passed. | False | 2026-07-07T18:30:51+00:00 |
| 4684 | SRC4684_13_formal612 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\612-PPC4161-memory-fibre-source-kernel-insertion-or-first-body-charge-coefficient-row.md | True | J_X^live = J_X^EM_open | True | 27 | formal source-kernel insertion. | False | 2026-07-07T18:30:51+00:00 |

## Source-Kernel Insertion

| checkpoint | insertion_id | target | formula | zero_condition | consequence | status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4684 | INS4684_0_common_split | memory/fibre direct current | J_X = J_X^source_kernel + J_X^Hilbert_stationary + J_X^EM_open + J_X^nonHilbert + J_X^dyn_exchange + J_X^boundary_readout | same q-basic Hilbert/Maxwell worldtube branch; public Maxwell-Hodge EM in T_total; compact regular support; source-blind Href; certified Dq verticality; fixed readout mask; same tau/e_obs | J_X^source_kernel=0 and Hilbert stationary current contributes no extra direct memory/fibre current | SOURCE_KERNEL_SUBCURRENT_ZERO_INSERTED_CONDITIONALLY | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | INS4684_1_memory | J_mem | J_mem_live = J_mem^EM_open + J_mem^nonHilbert + J_mem^dyn_exchange + J_mem^boundary_readout | strict source-kernel clauses fire and all live current subchannels are independently zero | A_mem envelope drops source-kernel subterm but retains J_mem_live | MEMORY_J_VECTOR_REDUCED_NOT_CLOSED | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | INS4684_2_fibre | J_h | J_h_live = J_h^EM_open + J_h^nonHilbert + J_h^dyn_exchange + J_h^boundary_readout | same source-kernel branch plus h-blind source functor and no retained fibre current | A_h envelope drops source-kernel subterm but retains J_h_live | FIBRE_J_VECTOR_REDUCED_NOT_CLOSED | False | False | 2026-07-07T18:30:51+00:00 |

## Cmem / Ch Source-Descent Contract

| checkpoint | contract_id | coefficient | derivation | zero_condition | fallback | status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4684 | DS4684_0_chain_rule | C_X | If S_src=Sbar_src[q(Phi),Psi,A,theta] and v_X in ker(Dq), then delta_X S_src=(delta Sbar/dq)Dq[v_X]=0. | source action, masses, clocks, EM Hodge/current owner and support/readout are all q-basic before variation | \|C_X T\| retained as an absolute body-charge density term | EXACT_CHAIN_RULE_CONTRACT_NOT_PARENT_SIGNED_FOR_ALL_X | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | DS4684_1_memory | C_mem | memory/class scalar is matter-trace silent if it is a vertical memory coordinate of q and active source functor descends through q | v_m in ker(Dq); no explicit m-dependence in masses/standards/Hodge/support/readout | \|C_mem\| \|\|T\|\| remains in A_mem | CONDITIONAL_ZERO_ROUTE_READY_PARENT_SIGNATURE_UNSIGNED | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | DS4684_2_fibre | C_h | finite-cell fibre is matter-trace silent if h is absent from source grammar or eliminated before source functor is varied | h-blind S_src or h vertical to q plus no source standards/hodge/support dependence | \|C_h\| \|\|T\|\| remains in A_h | CONDITIONAL_ZERO_ROUTE_READY_PARENT_SIGNATURE_UNSIGNED | False | False | 2026-07-07T18:30:51+00:00 |

## Jmem / Jh Reduced Residual Vector

| checkpoint | residual_id | symbol | status_after_4684 | bound_if_open | next_input | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4684 | J4684_0_source_kernel | J_X^source_kernel | ZERO_ON_STRICT_BRANCH | L_JX L_K_source*(E_rho_qbasic+E_boundary_birth+E_Dq_source+E_tau_eobs+E_Href+E_readout_mask+E_EM_flux) | same-branch certificate tying source-worldtube clauses to memory/fibre X | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | J4684_1_EM_open | J_X^EM_open | ZERO_ONLY_FOR_MAXWELL_HODGE_NO_FLUX_BRANCH | \|int_boundary T_EM(tau,n)dSigma dt\|/\|M_H_ref\| times source-coupling operator norm | no-radiation collar or finite Poynting flux profile | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | J4684_2_nonHilbert | J_X^nonHilbert | LIVE | \|\|J_X^nonHilbert\|\| absolute source profile | prove no retained non-Hilbert source current or fill finite profile | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | J4684_3_dynamic_exchange | J_X^dyn_exchange | LIVE_OUTSIDE_STATIONARY_BRANCH | \|\|exchange/clock/source current\|\| | stationary exchange closure or finite dynamic current row | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | J4684_4_boundary_readout | J_X^boundary_readout | LIVE_UNLESS_BOUNDARY_READOUT_NEUTRAL | \|\|boundary/readout source reference shift\|\| | boundary/reference neutrality theorem or finite coefficient | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | J4684_5_live_total | J_X^live | REDUCED_VECTOR_READY | \|\|J_X^live\|\| <= \|\|J_X^EM_open\|\|+\|\|J_X^nonHilbert\|\|+\|\|J_X^dyn_exchange\|\|+\|\|J_X^boundary_readout\|\| | first finite norm row or parent-zero certificate | False | False | 2026-07-07T18:30:51+00:00 |

## Body-Charge Envelope Update

| checkpoint | update_id | target | before | after | claim_effect | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4684 | BU4684_0_memory_density | rho_mem | \|\|rho_mem\|\| <= \|\|B_mem_eff\|\|\|\|R_obs\|\| + \|\|C_mem\|\|\|\|T\|\| + \|\|J_mem\|\| | strict source-kernel branch: \|\|rho_mem\|\| <= \|\|B_mem_eff\|\|\|\|R_obs\|\| + \|\|C_mem\|\|\|\|T\|\| + \|\|J_mem_live\|\| | source-kernel subcurrent removed; B_mem_eff,C_mem,J_mem_live,Q_boundary_mem still block local-GR claim | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | BU4684_1_memory_amplitude | A_mem | \|A_mem\| envelope contains total J_mem | \|A_mem\| <= [exp(R/lambda_mem) int_body (\|\|B_mem_eff\|\|\|\|R_obs\|\|+\|\|C_mem\|\|\|\|T\|\|+\|\|J_mem_live\|\|) dV + \|\|Q_boundary_mem\|\|]/(4*pi\|\|Z_mem\|\|) | ready for first live-current norm or C_mem parent descent | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | BU4684_2_fibre_density | rho_h | \|\|rho_h\|\| <= \|\|B_h\|\|\|\|R_obs\|\| + \|\|C_h\|\|\|\|T\|\| + \|\|J_h\|\| | strict source-kernel branch: \|\|rho_h\|\| <= \|\|B_h\|\|\|\|R_obs\|\| + \|\|C_h\|\|\|\|T\|\| + \|\|J_h_live\|\| | source-kernel subcurrent removed; B_h,C_h,J_h_live,Q_boundary_h still block local-GR claim | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | BU4684_3_fibre_amplitude | A_h | \|A_h\| envelope contains total J_h | \|A_h\| <= [exp(R/lambda_h) int_body (\|\|B_h\|\|\|\|R_obs\|\|+\|\|C_h\|\|\|\|T\|\|+\|\|J_h_live\|\|) dV + \|\|Q_boundary_h\|\|]/(4*pi\|\|Z_h\|\|) | ready for h-blind source descent or first live-current norm | False | False | 2026-07-07T18:30:51+00:00 |

## First Body-Charge Coefficient Rows

| checkpoint | coefficient_id | symbol | role | derive_first | finite_fallback | current_status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4684 | CO4684_0_Cmem | C_mem | matter-trace memory coupling | parent-sign q-basic source descent | \|C_mem\| | MISSING_PARENT_ZERO_OR_VALUE | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | CO4684_1_Ch | C_h | matter-trace fibre coupling | parent-sign h-blind/q-basic source descent | \|C_h\| | MISSING_PARENT_ZERO_OR_VALUE | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | CO4684_2_Jkernel | J_X^source_kernel | source-worldtube active kernel | strict source-kernel branch tied to X | 0 on strict branch; open bound otherwise | ZERO_INSERTED_IF_STRICT_BRANCH | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | CO4684_3_JEM | J_X^EM_open | radiative/nonminimal EM/Poynting flux | same Hodge/current owner plus no-flux collar | boundary Poynting flux norm | MISSING_PARENT_ZERO_OR_VALUE | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | CO4684_4_JnonHilbert | J_X^nonHilbert | retained non-Hilbert source current | no retained current theorem | absolute source profile | MISSING_PARENT_ZERO_OR_VALUE | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | CO4684_5_Jdyn | J_X^dyn_exchange | dynamic clock/source exchange | stationary exchange closure | dynamic current norm | MISSING_PARENT_ZERO_OR_VALUE | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | CO4684_6_Qboundary | Q_boundary_X | boundary/body charge | regular neutral boundary/source-reference lock | finite boundary integral | MISSING_PARENT_ZERO_OR_VALUE | False | False | 2026-07-07T18:30:51+00:00 |

## Survivor Update

| checkpoint | survivor_id | residual_family | status_after_4684 | next_action | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4684 | SURV4684_0_Cmem_Ch | C_mem/C_h source-functor descent | chain-rule route written; q-basic/h-blind parent signatures missing | 4685-Y5-R2FR-Cmem-Ch-parent-source-descent-or-Jlive-first-norm.md | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | SURV4684_1_Jlive | J_X live direct current | source-kernel removed on strict branch; EM_open/nonHilbert/dyn/boundary live | 4685-Y5-R2FR-Cmem-Ch-parent-source-descent-or-Jlive-first-norm.md | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | SURV4684_2_memory_fibre_body_charge | A_mem/A_h body-charge envelope | reduced envelope with J_live; B/C/J/Q inputs remain finite | 4685-Y5-R2FR-Cmem-Ch-parent-source-descent-or-Jlive-first-norm.md | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | SURV4684_3_cR2_MR | c_R2/M_R finite-range branch | pressure now routed through memory/fibre source coefficients | continue source-functor descent before returning to R10 scoring | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | SURV4684_4_global_parent | EH/global parent/material projection | unchanged public blockers | keep promotion firewall active | False | False | 2026-07-07T18:30:51+00:00 |

## Controls

| checkpoint | control_id | rule | status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4684 | CTRL4684_0 | Do not set all J_X to zero when only the strict source-kernel subcurrent is zero. | ACTIVE | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | CTRL4684_1 | C_mem/C_h vanish only if the whole source functor is q-basic/h-blind before variation. | ACTIVE | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | CTRL4684_2 | EM/Poynting can remain in J_X^EM_open unless same-Hodge/current/no-flux guards fire. | ACTIVE | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | CTRL4684_3 | Body-charge envelopes must use absolute live terms; no cancellation between B, C, J and boundary pieces. | ACTIVE | False | False | 2026-07-07T18:30:51+00:00 |
| 4684 | CTRL4684_4 | Next target is C_mem/C_h q-basic split or first J_live norm, not a broad cR2 rerun. | ACTIVE | False | False | 2026-07-07T18:30:51+00:00 |

## Decision

| checkpoint | decision | summary | next_target | public_claim | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4684 | STRICT_SOURCE_KERNEL_INSERTED_INTO_MEMORY_FIBRE_J_VECTOR_LIVE_CX_JLIVE_ENVELOPE_REDUCED_CURRENT_BRANCH_NONCLAIM | 4684 imports the 4596 source-kernel insertion into the current branch. The strict source-kernel subcurrent is zero only on the same q-basic/Hodge/worldtube/readout branch. The live memory/fibre currents are J_X^EM_open, J_X^nonHilbert, J_X^dyn_exchange and J_X^boundary_readout. C_mem/C_h have a clean chain-rule zero route, but only if the source functor is q-basic/h-blind before variation. The next target is the Cmem/Ch q-basic split or first finite J_live norm. | 4685-Y5-R2FR-Cmem-Ch-parent-source-descent-or-Jlive-first-norm.md | False | False | 2026-07-07T18:30:51+00:00 |

## Status

| checkpoint | marker | claim_id | decision | derived | not_derived | claim_status | local_GR_public_claim | next_target | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4684 | PPC4161_MEMORY_FIBRE_SOURCE_KERNEL_INSERTION_CURRENT_BRANCH_4684 | L-526 | STRICT_SOURCE_KERNEL_INSERTED_INTO_MEMORY_FIBRE_J_VECTOR_LIVE_CX_JLIVE_ENVELOPE_REDUCED_CURRENT_BRANCH_NONCLAIM | strict source-kernel subcurrent insertion into J_mem/J_h; C_X chain-rule source descent contract; reduced A_mem/A_h envelope with J_live; first coefficient rows | parent-signed C_mem=C_h=0; parent-signed J_live=0; numeric Jlive/Qboundary/B/C coefficients; full local-GR/R10/PPN scoring | PRIVATE_NONCLAIM | False | 4685-Y5-R2FR-Cmem-Ch-parent-source-descent-or-Jlive-first-norm.md | False | 2026-07-07T18:30:51+00:00 |

## Next Target

| checkpoint | next_id | target | reason | derive_first | fallback | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4684 | NT4684_0 | 4685-Y5-R2FR-Cmem-Ch-parent-source-descent-or-Jlive-first-norm.md | After source-kernel insertion, the fastest remaining progress is either parent-sign C_mem/C_h descent or put the first finite J_live norm into the body-charge envelope. | prove source action and EM/Hodge/support/readout are q-basic/h-blind for memory and fibre | fill first finite norm row for J_X^EM_open, J_X^nonHilbert, J_X^dyn_exchange or Q_boundary_X | False | 2026-07-07T18:30:51+00:00 |

## Validation

| checkpoint | check_id | passed | detail | valid_for_claim |
| --- | --- | --- | --- | --- |
| 4684 | VAL4684_0_sources_exist | True | all source-register paths exist | False |
| 4684 | VAL4684_1_needles_found | True | all source-register needles found | False |
| 4684 | VAL4684_2_source_kernel_inserted | True | source-kernel split inserted | False |
| 4684 | VAL4684_3_chain_rule_contract | True | C_X chain-rule contract written | False |
| 4684 | VAL4684_4_jlive_vector | True | J_live reduced vector present | False |
| 4684 | VAL4684_5_body_update | True | A_mem/A_h envelope update present | False |
| 4684 | VAL4684_6_coeff_rows | True | first coefficient rows staged | False |
| 4684 | VAL4684_7_next_cmem_ch | True | next Cmem/Ch target selected | False |
| 4684 | VAL4684_8_claim_row_exists | True | claims register contains L-526 | False |
| 4684 | VAL4684_9_formal_doc | True | formal doc exists with marker | False |
| 4684 | VAL4684_10_post_doc | True | post checkpoint exists with marker | False |
| 4684 | VAL4684_11_spine_marker | True | spine marker written | False |
| 4684 | VAL4684_12_packet_marker | True | packet marker written | False |
| 4684 | VAL4684_csv_P8_Y5_R2FR_4684_SOURCE_REGISTER | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4684_SOURCE_REGISTER.csv parses with 14 rows | False |
| 4684 | VAL4684_csv_P8_Y5_R2FR_4684_SOURCE_KERNEL_TO_JMEM_INSERTION | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4684_SOURCE_KERNEL_TO_JMEM_INSERTION.csv parses with 3 rows | False |
| 4684 | VAL4684_csv_P8_Y5_R2FR_4684_CMEM_CH_SOURCE_DESCENT_CONTRACT | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4684_CMEM_CH_SOURCE_DESCENT_CONTRACT.csv parses with 3 rows | False |
| 4684 | VAL4684_csv_P8_Y5_R2FR_4684_JMEM_JH_REDUCED_RESIDUAL_VECTOR | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4684_JMEM_JH_REDUCED_RESIDUAL_VECTOR.csv parses with 6 rows | False |
| 4684 | VAL4684_csv_P8_Y5_R2FR_4684_BODY_CHARGE_ENVELOPE_UPDATE | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4684_BODY_CHARGE_ENVELOPE_UPDATE.csv parses with 4 rows | False |
| 4684 | VAL4684_csv_P8_Y5_R2FR_4684_FIRST_BODY_CHARGE_COEFFICIENT_ROWS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4684_FIRST_BODY_CHARGE_COEFFICIENT_ROWS.csv parses with 7 rows | False |
| 4684 | VAL4684_csv_P8_Y5_R2FR_4684_SURVIVOR_UPDATE | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4684_SURVIVOR_UPDATE.csv parses with 5 rows | False |
| 4684 | VAL4684_csv_P8_Y5_R2FR_4684_CONTROL_ROWS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4684_CONTROL_ROWS.csv parses with 5 rows | False |
| 4684 | VAL4684_csv_P8_Y5_R2FR_4684_DECISION | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4684_DECISION.csv parses with 1 rows | False |
| 4684 | VAL4684_csv_P8_Y5_R2FR_4684_STATUS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4684_STATUS.csv parses with 1 rows | False |
| 4684 | VAL4684_csv_P8_Y5_R2FR_4684_NEXT_TARGET | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4684_NEXT_TARGET.csv parses with 1 rows | False |
| 4684 | VAL4684_13_no_claim_rows_true | True | generated rows keep valid_for_claim false | False |
| 4684 | VAL4684_14_pycache_absent | True | scripts __pycache__ absent | False |
| 4684 | VAL4684_OVERALL | True | PASS | False |
