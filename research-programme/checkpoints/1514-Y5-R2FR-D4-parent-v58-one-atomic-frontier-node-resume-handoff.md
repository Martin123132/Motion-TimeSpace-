# 5498: D4 parent-v58 one atomic frontier node resume handoff

## Source lock

- Checkpoint-5497 source state: `179/3/0`, SHA-256 `0bb34051ffe2e603d6429fd2a6aab76b285633f2a81db0e63787f2c73024a69f`.
- Evaluated path: `R_E0S_E0S_E1S`, epsilon `[0.0025,0.005]`, full target x/t box.
- Parent: exact reconstruction through v57 plus the checkpoint-5496 source-bound v58 certificate.
- Resource contract: one core, BelowNormal priority, one MTS numerical worker.

## Atomic result

- Runtime: `509.20579050004017` seconds.
- Outcome: `REFINED_X2`.
- Failure class: `EnclosureFailure`.
- Failure: `global contour geometric denominator reaches zero`.
- Collision-Jacobian interval lower: `0.0`.
- Relative-root lower: `0.9945369405616669`.
- Selected-global-root lower: `3.21968970897564`.
- Children: `R_E0S_E0S_E1S_X0S` and `R_E0S_E0S_E1S_X1S`.
- Frontier: `179/4/0`; witnesses: `60`; exact partition error: `0.0`.
- New parent-v58 applications: `0`.
- Validation: `16/16` gates pass; `45/45` registered sources are current.

## Next calculation

The LIFO node is `R_E0S_E0S_E1S_X0S`. Evaluate it under the unchanged v58
parent. If it passes, commit one accepted node. If it reaches the same
collision-Jacobian class, apply only the inherited source-width split and
continue atomically. Do not transplant the checkpoint-5496 target certificate:
its binding is different and checkpoint 5498 proves application count remains
zero here.

## Immutable evidence

- Runner: `scripts/Y5_R2FR_5498_D4_parent_v58_one_atomic_frontier_node.py`
- State: `source-intake/functional_rg/5498/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`
- Result: `source-intake/functional_rg/5498/D4_parent_v58_one_atomic_frontier_node_result.json`
- Validation: `source-intake/functional_rg/5498/P8_Y5_BRR5497_5498_VALIDATION.csv`
- Source register: `source-intake/functional_rg/5498/source_register.csv`
- Node audit: `source-intake/functional_rg/5498/D4_parent_v58_one_atomic_frontier_node_audit.csv`
- Runner SHA-256: `8ff72aa9a079e7bbca4144e00be186f99a3b2f34e1fb94f468881a2342e09c87`
- State SHA-256: `3fb9224e90c8864568075ba5227a3eb0cfdea1bd0e17a938c9f28b1b9e4cbde7`
- Result SHA-256: `0c22ac6481eac41bb884bf866e1e6d8b60c742350bf87d4a6b3483b3a6e280b5`
- Validation SHA-256: `faa01d8bb09d9566170ce8b985ffa8a7c310f189273c8b83d610eedfa8f2c142`
- Source-register SHA-256: `ffea2c533775304833d616b75bbd31fba36313b87e8db944d695038e30424ac6`
- Node-audit SHA-256: `7ed4a1a9a66ba9ecc6c5806ac48fef124b2146aa97fb65933e4664162e5667e7`

## Claim boundary

Checkpoint 5498 certifies one node evaluation and its exact refinement. It does
not certify the complete active cuboid, full outer enclosure, event-local or
combined `W3`, the regulator limit, all-operator local GR or full MTS.
