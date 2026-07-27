# 3749 - Local Fermi-Domain Projector Leak Numeric Smoke

## Status
- `FERMI_PROJECTOR_LEAK_NUMERIC_SMOKE_PASSES_NONCLAIM`
- This is a scale smoke test only: all rows stay nonclaim.
- Under unit hidden operator norms, the Fermi-domain curvature projector drift is tiny in the tested Earth/Solar domains.

## Formula
- `epsilon_comm_Fermi = C_pair * ||E_M^nabla|| * (C_Fermi L_D ||Riemann|| + C_Fermi2 L_D^2 ||nabla Riemann||) * ||deltaPhi_L||`.
- Curvature proxy: `||Riemann|| ~ sqrt(48) G M / (c^2 r^3)`, `||nabla Riemann|| ~ 3 ||Riemann|| / r`.

## Smoke Results
- `RES3749_0_earth_surface_1m` `scale_not_obviously_fatal_nonclaim`: epsilon=1.188219482376e-22 gain_to_fail=8.415953574507e+16 claim_allowed=False
- `RES3749_1_earth_surface_1km` `scale_not_obviously_fatal_nonclaim`: epsilon=1.188778435776e-19 gain_to_fail=8.411996465491e+13 claim_allowed=False
- `RES3749_2_solar_1AU_1m` `scale_not_obviously_fatal_nonclaim`: epsilon=3.055819821027e-30 gain_to_fail=3.272444249229e+24 claim_allowed=False
- `RES3749_3_solar_1AU_1km` `scale_not_obviously_fatal_nonclaim`: epsilon=3.055819882247e-27 gain_to_fail=3.272444183670e+21 claim_allowed=False
- `RES3749_4_solar_surface_1m` `scale_not_obviously_fatal_nonclaim`: epsilon=3.038351195620e-23 gain_to_fail=3.291258763772e+17 claim_allowed=False
- `RES3749_5_solar_surface_1km` `scale_not_obviously_fatal_nonclaim`: epsilon=3.038364284507e-20 gain_to_fail=3.291244585448e+14 claim_allowed=False
- `RES3749_6_solar_1AU_large_domain` `scale_not_obviously_fatal_nonclaim`: epsilon=1.828576553837e-18 gain_to_fail=5.468734671794e+12 claim_allowed=False

## Caveats
- `CAV3749_0_operator_norms`: operator constants and norm products are set to one | must source/bound operator norms
- `CAV3749_1_projector_origin`: parallel parent projector still unsigned | must derive parent bundle split or keep closure label
- `CAV3749_2_curvature_model`: Schwarzschild curvature scale is a proxy | replace smoke constants with source rows
- `CAV3749_3_no_claim`: all numeric rows are nonclaim | do not promote local GR/PPN pass

## Decisions
- `DEC3749_0_scale_result` `FERMI_PROJECTOR_DRIFT_NOT_OBVIOUSLY_FATAL_IN_SMOKE` | all scenarios pass smoke tolerances=True; smallest hidden-operator gain-to-fail is 5.469e+12
- `DEC3749_1_no_claim` `NO_LOCAL_GR_CLAIM` | the smoke uses proxy constants and unit operator norms, so it cannot prove PPN safety
- `DEC3749_2_best_next` `SOURCE_OPERATOR_NORMS_OR_PARENT_PARALLEL_SPLIT` | the next real discriminator is either C/operator norm acquisition or parent proof of A_ML=0

## Claim Gates
- `CG3749_0_sources` passed=True claim_allowed=False | 3749 source handoff complete: local source handoff rows and anchors found
- `CG3749_1_smoke_inputs` passed=True claim_allowed=False | smoke constants and scenarios emitted: constants and curvature scenarios written
- `CG3749_2_smoke_runner` passed=True claim_allowed=False | Fermi drift smoke runner executed: epsilon_comm_Fermi computed for all scenarios
- `CG3749_3_smoke_pass` passed=True claim_allowed=False | all nominal smoke scenarios pass placeholder tolerances: scale check is not obviously fatal under unit operator norms
- `CG3749_4_source_values` passed=False claim_allowed=False | all constants/operators/tolerances are claim-source-backed: operator norms and official claim tolerances are not sourced here
- `CG3749_5_parent_projector` passed=False claim_allowed=False | parent parallel projector is derived: 3748 parent split remains ansatz only
- `CG3749_6_local_claim` passed=False claim_allowed=False | local GR/Newton/PPN pass claim allowed: nonclaim smoke only

## Next Target
- `3750-Y5-R2FR-operator-norm-source-or-parent-parallel-split-proof.md`
- Objective: either source/bound the hidden operator norm product in epsilon_comm_Fermi, or attempt the stronger parent proof A_ML=0 for the structural parallel split
