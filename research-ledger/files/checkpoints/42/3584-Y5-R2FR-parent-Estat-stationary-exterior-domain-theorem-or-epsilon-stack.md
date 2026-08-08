# 3584 — parent E_stat stationary exterior theorem or epsilon stack

## Verdict
3584 finds the clean non-smuggled route to `E_stat`: if the parent exterior equations, boundary data, and source/current data are invariant under one time generator `K`, and the exterior boundary-value problem is unique modulo gauge with no radiative homogeneous kernel, then the `K`-flowed solution is the same solution.  Therefore `L_K fields=0` and the stationary exterior domain follows.

That is a real theorem pattern, not a closure axiom.  But MTS does not yet own the premises: EH/non-EH operator selection, boundary `K`, compact K-invariant source/current owner, uniqueness/no-homogeneous-mode, and extra-field silence remain unsigned.

So `E_stat` is not claimed.  The honest fallback is:

`epsilon_Estat = epsilon_boundary_K + epsilon_source_K + epsilon_unique_ext + epsilon_hom_mode + epsilon_extra_hair`.

## E_stat theorem attempt
- `PET3584_0_target`: E_stat=(D_ext,K,r,W_source,Sigma_tau,S_in,S_out,Phi_infty) (TARGET_DEFINED_BY_3583)
- `PET3584_1_operator_route`: 4D + local + diffeo invariant + metric-only + Levi-Civita + second-order + boundary-harmless => E_mn=aG_mn+bg_mn (CONDITIONAL_EH_OPERATOR_AVAILABLE)
- `PET3584_2_symmetry_inheritance`: If F(Phi)=0, L_K F=0, boundary/source data are K-invariant, and the exterior solution is unique modulo gauge, then L_K Phi=0 (MATHEMATICAL_LEMMA_CLEAN_CONDITIONAL)
- `PET3584_3_no_homogeneous_kernel`: ker(D F_ext) contains no physical time-dependent/radiative mode compatible with the chosen boundary class (MISSING_NO_RADIATIVE_HOMOGENEOUS_KERNEL_THEOREM)
- `PET3584_4_source_boundary_route`: L_K J_H=0, closure(supp J_H) compact inside S_in, and source/current owner fixed before readout (MISSING_PARENT_SOURCE_CURRENT_OWNER_FOR_ESTAT)
- `PET3584_5_Estat_construction`: K from boundary symmetry; Sigma_tau orthogonal/compatible slice; r K-invariant exterior radius; S_in/S_out regular level surfaces; W_source compact (E_STAT_DERIVED_IF_ALL_CLAUSES_SIGN)
- `PET3584_6_current_verdict`: E_stat is not claim-grade because uniqueness/no-radiative-kernel, extra-field silence, and source-current owner are unsigned (PARENT_ESTAT_NOT_PROVED_CURRENT_CORPUS)

## Stationarity clause audit
- `SCA3584_0_parent_operator` `Z_parent_operator`: CONDITIONAL_ONLY — Lovelock route is clean but its MTS premises are not parent-derived.
- `SCA3584_1_boundary_K` `Z_boundary_K`: MISSING_PARENT_BOUNDARY_TIME_GENERATOR — Needed so stationarity is inherited from a branch symmetry, not chosen after the fit.
- `SCA3584_2_source_K` `Z_source_K`: MISSING_PARENT_SOURCE_CURRENT_OWNER — Matter/current owner remains the source-side local-GR coupling problem.
- `SCA3584_3_uniqueness` `Z_unique_ext`: MISSING_EXTERIOR_UNIQUENESS_THEOREM — This is what converts symmetric data into a symmetric solution.
- `SCA3584_4_no_homogeneous_mode` `Z_no_hom_mode`: MISSING_NO_RADIATIVE_HOMOGENEOUS_KERNEL_THEOREM — This is the dangerous clause: without it, E_stat can fail even when boundary data are stationary.
- `SCA3584_5_extra_silence` `Z_extra_silence`: MISSING_EXTRA_FIELD_SILENCE_OR_RESIDUAL — Needed because EH stationarity is not enough if retained MTS fields source the observed geometry.
- `SCA3584_6_Estat` `Z_Estat`: FAIL_CURRENT_CLAIM_PREMISES_UNSIGNED — The theorem route is exact conditional; the current corpus has not signed the premises.

