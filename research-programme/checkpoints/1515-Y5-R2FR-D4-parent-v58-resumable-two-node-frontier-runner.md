# 5499: D4 parent-v58 resumable two-node frontier runner

The checkpoint-5498 frontier is hash locked. The unchanged parent-v58 chain advances depth first, committing each completed node atomically and stopping after two nodes or an unresolved result.

- `R_E0S_E0S_E1S_X0S` -> `REFINED_X2` in `412.5375010999851` seconds; failure `global contour geometric denominator reaches zero: {"collision_jacobian": 0.0, "relative_root": 0.9945369405616719, "selected_global_root": 3.2196897089756438}`.
- `R_E0S_E0S_E1S_X0S_X0S` -> `REFINED_T2` in `430.04919689998496` seconds; failure `global contour geometric denominator reaches zero: {"collision_jacobian": 0.0, "relative_root": 0.9967177681791107, "selected_global_root": 3.221296373403036}`.

Frontier: `179/6/0`. Exact partition error: `0.0`. New v58 applications: `0`.

**PARENT_V58_TWO_NODE_FRONTIER_CERTIFIED__INTERPRET_NEXT_OBSTRUCTION**

Complete active-cuboid, full outer, event-local/combined W3, regulator-limit, all-operator local GR and full MTS claims remain open.
