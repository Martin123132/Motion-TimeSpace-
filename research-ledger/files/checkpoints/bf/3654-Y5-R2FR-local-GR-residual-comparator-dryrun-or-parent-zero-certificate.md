# 3654 - Local-GR residual comparator dry-run or parent zero certificate

**Status:** 3654 builds the local-GR comparator dry-run: GR/null baseline rows and MTS residual rows use the same bound interface, baseline numeric rows pass, and MTS placeholders are refused.

**Claim ceiling:** no Newtonian, PPN, local-GR, source-calibration, WEP, R10, clock, orbital, or EH-dominance pass is claimed.

## Main result

The comparator now enforces the rule we wanted: `GR_null` and `MTS_local_GR_residual_vector` are evaluated against the same Newton/PPN interface. The GR/null numeric rows pass because their residuals are zero. MTS does **not** pass or fail physically yet, because every MTS residual row is still a missing component or unsigned parent-zero certificate.

That is the clean result: no more one-sided tests, and no more accidentally treating placeholders as zeros.

## Comparator interface
- `CI3654_0_gamma`: `delta_gamma_MTS` vs `R3_gamma` — NUMERIC_BOUND_READY
- `CI3654_1_beta`: `delta_beta_MTS` vs `R4_beta` — NUMERIC_BOUND_READY
- `CI3654_2_alpha1`: `alpha1_MTS` vs `R5_alpha1` — NUMERIC_BOUND_READY
- `CI3654_3_alpha2`: `alpha2_MTS` vs `R6_alpha2` — NUMERIC_BOUND_READY
- `CI3654_4_alpha3`: `alpha3_MTS` vs `R7_alpha3` — NUMERIC_BOUND_READY
- `CI3654_5_xi`: `xi_MTS` vs `R8_xi` — NUMERIC_BOUND_READY
- `CI3654_6_Gdot`: `Gdot_over_G_MTS` vs `R9_Gdot` — NUMERIC_BOUND_READY
- `CI3654_7_Poisson`: `q_Poisson` vs `R11_EH_operator_ledger` — SYMBOLIC_OR_VECTOR_GATE
- `CI3654_8_total`: `Delta_local_GR_abs` vs `R3-R9 plus R11` — SYMBOLIC_OR_VECTOR_GATE

## GR/null baseline rows
- `BL3654_0_gamma`: `gamma_minus_1` — BASELINE_NUMERIC_PASS
- `BL3654_1_beta`: `beta_minus_1` — BASELINE_NUMERIC_PASS
- `BL3654_2_alpha1`: `alpha1` — BASELINE_NUMERIC_PASS
- `BL3654_3_alpha2`: `alpha2` — BASELINE_NUMERIC_PASS
- `BL3654_4_alpha3`: `alpha3` — BASELINE_NUMERIC_PASS
- `BL3654_5_xi`: `xi` — BASELINE_NUMERIC_PASS
- `BL3654_6_Gdot`: `Gdot_over_G` — BASELINE_NUMERIC_PASS
- `BL3654_7_Poisson`: `Poisson_source_identity` — BASELINE_STRUCTURAL_ONLY_NOT_NUMERIC
- `BL3654_8_total`: `local_GR_residual_envelope` — BASELINE_STRUCTURAL_ONLY_NOT_NUMERIC

## MTS dry-run rows
- `MTS3654_0_gamma`: `delta_gamma_MTS` — BLOCKED_PLACEHOLDER_REFUSED
- `MTS3654_1_beta`: `delta_beta_MTS` — BLOCKED_PLACEHOLDER_REFUSED
- `MTS3654_2_alpha1`: `alpha1_MTS` — BLOCKED_PLACEHOLDER_REFUSED
- `MTS3654_3_alpha2`: `alpha2_MTS` — BLOCKED_PLACEHOLDER_REFUSED
- `MTS3654_4_alpha3`: `alpha3_MTS` — BLOCKED_PLACEHOLDER_REFUSED
- `MTS3654_5_xi`: `xi_MTS` — BLOCKED_PLACEHOLDER_REFUSED
- `MTS3654_6_Gdot`: `Gdot_over_G_MTS` — BLOCKED_PLACEHOLDER_REFUSED
- `MTS3654_7_Poisson`: `q_Poisson` — BLOCKED_PLACEHOLDER_REFUSED
- `MTS3654_8_total`: `Delta_local_GR_abs` — BLOCKED_PLACEHOLDER_REFUSED

