# 5487: D4 parent-v56 two-node frontier resume handoff

Checkpoint 5484 advances through two additional atomic nodes from the checkpoint-5486 state. Both are committed passes; neither produces a refinement witness or requires a new parent revision.

## First node: t-high inner sibling

- Refinement path: `R_E0S_E0S_E0S_E0S_X0S_X0S_T0S_X1S_X0M_T1S`.
- x interval: `[0.8570588830266272, 0.8570832661669409]`.
- t interval: `[0.25, 0.5]`.
- Method: `V53_EXACT_UNIFORM_T_LEAF_UNION_SUM`.
- Runtime: `75.3019853999722 s`.
- Amplitude-denominator lower: `7.38912229034473e-06`.
- Collision-Jacobian lower: `1.36424497524763`.

This node does not invoke parent v56.

## Second node: broad right-half sibling

- Refinement path: `R_E0S_E0S_E0S_E0S_X0S_X0S_T0S_X1S_X1M`.
- x interval: `[0.8570832661669409, 0.8571076493072545]`.
- t interval: `[0.0002, 0.5]`.
- Method: `V55_EXACT_UNIFORM_XT_LEAF_UNION_SUM`.
- Runtime: `10905.0779756 s`.
- Amplitude-denominator lower: `1.56457263377374e-09`.
- Relative-root lower: `0.958783557387883`.
- Selected-global-root lower: `0.310115769608701`.
- Collision-Jacobian lower: `0.780781591390064`.

This node invokes parent v56 once. The exact `16 x 128` Jacobian union passes with leaf-union lower `250.5009733405172`, rectangular-hull lower `248.14541457981065`, chart-denominator lower `6.353894055753064e-05` and exact-cover error `0.0`.

## Current frontier

- State: `source-intake/functional_rg/5484/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`.
- SHA-256: `ca9c9b7aebfcbe6258d121961f8c4da4ee49537abe4aaf016229fa406a765bd2`.
- Accepted/pending/unresolved: `171/7/0`.
- Parent-v56 node evaluations: `3`.
- Parent-v56 accepted nodes: `3`.
- Parent-v56 refinement witnesses: `0`.

The very small but strictly positive `1.56457263377374e-09` amplitude-denominator lower is retained exactly and must not be described as a uniform global margin.

## Exact next calculation

Resume checkpoint 5484 for one atomic node. The next box is
`R_E0S_E0S_E0S_E0S_X0S_X0S_T1S`, with x interval
`[0.8570372233341658, 0.8571076493072545]` and t interval `[0.5, 1.0]`.
Keep one BelowNormal core. Preserve a pass; stop and derive any new witness before
changing the parent, depth or acceptance threshold.

Full active-cuboid, full outer, event-local/combined `W3`, regulator-limit,
all-operator local-GR and full-MTS claims remain false. No GitHub action and no
`formalization-workbench` edit belongs to this checkpoint.

**PARENT_V56_TWO_MORE_NODES_ACCEPTED__ONE_NODE_RESUME_NEXT**
