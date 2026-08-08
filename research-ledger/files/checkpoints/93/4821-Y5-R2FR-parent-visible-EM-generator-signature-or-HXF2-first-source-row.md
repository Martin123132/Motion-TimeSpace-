# 4821 - Parent visible EM generator signature or HXF2 first source row

Marker: `PPC4161_PARENT_VISIBLE_EM_GENERATOR_SIGNATURE_OR_HXF2_FIRST_SOURCE_ROW_4821`
Decision: `VISIBLE_EM_GENERATOR_PARTIAL_EDGE_SIGNED_HXF2_MEMORY_ROW_STAGED_NONCLAIM`
Claim row: `L-663` private nonclaim
Generated: `2026-07-08T09:46:52+00:00`

## Result

4821 attempts the derivation route first. The result is a clean split:

```text
standard visible branch:
EM edge/Hodge/stress/Poynting ownership = ready inside the calibrated 4210 branch

full parent visible EM generator:
requires unique F2/no-Hom + charge-current owner + radiative/readout closure
current corpus does not sign those clauses

finite fallback:
C_memory_F2 = |kappa_memF2/Z_Q_eff| Delta_v m_mem
qbar_EM_memory = K_qbar_EM C_memory_F2
```

This is a real improvement because the EM/Poynting part is preserved as branch-owned source accounting while the missing coupling is reduced to a named coefficient law rather than a foggy coupling complaint.

## Source register

| source_id | source_path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC4821_00_resume | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\CURRENT_LOCAL_RESUME.md | True | True | current handoff |
| SRC4821_01_4820 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4820-Y5-R2FR-EM-F2-hardblocker-or-first-qbar-marker-bound-row.md | True | True | 4820 exact/finite EM gate |
| SRC4821_02_3506 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3506_PARENT_VISIBLE_EM_GENERATOR_SIGNATURE.csv | True | True | parent visible EM generator signature |
| SRC4821_03_4436_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4436-Y5-R2FR-visible-EM-action-edge-parent-signature-or-Kmactionscale-source-leg.md | True | True | branch EM edge signature |
| SRC4821_04_4436_out | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4436_VISIBLE_EM_SIGNATURE_OUTPUT.csv | True | True | edge ready but scale gates open |
| SRC4821_05_4617_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4617-Y5-R2FR-parent-scalar-functional-exhaustion-or-first-Hom-bound-value.md | True | True | HXF2 component vector law |
| SRC4821_06_4617_hxf2 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4617_HXF2_COMPONENT_VECTOR_NONCLAIM.csv | True | True | first HXF2 memory component |
| SRC4821_07_4618_cmemory | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4618_CMEMORY_F2_VALUE_ROW_NONCLAIM.csv | True | True | C_memory_F2 first value contract |
| SRC4821_08_4619_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4619_F2_MEMORY_OWNER_THEOREM.csv | True | True | finite memory/F2 identity |
| SRC4821_09_4619_source | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4619_KAPPA_MEMF2_ZMEM_M2MEM_SOURCE_ROWS_NONCLAIM.csv | True | True | kappa/Z/source rows |
| SRC4821_10_4620_numeric | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4620_KAPPA_MEMF2_FIRST_NUMERIC_ROW_NONCLAIM.csv | True | True | first numeric row template |
| SRC4821_11_4704_visible | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4704_VISIBLE_IMAGE_PROOF_ATTEMPT.csv | True | True | visible image bottleneck |
| SRC4821_12_4820_output | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4820_EMF2_RUNNER_OUTPUT.csv | True | True | 4820 runner handoff |
| SRC4821_13_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\visible_EM_generator_HXF2_runner.py | True | True | 4821 runner |

## Generator signature derivation

| row_id | piece | derived_law | status | blocks |
| --- | --- | --- | --- | --- |
| VES4821_0_edge_signature | standard visible EM edge | S_Maxwell-Hodge[A,g_obs;alpha_obs] in the 4210 standard branch owns EM stress and Poynting flux before readout. | EDGE_SIGNATURE_READY_PRIVATE_BRANCH | unique_F2_no_extra_prefactor; charge_current_owner; radiative_closure |
| VES4821_1_generator_full_signature | full parent visible EM generator | A full generator signature requires edge ownership plus unique F2/no-Hom, charge-current owner, fixed representation constants, no species prefactor, readout-after-variation and radiative closure. | NOT_SIGNED_CURRENT_CORPUS | unique F2/current/radiative gates remain open |
| VES4821_2_no_globalization | standard branch vs global MTS generator | The fixed q-basic standard branch may set C_XF2=0 as a branch condition, but that cannot be globalized to a dynamic MTS parent generator. | FIREWALL_ACTIVE | standard_branch_as_global shortcut |
| VES4821_3_memory_Hom_first_row | first HXF2 source fallback | If no-Hom/typed-domain zero fails, C_memory_F2=|kappa_memF2/Z_Q_eff| Delta_v m_mem at first order. | EXACT_FINITE_IDENTITY_VALUES_MISSING | kappa_memF2; Z_Q_eff_min; Delta_v_m_mem; arena K/tau/source rows |

