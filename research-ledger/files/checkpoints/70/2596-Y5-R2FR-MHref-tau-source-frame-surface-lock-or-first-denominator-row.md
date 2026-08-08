# 2596 Y5 R2FR MHref tau source-frame surface lock or first denominator row

**Status:** private nonclaim derivation checkpoint. The denominator/source-frame schema is strict, but current MTS still does not parent-sign `M_H_ref`, one tau, one observed coframe, or fixed linked surfaces.

**Main result:** the PiM equality and commutator rows cannot be scored until `M_H_ref=H_tau-H_ref` is positive, same-frame, source-backed, noncircular, and tied to fixed `S1/S2/A_ext` surfaces in one q/e_obs/tau branch. Orbital `GM`, EH-only charge, post-readout surfaces, and fitted references are rejected.

## Source Register
| source_id | source_path | exists | missing_needles | source_pass | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2596_00_2595_handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2595-Y5-R2FR-GM-transfer-PiM-equality-commutator-or-source-normalization-bound.md | true |  | true | active handoff selecting M_H_ref/tau/surface lock | false |
| SRC2596_01_2595_next_queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2595_MHREF_TAU_FRAME_LOCK_NEXT.csv | true |  | true | machine-readable 2596 task and guardrails | false |
| SRC2596_02_1519_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1519-Y5-parent-observed-coframe-tau-source-frame-lock-or-MHref-first-row.md | true |  | true | prior M_H_ref first-row schema and observed-frame/tau lock | false |
| SRC2596_03_1519_schema | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_FRAME_1519_MHREF_FIRST_ROW_SCHEMA.csv | true |  | true | machine M_H_ref first-row schema | false |
| SRC2596_04_1519_acquisition | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_FRAME_1519_DENOMINATOR_ACQUISITION_LEDGER.csv | true |  | true | denominator/source acquisition ledger | false |
| SRC2596_05_1518_mhref_surface | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_PIM_1518_MHREF_SURFACE_LOCK.csv | true |  | true | PiM commutator denominator/surface lock rows | false |
| SRC2596_06_2390_same_frame | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2390-Y5-R2FR-observed-coframe-pullback-same-frame-lock-or-frame-source-leak-values.md | true |  | true | same-frame coframe/tau/MHref anti-circularity gate | false |
| SRC2596_07_2588_observed_stack | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2588-Y5-R2FR-observed-stack-q-eobs-tau-parent-owner-or-source-leak-fill.md | true |  | true | observed-stack q/e_obs/tau/MHref ownership gaps | false |
| SRC2596_08_1008_theta_qtau | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md | true |  | true | theta_MTS/Q_tau total extraction still missing | false |

## Lock Audit
| lock_id | lock_piece | required_identity | current_status | why_needed | residual_if_missing | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MHL2596_0_system_worldtube | system and source worldtube identity | system_id and source worldtube W_M are fixed before readout and shared by J_H, Q_M, S1/S2, A_ext and orbital readout | MISSING_SYSTEM_AND_WORLDTUBE_ID | anonymous denominator rows cannot prove a source-transfer theorem | system_id;worldtube_id;source_support_lock | false | false |
| MHL2596_1_observed_coframe | observed coframe/q/Obs_e | e_obs/coframe_id is parent-owned through q/Obs_e before matter, source, clock, boundary and orbit readout | MISSING_PARENT_Q_OBS_E_OWNER | M_H_ref must be in the same source frame as the equality/commutator rows | e_obs_coframe_lock;epsilon_q_owner;Delta_frame_source_over_MH | false | false |
| MHL2596_2_tau_identity | single tau identity | tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary=tau_obs[e_obs] | MISSING_TAU_FRAME_LOCK | different time generators can make the same charge look like different masses | tau_frame_lock;epsilon_tau_selector | false | false |
| MHL2596_3_theta_Qtau | theta_MTS and Q_tau^MTS | theta_MTS and Q_tau^MTS include EH, boundary, extra, projector and matter/source sectors | MISSING_THETA_QTAU_TOTAL | EH-only Hamiltonian charge is not the MTS parent source charge | theta_MTS_source;Q_tau_MTS_source | false | false |
| MHL2596_4_Htau_Href | H_tau-H_ref denominator | M_H_ref=H_tau[S_outer]-H_ref is positive, finite, integrable and fixed before source/readout fitting | MISSING_H_TAU_H_REF_MHREF | R_eq and I_commutator require a noncircular denominator | M_H_ref;H_tau;H_ref;delta_H_tau_curl | false | false |
| MHL2596_5_surfaces_annulus | linked surfaces and annulus | S1, S2, A_ext, r1, r2, homology class and source-free exterior are fixed before readout | MISSING_SURFACE_HOMOLOGY_LOCK | post-readout surfaces can make commutator/equality residuals disappear by mask choice | surface_homology_lock;annulus_metadata | false | false |
| MHL2596_6_units_positivity_acceptance | units, positivity and anti-circularity acceptance | all rows have units/source paths/no MISSING markers and reject orbital GM, EH-only charge, fitted counterterms and post-readout frames | CLAIM_BLOCKED | a denominator row is dangerous unless it is source-backed and noncircular | denominator_acceptance_gate | false | false |
| MHL2596_7_verdict | current verdict | MHL2596_0 through MHL2596_6 all pass in the same branch | MHREF_TAU_SURFACE_LOCK_NOT_DERIVED_CURRENT_CORPUS | the PiM equality/commutator runner cannot be scored yet | Delta_MHref_tau_surface_total | false | false |

