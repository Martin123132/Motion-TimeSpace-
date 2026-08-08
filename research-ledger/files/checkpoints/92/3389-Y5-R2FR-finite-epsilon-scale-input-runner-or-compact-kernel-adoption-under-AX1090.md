# 3389 - Y5/R2FR finite epsilon scale-input runner or compact-kernel adoption under AX1090

## Summary
- 3389 turns the 3388 scale requirements into an executable nonclaim runner.
- Compact-kernel route: mathematically clean and can zero the collar tail, but it is not currently adopted because it needs a parent smoothing declaration and a replacement for the Gaussian transfer law.
- Gaussian route: still testable; strict rows require large enough `d_collar/ell_s`, small enough physical flux, and tiny projector/moment/gauge defects.
- Current strict scale lesson: with `C_boundary=1` and zero flux, the harsh rows require `d_collar/ell_s` up to about `7.136`; kernel additive terms can need budgets down to `8.756e-12`.
- Scenario runner result: pass-like rows exist only as hypothetical/nonclaim rows; flux or gauge defects easily dominate.
- No local-GR/PPN claim is allowed from 3389; the next step must source or derive the actual local scale inputs.

## Source Register
| source_id | source_path | exists | parse_ok | role | parse_error | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC3389_0_3388_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3388-Y5-R2FR-smoothing-projector-parent-owner-or-epsilon-scale-inputs-under-AX1090.md | true | true | 3388 smoothing/projector handoff |  | false |
| SRC3389_1_3388_targets | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3388_SCALE_TARGET_REQUIREMENTS.csv | true | true | scale target requirements |  | false |
| SRC3389_2_3388_inputs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3388_FIRST_SCALE_INPUT_ROWS_NONCLAIM.csv | true | true | finite scale input rows |  | false |
| SRC3389_3_3388_package | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3388_ADMISSIBLE_PACKAGE_CONTRACT.csv | true | true | admissible package contract |  | false |
| SRC3389_4_3388_zero | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3388_ZERO_IMPLICATIONS_AND_REDUCED_EPSILON.csv | true | true | zero and finite implications |  | false |
| SRC3389_5_3387_boundary | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3387_BOUNDARY_COLLAR_TAIL_LAW.csv | true | true | boundary collar-tail law |  | false |
| SRC3389_6_3387_kernel | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3387_KERNEL_PROJECTOR_COMMUTATOR_LAW.csv | true | true | kernel projector commutator law |  | false |
| SRC3389_7_3321_kernel | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3321_KERNEL_TRANSFER_LAW.csv | true | true | Gaussian kernel transfer law |  | false |
| SRC3389_8_3320_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3320-Y5-R2FR-local-first-gradient-silence-or-gradient-envelope-under-AX1090.md | true | true | compact-kernel stationarity route |  | false |
| SRC3389_9_3376_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3376-Y5-R2FR-boundary-zero-flux-or-Bzero-first-row-under-AX1090.md | true | true | boundary zero-flux package |  | false |

## Compact Kernel Adoption Audit
| audit_id | question | result | detail | blocks_current_adoption | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CK3389_0_mathematical_existence | Can an isotropic compact bump kernel with zero first moment exist? | YES_MATHEMATICALLY | In a local normal/Fermi patch one can choose a normalized radial compact bump K_ell with int z^i K_ell dV=0 up to curvature correction terms. | parent MTS has not selected this kernel branch before tests | false |
| CK3389_1_boundary_zero | Would compact/interior support zero epsilon_boundary_tail? | YES_CONDITIONALLY | If d_collar >= rho_K ell_s and the 3376 physical/reference/topology flux package is zero, boundary leakage vanishes structurally. | d_collar/ell_s, rho_K, and 3376 zero-flux clauses are not parent-signed | false |
| CK3389_2_transfer_replacement | Can compact kernel replace Gaussian without changing earlier transfer rows? | NO_REQUIRES_TRANSFER_REDERIVATION | 3321 Gaussian T_grad samples use exp[-ell_s^2/(2 lambda^2)]; a compact bump needs its own \|Khat(k ell_s)\| bound and constants. | compact branch must regenerate T_grad and threshold tables before empirical scoring | false |
| CK3389_3_projector_commutation | Does compact/isotropic smoothing solve kernel anisotropy? | ONLY_WITH_CONSTANT_PROJECTOR | Any scalar isotropic kernel commutes with a constant P0, but variable P_PPN still has [P,S]f=int K[P(x)-P(y)]f. | real-patch projector constancy or finite gradient bounds remain required | false |
| CK3389_4_current_verdict | Is compact kernel adopted for current MTS? | CURRENTLY_NOT_ADOPTED | Compact branch is a clean theorem route, but switching from Gaussian to compact would be a parent-action/readout choice requiring explicit adoption and transfer-law replacement. | no parent-signed smoothing branch declaration | false |

