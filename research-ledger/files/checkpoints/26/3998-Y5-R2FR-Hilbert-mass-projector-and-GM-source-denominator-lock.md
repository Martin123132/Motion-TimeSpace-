# 3998 - Hilbert Mass Projector And GM Source Denominator Lock

Timestamp: `2026-07-01T18:59:38+00:00`

## Result

The Newton amplitude route is now forced through a real source denominator:

`M_H_ref[S] := N_G int_S Pi_M J_H[tau]`.

This is a parent projected Hilbert/coframe current varied before readout. It is not allowed to be defined as `mu_obs/G0`.

## Denominator Lock

Surface independence is the exact flux identity

`M_H_ref[S2]-M_H_ref[S1] = N_G int_A d(Pi_M J_H)`.

So the next real proof target is concrete: close `d(Pi_M J_H)=0`, or bound its flux/projector/reference residuals.

## Active Mass

The source in Poisson is the selected active Hilbert/Hamiltonian source. In stationary branches this is Komar/Tolman-like, and in slow weak closed systems it reduces to rest/internal/binding/field mass only after pressure, stress, boundary and non-EH corrections are retained or bounded.

## Anti-Backfill Contract

`mu_obs = G0 M_H_ref (1+delta_cal+delta_range+delta_frame+delta_PPN+delta_boundary+delta_nonEH)`.

Orbital data can test the product after `G0` and `M_H_ref` are independently fixed. It cannot define both.

## Evaluator Results

- `CASE3998_0_parent_Hilbert_denominator_zero`: status `CONDITIONAL_ZERO_PARENT_UNSIGNED`, epsilon `0.000000000000e+00`, schema=True, anti_backfill=True, claim=False
- `CASE3998_1_small_residual_vector`: status `NUMERIC_SMOKE_ONLY_NOT_EVIDENCE`, epsilon `1.500000000000e-05`, schema=True, anti_backfill=True, claim=False
- `CASE3998_2_orbital_backfill_refused`: status `ORBITAL_GM_USED_AS_MASS_DENOMINATOR`, epsilon `0.000000000000e+00`, schema=True, anti_backfill=False, claim=False
- `CASE3998_3_pressure_binding_open`: status `PRESSURE_BINDING_VECTOR_NONZERO`, epsilon `1.200000000000e-04`, schema=True, anti_backfill=True, claim=False
- `CASE3998_4_missing_parent_rows`: status `MISSING_MHREF_COMPONENT_VECTOR`, epsilon `MISSING`, schema=False, anti_backfill=True, claim=False

## Next Target

The sharpest next gate is `Pi_M/H_tau` flux closure or the first genuinely source-backed `M_H` bound row. That is where Newtonian mechanics starts becoming a derivation instead of a `GM` fit.

- `3999-Y5-R2FR-PiM-Htau-flux-closure-or-source-backed-MH-bound.md`
- `scripts/Y5_R2FR_3999_PiM_Htau_flux_closure_or_source_backed_MH_bound.py`

## Source Count

- source needles found: `17/17`