## Denominator Rows
| row_id | symbol | definition | units | current_value | source_path | source_path_exists | observable_link | score_ready | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MHD2596_0_system | system_worldtube_lock | unique system_id, source worldtube W_M and source support fixed before readout | identifier_and_support_metadata | MISSING_SYSTEM_ID;MISSING_WORLDTUBE_ID;MISSING_SOURCE_SUPPORT_LOCK | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1519-Y5-parent-observed-coframe-tau-source-frame-lock-or-MHref-first-row.md | true | source_mass;GM_transfer | false | false | false |
| MHD2596_1_coframe | e_obs_coframe_lock | observed coframe fixed by q/Obs_e before matter/source/clock/orbit/boundary readout | certificate | MISSING_COFRAME_ID;MISSING_PARENT_Q_OBS_E_OWNER | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2588-Y5-R2FR-observed-stack-q-eobs-tau-parent-owner-or-source-leak-fill.md | true | same_frame;WEP;PPN;clock;orbital | false | false | false |
| MHD2596_2_tau | tau_frame_lock | same tau for source, charge, clocks, orbit, boundary and readout | certificate | MISSING_TAU_LOCK | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2390-Y5-R2FR-observed-coframe-pullback-same-frame-lock-or-frame-source-leak-values.md | true | clock;Hamiltonian_charge;source_mass;orbital | false | false | false |
| MHD2596_3_theta | theta_MTS_source | full parent symplectic potential including EH/boundary/extra/projector/matter-source sectors | equation_source | MISSING_THETA_MTS_SOURCE | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md | true | Hamiltonian_integrability;M_H_ref | false | false | false |
| MHD2596_4_Qtau | Q_tau_MTS_source | total parent Hamiltonian/Noether charge form for tau | charge_form_source | MISSING_Q_TAU_MTS_SOURCE | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md | true | Hamiltonian_charge;M_H_ref | false | false | false |
| MHD2596_5_MHref | M_H_ref | positive finite H_tau-H_ref in same e_obs/tau/source branch, not orbital GM | mass_or_energy_units | MISSING_M_H_REF | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_FRAME_1519_MHREF_FIRST_ROW_SCHEMA.csv | true | normalization;PiM_runner;GM_transfer | false | false | false |
| MHD2596_6_surfaces | surface_homology_lock | S1/S2/A_ext/r1/r2/homology/source-free exterior fixed before readout | surface_and_topology_metadata | MISSING_SURFACE_HOMOLOGY | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_PIM_1518_MHREF_SURFACE_LOCK.csv | true | I_commutator;R_eq_integral;radial_Meff | false | false | false |
| MHD2596_7_integrability | delta_H_tau_curl | field-space curl/integrability defect of H_tau with fixed reference | dimensionless_or_charge_curl_units | MISSING_INTEGRABILITY_CERTIFICATE | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_FRAME_1519_MHREF_FIRST_ROW_SCHEMA.csv | true | Hamiltonian_integrability;M_H_ref | false | false | false |
| MHD2596_TOTAL | Delta_MHref_tau_surface_total | absolute nonclaim envelope over system, coframe, tau, theta, Q_tau, M_H_ref, surfaces and integrability gaps | mixed_gate_not_score_ready | COMPONENTS_MISSING | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2596-Y5-R2FR-MHref-tau-source-frame-surface-lock-or-first-denominator-row.md | true | GM_transfer;PiM_runner;Newton;local_GR | false | false | false |

