# 3614 - principal Hodge bound or Htau curl integrability

## Verdict
3614 advances the principal-Hodge branch.  `Delta_chi_principal` now has both a conditional theorem-zero route and a no-cancellation bound law.

`||Delta_chi_principal||_H <= B_Fresnel + C_g||[g_EM]-[g_obs]|| + B_closure + B_orient`

The theorem-zero route is clean but not a current claim: reciprocal principal chi, nonbirefringent Fresnel reconstruction, closure relation, same public conformal metric, fixed orientation, and no independent principal tensor must all be parent-signed.  Scalar/conformal scale is still carried in source/clock/normalization gates, not silently discarded.

## Principal Hodge Theorem
- `PHT3614_0_reciprocal_principal` / `principal constitutive action branch`: DERIVED_CONDITIONAL_INPUT - A local bilinear EM action contributes only the reciprocal/symmetric principal constitutive part; skewon is non-Lagrangian and already belongs to a separate residual.
- `PHT3614_1_fresnel_reconstruction` / `nonbirefringent Fresnel branch`: DERIVED_CONDITIONAL_INPUT - If the Fresnel quartic is a repeated quadratic, the principal reciprocal chi reconstructs a conformal EM metric class.
- `PHT3614_2_metric_hodge_shape` / `closure relation to Hodge shape`: DERIVED_CONDITIONAL_INPUT - After axion/skewon removal, kappa^2=-lambda^2 I makes kappa/lambda a Hodge complex structure.
- `PHT3614_3_same_metric_clause` / `same public metric obstruction`: PARENT_SIGNATURE_REQUIRED - The EM metric reconstructed from rays must be identified with the matter/clock/source metric up to the conformal scale already separated in 3613.
- `PHT3614_4_conditional_zero` / `Delta_chi_principal Hodge zero theorem`: EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED - Delta_chi_principal is zero for the Hodge/cone branch if reciprocal nonbirefringent closure reconstructs the same public conformal metric and no independent principal tensor is allowed.

## Principal Hodge Bound
- `PHB3614_0_target` / `Delta_chi_principal`: TARGET_IMPORTED - `Delta_chi_principal := chi_EM_principal - chi_principal(g_obs)`
- `PHB3614_1_bound_law` / `principal Hodge no-cancellation bound`: SOURCE_BOUND_FILLED_NONCLAIM - `||Delta_chi_principal||_H <= B_Fresnel + C_g||[g_EM]-[g_obs]|| + B_closure + B_orient`
- `PHB3614_2_B_Fresnel` / `B_Fresnel`: BOUND_COMPONENT_VALUES_MISSING - `B_Fresnel := ||G_chi(k)-rho(g_EM^{ab}k_a k_b)^2||_arena`
- `PHB3614_3_same_metric` / `same-metric mismatch`: BOUND_COMPONENT_VALUES_MISSING - `B_same_metric := C_g||[g_EM]-[g_obs]||`
- `PHB3614_4_closure_defect` / `closure-relation defect`: BOUND_COMPONENT_VALUES_MISSING - `B_closure := ||kappa^2+lambda^2 I||`
- `PHB3614_5_scale_guard` / `scalar impedance / conformal scale`: RECLASSIFIED_NOT_DROPPED - `B_scale not in ||Delta_chi_principal||_H; carry B_lambda/source_clock instead`

## Empirical Acquisition
- `PEA3614_0_existing_runner` / `Delta_chi_principal`: BLOCKED_INPUT_NOT_VALID_FOR_CLAIM - current local runner remains blocked because parent coefficient and observational bound rows are missing
- `PEA3614_1_bound_source_need` / `vacuum birefringence / light-cone bound`: ACQUISITION_REQUIRED_NO_NUMERIC_CLAIM - future numeric scoring needs a primary-source observational bound for B_Fresnel and a declared norm map
- `PEA3614_2_parent_coefficient_need` / `MTS predicted principal coefficient`: PARENT_INPUT_REQUIRED_NO_NUMERIC_CLAIM - future numeric scoring also needs a parent coefficient for B_Fresnel, same-metric mismatch or closure defect

## Htau Curl Fallback
- `HCF3614_0_identity` / `C_curl`: FALLBACK_TARGET_IMPORTED - `C_curl := Pi_M^H(curl(delta H_tau))/(Pi_M H_tau)`
- `HCF3614_1_curl_law` / `field-space curl identity`: EXACT_IDENTITY_IMPORTED - `d_F alpha_tau=-int_S i_tau omega_MTS + C_tau + C_S + C_ref; fixed-reference branch sets C_ref=0`
- `HCF3614_2_bound_vector` / `Delta_H_curl_bound`: BOUND_VECTOR_READY_VALUES_MISSING - `Delta_H_curl_bound <= A_F sup_BF (I_pub+I_EM+I_extra+I_boundary+I_tau_surface+I_qdescent)`
- `HCF3614_3_first_internal_zeroes` / `reference and PiM projector pieces`: SIGNED_INTERNAL_ZERO_NONCLAIM - `I_ref=0; I_projector_PiMH=0 in selected internal branch`
- `HCF3614_4_empirical_map` / `C_Htau observable map`: BOUND_ROUTE_IMPORTED - `C_Htau := norm(int_boundary i_tau omega_total)/norm(delta H_tau)`