## Parent zero-certificate audit
- `PZC3654_0_EH_action`: `q_EH_action` — MISSING_OR_UNSIGNED
- `PZC3654_1_EH_prefactor`: `q_GN_prefactor` — MISSING_OR_UNSIGNED
- `PZC3654_2_Poisson_source`: `q_Poisson_source` — MISSING_OR_UNSIGNED
- `PZC3654_3_metric_second_order`: `q_metric_PPN` — MISSING_OR_UNSIGNED
- `PZC3654_4_readout`: `q_readout_PPN` — MISSING_OR_UNSIGNED
- `PZC3654_5_boundary`: `q_boundary_PPN` — MISSING_OR_UNSIGNED
- `PZC3654_6_nonEH`: `q_nonEH_PPN` — MISSING_OR_UNSIGNED
- `PZC3654_7_source_coupling`: `q_source_coupling_PPN` — MISSING_OR_UNSIGNED
- `PZC3654_8_time_drift`: `q_time_drift` — MISSING_OR_UNSIGNED
- `PZC3654_9_total`: `Delta_local_GR_abs` — MISSING_OR_UNSIGNED

## Summary
- `SUM3654_0_baseline`: `GR_null_baseline` — BASELINE_NUMERIC_ROWS_PASS_SYMBOLIC_ROWS_STRUCTURAL
- `SUM3654_1_MTS`: `MTS_local_GR_residual_vector` — MTS_DRYRUN_BLOCKED_VALUES_MISSING
- `SUM3654_2_parent_zero_certificate`: `parent_zero_certificate` — PARENT_ZERO_CERTIFICATE_NOT_ACCEPTED

## Claim gates
- `CG3654_0_same_interface`: `PASSED` — GR/null and MTS rows use the same observable/bound interface
- `CG3654_1_baseline_runs`: `PASSED_FOR_NUMERIC_ROWS` — GR/null numeric rows pass their numeric bounds
- `CG3654_2_placeholders_refused`: `PASSED_REFUSAL` — MTS placeholders cannot score or pass
- `CG3654_3_parent_zero_certificate`: `FAILED_UNSIGNED` — parent zero certificate can replace numeric rows only if every component is signed
- `CG3654_4_no_public_claim`: `ACTIVE` — local-GR/Newton/PPN pass is not claimed
- `CG3654_5_next`: `LOCAL_GR_COMPONENT_FILL_NEXT` — next step must fill residual values or parent zero certificates

## Next checkpoint

`3655-Y5-R2FR-parent-local-GR-zero-certificate-or-first-residual-component-fill.md` via `scripts/Y5_R2FR_3655_parent_local_GR_zero_certificate_or_first_residual_component_fill.py`.

## Sources
- `next_3653`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3653_NEXT_TARGET.csv` exists=True needle_found=True
- `doc_3653`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3653-Y5-R2FR-Newton-Poisson-PPN-zero-vector-gate-or-local-GR-residual-fit.md` exists=True needle_found=True
- `theorem_3653`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3653_NEWTON_PPN_ZERO_VECTOR_THEOREM_ATTEMPT.csv` exists=True needle_found=True
- `bound_interface_3653`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3653_BOUND_INTERFACE_ROWS.csv` exists=True needle_found=True
- `residual_rows_3653`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3653_LOCAL_GR_RESIDUAL_COMPONENT_ROWS.csv` exists=True needle_found=True
- `zero_contract_3653`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3653_ZERO_CONTRACT_ROWS.csv` exists=True needle_found=True
- `doc_425`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\425-EH-operator-retained-ledger-and-source-normalization-test-plan.md` exists=True needle_found=True
- `bounds_R3`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `bounds_R4`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `bounds_R5`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `bounds_R6`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `bounds_R7`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `bounds_R8`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `bounds_R9`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
