# 1017 Y5 R10 Hamiltonian PiM reference lock or MHref first row

**Status:** `FB554_0` is now split into the exact reference-lock law: integrability curl, fixed reference, symplectic/boundary flux, tau lock, and a stable same-frame `M_H_ref` denominator. Current MTS does not prove those pieces zero and has no source-backed first row.

**Claim ceiling:** no stable Hamiltonian source charge, `M_H_ref`, `R_eq` scoring, measured-GM closure, Newton/GR reduction, R10/R11 pass, PPN pass, or local-GR claim is allowed from 1017.

## Source register
| source_id | source_path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC1017_0_1016_next | source-intake/mts_residuals/P8_Y5_R10_1016_NEXT_TARGET.csv | true | true | 1016 handoff target. |
| SRC1017_1_1016_schema | source-intake/mts_residuals/P8_Y5_R10_1016_FIRST_INPUT_SCHEMA.csv | true | true | 1016 first input schema. |
| SRC1017_2_1016_selector | source-intake/mts_residuals/P8_Y5_R10_1016_PARENT_SELECTOR_CONTRACT.csv | true | true | 1016 selector denominator contract. |
| SRC1017_3_664_integrability | source-intake/mts_residuals/P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv | true | true | 664 integrability attempt. |
| SRC1017_4_664_fill | source-intake/mts_residuals/P8_Y5_R10_664_FIRST_RESIDUAL_FILL.csv | true | true | 664 first residual fill row. |
| SRC1017_5_554_integrability | source-intake/mts_residuals/P8_Y5_HAMILTONIAN_CHARGE_INTEGRABILITY_REFERENCE_ATTEMPT.csv | true | true | 554 integrability reference attempt. |
| SRC1017_6_554_fill | source-intake/mts_residuals/P8_Y5_HAMILTONIAN_INTEGRABILITY_SOURCE_EQUALITY_FILL_ROWS.csv | true | true | 554 fill row. |
| SRC1017_7_665_zero | source-intake/mts_residuals/P8_Y5_R10_665_THEOREM_ZERO_ATTEMPT.csv | true | true | 665 theorem-zero attempt. |
| SRC1017_8_665_fill | source-intake/mts_residuals/P8_Y5_R10_665_FIRST_FILL_ROW_STAGED.csv | true | true | 665 first fill row staged. |
| SRC1017_9_666_parent_lock | source-intake/mts_residuals/P8_Y5_R10_666_PARENT_LOCK_ATTEMPT.csv | true | true | 666 parent boundary/reference lock attempt. |
| SRC1017_10_666_hunt | source-intake/mts_residuals/P8_Y5_R10_666_FB5540_SOURCE_VALUE_HUNT_LEDGER.csv | true | true | 666 source value hunt ledger. |
| SRC1017_11_667_variation | source-intake/mts_residuals/P8_Y5_R10_667_VARIATION_LEDGER.csv | true | true | 667 variation ledger. |
| SRC1017_12_667_terms | source-intake/mts_residuals/P8_Y5_R10_667_FB5540_TERM_MAP.csv | true | true | 667 FB5540 term map. |
| SRC1017_13_667_fallback | source-intake/mts_residuals/P8_Y5_R10_667_RESIDUAL_FALLBACK_ROWS.csv | true | true | 667 residual fallback rows. |

