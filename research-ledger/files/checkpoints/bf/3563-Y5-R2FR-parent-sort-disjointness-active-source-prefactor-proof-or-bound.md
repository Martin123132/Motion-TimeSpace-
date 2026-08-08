# 3563 - Parent sort disjointness active-source-prefactor proof or bound

## Verdict
3563 takes the leap and rejects the live proof for now: the parent sort/no-Hom constructor theorem is exact conditionally, but current MTS does not parent-derive the constructor from primitives. Therefore the source-weight vector is now the official nonclaim density fallback.

This is progress, not retreat. We stop spending cycles re-saying `no-Hom missing`; future density/local-GR work must either bring a new parent sort constructor proof or use the official fallback rows.

## Constructor theorem
If `ActiveSourcePrefactor` is not a primitive parent sort, and the active source coefficient constructor has domain only `UniversalCalibration + total Hilbert source + explicit residual slots`, then species labels, hidden markers, readout selectors and worldtube selectors have no non-common incoming `Hom` into active source weights.

The proof fails live because constructor exhaustion, source-label forgetting, no-marker exhaustion and readout/action-scale stability are not parent-signed.

## What moved
- The conditional proof is preserved as an exact theorem target.
- Counterexamples remain explicit instead of hand-waved.
- The finite source-weight vector is promoted to official nonclaim fallback.
- Next work should move to a different gate: non-Hilbert source bypass or common coupling owner.

## Generated outputs
- `source_register`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3563_SOURCE_REGISTER.csv`
- `constructor_theorem`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3563_PARENT_SORT_CONSTRUCTOR_THEOREM.csv`
- `clause_audit`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3563_SORT_CLAUSE_AUDIT.csv`
- `official_fallback`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3563_OFFICIAL_DENSITY_FALLBACK_ROWS.csv`
- `decision_ledger`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3563_DECISION_LEDGER.csv`
- `status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3563_STATUS.csv`
- `next_target`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3563_NEXT_TARGET.csv`
- `canonical_status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_parent_sort_disjointness_official_fallback_status.csv`
- `validation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3563_VALIDATION.csv`

## Constructor theorem rows
- `PSD3563_0_constructor_signature`: A parent constructor C_MTS must generate public geometry Q_obs, ordinary matter fields, representation constants, gauge/current data, universal calibration, readout maps and explicit residual slots before fitting.
- `PSD3563_1_conditional_disjointness_proof`: If ActiveSourcePrefactor is not a primitive parent sort and the only scalar endomorphism of the action-density line is common calibration, then no non-common Hom from SpeciesLabel, HiddenMarker, ReadoutSelector or WorldtubeSelector to ActiveSourcePrefactor exists.
- `PSD3563_2_product_sequester_corollary`: If C_parent factors into visible source data times bookkeeping labels and the source coefficient functor factors only through the visible projection, label tangents annihilate active-source coefficients.
- `PSD3563_3_counterexample_obstruction`: If parent constructor exhaustion is absent, species constants, hidden invariant scalars, domain/material markers, boundary masks, action-scale coefficients and readout selectors can still be legal active-source coefficient arguments.
- `PSD3563_4_fallback_promotion`: Because parent sort construction and constructor exhaustion are not signed, the 3562 source-weight rows become the official nonclaim density-owner fallback until the parent sort proof is actually derived.
- `PSD3563_5_local_GR_effect`: A signed parent sort proof would narrow source universality but still would not by itself close local GR; EH origin, common coupling owner, source-current closure, PPN equations and residual silence remain separate gates.

## Clause audit
- `PSC3563_0_parent_sorts`: derive disjoint parent sorts from MTS primitives -> MISSING_PRIMITIVE_SORT_CONSTRUCTION
- `PSC3563_1_constructor_exhaustion`: all source/action constructors factor through allowed arguments before readout -> MISSING_CONSTRUCTOR_EXHAUSTION
- `PSC3563_2_active_source_domain`: ActiveSourcePrefactor domain only UniversalCalibration + total Hilbert source + retained residuals -> CONSTRUCTOR_DOMAIN_NOT_DERIVED
- `PSC3563_3_source_label_forgetting`: source functor forgets species labels before choosing gravitational/source coupling -> SOURCE_LABEL_FORGETTING_NOT_DERIVED
- `PSC3563_4_no_marker_extension`: no hidden/material/readout marker extends active-source coefficient domain -> NO_MARKER_EXHAUSTION_UNSIGNED
- `PSC3563_5_action_scale_stability`: one action-scale/measure owner and readout/radiative stability preserve no-Hom -> ACTION_SCALE_READOUT_STABILITY_UNSIGNED
- `PSC3563_6_common_calibration_split`: common scalar mode separated from relative source weights -> COMMON_CALIBRATION_ALLOWED_NONPREDICTIVE
- `PSC3563_7_fallback_basis`: finite Delta_w/source-weight fallback basis exists -> BASIS_SCHEMA_NONCLAIM_AVAILABLE

## Official fallback rows
- `FB3563_0_delta_w_species` `delta_w_species`: OFFICIAL_NONCLAIM_FALLBACK_ROW
- `FB3563_1_kappa_A_source` `kappa_A_source`: OFFICIAL_NONCLAIM_FALLBACK_ROW
- `FB3563_2_hidden_marker_source` `hidden_marker_source`: OFFICIAL_NONCLAIM_FALLBACK_ROW
- `FB3563_3_hidden_frame` `A_A(X);disformal_A(X)`: OFFICIAL_NONCLAIM_FALLBACK_ROW
- `FB3563_4_readout_worldtube_mask` `Delta_mask`: OFFICIAL_NONCLAIM_FALLBACK_ROW
- `FB3563_5_common_mode` `w_*;D_t ln w_*`: COMMON_MODE_NOT_RELATIVE_SOURCE_RESIDUAL
- `FB3563_6_nonHilbert_bypass` `nonHilbert_source_bypass`: OUTSIDE_SORT_NOHOM_OFFICIAL_FALLBACK
- `FB3563_7_total_envelope` `R_source_weight`: OFFICIAL_NONCLAIM_TOTAL_ENVELOPE

## Decision ledger
- `DEC3563_0`: Parent sort disjointness proof remains conditional, not live. The typed proof is correct if constructor exhaustion is parent-derived, but current MTS has not derived the constructor from primitives.
- `DEC3563_1`: Official nonclaim density fallback selected. Future local-GR source-density work should stop restating no-Hom and use the source-weight fallback rows unless a new parent constructor proof appears.
- `DEC3563_2`: Common calibration remains allowed. A universal common action/source scale is treated like GR's calibrated G, but relative species/hidden/readout weights remain forbidden-or-bounded.
- `DEC3563_3`: Next target should leave source weights and attack non-Hilbert bypass or common coupling owner. Because the no-Hom proof is now officially fallbacked, the best next derivation target is a different live gate, not another no-Hom restatement.

## Next target
- `3564-Y5-R2FR-nonHilbert-source-bypass-improvement-zero-or-bound.md`
- Objective: try to prove retained non-Hilbert source currents are exact improvements with zero exterior flux; if not, promote nonHilbert_source_bypass and boundary_flux rows as the next official density/source-current fallback
