# 2393 - vertical Noether charge Qv extraction or kernel-charge source row

## Result

2393 attacks the vertical charge object selected by 2392.

The formal extraction route is:

1. Parent variation:
   `delta L_parent = E_A delta Phi^A + dTheta_parent(Phi;delta Phi)`.
2. For a parent vertical generator `v_epsilon`, derive
   `delta_v L_parent = dmu_v + E_A v^A`.
3. Define the vertical Noether current:
   `J_v := Theta_parent(v_epsilon) - mu_v`.
4. Decompose on shell:
   `J_v = dQ_v + C_v`.
5. Test the compact local kernel Hamiltonian:
   `delta H_v[S] = integral_S(delta Q_v - i_v Theta_parent + delta B_v)`.

If that object is finite, integrable, and zero on the allowed compact local surfaces, the vertical kernel can pass the
presymplectic-null part of 2392.  If not, the kernel carries a real charge residual.

Current MTS does not yet provide the total parent action, `Theta_parent`, vertical generator action on all fields,
`mu_v`, `Q_v`, sector split, boundary convention `B_v`, zero compact flux, integrability, or positive same-frame
`M_H_ref`.

So 2393 is a formal extraction contract, not a `Q_v` extraction claim.  No vertical-kernel-nullness pass, parent
`q/Obs_e` pass, same-frame pass, local-GR pass, Newton pass, PPN, clock, orbital, R10, or public/GitHub claim is made.

## Source Register

| row_id | source_key | source_path | exists | needles_found | source_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2393_00_2392_doc | 2392_charge_handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2392-Y5-R2FR-vertical-kernel-presymplectic-null-and-matter-invisible-or-kernel-charge-row.md | true | true | 2392 selects vertical Noether charge extraction | false |
| SRC2393_01_2392_certificates | 2392_vertical_kernel_certificates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2392_VERTICAL_KERNEL_CERTIFICATE.csv | true | true | Theta/Qv and compact-flux gaps | false |
| SRC2393_02_2392_leaks | 2392_kernel_charge_leaks | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2392_KERNEL_CHARGE_LEAK_VALUES.csv | true | true | kernel-charge leak schema to refine | false |
| SRC2393_03_1008_doc | 1008_theta_Qtau_extraction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md | true | true | parent symplectic potential and Noether charge extraction precedent | false |
| SRC2393_04_1007_doc | 1007_Htau_integrability | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md | true | true | Hamiltonian integrability blocked by missing parent theta/Q | false |
| SRC2393_05_771_owner_audit | 771_theta_Qtau_owner_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv | true | true | machine owner audit for parent variation and Noether current | false |
| SRC2393_06_771_noether_test | 771_noether_extraction_test | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_771_NOETHER_EXTRACTION_TEST.csv | true | true | vertical/representative Noether extraction test | false |
| SRC2393_07_583_momentum_map | 583_momentum_map_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv | true | true | Noether momentum-map and boundary-zero contract | false |
| SRC2393_08_parent_noether_chain | parent_noether_chain | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv | true | true | parent Noether charge closure chain | false |
| SRC2393_09_1008_variation_audit | 1008_parent_variation_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv | true | true | parent action/theta extraction audit | false |
| SRC2393_10_1008_piece_ledger | 1008_charge_piece_ledger | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv | true | true | current charge pieces not extracted | false |
| SRC2393_11_993_qtau_ledger | 993_Qtau_decomposition | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv | true | true | Q_tau decomposition precedent and missing pieces | false |

## Vertical Noether Charge Theorem

