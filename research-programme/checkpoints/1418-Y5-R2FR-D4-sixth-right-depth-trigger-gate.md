# 5402 — Sixth-right depth-trigger gate

## Purpose

The sixth-support right connector reached depth `14` at `LDLDLDRDLDLDRU`. This checkpoint applies the same path-addressed rule used on the left connector: test the exact production leaf, prove the relevant factorized angle on a closed cover, and reject any unproved shortcut.

## Results

- The production evaluator certifies the leaf with amplitude-denominator lower bound `0.0010155353873341282`.
- `108` centred-Hessian derivative comparisons reproduce the production derivatives with maximum relative error `5.837451876955707e-16`.
- Every closed factorized-angle cover passes. The `16 x 16` cover proves `Im<14> >= 0.001364553706249723`; the `32 x 32` cover proves `|<14>| >= 0.004683928473624846`.
- The confirming production resume commits the audited leaf and advances the right connector to `34` accepted and `12` pending boxes. Maximum pending depth is `13`, below the audit trigger.

## Decision

The audited transition is finite and conservative. Revision v40 may continue from the saved right-connector state. No global-univalence, regular-away `W3`, regulator-removal, local-GR, or full-MTS claim follows.

Machine-readable validation is stored in `source-intake/functional_rg/5402/P8_Y5_BRR5396_5402_VALIDATION.csv` and `source-intake/functional_rg/5402/sixth_right_depth_trigger_gate_result.json`.
