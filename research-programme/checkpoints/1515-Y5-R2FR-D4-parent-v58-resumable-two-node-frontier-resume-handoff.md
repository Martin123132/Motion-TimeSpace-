# 5499: D4 parent-v58 resumable two-node frontier resume handoff

## Certified source and run

- Source: checkpoint-5498 state `179/4/0`, SHA-256 `3fb9224e90c8864568075ba5227a3eb0cfdea1bd0e17a938c9f28b1b9e4cbde7`.
- Parent: unchanged reconstruction through v57, plus exact-binding-only v58.
- Resource use: one MTS worker, one core, BelowNormal priority.
- Validation: `17/17`; current source rows: `51/51`; exact partition partition error: `0.0`.

## Node results

1. `R_E0S_E0S_E1S_X0S` -> `REFINED_X2`, runtime `412.5375010999851` seconds.
2. `R_E0S_E0S_E1S_X0S_X0S` -> `REFINED_T2`, runtime `430.04919689998496` seconds.

Both failures are `EnclosureFailure: global contour geometric denominator
reaches zero`. Collision-Jacobian lower is `0.0`; relative-root and
selected-global-root lowers stay positive. Each v56 `X16 x T128` audit remains
zero with a positive chart-denominator lower. V57 rows are explicit
`SCOPE_MISS`; new v58 application count is zero.

The frontier is `179/6/0`, with 62 retained witnesses. Its LIFO next path is
`R_E0S_E0S_E1S_X0S_X0S_T0S`, x
`[0.8570372233341658,0.8571076493072545]`, t `[0.0002,0.5]`, epsilon
`[0.0025,0.005]`.

## Next contract

1. Hash-lock all checkpoint-5499 evidence below.
2. Carry the `179/6/0` frontier exactly and preserve every source ledger as an append-only prefix.
3. Evaluate the low-t child first under unchanged parent v58 and commit it atomically.
4. Evaluate at most one depth-first successor in the same checkpoint, with an atomic save between nodes.
5. Require zero new v58 applications and retain every v57 scope miss explicitly.
6. If ordinary subdivision yields positive Jacobian lowers, continue the finite cover.
7. If zero persists, stop broad frontier work and locate the first exact zero leaf inside the v56 `X16 x T128` audit domain for this epsilon slab.

## Immutable evidence

- Runner: `scripts/Y5_R2FR_5499_D4_parent_v58_resumable_two_node_frontier_runner.py`
- State: `source-intake/functional_rg/5499/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`
- Result: `source-intake/functional_rg/5499/D4_parent_v58_resumable_two_node_result.json`
- Validation: `source-intake/functional_rg/5499/P8_Y5_BRR5498_5499_VALIDATION.csv`
- Source register: `source-intake/functional_rg/5499/source_register.csv`
- Node audit: `source-intake/functional_rg/5499/D4_parent_v58_resumable_two_node_audit.csv`
- Runner SHA-256: `0b40e436faa92226b5b8e36c075e0ce74be8d91a1581220a794a490cd1fa9962`
- State SHA-256: `c63cc94f32504abba2bf9adb5fa95e981505fd7d2a6260af8170ac60b47bd994`
- Result SHA-256: `d60c1832aa4496630f1c5ded08599841c71a657a54abe243b90c46b7ceb6d4b7`
- Validation SHA-256: `bd3269d7f16010d38e99a7eb463e251e5ae01ddc3068ebc8db7331fc33b6298c`
- Source-register SHA-256: `4d5ada1d49b7d0ed0e9f6929e9e3696ac762db0fc0c3613f7ad0d164553b403d`
- Node-audit SHA-256: `ca4f55e8547760d7787458e28088b0a4424108ae7d33a3b229e72ebb498ada83`

## Claim boundary

Checkpoint 5499 certifies two atomic refinements only. Complete active-cuboid,
full outer, event-local/combined `W3`, regulator-limit, all-operator local GR
and full MTS claims remain false.
