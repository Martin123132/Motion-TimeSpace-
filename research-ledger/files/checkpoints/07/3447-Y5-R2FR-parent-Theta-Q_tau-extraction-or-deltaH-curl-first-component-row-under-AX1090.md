# 3447 - Parent Theta/Qtau Extraction or DeltaH Curl First Component Row

## Summary
- This checkpoint extracts the public control current chain for the adopted `Pi_M^H` branch.
- The public sector is `L_pub=L_EH+L_matter+L_EM`, with `Theta_pub=Theta_EH+Theta_matter+Theta_EM` and `J_tau^pub=Theta_pub(L_tau Phi)-i_tau L_pub`.
- This is not the total MTS charge: extra, boundary/reference, tau/surface and source-glue pieces remain live.
- The first `Delta_H_curl` component row is now split out as `DHC3447_0_public_sector_curl`, separating standard public-sector flux from genuinely MTS-specific extra curl.
- `Pi_M^H` stays clean: no independent projector `Theta/Q_tau` component is introduced in the preferred identity branch.

## Source Register
| source_id | path | exists | role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| doc_3446 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3446-Y5-R2FR-Htau-exact-one-form-reference-lock-or-MHref-denominator-bound-under-AX1090.md | True | immediate Theta/Qtau extraction handoff | False | False |
| next_3446 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3446_NEXT_TARGET.csv | True | machine-readable 3447 target | False | False |
| denominator_rows_3446 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3446_MHREF_DENOMINATOR_BOUND_ROWS.csv | True | Delta_H_curl target rows | False | False |
| one_form_3446 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3446_HTAU_EXACT_ONE_FORM_THEOREM.csv | True | Htau one-form theorem and bound route | False | False |
| pimh_3446 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3446_PIMH_CARRYFORWARD.csv | True | PiMH carryforward | False | False |
| doc_3445 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3445-Y5-R2FR-Hilbert-identity-PiM-parent-adoption-or-Htau-source-current-lock-under-AX1090.md | True | PiMH adoption checkpoint | False | False |
| pimh_contract_3445 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3445_HILBERT_IDENTITY_PIM_PARENT_ADOPTION_CONTRACT.csv | True | Hilbert identity branch contract | False | False |
| doc_3424 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3424-Y5-R2FR-minimal-parent-source-coupling-action-or-PC3400-adoption-gate-under-AX1090.md | True | minimal parent action branch | False | False |
| parent_density_3424 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3424_PARENT_ACTION_DENSITY.csv | True | public EH/matter/EM parent density | False | False |
| parent_hilbert_clause_3340 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3340_PARENT_HILBERT_SOURCE_CLAUSE.csv | True | public Hilbert source clause | False | False |
| hilbert_theorem_3340 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3340_HILBERT_SOURCE_THEOREM_OR_FAIL.csv | True | conditional Hilbert source theorem | False | False |
| jh_derivation_3408 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3408_JH_HILBERT_SOURCE_DERIVATION.csv | True | Hilbert stress derivation | False | False |
| variation_667 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_667_VARIATION_LEDGER.csv | True | covariant phase-space variation ledger | False | False |
| qtau_decomp_993 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv | True | Q_tau sector decomposition | False | False |
| charge_spine_2340 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2340_PARENT_CHARGE_EXTRACTION_SPINE.csv | True | parent charge extraction spine | False | False |
| theta_qtau_rows_1733 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1733_THETA_QTAU_COMPONENT_ROWS.csv | True | Theta/Qtau component rows | False | False |
| qtau_status_1646 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1646_QTAU_DECOMPOSITION_STATUS.csv | True | Q_tau decomposition status | False | False |
| sector_ledger_2939 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2939_THETA_QTAU_SECTOR_CERTIFICATE_LEDGER.csv | True | sector certificate ledger | False | False |
| certificate_2947 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2947_THETA_QTAU_CERTIFICATE_ATTEMPT.csv | True | Theta/Qtau certificate attempt | False | False |
| feed_rows_3007 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3007_THETA_QTAU_FEED_ROWS.csv | True | Theta/Qtau feed rows | False | False |
| theta_qtau_owner_1646 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1646_THETA_QTAU_CURRENT_OWNER_AUDIT.csv | True | parent current owner audit | False | False |