## Runner Refusal
| runner_id | target_id | symbol | verdict | failure_reasons | score_ready | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MHR2596_MHD2596_0_system | MHD2596_0_system | system_worldtube_lock | REFUSED_NONCLAIM_MHREF_DENOMINATOR_ROW | VALID_FOR_CLAIM_FALSE;MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE | false | false | false |
| MHR2596_MHD2596_1_coframe | MHD2596_1_coframe | e_obs_coframe_lock | REFUSED_NONCLAIM_MHREF_DENOMINATOR_ROW | VALID_FOR_CLAIM_FALSE;MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE | false | false | false |
| MHR2596_MHD2596_2_tau | MHD2596_2_tau | tau_frame_lock | REFUSED_NONCLAIM_MHREF_DENOMINATOR_ROW | VALID_FOR_CLAIM_FALSE;MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE;MULTI_TAU_SOURCE_CHARGE_CLOCK_ORBIT_RISK | false | false | false |
| MHR2596_MHD2596_3_theta | MHD2596_3_theta | theta_MTS_source | REFUSED_NONCLAIM_MHREF_DENOMINATOR_ROW | VALID_FOR_CLAIM_FALSE;MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE | false | false | false |
| MHR2596_MHD2596_4_Qtau | MHD2596_4_Qtau | Q_tau_MTS_source | REFUSED_NONCLAIM_MHREF_DENOMINATOR_ROW | VALID_FOR_CLAIM_FALSE;MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE | false | false | false |
| MHR2596_MHD2596_5_MHref | MHD2596_5_MHref | M_H_ref | REFUSED_NONCLAIM_MHREF_DENOMINATOR_ROW | VALID_FOR_CLAIM_FALSE;MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE;ORBITAL_GM_DENOMINATOR_REJECTED | false | false | false |
| MHR2596_MHD2596_6_surfaces | MHD2596_6_surfaces | surface_homology_lock | REFUSED_NONCLAIM_MHREF_DENOMINATOR_ROW | VALID_FOR_CLAIM_FALSE;MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE | false | false | false |
| MHR2596_MHD2596_7_integrability | MHD2596_7_integrability | delta_H_tau_curl | REFUSED_NONCLAIM_MHREF_DENOMINATOR_ROW | VALID_FOR_CLAIM_FALSE;MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE | false | false | false |
| MHR2596_MHD2596_TOTAL | MHD2596_TOTAL | Delta_MHref_tau_surface_total | REFUSED_NONCLAIM_MHREF_DENOMINATOR_ROW | VALID_FOR_CLAIM_FALSE;MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE;DENOMINATOR_COMPONENTS_NOT_SCORE_READY | false | false | false |

## Claim Gates
| gate_id | claim | gate_status | reason | gate_pass | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| CG2596_0_schema | M_H_ref/tau/surface first-row schema is explicit | PASS_NONCLAIM_STRUCTURE_ONLY | system, coframe, tau, theta, Q_tau, M_H_ref, surfaces and integrability rows are named | true | false | false |
| CG2596_1_EH_only | EH Hamiltonian charge alone supplies MTS M_H_ref | REJECTED_SHORTCUT | theta_MTS/Q_tau^MTS retained sectors are not extracted or zeroed | false | false | false |
| CG2596_2_orbital_GM | observed orbital GM can be used as M_H_ref | REJECTED_SHORTCUT | orbital GM is the transfer target, not a denominator proof input | false | false | false |
| CG2596_3_post_readout_surfaces | surfaces/support can be chosen after seeing residuals | REJECTED_SHORTCUT | post-readout masks can erase equality/commutator residuals | false | false | false |
| CG2596_4_denominator_score_ready | R_eq/I_commutator denominator rows are score-ready | BLOCKED_NONCLAIM | M_H_ref, tau, coframe, surfaces, theta/Qtau and integrability are missing | false | false | false |
| CG2596_5_Newton_local_GR | source-normalized Newton/local GR is derived | BLOCKED_NONCLAIM | denominator/source-frame lock is upstream and unclosed | false | false | false |

## Decision Ledger
| decision_id | decision | reason | effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2596_0_schema_retained | MHREF_FIRST_ROW_SCHEMA_RETAINED | the PiM runner cannot be scored without a positive same-frame noncircular denominator | M_H_ref/tau/surface rows are promoted to the current bottleneck | false |
| DEC2596_1_no_denominator_claim | MHREF_TAU_SURFACE_LOCK_NOT_DERIVED | system, q/Obs_e, tau, theta, Q_tau, H_tau/H_ref, surfaces and integrability are not source-backed | R_eq/I_commutator and source-normalized Newton stay blocked | false |
| DEC2596_2_next | TAU_IDENTITY_OR_MHREF_SOURCE_ACQUISITION_SELECTED_NEXT | same tau/source/charge/clock/orbit identity is the narrowest denominator lock and feeds every M_H_ref row | 2597 should attempt tau identity theorem or fill first source-backed M_H_ref/tau/surface acquisition rows | false |