| row_id | step | statement | derivation_status | current_gain | remaining_gap | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| VNC2393_0_parent_variation | parent variation | Start from a parent local form L_parent with delta L_parent = E_A delta Phi^A + dTheta_parent(Phi;delta Phi). Without this, no vertical Noether charge is owned. | CONDITIONAL_VARIATION_IDENTITY | identifies the minimum object required before any Q_v extraction | explicit total L_parent and Theta_parent across EH/matter/extra/projector/boundary sectors are missing | false |
| VNC2393_1_vertical_current | vertical Noether current | For a parent vertical generator v_epsilon, if delta_v L_parent = dmu_v + E_A v^A, define J_v := Theta_parent(v_epsilon) - mu_v. On shell dJ_v=0. | CONDITIONAL_NOETHER_CURRENT | turns a vertical kernel direction into a charge-bearing or charge-silent current test | v_epsilon, mu_v, and action on all parent fields are not supplied | false |
| VNC2393_2_charge_decomposition | vertical charge decomposition | The kernel is Noether-null only if J_v = dQ_v + C_v with C_v proportional to constraints, and the allowed compact local charge integral of Q_v plus improvements vanishes. | CONDITIONAL_CHARGE_DECOMPOSITION | gives a precise route from parent symmetry to zero kernel charge | Q_v, C_v, improvement B_v, and compact boundary conditions are not extracted | false |
| VNC2393_3_kernel_Hamiltonian | kernel Hamiltonian variation | For the 2392 kernel test, require delta H_v[S] = integral_S(delta Q_v - i_v Theta_parent + delta B_v) to be finite, integrable, and zero on the allowed local surfaces. | CONDITIONAL_KERNEL_HAMILTONIAN_TEST | matches the exact epsilon_kernel_charge numerator instead of handwaving gauge | integrability, B_v convention, surface class, denominator, and zero-flux proof are missing | false |
| VNC2393_4_piece_split | sector piece split | Q_v must split into EH/reference, matter/source, extra/residual, projector, and boundary pieces; every piece must vanish by theorem or be included in epsilon_kernel_charge. | REQUIRED_SECTOR_LEDGER | prevents hiding extra-sector or boundary charge inside a total-zero slogan | piecewise vertical charge extraction is absent | false |
| VNC2393_5_verdict | current verdict | 2393 derives the formal vertical Noether charge contract but does not extract Q_v for current MTS. The kernel-charge row remains nonclaim until parent L, Theta_parent, mu_v, Q_v, B_v, constraints, and M_H_ref are sourced. | ROUTE_EXACT_NOT_CLAIMED | the next bottleneck is a sector-by-sector parent variation ledger for vertical v | no Q_v pass, no kernel-nullness pass | false |

## Vertical Qv Certificate

| row_id | certificate | required_test | status | residual_if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| VQC2393_0_L_parent | explicit total parent action | write L_parent including EH/local geometry, matter/source, extra/residual, projector, boundary/reference, and coupling sectors | MISSING_TOTAL_PARENT_ACTION | epsilon_kernel_charge | false |
| VQC2393_1_Theta_parent | parent symplectic potential | derive Theta_parent from delta L_parent = E delta Phi + dTheta_parent with all sector contributions | MISSING_THETA_PARENT | epsilon_kernel_charge | false |
| VQC2393_2_v_generator | vertical generator action | define v_epsilon on every parent field and prove it is the tested element of ker(Dq) | MISSING_VERTICAL_GENERATOR_ACTION | epsilon_q_rank_or_integrability | false |
| VQC2393_3_mu_v | Noether improvement mu_v | derive delta_v L_parent = dmu_v + E_A v^A and fix improvement ambiguity | MISSING_MU_V_IMPROVEMENT | epsilon_kernel_charge | false |
| VQC2393_4_Qv | vertical charge form Q_v | derive J_v = Theta_parent(v)-mu_v = dQ_v + C_v and list all sector pieces | MISSING_VERTICAL_QV | epsilon_kernel_charge | false |
| VQC2393_5_Bv_boundary | boundary/improvement convention | fix B_v/counterterm/reference convention and prove allowed dB improvements have zero compact local flux | MISSING_BV_BOUNDARY_CONVENTION | epsilon_boundary_history | false |
| VQC2393_6_zero_flux | zero compact kernel flux | prove integral_S(delta Q_v - i_v Theta_parent + delta B_v)=0 on linked local surfaces or source-bound it | MISSING_ZERO_KERNEL_FLUX | epsilon_kernel_charge | false |
| VQC2393_7_MHref | positive same-frame M_H_ref | derive same-frame denominator before normalizing kernel charge | MISSING_POSITIVE_SAME_FRAME_MHREF | kernel charge cannot be scored | false |