## Public Current Chain Extraction
| chain_id | piece | formula | extraction | status | remaining_gap | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PCE3447_0_public_L | public local action | L_pub=L_EH[g_obs;G_ref]+L_matter[e_obs,psi]+L_EM[g_obs,A;lambda_0] | delta L_pub=E_pub delta Phi_pub + d(Theta_EH+Theta_matter+Theta_EM) | PUBLIC_CONTROL_CHAIN_EXTRACTED_CONDITIONALLY | not the total MTS parent current; extra, boundary/reference, tau/surface and source-glue sectors remain | False | False |
| PCE3447_1_public_Noether | public observed-time current | J_tau^pub=Theta_pub(Phi,L_tau Phi)-i_tau L_pub | on public equations, J_tau^pub=dQ_tau^EH+C_tau^matter+C_tau^EM, with public matter/EM stress in the Hilbert source and any gauge/radiative boundary flux retained | FORMAL_PUBLIC_CURRENT_CHAIN_AVAILABLE | stationary/no-flux public boundary conditions are required before curl zero; matter/EM source support and radiation crossing must be handled | False | False |
| PCE3447_2_EM_Poynting | public EM/Poynting stress | S_EM=-(lambda_0/4) int sqrt(-g_obs) F^2; T_EM from Hilbert variation | Poynting flux is an observer split of T_EM/symplectic flux, not a separate gravitational source owner | PUBLIC_HILBERT_SOURCE_IF_LAMBDA0_AND_GOBS_SIGNED | public Maxwell/Hodge normalization and radiative boundary flux still need branch conditions or bounds | False | False |
| PCE3447_3_PiMH | Hilbert identity mass map | Pi_M^H=id/inclusion on C_H^M | no independent Theta_projector or Q_tau_projector is needed for the preferred identity branch | CARRIED_FORWARD_FROM_3445 | non-Hilbert J_extra and old non-identity projectors remain outside this result | False | False |
| PCE3447_4_total_verdict | Theta_MTS and Q_tau^MTS total | Theta_MTS=Theta_pub+Theta_extra+Theta_boundary+Theta_ref+Theta_glue; Q_tau^MTS=Q_tau^pub+Q_tau^extra+Q_tau^boundary+Q_tau^glue | public chain is extracted as a control sector, but total MTS charge is not promoted | PARTIAL_EXTRACTION_TOTAL_NOT_CLAIM_READY | extra-sector action/current, boundary/reference charge and tau/surface/source-glue rows are the live blockers | False | False |

## Theta/Qtau Component Status
| component_id | component | status_after_3447 | zero_or_bound_route | blocks_total_claim | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| TQS3447_0_public_EH | Theta_EH;Q_tau^EH | CONDITIONAL_PUBLIC_CONTROL_ANCHOR | EH exterior plus fixed tau/surface/reference and no non-EH flux | False | False | False |
| TQS3447_1_public_matter_EM | Theta_matter;Theta_EM;C_tau^matter;C_tau^EM | HILBERT_SOURCE_CONTROL_SECTOR_RETAIN_PUBLIC_FLUX | source-free/stationary exterior or explicit public matter/EM/radiation flux bound | True | False | False |
| TQS3447_2_PiMH | Theta_projector^H;Q_tau_projector^H | NO_INDEPENDENT_COMPONENT_IN_IDENTITY_BRANCH | reactivates only for non-identity PiM | False | False | False |
| TQS3447_3_extra_MTS | Theta_extra;Q_tau^extra;C_tau^extra | MISSING_L_EXTRA_THETA_QTAU | derive residual-sector L_X/Theta_X/Q_tau^X or source-bound its curl contribution | True | False | False |
| TQS3447_4_boundary_reference | Theta_boundary;Q_tau^boundary;delta B_ref | MISSING_BOUNDARY_REFERENCE_OWNER | fixed reference/no-retune boundary class or Delta_ref/symplectic flux bound | True | False | False |
| TQS3447_5_tau_surface_glue | tau/surface/worldtube source glue | MISSING_TAU_SURFACE_SOURCE_GLUE | same tau/frame/surface certificate and worldtube Hilbert source equality | True | False | False |
| TQS3447_6_total | Theta_MTS;Q_tau^MTS | TOTAL_NOT_PROMOTED_PUBLIC_CONTROL_PLUS_RETAINED_MTS_COMPONENTS | all components above must be theorem-zero, public-control, or source-bounded | True | False | False |

