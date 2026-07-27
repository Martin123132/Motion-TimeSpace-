# 3653 - Newton-Poisson PPN zero-vector gate or local-GR residual fit

**Status:** 3653 derives the Newton-Poisson/PPN zero-vector gate and creates a nonclaim local-GR residual component interface with bound anchors.

**Claim ceiling:** no Newtonian, PPN, local-GR, source-calibration, WEP, R10, clock, orbital, or EH-dominance pass is claimed.

## Main result

The local-GR target is now a vector gate, not a mood. Newton-Poisson requires `nabla^2 Phi_N = 4*pi*G_N*rho_inertial` with active/inertial source identity and no Newtonian-order residuals. PPN requires `Delta_PPN_MTS=(gamma-1,beta-1,alpha1,alpha2,alpha3,xi,Gdot/G)=0` with the same source, readout, boundary, and non-EH conventions.

Current MTS does not yet sign those clauses as one parent branch. Therefore the correct fallback is `Delta_local_GR_abs`, an absolute-envelope residual vector with bound anchors and a future GR/null baseline comparator.

## Theorem rows
- `NPG3653_0_parent_EH_weak_field`: `EXACT_CONDITIONAL_THEOREM_PREMISES_UNSIGNED` — The metric side of local GR is conditionally derivable, but only with source/readout/boundary/non-EH silence.
- `NPG3653_1_Poisson_zero_gate`: `NEWTON_POISSON_ZERO_CONDITION_DERIVED` — Newton's law is not just fitted GM; it is a zero condition on the Poisson source channel.
- `NPG3653_2_PPN_coefficient_gate`: `PPN_ZERO_VECTOR_CONDITION_DERIVED` — A local-GR claim requires the whole vector to be zero or below bounds with a common source/readout convention.
- `NPG3653_3_nonEH_operator_gate`: `NON_EH_RESIDUAL_GATE_DERIVED` — EH presence is not EH dominance; the retained non-EH vector remains a gate.
- `NPG3653_4_common_frame_source_readout_gate`: `COMMON_FRAME_GATE_DERIVED` — The local-GR gate includes no-shadow/no-source-only-frame conditions.
- `NPG3653_5_residual_bound_rule`: `NO_CANCELLATION_RESIDUAL_RULE_DERIVED` — This gives a scoreable future path without smuggling closure.
- `NPG3653_6_baseline_comparator_policy`: `BASELINE_COMPARATOR_POLICY_DERIVED` — The gate now encodes the user's correct criticism: test MTS and the comparator together.
- `NPG3653_7_verdict`: `FAIL_CURRENT_CLAIM_LOCAL_GR_ZERO_VECTOR_UNSIGNED` — Current MTS has a serious local-GR gate, not yet a local-GR pass.

## Zero-contract rows
- `ZC3653_0_EH_action`: `q_EH_action` — PARENT_EH_DOMINANCE_UNSIGNED
- `ZC3653_1_EH_prefactor`: `q_GN_prefactor` — GN_PREFACTOR_OWNER_UNSIGNED
- `ZC3653_2_Poisson_source`: `q_Poisson_source` — ACTIVE_INERTIAL_SOURCE_UNSIGNED
- `ZC3653_3_metric_second_order`: `q_metric_PPN` — PPN_METRIC_COEFFICIENTS_UNSIGNED
- `ZC3653_4_readout`: `q_readout_PPN` — READOUT_FRAME_UNSIGNED
- `ZC3653_5_boundary`: `q_boundary_PPN` — BOUNDARY_DOMAIN_UNSIGNED
- `ZC3653_6_nonEH`: `q_nonEH_PPN` — NON_EH_OPERATOR_VECTOR_UNSIGNED
- `ZC3653_7_source_coupling`: `q_source_coupling_PPN` — SOURCE_COUPLING_VECTOR_UNSIGNED
- `ZC3653_8_time_drift`: `q_time_drift` — TIME_DRIFT_UNSIGNED
- `ZC3653_9_total`: `Delta_local_GR_abs` — SCHEMA_READY_VALUES_MISSING

