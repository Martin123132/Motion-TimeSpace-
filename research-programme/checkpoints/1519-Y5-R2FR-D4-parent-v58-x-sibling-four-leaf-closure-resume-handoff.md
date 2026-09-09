# 5503: D4 parent-v58 x-sibling four-leaf closure resume handoff

## Certified result

- Source: checkpoint-5502 frontier `182/4/0`, SHA-256 `fa7e401c5981d83c12dffdbb9e4cc8b9e9d1847fe4393f3509fcde883fca892c`.
- Evaluated: `R_E0S_E0S_E1S_X0S_X1S`.
- Outcome: `REFINED_T2` after `1473.162050899933` seconds.
- Failure class: `IntervalSingularity` at `away_arc_left_K5:s1:c0:left1:edge_2_1_3:stable_edge`.
- Children: `R_E0S_E0S_E1S_X0S_X1S_T0S` and `R_E0S_E0S_E1S_X0S_X1S_T1S`.
- Frontier: `182/5/0`; witnesses: `64`.
- Exact partition error: `0.0`.
- New v58 applications: `0`.
- Validation: `16/16`; current source rows: `75/75`.

The broad sibling does not yet close the four-leaf parent union. This is an
ordinary source-width time refinement, not evidence for a new parent action,
contour rule or certificate. The checkpoint-5502 exact three-leaf union remains
accepted and unchanged.

## Next target

Evaluate `R_E0S_E0S_E1S_X0S_X1S_T0S`, epsilon `[0.0025,0.005]`, x
`[0.8571076493072545,0.8571564165685353]`, t `[0.0002,0.5]`. Use one core,
BelowNormal priority and evaluate-before-commit atomicity. If it passes, test
the exact high-t sibling and close `R_E0S_E0S_E1S_X0S_X1S` as a two-leaf
union. If it fails, refine only that low-t child and preserve all existing
accepted leaves.

## Immutable evidence

- Runner: `scripts/Y5_R2FR_5503_D4_parent_v58_x_sibling_four_leaf_closure_gate.py`
- State: `source-intake/functional_rg/5503/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`
- Result: `source-intake/functional_rg/5503/D4_parent_v58_x_sibling_four_leaf_closure_result.json`
- Validation: `source-intake/functional_rg/5503/P8_Y5_BRR5502_5503_VALIDATION.csv`
- Source register: `source-intake/functional_rg/5503/source_register.csv`
- Node audit: `source-intake/functional_rg/5503/D4_parent_v58_x_sibling_audit.csv`
- Runner SHA-256: `2da752bee1bac66d04986112a99e14f56cc85c2977a936b8c8f20b69ce0531e5`
- State SHA-256: `eef1658f0260e74ae1b39d2dfd1614ceefc20956efb1c94f54cd23f3c9c0a483`
- Result SHA-256: `30bc138acfeb43c169741a59b7fe52efce9a0c156945668559f76082b6bcf4d9`
- Validation SHA-256: `8c2fa7b7878dd19a0c45a495dbc9bec565f243dfcead39b2bc82722dc3a375ac`
- Source-register SHA-256: `d11fc68435fa08a288a67b2eb72c45f1d9eccc3c397412f6387d20fcda93bf8d`
- Node-audit SHA-256: `9ace90c064b93a903cb2b3d33a6a8dba877d544b04b7ecc85e5761ff20ea405d`

## Claim boundary

Checkpoint 5503 certifies one exact atomic refinement and preserves the
checkpoint-5502 three-leaf finite union. It does not certify the failed broad
x sibling, its four-leaf parent, the full active cuboid, full outer,
event-local/combined `W3`, regulator limit, all-operator local GR or full MTS.