## DeltaH Curl First Component Rows
| row_id | quantity | definition | formula | current_status | required_columns | numeric_or_theorem_value | source_path | score_ready | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DHC3447_0_public_sector_curl | Delta_H_curl_public | public EH+ordinary matter+EM contribution to int_BF/d_F alpha_tau/ | int_BF / -int_S i_tau omega_pub + C_tau^matter + C_tau^EM / | THEOREM_ZERO_IF_STATIONARY_PUBLIC_NO_FLUX_BOUNDARY_ELSE_BOUND_REQUIRED | system_id;tau_id;surface_pair;variation_pair;public_boundary_condition;EM_radiation_flux;matter_support;curl_public_bound;units;source_path | CONDITIONAL_ZERO_OR_MISSING_PUBLIC_FLUX_BOUND | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3447_PUBLIC_CURRENT_CHAIN_EXTRACTION.csv | False | False | False |
| DHC3447_1_extra_sector_curl | Delta_H_curl_extra | MTS extra/domain/memory/range/source-exchange contribution to H_tau curl | int_BF / -int_S i_tau omega_extra + C_tau^extra / | MISSING_EXTRA_SECTOR_LAGRANGIAN_CURRENT | system_id;sector;L_X;Theta_X;Q_tau_X;C_tau_X;surface_pair;variation_pair;curl_extra_bound;units;source_path | MISSING_EXTRA_CURL_COMPONENT | MISSING_SOURCE_PATH | False | False | False |
| DHC3447_2_boundary_reference_curl | Delta_H_curl_boundary_ref | boundary, corner and reference contribution to H_tau curl | int_BF /C_S+C_ref+delta B_ref curl/ | MISSING_BOUNDARY_REFERENCE_LOCK_OR_BOUND | system_id;reference_selector;surface_pair;corner_rule;Delta_ref_curl;boundary_flux_bound;units;source_path | MISSING_BOUNDARY_REFERENCE_CURL | MISSING_SOURCE_PATH | False | False | False |
| DHC3447_TOTAL | Delta_H_curl_bound | absolute no-cancellation H_tau curl bound after first public component extraction | abs(Delta_H_curl_public)+abs(Delta_H_curl_extra)+abs(Delta_H_curl_boundary_ref)+abs(tau_surface_frame_curl) | TOTAL_NONCLAIM_COMPONENT_VALUES_MISSING | all component rows plus M_H_ref_lower and no_cancellation_flag | MISSING_COMPONENT_VALUES | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3447_DELTAH_CURL_FIRST_COMPONENT_ROWS.csv | False | False | False |

## Denominator Row Update
| update_id | prior_row | before | after | effect | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| DU3447_0_DBR3446_1 | DBR3446_1_delta_H_curl | MISSING_CURL_COMPONENT_BOUNDS | first component split written: public sector conditional zero/bound row plus extra and boundary/reference residual rows | Delta_H_curl is no longer one blob; public GR-control and MTS-specific curl components are separated | False | False |
| DU3447_1_DBR3446_5 | DBR3446_5_epsilon_den_total | MISSING_COMPONENT_VALUES | epsilon_den_total must include DHC3447_TOTAL plus Delta_ref, tau/surface/frame and M_H_ref_lower | source denominator runner can later compare public-control zero branch against MTS extra-sector bound branch | False | False |

## PiMH Carryforward
| carry_id | result | guard | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- |
| PIMH3447_0 | Pi_M^H remains identity/inclusion and adds no independent Theta_projector/Q_tau_projector component | if non-identity PiM returns, TQS3447_2 is invalid and I_commutator/projector-stress rows reactivate | False | False |

