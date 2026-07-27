# 3997 - Common G Source Calibration Owner Or Gdot/PPN Bound

Timestamp: `2026-07-01T18:52:24+00:00`

## Result

This checkpoint answers the Newton-constant issue cleanly.

A serious local-GR/Newton reduction does **not** need MTS to derive the decimal SI value of `G`. GR itself uses one measured coupling. What MTS must derive or bound is stricter and more useful:

- the coupling is one common branch constant;
- it is derivative-silent over local tests;
- it multiplies the same Hilbert source denominator;
- it is not secretly backfilled from orbital `GM`.

## Calibration Law

`G0 := G_ref C_*(p0)`, and `kappa0 := 8*pi*G0/c^4`.

If `D ln C_* = 0` in time/radius/range/frame/domain and the source denominator is locked, the weak-field equation gives

`nabla^2 Phi = 4*pi*G0 rho_H`.

That is the right comparison with GR: derive the reduction and constancy, not pretend the numerical value appears from nowhere.

## Bound Branch

If derivative silence is not proved, the retained absolute-sum budget is

`B_Gdot = |D_t ln G_ref|+|D_t ln C_*|+|D_t ln w_common|+|D_t ln ell_J|+|D_t ln R_frame|+|D_t ln M_eff|+|D_t epsilon_mu|+|D_t ln Z_Poisson|+|D_t ln Z_frame|`.

The current nonclaim comparator budget is `9.600000000000e-15 yr^-1`.

## Evaluator Results

- `CASE3997_0_parent_superselection_zero`: status `CONDITIONAL_ZERO_PARENT_UNSIGNED`, B_Gdot `0.000000000000e+00`, pass=True, claim=False
- `CASE3997_1_constant_calibrated_G0`: status `CALIBRATED_CONSTANT_NOT_DECIMAL_G_CLAIM`, B_Gdot `0.000000000000e+00`, pass=True, claim=False
- `CASE3997_2_half_budget_common_drift`: status `NUMERIC_SMOKE_ONLY_NOT_EVIDENCE`, B_Gdot `4.800000000000e-15`, pass=True, claim=False
- `CASE3997_3_missing_components`: status `MISSING_GDOT_COMPONENT_VECTOR`, B_Gdot `MISSING`, pass=False, claim=False
- `CASE3997_4_oversized_common_drift`: status `OVERSIZED_GDOT_SMOKE_BLOCKS`, B_Gdot `1.920000000000e-14`, pass=False, claim=False

## PPN Guard

First-order `G0` calibration fixes the Newtonian potential convention. It does not prove `gamma=1`, `beta=1`, preferred-frame silence, or conservation-law PPN channels. Those remain component gates.

## Next Target

The next obstruction is the mass/source denominator: calibrated `G0` must multiply parent-owned `M_H`, not an orbital `GM` that already absorbed the residual.

- `3998-Y5-R2FR-Hilbert-mass-projector-and-GM-source-denominator-lock.md`
- `scripts/Y5_R2FR_3998_Hilbert_mass_projector_and_GM_source_denominator_lock.py`

## Source Count

- source needles found: `17/17`
