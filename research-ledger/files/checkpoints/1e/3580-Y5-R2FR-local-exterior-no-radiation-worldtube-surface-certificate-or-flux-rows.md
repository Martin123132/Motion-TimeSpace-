# 3580 - Local exterior no-radiation worldtube/surface certificate or flux rows

## Verdict
3580 proves the useful part and refuses the fake part.  In a stationary, source-free public EM collar the Poynting/Killing-energy flux is transported between linked surfaces: `Phi_out=Phi_in` up to explicit transport, crossing, gauge and corner defects.

That is not yet `Phi_EM_rad=0`.  No-radiation is reduced to a precise activation package: same stationary `tau`, actual `S_in/S_out` surface ownership, compact worldtube/no-crossing, corner-free fixed EM gauge surface, and one owned zero flux anchor.  If any clause fails, the fallback is the absolute nonclaim row `Phi_EM_public_abs`.

## Generated outputs
- `source_register`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3580_SOURCE_REGISTER.csv`
- `local_exterior_theorem`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3580_LOCAL_EXTERIOR_CERTIFICATE_THEOREM.csv`
- `transport_law`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3580_STATIONARY_COLLAR_TRANSPORT_LAW.csv`
- `clause_audit`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3580_CERTIFICATE_CLAUSE_AUDIT.csv`
- `flux_bound_rows`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3580_FLUX_BOUND_ROWS.csv`
- `htau_update`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3580_HTAU_UPDATE.csv`
- `activation_gates`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3580_ACTIVATION_GATES.csv`
- `decision_ledger`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3580_DECISION_LEDGER.csv`
- `status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3580_STATUS.csv`
- `next_target`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3580_NEXT_TARGET.csv`
- `canonical_status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_local_exterior_no_radiation_certificate_status.csv`
- `validation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3580_VALIDATION.csv`

## Local exterior theorem
- `LET3580_0_stationary_annulus`: A_tau(R_in,R_out)=Sigma_tau cap exterior(W_source) cap {R_in<=r<=R_out}; partial A=S_out union (-S_in) (CANDIDATE_OBJECT_DEFINED_NOT_PARENT_SIGNED)
- `LET3580_1_covariant_poynting_current`: j_EM^mu[tau]=-T_EM^{mu nu}tau_nu; div j_EM = -T_EM^{mu nu}nabla_(mu tau_nu)+tau_nu F^{nu lambda}J_lambda (EXACT_CONDITIONAL_IDENTITY)
- `LET3580_2_flux_transport`: Phi_out-Phi_in = int_A [partial_tau u_EM + J dot E + T_EM^{mu nu}nabla_(mu tau_nu)] dV + C_corner (TRANSPORT_THEOREM_DERIVED_CONDITIONAL)
- `LET3580_3_zero_anchor`: Phi_out=Phi_in and Phi_anchor=0 => Phi_EM_rad=0 on all linked surfaces (ZERO_REDUCED_TO_ANCHOR_PLUS_TRANSPORT)
- `LET3580_4_htau_component`: I_matter_EM_flux=0 if transport defect, anchor flux, crossing flux, and EM gauge/corner terms all vanish (HTAU_ACTIVATION_CONTRACT_WRITTEN)

## Transport rows
- `TRL3580_0_divergence_identity` `div j_EM[tau]`: -T_EM^{mu nu}nabla_(mu tau_nu)+tau_nu F^{nu lambda}J_lambda (EXACT_CONDITIONAL)
- `TRL3580_1_stationary_killing_zero` `T_EM symgrad(tau)`: T_EM^{mu nu}nabla_(mu tau_nu)=0 (ZERO_IF_STATIONARY_TAU_OWNER_SIGNED)
- `TRL3580_2_source_free_collar_zero` `tau.F.J collar work`: tau_nu F^{nu lambda}J_lambda=0 in A_tau (ZERO_IF_WORLDTUBE_SUPPORT_NO_CROSSING_SIGNED)
- `TRL3580_3_surface_transport` `Phi_out-Phi_in`: int_{S_out} S dot n dA - int_{S_in} S dot n dA = 0 (TRANSPORT_ZERO_IF_SURFACE_OWNER_SIGNED)
- `TRL3580_4_anchor_zero` `Phi_anchor`: Phi_anchor in {Phi_in, Phi_out, Phi_infty, prescribed no-incoming/no-outgoing boundary} (ANCHOR_REQUIRED_NOT_AUTOMATIC)

## Clause audit
- `LCA3580_0_same_hodge_current` `NFC3579_0;NFC3579_1`: PASS_CONDITIONAL_FROM_3463 (enough for public stress accounting but not full EM coupling ownership)
- `LCA3580_1_stationary_tau` `NFC3579_2`: NARROWED_TO_TAU_KILLING_OWNER (must prove tau_obs is parent-selected and Killing on the exterior collar, not fitted after readout)
- `LCA3580_2_no_radiation` `NFC3579_3`: NARROWED_TO_TRANSPORT_PLUS_ZERO_ANCHOR (source-free stationary collar gives Phi_out=Phi_in; zero additionally requires one owned zero anchor)
- `LCA3580_3_no_current_crossing` `NFC3579_4`: NARROWED_TO_WORLDTUBE_SUPPORT_NO_CROSSING (3560 gives a support-descent route, but compact support/no crossing remains unsigned unless parent-owned)
- `LCA3580_4_fixed_gauge_surface` `NFC3579_5`: NARROWED_TO_CONSTANT_GAUGE_PLUS_CORNER_FREE_SURFACE (gauge/corner contribution vanishes only if gauge parameter is constant on closed compatible surfaces or the corner term is exact/proper)
- `LCA3580_5_surface_owner` `implicit surface clause`: REQUIRED_NOT_PARENT_SIGNED (2065/2066 show the annulus is mathematically clean but not yet arena-certified as the actual parent surface)
- `LCA3580_6_verdict` `local exterior certificate`: CERTIFICATE_NARROWED_NOT_PROMOTED (do not claim I_matter_EM_flux=0 unless tau/surface/worldtube/anchor/gauge clauses all close)

## Flux bound rows
- `LFB3580_0_transport_defect` `Delta_Phi_transport`: abs(Phi_out-Phi_in) (ZERO_IF_STATIONARY_SOURCE_FREE_CORNER_FREE_ELSE_BOUND)
- `LFB3580_1_flux_anchor` `Phi_anchor`: min anchor among |Phi_in|, |Phi_out|, |Phi_infty|, or specified no-incoming/no-outgoing condition (ANCHOR_VALUE_OR_ZERO_REQUIRED)
- `LFB3580_2_current_crossing` `J_cross_EM`: int_boundary(A_tau) |J^mu n_mu| dSigma (WORLDTUBE_NO_CROSSING_OR_BOUND_REQUIRED)
- `LFB3580_3_surface_gauge_corner` `C_EM_surface_gauge`: absolute EM gauge/corner term in C_tau^EM on S_in union S_out (GAUGE_SURFACE_CERTIFICATE_OR_BOUND_REQUIRED)
- `LFB3580_4_regulator_corner` `B_corner_flux`: sum over active cutoff/excision/regulator/matched-patch seam fluxes (REGULATOR_LEDGER_OR_BOUND_REQUIRED)
- `LFB3580_5_total_public_EM_flux` `Phi_EM_public_abs`: Phi_anchor_abs + Delta_Phi_transport_abs + J_cross_work_abs + C_EM_surface_gauge_abs + B_corner_flux_abs (BOUND_FORMULA_READY_INPUT_VALUES_MISSING)
- `LFB3580_6_Htau_feed` `I_matter_EM_flux`: I_matter_EM_flux <= A_F sup_BF Phi_EM_public_abs (HTAU_FEED_READY_NONCLAIM)

## Htau update
- `HTU3580_0_3579_refinement` `PFB3579_1_Phi_EM_rad`: replace generic Phi_EM_rad with Phi_anchor + Delta_Phi_transport + crossing/gauge/corner rows -> public EM flux is now a transport/anchor problem, not a vague radiation placeholder
- `HTU3580_1_activation_rule` `I_matter_EM_flux`: I_matter_EM_flux=0 if LET3580 transport clauses plus zero anchor plus no-crossing plus gauge/surface clauses all close -> strict activation rule for 3579 public EM zero
- `HTU3580_2_nonclaim_bound` `Delta_H_curl_bound`: retain A_F sup_BF Phi_EM_public_abs if any clause is unsigned -> full H_tau curl remains nonclaim and no local-GR promotion follows

## Gates
- `GATE3580_0_sources`: PASS (all required 3580 source paths and anchors exist)
- `GATE3580_1_transport_law`: PASS_CONDITIONAL (Phi_out=Phi_in follows under Killing tau, source-free collar, and corner-free annulus)
- `GATE3580_2_no_radiation_zero`: FAIL_CURRENT_CLAIM (transport does not imply zero without a parent-owned zero anchor)
- `GATE3580_3_tau_surface_owner`: FAIL_CURRENT_CLAIM (2065/2066/2067 still mark parent tau/surface ownership unsigned)
- `GATE3580_4_worldtube_no_crossing`: FAIL_CURRENT_CLAIM (2388/3560 give a route, but compact support/no crossing is not parent-signed)
- `GATE3580_5_gauge_corner`: FAIL_CURRENT_CLAIM (constant gauge/exact corner route is conditional only)
- `GATE3580_6_htau_public_EM`: FAIL_CURRENT_CLAIM (zero allowed only after all above gates close; otherwise use LFB3580 rows)
- `GATE3580_7_local_GR`: FAIL_CURRENT_CLAIM (public EM branch narrowed, but other H_tau/local-GR residuals remain live)

## Decisions
- `DEC3580_0_transport_not_magic_zero`: accept the transport theorem and reject automatic no-radiation -> the zero proof now has a precise missing anchor instead of a vague radiation assumption
- `DEC3580_1_worldtube_surface_precision`: bind no-crossing and no-corner claims to actual parent surfaces -> prevents scoring a no-flux theorem on the wrong boundary
- `DEC3580_2_next_target`: attack stationary annulus same-tau/surface ownership plus flux anchor -> 3581 should try to parent-sign the common stationary annulus/tau/surface/anchor package or fill the first finite anchor/corner rows.

## Status
- `POYNTING_TRANSPORT_THEOREM_DERIVED_ZERO_REDUCED_TO_ANCHOR_AND_SURFACE_CERTIFICATE`: In a stationary source-free public EM collar, the Poynting/Killing-energy flux is transported between linked surfaces: Phi_out=Phi_in up to explicit transport, crossing, gauge and corner defects. Therefore no-radiation is reduced to one owned zero anchor plus the same tau/surface/worldtube/gauge certificate.

## Validation
- `VAL3580_0_sources_exist`: PASS (all required 3580 source paths exist)
- `VAL3580_1_required_needles_found`: PASS (all selected 3580 anchors found)
- `VAL3580_2_outputs_exist`: PASS (all pre-validation 3580 output files written)
- `VAL3580_3_csv_parse`: PASS (source_register:17; local_exterior_theorem:5; transport_law:5; clause_audit:7; flux_bound_rows:7; htau_update:3; activation_gates:8; decision_ledger:3; status:1; next_target:1; canonical_status:1)
- `VAL3580_4_transport_theorem_present`: PASS (flux transport theorem row present)
- `VAL3580_5_anchor_not_overclaimed`: PASS (zero anchor requirement retained)
- `VAL3580_6_transport_components_present`: PASS (stationary/source-free/anchor transport rows present)
- `VAL3580_7_clause_audit_present`: PASS (3579 clause audit narrowed)
- `VAL3580_8_bound_rows_present`: PASS (finite fallback rows present)
- `VAL3580_9_htau_update_present`: PASS (H_tau activation update present)
- `VAL3580_10_no_zero_claim`: PASS (no-radiation zero not overclaimed)
- `VAL3580_11_next_target_selected`: PASS (3581 target selected)
- `VAL3580_12_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3580_13_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3580_14_formalization_workbench_untouched`: PASS (no 3580 checkpoint output appears in formalization-workbench)

## Next target
- `3581-Y5-R2FR-stationary-annulus-same-tau-surface-owner-or-flux-anchor-row.md`
- Objective: parent-sign the common stationary annulus/tau/surface/zero-anchor package used by the 3580 Poynting transport theorem, or emit the first finite Phi_anchor, tau-surface, and EM gauge/corner rows with units
