# 3585 — no homogeneous exterior mode or extra-hair epsilon row

## Verdict
3585 does not prove full no-hair, but it turns the dangerous `3584` homogeneous-mode blocker into a channel theorem.  Radiative EH modes are killed only by a zero-news/no-radiation boundary; massive/coercive extra modes are killed only by a positive self-adjoint energy identity with zero boundary flux and zero source charge.

Everything else stays honest as a residual: cross terms, topological/boundary hair, projector-hidden modes, and retained non-EH operators.  The updated stack is:

`epsilon_hom_mode = epsilon_news + epsilon_coercive_extra + epsilon_cross_hair + epsilon_top_boundary_hair + epsilon_projector_hair + epsilon_nonEH_hair`.

So this checkpoint is progress because it says exactly what kind of hair can be killed by theorem and what kind must be bounded.

## No-homogeneous-mode theorem rows
- `NHE3585_0_decomposition`: delta Phi_hom = h_TT^rad + X_coercive + X_massless/top + X_gauge/proj (DECOMPOSITION_WRITTEN)
- `NHE3585_1_EH_no_news`: Bondi/news or Killing-energy flux N_AB N^AB=0 plus stationary boundary data => h_TT^rad=0 in the local stationary branch (CONDITIONAL_ZERO_FOR_RADIATIVE_EH_MODES)
- `NHE3585_2_coercive_extra_zero`: L_X X=0, <X,L_X X> >= c_X||X||^2, zero boundary flux, zero source charge => X=0 (CONDITIONAL_ZERO_FOR_COERCIVE_EXTRA_MODES)
- `NHE3585_3_cross_term_bound`: |<X,CY>| <= eta E_X + eta' E_Y with eta+eta'<1 (BOUND_REQUIRED_FOR_COERCIVITY)
- `NHE3585_4_topological_boundary_escape`: harmonic/topological class or finite boundary charge survives unless relative class/reference fixes its flux (NOT_ZERO_BY_DEFAULT_BOUNDARY_EPSILON_REQUIRED)
- `NHE3585_5_projector_gauge_escape`: P_loc delta Phi=0 does not imply delta Phi=0 unless kernel/gauge/topology are audited (NOT_ZERO_BY_DEFAULT_PROJECTOR_EPSILON_REQUIRED)
- `NHE3585_6_Estat_update`: Z_no_hom_mode = Z_EH_no_news & Z_coercive_extra & Z_cross_bound & Z_top_boundary & Z_projector_kernel (NO_HOM_MODE_ROUTE_SHARPENED_NOT_CLAIMED)

## Channel audit
- `CHA3585_0_EH_TT` `EH_radiative_TT`: PASS_IF_ZERO_NEWS_OR_NO_RADIATION_BOUNDARY_SIGNED -> `epsilon_news`
- `CHA3585_1_GammaKhat_GK` `Gamma/Khat local response`: PASS_IF_POSITIVE_ENERGY_IDENTITY_AND_BOUNDARY_ZERO_SIGNED -> `epsilon_GK_hair`
- `CHA3585_2_bulk_memory_range` `bulk/memory/range extra modes`: PASS_IF_FIELD_SPECIFIC_OPERATOR_POSITIVE_AND_SOURCE_CHARGE_ZERO -> `epsilon_bulk_memory_range_hair`
- `CHA3585_3_domain_projector` `domain/projector selector`: UNSIGNED_PROJECTOR_KERNEL_AUDIT_REQUIRED -> `epsilon_projector_hair`
- `CHA3585_4_boundary_topology` `boundary/topological sector`: UNSIGNED_RELATIVE_COHOMOLOGY_OR_BOUNDARY_FLUX_REQUIRED -> `epsilon_top_boundary_hair`
- `CHA3585_5_metric_operator` `non-EH metric operator family`: UNSIGNED_EH_DOMINANCE_OR_NON_EH_VECTOR_REQUIRED -> `epsilon_nonEH_hair`
- `CHA3585_6_source_normalization` `source/coupling normalization`: STILL_SEPARATE_SOURCE_COUPLING_GATE -> `epsilon_source_coupling`