## Kernel Charge Source Rows

| row_id | quantity | formula | units | current_value | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| VQL2393_0_kernel_charge | epsilon_kernel_charge | abs(integral_S(delta Q_v - i_v Theta_parent + delta B_v + C_v_piece))/M_H_ref | dimensionless Hamiltonian charge leakage | MISSING_THETA_PARENT;MISSING_Q_V;MISSING_B_V;MISSING_C_V;MISSING_ZERO_FLUX_CERTIFICATE;MISSING_M_H_REF | false | false |
| VQL2393_1_theta_piece | epsilon_theta_piece_missing | abs(integral_S i_v(Theta_EH+Theta_matter+Theta_extra+Theta_projector+Theta_boundary)_missing)/M_H_ref | dimensionless | MISSING_SECTOR_THETA_SPLIT;MISSING_M_H_REF | false | false |
| VQL2393_2_Qv_piece | epsilon_Qv_piece_missing | abs(integral_S (Q_v_EH+Q_v_matter+Q_v_extra+Q_v_projector+Q_v_boundary)_missing)/M_H_ref | dimensionless | MISSING_QV_SECTOR_LEDGER;MISSING_M_H_REF | false | false |
| VQL2393_3_improvement_ambiguity | epsilon_Bv_ambiguity | abs(integral_S delta B_v_unfixed)/M_H_ref | dimensionless | MISSING_BV_CONVENTION;MISSING_REFERENCE_LOCK;MISSING_M_H_REF | false | false |
| VQL2393_4_integrability | epsilon_Hv_integrability | curl_fieldspace integral_S(delta Q_v - i_v Theta_parent + delta B_v)/M_H_ref | dimensionless field-space curl | MISSING_FIELDSPACE_CURL_TEST;MISSING_SURFACE_CLASS;MISSING_M_H_REF | false | false |
| VQL2393_5_total | Delta_vertical_Noether_charge_total_over_MH | epsilon_kernel_charge + epsilon_theta_piece_missing + epsilon_Qv_piece_missing + epsilon_Bv_ambiguity + epsilon_Hv_integrability | dimensionless | COMPONENTS_MISSING | false | false |

## Decision Ledger

| row_id | decision | reason | consequence | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC2393_0_accept_formal_contract | accept vertical Noether charge extraction contract | the covariant phase-space shape J_v=Theta_parent(v)-mu_v=dQ_v+C_v is the correct charge test for kernel nullness | kernel nullness can no longer be claimed without Q_v and compact flux control | CONDITIONAL_VERTICAL_CHARGE_CONTRACT_ACCEPTED | false |
| DEC2393_1_no_promotion | do not promote Q_v extraction for current MTS | total parent action, Theta_parent, v action, mu_v, Q_v, B_v, sector split, zero flux, integrability, and M_H_ref remain missing | vertical kernel nullness and q/Obs_e promotion remain blocked | VERTICAL_QV_NOT_EXTRACTED | false |
| DEC2393_2_next | attack sector-by-sector parent variation ledger next | without sector Theta/Qv pieces, Q_v is only a formal symbol | 2394 should build the vertical sector variation ledger or keep Qv piece leaks nonclaim | SELECT_2394_VERTICAL_SECTOR_VARIATION_LEDGER | false |

## Claim Gates

