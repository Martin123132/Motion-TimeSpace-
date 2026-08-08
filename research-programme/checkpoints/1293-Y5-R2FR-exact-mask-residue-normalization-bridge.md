# 5277 — Exact-mask residue-normalization bridge

## Purpose

The eight-component basis and exact Boolean masks are not enough by
themselves. The pointwise contribution also needs the correct sign and
normalization:

`Delta w * orientation * C_2 / (R G (g_1'-g_2'))`,

where `C_2=lim_(delta->0) delta^2 I(G+delta)`.

## Exact sign bridge

- Root ownership is obtained directly from the analytic surface:
  a `u` root is inside when `F<0`, while a `v` root is inside when
  `F>0`.
- The local residue orientation is `+1` when the first pair label is
  owned and `-1` otherwise.
- Every active source component has `|Delta w|=2`.

All sixteen regulator/component source rows have an active exact mask
and unique ownership.

## Finite-displacement diagnosis

The legacy estimate

`C_legacy = 2 C(5e-6) - C(1e-5)`

reproduces every old material source residue to maximum relative error
`1.40684630601e-09`.
This confirms the sign, Jacobian, and winding bridge.

It also proves that the discrepancy is estimator truncation rather than
branch misidentification:

- dominant components shift by at most
  `3.56756678519e-07`;
- MC03/MC07 shift by at least
  `0.373985290981`;
- MC02/MC08 have nonzero true residues, with minimum magnitude
  `0.000734982818899`.

## Corrected source totals

- `E020`: corrected `-449.410756129+4.58916757515i`; old `-449.791410008+4.2497541365i`; relative shift `0.00113380581876`.
- `E040`: corrected `-449.357988703+9.17815356546i`; old `-449.743383329+8.84409865781i`; relative shift `0.00113380809322`.

## Acceptance gates

- `all_exact_masks_active_at_source`: **PASS**
- `all_ownership_states_unique`: **PASS**
- `all_source_winding_deltas_are_two`: **PASS**
- `claims_locked_false`: **PASS**
- `complete_two_regulator_eight_component_bridge`: **PASS**
- `corrected_totals_finite`: **PASS**
- `dominant_true_limits_stable`: **PASS**
- `formalization_workbench_unchanged`: **PASS**
- `hidden_MC02_MC08_residues_nonzero`: **PASS**
- `legacy_formula_reproduces_old_material_rows`: **PASS**
- `parent_5276_accepted`: **PASS**
- `small_component_truncation_bias_detected`: **PASS**

Validation: **PASS**.

## Claim boundary

The true local-limit residue evaluator is now normalized and may be
used in an eight-component exact-mask cubature smoke. This source-event
bridge is not itself a phase-space integral, UV coefficient, local-GR
result, or full-MTS claim.
