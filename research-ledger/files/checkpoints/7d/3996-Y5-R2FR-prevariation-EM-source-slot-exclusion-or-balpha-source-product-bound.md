# 3996 - Prevariation EM Source-Slot Exclusion Or b_alpha Source Product Bound

Timestamp: `2026-07-01T18:46:49+00:00`

## Result

The source-slot problem is now split cleanly.

Relative prevariation slots like `w_A^rel`, `c_A_pre`, `kappa_A`, and hidden/material source markers are ill-typed if the parent matter action has one typed density line, variation-before-readout, source-label forgetting, and no Hom into an active-source-prefactor object.

That is not a public local-GR claim yet, because the parent grammar is not fully signed. But it is a real narrowing: if the theorem closes, these terms vanish by syntax, not by tuning.

## Common Scalar

A common multiplier `w_*` is different. It scales all Hilbert sources together:

`T_source = w_* T_total`.

That is not WEP/composition poison by itself. It is the GR-like common `G_ref` or source-calibration gate. This matters because GR also uses Newton's constant as a calibrated coupling; the danger is drift/range/source-domain dependence, not the mere existence of one common coupling.

## Finite Product Vector

The retained finite branch is

`B_EM_source = |b_alpha|+|Dln c_pre|+|Dln w_rel|+|Dln kappa_A|+|Dln R_A|+|z_rad|`

with proxy projection

`eta_EM_source <= readout_floor |Qe_Earth DeltaQe| B_EM_source`.

For the current EM/DD proxy, `readout_floor=9.800000000000e-01`, `|Qe_Earth DeltaQe|=3.775876651739e-06`, and `eta_bound=2.700000000000e-15`.

## Evaluator Results

- `CASE3996_0_source_slot_theorem_zero`: status `CONDITIONAL_ZERO_THEOREM_UNSIGNED`, B `0.000000000000e+00`, eta `0.000000000000e+00`, pass=True, commonG=False
- `CASE3996_1_alpha_proxy_no_source_tail`: status `DD_ALPHA_PROXY_NONCLAIM`, B `7.296589096859e-10`, eta `2.700000000000e-15`, pass=True, commonG=False
- `CASE3996_2_small_finite_source_tail`: status `NUMERIC_SMOKE_ONLY_NOT_EVIDENCE`, B `4.742782912958e-10`, eta `1.755000000000e-15`, pass=True, commonG=False
- `CASE3996_3_common_scalar_only`: status `COMMON_SCALAR_NOT_COMPOSITION_SOURCE_BUT_G_GATE_OPEN`, B `0.000000000000e+00`, eta `0.000000000000e+00`, pass=True, commonG=True
- `CASE3996_4_missing_source_slot_inputs`: status `MISSING_SOURCE_SLOT_VECTOR`, B `MISSING`, eta `MISSING`, pass=False, commonG=False
- `CASE3996_5_large_tail_fails_proxy`: status `OVERSIZED_TAIL_SMOKE_BLOCKS`, B `2.918635638744e-09`, eta `1.080000000000e-14`, pass=False, commonG=False

## Current Closure Gate

3996 removes a major ambiguity: the next target is no longer the whole messy source-slot cloud. The next target is the universal common scalar: either derive the parent owner of `G_ref`/common source calibration, or bound its drift/range effect using Newton/PPN/Gdot-style rows.

## Source Count

- source needles found: `16/16`

## Next Target

- `3997-Y5-R2FR-common-G-source-calibration-owner-or-Gdot-PPN-bound.md`
- `scripts/Y5_R2FR_3997_common_G_source_calibration_owner_or_Gdot_PPN_bound.py`
