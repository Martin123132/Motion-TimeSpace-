# 5510: D4 parent-v59 resumable epsilon-child frontier resume handoff

## Certified result

- Source: checkpoint-5509 frontier `185/3/0`, witnesses `65`.
- Processed: eight depth-first nodes beginning at `R_E0S_E1S_E0S`.
- Outcomes: four exact refinements followed by four accepted leaves.
- Refinement sequence: x, x, t, x.
- Final accepted broad leaf uses one parent-v59 t split, two live parent-v58 terminal passes and one exact aggregate.
- Proof-cache hits: zero.
- Checkpoint numerical runtime: `24589.16293260001` seconds.
- Frontier: `189/3/0`; witnesses: `69`; unresolved: zero.
- Exact global partition error: `0.0`.
- Validation: `19/19`; current source rows: `122/122`.

## Exact nested closure

The newly accepted leaves close three failed ancestors with pairwise
interior-disjoint exact rational volumes:

- Two low-t x leaves close `R_E0S_E1S_E0S_X0S_X0S_T0S`.
- Those leaves plus the high-t leaf close `R_E0S_E1S_E0S_X0S_X0S`.
- Those three plus `R_E0S_E1S_E0S_X0S_X1S` close `R_E0S_E1S_E0S_X0S`.

The four-leaf region has regular-path upper `4.79438179528512e+17`,
amplitude-denominator lower `1.9057482833921196e-08`, relative-root lower
`0.9440484658536369`, selected-global-root lower `0.30997313846330493`, and
collision-Jacobian lower `0.4600781018753027`.

## Next target

Evaluate sibling `R_E0S_E1S_E0S_X1S` under unchanged parent v59. If accepted,
combine it with the certified four-leaf low-x region to close the complete
low-epsilon parent `R_E0S_E1S_E0S` exactly. If it refines, continue the same
source-width finite-cover route and require named-parent union audits.

## Immutable evidence

- Runner: `scripts/Y5_R2FR_5510_D4_parent_v59_resumable_epsilon_child_frontier.py`
- State: `source-intake/functional_rg/5510/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`
- Result: `source-intake/functional_rg/5510/D4_parent_v59_resumable_epsilon_child_frontier_result.json`
- Validation: `source-intake/functional_rg/5510/P8_Y5_BRR5509_5510_VALIDATION.csv`
- Source register: `source-intake/functional_rg/5510/source_register.csv`
- Node audit: `source-intake/functional_rg/5510/D4_parent_v59_epsilon_child_frontier_node_audit.csv`
- Nested-union audit: `source-intake/functional_rg/5510/D4_parent_v59_epsilon_child_nested_union_audit.csv`
- V59 audit: `source-intake/functional_rg/5510/D4_parent_v59_epsilon_child_frontier_adaptive_xt_audit.csv`
- Runner SHA-256: `034dcfbe9f2165cc4de7a4746ce298f4d8537ddde4090173bf164456f159f463`
- State SHA-256: `81e25bdd048fb35f533ef8e2fb8f4d2785dfc39a481836289502d5dd83f49028`
- Result SHA-256: `757f2cb1eb46ad087c26a18b811cc42024b274631e5b429ebb522bbdf61b9d87`
- Validation SHA-256: `72f198becefa4b6c8a3ee1226f89fb61f4c66f417fa9f9966c0378c75c7ace34`
- Source-register SHA-256: `a424a8a286bd83911888f0a4908ad784029c7b630b3e40b6531503aa68346c5d`
- Node-audit SHA-256: `c0314b772f85fdc6acd022d47c0d2658a44a1c007f74a8c0df9f05c219e836e0`
- Nested-union-audit SHA-256: `3f6ca0208261ec0ba7cbc357ce77647570439c899703af3574c0a548b639e698`
- V59-audit SHA-256: `6138db7bee8f9c7e0926de85ab1d5bea9a320e0cb1861870b1c7032ac1d1f0ab`

## Claim boundary

Checkpoint 5510 certifies this four-leaf low-x region and the soundness of its
nested exact unions. It does not yet certify the complete low-epsilon parent,
active cuboid, full outer cover, event-local/combined `W3`, regulator limit,
all-operator local GR or full MTS.