## Reference-lock law
| lock_id | required_lock | mathematical_form | current_status | failure_if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| HRL1017_0_variation_formula | Hamiltonian variation is defined by covariant phase space | delta H_tau[S] = integral_S(delta Q_tau^MTS - i_tau Theta_total) - delta H_ref[S] | conditional_formal_step | formal definition only; not an integrability theorem | false |
| HRL1017_1_integrability_curl | field-space curl of delta H_tau vanishes | I_tau(delta1,delta2)=integral_S i_tau omega_total + curl(delta H_ref)=0 | fail_current_claim | L_X, Theta_X, Q_X, reference curl, tau/domain/projector variations are not computed | false |
| HRL1017_2_reference_lock | reference subtraction is fixed once and derivative-silent | partial_{source,r,t,frame,lambda} Delta_ref = 0 | fail_current_claim | B_ref is named but not selected by a current parent principle | false |
| HRL1017_3_boundary_flux_zero | extra symplectic/boundary/projector leakage is zero or fixed | integral_boundary(delta Q_tau^extra - i_tau Theta_extra)+delta B_class = 0 | fail_current_claim | boundary class/nohair and projector silence remain unsigned | false |
| HRL1017_4_tau_lock | one observed time generator is used by source, charge, clocks, and readout | tau_source = tau_charge = tau_clock = tau_readout and delta tau = 0 | fail_current_claim | observed coframe/matter functor selecting tau is not parent-derived | false |
| HRL1017_5_MHref_denominator | M_H_ref is a positive same-frame dressed source denominator | M_H_ref = G_ref^-1 integral_S Q_tau^MTS, with same tau and observed frame | fail_current_claim | worldtube source equality and Poisson/Gauss/orbital readout remain downstream | false |
| HRL1017_6_FB5540_zero_law | FB554_0 vanishes componentwise | epsilon_HPiM_integrability_abs = \|delta_H_tau_nonintegrable\|/M_H_ref + \|Delta_ref\|/M_H_ref + \|symplectic_boundary_flux\|/M_H_ref = 0 | fail_current_claim | at least integrability curl, reference lock, boundary flux, tau lock, and denominator remain unsigned | false |

## Theorem attempt
| attempt_id | claim | current_status | would_close | current_blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| HPT1017_0_EH_reference | EH with stationary boundary conditions has a known conditional integrable charge route | known_conditional_reference | shows the route is mathematically legitimate | MTS has not inherited the EH symplectic charge sector-by-sector | false |
| HPT1017_1_parent_theta_Qtau | current MTS supplies explicit L_X, Theta_X, Q_X, and C_tau decomposition | not_derived | would make the integrability curl computable instead of schematic | sector Lagrangian owner is missing | false |
| HPT1017_2_reference_superselection | B_ref is selected by parent branch/topology/fixed stationarity and cannot absorb source calibration | not_derived | would zero or bound Delta_ref_over_MH without reference-only cheating | parent reference functional remains missing | false |
| HPT1017_3_boundary_class_nohair | B_class/C_top/chi_B are parent-owned and carry no compact linked mass flux | not_derived | would zero symplectic_boundary_flux and B_zero_flux terms | boundary class selection and projector silence are unsigned | false |
| HPT1017_4_denominator_guard | M_H_ref is not orbital GM, bare mass, or reference-only normalization | guardrail_pass_no_denominator_theorem | prevents circular normalization of R_eq and FB554_0 rows | source-measure equality and Gauss/orbital readout are downstream | false |
| HPT1017_5_verdict | Hamiltonian PiM reference/integrability lock is signed for current MTS | fail_current_claim | would open the first stable source-charge gate | not signed; use source-ready row schema or sector-owner target | false |

## MHref first-row schema
| row_id | quantity | definition | required_columns | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| MHR1017_0_M_H_ref_denominator | M_H_ref | positive dressed source charge denominator from same-frame Hamiltonian/Noether charge | system_id;tau_id;surface_outer;Q_tau_integral;G_ref;H_ref;M_H_ref;units;reference_rule;source_path;assumptions;valid_for_claim | MISSING_STABLE_MH_REF | false |
| MHR1017_1_delta_H_tau_nonintegrable | delta_H_tau_nonintegrable_over_MH | field-space curl obstruction of the Hamiltonian source charge normalized by M_H_ref | system_id;surface_pair;field_variation_pair;integrability_curl;M_H_ref;units;source_path;assumptions;valid_for_claim | MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO | false |
| MHR1017_2_Delta_ref | Delta_ref_over_MH;H_ref_shift | reference subtraction shift and derivative profile normalized by M_H_ref | system_id;reference_branch;surface_pair;Delta_ref;H_ref_shift;M_H_ref;derivative_profile;units;source_path;assumptions;valid_for_claim | MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO | false |
| MHR1017_3_symplectic_boundary_flux | symplectic_boundary_flux_over_MH;B_zero_flux;Delta_symp | boundary/projector/non-EH symplectic leakage through linked surfaces normalized by M_H_ref | system_id;surface_pair;boundary_rule;symplectic_boundary_flux;B_zero_flux;Delta_symp;M_H_ref;units;source_path;assumptions;valid_for_claim | MISSING_SYMPLECTIC_BOUNDARY_NUMERIC_OR_THEOREM_ZERO | false |
| MHR1017_4_tau_lock | time_generator_lock | certificate or bounded mismatch for tau_source=tau_charge=tau_clock=tau_readout | system_id;tau_source;tau_charge;tau_clock;tau_readout;mismatch_bound;units;source_path;assumptions;valid_for_claim | MISSING_TAU_LOCK_CERTIFICATE | false |
| MHR1017_5_FB5540_total | epsilon_HPiM_integrability_abs | no-cancellation total for FB554_0 with denominator and every numerator component present | system_id;epsilon_HPiM_integrability_abs;component_sum_abs;M_H_ref;normalization;source_path;assumptions;valid_for_claim | NOT_COMPUTED_COMPONENTS_MISSING | false |