## Local-GR residual rows
- `LGR3653_0_Poisson`: `q_Poisson` — NEWTON_COMPONENTS_REQUIRED
- `LGR3653_1_gamma`: `delta_gamma_MTS` — GAMMA_COMPONENTS_REQUIRED
- `LGR3653_2_beta`: `delta_beta_MTS` — BETA_COMPONENTS_REQUIRED
- `LGR3653_3_alpha1`: `alpha1_MTS` — ALPHA1_COMPONENTS_REQUIRED
- `LGR3653_4_alpha2`: `alpha2_MTS` — ALPHA2_COMPONENTS_REQUIRED
- `LGR3653_5_alpha3`: `alpha3_MTS` — ALPHA3_COMPONENTS_REQUIRED
- `LGR3653_6_xi`: `xi_MTS` — XI_COMPONENTS_REQUIRED
- `LGR3653_7_Gdot`: `Gdot_over_G_MTS` — GDOT_COMPONENTS_REQUIRED
- `LGR3653_8_source`: `q_source_PPN_abs` — SOURCE_VECTOR_REQUIRED
- `LGR3653_9_readout`: `q_readout_PPN_abs` — READOUT_VECTOR_REQUIRED
- `LGR3653_10_boundary`: `q_boundary_PPN_abs` — BOUNDARY_VECTOR_REQUIRED
- `LGR3653_11_nonEH`: `q_nonEH_PPN_abs` — NON_EH_VECTOR_REQUIRED
- `LGR3653_12_total`: `Delta_local_GR_abs` — SCHEMA_READY_VALUES_MISSING

## Bound interface rows
- `BI3653_0_gamma`: `delta_gamma_MTS` -> `R3_gamma` — BOUND_ANCHOR_READY_MTS_VALUE_MISSING
- `BI3653_1_beta`: `delta_beta_MTS` -> `R4_beta` — BOUND_ANCHOR_READY_MTS_VALUE_MISSING
- `BI3653_2_alpha1`: `alpha1_MTS` -> `R5_alpha1` — BOUND_ANCHOR_READY_MTS_VALUE_MISSING
- `BI3653_3_alpha2`: `alpha2_MTS` -> `R6_alpha2` — BOUND_ANCHOR_READY_MTS_VALUE_MISSING
- `BI3653_4_alpha3`: `alpha3_MTS` -> `R7_alpha3` — BOUND_ANCHOR_READY_MTS_VALUE_MISSING
- `BI3653_5_xi`: `xi_MTS` -> `R8_xi` — BOUND_ANCHOR_READY_MTS_VALUE_MISSING
- `BI3653_6_Gdot`: `Gdot_over_G_MTS` -> `R9_Gdot` — BOUND_ANCHOR_READY_MTS_VALUE_MISSING
- `BI3653_7_Poisson`: `q_Poisson` -> `R11_EH_operator_ledger` — SYMBOLIC_GATE_REQUIRED
- `BI3653_8_total`: `Delta_local_GR_abs` -> `R3-R9 plus R11` — BOUND_ANCHOR_READY_MTS_VALUE_MISSING

## Decisions
- `DEC3653_0_gate`: `NEWTON_PPN_ZERO_VECTOR_GATE_DERIVED` — Newton-Poisson and PPN are now one local-GR zero-vector gate, not separate claim fragments.
- `DEC3653_1_verdict`: `PARENT_LOCAL_GR_ZERO_VECTOR_UNSIGNED` — Current MTS does not sign EH dominance, source identity, readout, boundary, non-EH, and PPN coefficient zeros together.
- `DEC3653_2_residuals`: `LOCAL_GR_RESIDUAL_VECTOR_CREATED_NOT_SCORE_READY` — Local-GR residual rows are staged with units, bound anchors, source/readout/boundary/non-EH components, and no-cancellation guards.
- `DEC3653_3_next`: `LOCAL_GR_COMPARATOR_DRYRUN_NEXT` — Next target is an executable local-GR residual comparator/dry-run that runs the GR/null baseline and MTS residual vector through the same interface.

## Next checkpoint

`3654-Y5-R2FR-local-GR-residual-comparator-dryrun-or-parent-zero-certificate.md` via `scripts/Y5_R2FR_3654_local_GR_residual_comparator_dryrun_or_parent_zero_certificate.py`.

## Sources
- `next_3652`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3652_NEXT_TARGET.csv` exists=True needle_found=True
- `doc_3652`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3652-Y5-R2FR-weak-field-source-Hamiltonian-GM-calibration-or-source-vector-bound.md` exists=True needle_found=True
- `theorem_3652`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3652_WEAK_FIELD_HAMILTONIAN_THEOREM_ATTEMPT.csv` exists=True needle_found=True
- `calibration_3652`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3652_GM_SOURCE_CALIBRATION_ROWS.csv` exists=True needle_found=True
- `residual_3652`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3652_PPN_ORBITAL_RESIDUAL_VECTOR_ROWS.csv` exists=True needle_found=True
- `projection_3652`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3652_PROJECTION_ROWS.csv` exists=True needle_found=True
- `doc_425`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\425-EH-operator-retained-ledger-and-source-normalization-test-plan.md` exists=True needle_found=True
- `doc_02`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\02-motion-load-local-GR-reduction.md` exists=True needle_found=True
- `matrix_1048`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv` exists=True needle_found=True
- `bounds_R3`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `bounds_R4`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `bounds_R5`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `bounds_R6`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `bounds_R7`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `bounds_R8`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `bounds_R9`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
