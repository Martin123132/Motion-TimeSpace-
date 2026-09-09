# 5475: D4 parent-v53 hash-locked frontier runner

## Carry-forward contract

The checkpoint-5473 v52 state is preserved byte-for-byte. This checkpoint owns a separate hash-locked copy. Every earlier accepted subcuboid remains valid because v53 invokes its exact t-leaf union only after the precise stable-edge singularity; otherwise it returns the unchanged v52 result.

## Current result

Accepted: `160`. Pending: `13`. Unresolved: `0`.

V53 node evaluations: `11`. V53 accepted: `10`. Stable-edge audit rows: `165`.

## Decision

**PARENT_V53_FRONTIER_PARTIAL__RESUME**

## Claim boundary

Only this active coalesced cuboid is under reconstruction. Full outer-cover, W3, regulator-limit, local-GR, and full-MTS claims remain false.
