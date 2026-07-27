# 3995 - Current Normalization z_g Zero Or Joint Alpha/F2 Bound

Timestamp: `2026-07-01T18:40:30+00:00`

## Result

`z_g` is now split into a normalization-gauge leg and a physical source-slot leg.

The invariant coupling is not naked `z_g`; it is

`b_alpha = 2 z_g - s_XF2`.

Under `A_Q -> exp(sigma) A_Q`, `z_g -> z_g-Dsigma` and `s_XF2 -> s_XF2-2Dsigma`, so `b_alpha` is unchanged. That means a pure `z_g` drift can be bookkeeping, not physics.

## Ward-Current Gauge

If the visible charge current is varied before readout from the same q-basic matter action, choose `Dsigma=z_g`. Then `z_g'=0` and `s_XF2'=-b_alpha`.

This is better than claiming a mystical standalone `z_g=0`: it says the same-current branch should score the invariant alpha/F2 coupling, while source-slot/readout/radiative tails remain explicit residuals.

## Finite Bound

The 3994 EM/DD proxy gives `|b_alpha_channel| <= 7.296589096859e-10` in the single `Q_e` route, with readout floor `9.800000000000e-01` and DD weight `3.775876651739e-06`.

In arbitrary normalization gauge we still keep

`|s_XF2| <= |b_alpha| + 2|z_g|`.

In Ward-current gauge this tightens to

`|s_XF2'| = |b_alpha|`.

## Evaluator Results

- `CASE3995_0_Ward_current_gauge_zero`: status `CONDITIONAL_ZERO_GAUGE_NOT_PARENT_CLAIM`, identity `0.000000000000e+00`, eta `0.000000000000e+00`, claim=False
- `CASE3995_1_pure_rescaling_countermodel`: status `PURE_ZG_NOT_OBSERVABLE_IF_BALPHA_ZERO`, identity `0.000000000000e+00`, eta `0.000000000000e+00`, claim=False
- `CASE3995_2_alpha_bound_current_gauge`: status `DD_ALPHA_PROXY_NONCLAIM`, identity `0.000000000000e+00`, eta `2.700000000000e-15`, claim=False
- `CASE3995_3_live_zg_source_tail`: status `MISSING_SOURCE_SLOT_BOUND`, identity `MISSING`, eta `MISSING`, claim=False
- `CASE3995_4_readout_radiative_reentry`: status `MISSING_READOUT_RADIOUT_CLOSURE`, identity `MISSING`, eta `MISSING`, claim=False

## Current Closure Gate

This moves the problem forward: the next hard thing is not a vague `z_g` hunt. It is the explicit physical tail

`B_zg_source_tail <= |D ln kappa_A|+|D ln w_A|+|D ln R_A|+|z_rad|`.

Those terms are real only if they enter before variation/readout projection. If the parent grammar excludes them, the EM source branch gets much cleaner. If not, they become numeric product rows.

## Guard

This does not derive the absolute value of `alpha_EM`, just as local GR recovery does not require deriving the numerical value of Newton's constant. The live target is local drift/source-product silence or bounded residuals.

## Source Count

- source needles found: `18/18`

## Next Target

- `3996-Y5-R2FR-prevariation-EM-source-slot-exclusion-or-balpha-source-product-bound.md`
- `scripts/Y5_R2FR_3996_prevariation_EM_source_slot_exclusion_or_balpha_source_product_bound.py`
