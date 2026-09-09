# 5472: D4 parent-v52 collision-Jacobian leaf-union integration gate

## Derived enclosure law

For a compact finite cover `D = union_i D_i`, interval certificates `J(D_i) subset B_i` with `0 notin B_i` imply `inf_D |J| >= min_i dist(0,B_i) > 0`. Replacing the finite image union by one rectangular hull is sufficient but not necessary and can reintroduce zero between disconnected image boxes.

Parent v52 leaves the action, contour, configurations, residues and acceptance thresholds unchanged. It invokes a path-only leaf-union candidate only when every v51 collision-Jacobian candidate has zero lower bound. The interval hull is retained for diagnostics; the denominator uses the source-proved minimum over leaf images.

## Result

Previously unresolved target passes v52: `True`. Collision-Jacobian lower bound: `20.1217109261164`. Amplitude-denominator lower bound: `1.7395655362754908e-07`.

Untriggered passing control is unchanged: `True`. V52 fallback rows: `1`.

## Decision

**PARENT_V52_LEAF_UNION_ENCLOSURE_CERTIFIED__MIGRATE_RESUMABLE_FRONTIER**

## Claim boundary

This validates a stricter implementation of the existing finite-union theorem for collision-Jacobian enclosure. It does not yet migrate the complete checkpoint-5469 frontier or certify the active cuboid, full outer cover, W3, regulator limit, local GR or full MTS.
