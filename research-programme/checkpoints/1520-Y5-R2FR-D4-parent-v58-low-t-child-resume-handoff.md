# 5504: D4 parent-v58 low-t child resume handoff

## Certified result

- Source: checkpoint-5503 frontier `182/5/0`, SHA-256 `eef1658f0260e74ae1b39d2dfd1614ceefc20956efb1c94f54cd23f3c9c0a483`.
- Evaluated: `R_E0S_E0S_E1S_X0S_X1S_T0S`.
- Outcome: `ACCEPTED` after `5753.04687790002` seconds.
- Regular-path upper: `2.01250633633186e+17`.
- Amplitude-denominator lower: `2.95404190746998e-08`.
- Relative-root lower: `0.958348155300218`.
- Selected-global-root lower: `0.310046463478957`.
- Collision-Jacobian lower: `0.731510745407076`.
- Enclosure: `V55_EXACT_UNIFORM_XT_LEAF_UNION_SUM`.
- Frontier: `183/4/0`; witnesses: `64`.
- Exact partition error: `0.0`.
- New v58 applications: `0`.
- Validation: `16/16`; current source rows: `81/81`.

The result is a direct unchanged-parent finite-cover certificate. No inherited
aggregate is copied into this epsilon slab and no new physical or numerical
closure rule is introduced.

## Next target

Evaluate the matching high-t sibling
`R_E0S_E0S_E1S_X0S_X1S_T1S`, epsilon `[0.0025,0.005]`, x
`[0.8571076493072545,0.8571564165685353]`, t `[0.5,1.0]`. If it passes, its
union with the checkpoint-5504 leaf must exactly close failed parent
`R_E0S_E0S_E1S_X0S_X1S`. Then combine that two-leaf result with the immutable
checkpoint-5502 three-leaf union to close `R_E0S_E0S_E1S_X0S` under five
accepted leaves.

## Immutable evidence

- Runner: `scripts/Y5_R2FR_5504_D4_parent_v58_low_t_child_gate.py`
- State: `source-intake/functional_rg/5504/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`
- Result: `source-intake/functional_rg/5504/D4_parent_v58_low_t_child_result.json`
- Validation: `source-intake/functional_rg/5504/P8_Y5_BRR5503_5504_VALIDATION.csv`
- Source register: `source-intake/functional_rg/5504/source_register.csv`
- Node audit: `source-intake/functional_rg/5504/D4_parent_v58_low_t_child_audit.csv`
- Runner SHA-256: `e98781b737fcbf3cfe64f009d8f65040840d6cab3fc834e84fd77b888abc39b9`
- State SHA-256: `74ed505b52d668d1719e99f8c992e255b6c94dd6edf266afe265f90bbb63f02d`
- Result SHA-256: `e561f8368eebf30653a6a39e6920868054f01129cb52d8baf4885683a839ce2d`
- Validation SHA-256: `5d16b27dde44ee02a95a06336256fd4d2ad3c68aab7581ace2c47a28e08a9bc1`
- Source-register SHA-256: `9e496ff443353ccedec32bc4feb82b44a9f85abcafc6e9b67eca413868bf1e24`
- Node-audit SHA-256: `2708abd28221505d797b6b46269d2ef3acde82ec83a97ba8cbd92b47745cc27a`

## Claim boundary

Checkpoint 5504 certifies one low-t leaf. It does not yet certify its two-leaf
parent, the five-leaf x region, the full active cuboid, full outer,
event-local/combined `W3`, regulator limit, all-operator local GR or full MTS.
