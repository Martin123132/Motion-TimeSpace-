# 5482: D4 parent-v56 full-integration handoff

Checkpoint 5480 migrates the parent-v55 derivation into the hash-locked checkpoint-5477 frontier. The status-only carry preserves `162` accepted, `13` pending and zero unresolved nodes exactly. Nine bounded parent-v55 evaluations then commit six accepted nodes and three exact refinements, leaving `168` accepted, `10` pending and zero unresolved nodes.

## New obstruction

The three parent-v55 refinement witnesses are not repeats of the stable-edge or first-spinor-pivot classes. They are global-contour geometric-factor failures with positive relative-root and selected-global-root bounds but a zero collision-Jacobian interval lower bound. The largest witness is:

- refinement path: `R_E0S_E0S_E0S_E0S_X0S_X0S_T0S_X1S`;
- x interval: `[0.8570588830266272, 0.8571076493072545]`;
- t interval: `[0.0002, 0.5]`;
- failure: `global contour geometric denominator reaches zero` with `collision_jacobian = 0.0`.

This is an enclosure obstruction, not evidence that the pointwise Jacobian vanishes.

## Derived candidate

Checkpoint 5481 evaluates exact rectangular x/t covers using the unchanged parent collision-Jacobian chart candidates. The theorem is

`D = union_ij D_ij` and `0 notin J(D_ij)` for every leaf implies `inf_D |J| >= min_ij dist(0, J(D_ij))`.

The schedule audit is discriminating rather than threshold-tuned:

- `4 x 128`: lower bound `0.0`;
- `8 x 128`: lower bound `0.0`;
- `16 x 128`: lower bound `218.56599306552303`;
- `16 x 128` rectangular-hull diagnostic: `218.565993065523`;
- minimum chart denominator: `6.353850106517455e-05`.

The positive candidate stops before parent acceptance by construction. It is not yet a complete-amplitude certificate and is not valid for frontier migration.

## Immutable resume source

- State: `source-intake/functional_rg/5480/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`.
- SHA-256: `df0f84303a9dfabca740f368eb8e4dd1493245c3a21b68e26cf88c2bd9d45ef5`.
- Accepted/pending/unresolved: `168/10/0`.
- Total node evaluations: `219`.
- Refinement witnesses: `51`, of which `3` belong to parent v55.

## Exact next calculation

Build checkpoint 5483 as a parent-v56 complete-amplitude target/control integration gate. Install the exact `16 x 128` collision-Jacobian leaf union only after the demonstrated parent-v55 global-contour collision-Jacobian zero-lower-bound condition. Evaluate the complete parent amplitude on the largest witness, then require an untriggered parent-v55/v56 control to be exactly unchanged. Do not migrate the frontier unless the target passes with every parent denominator positive, the exact partition is preserved and all controls pass.

The action, contour, configurations, residues and numerical acceptance thresholds remain unchanged. Full active-cuboid, full outer, event-local/combined `W3`, regulator-limit, local-GR and full-MTS claims remain false. No GitHub action and no `formalization-workbench` edit belongs to this checkpoint.

**PARENT_V56_POSITIVE_EXACT_CANDIDATE_SAVED__FULL_AMPLITUDE_GATE_NEXT**