## Scale Input Schema
| input_id | quantity | definition | needed_for | current_value | runner_role | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SI3388_0_kernel_branch | kernel_branch | compact_bump or gaussian_heat_kernel selected before tests | decide exact collar zero versus exponential tail | MISSING_PARENT_KERNEL_BRANCH_DECLARATION | required input for exact compact branch or Gaussian finite bound | MISSING_NONCLAIM_INPUT | false |
| SI3388_1_d_over_ell | d_collar/ell_s | source-free collar distance divided by smoothing length | epsilon_boundary_tail <= C_B exp[-(d/ell)^2/2] | MISSING_D_COLLAR_OVER_ELL_S | required input for exact compact branch or Gaussian finite bound | MISSING_NONCLAIM_INPUT | false |
| SI3388_2_C_boundary | C_boundary | operator/source amplitude multiplying Gaussian boundary tail | boundary tail normalization | MISSING_C_BOUNDARY | required input for exact compact branch or Gaussian finite bound | MISSING_NONCLAIM_INPUT | false |
| SI3388_3_flux_envelope | epsilon_boundary_physical | (\|B_zero_flux\|+\|Delta_symp\|+\|Phi_Poynting_bound\|+\|corner/topology\|)/M_H_ref + epsilon_worldtube_mismatch | physical/reference/topology part of epsilon_boundary_PPN | MISSING_3376_FLUX_REFERENCE_VALUES | required input for exact compact branch or Gaussian finite bound | MISSING_NONCLAIM_INPUT | false |
| SI3388_4_projector_gradient | ell_s \|\|nabla P_PPN\|\| | first-order real-patch variation of local PPN projector across smoothing cell | kernel commutator bound | MISSING_PROJECTOR_GRADIENT_NORM | required input for exact compact branch or Gaussian finite bound | MISSING_NONCLAIM_INPUT | false |
| SI3388_5_projector_hessian | ell_s^2 \|\|nabla^2 P_PPN\|\| | second-order projector variation across smoothing cell | kernel commutator bound beyond tangent limit | MISSING_PROJECTOR_HESSIAN_NORM | required input for exact compact branch or Gaussian finite bound | MISSING_NONCLAIM_INPUT | false |
| SI3388_6_kernel_moment_defect | epsilon_kernel_moment | nonzero first moment or anisotropic moment defect of actual smoothing kernel | kernel anisotropy residual | MISSING_KERNEL_MOMENT_DEFECT | required input for exact compact branch or Gaussian finite bound | MISSING_NONCLAIM_INPUT | false |
| SI3388_7_gauge_readout_defect | epsilon_gauge_readout | PPN gauge/readout drift introduced by smoothing and local frame choice | kernel anisotropy residual and Cmetric separation | MISSING_GAUGE_READOUT_DEFECT | required input for exact compact branch or Gaussian finite bound | MISSING_NONCLAIM_INPUT | false |

