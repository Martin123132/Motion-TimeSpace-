# 5478: D4 parent-v55 stable-edge x/t-leaf-union integration gate

The v54 frontier showed that the t-only stable-edge union can still fail on x-wide boxes. Parent v55 changes no physics object: after that exact stable-edge error only, it evaluates the complete parent-v54 amplitude over an exact rectangular x/t source cover and aggregates the certified leaf bounds without replacing their image union by one convex hull.

V54 target failure reproduced: `True`. V55 target passed: `True` on `2 x 32` leaves.

Parent amplitude-denominator lower: `2.3640791503504712e-07`. The weaker centered-invariant diagnostic is `0.0` and is not used as a gate. Jacobian lower: `0.023597972930495505`. Control unchanged: `True`.

**PARENT_V55_STABLE_EDGE_XT_LEAF_UNION_CERTIFIED__MIGRATE_FRONTIER**

The active cuboid and every broader claim remain open until frontier migration completes.
