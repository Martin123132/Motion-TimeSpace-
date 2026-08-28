# 5400 — Generalized depth-trigger audit gate

## Purpose

Checkpoint 5396 first brought the active `S_X003_MC04_SP_DM` left connector to depth `14`. This checkpoint tests that exact leaf instead of raising the production depth gate or assuming that a repeated interval failure is physical.

## Audit contract

The existing angle, centred-Jacobian, and Gale–Nikaido runners now accept `mapped_cell_id`, `term_id`, and `path_segment`. Their historical `S_X002_MC04_SP_DM` right-connector settings remain defaults, while explicit path-addressed runs can audit any connector without editing formulas or silently reading a stale completed state.

The audited leaf is

\[
x\in[0.291159434430488,0.2912975122956845],\qquad
t\in[0.0078125,0.015625],
\]

at refinement path `RDRDRDLDRDLDRU`.

## Results

- `108` centred-Hessian derivatives reproduce the production dual derivatives with maximum relative error `4.031539536365012e-16`.
- All closed factorized-angle covers pass. The `16 x 16` cover proves `Im<14> >= 0.0021797980304410582`; the `32 x 32` cover gives `|<14>| >= 0.005027441170423727`.
- The Gale–Nikaido `1`, `2`, and `4` subdivision schemes remain unsigned, so `global_univalence_proved=false`. No global Jacobian shortcut is promoted.
- The production evaluator certifies the audited leaf by its ordinary pointwise route with amplitude-denominator lower bound `0.0010892239252466565`.
- The confirming resume advances the connector to `84` accepted and `7` pending boxes and lowers maximum pending depth from `14` to `10`.

## Decision

The depth-fourteen transition is a finite conservative enclosure transition, not evidence of a new zero. Revision v40 may continue from the preserved state. This checkpoint does not certify the full regular-away integral, global univalence, regulator removal, local GR, or full MTS.

Machine-readable evidence is written to `source-intake/functional_rg/5400/P8_Y5_BRR5396_5400_VALIDATION.csv` and `source-intake/functional_rg/5400/generalized_depth_trigger_audit_gate_result.json`.
