# 3579 - Public EM/Poynting Htau curl zero or flux bound

## Verdict
3579 gives the public matter+EM `H_tau` curl component a real theorem branch: under a compact stationary local exterior with the same observed Hodge/coframe, the same matter/EM current owner, no net radiative Poynting flux, no charged current crossing the linking surface, and fixed EM gauge/surface data, `I_matter_EM_flux=0`.

This is useful but not a local-GR or Maxwell-owner victory.  It does **not** derive `alpha_EM`, unique `F^2`, `w_EM=0`, `C_XF2=0`, or the full `H_tau` curl.  If the strict exterior clauses are not parent-signed, the fallback is `Phi_EM_rad + W_public_exchange + C_EM_surface_gauge` as explicit flux/corner rows.

## Generated outputs
- `source_register`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3579_SOURCE_REGISTER.csv`
- `public_em_theorem`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3579_PUBLIC_EM_POYNTING_THEOREM.csv`
- `no_flux_conditions`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3579_NO_FLUX_CONDITIONS.csv`
- `flux_bound_rows`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3579_POYNTING_FLUX_BOUND_ROWS.csv`
- `htau_component_update`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3579_HTAU_COMPONENT_UPDATE.csv`
- `activation_gates`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3579_ACTIVATION_GATES.csv`
- `decision_ledger`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3579_DECISION_LEDGER.csv`
- `status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3579_STATUS.csv`
- `next_target`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3579_NEXT_TARGET.csv`
- `canonical_status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_I_matter_EM_flux_status.csv`
- `validation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3579_VALIDATION.csv`

## Public EM theorem branch
- `PEM3579_0_public_Maxwell_stress`: S_EM=-1/(4 mu0) int sqrt(-g_obs) F_{mn}F^{mn}+int A_mu J^mu (EXACT_CONDITIONAL_ON_OBSERVED_HODGE)
- `PEM3579_1_matter_EM_exchange`: nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda and nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda (EXACT_CONDITIONAL_TOTAL_STRESS_ZERO)
- `PEM3579_2_poynting_flux_identity`: d_t U_EM(V)+int_boundary(V) S_Poynting dot n dA=-int_V J dot E dV (DERIVED_CONDITIONAL_NO_FLUX_IDENTITY)
- `PEM3579_3_covariant_phase_space_zero`: I_matter_EM_flux=abs(int_BF[-int_S i_tau omega_{matter+EM}+C_tau^{matter+EM}]) (CONDITIONAL_THEOREM_ZERO_WRITTEN)
- `PEM3579_4_not_alpha_owner`: I_matter_EM_flux=0 does not imply Delta_Hodge_EM=0, w_EM=0, C_XF2=0, or b_alpha=0. (SCOPE_GUARD_EXPLICIT)

## No-flux conditions
- `NFC3579_0_same_observed_Hodge` `same observed coframe/Hodge defines Maxwell stress and local geometry`: PASS_CONDITIONAL_STANDARD_FORM (Needed so the Poynting vector is the energy-current of the same public geometry that H_tau sees.)
- `NFC3579_1_same_current_owner` `matter current and Maxwell current are varied from the same public action`: PASS_CONDITIONAL_NOT_PARENT_GLOBAL (Needed for Lorentz-force exchange to cancel in total matter+EM Hilbert stress.)
- `NFC3579_2_stationary_generator` `tau is the same observed stationary generator on the collar`: REQUIRED_NOT_PARENT_SIGNED (Needed for L_tau Phi=0 and omega(delta Phi,L_tau Phi)=0.)
- `NFC3579_3_no_radiative_boundary_flux` `no net Poynting/radiation/background leakage through the linking boundary`: REQUIRED_NOT_PARENT_SIGNED (Needed to set int_boundary S_Poynting dot n dA=0 rather than merely bound it.)
- `NFC3579_4_no_current_crossing_surface` `charged matter worldtube is inside the linking surface and no public current crosses the boundary`: REQUIRED_NOT_PARENT_SIGNED (Needed so public EM/matter exchange is internal to the source worldtube.)
- `NFC3579_5_fixed_EM_gauge_surface` `EM gauge representative is fixed on the linking surface or contributes only an exact charge improvement`: REQUIRED_NOT_PARENT_SIGNED (Needed to prevent a gauge/corner term from masquerading as Poynting flux.)
- `NFC3579_6_local_exterior_clause` `local exterior is compact, source-free, stationary, and public-sector only for this component`: CONDITIONAL_ZERO_IF_ALL_ABOVE (This clause zeros only I_matter_EM_flux, not the full H_tau curl vector.)

## Fallback bound rows
- `PFB3579_0_I_matter_EM_flux` `I_matter_EM_flux`: abs(int_BF[-int_S i_tau omega_{matter+EM}+C_tau^{matter+EM}]) (CONDITIONAL_ZERO_ELSE_BOUND_READY)
- `PFB3579_1_Phi_EM_rad` `Phi_EM_rad`: int_boundary S_Poynting dot n dA (BOUND_ROW_READY_VALUE_MISSING)
- `PFB3579_2_public_work_exchange` `W_public_exchange`: int_BF int_V J dot E dV dt (CONDITIONAL_ZERO_IN_TOTAL_STRESS_ELSE_BOUND)
- `PFB3579_3_surface_gauge_corner` `C_EM_surface_gauge`: surface EM gauge/corner contribution to C_tau^{EM} (SURFACE_GAUGE_CERTIFICATE_REQUIRED)
- `PFB3579_4_Hodge_flow_mismatch` `Delta_Hodge_EM`: *_EM-*_obs[e_obs(q)] or chi_EM-chi_obs (RETAINED_COUPLING_GATE)
- `PFB3579_5_EM_normalization_multiplier` `w_EM`: S_EM -> w_EM S_EM; T_EM -> w_EM T_EM (RETAINED_COUPLING_GATE)
- `PFB3579_6_hidden_F2_counterterm` `C_XF2`: Delta S ~ int sqrt(-g) f_X(Phi) F_{mn}F^{mn} (RETAINED_COUPLING_GATE)
- `PFB3579_7_readout_radiative_regeneration` `C_EM_readout`: S_eff/readout regenerates f_X F^2, alpha_X, or EM binding response (RETAINED_COUPLING_GATE)

