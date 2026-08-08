# 3578 - Htau curl component zero or first bound vector

## Verdict
3578 turns the `H_tau` integrability problem into a live component vector.  The candidate branch earns two zeroes: `C_ref=0` from fixed `H_ref`, and `I_projector_PiMH=0` from the Hilbert-identity `Pi_M^H` branch.

The total curl is not zero.  The live vector is `I_matter_EM_flux`, `I_extra`, `I_boundary_corner`, `I_tau_surface`, and `I_qdescent_current`, with no cancellation credit.  The denominator feed is `Delta_H_curl_bound <= A_F sup_BF sum_live |I_i|`.

Best next target is public EM/Poynting flux because it is a concrete physical channel and less speculative than hidden extra-sector action reconstruction.

## Generated outputs
- `source_register`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3578_SOURCE_REGISTER.csv`
- `curl_identities`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3578_HTAU_CURL_IDENTITIES.csv`
- `curl_components`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3578_HTAU_CURL_COMPONENT_VECTOR.csv`
- `zero_audit`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3578_CURL_ZERO_AUDIT.csv`
- `theta_qtau_update`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3578_THETA_QTAU_COMPONENT_UPDATE.csv`
- `activation_gates`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3578_ACTIVATION_GATES.csv`
- `decision_ledger`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3578_DECISION_LEDGER.csv`
- `status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3578_STATUS.csv`
- `next_target`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3578_NEXT_TARGET.csv`
- `canonical_status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_Htau_curl_component_vector_status.csv`
- `validation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3578_VALIDATION.csv`

## Curl identities
- `CID3578_0_alpha`: alpha_tau(delta Phi)=int_S(delta Q_tau^MTS-i_tau Theta_MTS(delta Phi))-delta H_ref (EXACT_INPUT_FROM_3577)
- `CID3578_1_curl`: d_F alpha_tau=-int_S i_tau omega_MTS + C_tau + C_S + C_ref (DERIVED_IDENTITY_REFERENCE_TERM_ZEROED_INTERNAL)
- `CID3578_2_sector_split`: omega_MTS=omega_pub+omega_EM+omega_extra+omega_boundary+omega_projector+omega_selector+omega_memory (COMPONENT_SPLIT_DEFINED)
- `CID3578_3_branch_zeroes`: C_ref=0 and omega_projector^PiMH=0 in the Hilbert-identity single-charge branch (INTERNAL_ZEROES_ADOPTED_NONCLAIM)
- `CID3578_4_bound_route`: Delta_H_curl_bound <= A_F sup_BF (I_pub+I_EM+I_extra+I_boundary+I_tau_surface+I_qdescent) (BOUND_VECTOR_ROUTE)

## Component vector
- `HCURL3578_0_reference` `I_ref`: 0 in fixed-reference branch (SIGNED_INTERNAL_ZERO_FROM_3577)
- `HCURL3578_1_PiM_projector` `I_projector_PiMH`: 0 in Hilbert-identity Pi_M^H branch (SIGNED_INTERNAL_ZERO_FROM_3576)
- `HCURL3578_2_public_EH` `I_EH_stationary_boundary`: abs(int_S i_tau omega_EH) plus EH boundary flux (CONDITIONAL_ZERO_IF_STATIONARY_EH_BOUNDARY_ELSE_BOUND_REQUIRED)
- `HCURL3578_3_public_matter_EM` `I_matter_EM_flux`: int_BF | -int_S i_tau(omega_matter+omega_EM) + C_tau^matter + C_tau^EM | (PUBLIC_FLUX_BOUND_REQUIRED)
- `HCURL3578_4_extra_sector` `I_extra`: abs(int_BF[-int_S i_tau omega_X + C_tau^X + B_X]) (ZERO_IF_ABSENT_QUOTIENT_OR_VERTICAL_CONSTRAINT_SIGNED_ELSE_BOUND)
- `HCURL3578_5_boundary_corner` `I_boundary_corner`: abs(boundary/corner/edge contribution to d_F alpha_tau) excluding fixed H_ref derivative (BOUNDARY_EXACTNESS_OR_BOUND_REQUIRED)
- `HCURL3578_6_tau_surface` `I_tau_surface`: abs(C_tau+C_S) from tau generator or linking surface variation (TAU_SURFACE_LOCK_OR_BOUND_REQUIRED)
- `HCURL3578_7_qdescent_current` `I_qdescent_current`: epsilon_theta_Qtau_projectability_abs contribution from Dq/tau/current descent failure (Q_MAP_VERTICAL_BASIS_OR_BOUND_REQUIRED)
- `HCURL3578_8_total` `Delta_H_curl_bound`: A_F sup_BF sum_live |I_i| with no cancellation; signed-zero rows omitted from the live sum (FORMULA_READY_COMPONENT_VALUES_MISSING)

## Zero audit
- `ZERO3578_0_reference` `reference curl`: PASS_INTERNAL (fixed H_ref selected before source/readout in 3577)
- `ZERO3578_1_PiM` `Pi_M projector curl`: PASS_INTERNAL (Hilbert identity/inclusion branch from 3576)
- `ZERO3578_2_EH` `EH public curl`: CONDITIONAL_ONLY (requires stationary EH exterior and boundary conditions; not full MTS proof)
- `ZERO3578_3_public_EM` `public matter/EM curl`: NOT_SIGNED (radiation/Poynting/public flux needs no-flux theorem or data)
- `ZERO3578_4_extra` `extra-sector curl`: CONDITIONAL_ZERO_ROUTE_NOT_SIGNED (absent-quotient or vertical-constraint theorem exists as route, but not parent activated for every retained sector)
- `ZERO3578_5_boundary_tau_surface` `boundary/tau/surface curl`: NOT_SIGNED (requires boundary exactness, same tau, and fixed homology/surface branch)