## Target Requirement Summary
| summary_id | threshold_source | source_row | A_gamma_or_PPN_times_Cmetric | min_epsilon_boundary_target | required_d_collar_over_ell_Cboundary1_flux0 | min_epsilon_kernel_target | equal_quarter_kernel_term_budget | interpretation | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TS3389_TH3385_AxC_1e+00 | FULL_GAMMA_ZERO_FLOORS_3385 | TH3385_AxC_1e+00 | 1.000000e+00 | 2.728450923957483e-03 | 3.436283241514e+00 | 2.728450923957483e-03 | 6.821127309893707e-04 | target only; no current source-backed scale input | false |
| TS3389_TH3385_AxC_1e+06 | FULL_GAMMA_ZERO_FLOORS_3385 | TH3385_AxC_1e+06 | 1.000000e+06 | 2.728450923957483e-06 | 5.061971263636e+00 | 2.728450923957483e-06 | 6.821127309893707e-07 | target only; no current source-backed scale input | false |
| TS3389_TH3385_AxC_1e+12 | FULL_GAMMA_ZERO_FLOORS_3385 | TH3385_AxC_1e+12 | 1.000000e+12 | 2.728450923957483e-09 | 6.280052836708e+00 | 2.728450923957483e-09 | 6.821127309893708e-10 | target only; no current source-backed scale input | false |
| TS3389_TH3385_AxC_1e+16 | FULL_GAMMA_ZERO_FLOORS_3385 | TH3385_AxC_1e+16 | 1.000000e+16 | 2.728450923957483e-11 | 6.974912472843e+00 | 2.728450923957483e-11 | 6.821127309893708e-12 | target only; no current source-backed scale input | false |
| TS3389_TREE3336_resp_1e+00 | TREE_PARTITION_3336 | TREE3336_resp_1e+00 | 1.000000e+00 | 8.755950000000000e-04 | 3.752494344487e+00 | 8.755950000000000e-04 | 2.188987500000000e-04 | target only; no current source-backed scale input | false |
| TS3389_TREE3336_resp_1e+06 | TREE_PARTITION_3336 | TREE3336_resp_1e+06 | 1.000000e+06 | 8.755950000000001e-07 | 5.281734976631e+00 | 8.755950000000001e-07 | 2.188987500000000e-07 | target only; no current source-backed scale input | false |
| TS3389_TREE3336_resp_1e+12 | TREE_PARTITION_3336 | TREE3336_resp_1e+12 | 1.000000e+12 | 8.755949999999999e-10 | 6.458500980981e+00 | 8.755949999999999e-10 | 2.188987500000000e-10 | target only; no current source-backed scale input | false |
| TS3389_TREE3336_resp_1e+16 | TREE_PARTITION_3336 | TREE3336_resp_1e+16 | 1.000000e+16 | 8.755950000000000e-12 | 7.136005555863e+00 | 8.755950000000000e-12 | 2.188987500000000e-12 | target only; no current source-backed scale input | false |

## Scale Scenario Runner
| scenario_id | label | kernel_branch | parent_signed | d_collar_over_ell | C_boundary | flux_envelope | epsilon_worldtube_mismatch | epsilon_boundary_tail | epsilon_boundary_total | ell_gradP | ell2_hessP | epsilon_kernel_moment | epsilon_gauge_readout | epsilon_kernel_total | strict_boundary_target | strict_kernel_target | strict_boundary_pass_like | strict_kernel_pass_like | why_nonclaim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SC3389_0_compact_exact_unsigned | compact exact if parent signed | compact | false | inf | 0.000000e+00 | 0.000000e+00 | 0.000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000e+00 | 0.000000e+00 | 0.000000e+00 | 0.000000e+00 | 0.000000000000000e+00 | 8.755950000000000e-12 | 8.755950000000000e-12 | true | true | hypothetical exact branch; parent not signed | false |
| SC3389_1_gaussian_d4_loose | Gaussian collar d/ell=4 with mild projector | gaussian | false | 4.000000e+00 | 1.000000e+00 | 0.000000e+00 | 0.000000e+00 | 3.354626279025119e-04 | 3.354626279025119e-04 | 1.000000e-06 | 1.000000e-06 | 0.000000e+00 | 0.000000e+00 | 2.000000000000000e-06 | 8.755950000000000e-12 | 8.755950000000000e-12 | false | false | useful for loose bounds, fails harsh local PPN targets | false |
| SC3389_2_gaussian_d6_mid | Gaussian collar d/ell=6 with tiny projector | gaussian | false | 6.000000e+00 | 1.000000e+00 | 0.000000e+00 | 0.000000e+00 | 1.522997974471263e-08 | 1.522997974471263e-08 | 1.000000e-10 | 1.000000e-10 | 0.000000e+00 | 0.000000e+00 | 2.000000000000000e-10 | 8.755950000000000e-12 | 8.755950000000000e-12 | false | false | near harsh boundary pressure but projector still too large for strict target | false |
| SC3389_3_gaussian_d7p2_clean | Gaussian collar d/ell=7.2 clean projector | gaussian | false | 7.200000e+00 | 1.000000e+00 | 0.000000e+00 | 0.000000e+00 | 5.534610071701014e-12 | 5.534610071701014e-12 | 1.000000e-12 | 1.000000e-12 | 1.000000e-12 | 1.000000e-12 | 4.000000000000000e-12 | 8.755950000000000e-12 | 8.755950000000000e-12 | true | true | passes strict smoke if flux/gauge remain zero-level | false |
| SC3389_4_gaussian_flux_fail | Gaussian collar good but physical flux 1e-9 | gaussian | false | 7.200000e+00 | 1.000000e+00 | 1.000000e-09 | 0.000000e+00 | 5.534610071701014e-12 | 1.005534610071701e-09 | 1.000000e-12 | 1.000000e-12 | 1.000000e-12 | 1.000000e-12 | 4.000000000000000e-12 | 8.755950000000000e-12 | 8.755950000000000e-12 | false | true | shows 3376 flux rows can dominate even with excellent collar | false |
| SC3389_5_gaussian_gauge_fail | Gaussian collar good but gauge defect 1e-8 | gaussian | false | 7.200000e+00 | 1.000000e+00 | 0.000000e+00 | 0.000000e+00 | 5.534610071701014e-12 | 5.534610071701014e-12 | 1.000000e-12 | 1.000000e-12 | 1.000000e-12 | 1.000000e-08 | 1.000300000000000e-08 | 8.755950000000000e-12 | 8.755950000000000e-12 | true | false | shows gauge/readout defect can dominate kernel channel | false |
| SC3389_6_high_Cboundary | Gaussian collar d/ell=7.2 but C_boundary=1e3 | gaussian | false | 7.200000e+00 | 1.000000e+03 | 0.000000e+00 | 0.000000e+00 | 5.534610071701013e-09 | 5.534610071701013e-09 | 1.000000e-12 | 1.000000e-12 | 1.000000e-12 | 1.000000e-12 | 4.000000000000000e-12 | 8.755950000000000e-12 | 8.755950000000000e-12 | false | true | operator normalization can erase apparent tail safety | false |

