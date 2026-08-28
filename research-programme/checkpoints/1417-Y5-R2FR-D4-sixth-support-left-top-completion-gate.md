# 5401 — Sixth-support left/top completion gate

## Purpose

Checkpoint 5401 verifies the second depth-fourteen transition in `S_X003_MC04_SP_DM`, then proves that production actually completed the left connector and top path before moving to the right connector.

## Second trigger leaf

The audited path `RDRDRDRDRDLDRU` covers

\[
x\in[0.2922640573520605,0.29240213521725705],\qquad
t\in[0.0078125,0.015625].
\]

- `108` centred-Hessian derivative comparisons pass with maximum relative error `9.099443547528498e-15`.
- Every factorized-angle cover is nonzero. The `16 x 16` cover proves `Im<14> >= 0.0014911446327966968`; the `32 x 32` cover proves `|<14>| >= 0.004724186964500759`.
- The ordinary production evaluator certifies the leaf with amplitude-denominator lower bound `0.001027653220649849`. No global-univalence shortcut or fitted lower bound is used.

## Production result

- The sixth-support left connector completes at `110` certified boxes.
- The sixth-support top path completes at `1` certified box.
- Production advances from `15/240` to `17/240` completed paths.
- The right connector begins with `0` accepted and `4` pending boxes at maximum depth `3`; its state is revision-v40 and resume-safe.

## Claim boundary

This checkpoint authorizes resuming the sixth-support right connector. It does not establish global univalence, the atlas-wide regular-away `W3`, regulator removal, local GR, or full MTS.

Machine-readable validation is stored in `source-intake/functional_rg/5401/P8_Y5_BRR5396_5401_VALIDATION.csv` and `source-intake/functional_rg/5401/sixth_support_left_top_completion_gate_result.json`.
