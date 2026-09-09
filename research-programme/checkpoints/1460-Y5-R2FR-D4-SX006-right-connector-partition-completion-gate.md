# 5444: S_X006 right-connector partition completion gate

## Decision

**THE S_X006 MC04_SP_DP RIGHT-CONNECTOR PARTITION IS COMPLETE.**

Parent v49 exhausted the adaptive stack for regulator slab `bin_00/sub_00` and wrote the completed path CSV. This closes the exact production branch that exposed the external01 and collision-Jacobian enclosure failures repaired in checkpoints 5438-5441.

## Certified cover

- Leaves: `735`.
- Domain: `x in [0.31522842174025956, 0.3545559579457481]`, `t in [0,1]`.
- Prefix-free Kraft sum: `1.0`.
- Parameter-area sum: `0.03932753620548857` against expected `0.03932753620548857`.
- Maximum refinement depth: `17` of `18`.
- Minimum amplitude denominator: `0.00010237716235513576`.
- Minimum collision Jacobian: `0.7281267861815186`.

## Production transition

- Accepted count at v49 integration: `564`.
- Final completed leaf count: `735`.
- The target state file is removed: `True`.
- Parent advanced to `bin_00_sub_00_S_X007_MC04_SM_DM_TOP_part_00_of_01.state.json`.

## Claim boundary

This is a genuine finite-cover completion for one mapped cell, path segment, and regulator slab. Other path jobs and the second regulator slab remain; no all-right-connector, regular-away W3, UV, local-GR, or full-MTS claim is made.