## Input Acquisition Ledger
| acquisition_id | quantity | derive_or_source | acceptance_rule | current_status | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ACQ3389_0_kernel_branch | kernel_branch | derive from parent readout/action, not from posterior test pressure | branch declared before using 3321/3387/3388 thresholds; compact branch regenerates transfer law | MISSING_PARENT_DECLARATION | choose/adopt compact local bump or keep Gaussian heat-kernel branch with tail scoring | false |
| ACQ3389_1_d_over_ell | d_collar/ell_s | same-frame local geometry: source-free collar radius divided by parent smoothing length | numeric positive value with source path and unit convention; for strict target with C_B=1 flux=0, d/ell must exceed target row | MISSING_NUMERIC_SCALE | define local PPN arena and smoothing length before scoring | false |
| ACQ3389_2_C_boundary | C_boundary | operator norm of boundary readout relative to EH PPN response | dimensionless bound; if >1, required d/ell increases by sqrt(2 log C_B) in quadrature | MISSING_OPERATOR_NORM | derive from readout map or keep conservative symbol in runner | false |
| ACQ3389_3_flux_envelope | epsilon_boundary_physical | 3376 B_zero_flux/Delta_symp/Phi_Poynting/corner/M_H_ref rows | zero theorem or finite absolute no-cancellation sum below remaining boundary target | MISSING_3376_FINITE_ROWS | route through 3376 package; do not hide Poynting/physical flux as gauge boundary | false |
| ACQ3389_4_projector_gradients | ell_s\|\|nabla P_PPN\|\| and ell_s^2\|\|nabla^2P_PPN\|\| | UOC normal-frame/PPN gauge readout derivative bounds | each term or their absolute sum below epsilon_kernel target after moment/gauge allocations | MISSING_PROJECTOR_DERIVATIVE_BOUNDS | derive P_PPN constancy through smoothing support or source gradient norms | false |
| ACQ3389_5_moment_gauge | epsilon_kernel_moment and epsilon_gauge_readout | kernel moment calculation and fixed PPN gauge/readout theorem | zero theorem or finite additive values below remaining kernel target | MISSING_MOMENT_AND_GAUGE_BOUNDS | prove normalized isotropic zero-moment kernel and fixed gauge/readout, or source values | false |

## Nonclaim Runner
| run_id | test | result | detail | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RUN3389_0_compact_audit | compact-kernel exact-zero adoption audit | PASS_CONDITIONAL_ROUTE_BLOCKED_CURRENT | compact bump can exist and zero collar tail, but branch switch requires parent declaration and transfer replacement | false | false |
| RUN3389_1_scale_schema | finite scale inputs represented | PASS_SCHEMA_NONCLAIM | kernel branch, d/ell, C_boundary, flux, projector gradients, moment and gauge rows exist | false | false |
| RUN3389_2_target_summary | target requirements summarized | PASS_TARGET_SUMMARY_NONCLAIM | unique_targets=8 | false | false |
| RUN3389_3_scenario_runner | placeholder scale scenarios evaluated against strict target | PASS_SMOKE_NONCLAIM | scenarios=7 strict_pass_like=2 | false | false |
| RUN3389_4_firewall | prevent boundary/kernel or local-GR claim | PASS_CLAIM_FIREWALL | pass-like scenario rows are hypothetical/nonclaim until inputs are source-backed or parent-signed | false | false |