## First-row runner
| runner_id | row_id | quantity | computed_status | claim_allowed | failure_reasons |
| --- | --- | --- | --- | --- | --- |
| MRR1017_0_M_H_ref_denominator | MHR1017_0_M_H_ref_denominator | M_H_ref | blocked_missing_inputs | false | MISSING_THEOREM_OR_SOURCE_INPUT;VALID_FOR_CLAIM_FALSE |
| MRR1017_1_delta_H_tau_nonintegrable | MHR1017_1_delta_H_tau_nonintegrable | delta_H_tau_nonintegrable_over_MH | blocked_missing_inputs | false | MISSING_THEOREM_OR_SOURCE_INPUT;VALID_FOR_CLAIM_FALSE |
| MRR1017_2_Delta_ref | MHR1017_2_Delta_ref | Delta_ref_over_MH;H_ref_shift | blocked_missing_inputs | false | MISSING_THEOREM_OR_SOURCE_INPUT;VALID_FOR_CLAIM_FALSE |
| MRR1017_3_symplectic_boundary_flux | MHR1017_3_symplectic_boundary_flux | symplectic_boundary_flux_over_MH;B_zero_flux;Delta_symp | blocked_missing_inputs | false | MISSING_THEOREM_OR_SOURCE_INPUT;VALID_FOR_CLAIM_FALSE |
| MRR1017_4_tau_lock | MHR1017_4_tau_lock | time_generator_lock | blocked_missing_inputs | false | MISSING_THEOREM_OR_SOURCE_INPUT;VALID_FOR_CLAIM_FALSE |
| MRR1017_5_FB5540_total | MHR1017_5_FB5540_total | epsilon_HPiM_integrability_abs | blocked_missing_inputs | false | MISSING_THEOREM_OR_SOURCE_INPUT;VALID_FOR_CLAIM_FALSE |

## Claim gate
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1017_0_reference_lock_written | Hamiltonian reference/integrability lock is explicit | true | HRL1017 rows split variation, curl, reference, boundary, tau, denominator, and total law | false | false |
| CG1017_1_integrability_zero | delta_H_tau_nonintegrable_over_MH is theorem-zero | false | L_X/Theta_X/Q_X and integrability curl are not computed | false | false |
| CG1017_2_reference_zero | Delta_ref_over_MH and H_ref_shift are theorem-zero | false | B_ref is not parent-selected and derivative-silent | false | false |
| CG1017_3_boundary_zero | symplectic boundary flux, B_zero_flux, and Delta_symp are theorem-zero | false | boundary class/nohair/projector silence are unsigned | false | false |
| CG1017_4_MHref_claim | M_H_ref is a stable same-frame denominator | false | source-measure equality and Gauss/orbital readout remain downstream | false | false |
| CG1017_5_first_row_claim_ready | M_H_ref plus FB554_0 numerator rows are source-backed and normalized | false | all first-row schema entries are missing/nonclaim | false | false |
| CG1017_6_Newton_local_GR | Newton/local-GR gates can reopen | false | stable Hamiltonian source charge is not derived | false | false |
| CG1017_7_guardrail | Hamiltonian reference-lock guardrail is installed | true | no reference-only zero, bare mass denominator, or unnormalized R_eq scoring is allowed | false | false |