## Epsilon stack
- `ESE3584_0_epsilon_boundary_K` `epsilon_boundary_K`: norm(L_K boundary/reference data) (MISSING_NUMERIC_OR_PARENT_ZERO)
- `ESE3584_1_epsilon_source_K` `epsilon_source_K`: norm(L_K J_H) + tail/support leakage (MISSING_NUMERIC_OR_PARENT_ZERO)
- `ESE3584_2_epsilon_unique` `epsilon_unique_ext`: norm of nonunique exterior solution branch at fixed boundary/source data (MISSING_NUMERIC_OR_PARENT_ZERO)
- `ESE3584_3_epsilon_hom` `epsilon_hom_mode`: projection of radiative/time-dependent homogeneous exterior modes into R_ann (MISSING_NUMERIC_OR_PARENT_ZERO)
- `ESE3584_4_epsilon_extra` `epsilon_extra_hair`: local-order observed-geometry source from retained non-EH MTS fields (MISSING_NUMERIC_OR_PARENT_ZERO)
- `ESE3584_5_epsilon_Estat` `epsilon_Estat`: epsilon_boundary_K + epsilon_source_K + epsilon_unique_ext + epsilon_hom_mode + epsilon_extra_hair (NO_CANCELLATION_ESTAT_STACK_READY_VALUES_MISSING)
- `ESE3584_6_Rann_after_3584` `R_ann_abs`: C_EM_surface_gauge_abs + epsilon_Estat (REDUCED_AND_DECOMPOSED_NONCLAIM)

## Gates
- `GATE3584_0_sources`: PASS (all source paths and selected anchors exist)
- `GATE3584_1_symmetry_lemma`: PASS_CONDITIONAL_THEOREM (stationarity follows from K-invariant equations/data plus uniqueness modulo gauge)
- `GATE3584_2_EH_operator`: PASS_CONDITIONAL_ONLY (Lovelock gives EH operator only if MTS signs the premises)
- `GATE3584_3_Estat_claim`: FAIL_CURRENT_CLAIM (no-radiative homogeneous kernel, extra-field silence, and source-current owner are unsigned)
- `GATE3584_4_Newton_GR`: FAIL_CURRENT_CLAIM (Newton/local-GR transfer still needs source closure, GM calibration, coupling normalization, and PPN residual closure)
- `GATE3584_5_epsilon_stack`: PASS_NONCLAIM_FALLBACK (epsilon_Estat stack is explicit if E_stat cannot be parent-signed)

## Status
- `PARENT_ESTAT_ROUTE_DERIVED_AS_UNIQUENESS_LEMMA_BUT_NOT_SIGNED`: 3584 identifies the non-smuggled derivation route for E_stat: K-invariant parent exterior equations plus K-invariant boundary/source data plus uniqueness modulo gauge imply L_K fields=0, so the stationary exterior domain follows. This is an actual theorem pattern, not a plateau axiom.
- Still missing: MTS parent proof of the EH/non-EH operator premises, parent-owned boundary K, compact K-invariant source/current owner, exterior uniqueness/no homogeneous radiative kernel, extra-field no-hair/silence, EM gauge/corner term, source coupling normalization, and Newton/PPN calibration

## Validation
- `VAL3584_0_sources_exist`: PASS (all required 3584 source paths exist)
- `VAL3584_1_required_needles_found`: PASS (all selected 3584 anchors found)
- `VAL3584_2_outputs_exist`: PASS (all pre-validation 3584 output files written)
- `VAL3584_3_csv_parse`: PASS (source_register:13; estat_theorem:7; stationarity_clauses:7; epsilon_stack:7; activation_gates:6; status:1; next_target:1; canonical_status:1)
- `VAL3584_4_symmetry_lemma_present`: PASS (stationarity inheritance lemma present)
- `VAL3584_5_no_hom_blocker_present`: PASS (no homogeneous mode blocker present)
- `VAL3584_6_epsilon_stack_present`: PASS (epsilon_Estat stack present)
- `VAL3584_7_Estat_not_overclaimed`: PASS (E_stat remains unclaimed)
- `VAL3584_8_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3584_9_next_target_selected`: PASS (no-homogeneous-mode next target selected)
- `VAL3584_10_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3584_11_formalization_workbench_untouched`: PASS (no 3584 checkpoint output appears in formalization-workbench)

## Next target
- `NEXT3584_0` -> `3585-Y5-R2FR-no-homogeneous-exterior-mode-or-extra-hair-epsilon-row.md`
- Objective: attack the hardest unsigned clause in the E_stat theorem: prove no radiative/time-dependent homogeneous exterior mode or retained extra-field hair survives the local stationary boundary class, or write epsilon_hom_mode and epsilon_extra_hair rows