## Epsilon rows
- `EHB3585_0_epsilon_news` `epsilon_news`: integral_Iplus |N_AB|^2 duduOmega or local gravitational-wave energy flux through exterior boundary (MISSING_NUMERIC_OR_PARENT_ZERO)
- `EHB3585_1_epsilon_coercive_extra` `epsilon_coercive_extra`: sum_X max(0, boundary_flux_X + source_charge_X - c_X||X||^2 lower-bound certificate) (MISSING_FIELD_SPECIFIC_COERCIVITY_INPUTS)
- `EHB3585_2_epsilon_cross_hair` `epsilon_cross_hair`: uncancelled mixed A/Gamma/memory/operator cross-term bound (MISSING_CROSS_TERM_BOUND)
- `EHB3585_3_epsilon_top_boundary_hair` `epsilon_top_boundary_hair`: absolute boundary/topological flux or relative cohomology charge not fixed by reference class (MISSING_TOPOLOGY_OR_BOUNDARY_FLUX_VALUE)
- `EHB3585_4_epsilon_projector_hair` `epsilon_projector_hair`: norm((1-P_loc)delta Phi_hair) plus induced stress/source projection (MISSING_PROJECTOR_KERNEL_AUDIT)
- `EHB3585_5_epsilon_nonEH_hair` `epsilon_nonEH_hair`: norm of retained R11/non-EH operator response in the local exterior (MISSING_EH_DOMINANCE_OR_NON_EH_VECTOR)
- `EHB3585_6_epsilon_hom_mode` `epsilon_hom_mode`: epsilon_news + epsilon_coercive_extra + epsilon_cross_hair + epsilon_top_boundary_hair + epsilon_projector_hair + epsilon_nonEH_hair (NO_CANCELLATION_HOM_STACK_READY_VALUES_MISSING)
- `EHB3585_7_epsilon_Estat_after_3585` `epsilon_Estat`: epsilon_boundary_K + epsilon_source_K + epsilon_unique_ext + epsilon_hom_mode + epsilon_extra_hair (REFINED_NONCLAIM)

## Gates
- `GATE3585_0_sources`: PASS (all source paths and selected anchors exist)
- `GATE3585_1_nohair_method`: PASS_CONDITIONAL_THEOREM (energy-identity/coercivity no-hair route is written and channelized)
- `GATE3585_2_EH_radiation`: PASS_IF_ZERO_NEWS_BOUNDARY_SIGNED (EH radiative modes are killed by stationary/no-news boundary, not by local algebra alone)
- `GATE3585_3_extra_hair_claim`: FAIL_CURRENT_CLAIM (field-specific positivity, source charge zero, cross-term, topology, and projector kernel clauses remain unsigned)
- `GATE3585_4_Estat_claim`: FAIL_CURRENT_CLAIM (epsilon_hom_mode and epsilon_extra_hair are refined but not zeroed)
- `GATE3585_5_local_GR`: FAIL_CURRENT_CLAIM (local GR/Newton still needs E_stat, gauge/corner, source coupling, GM calibration, and PPN closure)
- `GATE3585_6_bound_fallback`: PASS_NONCLAIM_FALLBACK (homogeneous/extrafield hair has explicit no-cancellation epsilon rows)

## Status
- `NO_HOMOGENEOUS_MODE_ROUTE_CHANNELIZED_NOT_ZERO_CLAIMED`: 3585 sharpens the E_stat obstruction: radiative EH modes can be killed by a zero-news/no-radiation boundary; massive/coercive extra modes can be killed by a positive self-adjoint energy identity with zero boundary/source charge; but topological/boundary, cross-term, non-EH, and projector-kernel hair remain explicit epsilon channels.
- Still missing: field-specific coercivity signs, zero source charges, zero boundary fluxes, cross-term smallness, relative cohomology/reference lock, projector kernel audit, non-EH operator vector, source coupling normalization, GM calibration, and PPN closure

## Validation
- `VAL3585_0_sources_exist`: PASS (all required 3585 source paths exist)
- `VAL3585_1_required_needles_found`: PASS (all selected 3585 anchors found)
- `VAL3585_2_outputs_exist`: PASS (all pre-validation 3585 output files written)
- `VAL3585_3_csv_parse`: PASS (source_register:17; nohom_theorem:7; channel_audit:7; epsilon_rows:8; activation_gates:7; status:1; next_target:1; canonical_status:1)
- `VAL3585_4_channel_decomposition_present`: PASS (homogeneous-mode decomposition present)
- `VAL3585_5_coercive_zero_present`: PASS (coercive extra zero theorem row present)
- `VAL3585_6_escape_channels_present`: PASS (escape-channel epsilon rows present)
- `VAL3585_7_claim_blocked`: PASS (extra hair claim remains blocked)
- `VAL3585_8_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3585_9_next_target_selected`: PASS (field-specific coercivity next target selected)
- `VAL3585_10_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3585_11_formalization_workbench_untouched`: PASS (no 3585 checkpoint output appears in formalization-workbench)

## Next target
- `NEXT3585_0` -> `3586-Y5-R2FR-field-specific-coercivity-and-source-charge-zero-or-hair-bound-fill.md`
- Objective: attack the strongest zero route inside 3585: field-specific positive/coercive extra-sector operators with zero source charge and zero boundary flux, or fill the corresponding epsilon_coercive_extra and epsilon_cross_hair rows