## Promotion Gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| GATE3389_0_sources | all 3389 source paths exist and parse | true | source register validates 3388/3387/3376/3321/3320 inputs | false | false |
| GATE3389_1_compact_adopted | compact kernel branch is parent-adopted | false | compact branch is mathematically available but not parent-declared and would require transfer-law replacement | false | false |
| GATE3389_2_gaussian_values | Gaussian branch finite scale values are source-backed | false | d/ell, C_boundary, flux, projector gradients, moment and gauge values remain missing | false | false |
| GATE3389_3_runner_executes | scale scenario runner executes | true | placeholder scenarios evaluate boundary/kernel totals against strict targets | false | false |
| GATE3389_4_boundary_kernel_pass | epsilon_boundary and epsilon_kernel are claim-valid | false | no source-backed exact-zero or finite values; scenarios are nonclaim | false | false |
| GATE3389_5_local_ppn | local PPN/local-GR branch passes from 3389 | false | 3389 is a scale-input runner and compact-kernel audit only | false | false |

## Decision Ledger
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3389_0_progress | Boundary/kernel epsilons are now executable scale constraints. | strict rows require d_collar/ell_s up to about 7.136 for C_boundary=1, flux=0, and kernel terms down to 8.756e-12. | source or derive actual scale inputs, or parent-adopt compact kernel and replace Gaussian transfer law | false |
| DEC3389_1_compact | Compact kernel is a clean exact-zero theorem route but cannot be silently swapped in. | it changes the Gaussian transfer law used by 3321/3386/3388 and needs parent declaration. | if compact is chosen, build compact-kernel transfer replacement before scoring | false |
| DEC3389_2_gaussian | Gaussian branch remains viable only as a finite scale-separation claim. | collar tail can be tiny at d/ell around 7 for C_boundary=1, but flux, C_boundary, projector, moment and gauge defects can dominate. | define local PPN arena and get d/ell, C_boundary, projector derivative and gauge/moment values | false |
| DEC3389_3_best_next | Best next move is a concrete local-arena scale acquisition pass, not background-gradient yet. | without actual d/ell and projector-gradient values, epsilon_boundary/kernel cannot be inserted into the Cassini-style runner. | build 3390 local scale acquisition or compact transfer replacement | false |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3389_0_sources_exist_parse | all cited 3389 source paths exist and parse | true |  |
| VAL3389_1_outputs_parse | all generated CSV outputs parse cleanly | true | parsed=10 expected=10 |
| VAL3389_2_compact_audit | compact audit allows route but blocks current adoption | true |  |
| VAL3389_3_scale_schema | scale schema covers all required 3388 scale inputs | true |  |
| VAL3389_4_target_summary | target summary rows exist for response products | true | rows=8 |
| VAL3389_5_scenarios | scenario runner includes compact, clean Gaussian, and failure modes | true |  |
| VAL3389_6_runner | runner records compact audit, schema, target summary, smoke scenarios and firewall | true |  |
| VAL3389_7_gates | gates block compact adoption, Gaussian values, boundary/kernel claim and local PPN while runner executes | true |  |
| VAL3389_8_no_overclaim_flags | all generated rows with valid_for_claim remain false | true |  |
| VAL3389_9_next_target | next target moves to local scale acquisition or compact transfer replacement | true |  |
| VAL3389_10_write_scope_outside_formalization | no 3389 files were written under formalization-workbench | true | hits=0 |
| VAL3389_11_overall | 3389 validation overall | true | all required checks passed |

## Next Target
| target_id | target_script | objective | why_next | valid_for_claim |
| --- | --- | --- | --- | --- |
| 3390-Y5-R2FR-local-scale-acquisition-or-compact-kernel-transfer-replacement-under-AX1090.md | scripts/Y5_R2FR_3390_local_scale_acquisition_or_compact_kernel_transfer_replacement.py | choose a concrete local PPN arena and source/derive d_collar/ell_s, C_boundary, projector-gradient norms, kernel moment and gauge defect; if compact kernel is adopted, replace Gaussian T_grad/threshold rows with compact-kernel transfer bounds | 3389 runner shows these concrete values decide whether boundary/kernel epsilon channels can enter a real Cassini/local-GR pass | false |
| 3391-Y5-R2FR-background-gradient-and-Tgrad-scale-bound-under-AX1090.md | scripts/Y5_R2FR_3391_background_gradient_and_Tgrad_scale_bound.py | derive or source epsilon_bg_PPN and ell_s/lambda_PPN after boundary/kernel scale inputs are handled | once boundary/kernel are zeroed or bounded, epsilon_bg*T_grad is the remaining epsilon_eff channel | false |