| row_id | gate | gate_status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2393_0_formal_shape | vertical Noether charge formal shape | PASS_CONDITIONAL_THEOREM_ONLY | use as extraction contract, not current-MTS proof | false |
| CG2393_1_parent_variation | total L_parent and Theta_parent extracted | FAIL | Q_v not owned | false |
| CG2393_2_Qv_sector_split | Q_v sector split and constraints extracted | FAIL | kernel charge cannot be zeroed | false |
| CG2393_3_zero_flux | zero compact vertical flux | FAIL | epsilon_kernel_charge remains live | false |
| CG2393_4_MHref | positive same-frame M_H_ref | FAIL | kernel charge cannot be scored | false |
| CG2393_5_GR_Newton | local GR/Newton from vertical Q_v | BLOCKED | no GR/Newton reduction claim from 2393 | false |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2393_0_claim_Qv_extracted | vertical Q_v is extracted for current MTS | false | L_parent, Theta_parent, v action, mu_v, Q_v, sector split, boundary convention, and M_H_ref are missing | VQC2393_0_L_parent;VQC2393_1_Theta_parent;VQC2393_4_Qv;VQC2393_7_MHref | false |
| REF2393_1_claim_zero_flux | vertical kernel charge vanishes | false | formal Noether shape does not prove compact flux zero or integrability | VQC2393_5_Bv_boundary;VQC2393_6_zero_flux;VQL2393_4_integrability | false |
| REF2393_2_EH_import | EH Noether charge alone supplies MTS vertical Q_v | false | EH charge can be a reference only after MTS parent reduction and silent-sector clauses are signed | VQC2393_0_L_parent;VQC2393_4_Qv;VQL2393_2_Qv_piece | false |
| REF2393_3_claim_GR_Newton | local GR/Newton follows from formal vertical Noether machinery | false | Q_v extraction is only one upstream lock; q/Obs_e, source charge, M_H_ref, EH exterior, Poisson/Gauss, PPN, and boundary locks remain required | CG2393_5_GR_Newton;VQC2393_7_MHref | false |

## Next Target

| row_id | next_file | success_condition | fallback_condition | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2393_0_selected | 2394-Y5-R2FR-vertical-sector-variation-ledger-or-Qv-piece-leak-rows.md | derive sector pieces of Theta_parent(v), mu_v, Q_v and constraints for EH/local geometry, matter/source, extra/residual, projector, and boundary/reference sectors | fill epsilon_theta_piece_missing and epsilon_Qv_piece_missing with sector source paths and valid_for_claim=false | false |
| NEXT2393_1_parallel | 2394b-Y5-R2FR-Bv-boundary-improvement-convention-or-compact-flux-bound.md | fix B_v/reference convention and prove zero compact local flux | fill epsilon_Bv_ambiguity and epsilon_kernel_charge boundary-improvement terms | false |
| NEXT2393_2_parallel | 2394c-Y5-R2FR-Hv-integrability-fieldspace-curl-or-kernel-Hamiltonian-bound.md | prove delta H_v is integrable and zero for vertical kernel directions | fill epsilon_Hv_integrability with field-space curl/source rows | false |

## Validation

| row_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL2393_00_sources_exist | PASS | all required source paths exist | false |
| VAL2393_01_needles_found | PASS | all source needles found | false |
| VAL2393_02_parent_variation_present | PASS | parent variation identity is present | false |
| VAL2393_03_vertical_current_present | PASS | vertical Noether current formula is present | false |
| VAL2393_04_kernel_charge_present | PASS | kernel Hamiltonian variation test is present | false |
| VAL2393_05_required_gaps_explicit | PASS | L/theta/v/mu/Qv/Bv/flux/MHref gaps explicit | false |
| VAL2393_06_value_rows_nonready | PASS | kernel charge source rows remain non-score-ready | false |
| VAL2393_07_global_claims_blocked | PASS | global/local gates remain blocked | false |
| VAL2393_08_csv_parse | PASS | generated CSVs parse and have rows | false |
| VAL2393_09_no_claim_flags | PASS | no generated row has valid_for_claim=true | false |
| VAL2393_10_formalization_untouched_by_script | PASS | script writes only post-checkpoint-work outputs | false |
| VAL2393_11_next_selected | PASS | vertical sector variation ledger selected next | false |
| VAL2393_OVERALL | PASS | 2393 states the vertical Noether charge extraction contract, refuses Qv/zero-flux claims without sector parent variation, and selects sector variation ledger next | false |

## Practical Status

This is another useful narrowing.  The project now knows exactly what a non-smuggled kernel proof needs: not a word
like gauge, but a sector-derived `Q_v` with zero compact flux.  The next lock is sector bookkeeping: EH/local geometry,
matter/source, extra/residual, projector, and boundary/reference pieces must each be varied or retained as explicit
leaks.
