# 5474: D4 parent-v53 stable-edge t-leaf-union integration gate

## Derived enclosure law

The v52 frontier isolated `away_arc_left_K5:s1:c0:left1:edge_2_1_3:stable_edge`. The parent already partitions the left first-soft invariant internally, but then replaces its disconnected finite image union by one rectangular hull. That hull can contain zero even when every source leaf excludes zero.

Parent v53 changes no action, contour, selector, residue, or acceptance threshold. Only after the precise connector stable-edge singularity occurs, it partitions the original path-parameter interval into an exact finite cover, evaluates the complete unchanged v52 amplitude on every leaf, sums the integrated upper bounds, and takes minima of all denominator lower bounds.

## Result

The v52 target fails as expected: `True`. The same target passes v53: `True` using `8` leaves.

Minimum explicit left first-soft invariant lower: `1.2641887320927728e-07`. Minimum full-amplitude denominator lower: `1.2641887320927728e-07`. Minimum collision-Jacobian lower: `6.454166047674096`.

The untriggered v52/v53 control is exactly unchanged: `True`.

## Decision

**PARENT_V53_STABLE_EDGE_T_LEAF_UNION_CERTIFIED__MIGRATE_FRONTIER**

## Claim boundary

This proves a parent-level finite-union repair for one amplitude stable-edge enclosure class. It does not yet certify the active cuboid, full outer cover, W3, regulator limit, local GR, or full MTS.