## HXF2 first-source contract

| contract_id | quantity | formula | required_inputs | status |
| --- | --- | --- | --- | --- |
| HXF24821_0_zero | C_memory_F2 | C_memory_F2=0 if typed-domain/no-Hom, fixed branch, branch extremum, or exact symmetry zero is signed in the same branch with readout/radiative closure. | zero certificate; same branch; readout/radiative closure | conditional_only |
| HXF24821_1_finite | C_memory_F2_abs | |kappa_memF2| * Delta_v_m_mem_abs / Z_Q_eff_min | kappa_memF2_abs; Z_Q_eff_min>0; Delta_v_m_mem_abs; source_signed; units_signed; same_branch_signed | source_row_ready_values_missing |
| HXF24821_2_qbar | qbar_EM_memory_abs | K_qbar_EM_abs * C_memory_F2_abs | K_qbar_EM_abs and HXF24821_1 | projection_ready_values_missing |

## Runner output

| row_id | route_type | runner_status | edge_signature_ready | full_generator_ready | C_memory_F2_abs | qbar_EM_memory_abs | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RUN4821_0_standard_edge_partial | generator_signature | VISIBLE_EM_EDGE_SIGNATURE_READY_SCALE_GATES_OPEN | True | False | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | False |
| RUN4821_1_global_generator_blocked | generator_signature | BLOCKED_VISIBLE_EM_GENERATOR_SIGNATURE | False | False | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | False |
| RUN4821_2_conditional_full_generator_pass | generator_signature | VISIBLE_EM_GENERATOR_SIGNATURE_PASS_NONCLAIM | True | True | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | False |
| RUN4821_3_forbidden_standard_as_global | generator_signature | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | False | False | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | False |
| RUN4821_4_live_HXF2_missing | hxf2_memory_bound | BLOCKED_HXF2_MEMORY_SOURCE_INPUTS | False | False | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | False |
| RUN4821_5_HXF2_memory_smoke_pass | hxf2_memory_bound | HXF2_MEMORY_SOURCE_BOUND_PASS_NONCLAIM | False | False | 3.000000000000000e-03 | 1.500000000000000e-03 | False |
| RUN4821_6_HXF2_memory_zero_smoke | hxf2_memory_zero | HXF2_MEMORY_ZERO_PASS_NONCLAIM | False | False | 0.000000000000000e+00 | 0.000000000000000e+00 | False |
| RUN4821_7_forbidden_bound_as_source | hxf2_memory_bound | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | False | False | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | False |

## Claim gates

| gate_id | firewall | status | claim_allowed |
| --- | --- | --- | --- |
| G4821_0_no_global_EM_claim | Do not globalize the 4210 standard branch to a dynamic MTS visible EM generator. | ACTIVE_NONCLAIM | False |
| G4821_1_no_alpha_derivation | Do not treat calibrated alpha or field normalization as a derivation of unique F2. | ACTIVE_NONCLAIM | False |
| G4821_2_no_HXF2_claim | Do not claim H_XF2=0 or finite until kappa/Z/amplitude/source rows are real or zero-signed. | ACTIVE_NONCLAIM | False |
| G4821_3_no_bound_backfit | Do not infer kappa_memF2 or memory amplitude by saturating empirical bounds. | ACTIVE_NONCLAIM | False |
| G4821_4_no_local_GR_claim | Do not claim local GR/Newton/PPN/R10/clock/orbital closure from 4821. | ACTIVE_NONCLAIM | False |

## Decision ledger

| decision_id | decision | meaning |
| --- | --- | --- |
| DEC4821_0_signature_split | VISIBLE_EM_EDGE_READY_FULL_GENERATOR_OPEN | Standard branch owns EM Hodge/stress/Poynting edge, but full generator fails on unique F2, current owner and radiative closure. |
| DEC4821_1_HXF2_first_row | C_MEMORY_F2_SELECTED_AS_FIRST_HXF2_SOURCE_ROW | First finite source row is C_memory_F2=|kappa_memF2/Z_Q_eff| Delta_v m_mem, with zero switches retained. |
| DEC4821_2_next_target | 4822-Y5-R2FR-kappa-memF2-zero-certificate-or-Zmem-M2mem-source-row.md | Next best derivation target is kappa_memF2 zero/value plus Zmem/M2mem positive-operator source rows. |

## Next target

`4822-Y5-R2FR-kappa-memF2-zero-certificate-or-Zmem-M2mem-source-row.md`