## Decision ledger
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC1017_0_reference_lock | FB554_0 is still the right first hard local-GR source-charge lock. | without integrable H_tau, fixed H_ref, zero boundary/symplectic flux, tau lock, and stable M_H_ref, Pi_M^H is only notation. | derive the missing sector Lagrangian/boundary owners or keep first-row source hunt nonclaim | false |
| DEC1017_1_no_MHref_shortcut | M_H_ref cannot be replaced by orbital GM, bare mass, or reference-only 1. | that would normalize the obstruction with the readout the theorem is supposed to derive. | require Q_tau integral plus fixed reference before scoring R_eq or FB554_0 | false |
| DEC1017_2_first_row_schema | The first source-backed row must include denominator and numerator pieces together. | delta_H_tau_nonintegrable, Delta_ref, and boundary flux are meaningless as evidence without M_H_ref and no-cancellation bookkeeping. | do not run R10/R11/local comparisons until all FB554_0 components are real | false |
| DEC1017_3_next_target | The next root target is sector Lagrangian/boundary owner or first FB554_0 source row. | 667 shows the exact missing owners: L_X/Theta_X/Q_X, B_ref, B_class/C_top/chi_B, tau, and source readout. | 1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md | false |

## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V1017_SUMMARY | pass | 1017 Hamiltonian PiM reference-lock/MHref validation summary | 2026-06-14T05:04:55.088661+00:00 |
| V1017_0_sources_exist | pass | all source paths exist and needles are present | 2026-06-14T05:04:55.088616+00:00 |
| V1017_1_lock_split_complete | pass | reference lock splits integrability, reference, boundary, tau, denominator, and total law | 2026-06-14T05:04:55.088628+00:00 |
| V1017_2_lock_blocks_claim | pass | FB554_0 zero law remains nonclaim | 2026-06-14T05:04:55.088631+00:00 |
| V1017_3_theorem_attempt_complete | pass | theorem attempt records current failure | 2026-06-14T05:04:55.088634+00:00 |
| V1017_4_denominator_guard | pass | M_H_ref guardrail is explicit | 2026-06-14T05:04:55.088637+00:00 |
| V1017_5_first_row_schema_complete | pass | first row schema covers denominator and all FB554_0 numerator terms | 2026-06-14T05:04:55.088639+00:00 |
| V1017_6_first_row_schema_nonclaim | pass | all first row schema entries remain missing and nonclaim | 2026-06-14T05:04:55.088642+00:00 |
| V1017_7_runner_refuses | pass | runner refuses missing first row entries | 2026-06-14T05:04:55.088644+00:00 |
| V1017_8_claim_gates_blocked | pass | reference, M_H_ref, Newton, and local-GR claims remain blocked | 2026-06-14T05:04:55.088647+00:00 |
| V1017_9_guardrail_written | pass | Hamiltonian reference-lock guardrail is installed | 2026-06-14T05:04:55.088649+00:00 |
| V1017_10_decision_written | pass | 1018 root target decision is written | 2026-06-14T05:04:55.088652+00:00 |
| V1017_11_next_target_written | pass | 1018 target row is present and nonclaim | 2026-06-14T05:04:55.088654+00:00 |
| V1017_12_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T05:04:55.088657+00:00 |

## Next target
| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md | derive L_X/Theta_X/Q_X plus B_ref/B_class/tau ownership for the Hamiltonian source charge, or fill a source-backed FB554_0 row with M_H_ref and all numerator components | L_X, Theta_X, Q_X, omega_X, B_ref, B_class, C_top, chi_B, tau lock, M_H_ref, delta_H_tau_nonintegrable, Delta_ref, symplectic_boundary_flux, source paths | reference-only zero, bare mass denominator, orbital GM denominator, unnormalized R_eq, cancellation between unknowns, Newton/local-GR claim, GitHub action | false |