## Promotion Gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PG3447_0_sources | all 3447 cited source paths exist | True | source register path check | False | False |
| PG3447_1_public_chain | public EH+matter+EM current chain is extracted as a control sector | True | PCE3447 rows give L_pub, Theta_pub and J_tau^pub chain | False | False |
| PG3447_2_first_curl_row | first Delta_H_curl component row is written | True | DHC3447_0_public_sector_curl splits public control curl from MTS extra curl | False | False |
| PG3447_3_total_Qtau | Theta_MTS and Q_tau^MTS total are promoted | False | extra, boundary/reference and tau/surface/source-glue components remain missing | False | False |
| PG3447_4_local_GR_Newton | local GR/Newton denominator is promoted | False | M_H_ref_lower and total curl/reference/frame components are still nonclaim | False | False |

## Decision Ledger
| decision_id | decision | because | next_action | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3447_0_public_control | Use public EH+matter+EM current chain as the control branch. | it separates standard-GR current bookkeeping from genuinely MTS-specific extra/boundary/source-glue sectors | do not blame MTS-specific failures on the public control chain unless the public boundary/radiation flux also fails | False | False |
| DEC3447_1_extra_next | Attack the MTS extra-sector L_X/Theta_X/Q_tau_X next. | after Pi_M^H and public control extraction, the first real MTS denominator blocker is the extra-sector curl piece | derive extra-sector current owner or fill DHC3447_1 | False | False |

## Next Target
| target_doc | target_script | objective | success_condition | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| 3448-Y5-R2FR-extra-sector-LX-ThetaX-QtauX-owner-or-deltaHcurl-extra-row-under-AX1090.md | scripts/Y5_R2FR_3448_extra_sector_LX_ThetaX_QtauX_owner_or_deltaHcurl_extra_row.py | derive the MTS extra-sector L_X, Theta_X, Q_tau^X and C_tau^X contribution to the H_tau curl for the adopted Pi_M^H branch, or fill DHC3447_1 as a nonclaim source-bound component with units, surface pair, variation pair and source path | extra-sector curl is theorem-zero, public-bound style, or represented by a schema-valid nonclaim bound row; no local-GR/Newton claim until denominator total is closed | False | False |

## Runner Nonclaim
| runner_id | public_chain_extracted | first_curl_component_written | total_Qtau_promoted | score_ready | result | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RUN3447_0_public_control | True | True | False | False | PUBLIC_CONTROL_READY_TOTAL_MTS_CHARGE_BLOCKED | False | False |

## Validation
| check_id | condition | passed | detail |
| --- | --- | --- | --- |
| VAL3447_0_sources_exist | all cited 3447 source paths exist | True | 21/21 source paths exist |
| VAL3447_1_public_chain | public current chain extraction is present | True | L_pub and J_tau^pub rows written |
| VAL3447_2_first_curl_row | first Delta_H_curl component row is present | True | public-sector curl component split |
| VAL3447_3_total_not_promoted | total Theta_MTS/Q_tau^MTS remains nonclaim | True | total current chain still blocked |
| VAL3447_4_PiMH_no_reopen | Pi_M^H does not reintroduce projector charge | True | PiMH carryforward row present |
| VAL3447_5_next_extra | next target attacks extra-sector curl owner | True | 3448-Y5-R2FR-extra-sector-LX-ThetaX-QtauX-owner-or-deltaHcurl-extra-row-under-AX1090.md |
| VAL3447_6_generated_csv_parse | generated CSV rows parse cleanly | True | CSV reader pass for generated outputs present before validation write |
| VAL3447_7_nonclaim | all generated rows remain nonclaim | True | valid_for_claim=false and claim_allowed=false wherever present |
| VAL3447_8_formalization_untouched | formalization-workbench modified-file count remains 0 during this run | True | modified_count_since_start=0 |
| VAL3447_9_overall | 3447 Theta/Qtau checkpoint is internally valid | True | PASS |

## Bottom Line
We now have a control chain: public EH plus ordinary matter and public EM can be handled as the reference current sector, including Poynting as Hilbert/symplectic flux rather than a mystery source. The next hard part is genuinely MTS: `L_X`, `Theta_X`, `Q_tau^X`, and `C_tau^X` for the extra sector.