## Theta/Qtau update
- `TQU3578_0_EH` `Theta_EH;Q_tau^EH`: CONDITIONAL_PUBLIC_CONTROL_ANCHOR -> kept as public baseline, not total MTS charge
- `TQU3578_1_matter_EM` `Theta_matter;Theta_EM;C_tau^matter;C_tau^EM`: RETAIN_PUBLIC_FLUX_BOUND -> feeds I_matter_EM_flux
- `TQU3578_2_PiMH` `Theta_projector^H;Q_tau_projector^H`: ZERO_IN_IDENTITY_BRANCH -> do not retain old projector curl in the single-charge branch
- `TQU3578_3_extra` `Theta_extra;Q_tau^extra;C_tau^extra`: RETAIN_COMPONENT_VECTOR -> feeds I_extra until absent-quotient/vertical-constraint route is signed or bounded
- `TQU3578_4_boundary` `Theta_boundary;Q_tau^boundary;corner/exact improvements`: RETAIN_BOUNDARY_COMPONENT_EXCEPT_FIXED_HREF -> fixed reference derivative is zero, but boundary/corner symplectic flux still needs proof or bound
- `TQU3578_5_total` `Theta_MTS;Q_tau^MTS`: TOTAL_NOT_PROMOTED_COMPONENT_VECTOR_READY -> H_tau exactness remains a bounded component problem

## Gates
- `GATE3578_0_sources`: PASS (all required 3578 source paths exist)
- `GATE3578_1_reference_projector_zero`: PASS_INTERNAL_CANDIDATE (C_ref and Pi_M^H projector curl are zero in the candidate branch)
- `GATE3578_2_component_vector`: PASS_NONCLAIM (Delta_H_curl_bound now has live component rows and no-cancellation formula)
- `GATE3578_3_total_curl_zero`: FAIL_CURRENT_CLAIM (public EM, extra, boundary, tau/surface and qdescent components are not all zero-derived)
- `GATE3578_4_units_values`: FAIL_CURRENT_CLAIM (common units and numeric/theorem component values are missing)
- `GATE3578_5_denominator`: FAIL_CURRENT_CLAIM (curl bound feeds denominator lower-bound route but does not close it)
- `GATE3578_6_local_GR`: FAIL_CURRENT_CLAIM (downstream PPN/R10/clock/orbital vector remains open)

## Decisions
- `DEC3578_0_zeroes_kept`: keep only earned curl zeroes -> prevents a fake H_tau integrability promotion
- `DEC3578_1_component_vector`: replace generic curl blocker with component vector -> next work can attack the largest-looking component instead of repeating 'H_tau curl missing'
- `DEC3578_2_next_target`: attack public EM/Poynting flux first -> 3579 should derive public matter/EM no-flux or fill the Poynting/radiation flux bound row.

## Status
- `HTAU_CURL_COMPONENT_VECTOR_READY_REFERENCE_AND_PIM_ZEROES_SIGNED_INTERNAL`: The H_tau curl is no longer a generic blocker: C_ref and Pi_M^H projector curl are internally zero, and the live no-cancellation vector is public EM/matter flux, extra-sector curl, boundary/corner flux, tau/surface mismatch, and qdescent current leakage.

## Validation
- `VAL3578_0_sources_exist`: PASS (all required 3578 source paths exist)
- `VAL3578_1_required_needles_found`: PASS (all selected Htau curl component needles found)
- `VAL3578_2_outputs_exist`: PASS (all pre-validation 3578 output files written)
- `VAL3578_3_csv_parse`: PASS (source_register:23; curl_identities:5; curl_components:9; zero_audit:6; theta_qtau_update:6; activation_gates:7; decision_ledger:3; status:1; next_target:1; canonical_status:1)
- `VAL3578_4_reference_PiM_zeroes_present`: PASS (reference and PiM zero component rows present)
- `VAL3578_5_live_components_present`: PASS (live curl components present)
- `VAL3578_6_total_bound_formula_present`: PASS (total curl no-cancellation formula present)
- `VAL3578_7_zero_audit_present`: PASS (public EM zero not overclaimed)
- `VAL3578_8_theta_qtau_update_present`: PASS (theta/Qtau total not promoted)
- `VAL3578_9_total_curl_not_claimed`: PASS (total Htau curl remains unclaimed)
- `VAL3578_10_next_target_selected`: PASS (public EM/Poynting next target selected)
- `VAL3578_11_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3578_12_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3578_13_formalization_workbench_untouched`: PASS (no 3578 checkpoint output appears in formalization-workbench)

## Next target
- `3579-Y5-R2FR-public-EM-Poynting-Htau-curl-zero-or-flux-bound.md`
- Objective: derive public matter/EM no-flux contribution to the H_tau curl in the compact local exterior, or fill the first Poynting/radiation flux bound row with units and source paths