## Decision Gates
- `DEC3614_0_principal_theorem` / `Delta_chi_principal theorem-zero route`: CONDITIONAL_THEOREM_WRITTEN - Principal Hodge mismatch vanishes if reciprocal nonbirefringent closure reconstructs the same public conformal metric and independent principal tensors are forbidden.
- `DEC3614_1_principal_bound` / `Delta_chi_principal source-bound route`: ADVANCED - A sourced no-cancellation bound now splits principal Hodge failure into Fresnel, same-metric, closure and orientation components.
- `DEC3614_2_empirical` / `observational/numeric claim`: BLOCKED - No numeric claim is allowed until primary observational bounds and parent coefficients replace MISSING rows.
- `DEC3614_3_htau` / `C_curl fallback`: READY - H_tau curl fallback is imported with internal zeroes for reference/projector and live public/EM/extra/boundary/tau/qdescent components.
- `DEC3614_4_claim_guard` / `local-GR/Newton/Maxwell claim`: BLOCKED_FOR_CLAIM_NOT_FOR_WORK - No local-GR/Newton/Maxwell pass follows because principal Hodge theorem is conditional and numeric bounds are not sourced.
- `DEC3614_5_next` / `next best attack`: SELECT_BFRESNEL_SOURCE_OR_HTAU_PUBLIC_FLUX - Either acquire a real primary-source B_Fresnel/light-cone bound, or attack I_public/I_matter_EM in C_curl as the next Hamiltonian integrability component.

## Status
- `PRINCIPAL_HODGE_BOUND_FILLED_CONDITIONAL_ZERO_ROUTE_WRITTEN_HTAU_CURL_READY`: 3614 writes the conditional principal-Hodge zero theorem and fills a source-backed no-cancellation bound for Delta_chi_principal: Fresnel/birefringent shape, same-metric mismatch, closure defect and orientation. Numeric scoring remains blocked by missing parent coefficients and primary observational bound rows. C_curl is carried as the Pi_M/H_tau Hamiltonian fallback with component envelope ready.

## Validation
- `VAL3614_0_sources_exist`: PASS (all required 3614 source paths exist)
- `VAL3614_1_needles_found`: PASS (all selected 3614 source anchors found)
- `VAL3614_2_outputs_exist`: PASS (all pre-validation 3614 csv outputs written)
- `VAL3614_3_csv_parse`: PASS (source_register:13; principal_hodge_theorem:5; principal_hodge_bound:6; empirical_bound_acquisition:3; htau_curl_fallback:5; decision_gates:6; status:1; next_target:1; canonical_status:1)
- `VAL3614_4_conditional_theorem_written`: PASS (principal-Hodge conditional zero theorem written)
- `VAL3614_5_principal_bound_filled`: PASS (Delta_chi_principal no-cancellation bound filled)
- `VAL3614_6_scale_not_dropped`: PASS (scalar/conformal scale reclassified, not discarded)
- `VAL3614_7_empirical_claim_blocked`: PASS (numeric empirical claim remains blocked without primary/source rows)
- `VAL3614_8_htau_curl_fallback_ready`: PASS (C_curl fallback bound vector imported)
- `VAL3614_9_no_claim_flags`: PASS (all generated rows remain nonclaim)
- `VAL3614_10_next_target_selected`: PASS (3615 target selected from concrete bound branches)
- `VAL3614_11_status_ok`: PASS (canonical status matches 3614 verdict)
- `VAL3614_12_formalization_workbench_untouched`: PASS (no 3614 checkpoint output appears in formalization-workbench outside package/venv noise)

## Next Target
- `NEXT3614_0` -> `3615-Y5-R2FR-BFresnel-primary-bound-or-Htau-public-flux.md`
- Objective: try to acquire/source a primary nonclaim observational bound row for B_Fresnel / Delta_chi_principal; if not, attack the public EH plus matter/EM flux components of H_tau curl
- Success gate: must produce either a primary-source empirical bound acquisition row for B_Fresnel with units/arena, or a theorem-zero/source-bound row for I_EH_stationary_boundary or I_matter_EM_flux
- Reason: 3614 split the principal-Hodge problem enough that the next useful move is either real bound data or Hamiltonian curl flux reduction.