## Next Target
| route_id | selection_status | target_file | target_script | task | success_condition | fallback_condition | guardrails | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT2596_0_selected | selected | 2597-Y5-R2FR-tau-identity-source-charge-clock-orbit-or-MHref-source-acquisition.md | scripts/Y5_R2FR_tau_identity_source_charge_clock_orbit_or_MHref_source_acquisition_2597.py | try to prove one parent tau generates source, Hamiltonian charge, clocks, orbit and boundary reference in the same q/e_obs branch; otherwise fill first source-backed M_H_ref/tau/surface acquisition rows | tau_frame_lock and M_H_ref denominator rows become source-backed enough to start scoring R_eq/I_commutator | nonclaim rows for tau_source/tau_charge/tau_clock/tau_orbit/tau_boundary, H_tau, H_ref, S1/S2/A_ext, units and source paths | no orbital GM denominator; no EH-only tau charge; no post-readout frame/surface; no Newton/local-GR claim; no GitHub; no formalization-workbench edits | false |

## Branch Copies
| copy_id | source_path | target_path | source_exists | target_exists | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| COPY2596_lock_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_MHREF_2596_LOCK_AUDIT.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2596_MHREF_TAU_SURFACE_LOCK_AUDIT_NONCLAIM.csv | true | true | false |
| COPY2596_denominator_rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_MHREF_2596_DENOMINATOR_ROWS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\MHref_tau_surface_denominator_rows_2596_NONCLAIM.csv | true | true | false |
| COPY2596_next_target | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_MHREF_2596_NEXT_TARGET.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2596_TAU_IDENTITY_OR_MHREF_SOURCE_ACQUISITION_NEXT.csv | true | true | false |

## Validation
| check_id | status | notes | detail | valid_for_claim |
| --- | --- | --- | --- | --- |
| VAL2596_00_sources_exist | PASS | all cited local source paths exist and needles are present |  | false |
| VAL2596_01_lock_audit_complete | PASS | M_H_ref/tau/surface lock audit covers all required clauses |  | false |
| VAL2596_02_denominator_rows_present | PASS | denominator rows cover system, frame, tau, charge, surfaces and total |  | false |
| VAL2596_03_denominator_sources_exist | PASS | denominator rows point to existing local sources |  | false |
| VAL2596_04_rows_nonclaim | PASS | denominator rows remain non-score-ready and nonclaim |  | false |
| VAL2596_05_runner_refuses | PASS | runner refuses all unfilled denominator rows |  | false |
| VAL2596_06_claim_gates_safe | PASS | EH-only/orbital-GM/post-readout shortcuts and local-GR claims remain blocked |  | false |
| VAL2596_07_no_claim_flags | PASS | no generated row sets valid_for_claim=true or claim_allowed=true |  | false |
| VAL2596_08_no_formalization_artifacts | PASS | no 2596 artifacts were written to formalization-workbench |  | false |
| VAL2596_09_next_selected | PASS | 2597 tau identity/source-acquisition target selected next |  | false |
| VAL2596_10_branch_copies | PASS | nonclaim branch copies exist |  | false |
| VAL2596_CSV_P8_Y5_MHREF_2596_SOURCE_REGISTER | PASS | CSV parses with 9 rows |  | false |
| VAL2596_CSV_P8_Y5_MHREF_2596_LOCK_AUDIT | PASS | CSV parses with 8 rows |  | false |
| VAL2596_CSV_P8_Y5_MHREF_2596_DENOMINATOR_ROWS | PASS | CSV parses with 9 rows |  | false |
| VAL2596_CSV_P8_Y5_MHREF_2596_RUNNER_REFUSAL | PASS | CSV parses with 9 rows |  | false |
| VAL2596_CSV_P8_Y5_MHREF_2596_CLAIM_GATES | PASS | CSV parses with 6 rows |  | false |
| VAL2596_CSV_P8_Y5_MHREF_2596_DECISION_LEDGER | PASS | CSV parses with 3 rows |  | false |
| VAL2596_CSV_P8_Y5_MHREF_2596_NEXT_TARGET | PASS | CSV parses with 1 rows |  | false |
| VAL2596_CSV_P8_Y5_MHREF_2596_BRANCH_COPIES | PASS | CSV parses with 3 rows |  | false |
| VAL2596_COPY_CSV_lock_audit | PASS | copy CSV parses with 8 rows |  | false |
| VAL2596_COPY_CSV_denominator_rows | PASS | copy CSV parses with 9 rows |  | false |
| VAL2596_COPY_CSV_next_target | PASS | copy CSV parses with 1 rows |  | false |
| VAL2596_OVERALL | PASS | 2596 refreshes the M_H_ref/tau/source-frame/surface first-row schema, rejects circular denominators and post-readout surfaces, keeps rows nonclaim, and selects tau identity/source acquisition next |  | false |

## Practical Status

This is a boring-looking but crucial lock. A beautiful charge identity is useless if the denominator is circular or from another frame. The next best move is the tau identity: one parent time generator for source, Hamiltonian charge, clocks, orbit and boundary reference, or the first honest source-acquisition rows.