## Htau component update
- `HCU3579_0_before` `I_matter_EM_flux`: 3578 status: PUBLIC_FLUX_BOUND_REQUIRED -> public EM/matter contribution was live and unsplit
- `HCU3579_1_after_conditional` `I_matter_EM_flux`: CONDITIONAL_ZERO_ON_STRICT_PUBLIC_LOCAL_EXTERIOR_ELSE_FLUX_BOUND_READY -> if same-Hodge, same-current, stationary, no-radiation, no-current-crossing, fixed-gauge-surface clauses are signed, this component is zero
- `HCU3579_2_after_fallback` `Delta_H_curl_bound`: replace live I_matter_EM_flux by Phi_EM_rad + W_public_exchange + C_EM_surface_gauge if clauses fail -> the total H_tau curl vector remains nonzero/not claimed because other components live
- `HCU3579_3_live_after_3579` `live_Htau_components`: I_extra;I_boundary_corner;I_tau_surface;I_qdescent_current;plus_public_EM_flux_if_no_flux_clause_unsigned -> 3579 narrows the public EM term but does not close the local GR branch

## Gates
- `GATE3579_0_sources`: PASS (all required source paths exist and anchors are present)
- `GATE3579_1_standard_public_EM`: PASS_CONDITIONAL (public EM stress, Poynting current, and matter-EM exchange identities are recorded)
- `GATE3579_2_no_flux_theorem`: PASS_CONDITIONAL_ONLY (zero theorem holds only under strict stationary/source-free/no-radiation/fixed-surface clauses)
- `GATE3579_3_parent_local_exterior`: FAIL_CURRENT_CLAIM (stationarity, no-radiation, current containment, and fixed gauge/surface are not parent-signed globally)
- `GATE3579_4_coupling_owner`: FAIL_CURRENT_CLAIM (Delta_Hodge_EM, w_EM, C_XF2, charge/current owner and readout/radiative closure remain separate gates)
- `GATE3579_5_total_Htau_curl`: FAIL_CURRENT_CLAIM (I_extra, I_boundary_corner, I_tau_surface, and I_qdescent_current remain live)
- `GATE3579_6_local_GR`: FAIL_CURRENT_CLAIM (public EM narrowing is useful but insufficient for local GR reduction)

## Decisions
- `DEC3579_0_public_EM_zero`: accept strict conditional no-flux theorem for public EM/matter component -> I_matter_EM_flux is no longer a shapeless missing term; it has a theorem-zero branch and a fallback flux-bound branch.
- `DEC3579_1_no_alpha_overreach`: separate Poynting no-flux from EM coupling ownership -> prevents a fake Maxwell/local-GR pass while preserving the useful public stress result
- `DEC3579_2_next_target`: attack the strict local exterior certificate next -> 3580 should prove the local exterior no-radiation/worldtube-surface certificate or emit concrete flux rows.

## Status
- `PUBLIC_EM_POYNTING_HTAU_COMPONENT_CONDITIONAL_ZERO_AND_BOUND_READY`: The public matter+EM H_tau curl component has a concrete conditional zero: in a compact stationary local exterior with same observed Hodge, same matter/EM current owner, no radiative Poynting flux, no current crossing the linking surface, and fixed EM gauge/surface data, I_matter_EM_flux=0.

## Validation
- `VAL3579_0_sources_exist`: PASS (all required 3579 source paths exist)
- `VAL3579_1_required_needles_found`: PASS (all selected EM/Poynting and H_tau anchors found)
- `VAL3579_2_outputs_exist`: PASS (all pre-validation 3579 output files written)
- `VAL3579_3_csv_parse`: PASS (source_register:17; public_em_theorem:5; no_flux_conditions:7; flux_bound_rows:8; htau_component_update:4; activation_gates:7; decision_ledger:3; status:1; next_target:1; canonical_status:1)
- `VAL3579_4_poynting_identity_present`: PASS (Poynting flux identity row present)
- `VAL3579_5_conditional_zero_present`: PASS (conditional covariant phase-space zero row present)
- `VAL3579_6_strict_conditions_retained`: PASS (strict local exterior conditions retained)
- `VAL3579_7_flux_bound_rows_present`: PASS (fallback flux/corner bound rows present)
- `VAL3579_8_no_alpha_overclaim`: PASS (scope guard prevents alpha/unique-F2 overclaim)
- `VAL3579_9_htau_update_present`: PASS (H_tau component update present)
- `VAL3579_10_total_curl_not_claimed`: PASS (full H_tau curl remains unclaimed)
- `VAL3579_11_next_target_selected`: PASS (local exterior certificate next target selected)
- `VAL3579_12_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3579_13_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3579_14_formalization_workbench_untouched`: PASS (no 3579 checkpoint output appears in formalization-workbench)

## Next target
- `3580-Y5-R2FR-local-exterior-no-radiation-worldtube-surface-certificate-or-flux-rows.md`
- Objective: derive the strict local exterior certificate needed by the 3579 public EM/Poynting no-flux theorem, or emit concrete nonclaim flux rows for radiation, current crossing, and EM surface gauge/corner leakage
