# 5486: D4 parent-v56 first frontier-node resume handoff

Checkpoint 5484 has completed its first post-migration atomic node. The checkpoint-5485 source state was verified before evaluation, and the one-node limit prevented the runner from beginning a second expensive calculation.

## Committed node

- Refinement path: `R_E0S_E0S_E0S_E0S_X0S_X0S_T0S_X1S_X0M_T0S_X1M`.
- x interval: `[0.857071074596784, 0.8570832661669409]`.
- t interval: `[0.0002, 0.25]`.
- Evaluation method: `V55_EXACT_UNIFORM_XT_LEAF_UNION_SUM`.
- Runtime: `2910.15657289996 s`.
- Amplitude-denominator lower: `8.26712756754866e-08`.
- Relative-root lower: `0.958879523490903`.
- Selected-global-root lower: `0.310144265863533`.
- Collision-Jacobian lower: `1.07814613289885`.

The node passed without invoking the parent-v56 collision-Jacobian fallback. It emitted no refinement witness and introduced no new local repair class.

## Current frontier

- State: `source-intake/functional_rg/5484/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`.
- SHA-256: `2b521f1802065690ffb29ab8db71a9747569483ed57b832f41ceca8b1e843288`.
- Accepted/pending/unresolved: `169/9/0`.
- Parent-v56 node evaluations: `1`.
- Parent-v56 accepted nodes: `1`.
- Parent-v56 refinement witnesses: `0`.

## Exact next calculation

Resume checkpoint 5484 for one atomic node. The next pending box is
`R_E0S_E0S_E0S_E0S_X0S_X0S_T0S_X1S_X0M_T1S`, with x interval
`[0.8570588830266272, 0.8570832661669409]` and t interval `[0.25, 0.5]`.
Keep the one-node, one-core, BelowNormal contract. Preserve a pass exactly; if
a new witness appears, stop and derive it before any depth or parent change.

Full active-cuboid, full outer, event-local/combined `W3`, regulator-limit,
all-operator local-GR and full-MTS claims remain false. No GitHub action and no
`formalization-workbench` edit belongs to this checkpoint.

**PARENT_V56_FIRST_FRONTIER_NODE_ACCEPTED__ONE_NODE_RESUME_NEXT**
