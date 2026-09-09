# 5473: D4 parent-v52 hash-locked frontier runner

## Carry-forward rule

The checkpoint-5469 v51 state is preserved unchanged. This checkpoint creates a separate hash-locked copy. Every v51 passing leaf remains valid because parent v52 returns the original v51 geometric factors without invoking its fallback whenever the v51 collision-Jacobian lower bound is positive. Only newly evaluated zero-lower boxes may use the checkpoint-5472 finite leaf-union theorem.

## Current state

Accepted subcuboids: `150`. Pending: `22`. Unresolved: `0`.

New v52 evaluations: `8`. New v52 accepted subcuboids: `4`. V52 leaf-union fallback rows: `1`.

## Decision

**PARENT_V52_FRONTIER_PARTIAL__RESUME**

## Claim boundary

The active cuboid is certified only when its pending and unresolved counts both reach zero and exact partition volume is preserved. Full outer cover, W3, the regulator limit, local GR and full MTS remain unclaimed.
